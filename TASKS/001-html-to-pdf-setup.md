# Task 001: HTML to PDF/Docx Workflow Setup

## Objective
Create a structured mono-repo that manages HTML templates with Tailwind CSS and automates conversion to PDF and Docx outputs for educational and research documentation.

## Requirements
- Use PDM for Python dependency management and CLI orchestration.
- Use pnpm + Tailwind + Vite for frontend CSS compilation and preview.
- Provide conversion pathways via WeasyPrint (PDF) and Pandoc/DocxTpl (Docx).
- Maintain governance per `.windsurf/rules/` and task documentation standards.

## Acceptance Criteria
- Governance directories (`.windsurf/`, `TASKS/`) populated with baseline rules/documents.
- `pyproject.toml` initialized with scripts for build/lint/test.
- Tailwind pipeline configured and integrated with Python CLI commands.
- CLI scripts documented and capable of generating sample outputs from existing templates.
- Tests and lint commands runnable via `pdm run` with initial coverage of conversion utilities.

## Checklist
- [ ] Governance scaffolding committed
- [ ] Python environment configured
- [ ] Frontend tooling configured
- [ ] CLI workflow implemented
- [ ] Validation tests executed (`pdm run pytest -s`)
