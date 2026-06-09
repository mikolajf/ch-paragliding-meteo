<script setup>
defineProps({ src: String })
</script>

<template>
  <section class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-semibold mb-4">Synoptic Chart</h2>
    <img :src="src" alt="Synoptic weather chart" class="w-full rounded" />
  </section>
</template>
