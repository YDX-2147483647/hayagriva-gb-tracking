# Hayagriva对GB/T 7714—2015的支持情况

GB/T 7714—2015的128条示例文献中，有57条存在差异，占45%。下表是各种差异的数量以及它们在所有差异文献中的占比。

| 差异       | 总数量 ≈ 总占比 | 解释                                            |
| ---------- | --------------: | ----------------------------------------------- |
| lang       |         9 ≈ 21% | `等`/`et al.`等语言翻译问题                     |
| 卷         |         9 ≈ 21% | 多`卷`字（例：`第4册`误为`卷 第4册`）           |
| case       |         8 ≈ 19% | 大小写问题（例：英文机构名称被全大写）          |
| code_space |         7 ≈ 17% | 代码中的空格错误（例：`GB/T 123`误为`GB/T123`） |
| han_space  |         7 ≈ 17% | 中西字符间的空格差异（例：“第 1 卷”与“第1卷”）  |
| escape     |          3 ≈ 7% | CSL-JSON中的`\-`被原样输出，而未转成`-`         |
| num        |          3 ≈ 7% | 数码格式错误（例：`011`误为`11`）               |
| 其它       |        10 ≈ 24% | 以上未列出的差异，具体见后                      |

| 数量 ≈ 占比 | 差异情况（`+`表示兼有）    |
| ----------: | -------------------------- |
|     8 ≈ 19% | lang                       |
|     7 ≈ 17% | 卷 + han_space             |
|     5 ≈ 12% | code_space                 |
|     4 ≈ 10% | case                       |
|      3 ≈ 7% | num                        |
|      2 ≈ 5% | escape                     |
|      2 ≈ 5% | lang + case                |
|      1 ≈ 2% | case + escape + code_space |
|    10 ≈ 24% | 其它                       |
|   42 = 100% | 合计                       |

| 编号  | 以上已列出的差异 | 其它差异                                                      |
| ----- | ---------------- | ------------------------------------------------------------- |
| [9]   |                  | 文献类型代码错误（A误为M）                                    |
| [27]  | case + 卷        | 文献类型代码错误（J误为M）                                    |
| [26]  |                  | 文献类型代码错误（J误为M），缺少年份 issued、期 issue         |
| [25]  | 卷               | 文献类型代码错误（J误为M），缺少年份 issued、期 issue         |
| [107] | code_space       | 析出文献缺少编委会 editor                                     |
| [15]  |                  | 没支持CSL-JSON的`nocase`标签                                  |
| [88]  | lang             | 没支持CSL-JSON的`nocase`标签                                  |
| [111] |                  | 没支持CSL-JSON的`nocase`标签和`issued.literal`格式            |
| [110] |                  | 名字后缀`Jr,`误为`Jr.,`、没支持CSL-JSON的`issued.literal`格式 |
| [23]  |                  | 名字后缀`Jr,`误为`Jr.,`                                       |

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
