#!/usr/bin/env python3
"""Convert markdown exam files into HTML/PDF assets using the written-exam template."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = PROJECT_ROOT / "handout_templates" / "written_exam_templates"
OUTPUT_DIR = PROJECT_ROOT / "build" / "html"
TEMPLATE_STATIC_BASE = TEMPLATE_DIR

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(slots=True)
class Question:
    """Structured representation of a question block."""

    label: str | None
    title: str
    points: int | None
    body_markdown: str
    type: str

    def body_html(self) -> str:
        if not self.body_markdown.strip():
            return ""
        return markdown.markdown(self.body_markdown, extensions=["extra"])


@dataclass(slots=True)
class Section:
    """Structured representation of an exam section."""

    title: str
    points: int | None
    instructions: list[str] = field(default_factory=list)
    questions: list[Question] = field(default_factory=list)


ANSWER_TYPE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"<!--\s*answer-type\s*:\s*([a-zåäö_\-]+)\s*-->", re.IGNORECASE),
    re.compile(r"<!--\s*svarstyp\s*:\s*([a-zåäö_\-]+)\s*-->", re.IGNORECASE),
    re.compile(r"<\s*svarstyp\s*:\s*([a-zåäö_\-]+)\s*>", re.IGNORECASE),
    re.compile(r"^\s*svarstyp\s*:\s*([a-zåäö_\-]+)\s*$", re.IGNORECASE | re.MULTILINE),
)

ANSWER_TYPE_MAP = {
    "short": "short",
    "short_answer": "short",
    "kort": "short",
    "kort_svar": "short",
    "medium": "medium",
    "medel": "medium",
    "default": "medium",
    "standard": "medium",
    "long": "long",
    "lang": "long",
    "lång": "long",
    "dubbel": "long",
    "extended": "long",
    "full": "long",
    "essay": "essay",
    "essä": "essay",
    "essa": "essay",
}

LONG_ANSWER_LABELS = {"10"}
ESSAY_LABELS = {"11"}


def extract_points(text: str) -> int | None:
    """Return the first integer followed by `p`/`poäng` in `text`, if any."""

    match = re.search(r"(\d+)\s*p", text.lower())
    return int(match.group(1)) if match else None


def parse_instruction_block(body: str) -> tuple[list[str], str]:
    """Extract the global instruction block and return (instructions, remaining_body)."""

    pattern = re.compile(
        r"Instruktioner:\s*\n(?P<block>.*?)(?=\n##\s+|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(body)
    if not match:
        return [], body

    block = match.group("block")
    instructions: list[str] = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            instructions.append(stripped[2:].strip())
        elif stripped:
            instructions.append(stripped)

    remaining = body[: match.start()] + body[match.end() :]
    return instructions, remaining


def slice_blocks(text: str, pattern: re.Pattern[str]) -> Iterable[tuple[str, str]]:
    """Yield (header, body) pairs for blocks delimited by `pattern` headings."""

    matches = list(pattern.finditer(text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        header = match.group(1).strip()
        body = text[start:end].strip()
        yield header, body


def clean_lines(block: str) -> list[str]:
    """Return non-empty, stripped lines from `block`."""

    return [line.strip() for line in block.strip().splitlines() if line.strip()]


def infer_question_type(label: str | None) -> str:
    """Default inference for question type when no explicit override is provided."""

    if label and label in ESSAY_LABELS:
        return "essay"
    if label and label in LONG_ANSWER_LABELS:
        return "long"
    return "medium"


def extract_answer_type(block: str) -> tuple[str | None, str]:
    """Return explicit answer type marker (if present) and the cleaned block."""

    for pattern in ANSWER_TYPE_PATTERNS:
        match = pattern.search(block)
        if not match:
            continue
        key = match.group(1).lower()
        answer_type = ANSWER_TYPE_MAP.get(key, ANSWER_TYPE_MAP["default"])
        cleaned = (block[: match.start()] + block[match.end():]).strip()
        return answer_type, cleaned
    return None, block


def parse_markdown_exam(md_path: Path) -> dict[str, Any]:
    """Parse the markdown exam into a context dictionary consumable by the template."""

    raw = md_path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)
    body = post.content

    title = post.get("title")
    if not title:
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else md_path.stem

    instructions, body_without_instructions = parse_instruction_block(body)

    section_pattern = re.compile(r"^##\s+(.*)$", re.MULTILINE)
    question_pattern = re.compile(r"^###\s+(.*)$", re.MULTILINE)

    sections: list[Section] = []
    for section_header, section_body in slice_blocks(body_without_instructions, section_pattern):
        section_points = extract_points(section_header)
        section_title = re.sub(r"\s*\(.*\)\s*$", "", section_header).strip()

        question_matches = list(question_pattern.finditer(section_body))
        instructions_text = ""
        if question_matches:
            instructions_text = section_body[: question_matches[0].start()].strip()
        section_instructions = clean_lines(instructions_text)

        questions: list[Question] = []
        if not question_matches:
            sections.append(
                Section(
                    title=section_title,
                    points=section_points,
                    instructions=section_instructions,
                    questions=[],
                )
            )
            continue

        for index, question_match in enumerate(question_matches):
            question_header = question_match.group(1).strip()
            start = question_match.end()
            end = (
                question_matches[index + 1].start()
                if index + 1 < len(question_matches)
                else len(section_body)
            )
            question_body = section_body[start:end].strip()

            header_without_points = re.sub(r"\s*\(.*\)\s*$", "", question_header).strip()
            question_points = extract_points(question_header)

            label = None
            title_text = header_without_points
            header_match = re.match(
                r"(?:Fråga\s+)?([0-9A-Za-z]+)[\s\u2013\-:]+(.+)",
                header_without_points,
            )
            if header_match:
                label = header_match.group(1).strip()
                title_text = header_match.group(2).strip()
            elif header_without_points.lower().startswith("fråga"):
                label = header_without_points

            answer_type_override, question_body = extract_answer_type(question_body)

            question_type = answer_type_override or infer_question_type(label)

            questions.append(
                Question(
                    label=label,
                    title=title_text or header_without_points,
                    points=question_points,
                    body_markdown=question_body,
                    type=question_type,
                )
            )

        sections.append(
            Section(
                title=section_title,
                points=section_points,
                instructions=section_instructions,
                questions=questions,
            )
        )

    max_points = post.get("max_points")
    if max_points is None:
        max_points = sum(section.points or 0 for section in sections)

    return {
        "title": title,
        "subtitle": post.get("subtitle", ""),
        "course_code": post.get("course_code", ""),
        "date": post.get("date", datetime.now().strftime("%Y-%m-%d")),
        "exam_duration": post.get("duration", "90 minuter"),
        "allowed_materials": post.get("allowed_materials", "Inga hjälpmedel"),
        "max_points": max_points,
        "instructions": instructions,
        "sections": [
            {
                "title": section.title,
                "points": section.points,
                "instructions": section.instructions,
                "questions": [
                    {
                        "label": question.label,
                        "title": question.title,
                        "text": (
                            f"{question.label}. {question.title}"
                            if question.label
                            else question.title
                        ),
                        "points": question.points,
                        "body_html": question.body_html(),
                        "type": question.type,
                        "notes_class": (
                            "small-notes"
                            if question.type == "short"
                            else "medium-notes"
                            if question.type == "medium"
                            else "long-notes"
                            if question.type == "long"
                            else "essay-notes"
                            if question.type == "essay"
                            else ""
                        ),
                        "lines": (
                            1
                            if question.type == "short"
                            else 10
                            if question.type == "medium"
                            else 24
                            if question.type == "long"
                            else 80
                            if question.type == "essay"
                            else 0
                        ),
                    }
                    for question in section.questions
                ],
            }
            for section in sections
        ],
    }


def render_template(template_path: Path, context: dict[str, Any]) -> str:
    """Render the Jinja2 template with the provided context."""

    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_path.name)
    return template.render(**context)


def convert_md_to_html(md_path: Path, output_path: Path) -> None:
    """Convert the provided markdown file into an HTML artefact."""

    exam_data = parse_markdown_exam(md_path)
    exam_data["now"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    template_path = TEMPLATE_DIR / "written_exam_template.html"
    html_content = render_template(template_path, exam_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")
    print(f"✅ Generated HTML: {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert markdown exams to HTML/PDF using the written-exam template.",
    )
    parser.add_argument("input", help="Path to the markdown exam file")
    parser.add_argument("-o", "--output", help="Output HTML path")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        return 1

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_filename = input_path.stem + ".html"
        output_path = OUTPUT_DIR / output_filename

    convert_md_to_html(input_path, output_path)

    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    from scripts.converters.convert_html_to_pdf import convert_html_to_pdf

    pdf_path = output_path.with_suffix(".pdf")
    try:
        pdf_path, _ = convert_html_to_pdf(
            output_path,
            output_path=pdf_path,
            verbose=True,
            base_url=str(TEMPLATE_STATIC_BASE.resolve()),
        )
        print(f"✅ Generated PDF: {pdf_path}")
    except Exception as error:  # pragma: no cover - diagnostic output
        print(f"❌ Failed to generate PDF: {error}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
