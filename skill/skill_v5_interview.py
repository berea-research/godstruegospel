"""
skill_v5_interview.py — godstruegospel skill v5.4, module 1: interview
======================================================================

Drie-dimensies-interview voor de godstruegospel skill. v5.4 aanpassingen:
- A4-samenvatting is altijd onderdeel van de output en wordt NIET bevraagd
  in het interview. Default-aanname: A4 is altijd inbegrepen.
- 'output_type' (oude dossier/summary/transcript) is vervangen door
  'blocks_requested': een lijst met subset van {A, B, C, D, E, F}. Lege
  lijst = alleen A4.
- Talen NL, EN en ES zijn operationeel. Overige 14 talen vallen terug op NL
  met expliciete waarschuwing.
- Bij ontbrekende dimensies returnt het script 'unknown' en exit-code 1 met
  --enforce, zodat de aanroeper expliciet door moet vragen.
- Vlag --confirm bouwt een Nederlandstalige bevestigingsprompt voor Claude.

Levert structured output:
    {
      "language": "nl" | "en" | "es" | ... | "unknown",
      "language_operational": true | false | null,
      "blocks_requested": ["A", "C", "E"] | [] | "unknown",
      "depth": "vers" | "word" | "theme" | "unknown",
      "missing": ["language", ...],
      "confirm_prompt": "... (alleen bij --confirm)"
    }

CLI / direct-aanroep:
    python3 skill_v5_interview.py                              # interactief
    python3 skill_v5_interview.py --auto nl,ACE,vers --json    # skip-modus (automation)
    python3 skill_v5_interview.py --auto nl,,vers --json       # alleen A4 (geen blokken)
    python3 skill_v5_interview.py --infer "<vraag>" --json
    python3 skill_v5_interview.py --infer "<vraag>" --enforce --json
    python3 skill_v5_interview.py --infer "<vraag>" --confirm --json
"""
import json
import re
import sys

OPERATIONAL_LANGUAGES = {'nl', 'en', 'es'}

SUPPORTED_LANGUAGES = [
    ('nl', 'Nederlands'),
    ('en', 'English'),
    ('es', 'Espanol'),
    ('fr', 'francais'),
    ('it', 'Italiano'),
    ('pt', 'Portugues'),
    ('bg', 'bulgaars'),
    ('ru', 'russisch'),
    ('ar', 'arabisch'),
    ('hi', 'hindi'),
    ('zh', 'chinees'),
    ('ja', 'japans'),
    ('ko', 'koreaans'),
    ('tr', 'turks'),
    ('el', 'grieks'),
    ('ta', 'tamil'),
    ('he', 'hebreeuws'),
]

# Blok-opties met functionele beschrijving voor de interview-prompt.
# A4-samenvatting is NIET in deze lijst, die wordt altijd geleverd.
BLOCK_OPTIONS = [
    ('A', 'Woord-Strong-tabel - rauwe tabel per vers met Grieks/Hebreeuws, transliteratie, Strong, parsing en NL-concordant'),
    ('B', 'Etymologisch dieptedossier - wortel, semantische velden, cognaten, zeven-ankers per kernwoord'),
    ('C', 'Cross-references + LXX-bruggen - alle vers-plekken met dezelfde Strong, plus OT-NT LIFT-koppelingen'),
    ('D', 'Vers-lijst per Strong - complete lijst via omgekeerde index, gegroepeerd per genre'),
    ('E', 'Taalkundige synthese - samenvatting van A+B+C+D zonder theologische conclusies'),
    ('F', 'Instagram/Reels-tekst - ~100 woorden voor ElevenLabs-voiceover en Kling-video'),
]

DEPTHS = [
    ('vers', 'Vers-niveau - beperkt tot de exacte verzen die je noemt'),
    ('word', 'Woord-niveau - kernwoorden door de hele Schrift heen volgen'),
    ('theme', 'Thema-niveau - chronologie, parallelle passages, of cross-thematisch onderzoek'),
]


