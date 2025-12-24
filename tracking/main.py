from collections import Counter, deque
from pathlib import Path
from sys import stderr

from diff import Difference
from fixture import FILE, ensure_fixture
from load_entries import load_entries
from util import CACHE_DIR

from hayagriva import check_csl, reference


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
    ensure_fixture()

    expected_output = FILE.expected_output.read_text(encoding="utf-8")
    csl = FILE.csl.read_text(encoding="utf-8")
    entries = load_entries(FILE.entries)

    assert check_csl(csl) is None

    actual_output = reference(entries, csl)
    actual_output_file = CACHE_DIR / "actual-output.txt"
    actual_output_file.write_text(actual_output, encoding="utf-8")

    compare_outputs(expected_output, actual_output)
    print(
        f"""
You may also use VS Code to compare the outputs:
    code --diff {FILE.expected_output.relative_to(Path.cwd())} {actual_output_file.relative_to(Path.cwd())}
""",
        file=stderr,
    )
