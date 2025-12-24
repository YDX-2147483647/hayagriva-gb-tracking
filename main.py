import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, deque
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

        # Extract cheater data from the note field
        note_raw: str | None
        if (note_raw := entry.get("note")) is not None and (
            note := note_raw.splitlines()
        ):
            note_rest: deque[str] = deque()
            for line in note:
                # Parse line
                match line.split(": ", maxsplit=1):
                    case [key, value]:
                        pass
                    case [value] if re.match(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", value):
                        key = "DOI"
                    case _:
                        note_rest.append(line)
                        continue

                # Process line
                if (
                    key
                    and value
                    and key not in entry
                    and key not in {"tex.entrytype", "issue"}
                ):
                    assert key in {"DOI", "page", "editor", "container-title"}, (
                        f"Trying to extract a new cheater data from the note field in CSL-JSON: “{line}” of {entry['id']}. Check if it is expected."
                    )
                    entry[key] = value
                else:
                    note_rest.append(line)

            if note_rest:
                entry["note"] = "\n".join(note_rest)
            else:
                del entry["note"]

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
Cause: {diff.cause()}
""")

    print("Summary of differences:")
    causes = Counter(d.cause() for d in diff_list)
    for cause, count in causes.most_common():
        print(
            f"- {count:3} ≈ {count / len(diff_list):>3.0%} caused by {cause.replace('+', ' + ')}"
        )
    print(f"Total differences: {len(diff_list)}")


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
