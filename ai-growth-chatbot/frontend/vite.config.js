import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5174,        // Match backend CORS allowlist
    strictPort: true,  // Fail if 5174 is taken (prevents auto-switching)
    open: true,        // Open browser automatically
  },
})
