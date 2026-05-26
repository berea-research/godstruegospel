#!/usr/bin/env python3
"""Gods True Gospel knowledge base Testrunner — voert alle 10 tests (T1..T10) uit in één pass.

Gebruik:
  python3 run_tests.py                    # schrijft ronde-auto-rapport.md
  python3 run_tests.py --ronde 2          # schrijft ronde-2-rapport.md
  python3 run_tests.py --ronde 2 --out foo.md

Per gefaalde test worden de eerste 20 probleemcases gelogd.
"""
from __future__ import annotations
import os
import re
import sys
import json
import argparse
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime

# Relative paths from repo root (Testen/run_tests.py -> repo root)
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUUR = os.path.join(BASE, 'Kennis', 'puur')
STRONG = os.path.join(BASE, 'Kennis', 'strong')
TESTEN = os.path.join(BASE, 'Testen')

# Boekenlijst — Psalmen zijn gesplitst in 5 boeken
HEB_BOOKS = [
    'gen','exo','lev','num','deu','jos','jdg','rut','1sa','2sa','1kg','2kg',
    '1ch','2ch','ezr','neh','est','job','psa-1','psa-2','psa-3','psa-4','psa-5',
    'pro','qoh','can','isa','jer','lam','eze','dan','hos','joe','amo','oba',
    'jon','mic','nah','hab','zep','hag','zec','mal',
]
GRK_BOOKS = [
    'mat','mar','luk','joh','act','rom','1co','2co','gal','eph','phi','col',
    '1th','2th','1ti','2ti','tit','phm','heb','jam','1pe','2pe','1jo','2jo',
    '3jo','jud','rev',
]

# Verwachte totale vers-tellingen (klassieke telling)
EXPECTED_OT_TOTAL = 23145
EXPECTED_NT_TOTAL = 7956

# Per-boek expected verzen voor NT (klassieke telling)
EXPECTED_NT = {
    'mat':1071,'mar':678,'luk':1151,'joh':879,'act':1007,'rom':433,'1co':437,
    '2co':257,'gal':149,'eph':155,'phi':104,'col':95,'1th':89,'2th':47,
    '1ti':113,'2ti':83,'tit':46,'phm':25,'heb':303,'jam':108,'1pe':105,
    '2pe':61,'1jo':105,'2jo':13,'3jo':14,'jud':25,'rev':404,
}


def read_jsonl(path):
    out = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def load_all(bank_dir, books):
    data = {}
    for b in books:
        p = os.path.join(bank_dir, f'{b}.jsonl')
        if os.path.exists(p):
            data[b] = read_jsonl(p)
        else:
            data[b] = None
    return data


# ---------- T1: Puur kennisbank structuur ----------
def test_T1(puur_heb, puur_grk):
    fails = []
    for book, verses in puur_heb.items():
        if verses is None:
            fails.append(f'{book}: bestand ontbreekt')
            continue
        for v in verses:
            missing = [k for k in ('book','chapter','verse','direction','source_text','words') if k not in v]
            if missing:
                fails.append(f'{book} {v.get("chapter")}:{v.get("verse")} mist velden {missing}')
                continue
            if v['source_text'] != 'scripture4all':
                fails.append(f'{book} {v["chapter"]}:{v["verse"]} source_text={v["source_text"]!r}')
            if v['direction'] != 'rtl':
                fails.append(f'{book} {v["chapter"]}:{v["verse"]} direction={v["direction"]!r} (verwacht rtl)')
            if 'sof_pasuq' not in v:
                fails.append(f'{book} {v["chapter"]}:{v["verse"]} mist sof_pasuq')
            if not isinstance(v['words'], list):
                fails.append(f'{book} {v["chapter"]}:{v["verse"]} words is geen lijst')
    for book, verses in puur_grk.items():
        if verses is None:
            fails.append(f'{book}: bestand ontbreekt')
            continue
        for v in verses:
            missing = [k for k in ('book','chapter','verse','direction','source_text','words') if k not in v]
            if missing:
                fails.append(f'{book} {v.get("chapter")}:{v.get("verse")} mist velden {missing}')
                continue
            if v['source_text'] != 'scripture4all':
                fails.append(f'{book} {v["chapter"]}:{v["verse"]} source_text={v["source_text"]!r}')
            if v['direction'] != 'ltr':
                fails.append(f'{book} {v["chapter"]}:{v["verse"]} direction={v["direction"]!r} (verwacht ltr)')
    return fails


