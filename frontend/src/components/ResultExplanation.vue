<script setup lang="ts">
const props = defineProps<{
  imgSrc: string | null,
  isAnalyzing: Boolean,
  result: any, 
}>()
</script>
<template>
  <div>
    <h3>分析結果</h3>

    <p v-if="!imgSrc && !isAnalyzing">
      上傳圖片後，這裡會顯示分析說明
    </p>

    <p v-if="isAnalyzing">
      分析中，請稍候…
    </p>

    <div v-if="imgSrc && result">
      <p>評分等級：<strong>{{ result.rank }}</strong></p>
      <p>總分：{{ Number(result.score).toFixed(2) }}</p>

      <h4>聲骸評分</h4>
      <ul class="echo-list">
        <li v-for="(echo, i) in result.echo_results" :key="i">
            {{ echo.name }} (分數: {{ Number(echo.score).toFixed(2) }}) - {{ echo.message }}
        </li>
      </ul>
    </div>
  </div>
</template>
<style scoped>
.echo-list {
  text-align: left;   /* 文字靠左 */
  padding-left: 20px;  /* ul 的內縮 */
  list-style-position: inside;  /* 避免 bullet 被裁切 */
}
</style>