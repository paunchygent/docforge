# INSTRUKTION: Hur jag (LLM-bedömare) ska rätta proven systematiskt

> **OBS!** Detta projekt har nu en Claude Code Skill för provbedömning.
> För att använda den, be Claude: "Hjälp mig rätta provet" eller "Använd grading-skillen".
> Skillen finns i `.claude/skills/grading/SKILL.md` och följer denna metodik automatiskt.

## Steg 1: Förberedelser

### 1.1 Läs provinstruktioner
```bash
Read: medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/provinstruktion.md
```
**VIKTIGT att notera från [provinstruktion.md](../../medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/provinstruktion.md):**
- Del A: 6 frågor varav **5 ska besvaras** (eleverna väljer vilka 5)
- Del B: **Minst 2 av 3 aspekter** för godkänt, **SAMTLIGA 3 aspekter krävs för full poäng (9-10p)**
- Del C: Essäfråga, minst 250 ord, max 400 ord, fokus på analys och diskussion

### 1.2 Läs bedömningskriterier (facit)
```bash
Read: medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/facit.md
```
**Anteckna för varje fråga:**
- Maxpoäng
- Vad som krävs för full poäng (6p/9-10p/13-15p)
- Vad som krävs för godkänt (3-4p/6-8p/8-12p)
- Vad som ger underkänt (0-2p/0-5p/0-7p)

### 1.3 Verifiera att parsern fungerar
```bash
Bash: pdm run python scripts/grading/verify_parser.py
```
**Kontrollera:**
- Alla 11 elever parsas korrekt
- Antalet besvarade frågor per elev stämmer

## Steg 2: Systematisk bedömning fråga för fråga

### 2.1 Kör graderingsassistenten för att se alla svar
```bash
Bash: pdm run python scripts/grading/manual_grading_assistant.py
```

### ⚠️ KRITISKT: Bedöm ALLA elever för EN fråga åt gången

**VARFÖR DETTA ÄR VIKTIGT:**
- **Rättvis bedömning**: Du ser hela variationen av svar samtidigt
- **Konsekvent standard**: Du kan jämföra svar direkt mot varandra
- **Undvik drift**: Din bedömning blir inte strängare/mildare genom sessionen
- **Kalibrering**: Du ser vad som är 6p vs 5p vs 4p i praktiken

**FEL arbetssätt:**
❌ Rätta alla frågor för Elvira, sedan alla för Eric, osv.

**RÄTT arbetssätt:**
✅ Rätta A1 för ALLA 11 elever, sedan A2 för ALLA 11 elever, osv.

### 2.2 Bedömningsprocess för varje fråga

För **VARJE FRÅGA** (A1, A2, A3, A4, A5, A6, B, C):

**Steg 1: Förberedelse**
1. Läs bedömningskriterierna från graderingsassistenten
2. Identifiera nyckelelement som MÅSTE finnas för full poäng
3. Notera vad som skiljer 6p från 5p från 4p

**Steg 2: Första genomläsningen**
1. Läs ALLA 11 elevsvar på frågan
2. Anteckna preliminära intryck:
   - Vilka svar är tydligt starka (6p)?
   - Vilka är i mittenområdet (4-5p)?
   - Vilka är svaga (0-3p)?

**Steg 3: Detaljerad bedömning**
För varje elev:
1. **Checklista mot kriterier:**
   - [ ] Komponent 1 finns?
   - [ ] Komponent 2 finns?
   - [ ] Förklaringar tydliga?
   - [ ] Exempel/konkretisering?

2. **Tilldela poäng:**
   - Jämför mot andra elevsvar du precis läst
   - Använd kriterierna strikt
   - Motivera varje poäng

3. **Dokumentera:**
   ```
   Elvira (5p): Båda modellerna, motiv för Europa tydligt (ekonomiska intressen), USA:s motiv implicit
   Eric (3p): Båda modellerna nämnda kortfattat, inga tydliga motiv förklarade
   ```

**Steg 4: Kvalitetskontroll för frågan**
- Har jag använt hela skalan (0-6p)?
- Är poängen konsekvent med kriterierna?
- Kan jag försvara varför elev X fick 5p och elev Y fick 4p?

## Steg 3: Specialfall att hantera

### 3.1 Del A - Eleverna väljer 5 av 6 frågor
- Om eleven besvarar färre än 5 frågor: De förlorar poäng för obesvarade
- Om eleven besvarar alla 6: Rätta alla 6, räkna totalpoäng
- **Maxpoäng Del A: 30p** (5 frågor × 6p)
- **Om eleven besvarar 6 frågor och får t.ex. 5+6+5+6+4+3 = 29p** → **Eleven får 29p** (över 30p är OK enligt facit)

### 3.2 Del B - ALLA TRE aspekter krävs för full poäng
**KRITISKT VIKTIGT från [provinstruktion.md](../../medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/provinstruktion.md) rad 68:**
> "Din text ska behandla minst två av följande tre aspekter av radions utveckling. **Samtliga aspekter krävs för full poäng**"

**Bedömning:**
- **9-10p**: Alla TRE aspekter (a+b+c) behandlade med orsakssamband
- **6-8p**: TVÅ aspekter behandlade MED orsakssamband ELLER en aspekt mycket väl beskriven
- **0-5p**: Bara en aspekt vagt beskriven ELLER inga orsakssamband

