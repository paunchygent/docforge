#!/usr/bin/env python3
"""Remove textbook questions and exercises from text files."""

import re
from pathlib import Path


def clean_textbook_content(content: str) -> str:
    """Remove textbook questions and exercises from content."""
    lines = content.split('\n')
    cleaned_lines = []
    skip_section = False
    
    # Patterns for exercise/question headers
    exercise_patterns = [
        r'^###\s+(Samtala om texten|Skriv|Diskutera|Tala|Agera|Undersök|Samtala om bilden)',
    ]
    
    # Pattern for next section (stop skipping)
    next_section_patterns = [
        r'^##\s+',  # New main section
        r'^#\s+',   # New chapter
    ]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is an exercise section
        is_exercise = any(re.match(pattern, line) for pattern in exercise_patterns)
        
        if is_exercise:
            skip_section = True
            i += 1
            continue
        
        # Check if we've reached a new section (stop skipping)
        is_new_section = any(re.match(pattern, line) for pattern in next_section_patterns)
        
        if skip_section and is_new_section:
            skip_section = False
        
        # Add line if we're not skipping
        if not skip_section:
            cleaned_lines.append(line)
        
        i += 1
    
    # Join and clean up multiple blank lines
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result


def main():
    """Clean textbook questions from specified files."""
    base_path = Path(__file__).resolve().parent.parent.parent
    files_to_clean = [
        base_path / "svenska_2/medeltiden_renässansen/impulser_2_inskannade_sidor/Impulser 2 Medeltiden (ss 82-102).txt",
        base_path / "svenska_2/medeltiden_renässansen/impulser_2_inskannade_sidor/Impulser 2 Renässansen (ss 108-139).txt",
    ]
    
    for file_path in files_to_clean:
        if not file_path.exists():
            print(f"File not found: {file_path}")
            continue
        
        print(f"Cleaning: {file_path.name}")
        
        # Read original content
        content = file_path.read_text(encoding='utf-8')
        
        # Clean content
        cleaned_content = clean_textbook_content(content)
        
        # Write back
        file_path.write_text(cleaned_content, encoding='utf-8')
        
        print(f"  ✓ Cleaned {file_path.name}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
