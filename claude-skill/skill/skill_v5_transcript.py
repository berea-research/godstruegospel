"""
skill_v5_transcript.py — godstruegospel skill v5, module 4: video-transcript
============================================================================

Bouwt Blok F (video-transcript) per godstruegospel-v5-eindspec sectie 5:
- 100-110 woorden plain text
- Vaste structuur:
    * ~8 sec vraag      (~16-22 woorden)
    * ~27 sec antwoord  (~70-78 woorden), met 2-3 bijbelverwijzingen
    * ~5 sec slotzin    (~12-15 woorden)
- Geschikt voor ElevenLabs voice-synthese -> Kling 3.0 video-pipeline
- Geen markdown, geen opsommingstekens, geen headers

CLI:
    python3 skill_v5_transcript.py --vers joh:3:16 --taal nl
    python3 skill_v5_transcript.py --vers joh:3:16 --taal nl --vraag "Wat zegt Joh 3:16?"
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_v5_lookup as lk

WORD_TARGET_MIN = 95
WORD_TARGET_MAX = 115

PROMPTS = {
    'nl': {
        'open_default': 'De vraag is: wat staat er werkelijk geschreven in {ref}?',
        'kerns_intro': 'In de grondtekst lezen we {kerns}.',
        'parallel_intro': 'Parallel daarmee staan',
        'sluit_default': 'Het concordante woord vraagt geen vertaling, maar luisteren.',
        'tweede_context': 'Naast {eerste_translit} draagt ook {tweede_translit} betekenis: {tweede_concordant}.',
        'parallel_tail': '{p1} en {p2}; daar staat hetzelfde grondwoord en belicht een ander aspect.',
        'derde_context': 'Ook {translit} ({concordant}) staat in dit vers en versterkt de boodschap.',
        'reflectie': 'Deze drie grondwoorden samen openen een laag die in een gewone vertaling makkelijk vlak wordt. Door ze concordant te lezen blijft de eigen klank van de tekst hoorbaar.',
        'vers_niet_gevonden': '[Vers niet gevonden: {ref}]',
    },
    'en': {
        'open_default': 'The question is: what does {ref} actually say in the source text?',
        'kerns_intro': 'In the source text we read {kerns}.',
        'parallel_intro': 'In parallel we find',
        'sluit_default': 'The concordant word asks no translation, only listening.',
        'tweede_context': 'Alongside {eerste_translit}, {tweede_translit} also carries meaning: {tweede_concordant}.',
        'parallel_tail': '{p1} and {p2}; the same root word stands there and lights up another aspect.',
        'derde_context': '{translit} ({concordant}) also stands in this verse and reinforces the message.',
        'reflectie': 'These three root words together open a layer that an ordinary translation easily flattens. Reading them concordantly keeps the text\'s own sound audible.',
        'vers_niet_gevonden': '[Verse not found: {ref}]',
    },
}


def _concordant_key(lang):
    return f'{lang}_concordant'


def _concordant_value(master, lang):
    if not master:
        return ''
    val = master.get(_concordant_key(lang))
    if val:
        return val
    return master.get('nl_concordant', '')


def count_words(s):
    return len(re.findall(r'\b\w+\b', s))


def shorten_to(text, max_words):
    words = text.split()
    if len(words) <= max_words:
        return text
    return ' '.join(words[:max_words]).rstrip('.,;:') + '...'


def build_transcript_voor_vers(vers_ref, lang='nl', vraag=None):
    """Build transcript van 95-115 woorden (target 100-110) volgens eindspec
    sectie 5 Blok F."""
    boek, h, v = lk.parse_vers_ref(vers_ref)
    row = lk.lookup_vers(boek, h, v, with_strong=True)
    p = PROMPTS.get(lang, PROMPTS['nl'])
    if not row:
        return p['vers_niet_gevonden'].format(ref=vers_ref)

    vraag_open = vraag or p['open_default'].format(ref=f"{boek.upper()} {h}:{v}")

    # Kernwoorden: pak top-3 inhoudswoorden
    SKIP_PARSING = {'pn', 't_', 'Conj', 'Prep', 'Part Neg', 'Adv'}
    kernen = []
    seen = set()
    for w in row['words']:
        s = w.get('strong', '')
        ws = (w.get('parsing') or '').split()[0] if w.get('parsing') else ''
        if not s or s in seen or ws in SKIP_PARSING:
            continue
        if w.get('parsing','').startswith(('t_', 'pp')):
            continue
        seen.add(s)
        master = lk.lookup_strong(s, taal=lang)
        if master:
            kernen.append({
                'strong': s,
                'translit': w.get('translit', ''),
                'concordant': _concordant_value(master, lang),
                'toel': master.get('toelichting', ''),
            })
        if len(kernen) >= 3:
            break

    # Segmenten bouwen
    if kernen:
        kerns_str = ', '.join(f"{k['translit']} ({k['concordant']})" for k in kernen)
        kerns_intro = p['kerns_intro'].format(kerns=kerns_str)
        eerste_toel = ''
        if kernen[0]['toel']:
            zinnen = re.split(r'(?<=[.;])\s', kernen[0]['toel'])
            eerste_toel = zinnen[0] if zinnen else ''
            if len(eerste_toel) > 200:
                eerste_toel = eerste_toel[:197] + '...'
        tweede_context = ''
        if len(kernen) > 1:
            tweede_context = p['tweede_context'].format(
                eerste_translit=kernen[0]['translit'],
                tweede_translit=kernen[1]['translit'],
                tweede_concordant=kernen[1]['concordant'],
            )
    else:
        kerns_intro = ''
        eerste_toel = ''
        tweede_context = ''

    # Parallel-verwijzingen voor 1e kernwoord
    parallels = []
    if kernen:
        s = kernen[0]['strong']
        locs = lk.lookup_index(s, max_n=20)
        for loc in locs:
            if loc['b'] == boek and loc['c'] == h and loc['v'] == v:
                continue
            parallels.append(f"{loc['b']} {loc['c']}:{loc['v']}")
            if len(parallels) >= 2:
                break

    parallel_str = ''
    if parallels:
        tail = p['parallel_tail'].format(p1=parallels[0], p2=parallels[1])
        parallel_str = f"{p['parallel_intro']} {tail}"

    sluit = p['sluit_default']

    # Combineer
    parts = [vraag_open, kerns_intro, eerste_toel, tweede_context, parallel_str, sluit]
    full = ' '.join(x for x in parts if x).strip()
    wc = count_words(full)

    # Tuning naar target 95-115
    if wc < WORD_TARGET_MIN and len(kernen) > 2:
        derde = p['derde_context'].format(
            translit=kernen[2]['translit'],
            concordant=kernen[2]['concordant'],
        )
        parts = [vraag_open, kerns_intro, eerste_toel, tweede_context, derde,
                 parallel_str, sluit]
        full = ' '.join(x for x in parts if x).strip()
        wc = count_words(full)

    if wc > WORD_TARGET_MAX:
        parts = [vraag_open, kerns_intro, eerste_toel, parallel_str, sluit]
        full = ' '.join(x for x in parts if x).strip()
        wc = count_words(full)
        if wc > WORD_TARGET_MAX:
            full = shorten_to(full, WORD_TARGET_MAX)
            wc = count_words(full)

    # Tweede tuning-pass: nog steeds onder min? Voeg reflectie toe.
    if wc < WORD_TARGET_MIN and kernen:
        reflectie = p['reflectie']
        parts_with_refl = [vraag_open, kerns_intro, eerste_toel, tweede_context]
        if len(kernen) > 2:
            parts_with_refl.append(p['derde_context'].format(
                translit=kernen[2]['translit'],
                concordant=kernen[2]['concordant'],
            ))
        parts_with_refl.extend([reflectie, parallel_str, sluit])
        full = ' '.join(x for x in parts_with_refl if x).strip()
        wc = count_words(full)
        # Als we nu boven max zijn, kort in
        if wc > WORD_TARGET_MAX:
            full = shorten_to(full, WORD_TARGET_MAX)
            wc = count_words(full)

    return {
        'transcript': full.strip(),
        'word_count': wc,
        'estimated_seconds': round(wc / 2.5, 1),
        'lang': lang,
        'vers': vers_ref,
        'kernen': [{'strong': k['strong'], 'translit': k['translit'],
                    'concordant': k['concordant']}
                   for k in kernen],
        'parallels': parallels,
    }


def main():
    args = sys.argv[1:]

    def get(flag, default=None):
        if flag in args:
            i = args.index(flag)
            return args[i+1] if i+1 < len(args) else default
        return default

    vers = get('--vers')
    lang = get('--taal', 'nl')
    vraag = get('--vraag')
    json_out = '--json' in args

    if not vers:
        print(__doc__)
        return

    result = build_transcript_voor_vers(vers, lang=lang, vraag=vraag)

    if json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"# Transcript ({result['lang']}) — {result['vers']}")
        print(f"# {result['word_count']} woorden, ~{result['estimated_seconds']}s gesproken\n")
        print(result['transcript'])


if __name__ == '__main__':
    main()
