#!/usr/bin/env python3
"""
Advanced PDF to Markdown converter using IBM Docling.

Converts PDF files to Markdown format using Docling's AI-powered document
understanding, preserving complex structures like tables, figures, and citations.
Ideal for academic papers and technical documents.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.document_converter import DocumentConverter, PdfFormatOption
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

app = typer.Typer(help="Convert PDF files to Markdown using IBM Docling")
console = Console()


def convert_pdf_to_markdown(
    pdf_path: Path,
    output_path: Optional[Path] = None,
    overwrite: bool = False,
) -> Path:
    """
    Convert a PDF file to Markdown using Docling.

    Args:
        pdf_path: Path to the PDF file
        output_path: Optional output path for the Markdown file
        overwrite: Whether to overwrite existing files

    Returns:
        Path to the created Markdown file
    """
    logger.info(f"Starting conversion: {pdf_path.name}")

    if not pdf_path.exists():
        logger.error(f"PDF file not found: {pdf_path}")
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Determine output path
    if output_path is None:
        output_path = pdf_path.with_suffix(".md")

    if output_path.exists() and not overwrite:
        logger.warning(f"Output file already exists: {output_path}")
        raise FileExistsError(
            f"Output file already exists: {output_path}. Use --overwrite to replace."
        )

    logger.info(f"Output will be saved to: {output_path}")

    # Configure pipeline for academic papers (optimized for speed and quality)
    logger.info("Configuring Docling pipeline (OCR disabled, fast table mode)")
    pipeline_options = PdfPipelineOptions()
    # Disable OCR for digital PDFs (academic papers are typically digital)
    pipeline_options.do_ocr = False
    # Keep table extraction for research papers
    pipeline_options.do_table_structure = True
    # Faster table processing
    pipeline_options.table_structure_options.mode = TableFormerMode.FAST

    # Create format options
    format_options = {
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }

    # Convert PDF using Docling
    console.print(f"[cyan]Converting with Docling:[/cyan] {pdf_path.name}")
    logger.info("Initializing DocumentConverter...")

    try:
        converter = DocumentConverter(format_options=format_options)
        logger.info(f"Converting PDF: {pdf_path} (this may take a few minutes)")
        result = converter.convert(str(pdf_path))
        logger.info(f"Conversion status: {result.status}")

        logger.info("Exporting to markdown format...")
        markdown_content = result.document.export_to_markdown()
        logger.info(f"Markdown export complete ({len(markdown_content):,} characters)")
    except Exception as e:
        logger.error(f"Conversion failed: {e}", exc_info=True)
        console.print(f"[red]✗ Conversion failed:[/red] {e}")
        raise

    # Add metadata header
    header = f"""---
source: {pdf_path.name}
converted_with: IBM Docling
converter_script: {Path(__file__).name}
conversion_date: {datetime.now().isoformat()}
---

"""
    markdown_content = header + markdown_content

    # Write to file
    logger.info(f"Writing markdown to file: {output_path}")
    output_path.write_text(markdown_content, encoding="utf-8")

    # Validate output
    file_size = output_path.stat().st_size
    if file_size == 0:
        logger.error(f"Conversion produced empty file: {output_path}")
        raise RuntimeError(f"Conversion produced empty file: {output_path}")

    logger.info(f"Conversion successful! Output size: {file_size:,} bytes")
    console.print(f"[green]✓ Created:[/green] {output_path}")
    console.print(f"  Size: {file_size:,} bytes")

    return output_path


@app.command()
def convert(
    pdf_file: Path = typer.Argument(..., help="Path to PDF file or directory"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output directory for Markdown files"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-f", help="Overwrite existing files"
    ),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Process directories recursively"
    ),
) -> None:
    """Convert PDF file(s) to Markdown using IBM Docling."""
    logger.info("=== Docling PDF to Markdown Converter ===")

    try:
        if pdf_file.is_file():
            # Single file conversion
            logger.info(f"Single file mode: {pdf_file}")
            output_path = None
            if output:
                # If output is specified, treat as directory or file
                if output.is_dir() or (not output.exists() and not output.suffix):
                    output.mkdir(parents=True, exist_ok=True)
                    output_path = output / pdf_file.with_suffix(".md").name
                else:
                    output_path = output

            convert_pdf_to_markdown(pdf_file, output_path, overwrite)

        elif pdf_file.is_dir():
            # Directory conversion
            logger.info(f"Batch mode: Processing directory {pdf_file}")
            pattern = "**/*.pdf" if recursive else "*.pdf"
            logger.info(f"Using pattern: {pattern}")
            pdf_files = list(pdf_file.glob(pattern))

            if not pdf_files:
                logger.warning(f"No PDF files found in {pdf_file}")
                console.print(f"[yellow]No PDF files found in[/yellow] {pdf_file}")
                return

            # Create output directory if specified
            output_dir = output if output else pdf_file
            if output:
                logger.info(f"Creating output directory: {output_dir}")
                output_dir.mkdir(parents=True, exist_ok=True)

            logger.info(f"Found {len(pdf_files)} PDF file(s) to convert")
            console.print(f"[cyan]Found {len(pdf_files)} PDF file(s)[/cyan]")
            console.print(f"[cyan]Output directory:[/cyan] {output_dir}\n")

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Converting...", total=len(pdf_files))

                for idx, pdf in enumerate(pdf_files, 1):
                    logger.info(f"Processing file {idx}/{len(pdf_files)}: {pdf.name}")
                    try:
                        # Preserve relative directory structure if recursive
                        if recursive and output:
                            rel_path = pdf.relative_to(pdf_file)
                            output_path = output_dir / rel_path.with_suffix(".md")
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                        else:
                            output_path = output_dir / pdf.with_suffix(".md").name

                        convert_pdf_to_markdown(pdf, output_path, overwrite=overwrite)
                        logger.info(f"Successfully converted {pdf.name}")
                        progress.advance(task)
                    except Exception as e:
                        logger.error(f"Failed to convert {pdf.name}: {e}")
                        console.print(f"[red]✗ Error converting {pdf.name}: {e}[/red]")

            logger.info("Batch conversion complete!")
            console.print(f"\n[green]✓ Conversion complete![/green]")

        else:
            logger.error(f"{pdf_file} is not a file or directory")
            console.print(f"[red]Error: {pdf_file} is not a file or directory[/red]")
            raise typer.Exit(1)

    except Exception as e:
        logger.error(f"Conversion failed with error: {e}", exc_info=True)
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
