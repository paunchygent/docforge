"""Convert DOCX files to Markdown in the same directory using Pandoc."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence


def discover_docx(paths: Sequence[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            yield from path.rglob("*.docx")
        elif path.suffix.lower() == ".docx":
            yield path
        else:
            print(f"[skip] Not a DOCX file: {path}", file=sys.stderr)


def convert_docx_to_md(docx_path: Path, pandoc: str = "pandoc") -> None:
    output_path = docx_path.with_suffix(".md")
    cmd = [pandoc, str(docx_path), "-t", "markdown", "-o", str(output_path)]
    subprocess.run(cmd, check=True)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="DOCX files or directories to convert recursively",
    )
    parser.add_argument(
        "--pandoc",
        default="pandoc",
        help="Path to the pandoc executable (default: pandoc)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    docx_files = list(discover_docx(args.paths))
    if not docx_files:
        print("No DOCX files found to convert.", file=sys.stderr)
        return 1

    for docx_file in docx_files:
        print(f"[convert] {docx_file}")
        convert_docx_to_md(docx_file, pandoc=args.pandoc)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
