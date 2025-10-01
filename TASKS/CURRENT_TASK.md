# Current Task: Establish HTML→PDF/Docx Workflow Hub

## Context
- Set up repository governance, environments, and build tooling for HTML/Tailwind templates converted to PDF/Docx.

## Worklog
- 2025-10-01T18:13+02:00 — Installed Tailwind v3 CLI via pnpm along with @tailwindcss/cli, postcss, and autoprefixer.
- 2025-10-01T17:58+02:00 — Initialized root `package.json` via pnpm.
- 2025-10-01T17:37+02:00 — Updated frontend documentation to clarify Tailwind without Vite.
- 2025-10-01T16:50+02:00 — Added script stubs `scripts/build_css.py` and `scripts/handout_builder.py`.
- 2025-10-01T16:43+02:00 — Corrected `pyproject.toml` PDM script keys to use quoted names.
- 2025-10-01T16:40+02:00 — Drafted initial `pyproject.toml` with PDM configuration for HTML/PDF workflow.
- 2025-10-01T16:33+02:00 — Initialized governance scaffolding files under `.windsurf/rules/` and created `TASKS/` directory.

## Outstanding Questions
- None at this time.

## Next Actions
- Initialize Python project via PDM with required dependencies and scripts.
- Finalize pnpm Tailwind pipeline (configure config files, build script, and CSS sources).
- Implement unified CLI for template rendering and conversions.
