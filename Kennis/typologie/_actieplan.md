# Actieplan — typologie-laag inkleuren

Status: actieplan, opgesteld 2026-05-02. Het raamwerk staat (V2). De architectuur staat. De pilot-entries voor `B_cijfer/120.md` en `C_tijd/derde-dag.md` staan. Dit document beschrijft hoe we het raamwerk verder vol-bouwen, in tien afroepbare fasen.

## Uitgangspunten

Iedere fase volgt dezelfde discipline:
- Sola scriptura, alleen `Kennis/puur/` en `Kennis/strong/` (70 boeken).
- Bron-zoek via `skill/typologie_zoek.py`, geen geheugen-input.
- Zeven werkstappen uit `protocollen/typologie-detectie.md`.
- Sjabloon V2 uit `_entry-sjabloon.md`.
- Twee-getuigen drempel.
- Oplettende-lezer-presumptie: aanwijsbare verbanden tellen volwaardig mee.
- Strong-codes alleen in zoekquery-blok, niet als typologie-element.
- Per nieuwe entry: cross-references in bestaande entries waar relevant.

Iedere fase resulteert in:
- Een set nieuwe entries in de juiste submap.
- Updates aan README.md status-tabel.
- Updates aan `skill/skill_v5_preflight.py` TYPOLOGIE_TRIGGERS waar de nieuwe entries automatische detectie verdienen.
- Vermelding van openstaande vervolgvragen die naar latere fasen kunnen.

## Tien fasen

### Fase 1 — Cijfer-typologie compleet

**Submap:** `B_cijfer/`
**Skill:** `/gtg-fase1-cijfers`
**Doel:** alle bijbels significante cijfers verankeren als entries.

**Patroon-kandidaten (in voorgestelde volgorde):**
1. `3.md` — drievoud, drie dagen, drie getuigen, goddelijke compleetheid
2. `7.md` — sabbatisch, scheppingsdag, volheid, oordeel-cyclus
3. `8.md` — nieuw begin, achtste dag, besnijdenis, opstanding-na-sabbat
4. `10.md` — wettelijke compleetheid (geboden, plagen, tienden)
5. `12.md` — bestuurlijke compleetheid (stammen, apostelen, poorten)
6. `40.md` — beproeving (vloed, woestijn, vasten, regering)
7. `50.md` — jubel, Pinksterdag-pendant
8. `70.md` — nationale compleetheid (volken, oudsten, ballingschap, jaarweken)
9. `144.md` — 12 × 12, Openbaring 7 en 14
10. `153.md` — vissen Joh 21
11. `666.md` — mens-getal Op 13
12. `1000.md` — millennium, "duizend jaren" Op 20

**Geschat aantal entries:** 12.
**Geschat per sessie:** 1 entry. Twaalf sessies voor de hele fase.

### Fase 2 — Tijd-typologie compleet

**Submap:** `C_tijd/`
**Skill:** `/gtg-fase2-tijd`
**Doel:** alle dagen, jaren, cycli en profetische perioden verankeren.

**Patroon-kandidaten:**
1. `dagen-eerste.md` — schepping dag 1, licht, eerste dag week (opstanding)
2. `dagen-tweede.md` — wateren scheiden, bijzondere structuur
3. `dagen-vierde.md` — lichten in de hemel
4. `dagen-vijfde.md` — leven in wateren en hemelen
5. `dagen-zesde.md` — mens als heerser
6. `dagen-zevende.md` — sabbat
7. `dagen-achtste.md` — nieuw begin (al benoemd in raamwerk)
8. `jaren-veertig.md` — vloed-dagen-jaren, woestijn, Mozes-fasen, regering, vasten
9. `jaren-vijftig.md` — jubel, Pinksterdag jaartelling
10. `jaren-zeventig.md` — verwoesting, jaarweken
11. `cycli-sabbat.md` — Lev 23, Lev 25
12. `cycli-jubel.md` — 7×7+1, Lev 25
13. `cycli-feesten.md` — drie pelgrimsfeesten als heilshistorie
14. `profetisch-zeventig-weken.md` — Daniël 9
15. `profetisch-tijden-en-tijden.md` — Daniël 7, Op 12

**Geschat aantal:** 15.

### Fase 3 — Entiteit-typologie personen

**Submap:** `A_entiteit/`
**Skill:** `/gtg-fase3-personen`
**Doel:** christustypen, vrouwen-typologie en negatieve typen.

