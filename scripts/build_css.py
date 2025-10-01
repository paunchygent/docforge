#!/usr/bin/env python3
"""Tailwind CSS build orchestrator.

Wraps the pnpm Tailwind CLI so Python tooling (PDM scripts, Typer CLI) can
trigger CSS builds in a consistent way. Supports one-off builds and watch mode.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STYLES_DIR = PROJECT_ROOT / "styles"
SRC_CSS = STYLES_DIR / "src" / "tailwind.css"
DIST_CSS = STYLES_DIR / "dist" / "tailwind.css"


def ensure_structure() -> None:
    """Make sure source/output directories exist before running Tailwind."""
    SRC_CSS.parent.mkdir(parents=True, exist_ok=True)
    DIST_CSS.parent.mkdir(parents=True, exist_ok=True)


def run_tailwind(watch: bool) -> int:
    """Invoke the configured pnpm script for Tailwind CSS."""
    pnpm = shutil.which("pnpm")
    if pnpm is None:
        print("pnpm is required to build Tailwind CSS. Install pnpm and retry.", file=sys.stderr)
        return 1

    script = "tailwind:watch" if watch else "tailwind:build"
    command = [pnpm, "run", script]

    try:
        return subprocess.run(command, cwd=PROJECT_ROOT, check=True).returncode
    except subprocess.CalledProcessError as exc:  # pragma: no cover - thin wrapper
        print(f"Tailwind CLI exited with code {exc.returncode}.", file=sys.stderr)
        return exc.returncode


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Tailwind CSS v4 pipeline.")
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Keep the Tailwind CLI running in watch mode.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ensure_structure()
    return run_tailwind(watch=args.watch)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
