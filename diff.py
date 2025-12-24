import re
from collections import OrderedDict
from dataclasses import dataclass
from typing import Literal

import regex  # for matching the Unicode script property

type Ignorance = Literal["page", "lang", "case", "卷", "escape", "space"]


def _ignore(x: str, /, *actions: Ignorance) -> str:
    for action in actions:
        match action:
            case "page":
                x = re.sub(r": [-\d]+", "", x)
            case "lang":
                x = _map_zh_to_bilingual(x)
            case "case":
                x = x.casefold()
            case "卷":
                x = x.replace(": 卷 ", ": ")
            case "escape":
                x = x.replace(R"\-", "-")
            case "space":
                x = x.replace(" ", "")
    return x


def _eq_ignore(a: str, b: str, /, *actions: Ignorance) -> bool:
    return _ignore(a, *actions) == _ignore(b, *actions)


@dataclass
class Difference:
    outputs: tuple[str, str]

    eq_ignore: list[OrderedDict[str, bool]]
    """A grouped ordered dict of equalities."""

    def __init__(self, a: str, b: str, /) -> None:
        assert a != b, f"No difference between outputs: {a} == {b}"
        self.outputs = (a, b)

        self.eq_ignore = list(
            map(
                OrderedDict,
                [
                    {
                        "page": _eq_ignore(a, b, "page"),
                        "page+space": _eq_ignore(a, b, "page", "space"),
                        "page+escape+space": _eq_ignore(
                            a, b, "page", "escape", "space"
                        ),
                    },
                    {
                        "lang": _eq_ignore(a, b, "lang"),
                        "lang+case": _eq_ignore(a, b, "lang", "case"),
                        "lang+case+space": _eq_ignore(a, b, "lang", "case", "space"),
                    },
                    {"page+lang": _eq_ignore(a, b, "page", "lang")},
                    {
                        "卷": _eq_ignore(a, b, "卷"),
                        "卷+space": _eq_ignore(a, b, "卷", "space"),
                        "卷+page+space": _eq_ignore(a, b, "卷", "page", "space"),
                    },
                    {"卷+page": _eq_ignore(a, b, "卷", "page")},
                    {
                        "escape": _eq_ignore(a, b, "escape"),
                        "escape+space": _eq_ignore(a, b, "escape", "space"),
                    },
                    {
                        "case": _eq_ignore(a, b, "case"),
                        "case+escape": _eq_ignore(a, b, "case", "escape"),
                        "case+escape+space": _eq_ignore(
                            a, b, "case", "escape", "space"
                        ),
                    },
                    {
                        "space": _eq_ignore(a, b, "space"),
                        "all": _eq_ignore(
                            a, b, "page", "lang", "case", "卷", "escape", "space"
                        ),
                    },
                ],
            )
        )

    def as_key(self) -> tuple[list[list[int]] | int | tuple[str, ...], ...]:
        return (
            [[1 - eq for eq in group.values()] for group in self.eq_ignore],
            (
                # The citation number
                int(n.group(1))
                if (n := re.match(r"^\[(\d+)\]", self.outputs[0])) is not None
                else -1
            ),
            self.outputs,
        )

    def reason(self) -> Ignorance | Literal["Unknown"] | str:
        for group in self.eq_ignore:
            for name, eq in group.items():
                if eq:
                    return name
        return "Unknown"

    def eq_emojis(self) -> str:
        flattened: dict[str, bool] = {}
        for group in self.eq_ignore:
            match list(set(group.values())):
                case [True]:
                    flattened[list(group.keys())[0]] = True
                case [False]:
                    flattened[list(group.keys())[-1]] = False
                case _:
                    # Push an interval in the group
                    # start: the end of the first continuous False sequence
                    # end: the start of the last continuous True sequence
                    start = None
                    for i, eq in enumerate(group.values()):
                        if eq:
                            start = i - 1  # start == -1 is okay
                            break
                    assert start is not None
                    end = None
                    for i_rev, eq in enumerate(reversed(group.values())):
                        if not eq:
                            i = len(group) - i_rev - 1
                            end = i + 2
                            break
                    assert end is not None

                    for i, (name, eq) in enumerate(group.items()):
                        if i < start:
                            continue
                        if i >= end:
                            break
                        flattened[name] = eq

        if "all" in flattened and not flattened["all"]:
            flattened.clear()
            flattened["all"] = False

        return f"equal if ignoring {', '.join(f'{name} {_emoji_bool(eq)}' for name, eq in flattened.items())}."


def _emoji_bool(x: bool) -> str:
    return "✅" if x else "❌"


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
            if len((num := m.group(2))) == 2 and num[0] == "1"
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
