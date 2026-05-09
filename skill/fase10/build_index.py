#!/usr/bin/env python3
"""
Fase 10 web-integratie — bouwt _index.json voor reverse-lookup vers -> entries.

Parsed alle .md files in Kennis/typologie/[A-H]_*/ en extraheert vers-references.
Output: _index.json met structuur:
{
  "verzen": { "Gen 22:4": ["A_entiteit/abraham.md", "B_cijfer/3.md", ...], ... },
  "strongs": { "H7651": [...], "G2033": [...] },
  "stats": { "total_entries": 126, "total_verzen": ..., "total_strongs": ... }
}
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

# Afkortings-map: alle Bijbelboek-aanduidingen die in entries voorkomen, gemapt naar canonical NL-naam.
BOEKEN = {
    # OT
    "gen": "Gen", "genesis": "Gen", "Gen": "Gen", "Genesis": "Gen",
    "exo": "Exo", "exodus": "Exo", "Exo": "Exo", "Exodus": "Exo",
    "lev": "Lev", "leviticus": "Lev", "Lev": "Lev", "Leviticus": "Lev",
    "num": "Num", "numeri": "Num", "Num": "Num", "Numeri": "Num",
    "deu": "Deu", "deuteronomium": "Deu", "Deu": "Deu", "Deuteronomium": "Deu",
    "joz": "Joz", "jozua": "Joz", "Joz": "Joz", "Jozua": "Joz", "jos": "Joz", "Jos": "Joz",
    "ri": "Ri", "richteren": "Ri", "Ri": "Ri", "Richteren": "Ri", "jdg": "Ri",
    "ru": "Ru", "ruth": "Ru", "Ru": "Ru", "Ruth": "Ru", "rut": "Ru",
    "1sa": "1Sa", "1sam": "1Sa", "1 sam": "1Sa", "1 Sam": "1Sa", "1 Samuel": "1Sa", "1 Samuël": "1Sa",
    "2sa": "2Sa", "2sam": "2Sa", "2 sam": "2Sa", "2 Sam": "2Sa", "2 Samuel": "2Sa", "2 Samuël": "2Sa",
    "1kn": "1Kn", "1 kn": "1Kn", "1 Kn": "1Kn", "1 Koningen": "1Kn", "1 koningen": "1Kn", "1kg": "1Kn",
    "2kn": "2Kn", "2 kn": "2Kn", "2 Kn": "2Kn", "2 Koningen": "2Kn", "2 koningen": "2Kn", "2kg": "2Kn",
    "1kr": "1Kr", "1 kr": "1Kr", "1 Kr": "1Kr", "1 Kronieken": "1Kr", "1 kronieken": "1Kr", "1ch": "1Kr", "1 Kron": "1Kr",
    "2kr": "2Kr", "2 kr": "2Kr", "2 Kr": "2Kr", "2 Kronieken": "2Kr", "2 kronieken": "2Kr", "2ch": "2Kr", "2 Kron": "2Kr",
    "ezr": "Ezr", "ezra": "Ezr", "Ezr": "Ezr", "Ezra": "Ezr",
    "neh": "Neh", "nehemia": "Neh", "Neh": "Neh", "Nehemia": "Neh",
    "est": "Est", "ester": "Est", "esther": "Est", "Est": "Est", "Ester": "Est", "Esther": "Est",
    "job": "Job", "Job": "Job",
    "ps": "Ps", "psalm": "Ps", "psalmen": "Ps", "Ps": "Ps", "Psalm": "Ps", "Psalmen": "Ps", "psa": "Ps",
    "spr": "Spr", "spreuken": "Spr", "Spr": "Spr", "Spreuken": "Spr", "pro": "Spr", "Pro": "Spr",
    "pred": "Pred", "prediker": "Pred", "Pred": "Pred", "Prediker": "Pred", "qoh": "Pred", "Qoh": "Pred",
    "hl": "Hl", "hooglied": "Hl", "Hl": "Hl", "Hooglied": "Hl", "can": "Hl",
    "jes": "Jes", "jesaja": "Jes", "Jes": "Jes", "Jesaja": "Jes", "isa": "Jes",
    "jer": "Jer", "jeremia": "Jer", "Jer": "Jer", "Jeremia": "Jer",
    "klaag": "Klaag", "Klaag": "Klaag", "klaagliederen": "Klaag", "Klaagliederen": "Klaag", "lam": "Klaag",
    "eze": "Eze", "ezechiel": "Eze", "Eze": "Eze", "Ezechiël": "Eze", "Ezechiel": "Eze", "ezek": "Eze",
    "dan": "Dan", "daniel": "Dan", "Dan": "Dan", "Daniel": "Dan", "Daniël": "Dan",
    "hos": "Hos", "hosea": "Hos", "Hos": "Hos", "Hosea": "Hos",
    "joel": "Joël", "joël": "Joël", "Joel": "Joël", "Joël": "Joël", "joe": "Joël",
    "amos": "Amos", "Amos": "Amos", "amo": "Amos",
    "oba": "Oba", "obadja": "Oba", "Oba": "Oba", "Obadja": "Oba",
    "jon": "Jona", "jona": "Jona", "Jon": "Jona", "Jona": "Jona",
    "mi": "Mi", "micha": "Mi", "Mi": "Mi", "Micha": "Mi", "mic": "Mi",
    "nah": "Nah", "nahum": "Nah", "Nah": "Nah", "Nahum": "Nah",
    "hab": "Hab", "habakuk": "Hab", "Hab": "Hab", "Habakuk": "Hab",
    "zef": "Zef", "zefanja": "Zef", "Zef": "Zef", "Zefanja": "Zef", "zep": "Zef",
    "hag": "Hag", "haggai": "Hag", "Hag": "Hag", "Haggai": "Hag",
    "zach": "Zach", "zacharia": "Zach", "Zach": "Zach", "Zacharia": "Zach", "zec": "Zach",
    "mal": "Mal", "maleachi": "Mal", "Mal": "Mal", "Maleachi": "Mal",
    # NT
    "mat": "Mat", "mattheus": "Mat", "mattheüs": "Mat", "Mat": "Mat", "Mattheüs": "Mat", "Mattheus": "Mat",
    "mar": "Mar", "marcus": "Mar", "markus": "Mar", "Mar": "Mar", "Marcus": "Mar", "Markus": "Mar",
    "luk": "Luk", "lukas": "Luk", "Luk": "Luk", "Lukas": "Luk", "luc": "Luk", "Lucas": "Luk",
    "joh": "Joh", "johannes": "Joh", "Joh": "Joh", "Johannes": "Joh",
    "hand": "Hand", "handelingen": "Hand", "Hand": "Hand", "Handelingen": "Hand", "act": "Hand",
    "rom": "Rom", "romeinen": "Rom", "Rom": "Rom", "Romeinen": "Rom",
    "1ko": "1Ko", "1 kor": "1Ko", "1 Kor": "1Ko", "1 korinthe": "1Ko", "1 Korinthe": "1Ko", "1co": "1Ko",
    "2ko": "2Ko", "2 kor": "2Ko", "2 Kor": "2Ko", "2 korinthe": "2Ko", "2 Korinthe": "2Ko", "2co": "2Ko",
    "gal": "Gal", "galaten": "Gal", "Gal": "Gal", "Galaten": "Gal",
    "ef": "Ef", "efeze": "Ef", "Ef": "Ef", "Efeze": "Ef", "eph": "Ef", "Efeziërs": "Ef",
    "fil": "Fil", "filippenzen": "Fil", "Fil": "Fil", "Filippenzen": "Fil", "phi": "Fil",
    "kol": "Kol", "kolossenzen": "Kol", "Kol": "Kol", "Kolossenzen": "Kol", "col": "Kol",
    "1th": "1Th", "1 thes": "1Th", "1 Thessalonicenzen": "1Th",
    "2th": "2Th", "2 thes": "2Th", "2 Thessalonicenzen": "2Th",
    "1ti": "1Ti", "1 tim": "1Ti", "1 Tim": "1Ti", "1 Timoteüs": "1Ti", "1 Timotheüs": "1Ti",
    "2ti": "2Ti", "2 tim": "2Ti", "2 Tim": "2Ti", "2 Timoteüs": "2Ti", "2 Timotheüs": "2Ti",
    "tit": "Tit", "titus": "Tit", "Tit": "Tit", "Titus": "Tit",
    "phm": "Phm", "filemon": "Phm", "Filemon": "Phm",
    "heb": "Heb", "hebr": "Heb", "hebreeen": "Heb", "Heb": "Heb", "Hebr": "Heb", "Hebreeën": "Heb", "Hebreeen": "Heb",
    "jak": "Jak", "jakobus": "Jak", "Jak": "Jak", "Jakobus": "Jak", "jam": "Jak",
    "1pe": "1Pe", "1 pet": "1Pe", "1 Petrus": "1Pe",
    "2pe": "2Pe", "2 pet": "2Pe", "2 Petrus": "2Pe",
    "1jo": "1Jo", "1 joh": "1Jo", "1 Johannes": "1Jo",
    "2jo": "2Jo", "2 joh": "2Jo", "2 Johannes": "2Jo",
    "3jo": "3Jo", "3 joh": "3Jo", "3 Johannes": "3Jo",
    "jud": "Jud", "Judas": "Jud",
    "op": "Op", "openb": "Op", "openbaring": "Op", "Op": "Op", "Openb": "Op", "Openbaring": "Op", "rev": "Op",
}

# Sorteer keys op lengte aflopend zodat "1 Kr" gematcht wordt vóór "1".
SORTED_KEYS = sorted(BOEKEN.keys(), key=lambda x: -len(x))

def make_book_pattern():
    # alternation van afkortingen, gesorteerd op lengte aflopend
    # gebruik woord-grenzen + space-tolerant
    parts = [re.escape(k) for k in SORTED_KEYS]
    return r"(?:" + "|".join(parts) + r")"

BOOK_RE = make_book_pattern()
# patroon: BOOK SP CHAPTER : VERSE [- VERSE2] [, VERSE3]
# we matchen: "Gen 22:4", "Gen 22:4-5", "Gen 22:4, 6"
VERS_PATTERN = re.compile(
    r"\b(" + BOOK_RE + r")\s+(\d+):(\d+)(?:[–-](\d+))?",
    re.IGNORECASE
)
STRONG_PATTERN = re.compile(r"\b([HG]\d{1,5}[a-c]?)\b")

def normalize_ref(book_raw, chap, vs_start, vs_end=None):
    # zoek case-insensitive in BOEKEN
    book = None
    for k, v in BOEKEN.items():
        if k.lower() == book_raw.lower():
            book = v
            break
    if book is None:
        return None
    if vs_end:
        return f"{book} {chap}:{vs_start}-{vs_end}"
    return f"{book} {chap}:{vs_start}"

def extract_refs(text):
    verzen = set()
    for m in VERS_PATTERN.finditer(text):
        ref = normalize_ref(m.group(1), m.group(2), m.group(3), m.group(4))
        if ref:
            verzen.add(ref)
    strongs = set(STRONG_PATTERN.findall(text))
    return verzen, strongs

def main():
    # Relatief pad: script staat in skill/fase10/, base is Kennis/typologie/
    script_dir = Path(__file__).resolve().parent
    base = script_dir.parent.parent / "Kennis" / "typologie"
    vers_idx = defaultdict(list)
    strong_idx = defaultdict(list)
    entry_count = 0
    entries_meta = {}
    for sub in sorted(base.iterdir()):
        if not sub.is_dir():
            continue
        if not sub.name[0].isupper() or "_" not in sub.name:
            continue
        for md in sorted(sub.glob("*.md")):
            rel = f"{sub.name}/{md.name}"
            text = md.read_text(encoding="utf-8", errors="replace")
            verzen, strongs = extract_refs(text)
            entry_count += 1
            entries_meta[rel] = {
                "verzen_count": len(verzen),
                "strongs_count": len(strongs),
            }
            for v in verzen:
                vers_idx[v].append(rel)
            for s in strongs:
                strong_idx[s].append(rel)
    out = {
        "stats": {
            "total_entries": entry_count,
            "total_unique_verzen": len(vers_idx),
            "total_unique_strongs": len(strong_idx),
        },
        "entries": entries_meta,
        "verzen": {k: sorted(set(v)) for k, v in sorted(vers_idx.items())},
        "strongs": {k: sorted(set(v)) for k, v in sorted(strong_idx.items())},
    }
    out_path = base / "_index.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Geschreven: {out_path}")
    print(f"  entries: {entry_count}")
    print(f"  unieke verzen: {len(vers_idx)}")
    print(f"  unieke Strong-codes: {len(strong_idx)}")

if __name__ == "__main__":
    main()