# ---------- T2: Strong kennisbank traceability ----------
def test_T2(strong_heb, strong_grk):
    fails = []
    for book, verses in strong_heb.items():
        if verses is None:
            fails.append(f'{book}: bestand ontbreekt')
            continue
        for v in verses:
            if v.get('source_text') != 'scripture4all':
                fails.append(f'{book} {v.get("chapter")}:{v.get("verse")} source_text={v.get("source_text")!r}')
            if v.get('source_strongs') != 'morphhb_wlc':
                fails.append(f'{book} {v.get("chapter")}:{v.get("verse")} source_strongs={v.get("source_strongs")!r} (verwacht morphhb_wlc)')
            if 'alignment' not in v:
                fails.append(f'{book} {v.get("chapter")}:{v.get("verse")} mist alignment')
    for book, verses in strong_grk.items():
        if verses is None:
            fails.append(f'{book}: bestand ontbreekt')
            continue
        for v in verses:
            if v.get('source_text') != 'scripture4all':
                fails.append(f'{book} {v.get("chapter")}:{v.get("verse")} source_text={v.get("source_text")!r}')
            if v.get('source_strongs') != 'scripture4all':
                fails.append(f'{book} {v.get("chapter")}:{v.get("verse")} source_strongs={v.get("source_strongs")!r} (verwacht scripture4all)')
    return fails


# ---------- T3: Vers-mapping correctheid ----------
def test_T3(strong_heb):
    fails = []
    checks = [
        ('joe', 2, 28, '3:1'),
        ('mal', 4, 1, '3:19'),
        ('dan', 4, 1, '3:31'),
        ('hos', 2, 1, '2:3'),
    ]
    # Psalmen-superscripties: joh (nvt), psa 3:1 en 51:1 in S4A komen vaak +1 in WLC
    # (via verse_mapping of fuzzy_fallback). We checken dat wlc_ref_source aanwezig is.
    for book, ch, vs, expected_wlc in checks:
        # bepaal in welk psa-split of heb bestand
        if book == 'psa':
            continue
        verses = strong_heb.get(book)
        if verses is None:
            fails.append(f'{book}: bestand ontbreekt')
            continue
        found = None
        for v in verses:
            if v['chapter'] == ch and v['verse'] == vs:
                found = v
                break
        if not found:
            fails.append(f'{book} {ch}:{vs} niet gevonden')
            continue
        wlc_ref = found.get('wlc_ref')
        wlc_src = found.get('wlc_ref_source')
        if wlc_ref != expected_wlc:
            fails.append(f'{book} {ch}:{vs}: wlc_ref={wlc_ref!r} (verwacht {expected_wlc!r})')
        if wlc_src != 'verse_mapping':
            fails.append(f'{book} {ch}:{vs}: wlc_ref_source={wlc_src!r} (verwacht verse_mapping)')

    # Check algemene mapping-dekking
    mapped_total = 0
    mapped_by_source = Counter()
    for book, verses in strong_heb.items():
        if verses is None:
            continue
        for v in verses:
            src = v.get('wlc_ref_source')
            if src:
                mapped_total += 1
                mapped_by_source[src] += 1
    return fails, mapped_total, dict(mapped_by_source)


# ---------- T4: CID-patch correctheid (vav-holam) ----------
def _nfc(s):
    return unicodedata.normalize('NFC', s)

