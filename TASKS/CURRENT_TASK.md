# Current Task: Establish HTML→PDF/Docx Workflow Hub

## Context

- Stand up repository governance, Python/PDM tooling, and a Tailwind CSS v4 build so HTML handouts export cleanly to PDF/Docx through a single CLI.

## Worklog

- 2025-10-21T09:59+02:00 — Skapade separat mapp `build/pdf/debattämnen/` och kopierade alla 10 svenska debattkort-PDF:er (9 ämnen + mall) dit för enklare distribution.
- 2025-10-21T09:55+02:00 — Förenklade testfrågor till rakare språk utan onödiga bisatser: "Om systemet blir för krångligt, varför inte bara höja flygskatter istället?" → "Varför inte bara höja flygskatter om systemet blir för krångligt?"; "Varför inte fixa tätning och ventilation istället, som sparar mer utan att göra det kallare?" → "Varför inte täta fönster och fixa ventilationen istället?"; och liknande förenklingar i `energiskatt_ai.html`, `kottfri_skola.html`, `miljotull_mode.html`, `karnkraft_vindkraft.html`.
- 2025-10-21T09:53+02:00 — Lade till andra frågan i "Frågor för att testa motståndarsidan" för alla 9 debattkort (en fråga per sida, totalt två frågor per kort).
- 2025-10-21T09:49+02:00 — Slutförde språkgranskning samtliga svenska debattkort: förbättrade idiomatik i `temperatur_skola.html` kontext ("sänkningar sparar märkbart" → "om vi sänker temperaturen lite sparar vi mycket"); ändrade rubrik från "POI-frågor att testa motståndarsidan" till "Frågor för att testa motståndarsidan" och reducerade till en fråga per kort i alla 9 debattkort; regenererade samtliga PDF:er.
- 2025-10-21T09:44+02:00 — Språkgranskning svenska debattkort: förbättrade "fixa" → "förbättra" i `elbilar_etik.html`, lade till info om vindkrafts korta livslängd (20–25 år) och återvinningsproblem i `karnkraft_vindkraft.html`, ersatte ogrammatiskt "korttidskläder" med "kläder som inte håller länge" i `miljotull_mode.html`.
- 2025-10-21T09:33+02:00 — Språkgranskning och förenkling av samtliga 9 svenska debattkort: tog bort alla Nyckelbegrepp-sektioner, ersatte nominaliseringar och passiva konstruktioner med aktiva verb och enkla formuleringar (t.ex. "internalisera miljökostnaden" → "låt företagen betala för miljöpåverkan", "carbon leakage" → "företag flyttar utomlands").
- 2025-10-21T09:26+02:00 — Skapade 9 färdiga svenska debattkort för klimat- och miljöfrågor (`energiskatt_ai.html`, `utslapsratter_flyg.html`, `mopedbilar_elcyklar.html`, `kottfri_skola.html`, `temperatur_skola.html`, `miljotull_mode.html`, `norden_klimatansvar.html`, `elbilar_etik.html`, `karnkraft_vindkraft.html`) och återställde mallen till 2–3 centrala frågor; genererade samtliga 28 PDF-artefakter.
- 2025-10-21T09:24+02:00 — Förenklade `debatt_mall.html` ytterligare: bytte "Motion" → "Förslag", reducerade "Centrala frågor" (3 punkter) till "Central fråga" (en avgörande fråga), och komprimerade JA/NEJ-panelerna från 3 argument per sida till 1 starkt argument per sida.
- 2025-10-21T09:17+02:00 — Skapade `handout_templates/debate_card_templates/debatt_mall.html`: förenklad svensk debattmall för snabb prep, översatte och komprimerade strukturen från `debate_card_template.html`, ersatte engelska glosor och domänord med en enda nyckelbegrepp-panel för 3–6 termer med definitioner.
- 2025-10-18T18:59+02:00 — Uppdaterade debattformat i samtliga handledningar (`student_debate_guide.html`, `student_quick_rules_and_role_instructions_for_teams_and_judges.html`, `debate_foundations_reference.html`, `debate_foundations_slides.html/.md`, `moderator_script.html`, `judges_score_card.html`) till 2 minuters tal, max 1 POI per Builder/Closer-tal, och 5 minuters avslutande POI-runda med växelvisa frågor; regenererade alla PDF-artefakter via `pdm run build:pdf --template debate_card_templates`.
- 2025-10-14T16:18+02:00 — Synkroniserade `svenska_2/medeltiden_renässansen/impulser_2_inskannade_sidor/sammanfattning_prov.md` med HTML-mallen: fyllde på Island-avsnittet, återinförde jämförelsetabell, brobyggarsektioner och hovkultur; la till avslutande uppmuntran.
- 2025-10-14T16:45+02:00 — Skrev `scripts/converters/docx_to_markdown.py` och körde mot `svenska_2/medeltiden_renässansen/Läxförhör/` för att få `.md`-versioner av samtliga DOCX-filer; uppdaterade `laxforhor_med_svar.md` så att samtliga formuleringar matchar källfilerna exakt.
- 2025-10-14T17:24+02:00 — Lade till `scripts/converters/convert_md_to_docx.py`, uppdaterade `pyproject.toml` med `build:md-docx`, fixade relativsökvägshantering och genererade `build/docx/svenska_2/medeltiden_renässansen/Läxförhör/laxforhor_4_utkast.docx` från Markdownutkastet.
- 2025-10-14T16:05+02:00 — Jämförde `handout_templates/instuderingsfrågor_templates/sammanfattning_medeltiden_renässansen.html` mot `svenska_2/medeltiden_renässansen/impulser_2_inskannade_sidor/sammanfattning_prov.md` och noterade saknade avsnitt och detaljer i Markdownversionen.
- 2025-10-18T16:55+02:00 — Dokumenterade svarstyperna för skrivprov i `docs/converters/html_to_pdf.md`, skapade `.windsurf/rules/120-written-exam-markdown-labels.mdc`, och noterade processen att köra `convert_md_to_written_exam.py` efter märkning.
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
