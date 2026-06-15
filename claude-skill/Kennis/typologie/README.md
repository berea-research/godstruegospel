# Typologie — patroon-laag van de godstruegospel skill

Deze map bevat de typologie-kennislaag. Patronen die de Schrift zelf legt door consistent woord-, cijfer-, naam-, plaats-, dag- of structuurgebruik worden hier verankerd, uitsluitend op basis van directe grondtekst-evidentie uit de 70 boeken in `Kennis/puur/` en `Kennis/strong/`.

## Architectuur-bestanden

| Bestand | Doel |
|---|---|
| `_raamwerk.md` | Het volledige raamwerk V2 met drie assen (categorie, hermeneutische laag, zekerheids-niveau), operationele modi, anti-patronen, oplettende-lezer-presumptie, sola-scriptura discipline. |
| `_entry-sjabloon.md` | Verplichte structuur voor elke entry. Geen entry zonder dit sjabloon. |
| `_actieplan.md` | Fase-overzicht met patroon-kandidaten per fase. |
| `README.md` | Dit bestand. |
| `_index.json` | Fase 10 reverse-lookup vers → entries + Strong → entries (machine-leesbaar). |
| `_xref_check.md` | Fase 10 cross-reference rapport. |
| `_dataset-onderhoud-psalmen.md` | Fase 10 inventarisatie van Psalmen-tagging-issues. |
| `_fase10-deliverables.md` | Fase 10 web-integratie samenvatting. |

## Submappen — hoofdcategorieën uit raamwerk V2

De acht hoofdcategorieën uit het raamwerk corresponderen 1:1 met deze submappen.

| Map | Hoofdcategorie | Subsoorten (uit raamwerk) |
|---|---|---|
| `A_entiteit/` | Entiteit-typologie | A1 personen-rol, A2 vrouwen, A3 negatieve typen, A4-A6 plaatsen, A7 voorwerpen, A8 dieren, A9 planten, A10 materialen, A11 kleuren, A12 lichaamsdelen |
| `B_cijfer/` | Patroon-typologie numeriek | B1 cijfers expliciet, B2 cijfers impliciet (optellingen), B3 cijfer-vermenigvuldiging, B4 cijfer-structuur in compositie |
| `C_tijd/` | Tijd-typologie | C1 dagen, C2 jaren, C3 cycli, C4 profetische perioden |
| `D_taal/` | Taal-typologie | D1 woordklank-paronomasie, D2 wortel-verbindingen, D3 hapax legomena, D4 gematria, D5 polysemie |
| `E_structuur/` | Structuur-typologie | E1 chiasme, E2 parallellismen, E3 inclusio, E4 tabernakel, E5 feest-cyclus |
| `F_verhaal/` | Verhaal-typologie | F1 opdracht-vervulling, F2-F3 profetie-vervulling, F4 eerstgeborene-omkering, F5 drievoudige herhaling, F6 reis-en-terugkeer, F7 verschijning-aan-verlatene |
| `G_rol/` | Rol-typologie | G1 drie ambten, G2 vader-zoon, G3 broer-broer, G4 bruidegom-bruid, G5 herder-schaap, G6 knecht-heer |
| `H_contrast/` | Contrast-typologie | H1 eerste-laatste Adam, H2-H3 twee bergen/steden, H4 twee verbonden, H5 twee wegen, H6 twee vrouwen Op, H7 oude/nieuwe schepping |

Een entry kan via tags meerdere hoofdcategorieën dragen (cross-categorie web-structuur). De submap waar het bestand fysiek staat is de **primaire** categorie; verdere categorieën zijn secundair en worden in het meta-veld `As 1 (categorieën)` vermeld.

## Open uitbreiding

Wanneer een patroon-onderzoek een verbinding blootlegt die in geen van A-H past, wordt een nieuwe hoofdcategorie geopend (`I_*`, `J_*`, `K_*`) in plaats van de bevinding in een verkeerde categorie te persen. Het raamwerk wordt dan bijgewerkt.

## Negatieve patronen

Afwezigheids-patronen (wat er NIET staat) zijn sub-categorieën binnen elke relevante hoofdcategorie. Markering: `negatief` tag in de meta van de entry. Behandeling: clue, geen bewijs.

## Status van de inhoudelijke entries