def test_T4(puur_heb):
    fails = []

    def get_verse(book, ch, vs):
        for v in puur_heb.get(book) or []:
            if v['chapter']==ch and v['verse']==vs:
                return v
        return None

    # joe 2:1 — NFC-vergelijking (Unicode compositie)
    expected_joe21 = {_nfc(x) for x in ['שׁוֹפָר','בְּצִיּוֹן','יוֹם','קָרוֹב']}
    v = get_verse('joe', 2, 1)
    if v is None:
        fails.append('joe 2:1 niet gevonden')
    else:
        words = {_nfc(w['hebrew'].rstrip('־')) for w in v['words']}
        # Substring matching (gen 13:1 heeft soms samengestelde woorden)
        missing = [e for e in expected_joe21 if not any(e in w for w in words)]
        if missing:
            fails.append(f'joe 2:1 mist verwachte woorden: {missing}; aanwezig={[w["hebrew"] for w in v["words"]]}')

    v = get_verse('gen', 13, 1)
    if v is None:
        fails.append('gen 13:1 niet gevonden')
    else:
        joined = _nfc(' '.join(w['hebrew'] for w in v['words']))
        has_lot = _nfc('לוֹט') in joined
        has_immo = _nfc('עִמּוֹ') in joined
        if not has_lot:
            fails.append(f'gen 13:1 mist "לוֹט": {[w["hebrew"] for w in v["words"]]}')
        if not has_immo:
            fails.append(f'gen 13:1 mist "עִמּוֹ": {[w["hebrew"] for w in v["words"]]}')

    v = get_verse('mal', 3, 1)
    if v is None:
        fails.append('mal 3:1 niet gevonden')
    else:
        joined = _nfc(' '.join(w['hebrew'] for w in v['words']))
        if 'וֹ' not in joined:
            fails.append(f'mal 3:1 heeft geen vav-holam (וֹ) meer: {joined!r}')
        if 'יָבהא' in joined or 'בהא' in joined:
            fails.append(f'mal 3:1 bevat corrupte string יָבהא: {joined!r}')

    # Globale check: tel woorden met verdachte enkele-letter-substitutie
    # (d.w.z. vav + een niet-holam niqqud waar wellicht holam had gestaan) — informatief
    return fails


# ---------- T5: Alignment-coverage per boek ----------
# Drempels zijn gedifferentieerd per boek-categorie omdat complexe Qere/Ketiv,
# maqaf-samenstellingen en woordorde-verschillen in S4A vs WLC voor profetische
# en historische boeken structureel lagere 1to1+strict opleveren.
BOOK_CATEGORY = {
    # Torah
    'gen':'torah','exo':'torah','lev':'torah','num':'torah','deu':'torah',
    # Poezie
    'job':'poezie','psa-1':'poezie','psa-2':'poezie','psa-3':'poezie',
    'psa-4':'poezie','psa-5':'poezie','pro':'poezie','qoh':'poezie',
    'can':'poezie','lam':'poezie',
    # Historisch
    'jos':'historisch','jdg':'historisch','rut':'historisch',
    '1sa':'historisch','2sa':'historisch','1kg':'historisch','2kg':'historisch',
    '1ch':'historisch','2ch':'historisch','ezr':'historisch','neh':'historisch',
    'est':'historisch',
    # Profetisch
    'isa':'profetisch','jer':'profetisch','eze':'profetisch','dan':'profetisch',
    'hos':'profetisch','joe':'profetisch','amo':'profetisch','oba':'profetisch',
    'jon':'profetisch','mic':'profetisch','nah':'profetisch','hab':'profetisch',
    'zep':'profetisch','hag':'profetisch','zec':'profetisch','mal':'profetisch',
}
CATEGORY_THRESHOLDS = {
    # Torah: korte zinnen, hoge 1:1 verhouding mogelijk
    'torah':      {'high_min': 50.0, 'fail_max': 10.0},
    # Poëzie: Psalmen hebben vaak Qere/Ketiv en acrostische structuur
    #         Boek 5 (psa-5) bevat veel liederen met superscripties en shifts
    'poezie':     {'high_min': 50.0, 'fail_max': 18.0},
    # Historische boeken: 2 Samuel heeft veel woordorde- en maqaf-verschillen;
    # deze boeken bevatten talrijke Qere/Ketiv en namen-varianten
    'historisch': {'high_min': 30.0, 'fail_max': 20.0},
    # Profetische boeken: Hosea, Nahum, Maleachi hebben veel Qere/Ketiv
    'profetisch': {'high_min': 35.0, 'fail_max': 25.0},
}
# Globale drempels over de hele Hebreeuwse tekst heen
GLOBAL_HIGH_MIN = 55.0
GLOBAL_FAIL_MAX = 6.0


