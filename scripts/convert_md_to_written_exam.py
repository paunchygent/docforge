#!/usr/bin/env python3
"""Convert markdown exam to HTML using the written exam template."""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import frontmatter
import markdown

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = PROJECT_ROOT / "handout_templates" / "written_exam_templates"
OUTPUT_DIR = PROJECT_ROOT / "build" / "html"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def parse_markdown_exam(md_path: Path) -> Dict[str, Any]:
    """Parse markdown exam file into a structured format for the template."""
    # Read markdown content
    content = md_path.read_text(encoding='utf-8')
    
    # Extract frontmatter if exists
    post = frontmatter.loads(content)
    
    # Get title from first heading if not in frontmatter
    title = post.get('title', '')
    if not title:
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
    
    # Initialize exam data structure
    exam_data = {
        'title': title,
        'subtitle': post.get('subtitle', ''),
        'course_code': post.get('course_code', ''),
        'date': post.get('date', datetime.now().strftime('%Y-%m-%d')),
        'exam_duration': post.get('duration', '90 minuter'),
        'allowed_materials': post.get('allowed_materials', 'Inga hjälpmedel'),
        'max_points': post.get('max_points', 50),
        'sections': []
    }
    
    # Split into sections
    sections = re.split(r'\n##\s+', content)[1:]  # Skip the first part (title)
    
    for section_text in sections:
        # Split section into header and content
        section_parts = section_text.split('\n', 1)
        if len(section_parts) != 2:
            continue
            
        section_title = section_parts[0].strip()
        section_content = section_parts[1].strip()
        
        # Skip instructions section for now
        if 'nstruktion' in section_title.lower():
            continue
            
        # Create section
        section = {
            'title': section_title,
            'questions': []
        }
        
        # Extract questions
        questions = re.split(r'\n###?\s+', section_content)
        for question_text in questions[1:]:  # Skip the first part (section intro)
            # Split question into number/text and options
            question_parts = re.split(r'\n', question_text, 1)
            if len(question_parts) != 2:
                continue
                
            question_header = question_parts[0].strip()
            question_content = question_parts[1].strip()
            
            # Initialize default values
            question_text = question_header
            points = 0
            
            # Try to extract question number and points
            match = re.match(r'^(?:Fråga\s+)?(\d+)[.:]?\s*(.*?)(?:\s*\([^)]*\))?$', question_header)
            if match:
                question_num = match.group(1)
                question_text = match.group(2).strip()
                
                # Try to find points in the header
                points_text = match.group(3) or ''
                points_match = re.search(r'(\d+)\s*p(?:oäng)?\b', points_text.lower())
                if points_match:
                    points = int(points_match.group(1))
                
                question_text = f"{question_num}. {question_text}"
            
            # Determine question type based on content
            question_type = 'essay' if any(word in question_text.lower() for word in ['essä', 'utveckla', 'förklara', 'beskriv', 'jämför', 'diskutera']) else 'short_answer'
            
            # Add question to section
            section['questions'].append({
                'text': question_text,
                'type': question_type,
                'points': points if points > 0 else None
            })
    
        exam_data['sections'].append(section)
    
    return exam_data

def render_template(template_path: Path, context: Dict) -> str:
    """Render Jinja2 template with the given context."""
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    
    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    template = env.get_template(template_path.name)
    return template.render(**context)

def convert_md_to_html(md_path: Path, output_path: Path) -> None:
    """Convert markdown exam to HTML using the written exam template."""
    # Parse markdown exam
    exam_data = parse_markdown_exam(md_path)
    
    # Add current timestamp
    exam_data['now'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Render template
    template_path = TEMPLATE_DIR / 'written_exam_template.html'
    html_content = render_template(template_path, exam_data)
    
    # Save HTML
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding='utf-8')
    print(f"✅ Generated HTML: {output_path}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert markdown exam to HTML using the written exam template.')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output HTML file')
    
    args = parser.parse_args()
    
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_filename = input_path.stem + '.html'
        output_path = OUTPUT_DIR / output_filename
    
    convert_md_to_html(input_path, output_path)
    
    # Also generate PDF
    from scripts.converters.convert_html_to_pdf import convert_html_to_pdf
    pdf_path = output_path.with_suffix('.pdf')
    try:
        pdf_path, _ = convert_html_to_pdf(output_path, output_path=pdf_path, verbose=True)
        print(f"✅ Generated PDF: {pdf_path}")
    except Exception as e:
        print(f"❌ Failed to generate PDF: {e}")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
