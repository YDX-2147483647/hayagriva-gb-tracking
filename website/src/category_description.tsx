import type { Category } from './types'

export const descriptions: Record<Category, JSX.Element> = {
  lang: (
    <span>
      <code>等</code>/<code>et al.</code>等语言翻译问题
    </span>
  ),
  case: <span>大小写问题（例：英文机构名称被全大写）</span>,
  卷: (
    <span>
      多<code>卷</code>字（例：<code>第4册</code>误为<code>卷 第4册</code>）
    </span>
  ),
  han_space: (
    <span>
      中西字符间的空格差异（例：<code>第 1 卷</code>与<code>第1卷</code>）
    </span>
  ),
  code_space: (
    <span>
      代码中的空格错误（例：<code>GB/T 123</code>误为<code>GB/T123</code>）
    </span>
  ),
  escape: (
    <span>
      CSL-JSON中的<code>\-</code>被原样输出，而未转成<code>-</code>
    </span>
  ),
  num: (
    <span>
      数码格式错误（例：<code>011</code>误为<code>11</code>）
    </span>
  ),
  punct: (
    <span>
      标点符号缺少或错误（例：<code>[J].</code>缺点或<code>北京: 中华书局</code>
      缺冒号）
    </span>
  ),
  // Unknown is always shown last, so it's okay to use 以上.
  Unknown: <span>以上未列出的差异</span>,
}
