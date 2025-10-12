#!/usr/bin/env python3
"""Extract text from an image using Tesseract OCR."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image as PILImage
import pytesseract


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract text content from an image file using Tesseract OCR.",
    )
    parser.add_argument(
        "image",
        type=Path,
        help="Path to the source image (e.g. JPEG, PNG).",
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="eng",
        help="Tesseract language code to use (default: eng).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help=(
            "Optional path for the generated text file "
            "(defaults to the image path with .txt suffix)."
        ),
    )
    return parser.parse_args()


def ensure_image_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Image file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Image path is not a file: {path}")


def determine_output_path(image_path: Path, output_path: Path | None) -> Path:
    if output_path is None:
        return image_path.with_suffix(".txt")
    if output_path.is_dir():
        return output_path / image_path.with_suffix(".txt").name
    return output_path


def extract_text(image_path: Path, language: str) -> str:
    with PILImage.open(image_path) as img:
        rgb_image = img.convert("RGB")
        return pytesseract.image_to_string(rgb_image, lang=language)


def main() -> None:
    args = parse_args()
    ensure_image_file(args.image)
    output_path = determine_output_path(args.image, args.output)
    text = extract_text(args.image, args.lang)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_text = text.rstrip("\n") + "\n"
    output_path.write_text(cleaned_text, encoding="utf-8")
    print(f"Wrote OCR text to: {output_path}")


if __name__ == "__main__":
    main()
