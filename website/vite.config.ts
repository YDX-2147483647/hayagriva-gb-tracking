import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

import historyDataPlugin from './plugins/history_data'

export default defineConfig({
  build: {
    chunkSizeWarningLimit: 1000,
  },
  plugins: [react(), tailwindcss(), historyDataPlugin()],
})
