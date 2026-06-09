<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps({ title: String, de: String, en: String })

const enHtml = computed(() => marked(props.en || ''))
</script>

<template>
  <section class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-semibold mb-4">{{ title }}</h2>
    <div class="grid md:grid-cols-2 gap-4">
      <div>
        <h3 class="text-sm font-medium text-gray-500 mb-1">Deutsch</h3>
        <p class="text-gray-800 whitespace-pre-line">{{ de }}</p>
      </div>
      <div>
        <h3 class="text-sm font-medium text-gray-500 mb-1">English</h3>
        <div class="text-gray-800 prose prose-sm" v-html="enHtml"></div>
      </div>
    </div>
  </section>
</template>
