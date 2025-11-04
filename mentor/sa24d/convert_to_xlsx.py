"""Convert the mentor CSV file to an Excel workbook."""

import csv
from openpyxl import Workbook


def csv_to_xlsx(input_csv: str, output_xlsx: str) -> None:
    """Convert CSV file to Excel workbook."""
    # Read CSV
    with open(input_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Mentorselever"

    # Write all rows
    for row in rows:
        ws.append(row)

    # Save workbook
    wb.save(output_xlsx)
    print(f"Converted {input_csv} to {output_xlsx}")
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    input_csv = "sa24d_mentorselever_olof_ola.csv"
    output_xlsx = "sa24d_mentorselever_olof_ola.xlsx"
    csv_to_xlsx(input_csv, output_xlsx)
