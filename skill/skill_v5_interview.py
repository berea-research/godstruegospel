"""
skill_v5_interview.py — godstruegospel skill v5.1, module 1: interview
======================================================================

Drie-vragen-interview voor de godstruegospel skill. v5.1 aanpassingen:
- Default-modus is geen-default-meer: bij ontbrekende dimensies returnt het
  script 'unknown' en exit-code 1, zodat de aanroeper expliciet door moet vragen.
- Nieuwe vlag --enforce: faalt hard als ook na infer dimensies onbekend zijn,
  met een JSON-payload die aangeeft welke vragen aan de gebruiker gesteld
  moeten worden.
- Nieuwe vlag --confirm: bouwt een Nederlandstalige bevestigingsprompt die
  Claude in de chat kan stellen na een geslaagde infer.

Levert structured output:
    {
      "language": "nl" | "en" | ... | "unknown",
      "output_type": "dossier" | "summary" | "transcript" | "unknown",
      "depth": "vers" | "word" | "theme" | "unknown",
      "missing": ["language", ...],
      "confirm_prompt": "... (alleen bij --confirm)"
    }

CLI / direct-aanroep:
    python3 skill_v5_interview.py                       # interactief
    python3 skill_v5_interview.py --auto nl,dossier,vers # skip-modus (alleen voor automation)
    python3 skill_v5_interview.py --json                # alleen JSON terug
    python3 skill_v5_interview.py --infer "<vraag>" --json
    python3 skill_v5_interview.py --infer "<vraag>" --enforce --json   # exit 1 als incompleet
    python3 skill_v5_interview.py --infer "<vraag>" --confirm --json   # met confirm-prompt
"""
import json
import re
import sys

SUPPORTED_LANGUAGES = [
    ('nl', 'Nederlands'),
    ('en', 'English'),
    ('fr', 'français'),
    ('it', 'Italiano'),
    ('es', 'Español'),
    ('pt', 'Português'),
    ('bg', 'български'),
    ('ru', 'русский'),
    ('ar', 'العربية'),
    ('hi', 'हिन्दी'),
    ('zh', '汉语'),
    ('ja', '日本語'),
    ('ko', '한국어'),
    ('tr', 'Türkçe'),
    ('el', 'ελληνικά'),
    ('ta', 'தமிழ்'),
    ('he', 'עברית'),
]

OUTPUT_TYPES = [
    ('dossier', 'Volledig dossier (Blok A-E)'),
    ('summary', 'Korte tekstuele samenvatting'),
    ('transcript', 'Video-transcript (Blok F, ~40s)'),
]

DEPTHS = [
    ('vers', 'Vers-niveau'),
    ('word', 'Woordstudie'),
    ('theme', 'Cross-thema onderzoek (chronologie, parallelle passages, etc.)'),
]


def question_language():
    print("\n[1/3] Output-taal:\n")
    for i, (code, name) in enumerate(SUPPORTED_LANGUAGES, 1):
        print(f"  {i:>2}. {code} - {name}")
    print("   0. (vrije tekst)")
    raw = input("Keuze (1-17 of 0): ").strip()
    if raw == '0':
        return input("Geef taal-code: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(SUPPORTED_LANGUAGES):
        return SUPPORTED_LANGUAGES[int(raw) - 1][0]
    return 'unknown'


def question_output_type():
    print("\n[2/3] Type uitvoer:\n")
    for i, (code, name) in enumerate(OUTPUT_TYPES, 1):
        print(f"  {i}. {code} - {name}")
    print("  0. (vrije tekst)")
    raw = input("Keuze (1-3 of 0): ").strip()
    if raw == '0':
        return input("Geef output-type: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(OUTPUT_TYPES):
        return OUTPUT_TYPES[int(raw) - 1][0]
    return 'unknown'


def question_depth():
    print("\n[3/3] Onderzoeksdiepte:\n")
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
        'output_type': question_output_type(),
        'depth': question_depth(),
    }


def parse_auto(spec):
    """Parse 'nl,dossier,vers' naar dict. Alleen voor automation/testing."""
    parts = [p.strip() for p in spec.split(',')]
    if len(parts) != 3:
        raise ValueError("--auto verwacht 3 komma-gescheiden waarden: language,output_type,depth")
    return {'language': parts[0], 'output_type': parts[1], 'depth': parts[2]}


def infer_from_query(query):
    """Probeer dimensies te detecteren in gebruikersvraag.
    Niet-gedetecteerde waarden krijgen 'unknown' — geen stille defaults."""
    q = query.lower()
    out = {'language': 'unknown', 'output_type': 'unknown', 'depth': 'unknown'}

    # Taal-detectie
    if re.search(r'\b(in het nederlands|in dutch|in nederlands|nederlands)\b', q):
        out['language'] = 'nl'
    elif re.search(r'\b(in english|in het engels|engels)\b', q):
        out['language'] = 'en'
    elif re.search(r'\b(in french|in het frans|frans|en français)\b', q):
        out['language'] = 'fr'
    elif re.search(r'\b(in spanish|in het spaans|spaans|en español)\b', q):
        out['language'] = 'es'
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

    # Output-type-detectie
    if re.search(r'\b(transcript|video|kling|elevenlabs|40 sec|veertig seconden)\b', q):
        out['output_type'] = 'transcript'
    elif re.search(r'\b(samenvatting|summary|kort antwoord|korte samenvatting|in het kort)\b', q):
        out['output_type'] = 'summary'
    elif re.search(r'\b(dossier|volledig dossier|full dossier|complete analyse)\b', q):
        out['output_type'] = 'dossier'

    # Depth-detectie
    if re.search(r'\b(chronologi|tijdrekening|jaren sinds|hoeveel jaar|anno hominis|anno mundi|geslachtsregister|tijdlijn|cross-thema|cross thema|over heel|door de hele schrift)\b', q):
        out['depth'] = 'theme'
    elif re.search(r'\b(woordstudie|word study|wortel van|etymologie|strong-code|strong nummer|wat betekent\s+\w+\b)\b', q):
        out['depth'] = 'word'
    elif re.search(r'\b\w+\s*\d+:\d+\b', q) or re.search(r'\bvers\b', q):
        out['depth'] = 'vers'

    return out


def build_confirm_prompt(result):
    """Bouw Nederlandstalige bevestigingsprompt voor Claude na infer."""
    lang_label = next((name for code, name in SUPPORTED_LANGUAGES if code == result.get('language')), result.get('language'))
    type_label = next((name for code, name in OUTPUT_TYPES if code == result.get('output_type')), result.get('output_type'))
    depth_label = next((name for code, name in DEPTHS if code == result.get('depth')), result.get('depth'))

    parts = []
    parts.append("Voor ik begin, bevestig je deze dimensies?")
    parts.append(f"Taal: {lang_label} | Type: {type_label} | Diepte: {depth_label}")
    if result.get('missing'):
        miss = ", ".join(result['missing'])
        parts.append(f"Nog open: {miss} — geef je hier de keuze voor?")
    return "\n".join(parts)


def compute_missing(result):
    return [k for k in ('language', 'output_type', 'depth') if result.get(k) == 'unknown']


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
                print(f"  {k:>14}: {v}")

    # Exit-code: 1 als enforce en nog dimensies missen
    if enforce and result['missing']:
        sys.exit(1)


if __name__ == '__main__':
    main()
