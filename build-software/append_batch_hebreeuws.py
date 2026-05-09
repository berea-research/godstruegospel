#!/usr/bin/env python3
"""Append a batch of concordant entries to the master JSON.

Usage: append_batch.py <batch_file.py>
The batch file must define: BATCH = [(strong, hebreeuws, translit, woordsoort, nl, stamfam, voork, toel), ...]

Paths zijn relatief aan deze script-locatie:
- Master:  ../Kennis/concordant-nl-hebreeuws.json
- Corpus:  ../Kennis/strong/*.jsonl
"""
import json
import sys
import importlib.util
from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).resolve().parent
MASTER = SCRIPT_DIR.parent / "Kennis" / "concordant-nl-hebreeuws.json"
CORPUS = SCRIPT_DIR.parent / "Kennis" / "strong"
OT_BOOKS = ['gen','exo','lev','num','deu','jos','jdg','rut','1sa','2sa','1kg','2kg','1ch','2ch','ezr','neh','est','job','psa-1','psa-2','psa-3','psa-4','psa-5','pro','ecc','can','isa','jer','lam','eze','dan','hos','joe','amo','oba','jon','mic','nah','hab','zep','hag','zec','mal']

def count_corpus():
    counter = Counter()
    for book in OT_BOOKS:
        p = CORPUS / f'{book}.jsonl'
        if not p.exists():
            continue
        with open(p) as f:
            for line in f:
                v = json.loads(line)
                for w in v.get('words', []):
                    s = w.get('strong', '')
                    if not s:
                        continue
                    for pa in s.split('/'):
                        if pa and (pa.startswith('H') or pa.startswith('A')):
                            counter[pa] += 1
    return counter

def tup_to_dict(tup):
    strong, hebreeuws, translit, woordsoort, nl, stamfam, voork, toel = tup
    return {
        "strong": strong,
        "hebreeuws": hebreeuws,
        "translit": translit,
        "woordsoort": woordsoort,
        "nl_concordant": nl,
        "grondvorm": nl,
        "stamfamilie": list(stamfam),
        "voorkomens_ca": voork,
        "toelichting": toel,
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: append_batch.py <batch_file.py>")
        sys.exit(1)

    batch_path = Path(sys.argv[1])
    spec = importlib.util.spec_from_file_location("batch_mod", batch_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    BATCH = mod.BATCH

    master = json.loads(MASTER.read_text(encoding='utf-8'))
    existing = {e['strong']: i for i, e in enumerate(master['entries'])}

    added = 0
    updated = 0
    for tup in BATCH:
        if len(tup) != 8:
            raise ValueError(f"Wrong tuple length for {tup[0]}: {len(tup)}")
        d = tup_to_dict(tup)
        if d['strong'] in existing:
            master['entries'][existing[d['strong']]] = d
            updated += 1
        else:
            master['entries'].append(d)
            added += 1

    def sort_key(e):
        s = e['strong']
        is_prefix = len(s) >= 2 and not s[1].isdigit()
        return (0 if is_prefix else 1, -e['voorkomens_ca'])
    master['entries'].sort(key=sort_key)

    master['meta']['aantal_entries'] = len(master['entries'])
    master['meta']['aantal_prefixen'] = sum(1 for e in master['entries'] if not e['strong'][1].isdigit())
    master['meta']['aantal_woorden'] = sum(1 for e in master['entries'] if e['strong'][1].isdigit())

    MASTER.write_text(json.dumps(master, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"Batch verwerkt: {batch_path.name}")
    print(f"  Nieuw toegevoegd: {added}")
    print(f"  Bijgewerkt: {updated}")
    print(f"  Totaal in master: {master['meta']['aantal_entries']} ({master['meta']['aantal_woorden']} woorden + {master['meta']['aantal_prefixen']} prefixen)")

if __name__ == '__main__':
    main()
