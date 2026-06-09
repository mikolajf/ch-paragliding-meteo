<script setup>
defineProps({ title: String, de: String, en: String })
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
        <p class="text-gray-800 whitespace-pre-line">{{ en }}</p>
      </div>
    </div>
  </section>
</template>
