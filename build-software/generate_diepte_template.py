"""
generate_diepte_template.py
===========================

Genereert sjabloon-notities voor diepte-laag uit master, index, en LXX-mapping.
Sectie A, D, E (LXX-tabel), G (stamfamilie) en H worden automatisch gevuld;
B, C, E (cognaten), F en G (clusters) zijn placeholders die via de
zeven-ankers-discipline (B5-impl-3) handmatig moeten worden gevuld of via de
r_common+r_mk-helpers in outputs/ kunnen worden geupgrade naar route-A-kwaliteit.

Output: Kennis/diepte/[Strong].md

Gebruik:
    python3 generate_diepte_template.py H559                # 1 specifieke H/G-code
    python3 generate_diepte_template.py G2316               # idem voor Grieks
    python3 generate_diepte_template.py 31-60               # range items 31-60 (Hebreeuws kernwoordenlijst)
    python3 generate_diepte_template.py                     # default top-30 Hebreeuws

Vlaggen:
    --force      Overschrijf bestaande diepte-notities (DEFAULT: skip)
    --dry-run    Print alleen wat zou worden geschreven, schrijf niets

Reparatie 2026-04-28:
- Oorspronkelijk script was afgekapt: targets-regel + for-loop + __main__-block
  ontbraken, waardoor main() nooit werd aangeroepen.
- Toegevoegd: skip-bestaande-bestanden default + --force/--dry-run vlaggen om
  bestaande route-A-notities niet onbedoeld te overschrijven met sjabloon-
  placeholders.
- Toegevoegd: NT_GENRES voor G-prefix items en index_g support.
"""
import json
import sys
import re as _re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Kennis"
DIEPTE_DIR = ROOT / "diepte"
MASTER_HEB = ROOT / "concordant-nl-hebreeuws.json"
MASTER_GR = ROOT / "concordant-nl-grieks.json"
INDEX_HEB = ROOT / "index" / "strong-vers-hebreeuws.json"
INDEX_GR = ROOT / "index" / "strong-vers-grieks.json"
LXX = ROOT / "lxx-mapping-hebreeuws.json"

HEB_GENRES = {
    'Tora': {'gen', 'exo', 'lev', 'num', 'deu'},
    'Vroege Profeten': {'jos', 'jdg', '1sa', '2sa', '1kg', '2kg'},
    'Late Profeten': {'isa', 'jer', 'eze', 'hos', 'joe', 'amo', 'oba', 'jon',
                      'mic', 'nah', 'hab', 'zep', 'hag', 'zec', 'mal'},
    'Geschriften': {'psa', 'pro', 'job', 'can', 'rut', 'lam', 'qoh', 'est',
                    'dan', 'ezr', 'neh', '1ch', '2ch'},
}

NT_GENRES = {
    'Evangelien + Hand': {'mat', 'mar', 'luk', 'joh', 'act'},
    'Paulus': {'rom', '1co', '2co', 'gal', 'eph', 'phi', 'col', '1th', '2th',
               '1ti', '2ti', 'tit', 'phm'},
    'Algemene brieven': {'heb', 'jam', '1pe', '2pe', '1jo', '2jo', '3jo', 'jud'},
    'Openbaring': {'rev'},
}


def get_voork(e):
    v = e.get('voorkomens')
    if v is None:
        v = e.get('voorkomens_ca', 0)
    return v if isinstance(v, int) else 0