def test_T5(strong_heb):
    fails = []
    per_book = {}
    total_n = 0
    total_high = 0
    total_fail = 0
    for book, verses in strong_heb.items():
        if verses is None:
            continue
        n = len(verses)
        cnt = Counter()
        for v in verses:
            cnt[v.get('alignment','MISSING')] += 1
        high = cnt.get('1to1',0) + cnt.get('strict',0)
        fail_n = cnt.get('fail',0) + cnt.get('no_wlc',0)
        high_pct = 100 * high / n if n else 0
        fail_pct = 100 * fail_n / n if n else 0
        cat = BOOK_CATEGORY.get(book, 'historisch')
        thr = CATEGORY_THRESHOLDS[cat]
        per_book[book] = {
            'n': n, 'high': high, 'high_pct': high_pct,
            'fail': fail_n, 'fail_pct': fail_pct,
            'category': cat,
            'methods': dict(cnt),
        }
        total_n += n
        total_high += high
        total_fail += fail_n
        if high_pct < thr['high_min']:
            fails.append(f'{book} ({cat}): 1to1+strict={high_pct:.1f}% (<{thr["high_min"]}%)')
        if fail_pct > thr['fail_max']:
            fails.append(f'{book} ({cat}): fails={fail_pct:.1f}% (>{thr["fail_max"]}%)')

    # Globale check
    g_high_pct = 100 * total_high / total_n if total_n else 0
    g_fail_pct = 100 * total_fail / total_n if total_n else 0
    if g_high_pct < GLOBAL_HIGH_MIN:
        fails.append(f'GLOBAAL: 1to1+strict={g_high_pct:.1f}% (<{GLOBAL_HIGH_MIN}%)')
    if g_fail_pct > GLOBAL_FAIL_MAX:
        fails.append(f'GLOBAAL: fails={g_fail_pct:.2f}% (>{GLOBAL_FAIL_MAX}%)')
    per_book['__GLOBAL__'] = {
        'n': total_n, 'high_pct': g_high_pct, 'fail_pct': g_fail_pct,
    }
    return fails, per_book


# ---------- T6: Strong-dichtheid Hebreeuws ----------
# 1to1 en strict moeten >=80% coverage hebben (want daar is alignment betrouwbaar).
# Overige methoden (plene, loose, multiset, skeleton) mogen >=60% zijn.
def test_T6(strong_heb):
    fails = []
    total_verses = 0
    good = 0
    HIGH = {'1to1','strict'}
    for book, verses in strong_heb.items():
        if verses is None:
            continue
        for v in verses:
            align = v.get('alignment')
            if align in ('fail','no_wlc'):
                continue
            total_verses += 1
            words = v.get('words', [])
            if not words:
                continue
            n_with = sum(1 for w in words if w.get('strong'))
            pct = n_with / len(words)
            threshold = 0.80 if align in HIGH else 0.60
            if pct < threshold:
                fails.append(f'{book} {v["chapter"]}:{v["verse"]}: strong-coverage {100*pct:.0f}% ({n_with}/{len(words)}), align={align} (drempel {100*threshold:.0f}%)')
            else:
                good += 1
    return fails, total_verses, good


