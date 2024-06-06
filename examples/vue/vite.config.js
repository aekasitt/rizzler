/* ~~/examples/vue/vite.config.js */

import { defineConfig } from 'vite'
import path from 'path'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  build: {
    rollupOptions: {
      input: path.resolve(__dirname, './pages/main.js')
    }
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './pages'),
    },
  }
})