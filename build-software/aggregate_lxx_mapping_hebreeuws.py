"""
aggregate_lxx_mapping.py (versie 2)
====================================

Aggregeert per-boek LXX-extracts tegen Hebreeuwse feitenlaag.
Gebruikt LIFT-score om grammaticale stop-words (lidwoord, voegwoord) te filteren.

Lift = (count_HG / count_H) / (count_G / total_verses)
Hoge lift = G is opvallend geassocieerd met H boven baseline.
"""

import json, time
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Kennis"
TMP_DIR = Path("/tmp/lxx_per_boek")
STRONG_DIR = ROOT / "strong"
MASTER_HEB = ROOT / "concordant-nl-hebreeuws.json"
MASTER_GR = ROOT / "concordant-nl-grieks.json"
OUT_PATH = ROOT / "lxx-mapping-hebreeuws.json"

BOOK_MAP = {
    'gen':'gen','exod':'exo','lev':'lev','num':'num','deut':'deu',
    'josh':'jos','judg':'jdg','ruth':'rut',
    '1sam':'1sa','2sam':'2sa','1kgs':'1kg','2kgs':'2kg',
    '1chr':'1ch','2chr':'2ch','ezra':'ezr','neh':'neh','esth':'est',
    'job':'job','ps':'psa','prov':'pro','eccl':'qoh','song':'can',
    'isa':'isa','jer':'jer','lam':'lam','ezek':'eze','dan':'dan',
    'hos':'hos','joel':'joe','amos':'amo','obad':'oba','jonah':'jon',
    'mic':'mic','nah':'nah','hab':'hab','zeph':'zep','hag':'hag',
    'zech':'zec','mal':'mal',
}


def book_from_filename(fname):
    base = fname.replace('.jsonl', '')
    if '-' in base: base = base.split('-')[0]
    return base


