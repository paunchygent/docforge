#!/usr/bin/env python3
"""Handout build CLI stub.

This Typer application coordinates template rendering and delegates to tools in
`scripts.converters`. Commands are placeholder stubs until the workflow is wired up.
"""

from __future__ import annotations

import typer

app = typer.Typer(help="Manage handout template builds and conversions.")


def _not_implemented(action: str) -> None:
    """Common helper for placeholder commands."""
    typer.echo(
        f"{action} is not implemented yet. Configure the build workflow and update "
        "scripts/handout_builder.py accordingly."
    )


@app.command()
def build(
    target: str = typer.Argument(..., help="Output target: pdf, docx, or all."),
) -> None:
    """Build the requested output format(s)."""
    _not_implemented(f"Build pipeline for '{target}'")


@app.command()
def watch() -> None:
    """Watch templates for changes and rebuild automatically."""
    _not_implemented("Watch mode")


if __name__ == "__main__":
    app()