def gen_template(strong, master_h, master_g, index_h, index_g, lxx_map):
    is_grieks = strong.startswith('G')
    target_master = master_g if is_grieks else master_h
    other_master = master_h if is_grieks else master_g
    index = index_g if is_grieks else index_h
    genres = NT_GENRES if is_grieks else HEB_GENRES

    e = target_master.get(strong) or other_master.get(strong)
    if not e:
        return f"# {strong}\n\nStrong {strong} niet gevonden in master.\n"

    voork = get_voork(e)
    woord = e.get('hebreeuws') or e.get('grieks', '')
    translit = e.get('translit', '')
    nl = e.get('nl_concordant', '')
    woordsoort = e.get('woordsoort', '')
    toel = e.get('toelichting', '')
    stamfam = e.get('stamfamilie', [])

    locs = index.get(strong, [])
    book_count = Counter(l['b'] for l in locs)
    genre_count = {g: 0 for g in genres}
    for b, c in book_count.items():
        for g, books in genres.items():
            if b in books:
                genre_count[g] += c

    lxx_entry = lxx_map.get(strong, {})
    top_g = lxx_entry.get('top_g', [])

    base_match = _re.match(r'^([HG])(\d+)([a-f]?)\+?$', strong)
    base = (base_match.group(1) + base_match.group(2)) if base_match else strong
    cluster = []
    for s, ent in target_master.items():
        b_match = _re.match(r'^([HG])(\d+)([a-f]?)\+?$', s)
        if b_match and (b_match.group(1) + b_match.group(2)) == base and s != strong:
            cluster.append((s, ent.get('nl_concordant', ''), get_voork(ent)))

    today = date.today().isoformat()
    index_filename = 'strong-vers-grieks.json' if is_grieks else 'strong-vers-hebreeuws.json'

    out = []
    out.append(f"# {strong} {translit} - {nl}\n")
    out.append(f"**Versie:** v1.0 sjabloon | **Datum:** {today} | **Type:** diepte-notitie B5-impl-3\n\n")
    out.append("---\n\n")
    out.append("## A. Hoofd-blok\n\n")
    out.append(f"**Strong-code:** {strong}\n\n")
    label = 'Grieks' if is_grieks else 'Hebreeuws'
    out.append(f"**{label}:** {woord}\n\n")
    out.append(f"**Transliteratie:** {translit}\n\n")
    out.append(f"**NL-concordant:** {nl}\n\n")
    out.append(f"**Woordsoort:** {woordsoort}\n\n")
    out.append(f"**Voorkomens (corpus):** {voork}\n\n")
    if toel:
        out.append(f"**Master-toelichting:** {toel}\n\n")

    out.append("## B. Wortel-analyse (anker 1)\n\n")
    out.append("**Wortel:** _[handmatig invullen]_\n\n")
    out.append("**Etymologie:** _[handmatig invullen]_\n\n")
    out.append("**Basisbetekenis:** _[handmatig invullen]_\n\n")
    out.append("**Semantische velden:** _[handmatig invullen]_\n\n")

    out.append("## C. Morfologische varianten (anker 2)\n\n")
    out.append("**Vormen die voorkomen:** _[handmatig invullen]_\n\n")
    if stamfam:
        out.append(f"**Stamfamilie uit master:** {', '.join(stamfam)}\n\n")
    if cluster:
        out.append(f"**Sub-sense vertakkingen ({len(cluster)}):**\n\n")
        out.append("| Sub-Strong | NL | Voork |\n|---|---|---|\n")
        for s, n, v in sorted(cluster):
            out.append(f"| {s} | {n} | {v} |\n")
        out.append("\n")
    else:
        out.append("**Sub-sense vertakkingen:** geen\n\n")

    out.append("## D. Parallelplaatsen-overzicht (anker 3)\n\n")
    out.append("**Distributie per genre:**\n\n")
    out.append("| Genre | Voorkomens |\n|---|---|\n")
    for g, c in genre_count.items():
        out.append(f"| {g} | {c} |\n")
    out.append("\n")
    out.append(f"**Volledige vers-lijst:** zie omgekeerde index `Kennis/index/{index_filename}` onder key `{strong}`.\n\n")

    out.append("## E. Cognaten en LXX-koppeling (anker 4)\n\n")
    out.append("**Cognaten in zustertalen:** _[handmatig invullen: Aramees, Akkadisch, Ugaritisch, Fenicisch waar relevant; voor G-prefix: klassiek-Grieks + Indo-Europese cognaten]_\n\n")
    if top_g:
        kop = "Hebreeuwse OT-bronnen" if is_grieks else "Griekse LXX-tegenhangers"
        out.append(f"**{kop} (top 5 via LIFT-score):**\n\n")
        out.append("| Code | Co-voorkomens | Co-score | Lift |\n|---|---|---|---|\n")
        for g in top_g[:5]:
            ref = g.get('g') or g.get('h') or g.get('code', '')
            ref_entry = master_h.get(ref) or master_g.get(ref) or {}
            ref_nl = ref_entry.get('nl_concordant', '?')
            out.append(f"| {ref} ({ref_nl}) | {g.get('count','')} | {g.get('co_score','')} | {g.get('lift','')} |\n")
        out.append("\n")
    else:
        out.append("**LXX-tegenhangers:** geen significante mapping (woord komt mogelijk weinig voor in LXX of geen vers-niveau-correlatie).\n\n")

    out.append("## F. Syntactische gebruikspatronen (anker 5)\n\n")
    out.append("**Kenmerkende constructies:** _[handmatig invullen]_\n\n")
    out.append("**Voorkomende voorzetsels of bijbehorende werkwoorden:** _[handmatig invullen]_\n\n")

    out.append("## G. Lexicale clustering (anker 6)\n\n")
    if stamfam:
        out.append("**Stamfamilie-leden uit master:**\n\n")
        out.append("| Strong | NL | Voork |\n|---|---|---|\n")
        for sf in stamfam:
            ent = master_h.get(sf) or master_g.get(sf)
            if ent:
                out.append(f"| {sf} | {ent.get('nl_concordant','')} | {get_voork(ent)} |\n")
            else:
                out.append(f"| {sf} | _(niet in master)_ | - |\n")
        out.append("\n")
    else:
        out.append("**Stamfamilie:** geen verwijzingen in master\n\n")
    out.append("**Verwante semantische velden:** _[handmatig invullen - vijf clusters volgens zeven-ankers-discipline; Cluster I = kern-cluster met primary_pair en secondary_pair, Cluster II-V = structurele cross-reference-rasters (Yah/Christus, Israel/gemeente, tijds, werkwoord)]_\n\n")

    out.append("## H. Distributie-tabel per boek (anker 7)\n\n")
    out.append("**Top 15 boeken op voorkomens:**\n\n")
    out.append("| Boek | Voork |\n|---|---|\n")
    for b, c in book_count.most_common(15):
        out.append(f"| {b} | {c} |\n")
    out.append(f"\n**Totaal voorkomens:** {voork}\n\n")
    boekentotaal = 27 if is_grieks else 39
    out.append(f"**Aantal boeken waar gebruikt:** {len(book_count)}/{boekentotaal}\n\n")

    out.append("---\n\n")
    out.append("_Sjabloon-velden gemarkeerd met `_[handmatig invullen]_` moeten via zeven-ankers-discipline worden gevuld. Voor route-A-upgrade: gebruik r_common+r_mk-helpers in outputs/. Strikt taalkundig, geen theologische conclusies._\n")

    return ''.join(out)


