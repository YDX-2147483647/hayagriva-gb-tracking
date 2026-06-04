"""Convert from Bib(La)TeX `*.bib` to Hayagriva `*.yaml`

Usage:
    uv run convert.py
    cb | uv run convert.py -
"""

from collections import deque
from collections.abc import Generator
from pathlib import Path
from sys import argv, stdin

import hayagriva

CACHE_DIR = Path(__file__).parent.parent / "target/bib-interop-cache"
assert CACHE_DIR.exists() and CACHE_DIR.is_dir()


def split_bib(library: str) -> Generator[str]:
    """ "Split a full bib library into entries."""
    current: deque[str] = deque()
    for line in library.strip().splitlines():
        current.append(line)

        if line == "}" or line.startswith("}%"):
            yield "\n".join(current).strip()
            current.clear()

    remaining = "\n".join(current).strip()
    if remaining:
        yield remaining


def read_files() -> Generator[str]:
    if len(argv) > 1 and argv[1] == "-":
        yield stdin.read()
    else:
        for file in CACHE_DIR.glob("*.bib"):
            yield file.read_text(encoding="utf-8")


if __name__ == "__main__":
    failed = False
    for library in read_files():
        for bib in split_bib(library):
            try:
                yaml = hayagriva.biblatex_to_hayagriva(bib).strip()
                print(f"""
```bib
{bib}
```
```yaml
{yaml}
```
""")
                print()
            except ValueError as e:
                failed = True
                print(f"""
```bib
{bib}
```
Error: {e}
""")

    if failed:
        exit(1)
