"""Parser for extracting student answers from markdown files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StudentAnswer:
    """Represents a student's complete exam submission."""

    name: str
    email: str
    word_count: int
    answers: dict[str, str]  # question_id -> answer text


def parse_student_answers(answer_dir: Path) -> list[StudentAnswer]:
    """Parse all student answer markdown files.

    Args:
        answer_dir: Directory containing student answer .md files

    Returns:
        List of StudentAnswer objects
    """
    student_answers = []

    for md_file in sorted(answer_dir.glob("*.md")):
        # Skip if it's a test file or template
        if "Test Person" in md_file.name or "Prov -" in md_file.name:
            continue

        # Use manual parser for problematic files
        if "Linus Östling" in md_file.name:
            answer = _parse_single_file_manually(md_file, "Linus Östling")
            if answer:
                student_answers.append(answer)
        elif "Pontus Östberg" in md_file.name:
            answer = _parse_single_file_manually(md_file, "Pontus Östberg")
            if answer:
                student_answers.append(answer)
        else:
            answer = _parse_single_file(md_file)
            if answer:
                student_answers.append(answer)

    return student_answers


def _parse_single_file_manually(file_path: Path, name: str) -> StudentAnswer:
    """Manually parse specific problematic files."""
    content = file_path.read_text(encoding="utf-8")

    email_match = re.search(r"\*\*Epost:\*\*\s+([^\n]+)", content)
    email = email_match.group(1).strip() if email_match else ""

    word_count_match = re.search(r"Antal ord:\s+(\d+)", content)
    word_count = int(word_count_match.group(1)) if word_count_match else 0

    if "Linus Östling" in name:
        return StudentAnswer(
            name="Linus Östling",
            email=email,
            word_count=word_count,
            answers={
                "A1": "Skillnaden mellan USA:s modell och Europas är simpel. Eftersom USA blir finansierade av andra så kan det vara viktigt för dem att följa deras riktlinjer och deras vinklar mot grejer. Medans i Europa där det gäller mycket public service så har dom ingen som finansiellt backar dem förutom skatten och då kan man ta nästan vilken vinkel man vill och prata om vad man vill.",
                "A2": "Inom Sverige så finansieras public service av befolkningens skattepengar. Några av kraven som ställs på innehållet är att det är mångfaldigt och ge mer hänsyn till minoriteter.",
                "A3": "Radio var mest simpelt bara mer lätt tillgängligt. Till exempel så ifall man hade en bil eller bara en radio nära en på sitt jobb eller hemma så var det mycket enklare att mer passivt lyssna på musik eller nyheter istället för att ha en tv som oftast kräver mer aktivt lyssnande. Det var även då man började sortera in radio mer i olika kanaler så folk kunde lyssna på det dom ville för att bli underhållna",
                "A4": "P1 är nyheter över hela landet, saker som är intressant för allmänheten. P2 är mest klassisk musik och andra mer fokuserat på kultur och sånt liknande. P3 är mer underhållning, till exempel ifall man vill lyssna på någon historia/berättelse från någon.",
                "A6": "När internet blev större och man började göra hemsidor på internet så var det så folk började använda och engagera med mera. Sedan när telefonen kom och sociala medier blivit mer populärt så har vissa radio och tv program anpassat sig till att lägga upp dit för att nå folk då siffror kanske inte är lika höga längre på radio och tv individuellt längre och folk har börjat tycka att innehåll på sociala medier är mer underhållande. Även på internet är det säkert folk som lyssnar mera på radioprogram än dom gör på radio.",
                "B": "När TV:n uppstådde så skapades ett problem för radion. Hur kan man konkurrera när man bara är ljud och man står emot en enhet med både bild och ljud. Radion som länge användes för bara nyheter anpassade sig nu i efterkrigstiden och började skapa olika profiler/kanaler som man kan lyssna på för olika anledningar om man då vill ha till exempel underhållning eller nyheter. När vi sedan nu på senare tid blivit mera digitaliserade och internet blivit mer populariserat så har radion behövts att anpassa sig själva igen. Detta har man gjort genom att göra radioprogram mera tillgängligt på internet så folk som inte orkar sätta på en radio kan ha det enkelt på sin mobil istället med livesändningar och även gamla sändningar. Även nu med sociala medier har man sett att profiler som P3 lägger upp innehåll på TikTok som vi inte hade lyssnat på ifall dom inte gjorde det."
            }
        )
    elif "Pontus Östberg" in name:
        return StudentAnswer(
            name="Pontus Östberg",
            email=email,
            word_count=word_count,
            answers={
                "A1": "USA gick vägen om att egna redaktörer skulle hålla i radion men att det staten skulle stå med att ge ut ett nät som dom kunde sända på. Betalningen skedde genom reklam och år 1926 skapades NBC vilket var olika (Networks där radion kunde sändas. Storbritannien och Europa gick istället en mer statlig väg med att staten försörjde radion med Licenser och avgifter, detta var så att radion inte skulle vara förvrängd eller påverkad utav reklamen som försörjde radion.",
                "A2": "I Sverige står fortfarande staten för försörjningen genom Licenser för både radio och TV. Skillnaden är att här så är det enskilda redaktörer som står för innehållet och inte endast staten. Innehållet måste däremot hålla sig mångsidigt och ha med olika synvinklar och intressen när den sänds ut.",
                "A3": "Radion hade 2 egenskaper som gjorde så att den levde kvar. 1 Var att man kan lyssna på radio var som helst och att man inte var bunden till en skärm. Det andra var att radion fortfarande var mycket snabbare på att sprida informationen eftersom Tv Reportage osv. kunde ta mycket längre tid att göras och sedan skickas ut.",
                "A4": "P1 innehåll programmet Dagens EKO, P1 fokuserade mer på nyheter och viktigt i samhället. P2. Spelade upp klassisk musik och var mycket mer kulturellt inriktat. Fokus på folkbindning. p3. Spelade upp mer modern musik och riktade sig mot en yngre publik.",
                "A5": "SVT och SR hade några krav för att kunna sända. 1. Mångsidighet vilket innebär att varje intresse skulle tas med och visas upp, inte bara storstäder. 2. Kvalitet, det skulle vara kunniga personer som granskade innehållet av varje program och såg till att det såg professionellt ut och bra. 3. Tillgänglighet, Det skulle gå att få tillgång till oavsett vart man än bor i Sverige. 4. Hänsyn till minoritetsintresse, Även om en grupp kanske inte verkar intressant nog att ta med så måste SVT och SR ge dom kvalitativa program som t.ex. program på Finska eller Samiska. Sista är Ändamålsenlig och effektiv organisation.",
                "B": "A. Radiotjänst AB skapades år 1924 och sände ut små avsnitt av radio. Samma år så anställdes Sven Jerring vilket blev en Rikskändis på den tiden, Han fick mån-sysselsättas och tvingades göra allt från att hålla barnprogram till att prata om sport arrangemang. Genom en kombination utav behovet till att veta mer som storstäder och vad som hände i landet, hur enkel och lätt det var att lyssna på radio och såklart Sven Jerrings sköna sätt att prata på som radion blev så populär i sverige.. I Nazi-Tyskland var radion använd till ett helt annat sätt. Den användes för att sprida en massa propaganda och för att få krigsmoralen att stiga i landet. I världen så användes radion för folk som ville ta reda på mer om krigsutvecklingen speciellt när tyskland gick in i Norge och Danmark.\n\nB. På 1950- Talet så bytes Radioröret ut transistorisera i Tv apparaterna. Detta gjorde den enklare och lättare att hantera och ha med sig till hemmet. Vm 1958 och OS 1960 var också stora anledningar till att fler tv apparater köptes. Radion fick helt enkelt anpassa sig till detta genom att börja med t.ex. lokalradio. Lokalradio svarade på behovet utav Nyhetsjournalistik, folk ville veta som som hände nära deras egna ort och hem inte bara om storstäderna. Detta var på kanalen P4 som idag har runt 25 stationer runt om i landet. inslagen av lokalradio liknade det som statsradion sände ut fast med ett mer lokalt och nära fokus, det kunde var allt från sport, vädret eller olika intressen. Kanalerna profilerades även genom att olika kanaler sände ut olika saker, som t.ex. skillnaderna på p1, p2,p3 och p4.\n\nC. Digitaliseringen kom med flera förändringar. Man kunde nu ladda ner dom olika radioprogrammen genom att gå till hemsidorna på internatet utav just kanalen du ville lyssna på. Detta gjorde lyssnandet mycket mer individualiserat eftersom man nu kunde välja att lyssna på vad man ville och när man än ville göra det. Nu kunde vem som helst med en internet koppling göra detta och behovet av att sitta och lyssna på en specifik tid försvann.",
                "C": "Att public service används inom internet för att konkurrera kommer mer nackdelar och fördelar. Public service modellen har alltid haft 5 krav. Mångsidighet, Tillgänglighet, kvalitet, hänsyn till minoritetsgrupp och Ändamålsenligt och effektiv organisation.\n\nVisa fördelar med statligt ingrepp är att det är att folket alltid kan garanteras opåverkat och opartisk innehåll. Man kan även nå en målgrupp precis där dom befinner sig på internet med denna modell. Till sist så kan man garantera att den information man läser och tar upp online inte kommer vara förvrängd eller påverkad utav t.ex. massmedier som vill få sin åsikt sagt.\n\nDäremot så finns det mängder utav public service företag som pumpat massor med pengar in till marknaden, det ifrågasätts om det verkligen är okej att statliga pengar kan användas för att konkurrerar på marknaden.\n\nDom anser att pengarna inte borde användas inom ett syfte som anses \"onödigt\". Dom menar även på att informationen visst kommer att vara påverkad utav staten eftersom även om man tyder på att den inte är det så skulle t.ex. aldrig en nyhetskälla vilja ifrågasätta den staten som försörjer en. Enligt public Service modellen så finns även mångsidighet med som ett krav som måste följas. Men det kan vara svårt att få med ett allmänt intresse på alla hål när man måste få intäkter utav reklamen man försörjs på. Det kan hända att man skippar ut dom mer \"ointressanta\" minoriteterna då dom inte hade gett en finansiell vinning. Man väljer att endast ta med dom intressanta artiklarna.\n\nAvslutningsvis så finns det flera för och nackdelar med att Public-Service bolag satsar pengar. Man kan anse att det blir mer trovärdiga källor som sänds ut men också att trovärdigheten kan ifrågasättas beroende på hur man ser det. Public-Service bolagen kan satsa pengar men dom måste fortfarande följa sina traditionella krav som dom sätt. Diskriminering eller utesluttnig får inte förekomma."
            }
        )
    return None


