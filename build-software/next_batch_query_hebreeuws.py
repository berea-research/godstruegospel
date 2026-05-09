#!/usr/bin/env python3
"""Print next N Strongs not yet in master.

Usage: next_batch_query.py [N]  (default N=10; gebruik 20 om langs de 8 prefix-'+'-artefacten te kijken)

Paths zijn relatief aan deze script-locatie:
- Master:  ../Kennis/concordant-nl-hebreeuws.json
- Corpus:  ../Kennis/strong/*.jsonl
"""
import json
from collections import Counter
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
MASTER = SCRIPT_DIR.parent / "Kennis" / "concordant-nl-hebreeuws.json"
CORPUS = SCRIPT_DIR.parent / "Kennis" / "strong"
OT_BOOKS = ['gen','exo','lev','num','deu','jos','jdg','rut','1sa','2sa','1kg','2kg','1ch','2ch','ezr','neh','est','job','psa-1','psa-2','psa-3','psa-4','psa-5','pro','ecc','can','isa','jer','lam','eze','dan','hos','joe','amo','oba','jon','mic','nah','hab','zep','hag','zec','mal']

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10

d = json.loads(MASTER.read_text(encoding='utf-8'))
done = set(e['strong'] for e in d['entries'])

counter = Counter()
for book in OT_BOOKS:
    p = CORPUS / f'{book}.jsonl'
    if not p.exists(): continue
    with open(p) as f:
        for line in f:
            v = json.loads(line)
            for w in v.get('words', []):
                s = w.get('strong', '')
                if not s: continue
                for pa in s.split('/'):
                    if pa and (pa.startswith('H') or pa.startswith('A')):
                        counter[pa] += 1

remaining = [(s, c) for s, c in counter.most_common() if s not in done]
total_remaining = len(remaining)
for s, c in remaining[:N]:
    hebrew_sample = ''
    translit_sample = ''
    for book in OT_BOOKS:
        p = CORPUS / f'{book}.jsonl'
        if not p.exists(): continue
        found = False
        with open(p) as f:
            for line in f:
                v = json.loads(line)
                for w in v.get('words', []):
                    if w.get('strong', '').endswith(s) or w.get('strong','') == s:
                        hebrew_sample = w.get('hebrew','')
                        translit_sample = w.get('translit','')
                        found = True
                        break
                if found: break
        if found: break
    print(f'  {s}: freq={c} | {hebrew_sample} | {translit_sample}')
print(f'\nTotaal resterend: {total_remaining} Strongs, {sum(c for _,c in remaining)} tokens')
