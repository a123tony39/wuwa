<script setup lang = "ts">
import { ref } from "vue"
const props = defineProps<{
    isAnalyzing: boolean
    imgSrc: string | null
}>()
const emit = defineEmits<{
  (e: 'fileSelected', file: File): void
  (e: 'upload'): void
}>()

const selectedFile = ref<File | null>(null)
// 檔案選擇
const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
    emit('fileSelected', selectedFile.value)
  }
}
// 上傳按鈕觸發
const onUploadClick = () => {
    if (!selectedFile.value) return
    emit('upload')
}

</script>

<template>
    <div class = "panel">
        <!-- 尚未選擇圖片 -->
        <div v-if = "!props.isAnalyzing && !props.imgSrc">
            <input type="file" @change="onFileChange"/>
            <button @click="onUploadClick" :disabled="!selectedFile">上傳圖片</button>
         </div>
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
.loading {
  font-size: 15px;
  color: #666;
}
button {
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
}
button:hover:not(:disabled) {
  background: #f5f5f5;
  border-color: #ccc;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>