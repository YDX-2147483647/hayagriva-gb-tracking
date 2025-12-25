import xml.etree.ElementTree as ET
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from sys import stderr

import httpx

from .util import CACHE_DIR

ZOTERO_CHINESE_REPO = "https://github.com/zotero-chinese/styles/raw/ce0786d7"
CSL_SANITIZER_WEBSITE = "https://typst-doc-cn.github.io/csl-sanitizer"

assert not ZOTERO_CHINESE_REPO.endswith("/")
assert not CSL_SANITIZER_WEBSITE.endswith("/")


@dataclass(frozen=True)
class _File:
    entries = CACHE_DIR / "gbt7714-data.json"
    csl = CACHE_DIR / "GB-T-7714—2015（顺序编码，双语）.csl"
    expected_output = CACHE_DIR / "expected-output.txt"


FILE = _File()


_download_message: str | None = (
    f"Hint: You can edit the constants in {Path(__file__).relative_to(Path.cwd())} if you meet network issues."
)


def _download(url: str) -> str:
    print(f"Downloading from {url} …", file=stderr)

    global _download_message
    if _download_message is not None:
        print(_download_message, file=stderr)
        _download_message = None

    return httpx.get(url, follow_redirects=True).text


def ensure_fixture() -> None:
    """Download required fixtures if it does not exist."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if not FILE.entries.exists():
        FILE.entries.write_text(
            _download(
                f"{ZOTERO_CHINESE_REPO}/lib/data/items/gbt7714-data.json",
            ),
            encoding="utf-8",
        )

    if not FILE.csl.exists():
        FILE.csl.write_text(
            _download(
                f"{CSL_SANITIZER_WEBSITE}/chinese/src/GB-T-7714—2015（顺序编码，双语）/GB-T-7714—2015（顺序编码，双语）.csl",
            ),
            encoding="utf-8",
        )
    csl_updated_at = (
        ET.parse(FILE.csl)
        .getroot()
        .find(
            "cs:info/cs:updated", namespaces={"cs": "http://purl.org/net/xbiblio/csl"}
        )
    )
    print(
        f"CSL version: {csl_updated_at.text if csl_updated_at is not None else '(unknown)'}",
        file=stderr,
    )

    if not FILE.expected_output.exists():
        index_md = _download(
            f"{ZOTERO_CHINESE_REPO}/src/GB-T-7714—2015（顺序编码，双语）/index.md",
        )
        FILE.expected_output.write_text(
            _extract_expected_output(index_md),
            encoding="utf-8",
        )


def _extract_gb_example(index_md: str) -> Generator[str]:
    """Extract “GB/T 7714—2015 示例文献” from `index.md`."""
    lines = iter(index_md.splitlines())

    while (line := next(lines, None)) is not None:
        if line == "### GB/T 7714—2015 示例文献":
            break

    while (line := next(lines, None)) is not None:
        if line == "<!-- PLACEHOLDER FOR WEBSITE - BEFORE RESULT -->":
            break

    while (line := next(lines, None)) is not None:
        if line != "<!-- PLACEHOLDER FOR WEBSITE - AFTER RESULT -->":
            yield line
        else:
            break


def _extract_expected_output(index_md: str) -> str:
    """Extract the plain-text expected output from the HTML `index.md`.

    At present, the support for CSL of typst/hayagriva is still quite limited. Therefore, we strip HTML styles for comparison.
    """
    html = "\n".join(_extract_gb_example(index_md))

    plain_text = "".join(
        "\t".join("".join(col.itertext()) for col in row) + "\n"
        for row in (ET.fromstring(html).findall(".//div[@class='csl-entry']"))
    )
    return plain_text


if __name__ == "__main__":
    ensure_fixture()
