# Hayagriva对GB/T 7714—2015的支持情况

GB/T 7714—2015的128条示例文献中，有57条存在差异，占45%。下表是各种差异的数量以及它们在所有差异文献中的占比。

| 差异       | 总数量 ≈ 总占比 | 解释                                            |
| ---------- | --------------: | ----------------------------------------------- |
| page       |        28 ≈ 49% | 缺页码或页码错误（例：`011`丢失或误为`11`）     |
| lang       |        11 ≈ 19% | `等`/`et al.`等语言翻译问题                     |
| 卷         |         9 ≈ 16% | 多`卷`字（例：`第4册`误为`卷 第4册`）           |
| case       |         7 ≈ 12% | 大小写问题（例：英文机构名称被全大写）          |
| code_space |         7 ≈ 12% | 代码中的空格错误（例：`GB/T 123`误为`GB/T123`） |
| han_space  |         7 ≈ 12% | 中西字符间的空格差异（例：“第 1 卷”与“第1卷”）  |
| escape     |          3 ≈ 5% | CSL-JSON中的`\-`被原样输出，而未转成`-`         |
| 其它       |        12 ≈ 21% | 以上未列出的差异，具体见后                      |

| 数量 ≈ 占比 | 差异情况（`+`表示兼有）    |
| ----------: | -------------------------- |
|    17 ≈ 30% | page                       |
|     7 ≈ 12% | lang                       |
|      4 ≈ 7% | page + code_space          |
|      4 ≈ 7% | 卷 + han_space             |
|      3 ≈ 5% | case                       |
|      3 ≈ 5% | 卷 + page + han_space      |
|      2 ≈ 4% | lang + case                |
|      2 ≈ 4% | escape                     |
|      1 ≈ 2% | code_space                 |
|      1 ≈ 2% | lang + page                |
|      1 ≈ 2% | case + escape + code_space |
|    12 ≈ 21% | 其它                       |
|   57 = 100% | 合计                       |

| 编号    | 以上已列出的差异  | 其它差异                                            |
| ------- | ----------------- | --------------------------------------------------- |
| [9]     |                   | 文献类型代码错误                                    |
| [27]    | case + 卷         | 文献类型代码错误                                    |
| [25]    | 卷                | 文献类型代码错误，缺少年份                          |
| [26]    |                   | 文献类型代码错误，缺少年份、卷/期                   |
| [46–47] | page              | 缺DOI                                               |
| [107]   | page + code_space | 析出文献未识别                                      |
| [23]    |                   | 名字后缀的`Jr.`紧挨逗号时，`.,`没有简化为`,`        |
| [15]    |                   | 没支持CSL-JSON的`no-case`标签                       |
| [88]    | lang              | 没支持CSL-JSON的`no-case`标签                       |
| [110]   |                   | 没支持CSL-JSON的`issued.literal`格式                |
| [111]   | page              | 没支持CSL-JSON的`no-case`标签和`issued.literal`格式 |

注：

- 这些示例文献的[CSL-JSON由Zotero中文社区提供](https://github.com/zotero-chinese/styles/raw/ce0786d7/lib/data/items/gbt7714-data.json)。

- 测试使用的CSL样式不是Typst内置的`gb-7714-2015-numeric`，而是[`GB-T-7714—2015（顺序编码，双语）.csl`](https://zotero-chinese.com/styles/GB-T-7714—2015（顺序编码，双语）/)。

- 比较对象是[Zotero中文社区将该CSL传入citeproc-js生成的`index.md`](https://github.com/zotero-chinese/styles/raw/ce0786d7/src/GB-T-7714—2015（顺序编码，双语）/index.md)，与我将[相应净化版CSL](https://typst-doc-cn.github.io/csl-sanitizer/chinese/src/GB-T-7714—2015（顺序编码，双语）/GB-T-7714—2015（顺序编码，双语）.csl)传入Hayagriva生成的结果。二者之所以采用不同CSL，是因为未[净化](https://typst-doc-cn.github.io/csl-sanitizer/chinese/src/GB-T-7714—2015（顺序编码，双语）/diff.html)的原始CSL传入Hayagriva会报错 CSL file malformed。

  比较时只比较了文本内容，未考虑链接等特殊样式。

- 以上测试基于CSL-JSON，而非Typst正常使用的BibTeX或YAML，因此与实用可能存在差距。

  一方面，CSL-JSON中的变量与CSL样式完全匹配，不涉及从BibTeX、YAML转换，所以信息损失更少。

  另一方面，Hayagriva代码中的`csl-json`特性只用于开发测试，未经过仔细验证，所以并不识别CSL-JSON某些特殊格式。

## 开发

```shell
uv tool install maturin

uv venv
maturin develop --release

uv run main.py
```
