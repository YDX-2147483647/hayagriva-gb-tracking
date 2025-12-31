import assert from 'node:assert'
import fs from 'node:fs'
import path from 'node:path'

import { parse as parseToml } from '@std/toml'

import type {
  Category,
  HistoryRecord,
  InputVersion,
  OutputSummary,
} from '../src/types'

/// Categories of differences, ordered.
const categories: Category[] = [
  ['lang', 'case', '卷', 'num'],
  ['escape', 'han_space', 'code_space'],
  'punct',
  'Unknown',
].flat()

// To update:
//   gh release list --repo typst/hayagriva --json tagName,publishedAt --limit 3
// Note that the order matters.
const tags = [
  { publishedAt: '2025-09-26T16:04:05Z', tagName: 'v0.9.1' },
  { publishedAt: '2025-09-25T17:26:32Z', tagName: 'v0.9.0' },
  { publishedAt: '2025-02-05T11:15:17Z', tagName: 'v0.8.1' },
  { publishedAt: '2024-10-15T13:48:43Z', tagName: 'v0.8.0' },
  { publishedAt: '2024-10-03T14:54:02Z', tagName: 'v0.7.0' },
  { publishedAt: '2024-10-02T13:29:23Z', tagName: 'v0.6.0' },
  { publishedAt: '2024-05-16T10:23:58Z', tagName: 'v0.5.3' },
  { publishedAt: '2024-03-07T16:05:01Z', tagName: 'v0.5.2' },
  { publishedAt: '2023-11-29T17:37:41Z', tagName: 'v0.5.1' },
  { publishedAt: '2023-11-24T15:10:05Z', tagName: 'v0.5.0' },
  { publishedAt: '2023-10-31T00:21:37Z', tagName: 'v0.4.0' },
  { publishedAt: '2023-09-05T10:16:21Z', tagName: 'v0.3.2' },
  { publishedAt: '2023-09-05T09:53:21Z', tagName: 'v0.3.1' },
  { publishedAt: '2023-04-04T15:57:53Z', tagName: 'v0.3.0' },
  { publishedAt: '2023-03-28T13:46:35Z', tagName: 'v0.2.1' },
  { publishedAt: '2023-03-28T13:45:38Z', tagName: 'v0.2' },
  { publishedAt: '2021-01-18T15:40:31Z', tagName: 'v0.1.1' },
  { publishedAt: '2021-01-18T10:13:34Z', tagName: 'v0.1.0' },
]

// To update:
//   git log -1 --format='%h %ad' --date=iso-strict ⟨COMMIT-HASH⟩
// In the typst/hayagriva repo, author dates and committer dates are usually the same dates in different timezones.
const commits = `
a2bfce8 2025-12-21T06:07:37+01:00
a137441 2025-12-27T22:30:59Z
`

// To update:
//   gh release list --repo typst/typst --json tagName,publishedAt --limit 3
// Note that the order matters.
const typstTags = [
  { publishedAt: '2025-12-12T17:49:37Z', tagName: 'v0.14.2' },
  { publishedAt: '2025-12-03T17:10:21Z', tagName: 'v0.14.1' },
  { publishedAt: '2025-10-24T12:27:35Z', tagName: 'v0.14.0' },
  { publishedAt: '2025-10-17T16:54:42Z', tagName: 'v0.14.0-rc.2' },
  { publishedAt: '2025-10-10T12:54:29Z', tagName: 'v0.14.0-rc.1' },
  { publishedAt: '2025-03-07T12:50:41Z', tagName: 'v0.13.1' },
  { publishedAt: '2025-02-19T16:25:41Z', tagName: 'v0.13.0' },
  { publishedAt: '2025-02-05T17:31:03Z', tagName: 'v0.13.0-rc1' },
  { publishedAt: '2024-10-18T21:41:48Z', tagName: 'v0.12.0' },
  { publishedAt: '2024-10-15T14:28:05Z', tagName: 'v0.12.0-rc2' },
  { publishedAt: '2024-10-03T21:52:10Z', tagName: 'v0.12.0-rc1' },
  { publishedAt: '2024-05-17T15:33:15Z', tagName: 'v0.11.1' },
  { publishedAt: '2024-03-15T18:05:50Z', tagName: 'v0.11.0' },
  { publishedAt: '2024-03-09T18:29:10Z', tagName: 'v0.11.0-rc1' },
  { publishedAt: '2023-12-04T15:51:31Z', tagName: 'v0.10.0' },
  { publishedAt: '2023-10-31T01:32:16Z', tagName: 'v0.9.0' },
  { publishedAt: '2023-09-13T15:45:00Z', tagName: 'v0.8.0' },
  { publishedAt: '2023-08-07T16:20:37Z', tagName: 'v0.7.0' },
  { publishedAt: '2023-06-30T15:04:25Z', tagName: 'v0.6.0' },
  { publishedAt: '2023-06-09T14:55:29Z', tagName: 'v0.5.0' },
  { publishedAt: '2023-05-20T20:40:20Z', tagName: 'v0.4.0' },
  { publishedAt: '2023-04-26T14:20:47Z', tagName: 'v0.3.0' },
  { publishedAt: '2023-04-11T20:39:55Z', tagName: 'v0.2.0' },
  { publishedAt: '2023-04-04T23:46:28Z', tagName: 'v0.1.0' },
  { publishedAt: '2023-03-28T07:46:54Z', tagName: 'v23-03-28' },
  { publishedAt: '2023-03-21T22:21:52Z', tagName: 'v23-03-21-2' },
  { publishedAt: '2023-03-21T17:23:21Z', tagName: 'v23-03-21' },
]