def question_language():
    print("\n[1/3] Output-taal:")
    print("   Operationeel: NL, EN, ES")
    print("   Overige talen vallen terug op NL met waarschuwing.\n")
    for i, (code, name) in enumerate(SUPPORTED_LANGUAGES, 1):
        flag = '*' if code in OPERATIONAL_LANGUAGES else ' '
        print(f"  {flag} {i:>2}. {code} - {name}")
    print("   0. (vrije tekst)")
    raw = input("Keuze (1-17 of 0): ").strip()
    if raw == '0':
        return input("Geef taal-code: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(SUPPORTED_LANGUAGES):
        return SUPPORTED_LANGUAGES[int(raw) - 1][0]
    return 'unknown'


def question_blocks():
    print("\n[2/3] Blokken-keuze:")
    print("   De A4-samenvatting (max 1 A4, concreet antwoord) krijg je altijd.")
    print("   Wil je daarnaast extra blokken? Ja per blok, of leeg laten voor alleen A4.\n")
    selected = []
    for code, desc in BLOCK_OPTIONS:
        raw = input(f"  Blok {code} - {desc}\n  Erbij? (j/n): ").strip().lower()
        if raw in ('j', 'ja', 'y', 'yes'):
            selected.append(code)
    return selected


def question_depth():
    print("\n[3/3] Vers-scope:")
    for i, (code, name) in enumerate(DEPTHS, 1):
        print(f"  {i}. {code} - {name}")
    print("  0. (vrije tekst)")
    raw = input("Keuze (1-3 of 0): ").strip()
    if raw == '0':
        return input("Geef diepte: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(DEPTHS):
        return DEPTHS[int(raw) - 1][0]
    return 'unknown'


def run_interview():
    """Voer interactief interview uit. Returns dict zonder defaults."""
    return {
        'language': question_language(),
        'blocks_requested': question_blocks(),
        'depth': question_depth(),
    }


def parse_blocks_str(blocks_str):
    """Parse 'ACE' of 'A,C,E' of '' naar lijst ['A','C','E'] of []."""
    if not blocks_str:
        return []
    cleaned = blocks_str.replace(',', '').replace(' ', '').upper()
    valid = {code for code, _ in BLOCK_OPTIONS}
    return [c for c in cleaned if c in valid]


def parse_auto(spec):
    """Parse 'nl,ACE,vers' naar dict. Alleen voor automation/testing.
    Tweede veld mag leeg zijn ('nl,,vers' = alleen A4)."""
    parts = [p.strip() for p in spec.split(',', 2)]
    if len(parts) != 3:
        raise ValueError("--auto verwacht 3 komma-gescheiden waarden: language,blocks,depth")
    return {
        'language': parts[0],
        'blocks_requested': parse_blocks_str(parts[1]),
        'depth': parts[2],
    }


def infer_from_query(query):
    """Probeer dimensies te detecteren in gebruikersvraag.
    Niet-gedetecteerde waarden krijgen 'unknown' - geen stille defaults."""
    q = query.lower()
    out = {
        'language': 'unknown',
        'blocks_requested': 'unknown',
        'depth': 'unknown',
    }

    # Taal-detectie
    if re.search(r'\b(in het nederlands|in dutch|in nederlands|nederlands)\b', q):
        out['language'] = 'nl'
    elif re.search(r'\b(in english|in het engels|engels)\b', q):
        out['language'] = 'en'
    elif re.search(r'\b(in spanish|in het spaans|spaans|en espanol)\b', q):
        out['language'] = 'es'
    elif re.search(r'\b(in french|in het frans|frans|en francais)\b', q):
        out['language'] = 'fr'
    elif re.search(r'\b(in italian|in het italiaans|italiaans)\b', q):
        out['language'] = 'it'
    elif re.search(r'\b(in portuguese|in het portugees|portugees)\b', q):
        out['language'] = 'pt'
    elif re.search(r'\b(in russian|in het russisch|russisch)\b', q):
        out['language'] = 'ru'
    elif re.search(r'\b(in arabic|in het arabisch|arabisch)\b', q):
        out['language'] = 'ar'
    elif re.search(r'\b(in chinese|in het chinees|chinees|in mandarin)\b', q):
        out['language'] = 'zh'
    elif re.search(r'\b(in hebrew|in het hebreeuws|hebreeuws)\b', q):
        out['language'] = 'he'

    # Blokken-detectie. We zoeken naar expliciete mentions van blokken of
    # naar formats zoals 'instagram', 'reels', 'transcript' voor Blok F.
    # Default als de gebruiker niets noemt = onbekend (geen stille A4-only-aanname).
    blocks = []
    blocks_mentioned = False
    if re.search(r'\b(blok\s*a|woord-strong|woord strong|strong-tabel)\b', q):
        blocks.append('A'); blocks_mentioned = True
    if re.search(r'\b(blok\s*b|etymologie|wortel|wortel-analyse|zeven ankers|diepte-dossier|woordstudie)\b', q):
        blocks.append('B'); blocks_mentioned = True
    if re.search(r'\b(blok\s*c|cross-reference|cross reference|kruisreferent|lxx|parallelplaats)\b', q):
        blocks.append('C'); blocks_mentioned = True
    if re.search(r'\b(blok\s*d|vers-lijst|vers lijst|omgekeerde index|alle voorkomens)\b', q):
        blocks.append('D'); blocks_mentioned = True
    if re.search(r'\b(blok\s*e|synthese|taalkundige synthese)\b', q):
        blocks.append('E'); blocks_mentioned = True
    if re.search(r'\b(blok\s*f|instagram|reels|elevenlabs|kling|video-transcript|40 sec|veertig seconden|transcript)\b', q):
        blocks.append('F'); blocks_mentioned = True
    if re.search(r'\b(volledig dossier|alle blokken|alles erbij|full dossier|complete analyse)\b', q):
        blocks = ['A', 'B', 'C', 'D', 'E']  # F blijft expliciet opt-in
        blocks_mentioned = True
    if re.search(r'\b(alleen a4|alleen samenvatting|alleen de samenvatting|kort antwoord|alleen kort|geen blokken|short answer only|just the summary)\b', q):
        blocks = []
        blocks_mentioned = True
    if blocks_mentioned:
        seen = set()
        out['blocks_requested'] = [b for b in blocks if not (b in seen or seen.add(b))]

    # Depth-detectie
    if re.search(r'\b(chronologi|tijdrekening|jaren sinds|hoeveel jaar|anno hominis|anno mundi|geslachtsregister|tijdlijn|cross-thema|cross thema|over heel|door de hele schrift)\b', q):
        out['depth'] = 'theme'
    elif re.search(r'\b(woordstudie|word study|wortel van|etymologie|strong-code|strong nummer|wat betekent\s+\w+\b)\b', q):
        out['depth'] = 'word'
    elif re.search(r'\b\w+\s*\d+:\d+\b', q) or re.search(r'\bvers\b', q):
        out['depth'] = 'vers'

    return out


def is_operational(lang):
    return lang in OPERATIONAL_LANGUAGES


def build_confirm_prompt(result):
    """Bouw Nederlandstalige bevestigingsprompt voor Claude na infer."""
    lang = result.get('language')
    lang_label = next((name for code, name in SUPPORTED_LANGUAGES if code == lang), lang)
    depth = result.get('depth')
    depth_label = next((name for code, name in DEPTHS if code == depth), depth)

    blocks = result.get('blocks_requested')
    if blocks == 'unknown':
        blocks_label = 'NOG NIET BEKEND (vraag de gebruiker)'
    elif isinstance(blocks, list) and not blocks:
        blocks_label = 'alleen A4-samenvatting (geen extra blokken)'
    elif isinstance(blocks, list):
        labels = []
        for code in blocks:
            desc = next((d for c, d in BLOCK_OPTIONS if c == code), code)
            labels.append(f"{code} ({desc.split(' - ')[0]})")
        blocks_label = 'A4 + ' + ', '.join(labels)
    else:
        blocks_label = str(blocks)

    parts = []
    parts.append("Voor ik begin, bevestig je deze keuzes?")
    parts.append(f"Taal: {lang_label}")
    if lang and lang != 'unknown' and not is_operational(lang):
        parts.append(f"  LET OP: {lang} is nog niet operationeel. Operationeel: NL, EN, ES. Voorstel: terugvallen op NL?")
    parts.append(f"Output: {blocks_label}")
    parts.append(f"Vers-scope: {depth_label}")
    if result.get('missing'):
        miss = ', '.join(result['missing'])
        parts.append(f"Nog open: {miss} - geef je hier de keuze voor?")
    return '\n'.join(parts)


def compute_missing(result):
    missing = []
    for k in ('language', 'depth'):
        if result.get(k) == 'unknown':
            missing.append(k)
    if result.get('blocks_requested') == 'unknown':
        missing.append('blocks_requested')
    return missing


def main():
    args = sys.argv[1:]
    json_out = '--json' in args
    enforce = '--enforce' in args
    confirm = '--confirm' in args

    if '--auto' in args:
        i = args.index('--auto')
        spec = args[i+1] if i+1 < len(args) else ''
        result = parse_auto(spec)
    elif '--infer' in args:
        i = args.index('--infer')
        q = args[i+1] if i+1 < len(args) else ''
        result = infer_from_query(q)
    else:
        result = run_interview()

    lang = result.get('language')
    result['language_operational'] = is_operational(lang) if lang and lang != 'unknown' else None

    result['missing'] = compute_missing(result)

    if confirm:
        result['confirm_prompt'] = build_confirm_prompt(result)

    if json_out:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("\nInterview-uitkomst:")
        for k, v in result.items():
            if k == 'confirm_prompt':
                print(f"\n  {k}:\n{v}")
            else:
                print(f"  {k:>20}: {v}")

    if enforce and result['missing']:
        sys.exit(1)


if __name__ == '__main__':
    main()
