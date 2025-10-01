#!/usr/bin/env python3
"""Handout build CLI.

Coordinates Tailwind CSS builds and delegates to converter utilities in
`scripts/converters` to produce PDF/Docx artefacts from the handout templates.
"""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

import typer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.converters.convert_html_to_pdf import convert_html_to_pdf

app = typer.Typer(help="Manage handout template builds and conversions.")

TEMPLATES_ROOT = PROJECT_ROOT / "handout_templates"
BUILD_ROOT = PROJECT_ROOT / "build"
PDF_OUTPUT_ROOT = BUILD_ROOT / "pdf"
DOCX_OUTPUT_ROOT = BUILD_ROOT / "docx"
TAILWIND_SCRIPT = PROJECT_ROOT / "scripts" / "build_css.py"
VALID_TARGETS = {"pdf", "docx", "all"}


class BuildError(RuntimeError):
    """Raised when a build step fails."""


def _ensure_templates_root() -> None:
    if not TEMPLATES_ROOT.exists():
        raise BuildError(f"Template directory not found: {TEMPLATES_ROOT}")


def _discover_templates(filters: Sequence[str] | None) -> List[Path]:
    filters = [f.lower() for f in filters or [] if f]
    templates = sorted(TEMPLATES_ROOT.rglob("*.html"))

    if filters:
        templates = [
            path
            for path in templates
            if any(f in path.relative_to(TEMPLATES_ROOT).as_posix().lower() for f in filters)
        ]

    return templates


def _run_tailwind_build(skip_css: bool) -> None:
    if skip_css:
        typer.secho("Skipping Tailwind CSS build (per --skip-css).", fg=typer.colors.YELLOW)
        return

    if not TAILWIND_SCRIPT.exists():
        raise BuildError("Tailwind build helper script is missing. Re-run repository setup.")

    typer.echo("Building Tailwind CSS (pnpm run tailwind:build)…")
    try:
        subprocess.run([sys.executable, str(TAILWIND_SCRIPT)], cwd=PROJECT_ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        raise BuildError("Tailwind CSS build failed; see output above.") from exc


def _convert_html_to_docx(html_path: Path, output_path: Path) -> Tuple[Path, str]:
    try:
        import pypandoc
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise BuildError("pypandoc is required for Docx generation. Run: pdm add pypandoc") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        pypandoc.convert_file(
            str(html_path),
            "docx",
            outputfile=str(output_path),
            extra_args=["--standalone"],
        )
    except OSError as exc:  # pragma: no cover - pandoc binary missing
        raise BuildError(
            "Pandoc CLI is missing. Install Pandoc so pypandoc can perform Docx conversion."
        ) from exc
    except RuntimeError as exc:
        raise BuildError(f"Docx conversion failed for {html_path.name}: {exc}") from exc

    return output_path, "pypandoc"


def _build_pdfs(templates: Iterable[Path], verbose: bool) -> List[Tuple[Path, Path, str]]:
    results: List[Tuple[Path, Path, str]] = []
    for template in templates:
        relative = template.relative_to(TEMPLATES_ROOT)
        output_path = (PDF_OUTPUT_ROOT / relative).with_suffix(".pdf")
        typer.echo(f"  • {relative.as_posix()} → {output_path.relative_to(PROJECT_ROOT).as_posix()}")
        try:
            artefact, backend = convert_html_to_pdf(template, output_path, verbose=verbose)
        except Exception as exc:  # pragma: no cover - converter raises
            raise BuildError(f"PDF conversion failed for {relative.as_posix()}: {exc}") from exc
        results.append((template, artefact, backend))
    return results


def _build_docx(templates: Iterable[Path]) -> List[Tuple[Path, Path, str]]:
    results: List[Tuple[Path, Path, str]] = []
    for template in templates:
        relative = template.relative_to(TEMPLATES_ROOT)
        output_path = (DOCX_OUTPUT_ROOT / relative).with_suffix(".docx")
        typer.echo(f"  • {relative.as_posix()} → {output_path.relative_to(PROJECT_ROOT).as_posix()}")
        artefact, backend = _convert_html_to_docx(template, output_path)
        results.append((template, artefact, backend))
    return results


def _summarise(results: List[Tuple[Path, Path, str]], label: str) -> None:
    if not results:
        typer.secho(f"No {label} artefacts generated.", fg=typer.colors.YELLOW)
        return

    typer.secho(f"Generated {len(results)} {label} artefact(s):", fg=typer.colors.GREEN)
    for _, artefact, backend in results:
        rel = artefact.relative_to(PROJECT_ROOT)
        typer.echo(f"    - {rel.as_posix()} (backend: {backend})")


@app.command()
def build(
    target: str = typer.Argument(..., help="Output target: pdf, docx, or all."),
    template: List[str] = typer.Option(
        None,
        "--template",
        "-t",
        help="Filter templates by substring (case-insensitive). Repeat flag to combine filters.",
    ),
    skip_css: bool = typer.Option(False, help="Skip Tailwind CSS build step."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging for converters."),
) -> None:
    """Build the requested output artefacts for the discovered templates."""

    normalised_target = target.lower()
    if normalised_target not in VALID_TARGETS:
        raise typer.BadParameter(f"Target must be one of: {', '.join(sorted(VALID_TARGETS))}")

    try:
        _ensure_templates_root()
        templates = _discover_templates(template)
        if not templates:
            raise BuildError("No templates matched the selection criteria.")

        typer.echo(f"Found {len(templates)} template(s) to process.")

        if normalised_target in {"pdf", "all"}:
            _run_tailwind_build(skip_css=skip_css)

        pdf_results: List[Tuple[Path, Path, str]] = []
        docx_results: List[Tuple[Path, Path, str]] = []

        if normalised_target in {"pdf", "all"}:
            typer.secho("Generating PDF artefacts…", fg=typer.colors.CYAN)
            pdf_results = _build_pdfs(templates, verbose=verbose)

        if normalised_target in {"docx", "all"}:
            typer.secho("Generating Docx artefacts…", fg=typer.colors.CYAN)
            docx_results = _build_docx(templates)

        _summarise(pdf_results, "PDF")
        _summarise(docx_results, "Docx")

    except BuildError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc


@app.command()
def watch() -> None:
    """Watch mode placeholder until incremental rebuild logic is implemented."""
    typer.echo(
        "Watch mode is not ready yet. Use `pdm run build:css` and `pdm run build:pdf` for now."
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    app()
