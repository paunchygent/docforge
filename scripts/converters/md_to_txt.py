#!/usr/bin/env python3
"""Utility script to copy Markdown content into a plain-text file."""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a .txt copy of a Markdown file",
    )
    parser.add_argument("input", type=Path, help="Path to the source Markdown file")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for the generated text file (defaults to the input path with .txt suffix)",
    )
    return parser.parse_args()


def ensure_markdown_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Input file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")
    if path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError(f"Input file is not a Markdown file: {path}")


def determine_output_path(input_path: Path, output_path: Path | None) -> Path:
    if output_path is None:
        return input_path.with_suffix(".txt")
    if output_path.is_dir():
        return output_path / input_path.with_suffix(".txt").name
    return output_path


def convert_markdown_to_text(input_path: Path, output_path: Path) -> None:
    content = input_path.read_text(encoding="utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    ensure_markdown_file(args.input)
    output_path = determine_output_path(args.input, args.output)
    convert_markdown_to_text(args.input, output_path)
    print(f"Wrote text file to: {output_path}")


if __name__ == "__main__":
    main()
