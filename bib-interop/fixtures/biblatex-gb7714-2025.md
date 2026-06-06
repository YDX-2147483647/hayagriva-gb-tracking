# biblatex-gb7714-2025

- 此例来源：[`example2025.bib`](https://github.com/hushidong/biblatex-gb7714-2025/blob/8e01fcaf1e74ab690e86df0608b7be114d55e4e0/example2025.bib)
- 版权归属：[胡振震](https://github.com/hushidong)，LaTeX Project Public License 1.3c or later
- 说明文档：[§4 GB/T 7714—2015 标准说明与实现 — `biblatex-gb7714-2015.pdf` (2026-04-11) | CTAN](https://mirrors.ctan.org/macros/latex/contrib/biblatex-contrib/biblatex-gb7714-2015/biblatex-gb7714-2015.pdf#section.4)

[biblatex-gb7714-2015 宏包](https://www.ctan.org/pkg/biblatex-gb7714-2015)是 GB/T 7714 系列标准的 biblatex 实现。作者适配 GB/T 7714—2025 时，选择用[`gbT7714-2025.tex`](https://github.com/hushidong/biblatex-gb7714-2025/blob/main/gbT7714-2025.tex)与[`tngbcitationaynew.tex`](https://github.com/hushidong/biblatex-gb7714-2025/blob/main/tngbcitationaynew.tex)直接复现标准全文，`example2025.bib`是所用文献数据。

不过`example2025.bib`中有些文献未被以上`*.tex`引用，例如[`萨利斯2000`](https://github.com/hushidong/biblatex-gb7714-2025/blob/8e01fcaf1e74ab690e86df0608b7be114d55e4e0/example2025.bib#L583-L596)。这些文献可能是为了测试该宏包支持的其它样式（例如法学引注手册），或从 2015 版迁移时遗留的。

## 改动

- **将一部分不规则年份从`year`改为`date`**

  例：`year = {c1988}` → `date = {c1988}`

  出版年无法确定时，可能要标版权年（例：`c1988`）或估计的出版年（例：`[1936]`）。（GB/T 7714—2025 §7.5.4.3）

  这些不规则年份放到`year`会导致 Hayagriva 无法解析`*.bib`，报错 [WrongNumberOfDigits](https://docs.rs/biblatex/latest/biblatex/enum.TypeErrorKind.html#variant.WrongNumberOfDigits)。

  未修改`1995印刷`等其它不规则年份，因为它们不会触发错误。

- **删除`萨利斯2000`的`editortype = {著}`**

  `著`不是 biblatex 明文允许的`editortype`。Hayagriva [可以解析任意`editortype`](https://docs.rs/biblatex/latest/biblatex/enum.EditorType.html#variant.Unknown)，但若存在`editor`且`editortype`特殊，则解析后无法转为`*.yaml`，报错 the enum variant `PersonRole::Unknown` cannot be serialized。

  考虑到标准全文未引用`萨利斯2000`，直接删除其`editortype`。

```diff
--- biblatex-gb7714-2025.bib
+++ biblatex-gb7714-2025.bib
@@ -423,23 +423,23 @@
   title = {中文书},
   date  = {2013-03-27}
 }

 @book{egbookpubdated--,
   title = {中文书},
-  year  = {c1988}
+  date  = {c1988}
 }

 @book{egbookpubdatee--,
   title = {中文书},
   year  = {1995印刷}
 }

 @book{egbookpubdatef--,
   title = {中文书},
-  year  = {[1936]}
+  date  = {[1936]}
 }


 @online{egbookpubdateg--,
   title   = {english book},
   date    = {2012-05-03},
@@ -584,13 +584,12 @@
   author           = {萨利斯},
   author+an        = {1:=paperauthor},
   author+an:nation = {=American},
   title            = {想象的真理},
   editor           = {安东尼·弗卢 and others},
   editor+an:nation = {=Britain},
-  editortype       = {著},
   booktitle        = {西方哲学演讲录},
   translator       = {李超杰},
   publisher        = {商务印书馆},
   date             = {2000},
   pages            = {112}
 }
@@ -1633,13 +1632,13 @@

 @inbook{BUSECK1980-117-211,
   title      = {Subsolidus phenomena in pyroxenes},
   author     = {P R BUSECK and NORD, Jr., G L and D R VEBLEN},
   bookauthor = {CT PREWITT},
   booktitle  = {Pyroxense},
-  year       = {c1980},
+  date       = {c1980},
   pages      = {117-211},
   publisher  = {Mineralogical Society of America},
   location   = {Washington, D.C.}
 }

 @inbook{陈晋镳1980-56-114,
```
