#!/usr/bin/env python3
"""
PDF to Markdown converter.

Extracts text from PDF files and converts them to Markdown format,
preserving basic structure like headings and paragraphs.
"""

import re
from pathlib import Path
from typing import Optional

import pymupdf  # PyMuPDF
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer(help="Convert PDF files to Markdown format")
console = Console()


def clean_text(text: str) -> str:
    """Clean extracted text by removing excessive whitespace and normalizing."""
    # Remove multiple spaces
    text = re.sub(r" +", " ", text)
    # Remove multiple newlines (keep max 2 for paragraph breaks)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove trailing/leading whitespace from lines
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(lines)


def detect_heading(text: str, font_size: float, avg_font_size: float) -> Optional[int]:
    """
    Detect if text is a heading based on font size.
    Returns heading level (1-3) or None if not a heading.
    """
    if not text or len(text.strip()) > 100:  # Headings are usually short
        return None

    # If font is significantly larger than average, it's likely a heading
    if font_size > avg_font_size * 1.3:
        return 1
    elif font_size > avg_font_size * 1.15:
        return 2
    elif font_size > avg_font_size * 1.05:
        return 3

    return None


def extract_text_with_structure(pdf_path: Path) -> str:
    """
    Extract text from PDF with basic structure detection.
    Attempts to identify headings based on font size.
    """
    doc = pymupdf.open(pdf_path)
    markdown_content = []

    # Calculate average font size across document
    font_sizes = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        font_sizes.append(span.get("size", 12))

    avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 12

    # Extract text with structure
    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block.get("type") == 0:  # Text block
                block_text = []
                block_font_size = 12

                for line in block.get("lines", []):
                    line_text = []
                    for span in line.get("spans", []):
                        text = span.get("text", "")
                        block_font_size = span.get("size", 12)
                        line_text.append(text)

                    if line_text:
                        block_text.append(" ".join(line_text))

                if block_text:
                    full_text = " ".join(block_text).strip()
                    if full_text:
                        # Check if this is a heading
                        heading_level = detect_heading(
                            full_text, block_font_size, avg_font_size
                        )
                        if heading_level:
                            markdown_content.append(f"{'#' * heading_level} {full_text}")
                        else:
                            markdown_content.append(full_text)

                        markdown_content.append("")  # Add blank line after block

    doc.close()

    # Join and clean the content
    content = "\n".join(markdown_content)
    return clean_text(content)


def convert_pdf_to_markdown(
    pdf_path: Path,
    output_path: Optional[Path] = None,
    overwrite: bool = False,
) -> Path:
    """
    Convert a PDF file to Markdown.

    Args:
        pdf_path: Path to the PDF file
        output_path: Optional output path for the Markdown file
        overwrite: Whether to overwrite existing files

    Returns:
        Path to the created Markdown file
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Determine output path
    if output_path is None:
        output_path = pdf_path.with_suffix(".md")

    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Output file already exists: {output_path}. Use --overwrite to replace."
        )

    # Extract text with structure
    console.print(f"[cyan]Extracting text from:[/cyan] {pdf_path.name}")
    markdown_content = extract_text_with_structure(pdf_path)

    # Add metadata header
    header = f"""---
source: {pdf_path.name}
converted: {Path(__file__).name}
---

"""
    markdown_content = header + markdown_content

    # Write to file
    output_path.write_text(markdown_content, encoding="utf-8")
    console.print(f"[green]✓ Created:[/green] {output_path}")

    return output_path


@app.command()
def convert(
    pdf_file: Path = typer.Argument(..., help="Path to PDF file or directory"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output path for Markdown file"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-f", help="Overwrite existing files"
    ),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Process directories recursively"
    ),
) -> None:
    """Convert PDF file(s) to Markdown format."""
    try:
        if pdf_file.is_file():
            # Single file conversion
            convert_pdf_to_markdown(pdf_file, output, overwrite)

        elif pdf_file.is_dir():
            # Directory conversion
            pattern = "**/*.pdf" if recursive else "*.pdf"
            pdf_files = list(pdf_file.glob(pattern))

            if not pdf_files:
                console.print(f"[yellow]No PDF files found in {pdf_file}[/yellow]")
                return

            console.print(f"[cyan]Found {len(pdf_files)} PDF file(s)[/cyan]\n")

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Converting...", total=len(pdf_files))

                for pdf in pdf_files:
                    try:
                        convert_pdf_to_markdown(pdf, overwrite=overwrite)
                        progress.advance(task)
                    except Exception as e:
                        console.print(f"[red]✗ Error converting {pdf.name}: {e}[/red]")

            console.print(f"\n[green]✓ Conversion complete![/green]")

        else:
            console.print(f"[red]Error: {pdf_file} is not a file or directory[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
