declare module 'virtual:history_data' {
  import type { Category, HistoryRecord } from './types'

  export const categories: Category[]
  export const records: HistoryRecord[]
}
