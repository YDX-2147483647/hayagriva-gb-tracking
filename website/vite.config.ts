import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

import historyDataPlugin from './plugins/history_data'

export default defineConfig({
  base: './', // Use a relative base path
  build: {
    chunkSizeWarningLimit: 700,
  },
  plugins: [react(), tailwindcss(), historyDataPlugin()],
})
