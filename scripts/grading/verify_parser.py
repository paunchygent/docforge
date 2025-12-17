"""Verify that all students parse correctly."""

from pathlib import Path

from parsers.answer_parser import parse_student_answers

# Parse all students
answers_dir = Path("medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/elevsvar")
students = parse_student_answers(answers_dir)

print(f"\n✓ Successfully parsed {len(students)} students:\n")

for student in sorted(students, key=lambda s: s.name):
    question_count = len(student.answers)
    print(f"  {student.name:30} - {question_count} questions answered")

    # Show which questions
    questions = sorted(student.answers.keys())
    print(f"    Questions: {', '.join(questions)}")

print(f"\n✓ All {len(students)} students ready for grading!\n")
