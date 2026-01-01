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

  /** Human name for the hayagriva version */
  label: string
  /** The date of the hayagriva version */
  date: string

  /**
   * Information about the corresponding typst version
   *
   * - `null`
   *
   *   No released typst version has included the changes from this hayagriva version
   *
   * - `{firstCovered: X, coveredRange: [START, END] }`
   *
   *   X is the first typst version that included changes from this hayagriva version.
   *   In fact, X introduced changes from hayagriva versions from START to END (inclusive).
   */
  typstInfo: {
    /** The first version of typst that includes the changes from this hayagriva version */
    firstCovered: string
    /** The range of hayagriva versions (inclusive) covered by that typst version */
    coveredRange: [string, string]
  } | null

  /**
   * The expected and actual output for the input.
   *
   * This is an optional field.
   * - For the latest version input, `target/tracking-cache/{expected,actual}-output.txt` (if exists) will be taken as the result.
   * - For other versions, the results will always be omitted.
   */
  result: { expected: string; actual: string } | null
}

export interface XPointMeta {
  label: string // version label e.g., v0.8.1 or main (a137441)
  dateISO: string // ISO date used for x-axis
}
