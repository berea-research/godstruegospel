"""
build_strong_vers_index.py
==========================

Bouwt omgekeerde Strong-index uit feitenlaag.
Hebreeuws gebruikt verse_strongs + split op '/'.
Grieks gebruikt word.strong direct (een code per woord).
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Kennis"
STRONG_DIR = ROOT / "strong"
OUT_DIR = ROOT / "index"
MASTER_HEB = ROOT / "concordant-nl-hebreeuws.json"
MASTER_GR = ROOT / "concordant-nl-grieks.json"

OT_BOOKS = {
    'gen','exo','lev','num','deu','jos','jdg','rut','1sa','2sa','1kg','2kg',
    'isa','jer','eze','hos','joe','amo','oba','jon','mic','nah','hab','zep',
    'hag','zec','mal','psa','pro','job','can','lam','qoh',
    'est','dan','ezr','neh','1ch','2ch',
}
NT_BOOKS = {
    'mat','mar','luk','joh','act','rom','1co','2co','gal','eph','phi','col',
    '1th','2th','1ti','2ti','tit','phm','heb','jam','1pe','2pe','1jo','2jo','3jo','jud','rev',
}


def book_from_filename(fname):
    base = fname.replace('.jsonl', '')
    if '-' in base:
        base = base.split('-')[0]
    return base


def select_files(book_set):
    out = []
    for f in sorted(STRONG_DIR.iterdir()):
        if f.suffix != '.jsonl':
            continue
        if book_from_filename(f.name) in book_set:
            out.append(f)
    return out


def build_index(files):
    index = defaultdict(list)
    total_verses = 0
    total_tokens = 0
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                verse = json.loads(line)
                book = verse['book']
                ch = verse['chapter']
                v = verse['verse']
                total_verses += 1
                tags = verse.get('verse_strongs', [])
                if tags:
                    for tag in tags:
                        for part in tag.split('/'):
                            if part:
                                index[part].append({"b": book, "c": ch, "v": v})
                                total_tokens += 1
                else:
                    for word in verse.get('words', []):
                        tag = word.get('strong', '')
                        if tag:
                            for part in tag.split('/'):
                                if part:
                                    index[part].append({"b": book, "c": ch, "v": v})
                                    total_tokens += 1
    return index, total_verses, total_tokens


def load_master(path):
    m = json.load(open(path, 'r', encoding='utf-8'))
    return {e['strong']: e for e in m['entries']}


def parse_count(val):
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        s = val.replace('.', '').replace(',', '').strip()
        try:
            return int(s)
        except ValueError:
            return None
    return None


def validate(index, master_entries):
    mismatches = []
    iim = []
    imi = []
    for code, locs in index.items():
        if code in master_entries:
            entry = master_entries[code]
            mc = parse_count(entry.get('voorkomens'))
            if mc is None:
                mc = parse_count(entry.get('voorkomens_ca'))
            ic = len(locs)
            if mc is not None and mc != ic:
                mismatches.append((code, mc, ic))
        else:
            iim.append((code, len(locs)))
    for code, entry in master_entries.items():
        if code not in index:
            mc = parse_count(entry.get('voorkomens'))
            if mc is None:
                mc = parse_count(entry.get('voorkomens_ca'))
            imi.append((code, mc))
    return mismatches, iim, imi


def write_index(index, out_path):
    out = dict(index)
    with open(out_path, 'w', encoding='utf-8') as fp:
        json.dump(out, fp, ensure_ascii=False, separators=(',', ':'))


def run(language):
    if language == 'hebreeuws':
        files = select_files(OT_BOOKS)
        master_path = MASTER_HEB
        out_path = OUT_DIR / 'strong-vers-hebreeuws.json'
    else:
        files = select_files(NT_BOOKS)
        master_path = MASTER_GR
        out_path = OUT_DIR / 'strong-vers-grieks.json'

    print("=== " + language.upper() + " ===")
    print(f"Bestanden: {len(files)}")
    index, total_verses, total_tokens = build_index(files)
    print(f"Verzen: {total_verses}")
    print(f"Strong-tokens: {total_tokens}")
    print(f"Unieke Strong-codes in index: {len(index)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_index(index, out_path)
    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"Geschreven: {out_path.name} ({size_mb:.2f} MB)")

    print("\n--- VALIDATIE ---")
    master_entries = load_master(master_path)
    print(f"Master entries: {len(master_entries)}")
    mismatches, iim, imi = validate(index, master_entries)
    print(f"Count-mismatches: {len(mismatches)}")
    print(f"In index, niet in master: {len(iim)}")
    print(f"In master, niet in index: {len(imi)}")

    if mismatches:
        print("\nTop 20 mismatches:")
        for code, mc, ic in mismatches[:20]:
            print(f"  {code}: master={mc}, index={ic}, diff={ic - mc:+d}")
    if iim:
        print("\nTop 20 in_index_niet_master:")
        for code, c in sorted(iim, key=lambda x: -x[1])[:20]:
            print(f"  {code}: {c}")
    if imi:
        print("\nTop 20 in_master_niet_index:")
        for code, c in sorted(imi, key=lambda x: -(x[1] or 0))[:20]:
            print(f"  {code}: {c}")


if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'hebreeuws'
    run(lang)
    print("\n--- KLAAR ---")
