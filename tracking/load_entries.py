import json
import re
from collections import deque
from pathlib import Path
from typing import Any


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
            issued["date-parts"] = [[-2161]]  # Add dummy `date-parts` (`2162公元前`)

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
                        if key.startswith("tex.") and (
                            key_trimmed := key.removeprefix("tex.")
                        ) in {"DOI", "doi", "location", "institution"}:
                            key = key_trimmed

                        if key == "doi":
                            key = "DOI"

                        if key == "Book Title":
                            key = "container-title"

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
                    and (
                        key not in entry
                        # These are special types used by GB-T-7714—2015（顺序编码，双语）.csl.
                        or (key == "type" and value in {"collection", "periodical"})
                    )
                    and key
                    not in {
                        "tex.entrytype",
                        "number",
                        "tex.author_transliteration_en",
                        "tex.title_translation_en",
                        "tex.journal_translation_en",
                        "tex.eid",
                        "PMID",
                        "CSTR",
                        "tex.cstr",
                        "tex.holder",
                        "tex.number",
                        "archive-place",
                        "dimensions",
                        "version",
                    }
                    # `original-author` is too complex to be parsed. It may contain `||` or span multiple lines.
                    and not key.startswith("original-")
                ):
                    assert key in {
                        "DOI",
                        "page",
                        "editor",
                        "container-title",
                        "type",
                        "issue",
                        "jurisdiction",
                        "location",
                        "volume",
                        "institution",
                    }, (
                        f"Trying to extract a new cheater data from the note field in CSL-JSON: “{line}” of {entry['id']}. Check if it is expected."
                    )
                    entry[key] = value
                else:
                    note_rest.append(line)

            if note_rest:
                entry["note"] = "\n".join(note_rest)
            else:
                del entry["note"]

    return json.dumps(entries, ensure_ascii=False)
