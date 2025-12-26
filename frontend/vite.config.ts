import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    strictPort: true,
    // 允許外部 host 訪問
    allowedHosts: [
      'blink-governor-owner-carl.trycloudflare.com'
    ]
  }
})
