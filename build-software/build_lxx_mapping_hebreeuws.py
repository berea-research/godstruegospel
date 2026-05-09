"""
build_lxx_mapping.py
====================

Bouwt LXX-Heb-Grieks mapping uit Apostolic Bible Polyglot Strong-tagged LXX
plus onze Hebreeuwse feitenlaag.

Methodiek: per OT-boek, vers-voor-vers via get_iter, verzamel H-codes uit
feitenlaag (verse_strongs) en G-codes uit ABP. Index-match per boek.
Co-occurrence-tellingen per (H, G) paar.

B5-impl-2, datum 2026-04-26.
"""

import json
import re
import time
from collections import defaultdict, Counter
from pathlib import Path
from pysword.modules import SwordModules

ROOT = Path(__file__).resolve().parent.parent / "Kennis"
ABP_DIR = ROOT / "lxx-bron" / "ABP-extracted"
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


def normalize_g(g):
    """ABP G01722 -> G1722; G1510.7.3 -> G1510 (sub-form negeren)."""
    g_clean = g.split('.')[0]
    return 'G' + str(int(g_clean))


def main():
    t_start = time.time()
    print("Stap 1: ABP module laden...")
    modules = SwordModules(str(ABP_DIR))
    modules.parse_modules()
    abp = modules.get_bible_from_module('ABP')

    print("Stap 2: Hebreeuwse feitenlaag laden per boek...")
    heb_verses_by_book = defaultdict(list)  # boek -> lijst van (ch, v, set_h_codes), gesorteerd
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
    # Sorteer per boek
    for b in heb_verses_by_book:
        heb_verses_by_book[b].sort()
    print(f"   Hebreeuwse boeken: {len(heb_verses_by_book)}")
    total_heb_verses = sum(len(vs) for vs in heb_verses_by_book.values())
    print(f"   Totaal Hebreeuwse verzen: {total_heb_verses}")

    print("\nStap 3: Per boek LXX-sweep + co-occurrence telling...")
    pair_counts = defaultdict(Counter)
    h_total = Counter()
    g_total = Counter()
    matched_verses = 0
    skipped = 0
    book_stats = {}

    for abp_book, our_book in BOOK_MAP.items():
        t0 = time.time()
        heb_list = heb_verses_by_book.get(our_book, [])
        if not heb_list:
            continue
        try:
            lxx_verses = list(abp.get_iter(books=[abp_book], clean=False))
        except Exception as e:
            print(f"   FOUT {abp_book}: {e}")
            continue
        # Match per index
        n = min(len(heb_list), len(lxx_verses))
        for i in range(n):
            ch, v, hcodes = heb_list[i]
            lxx_text = lxx_verses[i]
            gcodes_raw = re.findall(r'strong:G(\d+(?:\.\d+)*)', lxx_text)
            gcodes = set()
            for g in gcodes_raw:
                try:
                    gcodes.add(normalize_g(g))
                except (ValueError, IndexError):
                    continue
            if not hcodes or not gcodes:
                skipped += 1
                continue
            matched_verses += 1
            for h in hcodes:
                h_total[h] += 1
                for g in gcodes:
                    pair_counts[h][g] += 1
            for g in gcodes:
                g_total[g] += 1

        book_stats[abp_book] = {
            'heb_verses': len(heb_list),
            'lxx_verses': len(lxx_verses),
            'matched': n,
            'time_s': round(time.time() - t0, 1),
        }
        print(f"   {abp_book}/{our_book}: heb={len(heb_list)} lxx={len(lxx_verses)} matched={n} ({book_stats[abp_book]['time_s']}s)")

    print(f"\nSweep totaal: {matched_verses} verzen matched, {skipped} geskipt")
    print(f"Unieke H-codes met data: {len(pair_counts)}")
    print(f"Unieke G-codes voorgekomen: {len(g_total)}")

    print("\nStap 4: Filter en construeer mapping...")
    mapping = {}
    for h_code, g_counter in pair_counts.items():
        h_count = h_total[h_code]
        if h_count < 2: continue
        scored = []
        for g_code, count in g_counter.most_common(20):
            score = count / h_count
            if score < 0.05: continue
            if count < 2: continue
            scored.append({'g': g_code, 'count': count, 'score': round(score, 3)})
        if scored:
            mapping[h_code] = {
                'h_total': h_count,
                'top_g': scored[:10],
            }
    print(f"Mapping bevat {len(mapping)} Hebreeuwse Strong-codes met G-equivalenten.")

    print("\nStap 5: Validatie tegen masters...")
    master_h = json.load(open(MASTER_HEB))
    master_h_codes = {e['strong'] for e in master_h['entries']}
    master_g = json.load(open(MASTER_GR))
    master_g_codes = {e['strong'] for e in master_g['entries']}

    h_in_mapping_not_master = [h for h in mapping if h not in master_h_codes]
    g_codes_in_mapping = set()
    for h, data in mapping.items():
        for g in data['top_g']:
            g_codes_in_mapping.add(g['g'])
    g_in_mapping_not_master = [g for g in g_codes_in_mapping if g not in master_g_codes]
    print(f"  H niet in master: {len(h_in_mapping_not_master)}")
    print(f"  G niet in master: {len(g_in_mapping_not_master)}")

    print("\nStap 6: Output schrijven...")
    output = {
        'meta': {
            'titel': 'LXX-mapping Heb-naar-Grieks per Strong-code',
            'versie': '1.0',
            'datum': '2026-04-26',
            'bron_lxx': 'Apostolic Bible Polyglot (CrossWire Sword module ABP)',
            'methodiek': 'vers-niveau co-occurrence: per OT-vers H-codes uit MorphHB-WLC + G-codes uit ABP-LXX, dan correlatie',
            'filter': 'minimum 5% relatieve frequentie EN minimum 2 absolute voorkomens; top 10 G-equivalenten per H',
            'aantal_h_codes': len(mapping),
            'aantal_g_codes_uniek': len(g_codes_in_mapping),
            'matched_verses': matched_verses,
            'h_in_mapping_niet_in_master': len(h_in_mapping_not_master),
            'g_in_mapping_niet_in_master': len(g_in_mapping_not_master),
            'opmerking': 'Vers-niveau co-occurrence is statistisch; voor cross-testament theologische kernwoorden zeer betrouwbaar (hoge frequentie + sterke signaal-ruis verhouding), voor zeldzame woorden minder.',
        },
        'mapping': mapping,
    }

    with open(OUT_PATH, 'w', encoding='utf-8') as fp:
        json.dump(output, fp, ensure_ascii=False, indent=2)
    print(f"  -> {OUT_PATH.name}")
    print(f"  Bestandsgrootte: {OUT_PATH.stat().st_size / 1024:.1f} KB")
    print(f"\nTotale duur: {time.time() - t_start:.1f}s")

    print("\nStap 7: Sample-resultaten kerntheologische woorden...")
    samples = ['H7585', 'H5769', 'H7307', 'H2617a', 'H1697', 'H2398', 'H6662', 'H6918', 'H430', 'H3068']
    for h in samples:
        if h in mapping:
            top3 = mapping[h]['top_g'][:3]
            print(f"  {h}: top-3 = {[(g['g'], g['count'], g['score']) for g in top3]}")
        else:
            print(f"  {h}: niet in mapping")


if __name__ == '__main__':
    main()