def load_master_data():
    print("Bestanden laden...")
    master_h_data = json.load(open(MASTER_HEB))
    master_g_data = json.load(open(MASTER_GR))
    master_h = {e['strong']: e for e in master_h_data['entries']}
    master_g = {e['strong']: e for e in master_g_data['entries']}
    index_h = json.load(open(INDEX_HEB))
    index_g = json.load(open(INDEX_GR)) if INDEX_GR.exists() else {}
    lxx_map = json.load(open(LXX))['mapping']
    return master_h, master_g, index_h, index_g, lxx_map


def resolve_targets(target, master_h, master_g):
    if target and '-' in target and not target.startswith(('H', 'G')):
        start, end = map(int, target.split('-'))
        kern_path = ROOT.parent / 'docs' / 'kernwoordenlijst-v1.0.json'
        kern = json.load(open(kern_path))
        targets = [k['strong'] for k in kern['hebreeuws'][start - 1:end]]
        print(f"Range-modus Hebreeuws: items {start} t/m {end} ({len(targets)} codes)")
    elif target:
        targets = [target]
    else:
        kern_path = ROOT.parent / 'docs' / 'kernwoordenlijst-v1.0.json'
        kern = json.load(open(kern_path))
        targets = [k['strong'] for k in kern['hebreeuws'][:30]]
        print(f"Default: top 30 Hebreeuwse kernwoorden ({len(targets)} codes)")
    return targets


def parse_args(argv):
    args = {'force': False, 'dry_run': False, 'target': None}
    for a in argv[1:]:
        if a == '--force':
            args['force'] = True
        elif a == '--dry-run':
            args['dry_run'] = True
        elif a.startswith('--'):
            print(f"Onbekende vlag: {a}", file=sys.stderr)
            sys.exit(2)
        else:
            args['target'] = a
    return args


def main():
    args = parse_args(sys.argv)
    DIEPTE_DIR.mkdir(parents=True, exist_ok=True)

    master_h, master_g, index_h, index_g, lxx_map = load_master_data()
    targets = resolve_targets(args['target'], master_h, master_g)

    print(f"Genereer {len(targets)} sjablonen (force={args['force']}, dry-run={args['dry_run']})...")
    written = 0
    skipped = 0
    for strong in targets:
        out_path = DIEPTE_DIR / f"{strong}.md"
        if out_path.exists() and not args['force']:
            print(f"  SKIP {strong}.md (bestaat al; gebruik --force om te overschrijven)")
            skipped += 1
            continue
        text = gen_template(strong, master_h, master_g, index_h, index_g, lxx_map)
        if args['dry_run']:
            print(f"  DRY-RUN {strong}.md ({len(text)} chars; niet geschreven)")
        else:
            with open(out_path, 'w', encoding='utf-8') as fp:
                fp.write(text)
            print(f"  {strong}.md ({len(text)} chars)")
            written += 1

    print(f"\nKlaar. {written} geschreven, {skipped} overgeslagen (totaal {len(targets)} targets) naar {DIEPTE_DIR}/")


if __name__ == '__main__':
    main()
