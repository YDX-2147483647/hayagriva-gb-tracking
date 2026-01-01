import { categories, records } from 'virtual:history_data'
import { lazy, StrictMode, Suspense, useState } from 'react'
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
