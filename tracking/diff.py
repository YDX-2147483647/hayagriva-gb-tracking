import re
from dataclasses import dataclass
from typing import Literal

import regex  # for matching the Unicode script property

from min_sub import minimize_seq

type Ignorance = Literal[
    "num", "lang", "case", "卷", "escape", "han_space", "code_space", "punct"
]

_IGNORANCE_ORDER: tuple[Ignorance, ...] = (
    *("lang", "case", "卷", "num"),
    *("escape", "han_space", "code_space"),
    # The following ignorances are redundant for hayagriva >= v0.8.1, kept only for generating legacy data.
    *("punct",),
)
"""The order of ignorances.

It makes sure that any subsequence of this list is safe for the `_ignore` function to apply in order.
"""


def _ignore(x: str, /, *actions: Ignorance) -> str:
    """Apply actions in order."""
    forbidden: set[Ignorance] = set()

    for action in actions:
        assert action not in forbidden, (
            f"{action} is forbidden due to previous actions."
        )

        match action:
            case "num":
                x = regex.sub(r": [-\d]+(\p{Punctuation})", r"\1", x)
            case "lang":
                x = _map_zh_to_bilingual(x)
            case "case":
                x = x.casefold()
            case "卷":
                x = x.replace(": 卷 ", ": ")
            case "escape":
                x = x.replace(R"\-", "-")
            case "han_space":
                x = regex.sub(r"(?<=\p{script=Han})\s+(?=\P{script=Han})", "", x)
                x = regex.sub(r"(?<=\P{script=Han})\s+(?=\p{script=Han})", "", x)
                # These actions assume the existence of spaces
                forbidden.update({"lang", "num", "卷"})
            case "code_space":
                x = re.sub(r"(?<=[\da-zA-Z])\s+(?=[\da-zA-Z])", "", x)
                # These actions assume the existence of spaces
                forbidden.update({"lang", "num", "卷"})
            case "punct":
                # We don't use `\p{Punctuation}\s*` here, because it's too general.
                x = regex.sub(r"((?<=\])\.|:)\s*", "", x)
        # lang should be the first if it exists
        forbidden.add("lang")
    return x


def _eq_ignore(a: str, b: str, /, *actions: Ignorance) -> bool:
    return _ignore(a, *actions) == _ignore(b, *actions)


@dataclass
class Difference:
    outputs: tuple[str, str]
    eq_ignore_min: tuple[Ignorance, ...] | None
    """The strongest equality between the outputs.
    Or equivalently, the minimal list of ignorances that makes them equal (weakly)."""

    def __init__(self, a: str, b: str, /) -> None:
        assert a != b, f"No difference between outputs: {a} == {b}"
        self.outputs = (a, b)

        # Determine the cause of the difference

        def f(actions: tuple[Ignorance, ...]) -> bool:
            return _eq_ignore(a, b, *actions)

        self.eq_ignore_min = minimize_seq(f, _IGNORANCE_ORDER)

    def cause(self) -> Literal["All", "Unknown"] | str:
        if self.eq_ignore_min == _IGNORANCE_ORDER:
            return "All"
        elif self.eq_ignore_min is None:
            return "Unknown"
        else:
            return "+".join(self.eq_ignore_min)

    def as_key(self) -> tuple[str | int | tuple[str | int, ...], ...]:
        return (
            (0, *(i not in self.eq_ignore_min for i in _IGNORANCE_ORDER))
            if self.eq_ignore_min is not None
            else (1,),
            (
                # The citation number
                int(n.group(1))
                if (n := re.match(r"^\[(\d+)\]", self.outputs[0])) is not None
                else -1
            ),
            self.outputs,
        )


def _map_zh_to_bilingual(x: str, /) -> str:
    """Convert a bibliography entry from (Simplified) Chinese to English if appropriate.

    See the `bilingual-bibliography` function provided by https://typst.app/universe/package/modern-nju-thesis/0.4.0/.
    """
    # 判断是否为中文文献：去除特定词组后，仍有至少两个连续汉字
    if regex.search(
        r"\p{script=Han}{2,}", re.sub(r"[等卷册和版本章期页篇译间者(不详)]", "", x)
    ):
        return x

    # 若不是中文文献，进行替换

    # 第○卷、第○册 → Vol. ○ 或 Bk. ○
    x = re.sub(
        r"(第\s?)?(\d+)\s?[卷册]",
        lambda m: ("Vol. " if "卷" in m.group(0) else "Bk. ") + m.group(2),
        x,
    )

    # 第○版、第○本 → 1st ed 格式
    x = re.sub(
        r"(\.?)\s*第?\s*(\d+)\s*[版本]",
        lambda m: (f"{m.group(1)} " if m.group(1) else "")
        + m.group(2)
        + (
            "th"
            if len(num := m.group(2)) == 2 and num[0] == "1"
            else {"1": "st", "2": "nd", "3": "rd"}.get(num[-1], "th")
        )
        + " ed",
        x,
    )

    # 跳过译者转换
    # 译者可能有多个，涉及折叠，tran(s)还有单复数之分。因此 bilingual-bibliography 的实现既复杂又不完善，故忽略。

    # 等 → et al.
    # 特殊处理：`等`后方接内容也需要译作 `et al.`，如 `等译` 需要翻译为 `et al. trans`
    # - 如果原文就是`等.`，则仅需简单替换，不需要额外处理
    # - 如果原文`等`后没有跟随英文标点，则需要补充一个空格
    # - 原文有英文句号时不需要重复句号，否则需要将匹配到的最后一个字符吐回来
    x = re.sub(
        r"等.",
        lambda m: "et al."
        + (" " if (last := m.group(0)[-1]) not in ".,;:[]/\\<>?() \"'" else "")
        + (last if last != "." else ""),
        x,
    )

    return x


assert _map_zh_to_bilingual("汉字. 第 3 卷") == "汉字. 第 3 卷"
assert _map_zh_to_bilingual("第 3 卷") == "Vol. 3"
assert _map_zh_to_bilingual("第13版") == "13th ed"
assert _map_zh_to_bilingual("第23版") == "23rd ed"
assert _map_zh_to_bilingual(". 2 版") == ". 2nd ed"
assert _map_zh_to_bilingual("WONG D M, 等. Foo") == "WONG D M, et al. Foo"
assert _map_zh_to_bilingual("WONG D M, 等 trans") == "WONG D M, et al. trans"