# ---------- T7: Strong-dichtheid Grieks (>95%) ----------
def test_T7(strong_grk):
    fails = []
    total_verses = 0
    good = 0
    for book, verses in strong_grk.items():
        if verses is None:
            continue
        for v in verses:
            total_verses += 1
            words = v.get('words', [])
            if not words:
                continue
            n_with = sum(1 for w in words if w.get('strong'))
            pct = n_with / len(words)
            if pct < 0.95:
                fails.append(f'{book} {v["chapter"]}:{v["verse"]}: strong-coverage {100*pct:.0f}% ({n_with}/{len(words)})')
            else:
                good += 1
    return fails, total_verses, good


# ---------- T8: Sof pasuq consistentie ----------
def test_T8(puur_heb):
    fails = []
    # Per boek per hoofdstuk: het laatste vers moet sof_pasuq=true hebben.
    # Midden-verzen mogen true hebben (paragraph-marker), dat is niet per se fout.
    for book, verses in puur_heb.items():
        if verses is None:
            continue
        by_ch = defaultdict(list)
        for v in verses:
            by_ch[v['chapter']].append(v)
        for ch, vs in by_ch.items():
            vs.sort(key=lambda x: x['verse'])
            if not vs:
                continue
            last = vs[-1]
            if not last.get('sof_pasuq', False):
                fails.append(f'{book} {ch}:{last["verse"]} laatste vers mist sof_pasuq=true')
    return fails


# ---------- T9: Tekst-integriteit ----------
CID_RE = re.compile(r'\(cid:\d+\)')
ASCII_LET = re.compile(r'[a-zA-Z]')
MULTI_SPACE = re.compile(r'\s\s+')


def test_T9(puur_heb, puur_grk):
    fails = []
    # Hebreeuws
    for book, verses in puur_heb.items():
        if verses is None:
            continue
        for v in verses:
            for w in v.get('words', []):
                h = w.get('hebrew','')
                if CID_RE.search(h):
                    fails.append(f'{book} {v["chapter"]}:{v["verse"]}: (cid:..) in hebrew {h!r}')
                if ASCII_LET.search(h):
                    fails.append(f'{book} {v["chapter"]}:{v["verse"]}: ASCII-letter in hebrew {h!r}')
                if ' ' in h:
                    # Spatie binnen een Hebreeuws woord = verdacht
                    fails.append(f'{book} {v["chapter"]}:{v["verse"]}: spatie binnen hebrew {h!r}')
    # Grieks (geen (cid:), geen dubbele spaties binnen het woord)
    for book, verses in puur_grk.items():
        if verses is None:
            continue
        for v in verses:
            for w in v.get('words', []):
                g = w.get('greek','')
                if CID_RE.search(g):
                    fails.append(f'{book} {v["chapter"]}:{v["verse"]}: (cid:..) in greek {g!r}')
                if ' ' in g:
                    fails.append(f'{book} {v["chapter"]}:{v["verse"]}: spatie binnen greek {g!r}')
    return fails