/** A map from tag names to their published dates */
const tagDates: Record<string, string> = Object.fromEntries(
  tags.map((t) => [t.tagName, t.publishedAt]),
)

/** A map from short commit hashes to their dates */
const commitDates: Record<string, string> = commits
  .trim()
  .split(/\r?\n/)
  .reduce<Record<string, string>>((acc, line) => {
    const [hash, date] = line.split(/\s+/, 2)
    const short = hash?.slice(0, 7)
    if (short && date) acc[short] = date
    return acc
  }, {})

function resolveSourceUrl(source: string): { label: string; date: string } {
  const url = new URL(source.replace(/^git\+/, ''))
  const tag = url.searchParams.get('tag')
  const branch = url.searchParams.get('branch')
  const hash = url.hash.replace(/^#/, '')
  if (tag) {
    return { label: tag, date: tagDates[tag] }
  }
  if (branch) {
    const short = hash.slice(0, 7)
    const date = commitDates[short]
    return { label: `${branch}\n(${short})`, date }
  }
  throw new Error(`Cannot determine the date for a hayagriva source: ${source}`)
}

/** Calculate typstInfo for a given hayagriva date */
function calculateTypstInfo(date: string): HistoryRecord['typstInfo'] {
  const haya = new Date(date)

  // Find firstCovered
  const firstCovered = typstTags.findIndex((current, i) => {
    const prev = typstTags[i + 1]
    if (prev === undefined) {
      // This can never be the first typst that covered this hayagriva version
      // Therefore, return false.
      return false
    }

    const currentTypstDate = new Date(current.publishedAt)
    const prevTypstDate = new Date(prev.publishedAt)

    return currentTypstDate >= haya && haya > prevTypstDate
  })
  if (firstCovered === -1) {
    return null
  }
  const firstCoveredTypst = new Date(typstTags[firstCovered].publishedAt)
  const lastUncoveredTypst = new Date(typstTags[firstCovered + 1].publishedAt)

  // Find coveredRange
  const coveredHayagrivaList = tags.filter(({ publishedAt }) => {
    const hayaDate = new Date(publishedAt)
    return firstCoveredTypst >= hayaDate && hayaDate > lastUncoveredTypst
  })
  const start = coveredHayagrivaList[coveredHayagrivaList.length - 1].tagName
  const end = coveredHayagrivaList[0].tagName

  return {
    firstCovered: typstTags[firstCovered].tagName,
    coveredRange: [start, end],
  }
}

export default function historyDataPlugin() {
  const virtualModuleId = 'virtual:history_data'
  const resolvedVirtualModuleId = `\0${virtualModuleId}`

  return {
    name: 'hayagriva-history-data',
    resolveId(id: string) {
      if (id === virtualModuleId) {
        return resolvedVirtualModuleId
      }
    },
    load(id: string) {
      if (id !== resolvedVirtualModuleId) {
        return
      }

      const root = path.resolve(__dirname, '..')
      const historyPath = path.join(root, '../history.toml')

      const tomlText = fs.readFileSync(historyPath, 'utf8')
      const history = parseToml(tomlText) as {
        version: number
        record: (InputVersion & { output: OutputSummary })[]
      }
      const records: HistoryRecord[] = history.record.map((r) => {
        const undeclared = Object.keys(r.output.diff_counts).filter(
          (k) => !categories.includes(k),
        )
        assert(
          undeclared.length === 0,
          `Undeclared categories of difference: ${JSON.stringify(undeclared)} from ${JSON.stringify(r)}`,
        )

        const { label, date } = resolveSourceUrl(r.hayagriva_source)
        const typstInfo = calculateTypstInfo(date)
        return { label, date, typstInfo, ...r }
      })

      const moduleCode = [
        `export const categories = ${JSON.stringify(categories)}`,
        `export const records = ${JSON.stringify(records)}`,
      ].join(`\n`)
      return moduleCode
    },
  }
}
