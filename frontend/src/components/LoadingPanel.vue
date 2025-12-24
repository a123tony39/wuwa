<script setup lang = "ts">
import { ref } from "vue"

const props = defineProps<{
    isAnalyzing : boolean
}>()
</script>

<template>
    <div class = "panel">
          <!-- 分析中 -->
        <div v-if = "props.isAnalyzing">
            <p class="loading">分析中... 請稍後</p>
        </div>
    </div>
</template>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}
</style>