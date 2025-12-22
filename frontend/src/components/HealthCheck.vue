<script setup lang = "ts">
    import { ref } from "vue"
    import { fetchHealth } from "../api/health"
    const result = ref<any>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)
    const run = async () => {
        loading.value = true
        try {
            result.value = await fetchHealth()
        } catch (err: any) {
            error.value = err.message
        } finally {
            loading.value = false
        }
    }
</script>

<template>
  <div>
    <button @click="run">測試 API</button>

    <p v-if="loading">載入中...</p>
    <p v-if="error" style="color:red">錯誤：{{ error }}</p>

    <pre v-if="result">{{ result }}</pre>
  </div>
</template>