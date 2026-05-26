"""
skill_v5_lookup.py — godstruegospel skill v5, module 2: lookup
==============================================================

Centrale lookup-functies voor de godstruegospel skill. Implementeert
de bron-discipline uit godstruegospel-v5-eindspec.md sectie 6: alleen
toegestane bronnen onder AP/Kennis/, geen externe vertaal-tradities.

Lagen:
  1. Tekstlaag      - puur/[boek].jsonl (grondtekst woorden)
                    - strong/[boek].jsonl (idem, met Strong-codes)
  2. Vertaallaag    - concordant-nl-hebreeuws.json + concordant-nl-grieks.json
                      (later: concordant-en-*, concordant-fr-* etc.)
  3. Diepte-laag    - diepte/[Strong].md per kernwoord
  4. Omgekeerde-idx - index/strong-vers-hebreeuws.json + strong-vers-grieks.json
  5. LXX-mapping    - lxx-mapping.json (H -> top-G)

CLI:
    python3 skill_v5_lookup.py --vers joh:3:16
    python3 skill_v5_lookup.py --strong G3056
    python3 skill_v5_lookup.py --diepte G3056
    python3 skill_v5_lookup.py --index G3056 --max 20
    python3 skill_v5_lookup.py --lxx H1254a
    python3 skill_v5_lookup.py --check-discipline
"""
import json
import sys
from pathlib import Path
from functools import lru_cache

# === Bron-discipline: enige toegestane root ===
ROOT = Path(__file__).resolve().parent.parent / "Kennis"

# Toegestane bestanden binnen ROOT
PUUR_DIR    = ROOT / "puur"
STRONG_DIR  = ROOT / "strong"
DIEPTE_DIR  = ROOT / "diepte"
INDEX_DIR   = ROOT / "index"
MASTER_HEB  = ROOT / "concordant-nl-hebreeuws.json"
MASTER_GR   = ROOT / "concordant-nl-grieks.json"
INDEX_HEB   = INDEX_DIR / "strong-vers-hebreeuws.json"
INDEX_GR    = INDEX_DIR / "strong-vers-grieks.json"
LXX_MAP_H   = ROOT / "lxx-mapping-hebreeuws.json"   # H -> top-G mappings
LXX_MAP_G   = ROOT / "lxx-mapping-grieks.json"      # G -> top-H mappings (zie build_lxx_mapping_grieks.py)
LXX_MAP     = LXX_MAP_H  # alias voor backward-compat

# Verboden patronen (vertaal-tradities)
FORBIDDEN_PATTERNS = ('kjv', 'sv-1977', 'nbg-51', 'nbv', 'hsv', 'naardense',
                      'lutheran', 'esv', 'niv', 'kingjames')


def check_discipline():
    """Verifieer dat geen verboden vertaal-traditie-bestanden in ROOT staan."""
    issues = []
    for p in ROOT.rglob('*'):
        name = p.name.lower()
        for fb in FORBIDDEN_PATTERNS:
            if fb in name:
                issues.append(f"VERBODEN BRON: {p}")
    return issues


# === Cache-laden ===

@lru_cache(maxsize=32)
def load_master(taal='nl', script='heb'):
    """Laad concordant-master voor (taal, script).

    nl: ROOT/concordant-nl-{script}.json (basis-master, blijft op huidige plek)
    overig: ROOT/masters/{taal}/concordant-{taal}-{script}.json
    """
    script_naam = 'hebreeuws' if script == 'heb' else 'grieks'
    if taal == 'nl':
        path = MASTER_HEB if script == 'heb' else MASTER_GR
    else:
        path = ROOT / 'masters' / taal / f'concordant-{taal}-{script_naam}.json'
    if not path.exists():
        raise NotImplementedError(
            f"Master voor taal '{taal}' nog niet gebouwd op {path}. "
            f"Beschikbare talen: nl (compleet), en (in opbouw)."
        )
    data = json.load(open(path, encoding='utf-8'))
    return {e['strong']: e for e in data['entries']}


@lru_cache(maxsize=1)
def load_index(script='heb'):
    """Omgekeerde index: Strong -> [{b, c, v}, ...]."""
    path = INDEX_HEB if script == 'heb' else INDEX_GR
    return json.load(open(path))


@lru_cache(maxsize=2)
def load_lxx(richting='h'):
    """LXX-mapping: 'h' levert H -> top-G; 'g' levert G -> top-H.
    Default 'h' voor backward-compat."""
    if richting == 'h':
        return json.load(open(LXX_MAP_H))['mapping']
    elif richting == 'g':
        if not LXX_MAP_G.exists():
            return {}
        return json.load(open(LXX_MAP_G))['mapping']
    raise ValueError(f"onbekende richting: {richting}")


@lru_cache(maxsize=64)
def load_book_words(boek, with_strong=True):
    """Laad alle verzen van een boek als list[dict]."""
    sub = STRONG_DIR if with_strong else PUUR_DIR
    path = sub / f"{boek}.jsonl"
    if not path.exists():
        return []
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


