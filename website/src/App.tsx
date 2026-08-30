import { categories, records } from 'virtual:history_data'
import { type JSX, lazy, StrictMode, Suspense, useState } from 'react'
import ReactDOM from 'react-dom/client'
import ChartLoading from './ChartLoading'
import ExternalLink from './ExternalLink'
import Postscript from './Postscript'
import RecordDetails from './RecordDetails'

import './global.css'

const Chart = lazy(() => import('./Chart'))

function App(): JSX.Element {
  const [selected, setSelected] = useState<number>(records.length - 1)

  return (
    <>
      <main>
        <h1 className="mt-8 text-center font-black text-4xl">
          Hayagriva对GB/T 7714—2015的支持情况
        </h1>
        <div className="mx-auto w-fit max-w-full px-4 py-8">
          <aside className="prose">
            <p>
              <strong>警告：</strong>
              本项目最新一条数据存在问题，建议参考
              <ExternalLink href="https://gb7714.zhtyp.art">
                另一项目对GB/T 7714—2025的测试结果
              </ExternalLink>
              。
            </p>
            <details>
              <summary>本项目最新一条数据的具体问题</summary>
              <p>
                Zotero中文社区于
                <ExternalLink href="https://github.com/zotero-chinese/styles/pull/613">
                  2026年1月
                </ExternalLink>
                将示例文献从2015版国标替换为2025版国标，又于
                <ExternalLink href="https://github.com/zotero-chinese/styles/pull/709">
                  同年8月
                </ExternalLink>
                将2015版国标CSL样式的标点符号改为全宽。
              </p>
              <p>
                本项目的实验组（Hayagriva）、对照组（Zotero）都使用2026年1月旧的2015版国标示例文献，但实验组采用2015版国标最新CSL样式，而对照组采用2015版国标2026年1月旧的CSL样式。在2026年8月以前，2015版国标CSL样式没有太大变化，所以实验组和对照组的处理结果适合相互比较；但现在2015版国标CSL改变了标点符号编码方式，二者不再适合比较。
              </p>
            </details>
          </aside>
        </div>
        <Suspense fallback={<ChartLoading />}>
          <Chart
            records={records}
            categories={categories}
            onSelect={setSelected}
          />
        </Suspense>
        <div className="mx-auto w-fit max-w-full px-4">
          <RecordDetails record={records[selected]} />
          <Postscript />
        </div>
      </main>
      <footer className="prose mx-auto mt-4 w-full max-w-full bg-gray-50 px-4 py-8 text-center">
        <ExternalLink href="https://github.com/YDX-2147483647/hayagriva-gb-tracking">
          GitHub: YDX-2147483647/hayagriva-gb-tracking
        </ExternalLink>
      </footer>
    </>
  )
}
const root = document.getElementById('root')
if (!root) {
  throw new Error('Root container missing')
}
ReactDOM.createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