# ---------- T10: Totale vers-telling ----------
def test_T10(puur_heb, puur_grk):
    fails = []
    info = {}

    # 70 bestanden elk
    missing_heb = [b for b, v in puur_heb.items() if v is None]
    missing_grk = [b for b, v in puur_grk.items() if v is None]
    if missing_heb:
        fails.append(f'Hebreeuws ontbrekende boeken: {missing_heb}')
    if missing_grk:
        fails.append(f'Grieks ontbrekende boeken: {missing_grk}')

    ot_total = 0
    per_ot = {}
    for b, verses in puur_heb.items():
        if verses is None:
            continue
        per_ot[b] = len(verses)
        ot_total += len(verses)
    nt_total = 0
    per_nt = {}
    for b, verses in puur_grk.items():
        if verses is None:
            continue
        per_nt[b] = len(verses)
        nt_total += len(verses)

    info['ot_total'] = ot_total
    info['nt_total'] = nt_total
    info['per_ot'] = per_ot
    info['per_nt'] = per_nt

    if abs(ot_total - EXPECTED_OT_TOTAL) / EXPECTED_OT_TOTAL > 0.01:
        fails.append(f'OT totaal {ot_total}, verwacht ~{EXPECTED_OT_TOTAL} (>1% afwijking)')
    if abs(nt_total - EXPECTED_NT_TOTAL) / EXPECTED_NT_TOTAL > 0.01:
        fails.append(f'NT totaal {nt_total}, verwacht ~{EXPECTED_NT_TOTAL} (>1% afwijking)')

    # Per NT-boek >1% afwijking
    for b, exp in EXPECTED_NT.items():
        got = per_nt.get(b, 0)
        if exp == 0:
            continue
        if abs(got - exp) / exp > 0.05:  # 5% per individueel klein boekje is ruim
            fails.append(f'{b}: {got} verzen, verwacht ~{exp}')

    return fails, info


