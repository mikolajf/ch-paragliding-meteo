<script setup>
import { ref } from 'vue'

defineProps({ title: String, url: String })
const open = ref(false)
</script>

<template>
  <section class="bg-white rounded-lg shadow">
    <button @click="open = !open" class="w-full flex justify-between items-center p-6 text-left">
      <h2 class="text-xl font-semibold">{{ title }}</h2>
      <span class="text-gray-400 text-2xl">{{ open ? '−' : '+' }}</span>
    </button>
    <div v-if="open" class="px-6 pb-6">
      <iframe :src="url" class="w-full h-[80vh] border rounded"></iframe>
    </div>
  </section>
</template>
