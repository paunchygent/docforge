# Current Task: Establish HTML→PDF/Docx Workflow Hub

## Context
- Stand up repository governance, Python/PDM tooling, and a Tailwind CSS v4 build so HTML handouts export cleanly to PDF/Docx through a single CLI.

## Worklog
- 2025-10-13T15:35+02:00 — Justerade `handout_templates/instuderingsfrågor_templates/tidslinje.html` med detaljerad renässansuppdelning i en kolumn, moderniserad framåtblick (upplysning + 1800-tal) och legendlayout som speglar enkel-sidemallen.
- 2025-10-13T15:05+02:00 — Uppdaterade `handout_templates/instuderingsfrågor_templates/tidslinje.html` till en förlängd enkelsideslayout (297×625 mm) i linje med kompaktmallen och säkrade att sektioner inte bryts över sidor.
- 2025-10-13T00:18+02:00 — Omarbetade introduktions- och Dante-föreläsningarna: expanderade Island-avsnittet med konkreta exempel (Gunnar, Chandler-koppling), utvecklade riddarromaner och Birgitta med mer substans, förbättrade Dantes biografiska kontext (exil, Beatrice), fördjupade strukturförklaringar (terzinen som kedja, treenighet), omskrev Purgatorio och Paradiso med mer dramatik och känslomässig tyngd, förstärkte avslutningen om medeltid/renässans-bryggningen.
- 2025-10-13T00:11+02:00 — Genererade TXT- och PDF-versioner av `föreläsningar_medeltiden_renässansen.md` med `md_to_txt.py` och `convert_md_to_pdf.py`; PDF-konvertering via pypandoc→HTML→WeasyPrint med default CSS-styling för A4-format (79KB PDF, 30KB TXT).
- 2025-10-13T00:06+02:00 — Färdigställde `föreläsningar_medeltiden_renässansen.md`: omformade Shakespeare-avsnittet och Stiernhielm-delen från punktlistor till löpande föreläsningsmanus med direkt elevtilltal; skapade strukturerade underrubriker (###) för alla delmoment; skrev omfattande avslutande återkoppling som knyter samman antiken (föregående läsår), medeltiden och renässansen genom Stiernhielms `Hercules` som syntes av alla tre epoker.
- 2025-10-12T22:46+02:00 — Strukturerade `svenska_2/medeltiden_renässansen/impulser_2_inskannade_sidor/föreläsningar_medeltiden_renässansen.md` med harmoniserade rubriknivåer, listor och sektioner i linje med referensmanus.
- 2025-10-12T22:18+02:00 — Gav `scripts/converters/md_to_txt.py` radbrytning (default 80 tecken) med paragraf-omslag och körde om konverteringen för `Impulser 2 Medeltiden (ss 82-102).md`.
- 2025-10-12T21:48+02:00 — OCR-extraherade text från Medeltiden-inledningen och fogade in avsnitten `Den medeltida världen` samt fortsättningen i `svenska_2/medeltiden_renässansen/impulser_2_inskannade_sidor/Impulser 2 Medeltiden (ss 82-102).md`; dokumenterade både `scripts/converters/extract_text_from_image.py` (JPG→text) och `scripts/converters/md_to_txt.py` (MD→text) som återanvändbara verktyg.
- 2025-10-06T09:14+02:00 — Created `debate_foundations_reference.html` as continuous A4-optimized reference document with logical sections and strategic page breaks for print cohesion.
- 2025-10-06T09:01+02:00 — Created `POWERPOINT_CONVERSION_INSTRUCTIONS.md` with AI agent instructions for interpreting markdown slide structure and `debate_foundations_slides.html` using debate_card_style.css for visual cohesion across all materials.
- 2025-10-06T08:54+02:00 — Created `debate_foundations_slides.md` as foundational slide deck covering debate format, SEAL structure, rebuttals, POIs, weighing, and core rhetorical concepts to ground students before using prep planner and score card.
- 2025-10-01T22:15+02:00 — Generated spaced repetition PDF via `pdm run build:pdf` and captured Fontconfig cache guidance.
- 2025-10-02T11:28+02:00 — Linked Tailwind bundle into spaced repetition template, rebuilt CSS, and verified WeasyPrint renders Tailwind classes (noting unsupported @layer/@property warnings).
- 2025-10-01T22:05+02:00 — Implemented Typer-based handout builder CLI that generates PDF/Docx artefacts under `build/` and documented usage.
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
- Integrate template front-matter parsing so builders can derive output names and assets dynamically.
- Create regression fixtures under `tests/` for HTML→PDF and Markdown→PDF flows, including binary diff strategy.
- Document manual QA checklist for new handouts in `docs/` so educators can verify layout before publishing.

## Acceptance Criteria
- `pdm run build:css` produces `styles/dist/tailwind.css` using Tailwind v4 with project-specific theme variables.
- `pdm run build:pdf` (or `build:docx`) renders at least one sample handout end-to-end without manual steps.
- Pytest suite exercises converter codepaths and passes on CI with coverage for backend selection logic.
