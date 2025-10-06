# PowerPoint Conversion Instructions for debate_foundations_slides.md

## Document Structure

**Slide Delimiter:** `---` (three hyphens) separates individual slides.

**Slide Title:** First `##` heading on each slide becomes the slide title.

**Subtitle/Tagline:** Bold text immediately following `#` (level-1 heading) is a subtitle, not a separate slide.

## Content Interpretation

### Headings
- `#` (H1) = Section title with subtitle (combine on one slide)
- `##` (H2) = Slide title
- `###` (H3) = Subsection heading within slide content

### Text Formatting
- `**bold**` = Emphasis (use bold or highlight color)
- `*italic*` = Examples or secondary emphasis
- `→` = Visual arrow (replace with PowerPoint arrow symbol)
- `✓` = Checkmark (use PowerPoint checkmark symbol)
- `❌` = Cross/X mark (use PowerPoint X symbol)

### Lists
- Numbered lists (1., 2., 3.) = Sequential steps or ordered items
- Bulleted lists (-) = Non-sequential points
- Checklist items (- [ ]) = Interactive checkboxes or checkbox symbols

### Tables
- Markdown tables = PowerPoint table objects
- Preserve column headers and alignment
- Use accent color for header row

### Special Patterns

**Definition Pattern:**  
`**Term** = explanation` → Use bold for term, regular text for definition

**Example Pattern:**  
`**Label:** *"quoted text"*` → Use bold for label, italic for example

**Multi-line Examples:**  
Indented italic text following a label → Group as a text box or callout

**Question-Answer Pattern:**  
`*"Question?"*` followed by `→ Answer` → Format as Q&A pair with visual separation

## Visual Design Guidelines

**Color Scheme:**
- Primary accent: `#1e3a8a` (dark blue) for titles and key terms
- Highlight: `#dbeafe` (light blue) for panels/boxes
- Text: `#1f2937` (dark gray)
- Muted: `#6b7280` (medium gray) for secondary text

**Layout:**
- Use consistent margins (match A4 proportions: 186mm max width)
- Two-column content (e.g., "Opener/Builder/Closer" sections) → Use PowerPoint columns or side-by-side text boxes
- Boxed content (e.g., examples, definitions) → Use bordered text boxes with light blue fill

**Typography:**
- Titles: Sans-serif (Avenir Next, Gill Sans, or Arial) in dark blue, uppercase for H2
- Body: Serif (Georgia or Times New Roman) for readability
- Code/terms: Monospace (Consolas or Courier) with light background

## Slide-Specific Notes

**Slide 1 (Title):** Combine "Debate Foundations" + subtitle on one title slide.

**Slides with Tables:** Convert markdown table to PowerPoint table with header styling.

**Slides with Examples:** Use callout boxes or bordered text boxes for multi-line examples (e.g., SEAL structure, rebuttal example).

**Slides with Subsections (###):** Use visual hierarchy—subsection headings in smaller bold text, content indented or in separate text boxes.

**Final Slide ("Questions?"):** Format Q&A pairs with visual separation (e.g., question in bold, answer indented with arrow).

## Automation Tips

1. **Split on `---`** to identify slide boundaries
2. **Extract first `##`** per slide as title
3. **Preserve formatting** (bold, italic, lists) using PowerPoint text formatting
4. **Convert special symbols** (→, ✓, ❌) to PowerPoint shapes/symbols
5. **Apply color scheme** from CSS variables to PowerPoint theme colors
6. **Use master slide** with consistent header/footer for branding
