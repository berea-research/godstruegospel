# Fase 10 web-integratie — deliverables

> Voltooid op 2026-05-08 als Optie 5 binnen GTG typologie-laag-traject.
> Doel: indexen + cross-references + dataset-onderhoud over alle 126 voltooide entries.

## Bestanden geleverd

| Bestand | Doel |
|---|---|
| `_index.json` | Reverse-lookup vers → entries + Strong → entries + entry-meta. Machine-leesbaar. |
| `_xref_check.md` | Cross-reference rapport: gebroken links, asymmetrische refs, top-gerefereerde entries, eilanden. |
| `_dataset-onderhoud-psalmen.md` | Psalmen-tagging-issue + andere dataset-onderhouds-issues voor toekomstige sessie. |
| `_fase10-deliverables.md` | Dit overzichtsdocument. |
| `../skill/fase10/build_index.py` | Python-script voor `_index.json` (herproduceerbaar). |
| `../skill/fase10/check_xrefs.py` | Python-script voor cross-reference check (herproduceerbaar). |

## Statistiek typologie-laag (per 2026-05-08)

| Fase | Map | Aantal | V2-status |
|---|---|---|---|
| 1 | B_cijfer | 13 | bron-geverifieerd 2026-05-08 |
| 2 | C_tijd | 16 | bron-geverifieerd 2026-05-05/06 |
| 3 | A_entiteit personen | 25 | bron-geverifieerd 2026-05-07 |
| 4 | A_entiteit overig | 49 | bron-geverifieerd 2026-05-07/08 |
| 5 | D_taal | 8 | pilot 2026-05-05 (V1-sjabloon, V2-herziening aanbevolen) |
| 6 | E_structuur | 15 | bron-geverifieerd 2026-05-05/08 |
| **Totaal** | | **126** | 118 V2-strict + 8 V1 (D_taal) |

## Index.json statistieken

- Totaal entries: 126
- Unieke vers-references: 1771
- Unieke Strong-codes: 1987
- Top-gerefereerde verzen: Heb 4:9 (9×), Gen 1:2 / 22:4 / Hos 6:2 (elk 6×), Gen 2:2 / Heb 11:19 / Mat 12:40 / Op 5:6 (elk 5×)
- Top Strong-codes: H3068 (JHWH-tetragrammaton, 49 entries), H3117 (yom — dag, 34×), H430 (elohim, 34×), H776 (eretz — aarde, 33×), H1121a (ben — zoon, 28×), H7651 (sheva — zeven, 22×)

## Cross-reference statistieken

- Totaal cross-references tussen entries: 222
- Gebroken links: 55
  - 54 verwijzingen naar **toekomstige entries** (Fase 7-9 + uitbreidingen) — bewust opgenomen voor latere realisatie
  - 1 echte fout: `D_taal/hapax-overzicht.md → A_entiteit/8.md` (gecorrigeerd naar `B_cijfer/8.md`)
- Asymmetrische refs: 138 (A→B zonder B→A; normaal voor hub-entries zoals B_cijfer/3.md)
- Entries zonder inkomende refs (eilanden): 76 (60% van totaal)
- Top-15 meest-gerefereerde entries: B_cijfer/3.md (22×), 7.md (20×), 12.md (14×), 40.md (13×), C_tijd/derde-dag.md (9×), B_cijfer/8.md (6×), C_tijd/profetisch-tijden-en-tijden.md (5×)

## Negatieve-patronen sweep — uitkomsten

### Gefixte items
- `B_cijfer/40.md` — vervangen "typologische drie-eenheid" (4×) door "typologische drie-groep" om verwarring met theologisch begrip te voorkomen
- `B_cijfer/3.md` — vervangen "drie-eenheid van pneuma + water + bloed" door "drievoud van pneuma + water + bloed"
- `D_taal/hapax-overzicht.md` — gebroken cross-ref `A_entiteit/8.md` gecorrigeerd naar `B_cijfer/8.md`

### Acceptabel binnen typologie-discipline
- "specific-doctrinal-position" — only as an anti-pattern in `_raamwerk.md`
- "calvinistisch" — in `E_structuur/staircase-parallellisme.md` waarschuwing tegen Calvinistische TULIP-uitleg (correct gebruik)
- "Hieronymus" + "Plinius" — in `B_cijfer/153.md` waarschuwing als buitenbijbels (correct gebruik)
- "midrasj" — in `C_tijd/dagen-vierde.md` als anti-patroon ("Geen midrasj-input"; correct gebruik)
- "kerkvader" — alleen in `_entry-sjabloon.md` en `_raamwerk.md` als anti-patroon
- "Drie-eenheid"/"drie-eenheid" — in `B_cijfer/153.md` (buitenbijbels), `A_entiteit/kandelaar.md` (N3-clue gemarkeerd) — acceptabel

### Bewust niet gefixed
- "eeuwig" / "eeuwigheid" — gebruikt als gangbare NL-vertaling van `olam` / `aiōn` / `aiōnios` in vers-citaten waar transliteratie + Strong-code er ook bij staat. Acceptabel binnen typologie-laag (deze laag claimt geen vertalings-discipline; zie `concordant-agent` skill voor concordant-vertaal-laag).
- "Heilige Geest" — in `A_entiteit/jona.md` (Mat 3:16-referentie naar duif-Geest, N3-clue gemarkeerd) en `D_taal/wortel-rua.md` (vers-citaat-vertaling). Acceptabel mits niet typologisch geclaimd.

## D_taal V1 → V2 herziening aanbevolen (toekomstig)

Alle 8 D_taal entries volgen V1-sjabloon van 2026-05-05. Voor compleetheid van Fase 10 web-integratie wordt aanbevolen om een eigen V2-herzieningsronde uit te voeren parallel aan de Fase 1 cijfer-herzieningsronde van 2026-05-08. Niet onderdeel van huidige Optie 5 Fase 10 — voorgesteld als toekomstige Optie 5b.

| Entry | Datum | Sjabloon |
|---|---|---|
| D_taal/gematria-inventaris.md | 2026-05-05 | V1 |
| D_taal/hapax-overzicht.md | 2026-05-05 | V1 |
| D_taal/paronomasie-dabar-devash.md | 2026-05-05 | V1 |
| D_taal/paronomasie-shalom-shalem.md | 2026-05-05 | V1 |
| D_taal/polysemie-elohim.md | 2026-05-05 | V1 |
| D_taal/wortel-chesed.md | 2026-05-05 | V1 |
| D_taal/wortel-rua.md | 2026-05-05 | V1 |
| D_taal/wortel-tsedek.md | 2026-05-05 | V1 |

## Vervolg-werk in raamwerk

- **Fase 7 verhaal-typologie** (F_verhaal): 0 entries — leeg, te starten
- **Fase 8 rol-typologie** (G_rol): 0 entries — leeg, te starten
- **Fase 9 contrast-typologie** (H_contrast): 0 entries — leeg, te starten

54 toekomstige cross-references naar Fase 7-9 + uitbreidingen staan klaar in bestaande entries — wanneer deze fasen ingevuld worden, zullen veel `[N3-clue]`-vooruitwijzingen automatisch in N1-typologische bridges veranderen.

## Reproduceerbaarheid

Beide scripts (`build_index.py`, `check_xrefs.py`) staan in `skill/fase10/` en kunnen herhaald worden uitgevoerd om geüpdatete `_index.json` en `_xref_check.md` te produceren wanneer entries worden toegevoegd of gewijzigd.

```bash
cd <repo-root>/skill/fase10
python3 build_index.py    # → _index.json
python3 check_xrefs.py    # → _xref_check.md
```