**Christustypen (A1):**
1. `adam.md` (1 Kor 15:45 expliciet)
2. `noach.md` (rechtvaardige bewaarder door oordeel)
3. `abraham.md` (vader des geloofs)
4. `isaak.md` (offer van geliefde zoon)
5. `jakob.md` (worsteling, naam-verandering)
6. `jozef.md` (verworpen-verheven, redt zijn broers)
7. `mozes.md` (bemiddelaar, profeet als Mij)
8. `jozua.md` (Yehoshua, brengt naar het land)
9. `boaz.md` (losser van Ruth)
10. `david.md` (koning naar Gods hart, Psalm 22)
11. `salomo.md` (koning van vrede, tempel-bouwer)
12. `elia.md` (komt eerst om de weg te bereiden)
13. `elisa.md` (dubbele portie, dubbel aantal wonderen)
14. `jona.md` (drie dagen)
15. `simson.md` (kracht, sterft door vijanden gedragen)
16. `gideon.md` (kleine groep, verborgen redder)
17. `melchizedek.md` (priester-koning, Hebr 7)

**Vrouwen-typologie (A2):**
18. `eva.md` (moeder van levenden, type bruid)
19. `sara-hagar.md` (twee verbonden, Gal 4)
20. `rachab.md` (heiden in geslachtslijn)
21. `ruth.md` (heidens-bruid)
22. `hannah-maria.md` (lofzang-parallel)

**Negatieve typen (A3):**
23. `kain.md` (1 Joh 3:12)
24. `bileam.md` (2 Pet 2:15)
25. `korach.md` (Jud 11)

**Geschat aantal:** 25.

### Fase 4 — Entiteit-typologie plaatsen, voorwerpen, dieren, planten, materialen, kleuren

**Submap:** `A_entiteit/`
**Skill:** `/gtg-fase4-plaatsen-objecten`
**Doel:** alle niet-persoon entiteit-typologie.

**Plaatsen-bergen (A4):**
1. `berg-sinai.md`, `berg-sion.md`, `berg-karmel.md`, `berg-tabor.md`, `berg-moria.md`, `berg-olijfberg.md`

**Plaatsen-water (A5):**
7. `water-rode-zee.md`, `water-jordaan.md`, `water-genesareth.md`, `water-eufraat.md`

**Plaatsen-steden (A6):**
11. `stad-jeruzalem.md`, `stad-babel.md`, `stad-bethlehem.md`, `stad-ninevé.md`, `stad-egypte.md`

**Voorwerpen (A7):**
16. `ark.md`, `manna.md`, `koperen-slang.md`, `toonbrood.md`, `kandelaar.md`, `wierookaltaar.md`

**Dieren (A8):**
22. `lam.md`, `leeuw.md`, `slang.md`, `duif.md`, `vis.md`, `adelaar.md`

**Bomen en planten (A9):**
28. `boom-des-levens.md`, `vijgenboom.md`, `wijnstok.md`, `olijfboom.md`, `hyssop.md`, `mosterdzaad.md`

**Materialen (A10):**
34. `goud.md`, `zilver.md`, `koper.md`, `hout.md`, `linnen.md`, `geitenhaar.md`

**Kleuren (A11):**
40. `blauw.md`, `purper.md`, `scharlaken.md`, `wit.md`

**Lichaamsdelen en handelingen (A12):**
44. `voet.md`, `hand.md`, `oog.md`, `oor.md`, `knielen.md`, `kussen.md`

**Geschat aantal:** 49. Mogelijk te splitsen over twee skill-aanroepen (4a en 4b).

### Fase 5 — Taal-typologie compleet

**Submap:** `D_taal/`
**Skill:** `/gtg-fase5-taal`
**Doel:** woordklank-paronomasie, wortel-verbindingen, hapax legomena, gematria, polysemie.

**Patroon-kandidaten (initiële inventaris, te verbreden tijdens onderzoek):**
1. `paronomasie-dabar-devash.md` — woord en honing (Ps 19:11, Ps 119:103)
2. `paronomasie-shalom-shalem.md` — vrede en Salem (Jeruzalem)
3. `wortel-chesed.md` — verbond-trouw door de hele Schrift
4. `wortel-tsedek.md` — gerechtigheid recurrent
5. `wortel-rua.md` — adem, geest, wind (ruach)
6. `hapax-overzicht.md` — methodologie voor hapax-zoeken
7. `gematria-inventaris.md` — alleen waar de tekst zelf signaal geeft (zoals Op 13:18)
8. `polysemie-elohim.md` — meervoud van majesteit, rechters, God