| Map | Bestanden | Status |
|---|---|---|
| `A_entiteit/` | 74 entries: Fase 3 (25 personen) + Fase 4 (49 plaatsen-voorwerpen-dieren-planten-materialen-kleuren-lichaamsdelen) | alle pilot, sjabloon V2 bron-geverifieerd 2026-05-07/08 — Fase 3 + Fase 4 **VOLLEDIG VOLTOOID** |
| `B_cijfer/` | 13 entries: `3.md`, `7.md`, `8.md`, `10.md`, `12.md`, `40.md`, `50.md`, `70.md`, `120.md`, `144.md`, `153.md`, `666.md`, `1000.md` | alle pilot, sjabloon V2 bron-geverifieerd 2026-05-08 — Fase 1 **VOLLEDIG VOLTOOID** |
| `C_tijd/` | 16 entries: `derde-dag.md` + 7 dagen-entries + 3 jaren-entries + 3 cycli-entries + 2 profetisch-entries | alle pilot, sjabloon V2 bron-geverifieerd 2026-05-05/06 — Fase 2 **VOLLEDIG VOLTOOID** |
| `D_taal/` | 8 entries (paronomasie-dabar-devash, paronomasie-shalom-shalem, wortel-chesed, wortel-tsedek, wortel-rua, hapax-overzicht, gematria-inventaris, polysemie-elohim) | alle pilot, V1-sjabloon 2026-05-05 — Fase 5 inhoudelijk VOLTOOID maar **V2-herziening aanbevolen** voor strikte bron-verificatie-discipline |
| `E_structuur/` | 15 entries (chiasme-ester, chiasme-onze-vader, chiasme-leviticus-19, parallellismen-psalmen, inclusio-mattheus, inclusio-genesis-openbaring, tabernakel-hemels-patroon, feest-cyclus-heilshistorie + Fase 6 uitbreiding 7×: acrostichon-alefbet, refrein-chesed-ps136, getals-formule-x-en-x-plus-1, chiasme-narratief-jona, inclusio-johannes-romeinen, staircase-parallellisme, zevenvoudige-opbouw) | alle pilot, sjabloon V2 — Fase 6 VOLTOOID + UITGEBREID |
| `F_verhaal/` | 17 entries: opdracht-vervulling (ark + tempel) + profetie-vervulling (bethlehem + cyrus) + profetie-meervoudig (jes-7-14 + joel-2) + eerstgeborene-omkering + drievoudige-herhaling (petrus + bileam + samuel) + reis-en-terugkeer (jakob + jozef + jezus) + verschijning-aan-verlatene (hagar + jakob + mozes + maria) | alle pilot, sjabloon V2 bron-geverifieerd 2026-05-08 — Fase 7 **VOLLEDIG VOLTOOID** |
| `G_rol/` | 15 entries: drie-ambten (profeet + priester + koning + samenval) + vader-zoon (abraham-isaak + david-salomo) + broer-broer (kain-abel + ezau-jakob + jozef-elf) + bruidegom-bruid (jhwh-israel + christus-gemeente) + herder-schaap + knecht-heer (eliezer + mozes + christus) | alle pilot, sjabloon V2 bron-geverifieerd 2026-05-08 — Fase 8 **VOLLEDIG VOLTOOID** |
| `H_contrast/` | 12 entries: `eerste-laatste-adam.md`, `twee-bergen-sinai-sion.md`, `twee-bergen-gerizim-ebal.md`, `twee-steden-babel-jeruzalem.md`, `twee-steden-sodom-jeruzalem.md`, `twee-verbonden-hagar-sara.md`, `twee-verbonden-oud-nieuw.md`, `twee-wegen-smal-breed.md`, `twee-wegen-leven-dood.md`, `twee-wegen-wijs-dwaas.md`, `twee-vrouwen-op12-op17.md`, `oude-nieuwe-schepping.md` | alle pilot, sjabloon V2 bron-geverifieerd 2026-05-08 — Fase 9 **VOLLEDIG VOLTOOID** |
| **TOTAAL** | **170 entries** | Fase 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 voltooid (2026-05-08); Fase 10 web-integratie voltooid (2026-05-08) — herziening aanbevolen na Fase 9 toevoegingen om _index.json + _xref_check.md te updaten met de twaalf nieuwe H_contrast-entries |

## Fase 10 deliverables (2026-05-08)

Web-integratie geleverd:
- `_index.json` — reverse-lookup over 1771 vers-references + 1987 Strong-codes
- `_xref_check.md` — cross-reference rapport (222 links totaal, 54 bewuste vooruitwijzingen naar Fase 7-9, 1 echte fout gefixed)
- `_dataset-onderhoud-psalmen.md` — Psalmen-tagging-issues voor toekomstige onderhoudssessie
- `_fase10-deliverables.md` — overzichtsdocument
- Negatieve-patronen sweep uitgevoerd: theologische school-termen gecontroleerd, "drie-eenheid" → "drie-groep" / "drievoud" gefixed in 40.md + 3.md, "Drie-eenheid" + "kerkvader"-discipline behouden.

> **Update 2026-06-15 — 0%-theologie-zuivering.** Een strengere zuivering is uitgevoerd over alle acht categorieën: élke geleende doctrine/duiding (Triniteit, avondmaal-sacramentalisme, substitutie-leer, pre-existentie/pre-incarnatie-christologie, dispensationalisme, eschatologie-scholen, kerkvaders/commentatoren/rabbijnse traditie) is verwijderd, ook als N3-clue. Tekst-feiten blijven. De eerdere "acceptabel"-oordelen hieronder zijn hierdoor achterhaald. Zie `_zuivering-voortgang.md` voor het volledige logboek.

Reproduceerbare scripts: `../skill/fase10/bui