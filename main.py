import json
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path
from sys import stderr
from typing import Any

from diff import Difference
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
