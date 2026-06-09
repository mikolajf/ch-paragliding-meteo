<script setup>
defineProps({ title: String, url: String })
</script>

<template>
  <section class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-semibold mb-2">{{ title }}</h2>
    <a :href="url" target="_blank" rel="noopener" class="text-blue-600 underline hover:text-blue-800">
      Open PDF ↗
    </a>
  </section>
</template>
