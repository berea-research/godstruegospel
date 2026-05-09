"""
extract_lxx_per_boek.py
=======================

Extracteer LXX G-codes per boek uit ABP en sla op als tussenbestand.
Run via: python3 extract_lxx_per_boek.py <boek1> <boek2> ...
Of zonder args: doet alle boeken die nog ontbreken.

Tussenbestanden in /tmp/lxx_per_boek/<boek>.json
"""

import json, re, sys, time, os
from pathlib import Path
from pysword.modules import SwordModules

ABP_DIR = str(Path(__file__).resolve().parent.parent / "Kennis" / "lxx-bron/ABP-extracted")
TMP_DIR = Path("/tmp/lxx_per_boek")
TMP_DIR.mkdir(exist_ok=True)

ABP_BOOKS = ['gen','exod','lev','num','deut','josh','judg','ruth','1sam','2sam','1kgs','2kgs','1chr','2chr','ezra','neh','esth','job','ps','prov','eccl','song','isa','jer','lam','ezek','dan','hos','joel','amos','obad','jonah','mic','nah','hab','zeph','hag','zech','mal']

def normalize_g(g):
    g_clean = g.split('.')[0]
    return 'G' + str(int(g_clean))

def main():
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        targets = [b for b in ABP_BOOKS if not (TMP_DIR / f"{b}.json").exists()]

    if not targets:
        print("Alle boeken al geëxtraheerd")
        return

    print(f"Targets: {targets}")
    modules = SwordModules(ABP_DIR)
    modules.parse_modules()
    abp = modules.get_bible_from_module('ABP')

    for book in targets:
        if book not in ABP_BOOKS:
            print(f"  {book}: onbekend, skip")
            continue
        out_path = TMP_DIR / f"{book}.json"
        if out_path.exists():
            print(f"  {book}: al klaar")
            continue
        t0 = time.time()
        try:
            verses = list(abp.get_iter(books=[book], clean=False))
        except Exception as e:
            print(f"  {book}: FOUT {e}")
            continue
        # Per vers G-codes
        per_verse = []
        for txt in verses:
            gcodes_raw = re.findall(r'strong:G(\d+(?:\.\d+)*)', txt)
            gcodes = []
            for g in gcodes_raw:
                try:
                    gcodes.append(normalize_g(g))
                except (ValueError, IndexError):
                    continue
            per_verse.append(sorted(set(gcodes)))
        with open(out_path, 'w') as fp:
            json.dump(per_verse, fp)
        print(f"  {book}: {len(per_verse)} verzen, {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
