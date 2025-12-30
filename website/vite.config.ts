import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

import historyDataPlugin from './plugins/history_data'

export default defineConfig({
  plugins: [react(), tailwindcss(), historyDataPlugin()],
})
