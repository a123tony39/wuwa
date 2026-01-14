<script setup lang = "ts">
import { ref } from "vue"
const props = defineProps<{
    isAnalyzing: boolean
    imgSrc: string | null
    previewUrl: string | null
    hasFile: boolean
}>()
const emit = defineEmits<{
  (e: 'fileSelected', file: File): void
  (e: 'upload'): void
  (e: 'update:previewUrl', url: string | null): void

}>()
const fileInputRef = ref<HTMLInputElement | null>(null)

const onPaste = (e: ClipboardEvent) => {
  const items = e.clipboardData?.items
  if (!items) return

  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (!item) continue
    if (item.type.indexOf('image') !== -1) {
      const file = item.getAsFile()
      if (file) {
        emit('update:previewUrl', URL.createObjectURL(file))  // 生成預覽
        emit('fileSelected', file)
      }
    }
  }
}

// 檔案選擇
const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    emit('update:previewUrl', URL.createObjectURL(target.files[0]))
    emit('fileSelected', target.files[0])
  }
}

// 點擊自訂按鈕觸發檔案選擇
const triggerFileSelect = () => {
  fileInputRef.value?.click()
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
        <!-- 自訂上傳按鈕 -->
        <div class="upload-controls">
          <input 
            type="file" 
            ref="fileInputRef" 
            @change="onFileChange" 
            style="display: none;" 
            accept="image/*"
          />
            <button class="file-btn" @click="triggerFileSelect">
              選擇圖片
            </button>
            <button 
              class="analyze-btn" 
              @click="emit('upload')" 
              :disabled="!props.hasFile"
            >
              開始分析
            </button>
          </div>
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
  display: flex;
  justify-content: center;
  align-items: center;
  width: auto;
  height: auto;
  min-width: 250px;
  min-height: 150px;
  max-width: 600px;
  max-height: 400px;
  border: 2px dashed #bbb;
  border-radius: 12px;
  background-color: #fafafa;
  color: #999;
  cursor: pointer;
  overflow: hidden;
  text-align: center;
  padding: 4px;
}
.paste-area:focus {
  outline: none;
  border-color: #888;
  color: #666;
}
/* 貼上圖片預覽 */
.paste-area img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.upload-controls {
  display: flex;
  gap: 12px;
  justify-content: center;
}
/* 選擇檔案按鈕 */
.file-btn {
  padding: 10px 18px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}
.file-btn:hover {
  background-color: #f0f0f0;
  border-color: #bbb;
  box-shadow: 0 4px 8px rgba(0,0,0,0.12);
}

/* 分析按鈕 */
.analyze-btn {
  padding: 10px 22px;
  background: linear-gradient(135deg, #4f9fff, #1c64f2);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  box-shadow: 0 4px 10px rgba(31, 102, 231, 0.3);
}
.analyze-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #1c64f2, #4f9fff);
  box-shadow: 0 6px 14px rgba(31, 102, 231, 0.4);
}
.analyze-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}
</style>