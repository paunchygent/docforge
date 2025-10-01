# Repository Guidelines
Contributors help convert Tailwind-powered HTML handouts into polished PDFs/Docx deliverables. Follow these practices to keep Python tooling and assets cohesive.

## Project Structure & Module Organization
- `handout_templates/` stores production-ready templates; keep related HTML, partials, and data files together per template family.
- `scripts/` houses Typer CLIs and helper scripts (e.g., `handout_builder.py`, `build_css.py`); extend existing commands before adding new entry points.
- `utils/` contains reusable conversion utilities (`convert_html_to_pdf.py`, `sync_rules.py`) and Mermaid diagrams; favour composable functions over script-level logic.
- `rapport_till_kollegor/` retains sample datasets and generated reports—sanitize sensitive exports before committing.
- `TASKS/` tracks ongoing work notes. Update or add task files instead of overwriting history.

## Build, Test, and Development Commands
- `pdm install` provisions the Python environment; run after dependency updates.
- `pdm run build:css` will compile Tailwind assets once the pipeline is wired (current stub prints a TODO).
- `pdm run build:pdf` / `pdm run build:docx` kick off conversion workflows; until implemented they log placeholders—extend them when adding new formats.
- `pdm run lint`, `pdm run format`, and `pdm run typecheck` wrap Ruff and MyPy checks.
- `pdm run test` executes pytest with verbose logging.

## Coding Style & Naming Conventions
- Python files use 4-space indentation, 100-character lines, and Ruff-managed imports. Prefer explicit function and module names (`convert_*`, `render_*`).
- Keep Jinja templates and CSS class names kebab-case; prefix shared utility templates with `_`.
- Run `pdm run format` before committing to maintain consistent quoting and whitespace.

## Testing Guidelines
- Place tests under `tests/` following `test_*.py` patterns; mirror module paths for clarity.
- Use pytest fixtures for HTML fixtures and PDF snapshots; aim for coverage on parsing and conversion branches.
- Document manual QA steps when adding new template assets.

## Commit & Pull Request Guidelines
- Write imperative, scoped commit messages (`Add Typer command for PDF build`). Combine related template assets in one commit to keep history reviewable.
- PRs should summarize behaviour, note file outputs (PDF/Docx paths), and include before/after screenshots or rendered PDFs when UI changes occur.
- Link task files or issues from `TASKS/` in the PR description and call out any manual data cleanup required.
