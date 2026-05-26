"""
fix_master_counts.py
====================

Lijnt master-counts uit op exacte tellingen uit de omgekeerde Strong-index.

Voor elke entry in concordant-nl-hebreeuws.json:
  - voorkomens_ca (circa-veld) wordt vervangen door voorkomens (exact, uit index).
  - Oude waarde wordt vastgelegd in een audit-log voor traceability.

253 codes in feitenlaag die niet in master zitten worden NIET door dit script
toegevoegd; die behoeven inhoudelijke entry-creatie via zeven-ankers (Fase A5).

Output:
  - concordant-nl-hebreeuws.json overschreven (backup eerst)
  - count-corrections-log-2026-04-26.md in docs/

B5-impl-1 vervolg, A3.7 master-correctie, datum 2026-04-26.
"""

import json
import shutil
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent / "Kennis"
DOCS = Path("./docs")

MASTER_HEB = ROOT / "concordant-nl-hebreeuws.json"
INDEX_HEB = ROOT / "index" / "strong-vers-hebreeuws.json"
BACKUP = ROOT / f"concordant-nl-hebreeuws.v2.0-pre-correctie.json"
LOG_FILE = DOCS / "count-corrections-log-2026-04-26.md"


def main():
    print("Backup originele master...")
    shutil.copy(MASTER_HEB, BACKUP)
    print(f"  -> {BACKUP.name}")

    print("Lezen master en index...")
    master = json.load(open(MASTER_HEB, 'r', encoding='utf-8'))
    index = json.load(open(INDEX_HEB, 'r', encoding='utf-8'))

    corrections = []
    unchanged = 0
    not_in_index = []

    for entry in master['entries']:
        code = entry['strong']
        if code in index:
            new_count = len(index[code])
            old_count = entry.get('voorkomens_ca')
            if old_count != new_count:
                corrections.append((code, old_count, new_count, new_count - (old_count if isinstance(old_count, int) else 0)))
            # Verwijder oude veld, voeg nieuwe toe
            entry.pop('voorkomens_ca', None)
            entry['voorkomens'] = new_count
            if old_count == new_count:
                unchanged += 1
        else:
            old_count = entry.get('voorkomens_ca', 0)
            not_in_index.append((code, old_count))
            # Geen index-data: zet voorkomens op 0 met flag
            entry.pop('voorkomens_ca', None)
            entry['voorkomens'] = 0
            entry['flag_corpus_afwezig'] = True

    # Update meta
    master['meta']['versie'] = '2.1'
    master['meta']['datum'] = str(date.today())
    audit_blok = master['meta'].get('audit_v2.0', {})
    if not isinstance(audit_blok, dict):
        audit_blok = {'v2.0': audit_blok}
    audit_blok['v2.1'] = (
        f"Master-counts uitgelijnd op exacte tellingen uit omgekeerde Strong-index. "
        f"{len(corrections)} entries gecorrigeerd, {unchanged} entries ongewijzigd. "
        f"{len(not_in_index)} entries hadden geen feitenlaag-voorkomen en zijn op 0 gezet "
        f"met flag_corpus_afwezig=True. Veld voorkomens_ca hernoemd naar voorkomens "
        f"(exact); circa-suffix was misleidend gebleken."
    )
    master['meta']['audit_v2.0'] = audit_blok

    # Schrijf bijgewerkte master
    print("Schrijven bijgewerkte master...")
    with open(MASTER_HEB, 'w', encoding='utf-8') as fp:
        json.dump(master, fp, ensure_ascii=False, indent=2)
    print(f"  -> {MASTER_HEB.name} (v2.1)")

    # Audit log
    DOCS.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'w', encoding='utf-8') as fp:
        fp.write("# Count-corrections-log Hebreeuwse master\n\n")
        fp.write(f"**Datum:** {date.today()}\n")
        fp.write(f"**Bron:** B5-impl-1 omgekeerde Strong-index\n")
        fp.write(f"**Methodiek:** master `voorkomens_ca` (circa) vervangen door `voorkomens` (exact, uit feitenlaag-sweep).\n\n")
        fp.write(f"## Samenvatting\n\n")
        fp.write(f"Master entries totaal: {len(master['entries'])}\n\n")
        fp.write(f"Entries gecorrigeerd: {len(corrections)}\n\n")
        fp.write(f"Entries ongewijzigd: {unchanged}\n\n")
        fp.write(f"Entries zonder feitenlaag-voorkomen (flag_corpus_afwezig): {len(not_in_index)}\n\n")
        fp.write(f"## Top 50 grootste correcties (absoluut verschil)\n\n")
        fp.write("| Strong | oud (ca) | nieuw (exact) | verschil |\n")
        fp.write("|--------|----------|---------------|----------|\n")
        for code, old, new, diff in sorted(corrections, key=lambda x: -abs(x[3] if isinstance(x[3], int) else 0))[:50]:
            fp.write(f"| {code} | {old} | {new} | {diff:+d} |\n")
        fp.write(f"\n## Entries zonder feitenlaag-voorkomen ({len(not_in_index)})\n\n")
        fp.write("Deze codes stonden in de master maar komen niet in de WLC-feitenlaag voor. "
                "Mogelijke oorzaken: dialect-varianten, foutieve master-entry van eerdere fase, "
                "of corpus-bron verschilt. Aparte review nodig in Fase A5.\n\n")
        fp.write("| Strong | oude voorkomens_ca |\n")
        fp.write("|--------|--------------------|\n")
        for code, old in sorted(not_in_index)[:100]:
            fp.write(f"| {code} | {old} |\n")
        if len(not_in_index) > 100:
            fp.write(f"\n_(... en {len(not_in_index) - 100} meer)_\n")

    print(f"  -> {LOG_FILE.name}")
    print(f"\nSamenvatting:")
    print(f"  Master entries: {len(master['entries'])}")
    print(f"  Gecorrigeerd:   {len(corrections)}")
    print(f"  Ongewijzigd:    {unchanged}")
    print(f"  Niet in feitenlaag (flag): {len(not_in_index)}")


if __name__ == '__main__':
    main()
