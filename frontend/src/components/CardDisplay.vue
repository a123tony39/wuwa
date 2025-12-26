<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import cardBack from '../assets/card/background.png'

const props = defineProps<{
  imgSrc: string | null,
  isCardMode: Boolean,
  isFlipped: Boolean,
}>()

const emit = defineEmits<{
  (e: 'update:isCardMode', value: boolean): void
  (e: 'update:isFlipped', value: boolean): void
  (e: 'reset'): void
}>()

// 3D 傾斜與拖拽
const tiltX = ref(0)
const tiltY = ref(0)
const hasMoved = ref(false)
const isDragging = ref(false)
const dragStart = ref<{ x: number, y: number } | null>(null)
const offset = ref({ x: 0, y: 0 })

const onMouseDown = (e: MouseEvent) => {
  e.preventDefault()
  hasMoved.value = false
  isDragging.value = true
  dragStart.value = {
    x: e.clientX - offset.value.x,
    y: e.clientY - offset.value.y,
  }
}

const onMouseUp = () => {
  if (!dragStart.value) return
  dragStart.value = null
  if (!isDragging.value) return
  isDragging.value = false
}

const onMouseMove = (e: MouseEvent) => {
  const card = document.querySelector('.card') as HTMLElement
  if (!card) return

  const rect = card.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  const maxTilt = 8

  if (dragStart.value) {
    const dx = e.clientX - (dragStart.value.x + offset.value.x)
    const dy = e.clientY - (dragStart.value.y + offset.value.y)

    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
      hasMoved.value = true
    }

    offset.value.x = e.clientX - dragStart.value.x
    offset.value.y = e.clientY - dragStart.value.y
  } else {
    tiltY.value = ((x - centerX) / centerX) * maxTilt
    tiltX.value = -((y - centerY) / centerY) * maxTilt

    // 光線效果
    const lightX = (x - centerX) / centerX
    const lightY = (y - centerY) / centerY
    const brightness = 1 + lightX * 0.1 - lightY * 0.1
    const front = document.querySelector('.card-front') as HTMLElement
    const back = document.querySelector('.card-back') as HTMLElement
    if (!props.isFlipped && front) front.style.filter = `brightness(${brightness})`
    if (props.isFlipped && back) back.style.filter = `brightness(${brightness})`
  }
}

onMounted(() => {
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
})
</script>

<template>
  <div v-if="imgSrc && isCardMode" class="card-container">
    <div class="page-overlay" @click="$emit('update:isCardMode', false); $emit('update:isFlipped', false)"></div>

    <div class="card-wrapper" :style="{ transform: `translate(${offset.x}px, ${offset.y}px)` }">
      <div
        class="card"
        :style="{
          transform: `rotateX(${tiltX}deg) rotateY(${tiltY}deg) ${props.isFlipped ? 'rotateY(180deg)' : ''}`
        }"
        @mousedown="onMouseDown"
        @click="!hasMoved && $emit('update:isFlipped', !props.isFlipped)"
      >
        <div class="card-face card-front">
            <img :src="imgSrc" />
        </div>
        <div class="card-face card-back">
          <img :src="cardBack" alt="背面圖片" />
        </div>
      </div>
    </div>
  </div>

  <img
    v-else-if="imgSrc && !isCardMode"
    :src="imgSrc"
    class="initial-img"
    @click="$emit('update:isCardMode', true); $emit('update:isFlipped', false)"
  />
</template>

<style scoped>
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

.card-wrapper {
  position: absolute;
}

.card {
  width: 350px;
  height: 500px;
  transform-style: preserve-3d;
  transition: transform 0.1s ease;
  cursor: pointer;
  position: relative;
}

.card-face {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 16px;
  backface-visibility: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.card-face img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* 前後面翻轉 + 微微 translateZ */
.card-front {
  transform: rotateY(0deg) translateZ(0.1px);
}

.card-back {
  transform: rotateY(180deg) translateZ(0.1px);
}

.page-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0);
  z-index: -1;
}

.initial-img {
  width: 400px;
  cursor: pointer;
  background-color: #111;
}
</style>
