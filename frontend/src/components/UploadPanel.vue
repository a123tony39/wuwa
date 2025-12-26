<script setup lang = "ts">
import { ref, onMounted, onUnmounted } from "vue"
const props = defineProps<{
    isAnalyzing: boolean
    imgSrc: string | null
}>()
const emit = defineEmits<{
  (e: 'fileSelected', file: File): void
  (e: 'upload'): void
}>()
onMounted(() => {
  window.addEventListener('paste', onPaste)
})

onUnmounted(() => {
  window.removeEventListener('paste', onPaste)
})
const previewUrl = ref<string | null>(null)
const onPaste = (e: ClipboardEvent) => {
  const items = e.clipboardData?.items
  if (!items) return

  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (!item) continue
    if (item.type.indexOf('image') !== -1) {
      const file = item.getAsFile()
      if (file) {
        selectedFile.value = file
        previewUrl.value = URL.createObjectURL(file)  // 生成預覽
        emit('fileSelected', file)
      }
    }
  }
}
const selectedFile = ref<File | null>(null)
// 檔案選擇
const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
    previewUrl.value = URL.createObjectURL(target.files[0])
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
            <!-- 可貼圖片區 -->
            <div 
              class="paste-area" 
              @paste="onPaste"
              tabindex="0"
            >
              <template v-if="previewUrl">
                <img :src="previewUrl" alt="預覽圖片">
              </template>
              <template v-else>
                點擊此區域並貼上圖片
              </template>
            </div>
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
  justify-content: center;
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

/*paste area*/
.paste-area {
  display: flex; /* 改回 flex，避免變成 inline 行內元素 */
  width: auto;   /* 自動跟圖片大小適應 */
  height: auto;  /* 自動跟圖片大小適應 */
  min-width: 250px;        /* 最小寬度 */
  min-height: 180px;       /* 最小高度 */
  max-width: 600px;        /* 最大寬度 */
  max-height: 400px;       /* 最大高度 */
  border: 2px dashed #aaa;
  border-radius: 12px;
  justify-content: center;
  align-items: center;
  color: #999;
  background-color: #f9f9f9;
  cursor: pointer;
  text-align: center;
  overflow: hidden;
  padding: 4px;
}
.paste-area:focus {
  outline: none;
  border-color: #666;
  color: #666;
}

/* 貼上圖片預覽 */
.paste-area img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

</style>