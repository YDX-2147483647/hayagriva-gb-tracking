import { descriptions } from './category_description'
import type { Category, HistoryRecord } from './types'

function buildHayagrivaUrl(hayagriva_source: string): string {
  const url = new URL(hayagriva_source.replace(/^git\+/, ''))
  const tag = url.searchParams.get('tag')
  const branch = url.searchParams.get('branch')
  const hash = url.hash.replace(/^#/, '')
  if (tag !== null) {
    url.pathname += `/releases/tag/${tag}`
  } else if (branch !== null) {
    url.pathname += `/tree/${hash}`
  }
  url.search = ''
  url.hash = ''

  return url.href
}

function buildEntriesUrl(entries_rev: string): string {
  const [repo, rev] = entries_rev.split('#')
  return `https://github.com/${repo}/blob/${rev}/lib/data/items/gbt7714-data.json`
}

function InputVersion({ record }: { record: HistoryRecord }): JSX.Element {
  return (
    <ul>
      <li>
        Hayagriva版本：
        <a href={buildHayagrivaUrl(record.hayagriva_source)}>
          <strong>{record.label}</strong> —{' '}
          <time dateTime={record.date}>{record.date}</time>
        </a>
      </li>
      <li>
        CSL样式版本：
        <time dateTime={record.csl_updated_at}>{record.csl_updated_at}</time>
      </li>
      <li>
        示例文献版本：
        <a href={buildEntriesUrl(record.entries_rev)}>{record.entries_rev}</a>
      </li>
    </ul>
  )
}

function DiffCountsTable({
  rows,
}: {
  rows: [Category, number][]
}): JSX.Element | null {
  if (rows.length === 0) {
    return null
  }

  return (
    <div className="overflow-x-auto">
      <table className="mx-auto mt-0 w-fit">
        <caption>各项差异的分布</caption>
        <thead>
          <tr>
            <th align="right" className="text-right">
              差异
            </th>
            <th align="right" className="text-nowrap text-right">
              总数量 ≈ 总占比
            </th>
            <th className="min-w-[14em]">解释</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([key, count]) => (
            <tr key={key}>
              <td align="right" className="text-right">
                {key === 'Unknown' ? '其它' : key}
              </td>
              <td align="right" className="text-nowrap text-right">
                {count} ≈{' '}
                {(
                  (count / rows.reduce((sum, [, c]) => sum + c, 0)) *
                  100
                ).toFixed(0)}
                %
              </td>
              <td>{descriptions[key as keyof typeof descriptions]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function CauseCountsTable({
  rows,
}: {
  rows: [string, number][]
}): JSX.Element | null {
  if (rows.length === 0) {
    return null
  }
  return (
    <table className="mx-auto w-fit">
      <caption>各种差异组合情况的分布</caption>
      <thead>
        <tr>
          <th align="right" className="text-right">
            数量 ≈ 占比
          </th>
          <th>
            差异情况（<code>+</code>表示兼有）
          </th>
        </tr>
      </thead>
      <tbody>
        {rows.map(([key, count]) => (
          <tr key={key}>
            <td align="right" className="text-right">
              {count} ≈{' '}
              {(
                (count / rows.reduce((sum, [, c]) => sum + c, 0)) *
                100
              ).toFixed(0)}
              %
            </td>
            <td>{key === 'Unknown' ? '其它' : key.replaceAll('+', ' + ')}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

function hasSpecialCase(record: HistoryRecord): boolean {
  return [
    'v0.8.1',
    'v0.9.0',
    'v0.9.1',
    'main (a2bfce8)',
    'main (a137441)',
  ].includes(record.label.replaceAll('\n', ' '))
}

function SpecialCases({
  record,
}: {
  record: HistoryRecord
}): JSX.Element | null {
  if (!hasSpecialCase(record)) {
    return null
  }

  return (
    <div className="overflow-x-auto">
      <table className="mx-auto mt-0 w-fit">
        <caption>其它差异的具体内容</caption>
        <colgroup>
          <col />
          <col />
          <col className="min-w-[16em]" />
        </colgroup>
        <thead>
          <tr>
            <th>编号</th>
            <th>
              <span className="text-nowrap">以上已列出</span>
              <span className="text-nowrap">的差异</span>
            </th>
            <th>其它差异</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>[107]</td>
            <td>code_space</td>
            <td>析出文献缺少编委会 editor</td>
          </tr>
          <tr>
            <td>[26]</td>
            <td></td>
            <td>en dash 与 hyphen minus 的区别（可能是citeproc-js不对？）</td>
          </tr>
          <tr>
            <td>[88]</td>
            <td>lang</td>
            <td>
              文献类型代码错误（M误为M/OL），没支持CSL-JSON的<code>nocase</code>
              标签，多DOI（可能是citeproc-js不对？）
            </td>
          </tr>
          <tr>
            <td>[15]</td>
            <td>case</td>
            <td>
              没支持CSL-JSON的<code>nocase</code>标签
            </td>
          </tr>
          <tr>
            <td>[111]</td>
            <td></td>
            <td>
              没支持CSL-JSON的<code>nocase</code>标签和
              <code>issued.literal</code>格式
            </td>
          </tr>
          <tr>
            <td>[23]</td>
            <td></td>
            <td>
              名字后缀<code>Jr,</code>误为<code>Jr.,</code>
            </td>
          </tr>
          <tr>
            <td>[110]</td>
            <td></td>
            <td>
              名字后缀<code>Jr,</code>误为<code>Jr.,</code>、没支持CSL-JSON的
              <code>issued.literal</code>格式
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

export default function RecordDetails({
  record,
}: {
  record: HistoryRecord
}): JSX.Element {
  const diffItems = Object.entries(record.output.diff_counts)
  const causeItems = Object.entries(record.output.cause_counts)

  return (
    <section className="prose">
      <h2>所选日期的详细数据</h2>
      <InputVersion record={record} />
      <p>
        GB/T 7714—2015的{record.output.n_entries}条示例文献中，有
        {record.output.n_diff}条存在差异，占
        {((record.output.n_diff / record.output.n_entries) * 100).toFixed(0)}
        %。
      </p>
      <p>
        下表是各种差异的数量以及它们在所有差异文献中的占比。由于一条文献可能同时存在多项差异，从而同时计入多项，所以各项占比总和可能超过100%。另外，“其它”差异文献也可能存在已列出的差异，不过为简便，下表统一不计入。
      </p>
      <DiffCountsTable rows={diffItems} />
      <p>
        下表展示了各种差异组合情况的数量及占比。与上表不同，下表各项互斥，能更具体地描述差异文献的分布。
      </p>
      <CauseCountsTable rows={causeItems} />
      {hasSpecialCase(record) && (
        <>
          <p>我们还人工分析了其它差异的具体内容，如下表。</p>
          <SpecialCases record={record} />
        </>
      )}
    </section>
  )
}
