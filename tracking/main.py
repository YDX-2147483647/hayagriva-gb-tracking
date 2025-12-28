from collections import deque
from dataclasses import asdict
from pathlib import Path
from sys import stderr

import click
from hayagriva import check_csl, reference

from .diff import Difference
from .fixture import FILE, ensure_fixture
from .history import InputVersion, OutputSummary
from .load_entries import load_entries
from .util import CACHE_DIR


def compare_outputs(
    expected_output: str,
    actual_output: str,
    *,
    show_summary: bool,
    show_details: bool,
    update_history: Path | None,
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

    if show_summary or update_history is not None:
        output_summary = OutputSummary.from_diff_list(
            diff_list=diff_list,
            n_entries=len(expected_output.splitlines()),
        )

        if show_summary:
            print("Summary of differences:")
            for d, count in output_summary.diff_counts.items():
                print(f"  {d:>10}: {count:3} ≈ {count / output_summary.n_diff:>3.0%}")

            print("\nSummary of combinations of differences:")
            for cause, count in output_summary.cause_counts.items():
                print(
                    f"  {count:3} ≈ {count / output_summary.n_diff:>3.0%} caused by {cause.replace('+', ' + ')}"
                )

            print(
                f"\n{output_summary.n_diff} of {output_summary.n_entries} entries differ."
            )

        if update_history is not None:
            from tomlkit import aot, document, dumps, parse, table

            if update_history.exists():
                doc = parse(update_history.read_text(encoding="utf-8"))
                records = doc["record"]
            else:
                doc = document()
                doc["version"] = 1
                records = aot()
                doc.add("record", records)

            tab = table()
            for k, v in asdict(InputVersion.build()).items():
                tab.add(k, v)
            tab.add("output", asdict(output_summary))

            records.append(tab)  # type: ignore

            update_history.write_text(dumps(doc), encoding="utf-8")


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
@click.option(
    "--update-history",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    default=None,
    help="Save the history of differences to a file.",
)
def main(
    show_details: bool,
    show_summary: bool,
    save_output: bool,
    update_history: Path | None,
) -> None:
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
            update_history=update_history,
        )

    if save_output:
        print(
            f"""
You may also use VS Code to compare the outputs:
    code --diff {FILE.expected_output.relative_to(Path.cwd())} {actual_output_file.relative_to(Path.cwd())}
""",
            file=stderr,
        )
