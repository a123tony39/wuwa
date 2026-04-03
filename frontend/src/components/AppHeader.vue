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
  color: #1E1E2F;
  font-size: 14px;
  gap: 6px;
}

.header p{
  font-size: 16px;
}
</style>