**Geschat aantal:** 8 in eerste ronde, uitbreidbaar.

### Fase 6 — Structuur-typologie compleet

**Submap:** `E_structuur/`
**Skill:** `/gtg-fase6-structuur`
**Doel:** chiasme, parallellismen, inclusio, tabernakel, feest-cyclus.

**Patroon-kandidaten:**
1. `chiasme-ester.md` — boek Ester als geheel
2. `chiasme-onze-vader.md` — Mat 6:9-13
3. `chiasme-leviticus-19.md` — middenvers Lev 19:18 over naasten-liefde
4. `parallellismen-psalmen.md` — drie soorten (synoniem, antithetisch, synthetisch)
5. `inclusio-mattheus.md` — Emmanuel begin en eind (Mat 1:23 + 28:20)
6. `inclusio-genesis-openbaring.md` — hemel en aarde, paradijs
7. `tabernakel-hemels-patroon.md` — Hebr 8:5
8. `feest-cyclus-heilshistorie.md` — Lev 23 als typologie

**Geschat aantal:** 8.

### Fase 7 — Verhaal-typologie compleet

**Submap:** `F_verhaal/`
**Skill:** `/gtg-fase7-verhaal`
**Doel:** narratieve patronen.

**Patroon-kandidaten:**
1. `opdracht-vervulling-ark.md` — Noach
2. `opdracht-vervulling-tempel.md` — David ontvangt blueprint, Salomo bouwt
3. `profetie-vervulling-cyrus.md` — Jes 44:28
4. `profetie-vervulling-bethlehem.md` — Mi 5:2
5. `profetie-meervoudig-jes-7-14.md` — Achaz én Christus
6. `profetie-meervoudig-joel-2.md` — vroege regen én Pinksteren
7. `eerstgeborene-omkering.md` — Kaïn-Abel, Ezau-Jakob, Manasse-Efraim, Adonia-Salomo
8. `drievoudige-herhaling-petrus.md` — 3× verloochening / 3× herstel
9. `drievoudige-herhaling-bileam.md` — ezel 3× geslagen
10. `drievoudige-herhaling-samuel.md` — 3× geroepen
11. `reis-en-terugkeer-jakob.md` — naar Laban en terug
12. `reis-en-terugkeer-jozef.md` — Egypte en gebeente terug
13. `reis-en-terugkeer-jezus.md` — Egypte en terug, en grotere parallel
14. `verschijning-aan-verlatene-hagar.md` — Gen 16, 21
15. `verschijning-aan-verlatene-jakob.md` — Bethel
16. `verschijning-aan-verlatene-mozes.md` — braamstruik
17. `verschijning-aan-verlatene-maria.md` — opstandingsmorgen

**Geschat aantal:** 17.

### Fase 8 — Rol-typologie compleet

**Submap:** `G_rol/`
**Skill:** `/gtg-fase8-rol`
**Doel:** drie ambten en relaties.

**Patroon-kandidaten:**
1. `drie-ambten-profeet.md` — Mozes-Christus
2. `drie-ambten-priester.md` — Aäron-Christus, Hebr 5-7
3. `drie-ambten-koning.md` — David-Christus
4. `drie-ambten-samenval.md` — Christus als enige in alle drie
5. `vader-zoon-abraham-isaak.md` — offer-typologie
6. `vader-zoon-david-salomo.md` — opvolging
7. `vader-zoon-god-zoon.md` — bovenliggend patroon
8. `broer-broer-kain-abel.md`
9. `broer-broer-ezau-jakob.md`
10. `broer-broer-jozef-elf.md`
11. `broer-broer-mozes-aaron.md`
12. `bruidegom-bruid-jhwh-israel.md` — Hos 2, Jer 2
13. `bruidegom-bruid-christus-gemeente.md` — Ef 5, Op 19
14. `herder-schaap.md` — David, Ps 23, Eze 34, Joh 10
15. `knecht-heer-eliezer.md` — Gen 24, Geest-typologie
16. `knecht-heer-mozes.md` — knecht des HEREN
17. `knecht-heer-christus.md` — Jes 53, Fil 2

**Geschat aantal:** 17.

### Fase 9 — Contrast-typologie compleet

