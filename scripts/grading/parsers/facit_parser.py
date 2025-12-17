"""Parser for extracting grading criteria from facit.md."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Question:
    """Represents a question with its grading criteria."""

    question_id: str
    title: str
    max_points: int
    criteria: str


def parse_facit(facit_path: Path) -> list[Question]:
    """Parse facit.md and extract all questions with grading criteria.

    Args:
        facit_path: Path to facit.md file

    Returns:
        List of Question objects with id, title, max_points, and criteria
    """
    content = facit_path.read_text(encoding="utf-8")
    questions = []

    # Split into sections
    sections = re.split(r"\n##\s+", content)

    for section in sections[1:]:  # Skip header
        # Parse Del A questions
        if section.startswith("Del A"):
            questions.extend(_parse_del_a(section))
        # Parse Del B
        elif section.startswith("Del B"):
            questions.append(_parse_del_b(section))
        # Parse Del C
        elif section.startswith("Del C"):
            questions.append(_parse_del_c(section))

    return questions


def _parse_del_a(section: str) -> list[Question]:
    """Parse Del A section with 6 questions."""
    questions = []
    # Split by ### Fråga
    question_blocks = re.split(r"\n###\s+Fråga\s+(\d+):", section)

    for i in range(1, len(question_blocks), 2):
        question_num = question_blocks[i]
        question_content = question_blocks[i + 1]

        # Extract title (first line after question number)
        title_match = re.search(r"^([^\n]+)", question_content.strip())
        title = title_match.group(1).strip() if title_match else f"Fråga {question_num}"

        # Extract max points (from "Full poäng (Xp)")
        points_match = re.search(r"Full poäng \((\d+)p\)", question_content)
        max_points = int(points_match.group(1)) if points_match else 6

        # Extract criteria (everything until next --- or end)
        criteria_match = re.search(r"(.*?)(?:\n---|\Z)", question_content, re.DOTALL)
        criteria = criteria_match.group(1).strip() if criteria_match else question_content.strip()

        questions.append(
            Question(
                question_id=f"A{question_num}",
                title=title,
                max_points=max_points,
                criteria=criteria,
            )
        )

    return questions


def _parse_del_b(section: str) -> Question:
    """Parse Del B section (fördjupningsfråga)."""
    # Extract title
    title_match = re.search(r"^###\s+([^\n]+)", section)
    title = title_match.group(1).strip() if title_match else "Fördjupningsfråga"

    # Extract criteria
    criteria_match = re.search(r"###[^\n]+\n\n(.*?)(?:\n---|\Z)", section, re.DOTALL)
    criteria = criteria_match.group(1).strip() if criteria_match else section.strip()

    return Question(
        question_id="B",
        title=title,
        max_points=10,
        criteria=criteria,
    )


def _parse_del_c(section: str) -> Question:
    """Parse Del C section (essäfråga)."""
    # Extract title
    title_match = re.search(r"^###\s+([^\n]+)", section)
    title = title_match.group(1).strip() if title_match else "Essäfråga"

    # Extract criteria
    criteria_match = re.search(r"###[^\n]+\n\n(.*?)(?:\n---|\Z)", section, re.DOTALL)
    criteria = criteria_match.group(1).strip() if criteria_match else section.strip()

    return Question(
        question_id="C",
        title=title,
        max_points=15,
        criteria=criteria,
    )
