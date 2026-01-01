import { diffWordsWithSpace } from 'diff'

export default function DiffResult({
  actual,
  expected,
}: {
  actual: string
  expected: string
}): JSX.Element {
  // Increase the spacing because we will set .whitespace-pre-wrap
  const diff = diffWordsWithSpace(
    actual.trim().replaceAll('\n', '\n\n'),
    expected.trim().replaceAll('\n', '\n\n'),
  )

  return (
    <details className="pb-8">
      <summary className="font-bold">全部示例文献的详情</summary>
      <p>
        记号：<del className="bg-red-200">红色删除</del>部分为
        <strong>实验组</strong>，<ins className="bg-green-200">绿色增加</ins>
        部分为<strong>对照组</strong>，其余部分二者相同。
      </p>
      {/* .wrap-break-word is necessary for long URL, DOI, etc. */}
      <pre className="prose wrap-break-word whitespace-pre-wrap">
        {diff.map((part) => {
          if (part.added) {
            return <ins className="bg-green-200">{part.value}</ins>
          } else if (part.removed) {
            return <del className="bg-red-200">{part.value}</del>
          } else {
            return <span>{part.value}</span>
          }
        })}
      </pre>
    </details>
  )
}
