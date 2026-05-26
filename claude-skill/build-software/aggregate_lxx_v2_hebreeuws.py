"""aggregate_lxx_v2.py - LIFT-score variant"""
import json, time
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Kennis"
TMP_DIR = Path("/tmp/lxx_per_boek")
STRONG_DIR = ROOT / "strong"
MASTER_HEB = ROOT / "concordant-nl-hebreeuws.json"
MASTER_GR = ROOT / "concordant-nl-grieks.json"
OUT_PATH = ROOT / "lxx-mapping-hebreeuws.json"

BOOK_MAP = {'gen':'gen','exod':'exo','lev':'lev','num':'num','deut':'deu','josh':'jos','judg':'jdg','ruth':'rut','1sam':'1sa','2sam':'2sa','1kgs':'1kg','2kgs':'2kg','1chr':'1ch','2chr':'2ch','ezra':'ezr','neh':'neh','esth':'est','job':'job','ps':'psa','prov':'pro','eccl':'qoh','song':'can','isa':'isa','jer':'jer','lam':'lam','ezek':'eze','dan':'dan','hos':'hos','joel':'joe','amos':'amo','obad':'oba','jonah':'jon','mic':'mic','nah':'nah','hab':'hab','zeph':'zep','hag':'hag','zech':'zec','mal':'mal'}

def book_from_filename(fname):
    base = fname.replace('.jsonl', '')
    if '-' in base: base = base.split('-')[0]
    return base

def main():
    t0 = time.time()
    heb_by_book = defaultdict(list)
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
                        if part and part.startswith('H'): hcodes.add(part)
                heb_by_book[ourbook].append((v['chapter'], v['verse'], hcodes))
    for b in heb_by_book: heb_by_book[b].sort()

    pair_counts = defaultdict(Counter)
    h_total = Counter()
    g_total = Counter()
    matched = 0
    for abp_book, our_book in BOOK_MAP.items():
        p = TMP_DIR / f"{abp_book}.json"
        if not p.exists(): continue
        lxx_v = json.load(open(p))
        heb_l = heb_by_book.get(our_book, [])
        n = min(len(heb_l), len(lxx_v))
        for i in range(n):
            ch, v, hc = heb_l[i]
            gc = set(lxx_v[i])
            if not hc or not gc: continue
            matched += 1
            for h in hc:
                h_total[h] += 1
                for g in gc: pair_counts[h][g] += 1
            for g in gc: g_total[g] += 1

    total = matched
    print(f"Matched: {total}, H-codes: {len(pair_counts)}, G-codes: {len(g_total)}")

    mapping = {}
    for h, gc in pair_counts.items():
        h_count = h_total[h]
        if h_count < 2: continue
        scored = []
        for g, count in gc.items():
            if count < 2: continue
            co = count / h_count
            base = g_total[g] / total
            if base == 0: continue
            lift = co / base
            if lift < 2.0 or co < 0.10: continue
            scored.append({'g': g, 'count': count, 'co_score': round(co, 3), 'lift': round(lift, 2)})
        scored.sort(key=lambda x: -(x['lift'] * x['co_score']))
        if scored:
            mapping[h] = {'h_total': h_count, 'top_g': scored[:10]}
    print(f"Mapping H-codes: {len(mapping)}")

    master_h_codes = {e['strong'] for e in json.load(open(MASTER_HEB))['entries']}
    master_g_codes = {e['strong'] for e in json.load(open(MASTER_GR))['entries']}
    h_not = [h for h in mapping if h not in master_h_codes]
    g_set = set()
    for h, d in mapping.items():
        for g in d['top_g']: g_set.add(g['g'])
    g_not = [g for g in g_set if g not in master_g_codes]
    print(f"H niet in master: {len(h_not)}, G niet in master: {len(g_not)}")

    output = {
        'meta': {
            'titel': 'LXX-mapping Heb-naar-Grieks per Strong-code',
            'versie': '1.0',
            'datum': '2026-04-26',
            'bron_lxx': 'Apostolic Bible Polyglot (CrossWire Sword ABP)',
            'methodiek': 'vers-niveau co-occurrence MT-OT vs LXX-OT, met LIFT-score om grammaticale partikels te filteren',
            'filter': 'lift>=2.0 EN co_score>=10% EN min 2 voorkomens; top 10 per H, gesorteerd op lift*co_score',
            'velden': 'count=absoluut co-voorkomens; co_score=P(G|H); lift=P(G|H)/P(G)',
            'aantal_h_codes': len(mapping),
            'aantal_g_codes_uniek': len(g_set),
            'matched_verses': total,
            'h_niet_in_master': len(h_not),
            'g_niet_in_master': len(g_not),
        },
        'mapping': mapping,
    }
    with open(OUT_PATH, 'w', encoding='utf-8') as fp:
        json.dump(output, fp, ensure_ascii=False, indent=2)
    print(f"\nGeschreven {OUT_PATH.name}: {OUT_PATH.stat().st_size/1024:.1f} KB ({time.time()-t0:.1f}s)")

    samples = [('H7585','sheol'),('H5769','olam'),('H7307','ruach'),('H2617a','chesed'),('H1697','davar'),('H2398','chata'),('H6662','tsaddiq'),('H6918','qadosh'),('H430','elohim'),('H3068','YHWH'),('H1254a','bara')]
    print("\nSample resultaten:")
    for h, naam in samples:
        if h in mapping:
            t3 = mapping[h]['top_g'][:3]
            print(f"  {h} {naam}: {[(g['g'], g['count'], g['co_score'], g['lift']) for g in t3]}")
        else:
            print(f"  {h} {naam}: niet")

if __name__ == '__main__':
    main()
