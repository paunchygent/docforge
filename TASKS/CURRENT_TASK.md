# Current Task: Establish HTML→PDF/Docx Workflow Hub

## Context
- Stand up repository governance, Python/PDM tooling, and a Tailwind CSS v4 build so HTML handouts export cleanly to PDF/Docx through a single CLI.

## Worklog
- 2025-10-01T21:34+02:00 — Migrated conversion utilities into `scripts/converters/` and archived docs under `docs/` with new Tailwind v4 guidance.
- 2025-10-01T21:24+02:00 — Upgraded Tailwind pipeline to v4 (pnpm-driven CLI wrapper on Tailwind 4.x) and implemented `scripts/build_css.py` runner.
- 2025-10-01T18:13+02:00 — Installed Tailwind v3 CLI via pnpm along with @tailwindcss/cli, postcss, and autoprefixer.
- 2025-10-01T17:58+02:00 — Initialized root `package.json` via pnpm.
- 2025-10-01T17:37+02:00 — Updated frontend documentation to clarify Tailwind without Vite.
- 2025-10-01T16:50+02:00 — Added script stubs `scripts/build_css.py` and `scripts/handout_builder.py`.
- 2025-10-01T16:43+02:00 — Corrected `pyproject.toml` PDM script keys to use quoted names.
- 2025-10-01T16:40+02:00 — Drafted initial `pyproject.toml` with PDM configuration for HTML/PDF workflow.
- 2025-10-01T16:33+02:00 — Initialized governance scaffolding files under `.windsurf/rules/` and created `TASKS/` directory.

## Outstanding Questions
- How should front-matter metadata drive output naming (PDF vs Docx) inside the Typer build command?
- Do we need additional guardrails before enabling automatic Tailwind content discovery in larger repos?

## Next Actions
- Implement template rendering + conversion orchestration inside `scripts/handout_builder.py` (delegate to modules in `scripts.converters`).
- Create regression fixtures under `tests/` for HTML→PDF and Markdown→PDF flows, including binary diff strategy.
- Document manual QA checklist for new handouts in `docs/` so educators can verify layout before publishing.

## Acceptance Criteria
- `pdm run build:css` produces `styles/dist/tailwind.css` using Tailwind v4 with project-specific theme variables.
- `pdm run build:pdf` (or `build:docx`) renders at least one sample handout end-to-end without manual steps.
- Pytest suite exercises converter codepaths and passes on CI with coverage for backend selection logic.
