#!/usr/bin/env python3
"""
Cross-reference check: scan alle entries op `./*.md` en `../*.md` links,
controleer of ze bestaan, en rapporteer gebroken links + ontbrekende
bidirectionele references.
"""
import os
import re
from pathlib import Path
from collections import defaultdict

# Relatief pad: script staat in skill/fase10/, base is Kennis/typologie/
_SCRIPT_DIR = Path(__file__).resolve().parent
BASE = _SCRIPT_DIR.parent.parent / "Kennis" / "typologie"
LINK_PATTERN = re.compile(r"`(\.\.?/[A-H]_[a-z]+/[A-Za-z0-9_\-\.]+\.md)`")

def main():
    # Verzamel alle bestaande entries (canonical relpath)
    existing = set()
    for sub in sorted(BASE.iterdir()):
        if not sub.is_dir():
            continue
        if not sub.name[0].isupper() or "_" not in sub.name:
            continue
        for md in sub.glob("*.md"):
            existing.add(f"{sub.name}/{md.name}")
    
    # Voor elke entry: extraheer alle ./*.md / ../*.md links
    refs_from = defaultdict(set)  # entry -> set of refs
    refs_to = defaultdict(set)    # entry -> set of entries die naar mij verwijzen
    broken = []
    
    for sub in sorted(BASE.iterdir()):
        if not sub.is_dir():
            continue
        if not sub.name[0].isupper() or "_" not in sub.name:
            continue
        for md in sorted(sub.glob("*.md")):
            rel_self = f"{sub.name}/{md.name}"
            text = md.read_text(encoding="utf-8", errors="replace")
            for m in LINK_PATTERN.finditer(text):
                link = m.group(1)
                # resolveer relatief
                if link.startswith("./"):
                    target = f"{sub.name}/{link[2:]}"
                elif link.startswith("../"):
                    target = link[3:]  # ../X_iets/y.md -> X_iets/y.md
                else:
                    continue
                # Verwijder fragment-anchors zoals .md#cluster-A
                target_clean = target.split("#")[0]
                refs_from[rel_self].add(target_clean)
                if target_clean not in existing:
                    broken.append((rel_self, link, target_clean))
                else:
                    refs_to[target_clean].add(rel_self)
    
    print(f"Totaal entries: {len(existing)}")
    print(f"Totaal links: {sum(len(v) for v in refs_from.values())}")
    print(f"Gebroken links: {len(broken)}")
    print()
    if broken:
        print("=== GEBROKEN LINKS (eerste 30) ===")
        for src, link, tgt in broken[:30]:
            print(f"  {src} → {link} (target: {tgt})")
    print()
    # Asymmetrie: A verwijst naar B, B verwijst niet terug naar A
    asym = []
    for entry, refs in refs_from.items():
        for r in refs:
            if r == entry:
                continue
            if r in existing:
                if entry not in refs_from.get(r, set()):
                    asym.append((entry, r))
    print(f"Asymmetrische cross-references: {len(asym)}")
    print("(A verwijst naar B, B niet terug naar A — niet altijd verkeerd, maar handig om te zien)")
    print()
    # Top-10 meest-gerefereerde entries (inkomende links)
    top_in = sorted(refs_to.items(), key=lambda x: -len(x[1]))[:15]
    print("=== Top-15 meest-gerefereerde entries ===")
    for entry, srcs in top_in:
        print(f"  {entry}: {len(srcs)} inkomende refs")
    print()
    # Entries zonder inkomende links (eilanden)
    no_in = [e for e in existing if e not in refs_to]
    print(f"=== Entries zonder inkomende cross-references: {len(no_in)} ===")
    for e in sorted(no_in)[:20]:
        print(f"  {e}")
    
    # Schrijf output naar bestand
    out_lines = []
    out_lines.append(f"# Fase 10 cross-reference check — {len(existing)} entries\n\n")
    out_lines.append(f"## Statistiek\n\n")
    out_lines.append(f"- Totaal entries: {len(existing)}\n")
    out_lines.append(f"- Totaal cross-reference links: {sum(len(v) for v in refs_from.values())}\n")
    out_lines.append(f"- Gebroken links: {len(broken)}\n")
    out_lines.append(f"- Asymmetrische refs: {len(asym)}\n")
    out_lines.append(f"- Entries zonder inkomende refs: {len(no_in)}\n\n")
    if broken:
        out_lines.append(f"## Gebroken links ({len(broken)})\n\n")
        for src, link, tgt in broken:
            out_lines.append(f"- `{src}` → `{link}` (target: `{tgt}`)\n")
    out_lines.append(f"\n## Top-15 meest-gerefereerde entries\n\n")
    for entry, srcs in top_in:
        out_lines.append(f"- `{entry}`: {len(srcs)} inkomende refs\n")
    out_lines.append(f"\n## Entries zonder inkomende cross-references ({len(no_in)})\n\n")
    for e in sorted(no_in):
        out_lines.append(f"- `{e}`\n")
    
    out_path = BASE / "_xref_check.md"
    with out_path.open("w", encoding="utf-8") as f:
        f.writelines(out_lines)
    print(f"\nVolledig rapport: {out_path}")

if __name__ == "__main__":
    main()
