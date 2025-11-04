#!/usr/bin/env python3
"""Extract email addresses from CSV and create semicolon-separated list."""

import csv
from pathlib import Path

csv_path = Path("mentor/sa24d/SA24D_VH_MEJL.csv")
output_path = csv_path.parent / "email_list.md"

emails = []

with open(csv_path, "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if row and row[0]:
            emails.append(row[0].strip())

# Create single line with semicolon-separated emails
email_string = ";".join(emails)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(email_string)

print(f"Created {output_path} with {len(emails)} email addresses")
