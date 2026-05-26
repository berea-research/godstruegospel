"""
append_batch_en.py - voeg een vertaal-batch toe aan de EN-master-bestanden.

Hergebruikbaar voor latere talen via --taal parameter (default: en).

Werkwijze:
- input is een JSON-bestand met velden:
    {
      "batch_id": "h_batch_001",
      "script": "heb" | "gr",
      "datum": "2026-04-29",
      "entries": [ {strong, hebreeuws|grieks, translit, woordsoort,
                    en_concordant, grondvorm, stamfamilie, toelichting,
                    voorkomens|voorkomens_ca}, ... ]
    }
- script laadt master, voegt entries toe (afgewezen bij duplicate-strong),
  update meta (aantal_entries, voortgang_pct, datum_laatste_batch, audit-log),
  schrijft master terug.

CLI:
    python3 append_batch_en.py --batch path/to/batch.json
    python3 append_batch_en.py --batch path/to/batch.json --taal en --dry-run
"""
import json
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent / "Kennis"


def master_path(taal, script):
    script_naam = 'hebreeuws' if script == 'heb' else 'grieks'
    if taal == 'nl':
        return ROOT / f'concordant-nl-{script_naam}.json'
    return ROOT / 'masters' / taal / f'concordant-{taal}-{script_naam}.json'


def load_master(path):
    return json.load(open(path, encoding='utf-8'))


def write_master(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def validate_entry(entry, taal):
    """Controleer dat een entry de verplichte velden heeft."""
    required = {'strong', 'translit', 'woordsoort', 'grondvorm',
                'stamfamilie', 'toelichting'}
    concordant_key = f'{taal}_concordant'
    required.add(concordant_key)
    missing = required - set(entry.keys())
    if missing:
        return f"missing fields: {sorted(missing)}"
    return None


def append_batch(batch_path, taal='en', dry_run=False):
    batch = json.load(open(batch_path, encoding='utf-8'))
    script = batch['script']
    batch_id = batch['batch_id']
    datum = batch.get('datum') or str(date.today())
    new_entries = batch['entries']

    mpath = master_path(taal, script)
    master = load_master(mpath)
    existing_strongs = {e['strong'] for e in master['entries']}

    # Validate all entries before writing anything
    errors = []
    for i, e in enumerate(new_entries):
        err = validate_entry(e, taal)
        if err:
            errors.append(f"  entry #{i} (strong={e.get('strong', '?')}): {err}")
        elif e['strong'] in existing_strongs:
            errors.append(f"  entry #{i}: duplicate strong '{e['strong']}'")
    if errors:
        print(f"VALIDATION FAILED for {batch_id}:")
        for e in errors:
            print(e)
        sys.exit(1)

    # Append
    master['entries'].extend(new_entries)
    aantal = len(master['entries'])
    doel = master['meta'].get('aantal_entries_doel', aantal)
    pct = round(100.0 * aantal / doel, 2) if doel else 0.0

    master['meta']['aantal_entries'] = aantal
    master['meta']['voortgang_pct'] = pct
    master['meta']['datum_laatste_batch'] = datum
    audit = master['meta'].setdefault('audit', {})
    audit[batch_id] = (f"{datum} - added {len(new_entries)} entries "
                       f"(cumulative {aantal}/{doel}, {pct}%)")

    if dry_run:
        print(f"DRY-RUN: would add {len(new_entries)} entries to {mpath}")
        print(f"         cumulative would be {aantal}/{doel} ({pct}%)")
        return

    write_master(mpath, master)
    print(f"OK: appended {len(new_entries)} entries to {mpath}")
    print(f"    cumulative {aantal}/{doel} ({pct}%)")
    print(f"    batch_id  {batch_id}")
    print(f"    datum     {datum}")


def main():
    args = sys.argv[1:]

    def get(flag, default=None):
        if flag in args:
            i = args.index(flag)
            return args[i+1] if i+1 < len(args) else default
        return default

    batch = get('--batch')
    if not batch:
        print(__doc__)
        sys.exit(1)

    taal = get('--taal', 'en')
    dry = '--dry-run' in args
    append_batch(batch, taal=taal, dry_run=dry)


if __name__ == '__main__':
    main()
