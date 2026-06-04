# gbt7714-bibtex-style

- 此例来源：[`gbt7714-examples.bib`](https://github.com/zepinglee/gbt7714-bibtex-style/blob/8ab8f4dd9e9ab3e58ee739ab19f10cc27a3dbef6/gbt7714-examples.bib)
- 版权归属：[Zeping Lee](https://github.com/zepinglee)，LaTeX Project Public License 1.3c
- 说明文档：[§6 BibTeX 数据库指南 — `gbt7714-doc.pdf` (v2.3.0, 2026-05-26) | CTAN](https://mirrors.ctan.org/biblio/bibtex/contrib/gbt7714/gbt7714-doc.pdf#section.0.6)

[gbt7714 宏包](https://www.ctan.org/pkg/gbt7714)是 GB/T 7714 系列标准的 BibTeX 实现（此处 BibTeX 指原始版本，并非 BibLaTeX）。作者适配 GB/T 7714 时，选择逐条复现标准示例，`gbt7714-examples.bib`是所用文献数据。

另外说明文档还包含`gbt7714-examples.bib`以外的示例文献数据，此处暂未收录。

## 改动

- **将`gbt7714.7.5.4.3:1`的不规则年份`c1988`从`year`改为`date`**

  出版年无法确定时，可能要标版权年（例：`c1988`）。（GB/T 7714—2025 §7.5.4.3）

  这些不规则年份放到`year`会导致 Hayagriva 无法解析`*.bib`，报错 [WrongNumberOfDigits](https://docs.rs/biblatex/latest/biblatex/enum.TypeErrorKind.html#variant.WrongNumberOfDigits)。

  未修改`year = {[1936]}, date = {1936~}`、`year = {1995印刷}`等其它不规则年份，因为它们不会触发错误。

```diff
--- gbt7714-bibtex-style.bib
+++ gbt7714-bibtex-style.bib
@@ -453,13 +453,13 @@
   year          = {2013},
   date          = {2013-01-08},
   langid        = {chinese}
 }

 @book{gbt7714.7.5.4.3:1,
-  year          = {c1988},
+  date          = {c1988},
   langid        = {chinese}
 }

 @book{gbt7714.7.5.4.3:2,
   year          = {1995印刷},
   langid        = {chinese}
```