# === Vers-lookup ===

def lookup_vers(boek, hoofdstuk, vers, with_strong=True):
    """Haal woorden van een specifiek vers op als list[dict]."""
    rows = load_book_words(boek, with_strong=with_strong)
    for r in rows:
        if r['chapter'] == hoofdstuk and r['verse'] == vers:
            return r
    return None


def parse_vers_ref(ref):
    """Parse 'joh:3:16' of 'gen:1:1' naar (boek, hfst, vers)."""
    parts = ref.lower().split(':')
    if len(parts) != 3:
        raise ValueError(f"Vers-ref moet 'boek:hfst:vers' zijn, niet '{ref}'")
    return parts[0], int(parts[1]), int(parts[2])


# === Strong-lookup ===

def lookup_strong(strong, taal='nl'):
    """Vertaal Strong-code naar concordant entry in opgegeven taal.

    Bij ontbrekende entry in niet-NL master: fallback naar NL-master zodat
    een dossier in EN bruikbaar blijft tijdens de build-fase (entries die
    nog niet vertaald zijn vallen terug op de NL-waarde, met markering
    via _en_pending=True in de meta-key)."""
    script = 'gr' if strong.startswith('G') else 'heb'
    master = load_master(taal=taal, script=script)
    entry = master.get(strong)
    if entry is None and taal != 'nl':
        # Fallback NL met merker dat dit nog niet vertaald is
        nl_master = load_master(taal='nl', script=script)
        nl_entry = nl_master.get(strong)
        if nl_entry is not None:
            entry = dict(nl_entry)
            entry['_taal_fallback'] = 'nl'
    return entry


def lookup_diepte(strong):
    """Lees diepte-notitie voor een Strong-code (markdown-tekst)."""
    path = DIEPTE_DIR / f"{strong}.md"
    if not path.exists():
        return None
    return path.read_text(encoding='utf-8')


def lookup_index(strong, max_n=None):
    """Alle vers-locaties voor een Strong-code via omgekeerde index."""
    script = 'gr' if strong.startswith('G') else 'heb'
    idx = load_index(script=script)
    locs = idx.get(strong, [])
    if max_n:
        locs = locs[:max_n]
    return locs


def lookup_lxx(strong):
    """LXX-tegenhanger. Bij H-Strong: top-G mappings.
    Bij G-Strong: top-H bron-mappings (als grieks-mapping beschikbaar is)."""
    if strong.startswith('G'):
        return load_lxx(richting='g').get(strong)
    return load_lxx(richting='h').get(strong)


# === Kerngegevens-aggregatie ===

def kern_voor_strong(strong, taal='nl'):
    """Verzamel alle data voor 1 Strong-code: master + diepte + index + LXX."""
    return {
        'strong': strong,
        'master': lookup_strong(strong, taal=taal),
        'diepte': lookup_diepte(strong),
        'index_count': len(lookup_index(strong)),
        'lxx': lookup_lxx(strong) if strong.startswith('H') else None,
    }


# === CLI ===

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    if '--check-discipline' in args:
        issues = check_discipline()
        if issues:
            print("BRON-DISCIPLINE PROBLEEM:")
            for i in issues:
                print(" ", i)
            sys.exit(1)
        print("Bron-discipline OK: geen verboden vertaal-tradities in", ROOT)
        return

    def get(flag, default=None):
        if flag in args:
            i = args.index(flag)
            return args[i+1] if i+1 < len(args) else default
        return default

    if vers := get('--vers'):
        boek, h, v = parse_vers_ref(vers)
        row = lookup_vers(boek, h, v)
        if not row:
            print(f"Vers niet gevonden: {vers}")
            sys.exit(1)
        print(json.dumps(row, ensure_ascii=False, indent=2))
        return

    if strong := get('--strong'):
        e = lookup_strong(strong)
        print(json.dumps(e, ensure_ascii=False, indent=2) if e else f"Strong niet gevonden: {strong}")
        return

    if strong := get('--diepte'):
        t = lookup_diepte(strong)
        print(t if t else f"Diepte-notitie niet gevonden: {strong}")
        return

    if strong := get('--index'):
        max_n = int(get('--max', '50'))
        locs = lookup_index(strong, max_n=max_n)
        print(json.dumps(locs, ensure_ascii=False, indent=2))
        return

    if strong := get('--lxx'):
        m = lookup_lxx(strong)
        print(json.dumps(m, ensure_ascii=False, indent=2) if m else f"Geen LXX-mapping: {strong}")
        return

    if strong := get('--kern'):
        d = kern_voor_strong(strong)
        # diepte verkort om uitvoer leesbaar te houden
        if d['diepte']:
            d['diepte'] = d['diepte'][:500] + '... [getrunked]'
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return

    print(__doc__)


if __name__ == '__main__':
    main()