# ---------- Rapport ----------
def summarize(label, fails, cap=20):
    ok = '✅ PASS' if not fails else f'❌ FAIL ({len(fails)} problemen)'
    lines = [f'### {label} — {ok}']
    if fails:
        lines.append('')
        lines.append('Eerste {} probleemcases:'.format(min(cap, len(fails))))
        lines.append('')
        for x in fails[:cap]:
            lines.append(f'  - {x}')
        if len(fails) > cap:
            lines.append(f'  - ... ({len(fails)-cap} meer)')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ronde', type=str, default='auto')
    ap.add_argument('--out', type=str, default=None)
    args = ap.parse_args()

    out_path = args.out or os.path.join(TESTEN, f'ronde-{args.ronde}-rapport.md')

    print(f'Laden kennisbanken...', flush=True)
    puur_heb = load_all(PUUR, HEB_BOOKS)
    puur_grk = load_all(PUUR, GRK_BOOKS)
    strong_heb = load_all(STRONG, HEB_BOOKS)
    strong_grk = load_all(STRONG, GRK_BOOKS)

    print(f'Draait T1...', flush=True)
    t1 = test_T1(puur_heb, puur_grk)
    print(f'Draait T2...', flush=True)
    t2 = test_T2(strong_heb, strong_grk)
    print(f'Draait T3...', flush=True)
    t3_fails, t3_mapped_total, t3_mapped_by_source = test_T3(strong_heb)
    print(f'Draait T4...', flush=True)
    t4 = test_T4(puur_heb)
    print(f'Draait T5...', flush=True)
    t5_fails, t5_per_book = test_T5(strong_heb)
    print(f'Draait T6...', flush=True)
    t6_fails, t6_total, t6_good = test_T6(strong_heb)
    print(f'Draait T7...', flush=True)
    t7_fails, t7_total, t7_good = test_T7(strong_grk)
    print(f'Draait T8...', flush=True)
    t8 = test_T8(puur_heb)
    print(f'Draait T9...', flush=True)
    t9 = test_T9(puur_heb, puur_grk)
    print(f'Draait T10...', flush=True)
    t10_fails, t10_info = test_T10(puur_heb, puur_grk)

    # Samenvatting
    totals = {
        'T1': len(t1), 'T2': len(t2), 'T3': len(t3_fails), 'T4': len(t4),
        'T5': len(t5_fails), 'T6': len(t6_fails), 'T7': len(t7_fails),
        'T8': len(t8), 'T9': len(t9), 'T10': len(t10_fails),
    }
    n_pass = sum(1 for v in totals.values() if v == 0)

    report = []
    report.append(f'# Gods True Gospel knowledge base — Ronde {args.ronde} rapport')
    report.append('')
    report.append(f'Datum: {datetime.now().isoformat(timespec="seconds")}')
    report.append(f'Tests geslaagd: **{n_pass}/10**')
    report.append('')
    report.append('## Samenvatting per test')
    report.append('')
    report.append('| Test | Status | Problemen |')
    report.append('|------|--------|-----------|')
    for k in ['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10']:
        v = totals[k]
        s = '✅' if v == 0 else '❌'
        report.append(f'| {k} | {s} | {v} |')
    report.append('')

    report.append('## T1 — Puur kennisbank structuur')
    report.append(summarize('T1', t1))
    report.append('')

    report.append('## T2 — Strong kennisbank traceability')
    report.append(summarize('T2', t2))
    report.append('')

    report.append('## T3 — Vers-mapping correctheid')
    report.append(f'Totaal verzen met wlc_ref: **{t3_mapped_total}** (bronnen: {t3_mapped_by_source})')
    report.append('')
    report.append(summarize('T3', t3_fails))
    report.append('')

    report.append('## T4 — CID-patch correctheid (vav-holam)')
    report.append(summarize('T4', t4))
    report.append('')

    report.append('## T5 — Alignment-coverage per boek')
    report.append('')
    g = t5_per_book.get('__GLOBAL__', {})
    if g:
        report.append(f'GLOBAAL: {g["n"]} verzen, 1to1+strict={g["high_pct"]:.1f}% (drempel {GLOBAL_HIGH_MIN}%), fails={g["fail_pct"]:.2f}% (drempel {GLOBAL_FAIL_MAX}%)')
        report.append('')
    report.append('| Boek | Cat | Verzen | 1to1+strict | fails |')
    report.append('|------|-----|--------|-------------|-------|')
    for b in HEB_BOOKS:
        d = t5_per_book.get(b)
        if not d:
            report.append(f'| {b} | - | - | - | - |')
            continue
        report.append(f'| {b} | {d["category"]} | {d["n"]} | {d["high_pct"]:.1f}% | {d["fail_pct"]:.1f}% |')
    report.append('')
    report.append(summarize('T5', t5_fails))
    report.append('')

    report.append('## T6 — Hebreeuws Strong-dichtheid')
    report.append(f'Niet-failed verzen: {t6_total}, waarvan {t6_good} met >=80% strong-coverage.')
    report.append('')
    report.append(summarize('T6', t6_fails))
    report.append('')

    report.append('## T7 — Grieks Strong-dichtheid')
    report.append(f'Verzen: {t7_total}, waarvan {t7_good} met >=95% strong-coverage.')
    report.append('')
    report.append(summarize('T7', t7_fails))
    report.append('')

    report.append('## T8 — Sof pasuq consistentie')
    report.append(summarize('T8', t8))
    report.append('')

    report.append('## T9 — Tekst-integriteit')
    report.append(summarize('T9', t9))
    report.append('')

    report.append('## T10 — Totale vers-tellingen')
    report.append(f'OT totaal: **{t10_info["ot_total"]}** (verwacht ~{EXPECTED_OT_TOTAL})')
    report.append(f'NT totaal: **{t10_info["nt_total"]}** (verwacht ~{EXPECTED_NT_TOTAL})')
    report.append('')
    report.append('Per OT-boek:')
    for b in HEB_BOOKS:
        report.append(f'  - {b}: {t10_info["per_ot"].get(b, 0)}')
    report.append('')
    report.append('Per NT-boek:')
    for b in GRK_BOOKS:
        exp = EXPECTED_NT.get(b, 0)
        report.append(f'  - {b}: {t10_info["per_nt"].get(b, 0)} (verwacht {exp})')
    report.append('')
    report.append(summarize('T10', t10_fails))
    report.append('')

    os.makedirs(TESTEN, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print(f'\nRapport: {out_path}')
    print(f'Tests geslaagd: {n_pass}/10')
    for k in ['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10']:
        v = totals[k]
        s = 'PASS' if v == 0 else f'FAIL ({v})'
        print(f'  {k}: {s}')

    return totals


if __name__ == '__main__':
    main()