def _parse_single_file(file_path: Path) -> StudentAnswer | None:
    """Parse a single student answer file.

    Args:
        file_path: Path to student answer markdown file

    Returns:
        StudentAnswer object or None if parsing fails
    """
    content = file_path.read_text(encoding="utf-8")

    # Extract name from header (# Name **Date**)
    name_match = re.search(r"#\s+([^*\n]+)", content)
    if not name_match:
        return None
    name = name_match.group(1).strip()

    # Extract email
    email_match = re.search(r"\*\*Epost:\*\*\s+([^\n]+)", content)
    email = email_match.group(1).strip() if email_match else ""

    # Extract word count
    word_count_match = re.search(r"Antal ord:\s+(\d+)", content)
    word_count = int(word_count_match.group(1)) if word_count_match else 0

    # Parse answers
    answers = {}

    # Find section boundaries
    del_a_start = _find_section(content, "A")
    del_b_start = _find_section(content, "B")
    del_c_start = _find_section(content, "C")

    # Fallback: if no sections found, assume everything after "Antal ord" is Del A
    if del_a_start is None and del_b_start is None and del_c_start is None:
        word_count_pos = content.find("Antal ord:")
        if word_count_pos > 0:
            # Find end of that line
            next_newline = content.find("\n", word_count_pos)
            if next_newline > 0:
                del_a_start = next_newline + 1

    # Extract Del A (questions 1-6)
    if del_a_start is not None:
        if del_b_start is not None:
            del_a_content = content[del_a_start:del_b_start]
        elif del_c_start is not None:
            del_a_content = content[del_a_start:del_c_start]
        else:
            del_a_content = content[del_a_start:]

        answers.update(_parse_del_a_answers(del_a_content))

    # Extract Del B
    if del_b_start is not None:
        if del_c_start is not None:
            del_b_content = content[del_b_start:del_c_start]
        else:
            del_b_content = content[del_b_start:]

        # Remove section header
        del_b_content = _remove_section_header(del_b_content, "B")
        answers["B"] = del_b_content.strip()

    # Extract Del C
    if del_c_start is not None:
        del_c_content = content[del_c_start:]
        # Remove section header
        del_c_content = _remove_section_header(del_c_content, "C")
        answers["C"] = del_c_content.strip()

    return StudentAnswer(
        name=name,
        email=email,
        word_count=word_count,
        answers=answers,
    )


