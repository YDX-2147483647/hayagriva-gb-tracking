import ExternalLink from './ExternalLink'

export default function Postscript(): JSX.Element {
  return (
    <section className="prose">
      <h2>测试细节</h2>
      <p>比较对象如下表。</p>

      {/* .text-center overrides tailwind .prose */}
      <table className="mx-auto w-fit [&_td]:text-center [&_th]:text-center">
        <thead>
          <tr>
            <th></th>
            <th>实验组</th>
            <th>对照组</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th>参考文献引擎</th>
            <td>
              <ExternalLink href="https://docs.rs/hayagriva/">
                typst/hayagriva
              </ExternalLink>
            </td>
            <td>
              <ExternalLink href="https://citeproc-js.readthedocs.io/">
                Juris-M/citeproc-js
              </ExternalLink>
            </td>
          </tr>
          <tr>
            <th className="text-nowrap">CSL样式</th>
            <td>
              <ExternalLink href="https://typst-doc-cn.github.io/csl-sanitizer/chinese/src/GB-T-7714—2015（顺序编码，双语）/GB-T-7714—2015（顺序编码，双语）.csl">
                Typst中文社区净化版
              </ExternalLink>
            </td>
            <td>
              <ExternalLink href="https://zotero-chinese.com/styles/GB-T-7714—2015（顺序编码，双语）/">
                Zotero中文社区原版
              </ExternalLink>
            </td>
          </tr>
          <tr>
            <th>示例文献</th>
            <td colSpan={2}>
              <ExternalLink href="https://github.com/zotero-chinese/styles/blob/main/lib/data/items/gbt7714-data.json">
                Zotero中文社区提供的<code>gbt7714-data.json</code>
              </ExternalLink>
            </td>
          </tr>
          <tr>
            <th className="text-nowrap">结果来源</th>
            <td>本项目编程生成</td>
            <td>
              <ExternalLink href="https://github.com/zotero-chinese/styles/blob/main/src/GB-T-7714—2015（顺序编码，双语）/index.md#gbt-77142015-示例文献">
                Zotero中文社区提供的<code>index.md</code>
              </ExternalLink>
            </td>
          </tr>
        </tbody>
      </table>

      <p>注意：</p>
      <ul>
        <li>
          <p>
            比较时<strong>只比较了文本内容</strong>，未考虑链接等特殊样式。
          </p>
        </li>
        <li>
          <p>
            测试使用的<strong>CSL样式</strong>不是Typst内置的
            <code>gb-7714-2015-numeric</code>，而是
            <ExternalLink href="https://zotero-chinese.com/styles/GB-T-7714—2015（顺序编码，双语）/">
              <code>GB-T-7714—2015（顺序编码，双语）.csl</code>
            </ExternalLink>
            。
          </p>
          <p>
            而且实验组和对照组采用的CSL不同，因为未
            <ExternalLink href="https://typst-doc-cn.github.io/csl-sanitizer/chinese/src/GB-T-7714—2015（顺序编码，双语）/diff.html">
              净化
            </ExternalLink>
            的原版CSL传入Hayagriva会报错 CSL file malformed。
          </p>
        </li>
        <li>
          <p>
            <strong>示例文献的格式</strong>
            是CSL-JSON，而非Typst正常使用的BibTeX或YAML，因此测试结果与实用可能存在差距。
          </p>
          <p>
            一方面，CSL-JSON中的变量与CSL样式完全匹配，不涉及从BibTeX、YAML转换，所以信息损失更少。
          </p>
          <p>
            另一方面，Hayagriva代码中的<code>csl-json</code>
            特性只用于开发测试，未经过仔细验证，所以并不识别CSL-JSON某些特殊格式，特别是
            <code>note</code>字段中的内容需要专门转换。
          </p>
        </li>
      </ul>
    </section>
  )
}
