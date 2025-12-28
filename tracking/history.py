import re
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from itertools import chain
from pathlib import Path
from pprint import pp
from typing import Literal, Self

import tomllib

from .diff import Difference, Ignorance
from .fixture import FILE, ZOTERO_CHINESE_REPO


@dataclass
class InputVersion:
    entries_rev: str
    """A string describing the git revision for entries and the CSL style."""
    csl_updated_at: str
    """The `<updated>` field in the CSL style, an ISO datetime with timezone, kept in its original form."""
    hayagriva_source: str
    """The exact revision of the hayagriva rust library, as a Cargo.lock-style source URL."""

    @classmethod
    def build(cls) -> Self:
        entries_rev = ZOTERO_CHINESE_REPO.split("/")[-1]
        assert re.match(r"^[0-9a-f]{7,}$", entries_rev)

        csl_updated_at = (
            ET.parse(FILE.csl)
            .getroot()
            .find(
                "cs:info/cs:updated",
                namespaces={"cs": "http://purl.org/net/xbiblio/csl"},
            )
        )
        assert csl_updated_at is not None and csl_updated_at.text is not None
        assert datetime.fromisoformat(csl_updated_at.text).tzname() is not None

        cargo_packages: list[dict[Literal["name", "source"], str]] = tomllib.loads(
            Path(__file__)
            .parent.parent.joinpath("Cargo.lock")
            .read_text(encoding="utf-8")
        )["package"]
        hayagriva_source = next(
            pkg for pkg in cargo_packages if pkg["name"] == "hayagriva"
        )["source"]
        assert hayagriva_source.startswith("git+https://")

        return cls(
            entries_rev=f"zotero-chinese/styles#{entries_rev}",
            csl_updated_at=csl_updated_at.text,
            hayagriva_source=hayagriva_source,
        )


@dataclass
class OutputSummary:
    n_entries: int
    """Number of bibliography entries processed."""
    n_diff: int
    """Total number of different entires."""
    diff_counts: dict[Ignorance | Literal["Unknown"], int]
    """Numbers of types of differences, in descending order, with Unknown at the end if it exists."""
    cause_counts: dict[Literal["All", "Unknown"] | str, int]
    """Numbers of causes (combinations of differences), in descending order, with Unknown at the end if it exists."""

    def __init__(
        self,
        n_entries: int,
        diff_counts: dict[Ignorance | Literal["Unknown"], int],
        cause_counts: dict[Literal["All", "Unknown"] | str, int],
    ) -> None:
        """
        `diff_counts` and `cause_counts` can be unordered.
        """
        self.n_entries = n_entries
        self.n_diff = sum(cause_counts.values())

        self.diff_counts = {
            diff: count
            for diff, count in sorted(
                diff_counts.items(), key=lambda x: (x[0] == "Unknown", -x[1])
            )
        }

        self.cause_counts = {
            cause: count
            for cause, count in sorted(
                cause_counts.items(), key=lambda x: (x[0] == "Unknown", -x[1])
            )
        }

    @classmethod
    def from_diff_list(cls, diff_list: list[Difference], n_entries: int) -> Self:
        differences: Counter[Ignorance | Literal["Unknown"]] = Counter(
            chain.from_iterable(
                d.eq_ignore_min if d.eq_ignore_min is not None else ("Unknown",)  # type: ignore
                for d in diff_list
            )
        )
        causes = Counter(d.cause() for d in diff_list)

        return cls(
            n_entries=n_entries,
            diff_counts=dict(differences),
            cause_counts=dict(causes),
        )


if __name__ == "__main__":
    print("Current input:")
    input_version = InputVersion.build()
    pp(input_version)
