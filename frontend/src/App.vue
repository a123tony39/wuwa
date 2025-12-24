<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import cardBack from './assets/card/background.png'
const tiltX = ref(0)
const tiltY = ref(0)
const selectedFile = ref<File | null>(null)
const imgSrc = ref<string | null>(null)
const isAnalyzing = ref(false)
const isCardMode = ref(false)
const isFlipped = ref(false)
const isDragging = ref(false)
// 檔案選擇
const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) selectedFile.value = target.files[0]
}

// 上傳圖片
const upload = async () => {
  if (!selectedFile.value) return
  isAnalyzing.value = true
  imgSrc.value = null
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    const res = await fetch("http://localhost:5000/api/process", {
      method: "POST",
      body: formData
    })
    const blob = await res.blob()
    imgSrc.value = URL.createObjectURL(blob)
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
}

const onMouseDown = (e: MouseEvent) => {
  e.preventDefault()
  isDragging.value = true
}
const onMouseUp = () => {
  if (!isDragging.value) return
  isDragging.value = false
  tiltX.value = 0
  tiltY.value = 0
  const front = document.querySelector('.card-front') as HTMLElement
  const back = document.querySelector('.card-back') as HTMLElement
  if (front) front.style.filter = 'brightness(1)'
  if (back) back.style.filter = 'brightness(1)'
}
onMounted(() => {
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
})
onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
})
// 滑鼠傾斜
const onMouseMove = (e: MouseEvent) => {
  if (!isDragging.value) return
  const card = document.querySelector('.card') as HTMLElement
  if (!card) return
  const front = document.querySelector('.card-front') as HTMLElement
  const back = document.querySelector('.card-back') as HTMLElement

  const rect = card.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  const maxTilt = 8

  tiltY.value = ((x - centerX) / centerX) * maxTilt
  tiltX.value = -((y - centerY) / centerY) * maxTilt

  // 卡片反光
  const lightX = (x - centerX) / centerX
  const lightY = (y - centerY) / centerY
  const brightness = 1 + lightX*0.2 - lightY*0.2
  if (!isFlipped.value && front) front.style.filter = `brightness(${brightness})`
  if (isFlipped.value && back) back.style.filter = `brightness(${brightness})`
}
</script>

<template>
  <header class="header">
    <h1>聲骸分析工具</h1>
    <p>上傳圖片，自動分析並產出分析結果圖</p>
  </header>

  <main class="page">
    <section class="workspace">

      <div v-if="!isAnalyzing && !imgSrc" class="panel">
        <input type="file" @change="onFileChange" />
        <button @click="upload" :disabled="!selectedFile">上傳圖片</button>
      </div>

      <div v-else-if="isAnalyzing" class="panel">
        <p class="loading">分析中... 請稍後</p>
      </div>

      <div v-else-if="imgSrc" class="panel">
        <img
          v-if="!isCardMode"
          :src="imgSrc"
          class="initial-img"
          @click="isCardMode=true; isFlipped=false"
        />

        <div v-else class="card-container">
          <div class="page-overlay" @click="isCardMode=false; isFlipped=false"></div>
          <div
            class="card"
            draggable="false"
            @mousedown="onMouseDown"
            @mouseup="onMouseUp"
            @click="isFlipped=!isFlipped"
            :style="{
              transform: `rotateX(${tiltX}deg) rotateY(${tiltY}deg) ${isFlipped ? 'rotateY(180deg)' : ''}`
            }"
          >
            <div class="card-face card-front">
              <img :src="imgSrc" alt="預覽圖" />
            </div>
            <div class="card-face card-back"
              :style="{ backgroundImage: `url(${cardBack})` }"
            ></div>
          </div>

        </div>  
        <div class="actions" v-if="imgSrc">
          <a :href="imgSrc" download="processed.png">
            <button>下載圖片</button>
          </a>
          <button @click="reset">再來一次</button>
        </div>
      </div>

    </section>
  </main>
</template>

<style scoped>
.header { text-align:center; margin-bottom:16px }
.page { min-height:100vh; display:flex; justify-content:center; align-items:flex-start; padding:1px }
.workspace { display:flex; flex-direction:column; align-items:center; padding:0; }

.panel { display:flex; flex-direction:column; gap:8px; align-items:center }
.initial-img { width:300px; cursor:pointer }

/* 卡片容器 */
.card-container {
  perspective: 800px;
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: radial-gradient(circle at center, #333 0%, #111 100%);
  z-index: 1001;
}

/* 卡片 */
.card {
  width: 320px;
  height: 450px;
  z-index: 2;
  transform-style: preserve-3d;
  transition: transform 0.15s ease; /* 滑鼠傾斜快速 */
  cursor: pointer;
}

/* 卡片翻轉 */
.card-face {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}
.card-face img { width: 100%; height: 100%; object-fit: contain }
.card-front { transform: rotateY(0deg) }
.card-back {
  position: absolute;
  inset: 0;

  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

  transform: rotateY(180deg);
  backface-visibility: hidden;
}
.back-content { padding:24px; text-align:center }

.page-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0); /* 半透明黑色 */
  z-index: 1; /* 卡片 z-index 高於 overlay */
}

/* 按鈕 */
button { padding:10px 16px; border-radius:8px; border:1px solid #ddd; background:#fff; cursor:pointer }
button:hover:not(:disabled) { background:#f5f5f5; border-color:#ccc }
button:disabled { opacity:.5; cursor:not-allowed }

.actions { display:flex; gap:12px; margin-top:16px; position:relative; z-index:10 }
.loading { font-size:15px; color:#666 }
</style>
