import { categories, records } from 'virtual:history_data'
import { useState } from 'react'
import ReactDOM from 'react-dom/client'
import Chart from './Chart'
import Postscript from './Postscript'
import RecordDetails from './RecordDetails'

import './global.css'

function App(): JSX.Element {
  const [selected, setSelected] = useState<number>(records.length - 1)

  return (
    <main>
      <h1 className="mt-8 text-center font-black text-4xl">
        Hayagriva对GB/T 7714—2015的支持情况
      </h1>
      <Chart records={records} categories={categories} onSelect={setSelected} />
      <div className="mx-auto mb-16 w-fit max-w-full px-4">
        <RecordDetails record={records[selected]} />
        <Postscript />
      </div>
    </main>
  )
}
const root = document.getElementById('root')
if (!root) {
  throw new Error('Root container missing')
}
ReactDOM.createRoot(root).render(<App />)
