"""
skill_v5_blocks.py — godstruegospel skill v5.4, module 3: output-blokken
=======================================================================

Bouwt A4-samenvatting (default) en optionele Blokken A t/m E van de
skill-uitvoer. Blok F wordt door skill_v5_transcript.py geleverd.

v5.4 aanpassingen:
- Nieuwe modus `--a4` produceert een A4-samenvatting-skeleton (max 1 A4)
  met bronnen-manifest-hook en vers-verankering reeds ingevuld. De prose
  van de concrete-antwoord-sectie wordt door Claude geschreven op basis
  van het grondige onderzoek (kennisbank-bron, sola scriptura).
- `--blok` blijft beschikbaar voor de opt-in blokken uit het interview.
- A4 is altijd inbegrepen; `--blok` voegt blokken toe boven op de A4.

Blokken:
  A4. Concreet antwoord  - max 1 A4 synthese met directe vers-verwijzingen
  A.  Vers-context       - vers-citatie + transliteratie + woord-Strong
  B.  Woordstudie        - per kernwoord wortel/etym/basis/clusters uit diepte
  C.  Cognaten + LXX     - zustertalen + LXX-mapping
  D.  Parallelplaatsen   - omgekeerde index gegroepeerd per genre
  E.  Synthese           - taalkundige samenvatting (geen vertaal-traditie)

CLI:
    python3 skill_v5_blocks.py --vers joh:3:16 --taal nl --a4
    python3 skill_v5_blocks.py --vers joh:3:16 --taal nl --a4 --blok ACE
    python3 skill_v5_blocks.py --vers joh:3:16 --taal nl --blok ABCDE
    python3 skill_v5_blocks.py --strong G3056 --taal nl --blok B
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# Import lookup-module uit dezelfde folder
sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_v5_lookup as lk


# === Genre-mapping (deel met generate_diepte_template.py) ===
HEB_GENRES = {
    'Tora': {'gen', 'exo', 'lev', 'num', 'deu'},
    'Vroege Profeten': {'jos', 'jdg', '1sa', '2sa', '1kg', '2kg'},
    'Late Profeten': {'isa', 'jer', 'eze', 'hos', 'joe', 'amo', 'oba', 'jon',
                      'mic', 'nah', 'hab', 'zep', 'hag', 'zec', 'mal'},
    'Geschriften': {'psa', 'pro', 'job', 'can', 'rut', 'lam', 'qoh', 'est',
                    'dan', 'ezr', 'neh', '1ch', '2ch'},
}
NT_GENRES = {
    'Evangelien + Hand': {'mat', 'mar', 'luk', 'joh', 'act'},
    'Paulus': {'rom', '1co', '2co', 'gal', 'eph', 'phi', 'col', '1th', '2th',
               '1ti', '2ti', 'tit', 'phm'},
    'Algemene brieven': {'heb', 'jam', '1pe', '2pe', '1jo', '2jo', '3jo', 'jud'},
    'Openbaring': {'rev'},
}


# === Vertaal-gevoelige strings (uitbreidbaar per taal) ===
PROMPT_TEMPLATES = {
    'nl': {
        'block_a_title': '## Blok A — Vers-context',
        'block_b_title': '## Blok B — Woordstudie',
        'block_c_title': '## Blok C — Cognaten en LXX-koppeling',
        'block_d_title': '## Blok D — Parallelplaatsen',
        'block_e_title': '## Blok E — Synthese',
        'verse_label': 'Vers',
        'words_label': 'Woord-voor-woord',
        'word_label': 'Woord',
        'strong_label': 'Strong',
        'translit_label': 'Transliteratie',
        'concordant_label': 'NL-concordant',
        'root_label': 'Wortel',
        'etym_label': 'Etymologie',
        'meaning_label': 'Basisbetekenis',
        'cognates_label': 'Cognaten in zustertalen',
        'lxx_label': 'LXX-tegenhanger',
        'lxx_h_to_g_label': 'LXX-tegenhanger (H -> G in LXX)',
        'lxx_g_to_h_label': 'LXX-bronnen (G <- H bij Septuaginta-vertaling)',
        'parallels_label': 'Parallelplaatsen via omgekeerde index',
        'no_diepte': '_Geen diepte-notitie beschikbaar voor {strong}._',
        'no_lxx': '_Geen LXX-mapping beschikbaar (G-prefix of geen significante mapping)._',
        'synthesis_intro': 'Taalkundige synthese op basis van A t/m D, strikt concordant zonder vertaal-traditie.',
        'verse_not_found': '_Vers {ref} niet gevonden._',
        'kernwoorden_count_label': 'Aantal kernwoorden behandeld',
        'kern_findings_label': 'Kern-bevindingen per Strong-code',
        'verse_context_label': 'Vers',
        'fallback_note': '_Vertaling ontleend aan NL-master (EN-master nog niet gevuld voor deze Strong-code)._',
        'further_synthesis_note': '_Verdere synthese vraagt om handmatige interpretatie binnen de zeven-ankers-discipline._',
    },
    'en': {
        'block_a_title': '## Block A — Verse context',
        'block_b_title': '## Block B — Word study',
        'block_c_title': '## Block C — Cognates and LXX',
        'block_d_title': '## Block D — Parallel passages',
        'block_e_title': '## Block E — Synthesis',
        'verse_label': 'Verse',
        'words_label': 'Word-by-word',
        'word_label': 'Word',
        'strong_label': 'Strong',
        'translit_label': 'Transliteration',
        'concordant_label': 'EN-concordant',
        'root_label': 'Root',
        'etym_label': 'Etymology',
        'meaning_label': 'Base meaning',
        'cognates_label': 'Cognates in sister languages',
        'lxx_label': 'LXX equivalent',
        'lxx_h_to_g_label': 'LXX equivalent (H -> G in LXX)',
        'lxx_g_to_h_label': 'LXX sources (G <- H at Septuagint translation)',
        'parallels_label': 'Parallel passages via reverse index',
        'no_diepte': '_No depth note available for {strong}._',
        'no_lxx': '_No LXX mapping available (G-prefix or no significant mapping)._',
        'synthesis_intro': 'Linguistic synthesis based on A through D, strictly concordant without translation tradition.',
        'verse_not_found': '_Verse {ref} not found._',
        'kernwoorden_count_label': 'Number of key words covered',
        'kern_findings_label': 'Core findings per Strong-code',
        'verse_context_label': 'Verse',
        'fallback_note': '_Translation borrowed from NL master (EN master not yet filled for this Strong-code)._',
        'further_synthesis_note': '_Further synthesis requires manual interpretation within the seven-anchor discipline._',
    },
    'es': {
        'block_a_title': '## Bloque A — Contexto del verso',
        'block_b_title': '## Bloque B — Estudio de palabra',
        'block_c_title': '## Bloque C — Cognados y LXX',
        'block_d_title': '## Bloque D — Pasajes paralelos',
        'block_e_title': '## Bloque E — Síntesis',
        'verse_label': 'Verso',
        'words_label': 'Palabra por palabra',
        'word_label': 'Palabra',
        'strong_label': 'Strong',
        'translit_label': 'Transliteración',
        'concordant_label': 'ES-concordante',
        'root_label': 'Raíz',
        'etym_label': 'Etimología',
        'meaning_label': 'Significado base',
        'cognates_label': 'Cognados en lenguas hermanas',
        'lxx_label': 'Equivalente LXX',
        'lxx_h_to_g_label': 'Equivalente LXX (H -> G en LXX)',
        'lxx_g_to_h_label': 'Fuentes LXX (G <- H en traducción Septuaginta)',
        'parallels_label': 'Pasajes paralelos vía índice inverso',
        'no_diepte': '_No hay nota de profundidad disponible para {strong}._',
        'no_lxx': '_No hay mapeo LXX disponible (prefijo G o sin mapeo significativo)._',
        'synthesis_intro': 'Síntesis lingüística basada en A hasta D, estrictamente concordante sin tradición de traducción.',
        'verse_not_found': '_Verso {ref} no encontrado._',
        'kernwoorden_count_label': 'Número de palabras clave cubiertas',
        'kern_findings_label': 'Hallazgos por código Strong',
        'verse_context_label': 'Verso',
        'fallback_note': '_Traducción tomada del master NL (master ES aún no completado para este Strong)._',
        'further_synthesis_note': '_La síntesis adicional requiere interpretación manual dentro de la disciplina de siete anclas._',
    },
}

# A4-template-strings per taal. De prose-secties zijn placeholders die door
# Claude worden ingevuld op basis van het bronnen-onderzoek.
A4_TEMPLATES = {
    'nl': {
        'title': '# A4-samenvatting — {vers_ref}',
        'discipline': '> _Bron-discipline: sola scriptura via `Kennis/`. Geen training, geen traditie-vertaling, geen theologie. Max 1 A4._',
        'antwoord_header': '## Concreet antwoord',
        'antwoord_placeholder': '_[Claude vult hier de directe beantwoording in, max ~250 woorden, op basis van het onderliggende onderzoek. Begrijpelijk Nederlands, geen technische apparatus. Sola scriptura.]_',
        'verankering_header': '## Vers-verankering',
        'verankering_intro': 'De uitspraak hierboven leunt op de volgende Strong-codes uit `{vers_ref}` plus relevante cross-references:',
        'manifest_header': '## Bronnen-manifest',
        'manifest_placeholder': '_[Claude vult hier de exacte bron-bestanden in die voor deze A4-synthese zijn gelezen.]_',
    },
    'en': {
        'title': '# A4 summary — {vers_ref}',
        'discipline': '> _Source discipline: sola scriptura via `Kennis/`. No training data, no translation tradition, no theology. Max 1 page._',
        'antwoord_header': '## Concrete answer',
        'antwoord_placeholder': '_[Claude fills in the direct answer here, max ~250 words, based on the underlying research. Plain English, no technical apparatus. Sola scriptura.]_',
        'verankering_header': '## Verse anchoring',
        'verankering_intro': 'The statement above rests on the following Strong codes from `{vers_ref}` plus relevant cross-references:',
        'manifest_header': '## Source manifest',
        'manifest_placeholder': '_[Claude fills in the exact source files read for this A4 synthesis.]_',
    },
    'es': {
        'title': '# Resumen A4 — {vers_ref}',
        'discipline': '> _Disciplina de fuentes: sola scriptura vía `Kennis/`. Sin datos de entrenamiento, sin tradición de traducción, sin teología. Máx 1 página._',
        'antwoord_header': '## Respuesta concreta',
        'antwoord_placeholder': '_[Claude rellena aquí la respuesta directa, máx ~250 palabras, basada en la investigación subyacente. Español claro, sin aparato técnico. Sola scriptura.]_',
        'verankering_header': '## Anclaje en versos',
        'verankering_intro': 'La declaración anterior se apoya en los siguientes códigos Strong de `{vers_ref}` más referencias cruzadas relevantes:',
        'manifest_header': '## Manifiesto de fuentes',
        'manifest_placeholder': '_[Claude rellena aquí los archivos fuente exactos leídos para esta síntesis A4.]_',
    },
}


def _concordant_key(lang):
    """Veld-naam voor concordant-waarde in master, per taal."""
    return f'{lang}_concordant'


def _concordant_value(master, lang):
    """Lees concordant-waarde voor opgegeven taal uit een master-entry.
    Valt terug op NL als de doeltaal nog geen waarde heeft (build-fase)."""
    if not master:
        return ''
    val = master.get(_concordant_key(lang))
    if val:
        return val
    return master.get('nl_concordant', '')


def t(lang, key, **kw):
    """Translation helper."""
    s = PROMPT_TEMPLATES.get(lang, PROMPT_TEMPLATES['nl']).get(
        key, PROMPT_TEMPLATES['nl'].get(key, key))
    return s.format(**kw) if kw else s


# === Helpers diepte-extractie ===

def _extract_section(diepte_md, header_letter):
    """Pak inhoud van sectie 'X. ...' uit diepte-markdown."""
    if not diepte_md:
        return None
    pat = rf'(?ms)^## {header_letter}\.\s.*?(?=^## [A-H]\.|\Z)'
    m = re.search(pat, diepte_md)
    return m.group(0).strip() if m else None


def _extract_field(section, label):
    """Pak '**label:** ...' regel uit een sectie."""
    if not section:
        return None
    pat = rf'\*\*{re.escape(label)}:\*\*\s*(.+?)(?=\n\n|\Z)'
    m = re.search(pat, section, re.DOTALL)
    return m.group(1).strip() if m else None


# === Blok A ===

def block_a(vers_ref, lang='nl'):
    boek, h, v = lk.parse_vers_ref(vers_ref)
    row = lk.lookup_vers(boek, h, v, with_strong=True)
    if not row:
        return t(lang, 'verse_not_found', ref=vers_ref) + '\n'
    out = [t(lang, 'block_a_title')]
    out.append(f"\n**{t(lang, 'verse_label')}:** {boek} {h}:{v}\n")
    out.append(f"\n**{t(lang, 'words_label')}:**\n")
    # Tekstlaag bevat geen literal-vertaling meer (KJV-traditie verwijderd 2026-04-28).
    # In plaats daarvan tonen we de concordante weergave per Strong-code in de
    # gekozen doeltaal (valt terug op NL bij ontbrekende EN-entries tijdens de build).
    # Tabel-kolomtitels: 'word' / 'woord' lang-aware; rest blijft kort/uniform
    # zodat downstream-tests stabiele headers zien.
    word_h = 'woord' if lang == 'nl' else 'word'
    concordant_h = t(lang, 'concordant_label')
    out.append(f"\n| # | {word_h} | translit | strong | parsing | {concordant_h} |")
    out.append("\n|---|---|---|---|---|---|")
    for i, w in enumerate(row['words'], 1):
        woord = w.get('hebreeuws') or w.get('greek', '')
        s = w.get('strong', '')
        master = lk.lookup_strong(s, taal=lang) if s else None
        conc = _concordant_value(master, lang)
        out.append(f"\n| {i} | {woord} | {w.get('translit','')} | "
                   f"{s} | {w.get('parsing','')} | {conc} |")
    return ''.join(out) + '\n'


# === Blok B ===

def block_b(strong_codes, lang='nl'):
    out = [t(lang, 'block_b_title'), '\n']
    seen = set()
    for s in strong_codes:
        if s in seen or not s:
            continue
        seen.add(s)
        master = lk.lookup_strong(s, taal=lang)
        if not master:
            continue
        diepte = lk.lookup_diepte(s)
        woord = master.get('hebreeuws') or master.get('grieks', '')
        translit = master.get('translit', '')
        conc = _concordant_value(master, lang)
        toel = master.get('toelichting', '')
        out.append(f"\n### {s} - {translit} ({woord}) - {conc}\n")
        if master.get('_taal_fallback') == 'nl' and lang != 'nl':
            out.append('\n' + t(lang, 'fallback_note') + '\n')
        # Hapax-markering — uncertainty-discipline volgens eindspec sectie 7
        voork = master.get('voorkomens') or master.get('voorkomens_ca', 0)
        if isinstance(voork, int) and voork <= 1:
            if lang == 'en':
                out.append(f"\n**[hapax]** This word occurs only {voork}x in the corpus. "
                           f"Identity and meaning carry greater uncertainty than with "
                           f"more frequent words. Treat any claims with appropriate restraint.\n")
            else:
                out.append(f"\n**[hapax]** Dit woord komt slechts {voork}x voor in het corpus. "
                           f"Identiteit en betekenis zijn met grotere onzekerheid omgeven dan bij "
                           f"frequentere woorden. Behandel uitspraken met passende terughoudendheid.\n")
        if toel:
            out.append(f"\n_Master:_ {toel}\n")
        if diepte:
            sec_b = _extract_section(diepte, 'B')
            if sec_b:
                # Pak alleen wortel, etym, basisbetekenis (kort)
                wortel = _extract_field(sec_b, 'Wortel')
                etym = _extract_field(sec_b, 'Etymologie')
                basis = _extract_field(sec_b, 'Basisbetekenis')
                if wortel:
                    out.append(f"\n**{t(lang, 'root_label')}:** {wortel[:300]}\n")
                if etym:
                    out.append(f"\n**{t(lang, 'etym_label')}:** {etym[:400]}\n")
                if basis:
                    out.append(f"\n**{t(lang, 'meaning_label')}:** {basis[:400]}\n")
        else:
            out.append('\n' + t(lang, 'no_diepte', strong=s) + '\n')
    return ''.join(out) + '\n'


# === Blok C ===

def block_c(strong_codes, lang='nl'):
    """Blok C: cognaten + LXX-koppeling.
    H-codes -> top-G LXX-tegenhangers (Grieks).
    G-codes -> top-H LXX-bronnen (Hebreeuws OT)."""
    out = [t(lang, 'block_c_title'), '\n']
    seen = set()
    for s in strong_codes:
        if s in seen or not s:
            continue
        seen.add(s)
        diepte = lk.lookup_diepte(s)
        out.append(f"\n### {s}\n")
        if diepte:
            sec_e = _extract_section(diepte, 'E')
            if sec_e:
                cog = _extract_field(sec_e, 'Cognaten in zustertalen')
                if cog:
                    out.append(f"\n**{t(lang, 'cognates_label')}:** {cog[:400]}\n")
        # LXX-mapping in beide richtingen
        lxx = lk.lookup_lxx(s)
        if lxx:
            if s.startswith('H') and lxx.get('top_g'):
                # Hebreeuws: toon top-3 Griekse tegenhangers in LXX
                out.append(f"\n**{t(lang, 'lxx_h_to_g_label')}:**\n")
                for g in lxx['top_g'][:3]:
                    gent = lk.lookup_strong(g['g'], taal=lang)
                    gconc = _concordant_value(gent, lang) or '?'
                    out.append(f"\n- {g['g']} ({gconc}) co={g['count']}, "
                               f"lift={g.get('lift', '?')}")
                out.append('\n')
            elif s.startswith('G') and lxx.get('top_h'):
                # Grieks: toon top-3 Hebreeuwse OT-bronnen waarvan dit Griekse
                # woord in de LXX een vertaling is.
                out.append(f"\n**{t(lang, 'lxx_g_to_h_label')}:**\n")
                for h in lxx['top_h'][:3]:
                    hent = lk.lookup_strong(h['h'], taal=lang)
                    hconc = _concordant_value(hent, lang) or '?'
                    out.append(f"\n- {h['h']} ({hconc}) co={h['count']}, "
                               f"lift={h.get('lift', '?')}")
                out.append('\n')
            else:
                out.append('\n' + t(lang, 'no_lxx') + '\n')
        else:
            out.append('\n' + t(lang, 'no_lxx') + '\n')
    return ''.join(out) + '\n'


# === Blok D ===

def block_d(strong_codes, lang='nl', max_per_strong=20):
    out = [t(lang, 'block_d_title'), '\n']
    seen = set()
    for s in strong_codes:
        if s in seen or not s:
            continue
        seen.add(s)
        locs = lk.lookup_index(s)
        if not locs:
            continue
        is_grieks = s.startswith('G')
        genres = NT_GENRES if is_grieks else HEB_GENRES
        per_genre = defaultdict(list)
        for loc in locs:
            for g, books in genres.items():
                if loc['b'] in books:
                    per_genre[g].append(loc)
                    break
        out.append(f"\n### {s} ({len(locs)} voorkomens)\n")
        for g in genres:
            entries = per_genre.get(g, [])
            if entries:
                preview = ', '.join(f"{e['b']} {e['c']}:{e['v']}"
                                    for e in entries[:max_per_strong // len(genres) + 1])
                out.append(f"\n- **{g}** ({len(entries)}): {preview}"
                           f"{'...' if len(entries) > max_per_strong // len(genres) + 1 else ''}\n")
    return ''.join(out) + '\n'


# === Blok E ===

def block_e(vers_ref, strong_codes, lang='nl'):
    """Synthese — strikt taalkundig, geen theologische conclusie.
    Voor MVP: korte samenvatting van blok-bevindingen."""
    out = [t(lang, 'block_e_title'), '\n']
    out.append(f"\n_{t(lang, 'synthesis_intro')}_\n")
    out.append(f"\n**{t(lang, 'verse_context_label')}:** {vers_ref}\n")
    out.append(f"\n**{t(lang, 'kernwoorden_count_label')}:** {len(set(strong_codes))}\n")
    # Per kernwoord: 1-zin samenvatting uit master.toelichting
    out.append(f"\n**{t(lang, 'kern_findings_label')}:**\n")
    seen = set()
    for s in strong_codes:
        if s in seen or not s:
            continue
        seen.add(s)
        master = lk.lookup_strong(s, taal=lang)
        if not master:
            continue
        conc = _concordant_value(master, lang)
        toel = master.get('toelichting', '')
        first_sent = re.split(r'(?<=[.;])\s', toel)[0] if toel else ''
        out.append(f"\n- **{s}** ({conc}): {first_sent[:200]}")
    out.append('\n\n' + t(lang, 'further_synthesis_note') + '\n')
    return ''.join(out) + '\n'


# === A4-modus (v5.4 default) ===

def block_a4(vers_ref, lang='nl'):
    """A4-samenvatting-skeleton. Max 1 A4 markdown.
    De prose-secties zijn placeholders die door Claude worden ingevuld op
    basis van het onderliggende onderzoek. Het script vult wel de
    structurele bron-data in (vers-referentie, kernwoord-Strongs)."""
    if lang not in A4_TEMPLATES:
        lang = 'nl'  # fallback voor niet-operationele talen
    tmpl = A4_TEMPLATES[lang]

    boek, h, v = lk.parse_vers_ref(vers_ref)
    row = lk.lookup_vers(boek, h, v, with_strong=True)
    if not row:
        return f"# {tmpl['title'].format(vers_ref=vers_ref)}\n\n" \
               f"_{t(lang, 'verse_not_found', ref=vers_ref)}_\n"

    out = []
    out.append(tmpl['title'].format(vers_ref=vers_ref))
    out.append('')
    out.append(tmpl['discipline'])
    out.append('')
    out.append(tmpl['antwoord_header'])
    out.append('')
    out.append(tmpl['antwoord_placeholder'])
    out.append('')
    out.append(tmpl['verankering_header'])
    out.append('')
    out.append(tmpl['verankering_intro'].format(vers_ref=vers_ref))
    out.append('')
    # Vul de kernwoord-Strongs reeds in zodat Claude daarop kan steunen.
    # We filteren grammaticale woorden (lidwoorden, voorzetsels, voegwoorden,
    # partikels, pronomina) op basis van de parsing-prefix in het vers-record
    # — die is betrouwbaarder dan master.woordsoort (die de Nederlandse
    # afkortingen lw/vgw/vz gebruikt en niet altijd consistent gevuld is).
    SKIP_PARSING_PREFIXES = ('t_', 'Prep', 'Part', 'Conj', 'pp', 'pf', 'pr', 'px', 'pd', 'ps', 'Cond', 'Adv')
    seen = set()
    for w in row['words']:
        s = w.get('strong', '')
        if not s or s in seen:
            continue
        parsing = w.get('parsing', '')
        if any(parsing.startswith(p) for p in SKIP_PARSING_PREFIXES):
            continue
        seen.add(s)
        master = lk.lookup_strong(s, taal=lang)
        if not master:
            continue
        conc = _concordant_value(master, lang)
        woord = master.get('hebreeuws') or master.get('grieks', '')
        translit = master.get('translit', '')
        out.append(f"- **{s}** {woord} ({translit}) — {conc}")
    out.append('')
    out.append(tmpl['manifest_header'])
    out.append('')
    out.append(tmpl['manifest_placeholder'])
    out.append('')
    return '\n'.join(out)


# === Composer ===

def build_dossier(vers_ref, lang='nl', blokken='', include_a4=True):
    """Bouwt complete output: optionele A4 + optionele blokken.
    v5.4: A4 is default-inbegrepen (include_a4=True); blokken alleen wanneer
    expliciet in `blokken` (de string uit blocks_requested van het interview).
    Lege `blokken` met include_a4=True = alleen A4 (default-uitkomst)."""
    boek, h, v = lk.parse_vers_ref(vers_ref)
    row = lk.lookup_vers(boek, h, v, with_strong=True)
    if not row:
        return f"# Vers niet gevonden: {vers_ref}\n"
    strong_codes = [w.get('strong') for w in row['words'] if w.get('strong')]

    sections = []
    if include_a4:
        sections.append(block_a4(vers_ref, lang))
    if blokken:
        sections.append(f"# Godstruegospel — Aanvullende blokken — {vers_ref}\n")
        if 'A' in blokken:
            sections.append(block_a(vers_ref, lang))
        if 'B' in blokken:
            sections.append(block_b(strong_codes, lang))
        if 'C' in blokken:
            sections.append(block_c(strong_codes, lang))
        if 'D' in blokken:
            sections.append(block_d(strong_codes, lang))
        if 'E' in blokken:
            sections.append(block_e(vers_ref, strong_codes, lang))
    return '\n'.join(sections)


def main():
    """CLI-aanroep. v5.4-semantiek:
    - A4-samenvatting is default-inbegrepen voor --vers-aanroepen.
    - --blok <subset van ABCDE> voegt opt-in blokken toe boven op de A4.
    - --no-a4 sluit de A4 expliciet uit (backward-compat voor tests).
    - --a4-only levert alleen de A4 zonder enige wrapper."""
    args = sys.argv[1:]

    def get(flag, default=None):
        if flag in args:
            i = args.index(flag)
            return args[i+1] if i+1 < len(args) else default
        return default

    def has_flag(flag):
        return flag in args

    vers = get('--vers')
    strong = get('--strong')
    lang = get('--taal', 'nl')
    blok = get('--blok', '')
    a4_only = has_flag('--a4-only')
    no_a4 = has_flag('--no-a4')
    # A4 default ON tenzij expliciet uitgezet, of --strong-modus (geen vers-context)
    a4 = not no_a4 or has_flag('--a4')
    if a4_only:
        a4 = True

    if vers:
        if a4_only:
            print(block_a4(vers, lang))
        else:
            print(build_dossier(vers, lang=lang, blokken=blok, include_a4=a4))
    elif strong:
        # Strong-modus: geen vers-context dus geen A4. Alleen losse blokken.
        codes = [strong]
        if 'B' in blok:
            print(block_b(codes, lang))
        if 'C' in blok:
            print(block_c(codes, lang))
        if 'D' in blok:
            print(block_d(codes, lang))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
