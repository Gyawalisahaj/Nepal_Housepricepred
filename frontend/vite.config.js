import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // base path for GitHub Pages; must include leading and trailing slash
  base: '/Nepal_Housepricepred/',
})