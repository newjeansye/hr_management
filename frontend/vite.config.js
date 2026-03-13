import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path' 

const BACKEND_TARGET = 'http://localhost:5000'; 

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: BACKEND_TARGET,
        changeOrigin: true
      }
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'), 
    }
  }
})