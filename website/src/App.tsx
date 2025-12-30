import { categories, records } from 'virtual:history_data'
import { useState } from 'react'
import ReactDOM from 'react-dom/client'
import Chart from './Chart'
import RecordDetails from './RecordDetails'

import './global.css'

function App(): JSX.Element {
  const [selected, setSelected] = useState<number>(records.length - 1)

  return (
    <main>
      <Chart records={records} categories={categories} onSelect={setSelected} />
      <RecordDetails record={records[selected]} />
    </main>
  )
}
const root = document.getElementById('root')
if (!root) {
  throw new Error('Root container missing')
}
ReactDOM.createRoot(root).render(<App />)
