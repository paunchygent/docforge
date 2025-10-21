# HTML to PDF Converter

## Overview
A robust HTML to PDF converter that preserves CSS styling, images, and supports Swedish characters.

## Installation
The converter requires weasyprint (already installed):
```bash
pdm add weasyprint  # Already done
```

## Usage

### Basic Conversion
```bash
# Always use PDM to ensure correct environment
pdm run python scripts/converters/convert_html_to_pdf.py input.html

# Specify output file
pdm run python scripts/converters/convert_html_to_pdf.py input.html -o output.pdf

# Verbose mode for debugging
pdm run python scripts/converters/convert_html_to_pdf.py input.html --verbose
```

### Check Available Backends
```bash
pdm run python scripts/converters/convert_html_to_pdf.py --check-backends
```

### Convert the Kalibrering Report
```bash
pdm run python scripts/converters/convert_html_to_pdf.py \
  handout_templates/report_templates/kalibrering_rapport_a4_optimized.html \
  -o build/pdf/report_templates/kalibrering_rapport_a4_optimized.pdf
```

### Batch Builds via Handout CLI
```bash
pdm run build:pdf --template kalibrering
```

- Outputs land in `build/pdf/`, preserving the template directory structure.
- Repeat `--template` flags to narrow builds, or omit them to process every template under `handout_templates/`.
- If Fontconfig reports missing cache directories, run with `XDG_CACHE_HOME=$PWD/.cache` or pre-create `~/.cache/fontconfig`.

## Features

- **WeasyPrint backend**: Excellent CSS support, preserves styling perfectly
- **pypandoc backend**: Basic fallback (limited Unicode and image support)
- Handles Swedish characters (å, ä, ö)
- Embeds images from relative paths
- Preserves complex CSS styling
- Configurable page margins
- Error handling and validation

## Output

The generated PDF:
- Preserves all HTML styling (colors, borders, tables)
- Embeds all referenced images
- Maintains proper Swedish text encoding
- Uses A4 page format with 1.5cm/2cm margins
- Avoids page breaks in tables and figures

## Notes

- Always use `pdm run` to execute the script (ensures correct Python environment)
- Images must be in the same directory as the HTML file or use absolute paths
- WeasyPrint provides the best results for complex styled HTML
- pypandoc fallback has limitations with Unicode symbols and image paths

### Template-specific PDF options
- Add `<meta name="handout:pdf:inject_supplementary_css" content="false">` inside `<head>` when your template already manages page size and break rules. Omit the tag (or set it to `true`) to keep the converter’s supplementary print CSS.

### Written exam workflow
- Markdown questions can set answer panel sizing with inline tags such as `<svarstyp: kort>`, `<svarstyp: medel>`, `<svarstyp: lång>`, or `<svarstyp: essä>`.
- If no tag exists, `scripts/convert_md_to_written_exam.py` defaults to `medel`. Labels `10` (`lång`) and `11` (`essä`) override automatically.
- The converter maps each type to a note class/line count rendered by `handout_templates/written_exam_templates/written_exam_template.html`, so the final PDF includes appropriately sized lined panels that can extend over multiple pages when needed.
