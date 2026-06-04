# 测试结果

## 确实存在的问题

### 文献类型

#### 不支持 biblatex 非标准文献类型

> [§2.1.3 Non-standard Types — `biblatex.pdf`][biblatex-2.1.3]
>
> The types in this section are similar to the custom types `@custom[a--f]`, i. e., the standard bibliography styles provide no bibliography drivers for these types. In the standard styles they will use the bibliography driver for `@misc` entries—exceptions to this rule are noted in the descriptions below. The types are known to the default data model and will be happily accepted by `biber`.

`biblatex.pdf`明文列出了若干“非标准”文献类型：`@artwork`、`@audio`、`@bibnote`、`@commentary`、`@image`、`@jurisdiction`、`@legislation`、`@legal`、`@letter`、`@movie`、`@music`、`@performance`、`@review`、`@standard`、`@video`。GB/T 7714—2025 要求用代码标明文献类型，因此即使某两类文献的著录项目相同，也不能合并。

下例简化自 [biblatex-gb7714-2025][]，其中`@standard`被误当作`@misc`。[gbt7714-bibtex-style][] 亦有相同用法。

```bib
@standard{gbt7714.8.9.2:2,
  author        = {国家能源局},
  title         = {水电工程水温实时监测系统技术规范},
  number        = {NB/T 10386—2020},
}
```

```typst
#assert.eq(converted.type, "misc") // 当前情况
```

`@image`、`@letter`、`@video`等也是这种情况。

#### 不支持 gbt7714-bibtex 增加的文献类型

与 biblatex 相比，[gbt7714-bibtex-style][] 明确增加了几种文献类型：`@archive`档案、`@map`地图、`@preprint`预印本。

下例简化自 gbt7714-bibtex-style，其中`@preprint`被误当作`@misc`。不过 [biblatex-gb7714-2025][] 没有类似用法。

```bib
@preprint{gbt7714.8.15.2:3,
  author        = {Jenkins, Stewart D. and Ruostekoski, Janne},
  title         = {Controlled Manipulation of Light by Cooperative Response of Atoms in an Optical Lattice},
  doi           = {10.48550/arXiv.1112.6136},
}
```

```typst
#assert.eq(converted.type, "misc") // 当前情况
```

