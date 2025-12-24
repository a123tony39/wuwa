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
  margin-bottom: 16px;
  font-size: larger;
}
.header p{
  font-size: large;
}
</style>