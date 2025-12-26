<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import UploadPanel from './components/UploadPanel.vue'
import CardDisplay from './components/CardDisplay.vue'

const selectedFile = ref<File | null>(null)
const imgSrc = ref<string | null>(null)
const isAnalyzing = ref(false)
const isCardMode = ref(false)
const isFlipped = ref(false)

// 上傳圖片
const upload = async () => {
  if (!selectedFile.value) return
  isAnalyzing.value = true
  imgSrc.value = null
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    const res = await fetch("/api/process", {
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

</script>

<template>
  <AppHeader title = "聲骸分析工具" subtitle = "上傳圖片，自動分析並產出結果圖" />
  <main class="page">
    <section class="workspace">
      <UploadPanel 
        :isAnalyzing = "isAnalyzing"
        :imgSrc = "imgSrc"
        @fileSelected = "selectedFile = $event"
        @upload= "upload"
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
  </main>
  <div v-if="imgSrc" class="actions">
    <a :href="imgSrc" download="processed.png">
      <button>下載圖片</button>
    </a>
    <button @click="reset">再來一次</button>
  </div>

</template>


<style scoped>
.page {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.workspace { 
  display:flex; 
  flex-direction:column; 
  align-items:center; 
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
