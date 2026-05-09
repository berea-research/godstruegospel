"""
build_lxx_mapping_grieks.py
============================

Bouwt LXX-Grieks-naar-Hebreeuws mapping. Per Griekse Strong-code een top-N
lijst van Hebreeuwse OT-bron-codes die in de Septuaginta naar dat Griekse
woord vertaald zijn.

Gespiegeld van build_lxx_mapping_hebreeuws.py:
- Daar: pivot is H, output per H = top-G mappings.
- Hier: pivot is G, output per G = top-H mappings.

Methodiek: vers-niveau co-occurrence per OT-vers tussen Hebreeuwse feitenlaag
en LXX (Apostolic Bible Polyglot Strong-tagged). Telling per (H, G) paar,
daarna gepivoteerd op G-as.

Gebruik:
    python3 build_lxx_mapping_grieks.py
    python3 build_lxx_mapping_grieks.py --bron /pad/naar/ABP-extracted

Als de bron niet bij --bron staat en niet onder Kennis/lxx-bron/, gebruikt
het script een fallback-pad naar het bron-archief.
"""
import json
import re
import sys
import time
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Kennis"
STRONG_DIR = ROOT / "strong"
MASTER_HEB = ROOT / "concordant-nl-hebreeuws.json"
MASTER_GR = ROOT / "concordant-nl-grieks.json"
OUT_PATH = ROOT / "lxx-mapping-grieks.json"

DEFAULT_BRON = ROOT / "lxx-bron" / "ABP-extracted"
FALLBACK_BRON = (ROOT.parent.parent / "concordant-agent" / "oud" /
                  "lxx-bron-archief" / "STEPBible-Data-bron" / "ABP-extracted")

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
    if '-' in base:
        base = base.split('-')[0]
    return base


def normalize_g(g):
    """Normaliseer G-code: ABP G01722 -> G1722; G1510.7.3 -> G1510."""
    g_clean = g.split('.')[0]
    return 'G' + str(int(g_clean))


