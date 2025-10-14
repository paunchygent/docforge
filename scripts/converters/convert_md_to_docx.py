#!/usr/bin/env python3
"""Convert a Markdown file to a Docx file using Pandoc."""

import sys
from pathlib import Path

import typer

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

BUILD_ROOT = PROJECT_ROOT / "build"
DOCX_OUTPUT_ROOT = BUILD_ROOT / "docx"

app = typer.Typer()

class ConversionError(RuntimeError):
    """Raised when a conversion step fails."""


def convert_md_to_docx(md_path: Path, output_path: Path) -> None:
    """Converts a Markdown file to a Docx file."""
    try:
        import pypandoc
    except ImportError as exc:
        raise ConversionError(
            "pypandoc is required for Docx generation. Run: pdm add pypandoc"
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        pypandoc.convert_file(
            str(md_path),
            "docx",
            outputfile=str(output_path),
            extra_args=["--standalone"],
        )
        typer.secho(
            f"Successfully converted {md_path.name} to {output_path.relative_to(PROJECT_ROOT)}",
            fg=typer.colors.GREEN,
        )
    except OSError as exc:
        raise ConversionError(
            "Pandoc CLI is missing. Install Pandoc for Docx conversion."
        ) from exc
    except RuntimeError as exc:
        raise ConversionError(f"Docx conversion failed for {md_path.name}: {exc}") from exc


@app.command()
def convert(
    input_file: Path = typer.Argument(..., help="Path to the input Markdown file."),
) -> None:
    """Convert a Markdown file to a Docx document."""
    if not input_file.exists() or not input_file.is_file():
        typer.secho(f"Error: Input file not found at {input_file}", fg=typer.colors.RED)
        raise typer.Exit(1)

    absolute_input = (PROJECT_ROOT / input_file).resolve()
    try:
        relative_parent = absolute_input.parent.relative_to(PROJECT_ROOT)
    except ValueError:
        typer.secho(
            f"Error: Input file must reside within project root {PROJECT_ROOT}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    output_dir = DOCX_OUTPUT_ROOT / relative_parent
    output_file = (output_dir / absolute_input.stem).with_suffix(".docx")

    try:
        convert_md_to_docx(absolute_input, output_file)
    except ConversionError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
