"""
append_a5_batch.py
==================

Appends a Fase A5-batch to master v2.1.

Usage: python3 append_a5_batch.py increments/h_a5_batchN.py

Verschillen met oudere append_batch.py:
  - Master gebruikt nu veld `voorkomens` (exact, uit feitenlaag-sweep), niet `voorkomens_ca`.
  - Verwacht voorkomens-aantal in tuple wordt gevalideerd tegen index-tellingen.
  - Bij mismatch tussen tuple-aantal en index-aantal: stop met error voor inhoudelijke check.
"""

import json
import sys
import importlib.util
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent / "Kennis"
MASTER = ROOT / "concordant-nl-hebreeuws.json"
INDEX = ROOT / "index" / "strong-vers-hebreeuws.json"


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
        "voorkomens": voork,
        "toelichting": toel,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: append_a5_batch.py <batch_file.py>")
        sys.exit(1)

    batch_path = Path(sys.argv[1])
    spec = importlib.util.spec_from_file_location("batch_mod", batch_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    batch = mod.BATCH

    print(f"Batch geladen: {len(batch)} entries uit {batch_path.name}")

    # Load master en index
    master = json.load(open(MASTER, 'r', encoding='utf-8'))
    index = json.load(open(INDEX, 'r', encoding='utf-8'))
    master_codes = {e['strong'] for e in master['entries']}

    # Validatie: tuple-aantal vs index-aantal, geen duplicaten
    errors = []
    for tup in batch:
        strong, _, _, _, _, _, voork, _ = tup
        if strong in master_codes:
            errors.append(f"  {strong}: al in master, duplicaat")
            continue
        idx_count = len(index.get(strong, []))
        if voork != idx_count:
            errors.append(f"  {strong}: tuple zegt {voork}, index zegt {idx_count}")

    if errors:
        print("VALIDATIE-FOUTEN:")
        for e in errors:
            print(e)
        print("Stop voor inhoudelijke check.")
        sys.exit(1)

    # Append
    for tup in batch:
        master['entries'].append(tup_to_dict(tup))

    # Update meta
    old_count = master['meta'].get('aantal_entries', 0)
    if isinstance(old_count, str):
        try: old_count = int(old_count)
        except: old_count = len(master['entries']) - len(batch)
    master['meta']['aantal_entries'] = len(master['entries'])
    master['meta']['aantal_woorden'] = master['meta'].get('aantal_woorden', 0)
    if isinstance(master['meta']['aantal_woorden'], int):
        master['meta']['aantal_woorden'] += len(batch)

    # Update audit
    audit = master['meta'].get('audit_v2.0', {})
    if not isinstance(audit, dict):
        audit = {'v2.0': str(audit)}
    log_key = f"a5_batch_{batch_path.stem}"
    audit[log_key] = f"Toegevoegd {len(batch)} entries via Fase A5 (B5-impl-1 gat-detectie)."
    master['meta']['audit_v2.0'] = audit

    # Schrijf
    with open(MASTER, 'w', encoding='utf-8') as fp:
        json.dump(master, fp, ensure_ascii=False, indent=2)

    print(f"Master bijgewerkt: {old_count} -> {len(master['entries'])} entries.")
    print(f"Toegevoegd: {len(batch)}")


if __name__ == '__main__':
    main()
