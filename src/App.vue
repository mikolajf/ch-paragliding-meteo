<script setup>
import { ref, onMounted, computed } from 'vue'
import ForecastCard from './components/ForecastCard.vue'
import SynopticChart from './components/SynopticChart.vue'
import DabsPanel from './components/DabsPanel.vue'

const forecast = ref(null)
const error = ref(null)
const loading = ref(true)

const BASE = import.meta.env.BASE_URL

const isStale = computed(() => {
  if (!forecast.value) return false
  const age = Date.now() - new Date(forecast.value.timestamp).getTime()
  return age > 7 * 60 * 60 * 1000
})

const today = computed(() => new Date().toISOString().slice(0, 10))
const tomorrow = computed(() => {
  const d = new Date()
  d.setDate(d.getDate() + 1)
  return d.toISOString().slice(0, 10)
})

const dabsUrl = (date) =>
  `https://www.skybriefing.com/de/dabs?p_p_id=ch_skyguide_ibs_portal_dabs_DabsUI&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=APP&p_p_cacheability=cacheLevelPage&_ch_skyguide_ibs_portal_dabs_DabsUI_v-resourcePath=%2FAPP%2Fconnector%2F0%2F2%2Fhref%2Fdabs-${date}.pdf`

onMounted(async () => {
  try {
    const res = await fetch(`${BASE}data/forecast.json`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    forecast.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-blue-700 text-white py-4 px-6 shadow">
      <h1 class="text-2xl font-bold">CH Paragliding Meteo</h1>
    </header>

    <main class="max-w-4xl mx-auto p-4 space-y-6 mt-6">
      <p v-if="loading" class="text-center text-gray-500">Loading forecast…</p>
      <p v-else-if="error" class="text-center text-red-600">Failed to load forecast: {{ error }}</p>

      <template v-else-if="forecast">
        <p v-if="isStale" class="text-amber-600 text-sm text-center">
          ⚠ Data may be outdated (last updated: {{ new Date(forecast.timestamp).toLocaleString() }})
        </p>
        <p v-else class="text-gray-500 text-sm text-center">
          Updated: {{ new Date(forecast.timestamp).toLocaleString() }}
        </p>

        <SynopticChart :src="`${BASE}${forecast.synopticChartUrl}`" />
        <ForecastCard title="General Situation" :de="forecast.generalSituation.de" :en="forecast.generalSituation.en" />
        <ForecastCard title="Weather Report" :de="forecast.weatherReport.de" :en="forecast.weatherReport.en" />
      </template>

      <DabsPanel :title="`DABS Today (${today})`" :url="dabsUrl(today)" />
      <DabsPanel :title="`DABS Tomorrow (${tomorrow})`" :url="dabsUrl(tomorrow)" />
    </main>

    <footer class="text-center text-xs text-gray-400 py-6">
      Data source: <a href="https://www.meteoswiss.admin.ch/" class="underline">MeteoSwiss</a>
    </footer>
  </div>
</template>