def main():
    t_start = time.time()
    args = sys.argv[1:]
    bron = None
    if '--bron' in args:
        i = args.index('--bron')
        bron = Path(args[i+1])
    elif DEFAULT_BRON.exists():
        bron = DEFAULT_BRON
    elif FALLBACK_BRON.exists():
        bron = FALLBACK_BRON
        print(f"NB: bron niet onder Kennis/, fallback naar archief: {bron}")

    if not bron or not bron.exists():
        print(f"FOUT: ABP-bron niet gevonden. Probeer --bron <pad>.")
        sys.exit(1)

    from pysword.modules import SwordModules
    print(f"Stap 1: ABP-module laden uit {bron}")
    modules = SwordModules(str(bron))
    modules.parse_modules()
    abp = modules.get_bible_from_module('ABP')

    print("Stap 2: Hebreeuwse feitenlaag laden per boek...")
    heb_verses_by_book = defaultdict(list)
    for f in sorted(STRONG_DIR.iterdir()):
        if f.suffix != '.jsonl':
            continue
        ourbook = book_from_filename(f.name)
        if ourbook not in BOOK_MAP.values():
            continue
        with open(f) as fp:
            for line in fp:
                v = json.loads(line)
                hcodes = set()
                for w in v.get('words', []):
                    s = w.get('strong', '')
                    if s.startswith('H'):
                        hcodes.add(s)
                heb_verses_by_book[ourbook].append((v['chapter'], v['verse'], hcodes))
    for b in heb_verses_by_book:
        heb_verses_by_book[b].sort()
    total_heb = sum(len(vs) for vs in heb_verses_by_book.values())
    print(f"   Hebreeuwse boeken: {len(heb_verses_by_book)}, totaal verzen: {total_heb}")

    print("\nStap 3: Per boek LXX-sweep + co-occurrence telling...")
    pair_counts = defaultdict(Counter)  # G -> Counter(H -> count)
    g_total = Counter()
    h_total = Counter()
    matched_verses = 0
    skipped = 0

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
            for g in gcodes:
                g_total[g] += 1
                for h in hcodes:
                    pair_counts[g][h] += 1
            for h in hcodes:
                h_total[h] += 1
        dt = round(time.time() - t0, 1)
        print(f"   {abp_book}/{our_book}: matched={n} ({dt}s)")

    print(f"\nSweep totaal: {matched_verses} verzen matched, {skipped} geskipt")
    print(f"Unieke G-codes met data: {len(pair_counts)}")
    print(f"Unieke H-codes voorgekomen: {len(h_total)}")

    print("\nStap 4: Filter en construeer G->H mapping...")
    mapping = {}
    for g_code, h_counter in pair_counts.items():
        g_count = g_total[g_code]
        if g_count < 2:
            continue
        scored = []
        for h_code, count in h_counter.most_common(20):
            score = count / g_count
            if score < 0.05:
                continue
            if count < 2:
                continue
            # lift = relatieve frequentie boven baseline
            h_count_total = h_total.get(h_code, 0)
            if matched_verses > 0 and h_count_total > 0:
                expected = (h_count_total / matched_verses) * g_count
                lift = count / expected if expected > 0 else 0
            else:
                lift = 0
            scored.append({
                'h': h_code,
                'count': count,
                'co_score': round(score, 3),
                'lift': round(lift, 2),
            })
        if scored:
            mapping[g_code] = {
                'g_total': g_count,
                'top_h': scored[:10],
            }
    print(f"Mapping bevat {len(mapping)} Griekse Strong-codes met H-bronnen.")

    print("\nStap 5: Validatie tegen masters...")
    master_g = json.load(open(MASTER_GR))
    master_g_codes = {e['strong'] for e in master_g['entries']}
    master_h = json.load(open(MASTER_HEB))
    master_h_codes = {e['strong'] for e in master_h['entries']}

    g_in_mapping_not_master = [g for g in mapping if g not in master_g_codes]
    h_codes_in_mapping = set()
    for g, data in mapping.items():
        for h in data['top_h']:
            h_codes_in_mapping.add(h['h'])
    h_in_mapping_not_master = [h for h in h_codes_in_mapping if h not in master_h_codes]
    print(f"  G niet in master: {len(g_in_mapping_not_master)}")
    print(f"  H niet in master: {len(h_in_mapping_not_master)}")

    print("\nStap 6: Output schrijven...")
    output = {
        'meta': {
            'titel': 'LXX-mapping Grieks-naar-Hebreeuws per Strong-code',
            'versie': '1.0',
            'datum': '2026-04-28',
            'methodiek': ('Vers-niveau co-occurrence: per OT-vers H-codes uit '
                          'tekstlaag + G-codes uit LXX-bron, met G als pivot. '
                          'Levert per G-Strong-code de top-10 H-Strong-bronnen '
                          'die in de Griekse vertaling naar dat woord werden vertaald.'),
            'filter': ('minimum 5% relatieve frequentie EN minimum 2 absolute '
                       'voorkomens; top 10 H-bronnen per G'),
            'aantal_g_codes': len(mapping),
            'aantal_h_codes_uniek': len(h_codes_in_mapping),
            'matched_verses': matched_verses,
        },
        'mapping': mapping,
    }
    with open(OUT_PATH, 'w', encoding='utf-8') as fp:
        json.dump(output, fp, ensure_ascii=False, indent=2)
    print(f"  -> {OUT_PATH.name} ({OUT_PATH.stat().st_size/1024:.1f} KB)")
    print(f"\nTotale duur: {time.time() - t_start:.1f}s")

    print("\nStap 7: Sample-resultaten kerntheologische G-woorden...")
    samples = ['G3056', 'G2316', 'G2962', 'G4151', 'G2424', 'G3962', 'G40']
    for g in samples:
        if g in mapping:
            top3 = mapping[g]['top_h'][:3]
            print(f"  {g}: top-3 = {[(h['h'], h['count'], h['co_score'], h['lift']) for h in top3]}")
        else:
            print(f"  {g}: niet in mapping")


if __name__ == '__main__':
    main()
