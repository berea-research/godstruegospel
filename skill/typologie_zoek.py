"""
typologie_zoek.py — godstruegospel skill v5.1, typologie-helper
================================================================

Zoekt patronen in de Hebreeuwse en Griekse grondtekst voor opbouw van de
typologie-laag. Gebruik:

    python3 typologie_zoek.py --cijfer 120
    python3 typologie_zoek.py --strong H120                       # alle voorkomens van Strong-code
    python3 typologie_zoek.py --strongs H3967,H6242 --nabijheid   # combinatie nabij elkaar
    python3 typologie_zoek.py --wortel "db" --hebr                # alle Hebreeuwse Strongs met wortel
    python3 typologie_zoek.py --dag 3                             # alle 'derde dag' voorkomens

Geen geheugen-input. Alle output uit GTG/Kennis/strong/ en /puur/.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KENNIS = os.path.join(ROOT, "Kennis")
STRONG_DIR = os.path.join(KENNIS, "strong")

# Hebreeuwse cijfer-Strongs (decoderingstabel uit chronologie.md)
HEBR_CIJFERS = {
    'H259': 1, 'H8147': 2, 'H7969': 3, 'H702': 4, 'H2568': 5,
    'H8337': 6, 'H7651': 7, 'H8083': 8, 'H8672': 9, 'H6235': 10,
    'H6240': '+10', 'H6242': 20, 'H7970': 30, 'H705': 40, 'H2572': 50,
    'H8346': 60, 'H7657': 70, 'H8084': 80, 'H8673': 90, 'H3967': 100,
    'H505': 1000,
}

# Aramese cijfer-Strongs (Daniël, Ezra)
ARAM_CIJFERS = {
    'H2298': 1, 'H8648': 2, 'H8532': 3, 'H703': 4, 'H2582': 5,
    'H8353': 6, 'H7655': 7, 'H8540': 8, 'H8648a': 9, 'H6236': 10,
    'H6243': 20, 'H8540a': 80, 'H3969': 100, 'H506': 1000,
}

# Griekse cijfer-Strongs
GR_CIJFERS = {
    'G1520': 1, 'G1417': 2, 'G5140': 3, 'G5064': 4, 'G4002': 5,
    'G1803': 6, 'G2033': 7, 'G3638': 8, 'G1767': 9, 'G1176': 10,
    'G1733': 11, 'G1427': 12, 'G1180': 13, 'G1180a': 14, 'G1178': 15,
    'G1501': 20, 'G5144': 30, 'G5062': 40, 'G4004': 50, 'G1835': 60,
    'G1440': 70, 'G3589': 80, 'G1768': 90, 'G1540': 100, 'G1250': 200,
    'G5145': 300, 'G5071': 400, 'G4001': 500, 'G1812': 600, 'G2035': 700,
    'G3637': 800, 'G1773': 900, 'G5507': 1000,
}

ALLE_CIJFERS = {**HEBR_CIJFERS, **ARAM_CIJFERS, **GR_CIJFERS}

# Bekende cijfer-combinaties (Hebreeuws)
def cijfer_naar_strong_combinatie(cijfer, taal='hebr'):
    """Returnt mogelijke Strong-combinaties voor een cijfer.
    taal: 'hebr', 'aram', of 'grieks'."""
    cijfer = int(cijfer)
    combinaties = []

    if taal == 'hebr':
        cijferdict = HEBR_CIJFERS
        honderd_strong = 'H3967'
    elif taal == 'aram':
        cijferdict = ARAM_CIJFERS
        honderd_strong = 'H3969'
    elif taal == 'grieks':
        cijferdict = GR_CIJFERS
        honderd_strong = 'G1540'
    else:
        return []

    # Direct match (single-Strong cijfers)
    for strong, val in cijferdict.items():
        if isinstance(val, int) and val == cijfer:
            combinaties.append([strong])

    # 100-en + tientallen + eenheden
    if 100 <= cijfer < 1000:
        rest = cijfer
        if rest >= 200:
            honderden = rest // 100
            kandidaten = [k for k, v in cijferdict.items() if v == honderden]
            if kandidaten:
                strong_voor_honderdtal = kandidaten[0]
                rest_na_honderden = rest % 100
                tienscombs = decompose_under_hundred(rest_na_honderden, cijferdict)
                for tc in tienscombs:
                    combinaties.append([strong_voor_honderdtal, honderd_strong] + tc)
        else:
            rest_onder = rest - 100
            tienscombs = decompose_under_hundred(rest_onder, cijferdict)
            for tc in tienscombs:
                combinaties.append([honderd_strong] + tc)

    if cijfer < 100:
        return [c for c in decompose_under_hundred(cijfer, cijferdict) if c]

    return combinaties


def decompose_under_hundred(n, cijferdict=None):
    """Decompose getal < 100 in tientallen + eenheden Strongs."""
    if cijferdict is None:
        cijferdict = HEBR_CIJFERS
    if n == 0:
        return [[]]
    out = []
    tien = (n // 10) * 10
    eenh = n % 10
    tienstrong = [k for k, v in cijferdict.items() if v == tien] if tien > 0 else []
    eenhstrong = [k for k, v in cijferdict.items() if v == eenh] if eenh > 0 else []
    combo = []
    if tienstrong:
        combo.extend(tienstrong[:1])
    if eenhstrong:
        combo.extend(eenhstrong[:1])
    if combo:
        out.append(combo)
    return out if out else [[]]


def normaliseer_strong(s):
    """Strip prefix-letters (Hc/, Hb/, etc.) van Strong-code."""
    if not s:
        return s
    if '/' in s:
        return s.split('/')[-1]
    return s


def vers_strongs_set(vers_obj):
    """Returnt set van genormaliseerde Strong-codes voor een vers.
    Probeert eerst 'verse_strongs' (Hebreeuws/Aramees), valt terug op
    words[].strong (Grieks)."""
    vs = vers_obj.get('verse_strongs')
    if vs:
        return set(normaliseer_strong(s) for s in vs)
    # Fallback: extract uit words
    out = set()
    for w in vers_obj.get('words', []):
        s = w.get('strong')
        if s:
            out.add(normaliseer_strong(s))
    return out


def laad_alle_verzen():
    """Laad alle Strong-jsonl bestanden en geef iterator over (vers_obj, boek)."""
    if not os.path.isdir(STRONG_DIR):
        print(f"FOUT: {STRONG_DIR} niet gevonden", file=sys.stderr)
        sys.exit(1)
    for fname in sorted(os.listdir(STRONG_DIR)):
        if not fname.endswith('.jsonl'):
            continue
        boek = fname[:-6]
        path = os.path.join(STRONG_DIR, fname)
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    yield obj, boek
                except json.JSONDecodeError:
                    continue


def zoek_strong(strong_code):
    """Vind alle voorkomens van een specifieke Strong-code."""
    target = normaliseer_strong(strong_code)
    treffers = []
    for vers, boek in laad_alle_verzen():
        if target in vers_strongs_set(vers):
            treffers.append({
                'boek': boek,
                'hoofdstuk': vers.get('chapter'),
                'vers': vers.get('verse'),
                'context': maak_context(vers),
            })
    return treffers


def zoek_strongs_nabij(strong_codes):
    """Vind verzen waar ALLE genoemde Strong-codes samen voorkomen."""
    targets = set(normaliseer_strong(s) for s in strong_codes)
    treffers = []
    for vers, boek in laad_alle_verzen():
        vstrongs = vers_strongs_set(vers)
        if targets.issubset(vstrongs):
            treffers.append({
                'boek': boek,
                'hoofdstuk': vers.get('chapter'),
                'vers': vers.get('verse'),
                'gevonden_strongs': list(targets),
                'context': maak_context(vers),
            })
    return treffers


def zoek_cijfer(cijfer):
    """Vind alle verzen waar een cijfer voorkomt, in alle drie bron-talen."""
    alle_treffers = {}
    for taal in ('hebr', 'aram', 'grieks'):
        combinaties = cijfer_naar_strong_combinatie(cijfer, taal)
        for combo in combinaties:
            if not combo:
                continue
            treffers = zoek_strongs_nabij(combo)
            for t in treffers:
                key = (t['boek'], t['hoofdstuk'], t['vers'])
                if key not in alle_treffers:
                    alle_treffers[key] = t
                    alle_treffers[key]['combinatie'] = combo
                    alle_treffers[key]['taal'] = taal
    return list(alle_treffers.values())


def maak_context(vers):
    """Bouw een leesbare context-string uit het vers-object."""
    woorden = vers.get('words', [])
    parts = []
    for w in woorden:
        h = w.get('hebrew') or w.get('greek') or ''
        t = w.get('translit', '')
        s = w.get('strong', '')
        parts.append(f"{h}({t}|{s})")
    return ' '.join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cijfer', type=int, help='Zoek alle voorkomens van een cijfer (Hebreeuws).')
    parser.add_argument('--strong', help='Zoek alle voorkomens van één Strong-code (bv. H120).')
    parser.add_argument('--strongs', help='Komma-gescheiden Strong-codes (bv. H3967,H6242). Vinden samen in één vers.')
    parser.add_argument('--nabijheid', action='store_true', help='Bij --strongs: alleen verzen waar ALLEN samen voorkomen.')
    parser.add_argument('--max', type=int, default=200, help='Maximaal aantal treffers in output (default 200).')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--samenvatting', action='store_true', help='Toon alleen statistieken per boek.')
    args = parser.parse_args()

    if args.cijfer:
        treffers = zoek_cijfer(args.cijfer)
        label = f"Cijfer {args.cijfer}"
    elif args.strong:
        treffers = zoek_strong(args.strong)
        label = f"Strong {args.strong}"
    elif args.strongs:
        codes = [c.strip() for c in args.strongs.split(',')]
        treffers = zoek_strongs_nabij(codes) if args.nabijheid else zoek_strong(codes[0])
        label = f"Strongs {','.join(codes)}"
    else:
        parser.print_help()
        sys.exit(1)

    if args.samenvatting:
        per_boek = defaultdict(int)
        for t in treffers:
            per_boek[t['boek']] += 1
        out = {
            'label': label,
            'totaal': len(treffers),
            'per_boek': dict(per_boek),
        }
    else:
        out = {
            'label': label,
            'totaal': len(treffers),
            'treffers': treffers[:args.max],
            'getoond': min(args.max, len(treffers)),
        }

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"=== {label} — {out['totaal']} treffers ===")
        if args.samenvatting:
            for boek, n in sorted(out['per_boek'].items(), key=lambda x: -x[1]):
                print(f"  {boek}: {n}")
        else:
            for t in treffers[:args.max]:
                print(f"\n{t['boek']} {t['hoofdstuk']}:{t['vers']}")
                if 'combinatie' in t:
                    print(f"  combinatie: {' + '.join(t['combinatie'])} (taal: {t.get('taal','?')})")
                print(f"  {t['context']}")


if __name__ == '__main__':
    main()
