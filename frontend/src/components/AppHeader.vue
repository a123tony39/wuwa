<script setup lang="ts">

const props = defineProps<{
  title: string
  subtitle?: string
}>()
</script>

<template>
  <header class="header">
    <h1>{{ props.title }}</h1>
    <p v-if="props.subtitle">{{ props.subtitle }}</p>
  </header>
</template>

<style scoped>
.header { 
  text-align: center; 
  font-size: 14px;
  border-bottom: 2px solid #E5E7EB;
}
.header p{
  font-size: 14px;
}
</style>