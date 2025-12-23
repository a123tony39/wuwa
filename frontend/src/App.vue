<script setup lang="ts">
  import { ref } from 'vue'
  const selectedFile = ref<File | null>(null)
  const imgSrc = ref<string | null>(null)
  const isAnalyzing = ref(false)

  const onFileChange = async (e: Event) => {
    const target = e.target as HTMLInputElement
    if (target.files && target.files[0]) {
      selectedFile.value = target.files[0]
    }
  }
  const upload = async () =>{
    if (!selectedFile.value) return

    isAnalyzing.value = true
    imgSrc.value = null

    try{
      const formData = new FormData()
      formData.append('file', selectedFile.value)
      const res = await fetch("http://localhost:5000/api/process", {
        method: "POST",
        body: formData
      })
      const blob = await res.blob()
      imgSrc.value = URL.createObjectURL(blob)
    }catch(err){
      console.error(err)
      alert("分析失敗")
      }finally{
      isAnalyzing.value = false
    }
}
</script>

<template>
  <header class = "header">
    <h1>聲骸分析工具</h1>
  <p>上傳圖片，自動分析並產出分析結果圖</p>
    </header>
  <main class = "page">
    <section class = "workspace">
      <!-- 狀態1: 尚未上傳-->
      <div v-if = "!isAnalyzing && !imgSrc" class = "panel">
        <input type = "file" @change = "onFileChange" />
        <button @click="upload" :disabled="!selectedFile">
          上傳圖片
        </button>
      </div>

      <!-- 狀態2: 分析中-->
      <div v-else-if = "isAnalyzing" class = "panel">
        <p class = "loading">❤️❤️❤️正在分析中... 請稍後❤️❤️❤️</p>
      </div>

      <!-- 狀態3: 產生結果-->
      <div v-else-if = "imgSrc" class="panel">
        <div class = "preview">
          <img :src = "imgSrc" alt="處理後圖片"/>
        </div>

        <div class = "actions">
          <a :href="imgSrc" download="processed.png">
            <button>下載圖片</button>
          </a>
          <button @click="selectedFile=null; imgSrc = null">
            再來一次
          </button>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
/* ===== 全域文字 ===== */
.header h1 {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.header p {
  font-size: 13px;
  color: #777;
  margin-top: 4px;
}

/* ===== Header ===== */
.header {
  max-width: 420px;
  margin: 0 auto 16px; /* ⬅ 底部留空間 */
  text-align: center;    
}
/* ===== 頁面背景 ===== */
.page {
  min-height: 100vh;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  padding: 1px;
  box-sizing: border-box;
}


/* ===== working space ===== */
.workspace {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 32px 24px;

  border: 1px solid #e0e0e0; 
  box-shadow: 0 4px 16px rgba(0,0,0,0.08); 
}

/* ===== Panel ===== */
.panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
}

/* ===== 圖片預覽 ===== */
.preview {
  background-color: #3f3a3a;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
}

.preview img {
  width: 260px;
  height: auto;
  image-rendering: pixelated;
  display: block;
}

/* ===== 按鈕 ===== */
button {
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background-color: #fff;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.15s ease, border-color 0.15s ease;
}

button:hover:not(:disabled) {
  background-color: #f5f5f5;
  border-color: #ccc;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ===== 操作區 ===== */
.actions {
  display: flex;
  gap: 12px;
}

/* ===== 分析中 ===== */
.loading {
  font-size: 15px;
  color: #666;
}
</style>