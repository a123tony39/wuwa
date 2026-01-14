<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'update:BackgroundFile', file: File | null): void
}>()

const backgroundFile = ref<File | null>(null)
const previewUrl = ref<string | null>(null)


// 按鈕選檔
const onBackgroundChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0] ?? null
  setBackground(file)
}

// 貼圖區域貼上圖片
const onPaste = (e: ClipboardEvent) => {
  const items = e.clipboardData?.items
  if (!items) return
  for (const item of items) {
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile()
      if (file) setBackground(file) // 直接更新背景
      break
    }
  }
}

// 更新背景圖片
const setBackground = (file: File | null) => {
  backgroundFile.value = file
  previewUrl.value = file ? URL.createObjectURL(file) : null
  emit('update:BackgroundFile', file)
}
</script>

<template>
  <div class="optional-setting">
    <label class="optional-title">背景圖片 (可選)</label>

    <!-- 貼圖區域，只能貼上 -->
    <div class="paste-box" tabindex="0" @paste="onPaste">
      <template v-if="previewUrl">
        <img :src="previewUrl" alt="預覽圖片" class="preview-img" />
      </template>
      <template v-else>
        點擊並貼上背景圖片
      </template>
    </div>

    <!-- 選擇檔案按鈕 -->
    <label class="bg-upload">
      選擇背景圖片
      <input 
        type="file" 
        accept="image/png, image/jpeg"
        ref="fileInputRef"
        @change="onBackgroundChange"
        hidden
      />
    </label>

    <!-- 顯示已選檔案 -->
    <span v-if="backgroundFile" class="file-hint">
      已選擇: {{ backgroundFile.name }}
    </span>
  </div>
</template>

<style scoped>
.optional-setting {
  margin-top: 12px;
  font-size: 13px;
  background-color: #d6dae25b;
  padding: 10px;
  border-radius: 12px;
}

.optional-title {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  color: #555;
}

/* 貼圖區域，只貼上 */
.paste-box {
  width: 250px;
  height: 80px;
  border: 2px dashed #bbb;
  border-radius: 8px;
  background-color: #fafafa;
  color: #999;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  overflow: hidden;
  font-size: 12px;
  user-select: none;
}
.paste-box:focus {
  border-color: #888;
  color: #666;
  outline: none;
}

.preview-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.bg-upload {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px dashed #bbb;
  cursor: pointer;
  color: #333;
  margin-top: 4px;
}
.bg-upload:hover {
  background: #eee;
}

.file-hint {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #666;
}
</style>
