<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import UploadPanel from './components/UploadPanel.vue'
import CardDisplay from './components/CardDisplay.vue'
import RuleExplanation from './components/RuleExplanation.vue'
import ResultExplanation from './components/ResultExplanation.vue'
import BackgroundUploader from './components/BackgroundUploader.vue'
const selectedFile = ref<File | null>(null)
const backgroundFile = ref<File | null>(null)    // 背景圖片
const imgSrc = ref<string | null>(null)
const isAnalyzing = ref(false)
const isCardMode = ref(false)
const isFlipped = ref(false)
const previewUrl = ref<string | null>(null)
const analysisResult = ref<any>(null)
// 上傳圖片

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
        <BackgroundUploader
          v-if="!isAnalyzing && !imgSrc"
          :backgroundFile = "backgroundFile"
          @update:BackgroundFile = "backgroundFile = $event"
        />
          
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
  padding: 12px 12px;
}
.side {
  background: #d6dae25b;
  border-radius: 16px;
  padding: 20px;
  font-size: 12px;
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

</style>