另外，可忽略的[丢失`pubstate`问题](#丢失pubstate)、[`archiveprefix`不识别问题](#不识别某些archiveprefix)也与预印本相关。

下例也简化自 gbt7714-bibtex-style，其中`@map`也被误当作`@misc`，并且`scale`与`dimensions`被丢失。[biblatex-gb7714-2025][] 亦有相同用法。

```bib
@map{gbt7714.8.13.3:1,
  author        = {胡健民},
  title         = {东南极拉斯曼丘陵地区地质图},
  scale         = {1:25000},
  dimensions    = {128cm×84cm},
}
```

```typst
// 当前情况：
#assert.eq(converted.type, "misc")
#assert("scale" not in converted and "dimensions" not in converted)
```

#### 不支持 biblatex-gb7714-2025 增加的文献类型

与 biblatex 相比，[biblatex-gb7714-2025][] 增加了`@newspaper`报纸文献类型。

下例简化自 biblatex-gb7714-2025，其中`@newspaper`被误当作`@misc`。不过 [gbt7714-bibtex-style][] 没有类似用法。

```bib
@newspaper{陈缮真2022--,
  title        = {探索微观世界的无穷奥秘（科技大观）},
  author       = {陈缮真},
  journaltitle = {人民日报},
}
```

```typst
// 当前情况：
#assert.ne(converted.type, "newspaper")
#assert("parent" not in converted)
```

#### 丢失`entrysubtype`

下例简化自 [gbt7714-bibtex-style][]，其中`entrysubtype = {newspaper}`会丢失。

```bib
@article{gbt7714.8.5.3:1,
  entrysubtype  = {newspaper},
  title         = {数字革命与竞争国际化},
  journal       = {中国青年报},
}
```

```typst
#assert.ne(converted.type, "newspaper") // 当前情况
```

#### `@inproceedings`带`eventtitle`时转换出异常`parent`

下例简化自 [biblatex-gb7714-2025][]，它会转换出两个parent，其中之一除`type: proceedings`外没有任何字段。[gbt7714-bibtex-style][] 亦有相同用法。

```bib
@inproceedings{gbt7714.8.6.3:2,
  author     = {Wang, Shanshan},
  title      = {Application of improved {SOM} neural network in intelligent auditing of hospital financial vouchers},
  eventtitle = {2022 6th {Asian Conference} on {Artificial Intelligence Technology}},
}
```

```yaml
gbt7714.8.6.3:2:
  type: article
  title: Application of improved {SOM} neural network in intelligent auditing of hospital financial vouchers
  author: Wang, Shanshan
  parent:
  - type: proceedings
  - type: conference
    title: 2022 6th {Asian Conference} on {Artificial Intelligence Technology}
```

```typst
#assert.ne(converted.parent.len(), 1) // 当前情况
```

建议：两个`parent`合一；`type`取`proceedings`还是`conference`待讨论。

### 著录项目

#### 不识别数字`month`

> [§2.2.2 Data Fields — `biblatex.pdf`][biblatex-2.2.2]
>
> `month` field (literal)
>
> The publication month. This must be an integer, not an ordinal or a string. Don’t say `month={January}` but `month={1}`. The bibliography style converts this to a language dependent string or ordinal where required. This field is a literal field only when given explicitly in the data (for plain BibTeX compatibility for example). It is however
better to use the `date` field as this supports many more features. See §§ 2.3.8 (Date and Time Specifications) and 2.3.9 (Year, Month and Date).

> §3.2 Fields — [`btxdoc.pdf`][btxdoc]
>
> `month` The month in which the work was published or, for an unpublished work, in which it was written. You should use the standard three-letter abbreviation, as described in Appendix B.1.3 of the LaTeX book.

The LaTeX book (ISBN 0-201-52983-1) was written by Leslie Lamport. In Appendix B.1.3 he wrote:

> Some abbreviations are predefined by the bibliography style. These always include the usual three-letter abbreviations for the month: `jan`, `feb`, `mar`, etc.

下例取自 [biblatex-gb7714-2025][]，`year`与`month`会被转换为`date: 2009`，丢失`month`。[gbt7714-bibtex-style][] 只使用`date`与`year`，无此问题。

```bib
@book{陈希孺2009--,
  title     = {概率论与数理统计},
  year      = {2009},
  month     = {2}
}
```

```typst
#assert.ne(converted.date, "2009-02") // 当前情况
```

#### 特殊`year`被错误简化

GB/T 7714—2025 规定：「8.5.1.3 凡是在同一期刊上连载的文献，其后续部分不必另行著录，可在原参考文献后直接注明后续部分的年、卷、期、页码等。」并附示例「2011, 33 (2): 20-25; 2011, 33 (3): 26-30」。

下例取自 [biblatex-gb7714-2025][]，`year`会被转换为`date: 2011`，丢失后面特殊内容。

```bib
@article{egdatevolnumpagefull--,
  title = {article of journal},
  year  = {2011，33（2）：20--25；2011，33（3）：26--30}
}
```

```typst
#assert.eq(converted.date, 2011) // 当前情况
```

[gbt7714-bibtex-style][] 也有类似写法，但将特殊处记在`pages`，并无此问题。

此外还有其它特殊`year`，GB/T 7714—2025 规定：「7.5.4.1 出版年应采用公元纪年，并用阿拉伯数字著录。如有其他纪年形式时，应将原有的纪年形式置于“（）”内。」

下例简化自 gbt7714-bibtex-style，`year`会被转换为`date: 1887`。biblatex-gb7714-2025 也有相同用法。

```bib
@letter{gbt7714.8.12.3:1,
  author        = {李鸿章},
  year          = {1887（光绪十三年三月十三日）},
}
```

```typst
#assert.eq(converted.date, 1887) // 当前情况
```

#### 丢失`cstr`

CSTR（科技资源标识符, common science and technology resource identifier）大致是中国化的 DOI，目前 CSL、CSL-M 均无正式支持。GB/T 7714—2025 虽然正文只要求「永久标识符」，但有些示例使用了 CSTR。

下例简化自 [biblatex-gb7714-2025][]，其中`cstr`会丢失。[gbt7714-bibtex-style][] 亦有相同用法。

```bib
@thesis{gbt7714.8.7.2:3,
  author      = {井丽南},
  url         = {http://dpaper.las.ac.cn/Dpaper/detail/detailNew?paperID=20209289},
  cstr        = {35001.37.01.33142.20220037},
}
```

```typst
#assert("serial-number" not in converted) // 当前情况
```

建议：

- 让`biblatex::Entry`与 citationberg 支持解析`cstr`字段

- 让 Hayagriva 将`cstr`记录到[`serial-number`](https://typst-community.github.io/extra-docs/hayagriva/file-format.html#serial-number)下：

  ```yaml
  gbt7714.8.7.2:3:
    type: thesis
    author: 井丽南
    url: http://dpaper.las.ac.cn/Dpaper/detail/detailNew?paperID=20209289
    serial-number:
      cstr: "35001.37.01.33142.20220037"
  ```

参见 [typst#8075 评论](https://github.com/typst/typst/issues/8075#issuecomment-4211410608)。

#### 丢失`titleaddon`与`*titleaddon`

> [§2.2.2 Data Fields — `biblatex.pdf`][biblatex-2.2.2]
>
> `booktitleaddon` field (literal)
>
> An annex to the `booktitle`, to be printed in a different font.
>
> `journaltitleaddon` field (literal)
>
> An annex to the `journaltitle`, to be printed in a different font.
>
> `titleaddon` field (literal)
>
> An annex to the `title`, to be printed in a different font.

下例简化自 [biblatex-gb7714-2025][]，其中`titleaddon`会丢失。[gbt7714-bibtex-style][] 无类似用法。

```bib
@article{刘彻东1998-38-39,
  title        = {中国的青年刊物},
  author       = {刘彻东},
  titleaddon   = {个性特色为本}
}
```

```typst
// 当前情况：
#assert.eq(converted.title, "中国的青年刊物")
#assert.eq(converted.keys(), ("type", "title", "author", "parent"))
#assert.eq(converted.parent.keys(), ("type",))
```

### 其它

#### 不支持用`langid`或`language`标注文献语种

> [§2.2.2 Data Fields — `biblatex.pdf`][biblatex-2.2.2]
>
> `language` list (key)
>
> The language(s) of the work. Languages may be specified literally or as localisation keys (see § 4.9.2 (Localization Keys), especially § 4.9.2.18 (Language Names)). If localisation keys are used, the prefix `lang` is omissible: both `langenglish` and `english` can be used. If the `clearlang` option is set, the content of this field may be cleared if it matches the `babel`/`polyglossia` language of the document (or the language specified explicitly with the `language` option), see § 3.1.2.1 (Preamble Options → General). See also `origlanguage` and compare `langid` in § 2.2.3 (Special Fields).
>
> [§2.2.3 Special Fields — `biblatex.pdf`][biblatex-2.2.3]
>
> `langid` field (identifier)
> 
> The language id of the bibliography entry. The alias `hyphenation` is provided for backwards compatibility. The identifier must be a language name known to the `babel`/`polyglossia` packages. This information may be used to switch hyphenation patterns and localise strings in the bibliography. Note that the language names are case sensitive. The languages currently supported by this package are given in table 2 (Supported Languages). Note that `babel` treats the identifier `english` as an alias for `british` or `american`, depending on the `babel` version. The `biblatex` package always treats it as an alias for `american`. It is preferable to use the language identifiers `american` and `british` (babel) or a language specific option to specify a language variant (`polyglossia`, using the `langidopts` field) to avoid any possible confusion. Compare `language` in § 2.2.2 (Data Fields).

不同语种的文献可能需按不同格式著录。

下例简化自 [biblatex-gb7714-2025][]，其中`langid`会丢失。[gbt7714-bibtex-style][] 亦有相同用法。

```bib
@online{gbt7714.8.11.2.2:1,
  title   = {中国国家博物馆},
  langid  = {chinese}
}
```

```typst
#assert.eq(converted.keys(), ("type", "title")) // 当前情况
```

下例简化自 [bithesis][]，其中`language`也会丢失。

```bib
@phdthesis{zhanghesheng,
  title    = {嵌入式单片机系统设计},
  language = {zh},
}
```

```typst
#assert.eq(converted.keys(), ("type", "title", "genre")) // 当前情况
```

参见 [clreq-gap for typst §7.2  参考文献表：英文用`et al.`，中文用`等`](https://gap.zhtyp.art/#et-al-lang)。

#### 不支持多语种对照的文献表

GB/T 7714—2015 曾要求「必要时，可采用双语著录」，不过 GB/T 7714—2025 删除了这一说法。

下例简化自 [gbt7714-bibtex-style][]，其中`*_en`几个字段会丢失。

```bib
@article{gbt7714.b.4:11,
  author        = {王利平 and 王福新 and 刘洪},
  author_transliteration_en = {Wang, Liping and Wang, Fuxin and Liu, Hong},
  title         = {过冷大水滴环境粒径分布模拟方法研究进展},
  title_translation_en = {Research progress on simulation methods of drop diameter distribution in supercooled large drop icing conditions},
  journal       = {航空学报},
  journal_translation_en = {Acta Aeronautica et Astronautica Sinica},
}
```

```typst
// 当前情况：
#assert.eq(converted.keys(), ("type", "title", "author", "parent"))
#assert.eq(converted.parent.keys(), ("type", "title"))
```

[biblatex-gb7714-2025][] 也支持多语种对照文献表，但支持方式不同，不涉及`*_en`字段，而是定义两条文献再用`entryset`绑定或用其它方式关联，这些方法也不支持。

参见 [typst-doc-cn/clreq#37](https://github.com/typst-doc-cn/clreq/issues/37)。

## 可忽略的问题

以下大部分是丢失字段，并且这些字段在[`biblatex::Entry`](https://docs.rs/biblatex/latest/biblatex/struct.Entry.html)都有接口，只是 Hayagriva 未使用。

### 丢失`authortype`

> [§2.2.2 Data Fields — `biblatex.pdf`][biblatex-2.2.2]
>
> `authortype` field (key)
>
> The type of author. This field will affect the string (if any) used to introduce the author.

以下两例简化自 [biblatex-gb7714-2025][]，其中`authortype`会丢失。

```bib
@book{胡长清1997,
  title      = {中国民法总论},
  author     = {胡长清},
  authortype = {著},
}
@book{张新宝2016,
  title      = {侵权责任法},
  author     = {张新宝},
  authortype = {主编},
}
```

```typst
// 当前情况：
#assert.eq(converted.胡长清1997.author, "胡长清")
#assert.eq(converted.张新宝2016.author, "张新宝")
```

不过标准全文未引用以上两例，故忽略。

### 丢失`author+an`与`editor+an`

> [§3.7 Data Annotations — `biblatex.pdf`][biblatex-3.7]
>
> Here the field name suffix `+an` is a user-definable (footnote: See `biber`’s `--annotation-marker` option.) suffix which marks a data field as an annotation of the unsuffixed field. Multiple annotations can be provided for the same field since all annotations are named. After the annotation marker is the optional named annotation marker (footnote: See `biber`’s `--named-annotation-marker` option.) and an optional annotation name. The annotation name is ‘default’ if not specified…

下例简化自 [biblatex-gb7714-2025][]，其中几个`+an`会丢失。

```bib
@inproceedings{萨利斯2000,
  author           = {萨利斯},
  author+an        = {1:=paperauthor},
  author+an:nation = {=American},
  title            = {想象的真理},
  editor           = {安东尼·弗卢 and others},
  editor+an:nation = {=Britain},
}
```

```typst
// 当前情况：
#assert.eq(converted, yaml(bytes(
  ```yaml
  type: article
  title: 想象的真理
  author: 萨利斯
  editor:
  - 安东尼·弗卢
  - others
  parent:
    type: proceedings
  ```.text,
)))
```

不过标准全文未引用上例，故忽略。

### 丢失`country`、`shorthand`

下例简化自 [biblatex-gb7714-2025][]，其中`country`会丢失。

```bib
@inproceedings{Nemec1997-209-214,
  title     = {Force control of redundant robots},
  author    = {B Nemec},
  country   = {Nantes France},
}
```

```typst
// 当前情况：
#assert.eq(converted.keys(), ("type", "title", "author", "parent"))
#assert.eq(converted.parent.keys(), ("type",))
```

标准全文未引用上例，biblatex-gb7714-2025 仅此一处且无说明，别处也无此用法，故忽略。

单数的`shorthand`也是类似情况，标准全文未引用，biblatex-gb7714-2025 有几处但无说明，别处无此用法，故也忽略。

### 丢失`eid`

> [§2.2.2 Data Fields — `biblatex.pdf`][biblatex-2.2.2]
>
> `eid` field (literal)
>
> The electronic identifier of an `@article` or chapter-like section of a larger work often called ‘article number’, ‘paper number’ or the like. This field may replace the `pages` field for journals deviating from the classic pagination scheme of printed journals by only enumerating articles or papers and not pages.
>
> Not to be confused with `number`, which for `@articles` subdivides the `volume`.

下例简化自 [biblatex-gb7714-2025][]，其中`eid`会丢失。

```bib
@article{MAURYA2023,
  author       = {MAURYA, A.  and SZYMANSKI, M. AND KARLOWSKI, W. M.},
  journaltitle = {GigaScience},
  eid          = {giad067},
  url          = {https://doi.org/10.1093/gigascience/giad067}
}
```

```typst
#assert("serial-number" not in converted) // 当前情况
```

`eid`一般用`pages`即可，其实该出版商网站也把`giad067`导出为`pages`而非`eid`，故忽略。

### 丢失`keywords`、`sortkey`、`key`

> [§2.2.3 Special Fields — `biblatex.pdf`][biblatex-2.2.3]
>
> `keywords` field (separated values)
>
> A separated list of keywords. These keywords are intended for the bibliography filters (see §§ 3.8.2 (The Bibliography) and 3.14.4 (Subdivided Bibliographies)), they are usually not printed. Note that with the default separator (comma), spaces around the separator are ignored.
>
> `sortkey` field (literal)
>
> A field used to modify the sorting order of the bibliography. Think of this field as the master sort key. If present, `biblatex` uses this field during sorting and ignores everything else, except for the `presort` field. Please refer to § 3.6 (Sorting Options) for further details. This field is consumed by the backend processing and does not appear in the `.bbl`.
>
> [§2.2.5 Field Aliases — `biblatex.pdf`][biblatex-2.2.5]
>
> `key` field (literal)
>
> An alias for `sortkey`, provided for BibTeX compatibility. See § 2.2.3 (Special Fields).

下例简化自 [bithesis][]，其中`keywords`会丢失。

```bib
@book{OBRIEN1994Aircraft,
  keywords={book},
}
```

```typst
#assert.eq(converted.keys(), ("type",)) // 当前情况
```

`keywords`用于拆分文献列表，`key`与`sortkey`用于调整文献在列表中的顺序，都不必专门支持，故忽略。

### 丢失`nameformat`

`nameformat`是 [biblatex-gb7714-2025][] 增加的选项，用于设置该条目作者名字的大小写、姓与名的顺序、拼音写法等。[gbt7714-bibtex-style][] 似乎没有类似用法。

下例简化自 biblatex-gb7714-2025，其中`nameformat`会丢失。

```bib
@article{gbt7714.b.4.11,
  author       = {Wang, Liping and Wang, Fuxin and Liu, Hong},
  title        = {Research progress on simulation methods of drop diameter distribution in supercooled large drop icing conditions},
  nameformat   = {quanpin}
}
```

```typst
// 当前情况：
#assert.eq(converted.keys(), ("type", "title", "author", "parent"))
#assert.eq(converted.parent.keys(), ("type",))
```

这是 biblatex-gb7714-2025 特殊功能，可以通过直接编辑`author`字段实现，故忽略。

### 丢失`options`

> [§2.2.3 Special Fields — `biblatex.pdf`][biblatex-2.2.3]
>
> `options` field (separated `〈key〉=〈value〉` options)
>
> A separated list of entry options in `〈key〉=〈value〉` notation. This field is used to set options on a per-entry basis. See § 3.1.3 (Entry Options) for details. Note that citation and bibliography styles may define additional entry options.

下例简化自 [biblatex-gb7714-2025][]，其中`options`会丢失。它设置`useprefix = false`是确保第一作者显示为 Veen P H v d 而非 V d Veen P H（其实默认如此）。

```bib
@article{gbt7714.8.5.3:10,
  author       = {v d Veen, Pieternella H. and Muller, Majon and Vincken, Koen L. and Witkamp, Theo D. and Mali, Willem P. T. M. and Graaf, Yolanda van der and Geerlings, Mirjam I. and {SMART-MR Study Group}},
  options      = {useprefix=false},
  title        = {Longitudinal changes in brain volumes and cerebrovascular lesions on {MRI} in patients with manifest arterial disease: the {SMART-MR} study},
}
```

```typst
// 当前情况：
#assert.eq(converted.keys(), ("type", "title", "author", "parent"))
#assert.eq(converted.parent.keys(), ("type",))
```

另外还有设置`labelnumber=true`等选项的。这些选项属于 biblatex 特殊功能，可用`show text`等机制替代，不必支持，故忽略。

### 丢失`primaryclass`

> [§2.2.5 Field Aliases — `biblatex.pdf`][biblatex-2.2.5]
>
> `primaryclass` field (literal)
>
> An alias for `eprintclass`, provided for arXiv compatibility. See §§ 2.2.2 (Data Fields) and 3.14.7 (Electronic Publishing Information).
>
> [§2.2.2 Data Fields — `biblatex.pdf`][biblatex-2.2.2]
>
> `eprintclass` field (literal)
>
> Additional information related to the resource indicated by the `eprinttype` field. This could be a section of an archive, a path indicating a service, a classification of some sort, etc. See § 3.14.7 (Electronic Publishing Information) for details. Also see `eprint` and `eprinttype`.

下例取自  [biblatex-gb7714-2025][]，其中`primaryclass = {stat.ML}`会丢失。

```bib
@misc{vinyals2017pointer,
  title         = {Pointer Networks},
  author        = {Oriol Vinyals and Meire Fortunato and Navdeep Jaitly},
  eprint        = {1506.03134},
  archiveprefix = {arXiv},
  primaryclass  = {stat.ML},
  url           = {https://arxiv.org/abs/1506.03134}
}
```

```typst
// 当前情况：
#assert.eq(converted.keys(), ("type", "title", "author", "url", "serial-number"))
#assert.eq(converted.serial-number.keys(), ("arxiv",))
```

[gbt7714-bibtex-style][] 的说明文档有相同用法，并写「`gbt7714` 兼容 `biblatex` 的 `eprinttype` 字段，同时兼容 arXiv 和 Google Scholar 导出的预印本格式」，但当前 arXiv 与 Google Scholar 似乎都不会标注`primaryclass`。

GB/T 7714—2025 似乎也不要求著录这一信息，故忽略。

### 丢失`pubstate`

> [§2.2.2 Data Fields — `biblatex.pdf`][biblatex-2.2.2]
>
> `pubstate` field (key)
>
> The publication state of the work, e. g., ‘in press’. See § 4.9.2.11 (Publication State) for known publication states.

下例简化自 [gbt7714-bibtex-style][]，其中`pubstate = {prepublished}`会丢失。不过 [biblatex-gb7714-2025][] 没有类似用法。

```bib
@preprint{gbt7714.8.15.2:3,
  author        = {Jenkins, Stewart D. and Ruostekoski, Janne},
  title         = {Controlled Manipulation of Light by Cooperative Response of Atoms in an Optical Lattice},
  pubstate      = {prepublished},
  doi           = {10.48550/arXiv.1112.6136},
}
```

```typst
// 当前情况：
#assert.eq(converted.keys(), ("type", "title", "author", "serial-number"))
#assert.eq(converted.serial-number.keys(), ("doi",))
```

目前所有条目中，`pubstate`标了的都是`prepublished`，并且类型都是`@preprint`，所以`pubstate`其实冗余，故忽略。

### 丢失`shortjournal`

> [§2.2.2 Data Fields — `biblatex.pdf`][biblatex-2.2.2]
>
> `shortjournal` field (literal) Label field
>
> A short version or an acronym of the `journaltitle`. Not used by the standard bibliography styles.

下例简化自 [biblatex-gb7714-2025][]，其中`shortjournal`会丢失。[gbt7714-bibtex-style][] 亦有相同用法。

```bib
@article{gbt7714.8.5.3:8,
  title = {Jadeite-Bearing Metagabbro in Serpentinite Melange of the “{{Kurosegawa Belt}}” in {{Izumi Town}}, {{Yatsushiro City}}, {{Kumamoto Prefecture}}, Central {{Kyushu}}},
  author = {Saito, Makoto and Miyazaki, Kazuhiro},
  journaltitle = {Bulletin of the Geological Survey of Japan},
  shortjournal = {Bull. Geol. Surv. Jpn.},
}
```

```typst
// 当前情况：
#assert.ne(converted.parent.title, (
  value: "Bulletin of the Geological Survey of Japan",
  short: "Bull. Geol. Surv. Jpn.",
))
```

GB/T 7714—2025 允许缩写但不强求，示例大多不缩写，因此`shortjournal`很少用到，故忽略。

### `@dataset`丢失`journal`

下例简化自 [biblatex-gb7714-2025][]，其中`journal`会丢失。[gbt7714-bibtex-style][] 无类似用法。

```bib
@dataset{李皓2024语料库,
  title   = {ESDC：一种用于支持地学文献信息抽取的开放地球科学数据语料库},
  journal = {中国科学：地球科学},
  url     = {http://kns.cnki.net/kcms/detail/11.5842.P.20241113.0954.002.html}
}
```

```typst
#assert("parent" not in converted) // 当前情况
```

不过标准全文未引用上例，故忽略。

### 不识别某些`archiveprefix`

> [§2.2.5 Field Aliases — `biblatex.pdf`][biblatex-2.2.5]
>
> `archiveprefix` field (literal)
>
> An alias for `eprinttype`, provided for arXiv compatibility. See §§ 2.2.2 (Data Fields) and 3.14.7 (Electronic Publishing Information).
>
> [§2.2.2 Data Fields — `biblatex.pdf`][biblatex-2.2.2]
>
> `eprinttype` field (literal)
>
> The type of `eprint` identifier, e. g., the name of the archive, repository, service, or system the `eprint` field refers to. See § 3.14.7 (Electronic Publishing Information) for details. Also see `eprint` and `eprintclass`.

下例简化自 [biblatex-gb7714-2025][]，其中`archiveprefix = {bioRxiv}`会丢失。[gbt7714-bibtex-style][] 亦有相同用法。

```bib
@preprint{BLOSS2025trial,
  author        = {Bloss, C. S. And Wineinger, N. E. And Peters, M. And Others},
  archiveprefix = {bioRxiv},
  url           = {https://doi.org/10.1101/029983}
}
```

```typst
#assert.eq(converted.keys(), ("type", "author", "url",)) // 当前情况
```

bioRxiv 上导出的其实是`journal = {bioRxiv}`，故忽略。

存在类似问题的还有`archiveprefix = {PSSXiv}`，但目前所有这种条目都有其它字段标注了 PSSXiv，故也忽略。

### 不识别大写`AND`

> [§2.2.1 Data Types — `biblatex.pdf`][biblatex-2.2.1]
>
> **Name lists** are parsed and split up into the individual items at the `and` delimiter.

下例简化自 [biblatex-gb7714-2025][]，转换时`AND`未被理解为分隔符。[gbt7714-bibtex-style][] 无类似用法。

```bib
@dataset{刘时银2012水川,
  author    = {刘时银 AND 郭万钦 AND 许君利},
  title     = {中国第二次水川编目科学数据：2006--2011},
}
```

```yaml
刘时银2012水川:
  type: repository
  title: 中国第二次水川编目科学数据：2006–2011
  author:
    name: AND 许君利
    given-name: 刘
    prefix: 时银 AND 郭万钦
```

```typst
#assert.ne(converted.author, ("刘时银", "郭万钦", "许君利")) // 当前情况
```

正常都用小写`and`分隔，不必支持大写`AND`，故忽略。

[gbt7714-bibtex-style]: ./fixtures/gbt7714-bibtex-style.md
[biblatex-gb7714-2025]: ./fixtures/biblatex-gb7714-2025.md
[bithesis]: ./fixtures/bithesis.md

[btxdoc]: https://mirrors.ctan.org/biblio/bibtex/base/btxdoc.pdf

[biblatex-2.1.3]: https://mirrors.ctan.org/macros/latex/contrib/biblatex/doc/biblatex.pdf#subsubsection.2.1.3
[biblatex-2.2.1]: https://mirrors.ctan.org/macros/latex/contrib/biblatex/doc/biblatex.pdf#subsubsection.2.2.1
[biblatex-2.2.2]: https://mirrors.ctan.org/macros/latex/contrib/biblatex/doc/biblatex.pdf#subsubsection.2.2.2
[biblatex-2.2.3]: https://mirrors.ctan.org/macros/latex/contrib/biblatex/doc/biblatex.pdf#subsubsection.2.2.3
[biblatex-2.2.5]: https://mirrors.ctan.org/macros/latex/contrib/biblatex/doc/biblatex.pdf#subsubsection.2.2.5
[biblatex-3.7]: https://mirrors.ctan.org/macros/latex/contrib/biblatex/doc/biblatex.pdf#subsection.3.7
