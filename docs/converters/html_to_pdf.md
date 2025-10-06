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
  rapport_till_kollegor/files/kalibrering_rapport_korrigerad.html \
  -o rapport_till_kollegor/files/kalibrering_rapport_korrigerad.pdf
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
