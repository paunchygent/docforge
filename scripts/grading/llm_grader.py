"""LLM-based grading module using Claude API."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import anthropic

if TYPE_CHECKING:
    from parsers.facit_parser import Question


class LLMGrader:
    """Grades student answers using Claude API."""

    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = anthropic.Anthropic(api_key=api_key)

    def grade_answer(
        self,
        question: Question,
        answer: str,
        student_name: str,
    ) -> tuple[float, str]:
        """Grade a single answer using Claude.

        Args:
            question: Question object with criteria
            answer: Student's answer text
            student_name: Name of student (for context)

        Returns:
            Tuple of (score, reasoning)
        """
        prompt = f"""Du är en gymnasielärare som bedömer elevsvar på ett prov om radio och TV i Sverige.

FRÅGA: {question.question_id} - {question.title}
MAXPOÄNG: {question.max_points}

BEDÖMNINGSKRITERIER:
{question.criteria}

ELEVENS SVAR:
{answer}

Bedöm elevens svar enligt kriterierna ovan och ge en poäng mellan 0 och {question.max_points}.

Svara i följande format:
POÄNG: [ditt poäng 0-{question.max_points}]
MOTIVERING: [kort motivering för poängen baserat på kriterierna]"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        # Parse response
        lines = response_text.strip().split("\n")
        score = 0.0
        reasoning = ""

        for line in lines:
            if line.startswith("POÄNG:"):
                score_text = line.replace("POÄNG:", "").strip()
                # Extract first number found
                import re

                match = re.search(r"(\d+(?:[.,]\d+)?)", score_text)
                if match:
                    score = float(match.group(1).replace(",", "."))
            elif line.startswith("MOTIVERING:"):
                reasoning = line.replace("MOTIVERING:", "").strip()
            elif reasoning:  # Continue reasoning if it spans multiple lines
                reasoning += " " + line.strip()

        # Validate score
        if score < 0:
            score = 0.0
        elif score > question.max_points:
            score = question.max_points

        return score, reasoning
