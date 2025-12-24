import json
import re
import xml.etree.ElementTree as ET
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from sys import stderr
from typing import Any

import regex  # for matching the Unicode script property

from hayagriva import check_csl, reference


def extract_expected_output(file: Path) -> str:
    """Extract and save the plain-text expected output from the HTML file.

    At present, the support for CSL of typst/hayagriva is still quite limited. Therefore, we strip HTML styles for comparison.
    """
    expected_output = "".join(
        "\t".join("".join(col.itertext()) for col in row) + "\n"
        for row in (ET.parse(file).getroot().findall(".//div[@class='csl-entry']"))
    )
    file.with_suffix(".txt").write_text(expected_output, encoding="utf-8")
    return expected_output


def load_entries(file: Path) -> str:
    """Load and normalize CSL-JSON entries from file."""
    entries: list[dict[str, Any]] = json.loads(file.read_text(encoding="utf-8"))

    # Make entries acceptable by citationberg.
    for entry in entries:
        # citationberg requires DateValue has either `raw` or `date-parts`.
        # https://docs.rs/crate/citationberg/0.6.1/source/src/json.rs#161-173
        issued: dict[str, str | list] | None
        if (issued := entry.get("issued")) is not None and (
            set(issued.keys()) == {"literal"}
        ):
            assert entry["id"] in {"gbt7714.A.07:07", "gbt7714.A.07:08"}, (
                f"Trying to normalize a new entry in CSL-JSON: {entry['id']}. Check if it is expected."
            )
            issued["date-parts"] = [[-2161]]  # Add dummy `date-parts`

    # Sort entries to be consistent with zotero-chinese.
    # https://github.com/zotero-chinese/styles/blob/ce0786d7/lib/data/index.ts#L103
    entries.sort(key=lambda e: e["id"])

    return json.dumps(entries, ensure_ascii=False)


@dataclass
class Difference:
    outputs: tuple[str, str]
    eq_ignore_case: bool
    eq_ignore_space: bool
    eq_ignore_lang: bool
    eq_ignore_all: bool

    def __init__(self, a: str, b: str, /) -> None:
        assert a != b, f"No difference between outputs: {a} == {b}"
        self.outputs = (a, b)

        self.eq_ignore_case = a.casefold() == b.casefold()
        self.eq_ignore_space = a.replace(" ", "") == b.replace(" ", "")
        self.eq_ignore_lang = self._map_zh_to_bilingual(a) == self._map_zh_to_bilingual(
            b
        )

        self.eq_ignore_all = (
            self._map_zh_to_bilingual(a).replace(" ", "").casefold()
        ) == self._map_zh_to_bilingual(b).replace(" ", "").casefold()

    def as_key(self) -> tuple[int | tuple[str, ...], ...]:
        return (
            1 - self.eq_ignore_all,
            1 - self.eq_ignore_lang,
            1 - self.eq_ignore_case,
            1 - self.eq_ignore_space,
            (
                int(n.group(1))
                if (n := re.match(r"^\[(\d+)\]", self.outputs[0])) is not None
                else -1
            ),
            self.outputs,
        )

    def eq_emojis(self) -> str:
        return (
            f"equal if ignoring all {emoji_bool(self.eq_ignore_all)} or only"
            f" lang {emoji_bool(self.eq_ignore_lang)},"
            f" case {emoji_bool(self.eq_ignore_case)},"
            f" space {emoji_bool(self.eq_ignore_space)}."
        )

    @classmethod
    def _map_zh_to_bilingual(cls, x: str) -> str:
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
            r"(第\s?)?(\d+)\s?[版本]",
            lambda m: m.group(2)
            + (
                "th"
                if len(m.group(2)) == 2 and m.group(2)[0] == "1"
                else {"1": "st", "2": "nd", "3": "rd"}.get(m.group(2)[-1], "th")
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


assert Difference._map_zh_to_bilingual("汉字. 第 3 卷") == "汉字. 第 3 卷"
assert Difference._map_zh_to_bilingual("第 3 卷") == "Vol. 3"
assert Difference._map_zh_to_bilingual("第13版") == "13th ed"
assert Difference._map_zh_to_bilingual("第23版") == "23rd ed"
assert Difference._map_zh_to_bilingual("WONG D M, 等. Foo") == "WONG D M, et al. Foo"
assert Difference._map_zh_to_bilingual("WONG D M, 等 trans") == "WONG D M, et al. trans"


def emoji_bool(x: bool) -> str:
    return "✅" if x else "❌"


def compare_outputs(
    expected_output: str,
    actual_output: str,
) -> None:
    """Compare the expected and actual outputs, and print the differences."""

    diff_deque: deque[Difference] = deque()
    for expected, actual in zip(
        expected_output.splitlines(), actual_output.splitlines()
    ):
        if expected != actual:
            diff_deque.append(Difference(expected, actual))

    diff_list = list(diff_deque)
    diff_list.sort(key=Difference.as_key)

    for n, diff in enumerate(diff_list, start=1):
        print(f"""
{n:03} — {diff.eq_emojis()}
Expected: {diff.outputs[0]}
Actual:   {diff.outputs[1]}
""")


if __name__ == "__main__":
    expected_output = extract_expected_output(Path("expected-output.html"))

    csl = Path("GB-T-7714—2015（顺序编码，双语）.csl").read_text(encoding="utf-8")
    assert check_csl(csl) is None

    entries = load_entries(Path("gbt7714-data.json"))

    actual_output = reference(entries, csl)
    Path("actual-output.txt").write_text(actual_output, encoding="utf-8")

    compare_outputs(expected_output, actual_output)
    print(
        """
You may also use VS Code to compare the outputs:
    code --diff expected-output.txt actual-output.txt
""",
        file=stderr,
    )
