# Hayagriva对GB/T 7714—2015的支持情况

GB/T 7714—2015的128条示例文献中，有40条存在差异，占31%。下表是各种差异的数量以及它们在所有差异文献中的占比。

| 差异       | 总数量 ≈ 总占比 | 解释                                            |
| ---------- | --------------: | ----------------------------------------------- |
| lang       |          11 ≈ 28% | `等`/`et al.`等语言翻译问题                     |
| case       |           9 ≈ 23% | 大小写问题（例：英文机构名称被全大写）          |
| 卷         |         7 ≈ 18% | 多`卷`字（例：`第4册`误为`卷 第4册`）           |
| han_space  |         7 ≈ 18% | 中西字符间的空格差异（例：“第 1 卷”与“第1卷”）  |
| code_space |         7 ≈ 18% | 代码中的空格错误（例：`GB/T 123`误为`GB/T123`） |
| escape     |          3 ≈ 8% | CSL-JSON中的`\-`被原样输出，而未转成`-`         |
| num        |          3 ≈ 8% | 数码格式错误（例：`011`误为`11`）               |
| 其它       |         7 ≈ 18% | 以上未列出的差异，具体见后                      |

| 数量 ≈ 占比 | 差异情况（`+`表示兼有）    |
| ----------: | -------------------------- |
|     8 ≈ 20% | lang                       |
|     7 ≈ 18% | 卷 + han_space             |
|     5 ≈ 12% | code_space                 |
|     5 ≈ 12% | case                       |
|      3 ≈ 8% | num                        |
|      2 ≈ 5% | escape                     |
|      2 ≈ 5% | lang + case                |
|      1 ≈ 2% | case + escape + code_space |
|     7 ≈ 18% | 其它                       |
|   40 = 100% | 合计                       |

| 编号  | 以上已列出的差异 | 其它差异                                                                                      |
| ----- | ---------------- | --------------------------------------------------------------------------------------------- |
| [107] | code_space       | 析出文献缺少编委会 editor                                                                     |
| [26]  |                  | en dash 与 hyphen minus 的区别（可能是citeproc-js不对？）                                     |
| [88]  | lang             | 文献类型代码错误（M误为M/OL），没支持CSL-JSON的`nocase`标签，多DOI（可能是citeproc-js不对？） |
| [15]  | case             | 没支持CSL-JSON的`nocase`标签                                                                  |
| [111] |                  | 没支持CSL-JSON的`nocase`标签和`issued.literal`格式                                            |
| [23]  |                  | 名字后缀`Jr,`误为`Jr.,`                                                                       |
| [110] |                  | 名字后缀`Jr,`误为`Jr.,`、没支持CSL-JSON的`issued.literal`格式                                 |

注：

- 这些示例文献的[CSL-JSON由Zotero中文社区提供](https://github.com/zotero-chinese/styles/raw/ce0786d7/lib/data/items/gbt7714-data.json)。

- 测试使用的CSL样式不是Typst内置的`gb-7714-2015-numeric`，而是[`GB-T-7714—2015（顺序编码，双语）.csl`](https://zotero-chinese.com/styles/GB-T-7714—2015（顺序编码，双语）/)。

- 比较对象是[Zotero中文社区将该CSL传入citeproc-js生成的`index.md`](https://github.com/zotero-chinese/styles/raw/ce0786d7/src/GB-T-7714—2015（顺序编码，双语）/index.md)，与我将[相应净化版CSL](https://typst-doc-cn.github.io/csl-sanitizer/chinese/src/GB-T-7714—2015（顺序编码，双语）/GB-T-7714—2015（顺序编码，双语）.csl)传入Hayagriva生成的结果。二者之所以采用不同CSL，是因为未[净化](https://typst-doc-cn.github.io/csl-sanitizer/chinese/src/GB-T-7714—2015（顺序编码，双语）/diff.html)的原始CSL传入Hayagriva会报错 CSL file malformed。

  比较时只比较了文本内容，未考虑链接等特殊样式。

- 以上测试基于CSL-JSON，而非Typst正常使用的BibTeX或YAML，因此与实用可能存在差距。

  一方面，CSL-JSON中的变量与CSL样式完全匹配，不涉及从BibTeX、YAML转换，所以信息损失更少。

  另一方面，Hayagriva代码中的`csl-json`特性只用于开发测试，未经过仔细验证，所以并不识别CSL-JSON某些特殊格式，特别是`note`字段中的内容需要自行转换。

## 开发

```shell
uv tool install maturin

uv venv
maturin develop --release

uv run tracking/main.py
```

`maturin develop`会编译hayagriva供python调用。此步需要rust工具链；如无条件，可[从 GitHub Actions 下载编译好的`hayagriva-py-wheels-*`](https://github.com/YDX-2147483647/hayagriva-gb-tracking/actions/workflows/build.yaml)，解压，然后`uv pip install path/to/hayagriva_py-*.whl`。
