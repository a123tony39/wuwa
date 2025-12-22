<script setup lang="ts">
  import { ref } from 'vue'
  import UploadImage from './components/UploadImage.vue'

  const result = ref<any>(null)
  const imgSrc = ref<string | null>(null)

  const upload = async (e: Event) => {
    const input = e.target as HTMLInputElement
    const files = input.files
    if(!files || files.length === 0) return
    const file = files[0]
    const formData = new FormData()
    formData.append("file", file)

    const res = await fetch("http://localhost:5000/api/process", {
      method: "POST",
      body: formData
    })
    const data = await res.json()
    result.value = data
    if (data.image_base64) {
      imgSrc.value = `data:image/png;base64,${data.image_base64}`
    }

}
</script>

<!-- <template>
  <HealthCheck />
</template> -->

<template>
  <input type = "file" @change ="upload" />
  <pre>{{ result }}</pre>
  <!-- 顯示 base64 圖片 -->
  <img v-if="imgSrc" :src="imgSrc" alt="處理後圖片" />
   <!-- 下載按鈕 -->
  <a v-if="imgSrc" :href="imgSrc" download="processed.png">
    <button>下載圖片</button>
  </a>
</template>

<style scoped>
h1 {
  font-size: 32px;
}
</style>