def main():
    t0 = time.time()
    print("Hebreeuwse feitenlaag laden per boek...")
    heb_verses_by_book = defaultdict(list)
    for f in sorted(STRONG_DIR.iterdir()):
        if f.suffix != '.jsonl': continue
        ourbook = book_from_filename(f.name)
        if ourbook not in BOOK_MAP.values(): continue
        with open(f) as fp:
            for line in fp:
                v = json.loads(line)
                hcodes = set()
                for tag in v.get('verse_strongs', []):
                    for part in tag.split('/'):
                        if part and part.startswith('H'):
                            hcodes.add(part)
                heb_verses_by_book[ourbook].append((v['chapter'], v['verse'], hcodes))
    for b in heb_verses_by_book:
        heb_verses_by_book[b].sort()

    print("LXX per-boek extracts aggregeren...")
    pair_counts = defaultdict(Counter)
    h_total = Counter()
    g_total = Counter()
    matched_verses = 0

    for abp_book, our_book in BOOK_MAP.items():
        tmp_path = TMP_DIR / f"{abp_book}.json"
        if not tmp_path.exists(): continue
        lxx_per_verse = json.load(open(tmp_path))
        heb_list = heb_verses_by_book.get(our_book, [])
        n = min(len(heb_list), len(lxx_per_verse))
        for i in range(n):
            ch, v, hcodes = heb_list[i]
            gcodes = set(lxx_per_verse[i])
            if not hcodes or not gcodes: continue
            matched_verses += 1
            for h in hcodes:
                h_total[h] += 1
                for g in gcodes:
                    pair_counts[h][g] += 1
            for g in gcodes:
                g_total[g] += 1

    total_v = matched_verses
    print(f"Matched verzen: {total_v}")
    print(f"H-codes: {len(pair_counts)}, G-codes: {len(g_total)}")

    print("Filter via LIFT-score (g_score = co_score / g_baseline)...")
    mapping = {}
    for h_code, g_counter in pair_counts.items():
        h_count = h_total[h_code]
        if h_count < 2: continue
        scored = []
        for g_code, count in g_counter.items():
            if count < 2: continue
            co_score = count / h_count           # P(G | H)
            g_baseline = g_total[g_code] / total_v   # P(G)
            if g_baseline == 0: continue
            lift = co_score / g_baseline
            # Drempel: lift > 2 betekent G is 2x meer geassocieerd met deze H dan baseline
            # En co_score >= 10% (komt in minstens 10% van H-verzen voor)
            if lift < 2.0: continue
            if co_score < 0.10: continue
            scored.append({
                'g': g_code,
                'count': count,
                'co_score': round(co_score, 3),
                'lift': round(lift, 2),
            })
        # Sorteer op lift x co_score (gewogen)
        scored.sort(key=lambda x: -(x['lift'] * x['co_score']))
        if scored:
            mapping[h_code] = {
                'h_total': h_count,
                'top_g': scored[:10],
            }
    print(f"Mapping: {len(mapping)} H-codes")

    print("Validatie tegen masters...")
    master_h = json.load(open(MASTER_HEB))
    master_h_codes = {e['strong'] for e in master_h['entries']}
    master_g = json.load(open(MASTER_GR))
    master_g_codes = {e['strong'] for e in master_g['entries']}
    h_not_master = [h for h in mapping if h not in master_h_codes]
    g_codes_in_mapping = set()
    for h, data in mapping.items():
        for g in data['top_g']:
            g_codes_in_mapping.add(g['g'])
    g_not_master = [g for g in g_codes_in_mapping if g not in master_g_codes]
    print(f"  H niet in master: {len(h_not_master)}")
    print(f"  G niet in master: {len(g_not_master)} (voorbeelden: {g_not_master[:5]})")

    output = {
        'meta': {
            'titel': 'LXX-mapping Heb-naar-Grieks per Strong-code',
            'versie': '1.0',
            'datum': '2026-04-26',
            'bron_lxx': 'Apostolic Bible Polyglot (CrossWire Sword module ABP)',
            'methodiek': 'vers-niveau co-occurrence + LIFT-score om grammaticale stopwoorden te filteren',
            'filter': 'lift >= 2.0 EN co_score >= 10% EN minimaal 2 absolute voorkomens; top 10 G-equivalenten per H',
            'velden': 'count = absolute co-voorkomens; co_score = P(G|H); lift = P(G|H) / P(G); ranking = lift x co_score',
            'aantal_h_codes': len(mapping),
            'aantal_g_codes_uniek': len(g_codes_in_mapping),
            'matched_verses': total_v,
            'h_niet_in_master': len(h_not_master),
            'g_niet_in_master': len(g_not_master),
        },
        'mapping': mapping,
    }
    with open(OUT_PATH, 'w', encoding='utf-8') as fp:
        json.dump(output, fp, ensure_ascii=False, indent=2)
    print(f"\nGeschreven: {OUT_PATH.name} ({OUT_PATH.stat().st_size / 1024:.1f} KB)")
    print(f"Duur: {time.time() - t0:.1f}s")

    print("\nSample kerntheologische woorden (top 3 per H):")
    samples = [
        ('H7585', 'sheol'), ('H5769', 'olam'), ('H7307', 'ruach'),
        ('H2617a', 'chesed'), ('H1697', 'davar'), ('H2398', 'chata'),
        ('H6662', 'tsaddiq'), ('H6918', 'qadosh'),
        ('H430', 'elohim'), ('H3068', 'YHWH'),
        ('H1254a', 'bara'), ('H2403a', 'chattat'),
    ]
    for h, naam in samples:
        if h in mapping:
            top3 = mapping[h]['top_g'][:3]
            print(f"  {h} {naam}: {[(g['g'], g['count'], g['co_score'], g['lift']) for g in top3]}")
        else:
            print(f"  {h} {naam}: niet in mapping")


if __name__ == '__main__':
    main()
