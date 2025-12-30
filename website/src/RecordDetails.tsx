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
          {record.label} — <time dateTime={record.date}>{record.date}</time>
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
            <th className="text-right" align="right">
              差异
            </th>
            <th className="text-nowrap text-right" align="right">
              总数量 ≈ 总占比
            </th>
            <th className="min-w-[14em]">解释</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([key, count]) => (
            <tr key={key}>
              <td className="text-right" align="right">
                {key}
              </td>
              <td className="text-nowrap text-right" align="right">
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
          <th className="text-right" align="right">
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
            <td className="text-right" align="right">
              {count} ≈{' '}
              {(
                (count / rows.reduce((sum, [, c]) => sum + c, 0)) *
                100
              ).toFixed(0)}
              %
            </td>
            <td>{key.replaceAll('+', ' + ')}</td>
          </tr>
        ))}
      </tbody>
    </table>
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
    <section className="prose mx-auto max-w-4/5">
      <InputVersion record={record} />
      <p>
        GB/T 7714—2015的{record.output.n_entries}条示例文献中，有
        {record.output.n_diff}条存在差异，占
        {((record.output.n_diff / record.output.n_entries) * 100).toFixed(0)}
        %。
      </p>
      <p>
        下表是各种差异的数量以及它们在所有差异文献中的占比。（由于一条文献可能同时存在多项差异，各项占比总和可能超过100%。）
      </p>
      <DiffCountsTable rows={diffItems} />
      <p>
        “其它”差异文献也可能存在以上已列出的差异。不过为简便，上表统一不计入。
      </p>
      <CauseCountsTable rows={causeItems} />
      <p>注：</p>
      <ul>
        <li>
          <p>
            这些示例文献的
            <a href="https://github.com/zotero-chinese/styles/raw/ce0786d7/lib/data/items/gbt7714-data.json">
              CSL-JSON由Zotero中文社区提供
            </a>
            。
          </p>
        </li>
        <li>
          <p>
            测试使用的CSL样式不是Typst内置的<code>gb-7714-2015-numeric</code>
            ，而是
            <a href="https://zotero-chinese.com/styles/GB-T-7714—2015（顺序编码，双语）/">
              <code>GB-T-7714—2015（顺序编码，双语）.csl</code>
            </a>
            。
          </p>
        </li>
        <li>
          <p>
            比较对象是
            <a href="https://github.com/zotero-chinese/styles/raw/ce0786d7/src/GB-T-7714—2015（顺序编码，双语）/index.md">
              Zotero中文社区将该CSL传入citeproc-js生成的<code>index.md</code>
            </a>
            ，与我将
            <a href="https://typst-doc-cn.github.io/csl-sanitizer/chinese/src/GB-T-7714—2015（顺序编码，双语）/GB-T-7714—2015（顺序编码，双语）.csl">
              相应净化版CSL
            </a>
            传入Hayagriva生成的结果。二者之所以采用不同CSL，是因为未
            <a href="https://typst-doc-cn.github.io/csl-sanitizer/chinese/src/GB-T-7714—2015（顺序编码，双语）/diff.html">
              净化
            </a>
            的原始CSL传入Hayagriva会报错 CSL file malformed。
          </p>
          <p>比较时只比较了文本内容，未考虑链接等特殊样式。</p>
        </li>
        <li>
          <p>
            以上测试基于CSL-JSON，而非Typst正常使用的BibTeX或YAML，因此与实用可能存在差距。
          </p>
          <p>
            一方面，CSL-JSON中的变量与CSL样式完全匹配，不涉及从BibTeX、YAML转换，所以信息损失更少。
          </p>
          <p>
            另一方面，Hayagriva代码中的<code>csl-json</code>
            特性只用于开发测试，未经过仔细验证，所以并不识别CSL-JSON某些特殊格式，特别是
            <code>note</code>字段中的内容需要自行转换。
          </p>
        </li>
      </ul>
    </section>
  )
}
