from collections import Counter, deque
from itertools import chain
from pathlib import Path
from sys import stderr

import click
from hayagriva import check_csl, reference

from .diff import Difference
from .fixture import FILE, ensure_fixture
from .load_entries import load_entries
from .util import CACHE_DIR


def compare_outputs(
    expected_output: str, actual_output: str, *, show_summary: bool, show_details: bool
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

    if show_details:
        for n, diff in enumerate(diff_list, start=1):
            print(f"""
{n:03} — cause: {diff.cause()}
Expected: {diff.outputs[0]}
Actual:   {diff.outputs[1]}
""")

    if show_summary:
        print("Summary of differences:")
        differences = Counter(
            chain.from_iterable(
                d.eq_ignore_min if d.eq_ignore_min is not None else ("Unknown",)
                for d in diff_list
            )
        )
        for d, count in differences.most_common():
            if d != "Unknown":
                print(f"  {d:>10}: {count:3} ≈ {count / len(diff_list):>3.0%}")
        if (count := differences.get("Unknown")) is not None:
            print(f"  {'Unknown':>10}: {count:3} ≈ {count / len(diff_list):>3.0%}")

        print("\nSummary of combinations of differences:")
        causes = Counter(d.cause() for d in diff_list)
        for cause, count in causes.most_common():
            if cause != "Unknown":
                print(
                    f"  {count:3} ≈ {count / len(diff_list):>3.0%} caused by {cause.replace('+', ' + ')}"
                )
        if (count := causes.get("Unknown")) is not None:
            print(f"  {count:3} ≈ {count / len(diff_list):>3.0%} caused by Unknown")

        print(f"\nTotal differences: {len(diff_list)}")


@click.command()
@click.option(
    "--show-details/--hide-details",
    default=False,
    is_flag=True,
    help="Show detailed differences. (default: false)",
)
@click.option(
    "--show-summary/--hide-summary",
    default=True,
    is_flag=True,
    help="Show a summary of differences. (default: true)",
)
@click.option(
    "--save-output/--no-save-output",
    default=True,
    is_flag=True,
    help="Save the actual output. (default: true)",
)
def main(show_details: bool, show_summary: bool, save_output: bool) -> None:
    ensure_fixture()

    expected_output = FILE.expected_output.read_text(encoding="utf-8")
    csl = FILE.csl.read_text(encoding="utf-8")
    entries = load_entries(FILE.entries)

    assert check_csl(csl) is None

    actual_output = reference(entries, csl)
    actual_output_file = CACHE_DIR / "actual-output.txt"
    if save_output:
        actual_output_file.write_text(actual_output, encoding="utf-8")

    if show_summary or show_details:
        compare_outputs(
            expected_output,
            actual_output,
            show_summary=show_summary,
            show_details=show_details,
        )

    if save_output:
        print(
            f"""
You may also use VS Code to compare the outputs:
    code --diff {FILE.expected_output.relative_to(Path.cwd())} {actual_output_file.relative_to(Path.cwd())}
""",
            file=stderr,
        )
