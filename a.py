import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from hayagriva import check_csl, reference

expected_output = "".join(
    "\t".join("".join(col.itertext()) for col in row) + "\n"
    for row in (
        ET.parse("expected-output.html").getroot().findall(".//div[@class='csl-entry']")
    )
)
Path("expected-output.txt").write_text(expected_output, encoding="utf-8")

csl = Path("GB-T-7714—2015（顺序编码，双语）.csl").read_text(encoding="utf-8")
assert check_csl(csl) is None

entries: list[dict[str, Any]] = json.loads(
    Path("gbt7714-data.json").read_text(encoding="utf-8")
)

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

actual_output = reference(json.dumps(entries, ensure_ascii=False), csl)
Path("actual-output.txt").write_text(actual_output, encoding="utf-8")

n = 0
for expected, actual in zip(expected_output.splitlines(), actual_output.splitlines()):
    if expected != actual:
        n += 1
        print(f"{n:3} Expected: {expected}\n    Actual:   {actual}\n")
