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
              <strong>提示：</strong>
              GB/T
              7714—2025已于2026年7月1日实施。为方便对比历史，本项目近期仍针对2015版国标；建议一同参考
              <ExternalLink href="https://gb7714.zhtyp.art">
                另一项目针对2025版国标的测试结果
              </ExternalLink>
              。
            </p>
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
