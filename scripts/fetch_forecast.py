"""Fetch latest MeteoSwiss forecast data and synoptic chart."""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import google.generativeai as genai
import requests

BASE_URL = "https://www.meteoswiss.admin.ch/product/output"
OUTPUT_DIR = Path("public/data")


def get_versions():
    """Fetch versions.json (flat key→version dict)."""
    resp = requests.get(f"{BASE_URL}/versions.json", timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_text(url):
    """Fetch xhtml and extract text content."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.texts = []

        def handle_data(self, data):
            stripped = data.strip()
            if stripped:
                self.texts.append(stripped)

    parser = TextExtractor()
    parser.feed(resp.text)
    return "\n".join(parser.texts)


def fetch_image(url, filename):
    """Download image to output directory."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / filename).write_bytes(resp.content)


def translate_with_gemini(text, api_key):
    """Translate German meteorological text to English using Gemini."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    prompt = (
        "Translate the following German weather forecast text to English. "
        "Preserve paragraph structure. Only output the translation, nothing else.\n\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    return response.text.strip()


def main():
    import os

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    print("Fetching versions.json...")
    versions = get_versions()

    # Extract version timestamps (flat keys)
    wr_version = versions["weather-report/de/north"]
    gs_version = versions["generalsituation/text/de"]
    gs_map_version = versions["generalsituation/map/de"]

    print(f"Weather report version: {wr_version}")
    print(f"General situation version: {gs_version}")
    print(f"Synoptic map version: {gs_map_version}")

    # Fetch texts
    wr_url = (
        f"{BASE_URL}/weather-report/de/north/version__{wr_version}/textproduct_de.xhtml"
    )
    gs_url = f"{BASE_URL}/generalsituation/text/de/version__{gs_version}/textproduct_de.xhtml"
    map_url = f"{BASE_URL}/generalsituation/map/de/version__{gs_map_version}/generalsituation_frontmap_de.png"

    print("Fetching weather report...")
    weather_report_de = fetch_text(wr_url)

    print("Fetching general situation...")
    general_situation_de = fetch_text(gs_url)

    print("Fetching synoptic chart...")
    fetch_image(map_url, "synoptic_chart.png")

    # Translate
    print("Translating weather report...")
    weather_report_en = translate_with_gemini(weather_report_de, api_key)

    print("Translating general situation...")
    general_situation_en = translate_with_gemini(general_situation_de, api_key)

    # Build output
    # Parse timestamp from version string (e.g., "20260609_0735")
    ts_match = re.match(r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})", wr_version)
    if ts_match:
        y, mo, d, h, mi = ts_match.groups()
        timestamp = f"{y}-{mo}-{d}T{h}:{mi}:00Z"
    else:
        timestamp = wr_version

    forecast = {
        "timestamp": timestamp,
        "version": wr_version,
        "weatherReport": {"de": weather_report_de, "en": weather_report_en},
        "generalSituation": {"de": general_situation_de, "en": general_situation_en},
        "synopticChartUrl": "data/synoptic_chart.png",
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "forecast.json").write_text(
        json.dumps(forecast, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Done! Output written to public/data/")


if __name__ == "__main__":
    main()