**Submap:** `H_contrast/`
**Skill:** `/gtg-fase9-contrast`
**Doel:** binaire opposities.

**Patroon-kandidaten:**
1. `eerste-laatste-adam.md` — 1 Kor 15:45-49, Rom 5:12-21
2. `twee-bergen-sinai-sion.md` — Hebr 12:18-22
3. `twee-bergen-gerizim-ebal.md` — zegen-vloek
4. `twee-steden-babel-jeruzalem.md` — Op 17-21
5. `twee-steden-sodom-jeruzalem.md` — Ez 16
6. `twee-verbonden-hagar-sara.md` — Gal 4:21-31
7. `twee-verbonden-oud-nieuw.md` — Hebr 8
8. `twee-wegen-smal-breed.md` — Mat 7
9. `twee-wegen-leven-dood.md` — Deu 30
10. `twee-wegen-wijs-dwaas.md` — Spreuken
11. `twee-vrouwen-op12-op17.md` — vrouw met zon vs hoer Babylon
12. `oude-nieuwe-schepping.md` — Gen 1 + Op 21

**Geschat aantal:** 12.

### Fase 10 — Web, index, cross-check, negatieve patronen

**Skill:** `/gtg-fase10-web`
**Doel:** integratie en consistentie van alle voorgaande fasen.

**Werkzaamheden:**
1. `_index.json` bouwen met reverse-lookup vers → entries
2. Cross-references in alle entries valideren en aanvullen
3. Conflicten tussen entries identificeren en arbitreren
4. Negatieve patronen sweep — door alle bestaande entries kijken naar afwezigheids-patronen die als sub-categorie kunnen worden toegevoegd
5. README.md status-tabel volledig bijwerken
6. Open-uitbreiding categorieën (I, J, K) en lagen (L5+) reserveren waar onderzoek erom vroeg
7. `skill/typologie_zoek.py` definitieve uitbreidingen (vorm-samen-cijfer filter, wortel-vergelijking voor woordklank, gematria-helper)

## Totaal-overzicht

| Fase | Submap | Skill | Patronen | Status |
|---|---|---|---|---|
| 1 | B_cijfer | `/gtg-fase1-cijfers` | 13 (13 al = 120, 3, 7, 8, 10, 12, 40, 50, 70, 144, 153, 666, 1000) | **VOLTOOID 13/13** |
| 2 | C_tijd | `/gtg-fase2-tijd` | 15 + derde-dag pilot = 16 | **VOLTOOID 16/16** |
| 3 | A_entiteit personen | `/gtg-fase3-personen` | 25 (alle voltooid: 17 christustypen + 5 vrouwen + 3 negatieve) | **VOLTOOID 25/25** |
| 4 | A_entiteit overig | `/gtg-fase4-plaatsen-objecten` | 49 (alle voltooid) | **VOLTOOID 49/49** |
| 5 | D_taal | `/gtg-fase5-taal` | 8 (alle voltooid) | **VOLTOOID 8/8** |
| 6 | E_structuur | `/gtg-fase6-structuur` | 8 (alle voltooid) | **VOLTOOID 8/8** |
| 7 | F_verhaal | `/gtg-fase7-verhaal` | 17 | **VOLTOOID 17/17** |
| 8 | G_rol | `/gtg-fase8-rol` | 17 (uitgebreid naar 18 in uitvoering) | **VOLTOOID** |
| 9 | H_contrast | `/gtg-fase9-contrast` | 12 | **VOLTOOID 12/12** |
| 10 | (allen) | `/gtg-fase10-web` | integratie | **VOLTOOID** — herziening aanbevolen na Fase 9 toevoegingen |

**Totaal entries:** ongeveer 163 + integratie. Bij 1 entry per sessie: 163+ sessies. Bij 2-3 entries per sessie: 60-80 sessies. Realistisch werk-traject.

## Fase-afroepbare skills

Per fase staat één skill-bestand klaar in `skill/fasen/`. Bij activatie laadt de skill:
- Het volledige raamwerk (`_raamwerk.md`)
- Het entry-sjabloon (`_entry-sjabloon.md`)
- Het detectie-protocol (`protocollen/typologie-detectie.md`)
- De fase-specifieke instructie (welke patronen, welke werkstrategie)
- Bestaande entries in de relevante submap

Daarna gaat de skill zelfstandig aan de slag met de volgende patroon-kandidaat in de fase, of de gebruiker kan een specifieke kandidaat aanwijzen.