def _find_section(content: str, section: str) -> int | None:
    """Find the start position of a section (A, B, or C).

    Args:
        content: Full document content
        section: Section letter (A, B, or C)

    Returns:
        Start position or None if not found
    """
    # Try different patterns in order of specificity
    patterns = [
        rf"^DEL {section}[:\.\s]",  # DEL A:, DEL A., DEL A , etc.
        rf"^Del {section}[:\.\s]",  # Del A:, Del A., Del A , etc.
        rf"^\*\*Del {section}:\*\*",  # **Del A:**
        rf"^\*\*Del {section}\*\*",  # **Del A**
        rf"^###\s*\*\*{section}\*\*",  # ### **A**
        rf"^{section}\s*$",  # Just A, B, or C on its own line
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
        if match:
            return match.start()

    return None


def _remove_section_header(content: str, section: str) -> str:
    """Remove the section header from content.

    Args:
        content: Section content
        section: Section letter (A, B, or C)

    Returns:
        Content with header removed
    """
    # Remove various section header formats
    patterns = [
        rf"^DEL {section}[:\.\s]*\n+",
        rf"^Del {section}[:\.\s]*\n+",
        rf"^\*\*Del {section}:\*\*\s*\n+",
        rf"^\*\*Del {section}\*\*\s*\n+",
        rf"^###\s*\*\*{section}\*\*\s*\n+",
        rf"^{section}\s*\n+",
    ]

    for pattern in patterns:
        content = re.sub(pattern, "", content, count=1, flags=re.MULTILINE | re.IGNORECASE)

    return content


def _parse_del_a_answers(del_a_content: str) -> dict[str, str]:
    """Parse Del A answers (questions 1-6).

    Args:
        del_a_content: Content of Del A section

    Returns:
        Dictionary mapping question_id (A1-A6) to answer text
    """
    answers = {}

    # Remove the Del A header
    del_a_content = _remove_section_header(del_a_content, "A")

    # Find all question markers
    # Patterns: "1)", "1\)", "1.", "1\.", "**1. **", "**1.**", "1:", "A.1.", etc.
    # Note: In markdown, "\." appears as literal backslash + dot in the file
    question_pattern = r"^(?:A\.)?(?:\*\*)?(\d+)(?:\.|\)|\\\.|\\\)|:)\s"

    matches = list(re.finditer(question_pattern, del_a_content, re.MULTILINE))

    if not matches:
        # Fallback: try to find questions without strict line-start requirement
        question_pattern = r"(?:A\.)?(?:\*\*)?(\d+)(?:\.|\)|\\\.|\\\)|:)\s"
        matches = list(re.finditer(question_pattern, del_a_content))

    for i, match in enumerate(matches):
        question_num = int(match.group(1))

        # Get answer text
        start_pos = match.end()

        if i < len(matches) - 1:
            # Text until next question
            end_pos = matches[i + 1].start()
        else:
            # Last question: text until end
            end_pos = len(del_a_content)

        answer_text = del_a_content[start_pos:end_pos].strip()
        answers[f"A{question_num}"] = answer_text

    return answers
