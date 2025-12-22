<script setup lang = "ts">
import { ref } from 'vue'
const imageUrl = ref('')
const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement
    if (!target.files || !target.files[0]) return
    const file = target.files[0]
    imageUrl.value = URL.createObjectURL(file)
}
</script>

<template>
    <div class = "upload-container">
        <input type="file" @change = "handleFileChange" accept= "image/*" />
        <div v-if = "imageUrl" class = "preview">
            <img :src="imageUrl" alt="預覽圖片"/>
        </div>
    </div>
</template>

<style scoped>
    .upload-container{
        margin-top: 20px;
    }
    input[type="file"]{
        display: block;
        margin-bottom: 10px;

    }
    .preview img{
        max-width: 300px;
        max-height: 300px;
    }
</style>