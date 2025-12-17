"""Interactive grading tool for student assessments."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import typer
from parsers.answer_parser import parse_student_answers
from parsers.facit_parser import parse_facit
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

app = typer.Typer()
console = Console()


class GradingSession:
    """Manages a grading session with auto-save functionality."""

    def __init__(self, facit_path: Path, answers_dir: Path, output_path: Path):
        self.facit_path = facit_path
        self.answers_dir = answers_dir
        self.output_path = output_path
        self.questions = parse_facit(facit_path)
        self.students = parse_student_answers(answers_dir)
        self.grades: dict[str, dict[str, float]] = {}

        # Initialize grades structure
        for student in self.students:
            self.grades[student.name] = {q.question_id: 0.0 for q in self.questions}

        # Load existing grades if file exists
        self._load_existing_grades()

    def _load_existing_grades(self) -> None:
        """Load existing grades from CSV if it exists."""
        if not self.output_path.exists():
            return

        with open(self.output_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Elev"]
                if name in self.grades:
                    for q in self.questions:
                        qid = q.question_id
                        if qid in row and row[qid]:
                            try:
                                self.grades[name][qid] = float(row[qid])
                            except ValueError:
                                pass

    def save_grades(self) -> None:
        """Save current grades to CSV."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["Elev", "Email"] + [q.question_id for q in self.questions] + ["Total"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for student in self.students:
                row = {
                    "Elev": student.name,
                    "Email": student.email,
                }
                total = 0.0
                for q in self.questions:
                    grade = self.grades[student.name][q.question_id]
                    row[q.question_id] = grade
                    total += grade
                row["Total"] = total
                writer.writerow(row)

    def grade_question(self, question_idx: int) -> None:
        """Grade a single question for all students interactively.

        Args:
            question_idx: Index of question in self.questions list
        """
        question = self.questions[question_idx]

        console.clear()
        console.print(f"\n[bold cyan]{'=' * 80}[/bold cyan]")
        console.print(
            f"[bold yellow]Fråga {question.question_id}: {question.title}[/bold yellow]"
        )
        console.print(f"[bold]Maxpoäng: {question.max_points}[/bold]")
        console.print(f"[bold cyan]{'=' * 80}[/bold cyan]\n")

        # Display grading criteria
        console.print(Panel(question.criteria, title="[bold green]Bedömningskriterier[/bold green]", border_style="green"))
        console.print()

        # Grade each student
        for student in self.students:
            answer = student.answers.get(question.question_id, "[Inget svar]")

            console.print(f"\n[bold magenta]{'─' * 80}[/bold magenta]")
            console.print(f"[bold blue]Elev: {student.name}[/bold blue]")
            console.print(f"[bold magenta]{'─' * 80}[/bold magenta]\n")

            # Display answer in a panel
            console.print(Panel(answer, border_style="blue"))

            # Get current grade
            current_grade = self.grades[student.name][question.question_id]
            prompt_text = f"Poäng (0-{question.max_points})"
            if current_grade > 0:
                prompt_text += f" [nuvarande: {current_grade}]"

            # Input validation loop
            while True:
                grade_input = Prompt.ask(prompt_text, default=str(current_grade))
                try:
                    grade = float(grade_input)
                    if 0 <= grade <= question.max_points:
                        self.grades[student.name][question.question_id] = grade
                        break
                    else:
                        console.print(
                            f"[red]Poäng måste vara mellan 0 och {question.max_points}[/red]"
                        )
                except ValueError:
                    console.print("[red]Ange ett giltigt tal[/red]")

        # Auto-save after each question
        self.save_grades()
        console.print(f"\n[green]✓ Fråga {question.question_id} bedömd och sparad![/green]")
        input("\nTryck Enter för att fortsätta...")

    def show_summary(self) -> None:
        """Display summary of all grades."""
        console.clear()
        console.print("\n[bold cyan]Sammanfattning av poäng[/bold cyan]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Elev", style="cyan")

        for q in self.questions:
            table.add_column(q.question_id, justify="right")
        table.add_column("Total", justify="right", style="bold green")

        for student in self.students:
            row = [student.name]
            total = 0.0
            for q in self.questions:
                grade = self.grades[student.name][q.question_id]
                row.append(f"{grade:.1f}")
                total += grade
            row.append(f"{total:.1f}")
            table.add_row(*row)

        console.print(table)
        console.print(f"\n[green]Resultat sparade i: {self.output_path}[/green]\n")


@app.command()
def grade(
    facit: Path = typer.Option(
        Path("medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/facit.md"),
        help="Path to facit.md file",
    ),
    answers: Path = typer.Option(
        Path("medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/elevsvar"),
        help="Directory containing student answer files",
    ),
    output: Path = typer.Option(
        Path("scripts/grading/output/grades.csv"),
        help="Output CSV file for grades",
    ),
) -> None:
    """Interactive grading tool for student assessments.

    Displays grading criteria and all student answers for each question,
    allowing you to grade all students question-by-question.
    """
    if not facit.exists():
        console.print(f"[red]Error: Facit file not found: {facit}[/red]")
        raise typer.Exit(1)

    if not answers.exists():
        console.print(f"[red]Error: Answers directory not found: {answers}[/red]")
        raise typer.Exit(1)

    session = GradingSession(facit, answers, output)

    if not session.students:
        console.print("[red]Error: No student answers found[/red]")
        raise typer.Exit(1)

    console.print(f"\n[green]Läste in {len(session.students)} elevsvar[/green]")
    console.print(f"[green]Hittade {len(session.questions)} frågor[/green]\n")

    # Main grading loop
    current_question = 0

    while current_question < len(session.questions):
        session.grade_question(current_question)
        current_question += 1

    # Show summary
    session.show_summary()


if __name__ == "__main__":
    app()
