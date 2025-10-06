# Agent Guidelines

Being in read-only sandbox means you can run any terminal command in sandbox but the user must then grant or deny each request.

## Repository Guidelines

Contributors help convert Tailwind-powered HTML handouts into polished PDFs/Docx deliverables. Follow these notes to keep Python, Tailwind, and documentation assets aligned.

## Project Structure & Module Organization

- `handout_templates/` holds production-ready HTML templates plus any data/partials required per handout family.
- `scripts/` contains operational tooling: CLI entry points at the root (`handout_builder.py`, `build_css.py`), conversion utilities in `scripts/converters/`, and maintenance helpers in `scripts/maintenance/`.
- `docs/` hosts converter manuals (e.g. `docs/converters/html_to_pdf.md`), Tailwind v4 notes, and supporting assets under `docs/assets/`.
- `build/` contains generated artefacts (PDF/Docx). Keep it untracked; outputs are regenerated on demand.
- `rapport_till_kollegor/` retains example datasets and generated reports—scrub sensitive exports before committing updates.
- `TASKS/` tracks worklog and plans; append new notes instead of rewriting history.

## Build, Test, and Development Commands

- `pnpm install` and `pdm install` set up Node + Python environments; rerun after dependency changes.
- Let pnpm manage semantic versions (use caret ranges by default; avoid hard pins unless a regression requires it).
- `pdm run build:css` wraps the Tailwind v4 CLI (`tailwindcss` via pnpm) and emits `styles/dist/tailwind.css`.
- `pdm run build:pdf` / `pdm run build:docx` invoke the Typer builder (`scripts/handout_builder.py`). Use the CLI flags (`--template`, `--verbose`) instead of creating new entry points.
- `pdm run lint`, `pdm run format`, and `pdm run typecheck` enforce Ruff and MyPy baselines.
- `pdm run test` executes the pytest suite; add fixtures for new template families.

## Coding Style & Naming Conventions

- Python: 4-space indentation, 100-character lines, Ruff-managed imports, and descriptive module names (`convert_*`, `render_*`).
- Tailwind: author source CSS in `styles/src/tailwind.css` using `@import "tailwindcss";` + `@theme` variables; keep class names kebab-case in templates.
- Templates: ensure Jinja blocks and front-matter keys read as lower_snake_case; prefix shared partials with `_`.

## Testing Guidelines

- Place automated tests under `tests/` following `test_*.py` naming; mirror module structure (`tests/converters/test_html_to_pdf.py`).
- Snapshot critical PDF/Docx outputs or compare metadata hashes; accompany binary checks with readable HTML fixtures.
- Document manual QA steps in `docs/` whenever you introduce a new handout style or conversion backend.

## Commit & Pull Request Guidelines

- Write imperative, scoped commit messages (`Add Tailwind v4 build runner`). Group related template/CSS assets in the same commit to simplify reviews.
- PRs should summarise behaviour changes, list generated artefacts (PDF/Docx paths), and include screenshots or rendered PDFs for visual updates.
- Link relevant `TASKS/` entries or GitHub issues in PR descriptions and note any required manual data cleanup or migration steps.
