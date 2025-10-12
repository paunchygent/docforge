#!/usr/bin/env python3
"""Utility script to copy Markdown content into a plain-text file."""

import argparse
from pathlib import Path
from textwrap import TextWrapper


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
    parser.add_argument(
        "--width",
        type=int,
        default=80,
        help="Maximum line width for wrapped paragraphs (default: 80)",
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


def wrap_paragraphs(content: str, width: int) -> str:
    wrapper = TextWrapper(
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
        replace_whitespace=False,
    )
    wrapped: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if not paragraph:
            return
        text = " ".join(part.strip() for part in paragraph)
        if text:
            wrapped.extend(wrapper.fill(text).splitlines())
        else:
            wrapped.append("")
        paragraph.clear()

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        if not line:
            flush_paragraph()
            wrapped.append("")
            continue

        structural_prefixes = ("#", ">", "- ", "* ", "1. ", "    ", "```")
        if line.startswith(structural_prefixes):
            flush_paragraph()
            wrapped.append(line)
            continue

        paragraph.append(line)

    flush_paragraph()
    return "\n".join(wrapped)


def convert_markdown_to_text(input_path: Path, output_path: Path, width: int) -> None:
    content = input_path.read_text(encoding="utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wrapped_content = wrap_paragraphs(content, width=width)
    output_path.write_text(wrapped_content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    ensure_markdown_file(args.input)
    output_path = determine_output_path(args.input, args.output)
    convert_markdown_to_text(args.input, output_path, args.width)
    print(f"Wrote text file to: {output_path}")


if __name__ == "__main__":
    main()