Kontrollera för varje elev:
- ✓ a) 1920-40-talen (Radiotjänst, Sven Jerring, andra världskriget)?
- ✓ b) 1950-70-talen (TV:ns intåg, kanalprofilering, lokalradio)?
- ✓ c) 1990-2020-talen (Digitalisering, internetradio)?

### 3.3 Del C - Essä med struktur
Kontrollera:
1. **Inledning** (3-4p): Historisk kontext om public service
2. **Huvuddel** (4-5p): För- OCH nackdelar diskuterade
3. **Avslutning** (3-4p): Syntes mellan historia och nutid
4. **Struktur** (3-4p): Tydlig essästruktur, språkkvalitet

**Ordräkning från [provinstruktion.md](../../medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/provinstruktion.md):**
- Minst 250 ord
- Max 400 ord (men detta påverkar inte bedömning enligt facit)

## Steg 4: Sammanställning

### 4.1 Skapa CSV-fil med alla betyg
```csv
Elev,Email,A1,A2,A3,A4,A5,A6,B,C,Total
Elvira Engman,EE23001@harryda.se,5,4,6,6,5,4,8,12,50
...
```

### 4.2 Skapa detaljerad bedömningsfil
```markdown
# DETALJERAD BEDÖMNING - Radio och TV i Sverige

## Fråga A1 (alla elever):
- Elvira (5/6p): Båda modellerna, motiv för Europa tydligt
- Eric (3/6p): Båda modellerna, inga tydliga motiv
...

## Fråga A2 (alla elever):
...

## Sammanfattning per elev:

### Elvira Engman (Total: 50p)
Del A: 5+4+6+6+5+4 = 30p
Del B: 8p (behandlar alla tre aspekter med orsakssamband)
Del C: 12p (bra struktur, för- och nackdelar, historisk kontext)
```

## Steg 5: Kvalitetskontroll

### 5.1 Verifiera maxpoäng
- Del A: Max 30p (5×6p, men över 30p är OK om eleven besvarar alla 6)
- Del B: Max 10p
- Del C: Max 15p
- **Totalt max: 55p** (eller mer om eleven besvarar alla 6 frågor i Del A)

### 5.2 Kontrollera att varje elev har:
- Minst 5 frågor i Del A bedömda (eller 0p för obesvarade)
- Del B bedömd
- Del C bedömd
- Total summa korrekt

### 5.3 Dubbelkolla gränsvärden
- Har någon fått exakt 6p på en fråga? Motivera varför full poäng.
- Har någon fått 0p? Kontrollera att inget svar finns.
- Har någon fått 9-10p på Del B? Kontrollera att ALLA TRE aspekter behandlas.

## Steg 6: Slutliga filer

Spara två filer:
1. **output/grades.csv** - Enkel poängöversikt för import
2. **output/detailed_assessment.md** - Detaljerad motivering per fråga (ALLA elever per fråga)

---

## CHECKLISTA före jag säger att jag är klar:

- [ ] Läst [provinstruktion.md](../../medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/provinstruktion.md)
- [ ] Läst alla bedömningskriterier från facit.md
- [ ] Verifierat att parsern fungerar för alla 11 elever
- [ ] Bedömt ALLA 11 elever för A1 samtidigt
- [ ] Bedömt ALLA 11 elever för A2 samtidigt
- [ ] Bedömt ALLA 11 elever för A3 samtidigt
- [ ] Bedömt ALLA 11 elever för A4 samtidigt
- [ ] Bedömt ALLA 11 elever för A5 samtidigt
- [ ] Bedömt ALLA 11 elever för A6 samtidigt
- [ ] Bedömt ALLA 11 elever för B samtidigt (kontrollerat att full poäng = 3 aspekter)
- [ ] Bedömt ALLA 11 elever för C samtidigt
- [ ] Kontrollerat att Del A har max 30p per elev (om 5 frågor)
- [ ] Kontrollerat att totalsumman är korrekt för varje elev
- [ ] Skapat output/grades.csv
- [ ] Skapat output/detailed_assessment.md med motiveringar per fråga
- [ ] Kvalitetskontrollerat gränsvärden (0p, 6p, 9-10p för Del B)

---

## Verktyg som finns tillgängliga:

### Claude Code Skill: `grading` (REKOMMENDERAT)
Använd Claude Code Skillen för automatiserad, systematisk bedömning:
```
Be Claude: "Hjälp mig rätta provet" eller "Använd grading-skillen"
```

Skillen kommer automatiskt att:
- Läsa provinstruktion och facit
- Verifiera parsern
- Visa alla svar per fråga
- Guida genom bedömning fråga-för-fråga
- Skapa output-filer (CSV + detaljerad bedömning)
- Köra kvalitetskontroll

**Plats:** `.claude/skills/grading/SKILL.md`

---

### Manual grading assistant
Visar alla svar fråga för fråga:
```bash
pdm run python scripts/grading/manual_grading_assistant.py
```

### Interactive grading (för manuell rättning)
Om du vill rätta interaktivt själv (kräver input för varje elev):
```bash
pdm run grade
```

### Verify parser
Kontrollera att alla elevsvar parsas korrekt:
```bash
pdm run python scripts/grading/verify_parser.py
```
