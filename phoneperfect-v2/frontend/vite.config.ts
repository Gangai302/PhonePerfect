import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Relative base './' ensures bundle assets resolve under file:///android_asset/ in Android WebView
export default defineConfig({
  plugins: [react()],
  base: './',
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
