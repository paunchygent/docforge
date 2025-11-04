"""Find students from the full student list who are not yet assigned to a mentor."""

import csv


def normalize_name(first_name: str, last_name: str) -> str:
    """Create a normalized full name for comparison."""
    # Remove accents and normalize (e.g., Odéhn -> Odehn for matching)
    full_name = f"{first_name} {last_name}"
    # Simple normalization: remove accents
    replacements = {"é": "e", "É": "E"}
    for old, new in replacements.items():
        full_name = full_name.replace(old, new)
    return full_name.strip()


def get_assigned_students(mentor_file: str) -> set:
    """Extract all students already assigned to mentors."""
    with open(mentor_file, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assigned = set()
    # Skip header row
    for row in rows[1:]:
        # Check both Olof and Ola columns
        if row[0].strip():
            assigned.add(row[0].strip())
        if len(row) > 1 and row[1].strip():
            assigned.add(row[1].strip())

    return assigned


def find_missing_students(student_list_file: str, mentor_file: str) -> list:
    """Find students not yet assigned to any mentor."""
    # Get all assigned students
    assigned = get_assigned_students(mentor_file)
    print(f"Found {len(assigned)} students already assigned to mentors")
    print(f"Assigned students: {sorted(assigned)}\n")

    # Read full student list
    with open(student_list_file, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    missing_students = []
    # Skip header row
    for row in rows[1:]:
        if len(row) >= 2:
            first_name = row[0].strip()
            last_name = row[1].strip()
            full_name = normalize_name(first_name, last_name)

            if full_name not in assigned:
                missing_students.append(full_name)

    return missing_students


def main():
    student_list_file = "sa24d_student_list.csv"
    mentor_file = "sa24d_mentorselever_olof_ola.csv"

    missing = find_missing_students(student_list_file, mentor_file)

    print(f"Found {len(missing)} students NOT assigned to any mentor:")
    print("These students should be added to Ola's list:\n")
    for student in sorted(missing):
        print(f"  - {student}")

    # Write to output file
    output_file = "students_to_add_to_ola.csv"
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Student Name"])
        for student in sorted(missing):
            writer.writerow([student])

    print(f"\nOutput written to: {output_file}")


if __name__ == "__main__":
    main()
