"""gen_kernwoorden_v3.py - fix voorkomens_ca/voorkomens veldnaam-verschil."""
import json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Kennis"
DOCS = Path("./docs")
MASTER_HEB = ROOT / "concordant-nl-hebreeuws.json"
MASTER_GR = ROOT / "concordant-nl-grieks.json"
INDEX_HEB = ROOT / "index" / "strong-vers-hebreeuws.json"
INDEX_GR = ROOT / "index" / "strong-vers-grieks.json"

HEB_GENRES = {
    'Tora': {'gen','exo','lev','num','deu'},
    'Vroege_Profeten': {'jos','jdg','1sa','2sa','1kg','2kg'},
    'Late_Profeten': {'isa','jer','eze','hos','joe','amo','oba','jon','mic','nah','hab','zep','hag','zec','mal'},
    'Geschriften': {'psa','pro','job','can','rut','lam','qoh','est','dan','ezr','neh','1ch','2ch'},
}
GR_GENRES = {
    'Evangelien': {'mat','mar','luk','joh'},
    'Handelingen': {'act'},
    'Paulinische': {'rom','1co','2co','gal','eph','phi','col','1th','2th','1ti','2ti','tit','phm'},
    'Algemene': {'heb','jam','1pe','2pe','1jo','2jo','3jo','jud'},
    'Openbaring': {'rev'},
}

HEB_KEEP = {'zn','ww','bn','bw','eign','tw'}
GR_KEEP = {'zn','ww','bn','bw','eigennaam','tw','tussenwerpsel'}


def get_voork(entry):
    """Probeer voorkomens dan voorkomens_ca."""
    v = entry.get('voorkomens')
    if v is None: v = entry.get('voorkomens_ca', 0)
    if isinstance(v, str):
        try: v = int(v)
        except: v = 0
    return v or 0


def get_base(s):
    m = re.match(r'^([HG])(\d+)([a-f]?)\+?$', s)
    if m: return m.group(1) + m.group(2)
    return s


def book_set(s, idx):
    if s not in idx: return set()
    return {l['b'] for l in idx[s]}


def selecteer(master_path, idx_path, drempel, keep_set, genres, taal):
    print(f"\n=== {taal.upper()} ===")
    m = json.load(open(master_path))
    entries = m['entries']
    idx = json.load(open(idx_path))

    cluster = defaultdict(int)
    for e in entries:
        cluster[get_base(e['strong'])] += 1

    cands = []
    n_freq = 0
    for e in entries:
        ws = (e.get('woordsoort') or '').lower().strip()
        ws_first = ws.split('-')[0].split(' ')[0].split('/')[0]
        if ws_first not in keep_set: continue
        v = get_voork(e)
        if v <= drempel: continue
        n_freq += 1
        books = book_set(e['strong'], idx)
        bestreken = sum(1 for g, bs in genres.items() if books & bs)
        totaal = len(genres)
        crit_g = bestreken == totaal
        clust_size = cluster[get_base(e['strong'])]
        crit_c = clust_size > 3
        if crit_g or crit_c:
            cands.append({
                'strong': e['strong'],
                'woord': e.get('hebreeuws') or e.get('grieks',''),
                'translit': e.get('translit',''),
                'nl': e.get('nl_concordant',''),
                'woordsoort': ws,
                'voorkomens': v,
                'genre_bestreken': bestreken,
                'genre_totaal': totaal,
                'cluster_grootte': clust_size,
                'crit_g': crit_g,
                'crit_c': crit_c,
            })
    print(f"Inhoudswoorden + freq>{drempel}: {n_freq}")
    print(f"  Eindlijst: {len(cands)} ({sum(1 for c in cands if c['crit_g'])} via genre, {sum(1 for c in cands if c['crit_c'])} via cluster)")
    cands.sort(key=lambda c: -c['voorkomens'])
    return cands


def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    heb = selecteer(MASTER_HEB, INDEX_HEB, 25, HEB_KEEP, HEB_GENRES, 'hebreeuws')
    gr = selecteer(MASTER_GR, INDEX_GR, 10, GR_KEEP, GR_GENRES, 'grieks')

    out_md = DOCS / 'kernwoordenlijst-v1.0.md'
    with open(out_md, 'w', encoding='utf-8') as fp:
        fp.write("# Kernwoordenlijst v1.0 voor diepte-notities\n\n")
        fp.write("Datum 2026-04-26. Bron B5-impl-3 stap 1, drie criteria architectuur-v2.0 sectie 9.4.\n\n")
        fp.write("Frequentie verplicht (Heb >25, Grieks >10) plus minstens een van: genre-breedte (alle genres) of cluster-kop (>3 sub-codes).\n")
        fp.write("Inhoudswoorden alleen (zn, ww, bn, bw, eigennaam, tussenwerpsel). Grammaticaal uitgesloten.\n\n")
        fp.write(f"Hebreeuws: {len(heb)} kernwoorden\n\n")
        fp.write(f"Grieks: {len(gr)} kernwoorden\n\n")
        fp.write(f"Totaal {len(heb)+len(gr)} diepte-notities te creeren in B5-impl-3 stap 2.\n\n")
        for naam, lst in [('Hebreeuws', heb), ('Grieks', gr)]:
            fp.write(f"\n## {naam} ({len(lst)})\n\n")
            fp.write("| # | Strong | NL | Woord | Translit | Voork | Genre | Cluster | Crit |\n|---|---|---|---|---|---|---|---|---|\n")
            for i, k in enumerate(lst, 1):
                crit = ('G' if k['crit_g'] else '') + ('C' if k['crit_c'] else '')
                fp.write(f"| {i} | {k['strong']} | {k['nl']} | {k['woord']} | {k['translit']} | {k['voorkomens']} | {k['genre_bestreken']}/{k['genre_totaal']} | {k['cluster_grootte']} | {crit} |\n")

    out_json = DOCS / 'kernwoordenlijst-v1.0.json'
    with open(out_json, 'w', encoding='utf-8') as fp:
        json.dump({
            'meta': {'versie':'1.0','datum':'2026-04-26',
                'aantal_hebreeuws': len(heb), 'aantal_grieks': len(gr),
                'criteria': 'freq>25Heb of >10Gr verplicht; plus minstens genre-breedte of cluster-kop'},
            'hebreeuws': heb, 'grieks': gr,
        }, fp, ensure_ascii=False, indent=2)
    print(f"\n{out_md.name}: {out_md.stat().st_size/1024:.1f} KB")
    print(f"{out_json.name}: {out_json.stat().st_size/1024:.1f} KB")


if __name__ == '__main__':
    main()
