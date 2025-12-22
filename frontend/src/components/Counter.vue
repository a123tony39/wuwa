<script setup lang = "ts">
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
    <div class = "counter">
        <button @click="count++">
            點了 {{ count }} 次
        </button>
        <button @click="count = 0">歸零</button>
    </div>
</template>

<style scoped>
    .counter{
        margin-top: 16px;
    }

    button{
        padding: 8px 16px;
        font-size: 16px;
        cursor: pointer;
    }
</style>

