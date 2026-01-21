<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import UploadPanel from './components/UploadPanel.vue'
import CardDisplay from './components/CardDisplay.vue'
import RuleExplanation from './components/RuleExplanation.vue'
import ResultExplanation from './components/ResultExplanation.vue'
import BackgroundUploader from './components/BackgroundUploader.vue'

const selectedFile = ref<File | null>(null)
const backgroundFile = ref<File | null>(null)
const imgSrc = ref<string | null>(null)
const isAnalyzing = ref(false)
const isCardMode = ref(false)
const isFlipped = ref(false)
const previewUrl = ref<string | null>(null)
const analysisResult = ref<any>(null)
const hasEntered = ref(false)

const enter = () => {
  hasEntered.value = true
}

const upload = async () => {
  if (!selectedFile.value) return
  isAnalyzing.value = true
  imgSrc.value = null
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    if (backgroundFile.value) {
      formData.append('background', backgroundFile.value)
    }
    const res = await fetch('/api/process', {
      method: 'POST',
      body: formData
    })
    const data = await res.json()
    imgSrc.value = 'data:image/png;base64,' + data.image_base64
    analysisResult.value = data.result
  } catch (err) {
    console.error(err)
    alert('分析失敗')
  } finally {
    isAnalyzing.value = false
  }
}

const reset = () => {
  selectedFile.value = null
  imgSrc.value = null
  isCardMode.value = false
  isFlipped.value = false
  previewUrl.value = null
}
</script>

<template>
  <!-- Entry Overlay -->
  <Transition name="fade">
    <div 
      v-if="!hasEntered"
      class="entry-overlay"
      @click="enter"
    >
      <!-- 背景影片 -->
      <video 
        class="entry-video-bg" 
        autoplay 
        loop 
        muted 
        playsinline
      >
        <source src="/1.mp4" type="video/mp4" />
      </video>

      <div class="entry-content">
        <h1>聲骸分析</h1>
        <p>上傳圖片，自動分析並產出結果</p>
        <span class="hint">點擊任意處開始</span>
      </div>
    </div>
  </Transition>
  <!-- Main App -->
  <AppHeader title="聲骸分析工具" subtitle="上傳圖片，自動分析並產出結果圖" />

  <main class="page">
    <section class="layout">
      <aside class="side left">
        <RuleExplanation />
      </aside>

      <section class="workspace">
        <UploadPanel
          :isAnalyzing="isAnalyzing"
          :imgSrc="imgSrc"
          :previewUrl="previewUrl"
          :hasFile="!!selectedFile"
          @fileSelected="selectedFile = $event"
          @update:previewUrl="previewUrl = $event"
          @upload="upload"
        />

        <BackgroundUploader
          v-if="!isAnalyzing && !imgSrc"
          :backgroundFile="backgroundFile"
          @update:BackgroundFile="backgroundFile = $event"
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
/* =====================
   Base Reset
===================== */
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

/* =====================
   Desktop layout
===================== */
.page {
  display: flex;
  flex-direction: column;
}

.layout {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 12px 12px;
}

.workspace {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.side {
  background: #d6dae25b;
  color: #222;
  border-radius: 16px;
  padding: 20px;
  font-size: 12px;
  line-height: 1.6;
}

/* =====================
   Actions
===================== */
.actions {
  display: flex;
  gap: 12px;
  margin: 16px 0;
  justify-content: center;
}

button {
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
}

/* =====================
   Mobile layout
===================== */
@media (max-width: 768px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .workspace {
    order: 1;
  }

  .side.right {
    order: 2;
    max-width: none;
  }

  .side.left {
    order: 3;
  }
}

/* =====================
   Entry Overlay
===================== */
.entry-overlay {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden; /* 避免溢出 */
  background-color: rgba(0,0,0);
}

.entry-video-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持比例填滿 */
  z-index: 0;
  filter: blur(12px); /* 初始模糊 */
  transition: filter 0.4s ease;
}

.entry-overlay:hover .entry-video-bg {
  filter: blur(0); /* 滑鼠 hover 變清晰 */
}

.entry-content {
  position: relative;
  text-align: center;
  color: #fff;
  z-index: 10;
  pointer-events: none; /* 文字不阻擋 hover */
  animation: floatIn 0.8s ease forwards;
}

.entry-content h1 {
  font-size: 28px;
  letter-spacing: 2px;
  margin-bottom: 12px;
}

.entry-content p {
  font-size: 14px;
  opacity: 0.85;
}

.entry-content .hint {
  display: block;
  margin-top: 32px;
  font-size: 12px;
  opacity: 0.6;
}

/* =====================
   文字浮入動畫
===================== */
@keyframes floatIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Transition fade */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.8s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
}
</style>
