<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import UploadPanel from './components/UploadPanel.vue'
import CardDisplay from './components/CardDisplay.vue'
import RuleExplanation from './components/RuleExplanation.vue'
import ResultExplanation from './components/ResultExplanation.vue'
const selectedFile = ref<File | null>(null)
const backgroundFile = ref<File | null>(null)    // 背景圖片
const imgSrc = ref<string | null>(null)
const isAnalyzing = ref(false)
const isCardMode = ref(false)
const isFlipped = ref(false)
const previewUrl = ref<string | null>(null)
const analysisResult = ref<any>(null)
// 上傳圖片
const onBackgroundChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0] ?? null  // undefined 轉成 null
  backgroundFile.value = file
}
const upload = async () => {
  if (!selectedFile.value) return
  isAnalyzing.value = true
  imgSrc.value = null
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    if (backgroundFile.value) {
      formData.append('background', backgroundFile.value)  // 新增背景檔案
    }
    const res = await fetch("/api/process", {
      method: "POST",
      body: formData
    })
    const data = await res.json()
    imgSrc.value = "data:image/png;base64," + data.image_base64
    analysisResult.value = data.result
  } catch(err) {
    console.error(err)
    alert("分析失敗")
  } finally {
    isAnalyzing.value = false
  }
}
// 重置
const reset = () => {
  selectedFile.value = null
  imgSrc.value = null
  isCardMode.value = false
  isFlipped.value = false
  previewUrl.value = null
}

</script>
<template>
  <AppHeader title = "聲骸分析工具" subtitle = "上傳圖片，自動分析並產出結果圖" />
  <main class="page">
    <section class="layout">
      <!-- 左：規則說明 -->
      <aside class="side left">
        <RuleExplanation />
      </aside>
      <section class="workspace">
        <UploadPanel 
          :isAnalyzing = "isAnalyzing"
          :imgSrc = "imgSrc"
          :previewUrl = "previewUrl"
          :hasFile="!!selectedFile"
          @fileSelected = "selectedFile = $event"
          @update:previewUrl = "previewUrl = $event"
          @upload= "upload"
        />
        <!-- 新增背景上傳 -->
        <div
          v-if="!isAnalyzing && !imgSrc"
          class="optional-setting"
        >
          <label class="optional-title">
            進階設定（可選）
          </label>

          <label class="bg-upload">
            自訂背景圖片
            <input
              type="file"
              accept="image/png, image/jpeg"
              @change="onBackgroundChange"
              hidden
            />
          </label>

          <span v-if="backgroundFile" class="file-hint">
            已選擇：{{ backgroundFile.name }}
          </span>
        </div>      
        <CardDisplay
          :imgSrc="imgSrc"
          :isCardMode="isCardMode"
          :isFlipped="isFlipped"
          @update:isCardMode="isCardMode = $event"
          @update:isFlipped="isFlipped = $event"
          @reset="reset"
        />
      </section>
      <!-- 右：結果說明 -->
      <aside class="side right">
        <ResultExplanation
          :imgSrc="imgSrc"
          :isAnalyzing="isAnalyzing"
          :result="analysisResult"
        />
      </aside>
    </section>
  </main>
  <div v-if="imgSrc" class="actions">
    <a :href="imgSrc" download="processed.png">
      <button>下載圖片</button>
    </a>
    <button @click="reset">再來一次</button>
  </div>
</template>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 24px;
}
.side {
  background: #fafafa;
  border-radius: 12px;
  padding: 20px;
  font-size: 14px;
  line-height: 1.6;
}

.page {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.workspace { 
  display:flex; 
  flex-direction:column; 
  align-items:center; 
  justify-content: center;
}
button { 
  padding:10px 16px; 
  border-radius:8px; 
  border:1px solid #ddd; 
  background:#fff; 
  cursor:pointer 
}

.actions { 
  display:flex; 
  gap:12px; 
  margin-top:16px; 
  position:relative; 
  align-items:center; 
  justify-content: center;
}

.optional-setting {
  margin-top: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  background: #f6f7f8;
  width: 100%;
  max-width: 420px;
  font-size: 13px;
}

.optional-title {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #555;
}
.bg-upload {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px dashed #bbb;
  cursor: pointer;
  color: #333;
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
