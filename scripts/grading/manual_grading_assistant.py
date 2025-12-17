"""Manual grading assistant - displays answers question by question for assessment."""

from pathlib import Path

from parsers.answer_parser import parse_student_answers
from parsers.facit_parser import parse_facit
from rich.console import Console
from rich.panel import Panel

console = Console()


def main():
    """Display all answers for systematic grading."""
    facit_path = Path("medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/facit.md")
    answers_dir = Path("medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/elevsvar")

    questions = parse_facit(facit_path)
    students = parse_student_answers(answers_dir)

    console.print("\n[bold cyan]RADIO OCH TV I SVERIGE - Systematisk Bedömning[/bold cyan]\n")
    console.print(f"[green]✓ {len(students)} elever[/green]")
    console.print(f"[green]✓ {len(questions)} frågor[/green]\n")

    # Grade question by question
    for question in questions:
        console.print(f"\n[bold yellow]{'=' * 80}[/bold yellow]")
        console.print(f"[bold yellow]{question.question_id}: {question.title}[/bold yellow]")
        console.print(f"[bold]Maxpoäng: {question.max_points}[/bold]")
        console.print(f"[bold yellow]{'=' * 80}[/bold yellow]\n")

        # Show criteria
        console.print(Panel(question.criteria, title="[bold green]Bedömningskriterier[/bold green]", border_style="green"))
        console.print()

        # Show all student answers for this question
        for student in sorted(students, key=lambda s: s.name):
            answer = student.answers.get(question.question_id, "[INGET SVAR]")

            console.print(f"\n[bold magenta]{'─' * 80}[/bold magenta]")
            console.print(f"[bold blue]{student.name}[/bold blue]")
            console.print(f"[bold magenta]{'─' * 80}[/bold magenta]\n")
            console.print(Panel(answer, border_style="blue"))

        input("\n[dim]Tryck Enter för nästa fråga...[/dim]\n")


if __name__ == "__main__":
    main()
