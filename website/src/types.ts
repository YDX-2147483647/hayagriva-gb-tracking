export type Category = string | 'Unknown'

export type InputVersion = {
  entries_rev: string
  csl_updated_at: string
  hayagriva_source: string
}
export type OutputSummary = {
  n_entries: number
  n_diff: number
  diff_counts: Record<Category, number>
  cause_counts: Record<Category | string, number>
}

export type HistoryRecord = InputVersion & {
  output: OutputSummary
  label: string
  date: string
}

export interface XPointMeta {
  label: string // version label e.g., v0.8.1 or main (a137441)
  dateISO: string // ISO date used for x-axis
}
