# Skill v5 — pairwise testset v3

**Datum opgesteld:** 28 april 2026 (v2.0), uitgebreid 9 mei 2026 (v3.0)
**Versie:** 3.0 (uitgebreid van 25 naar 43 cases met typologie-coverage, meertaligheid, en Fase 10 web-integratie)
**Status:** klaar voor uitvoering — maintainer approves the pass/fail-rubric en validatie-aanpak
**Werkwijze:** testpoort-regel uit `CLAUDE.md`. Ronde 1 = bouwen + uitvoeren met objectieve criteria. Ronde 2+ = bug-fix + regressie tot definitieve PASS.

---

## 1. Doel

Valideren dat de skill v5 betrouwbaar werkt op vier validatie-dimensies, vóór GitHub-publicatie. **Maximale kwaliteit, geen compromis op betrouwbaarheid.**

## 2. Wijzigingen t.o.v. v1

| Aspect | v1 | v2 |
|---|---|---|
| Aantal testcases | 15 | 25 (+10) |
| T03 transcript-tolerantie | 60-130 wo | 95-125 wo (was 95-115, 10 wo boven max-tolerantie wegens lange verzen) |
| T05/T06 bron-discipline | judgment | objectieve string-checks |
| T12 hapax | PASS-met-noot mogelijk | FAIL-criterium → fix vooraf gedaan |
| Hebreeuws-coverage | 0 cases | 5 cases (T16-T20) |
| Regressie-checks | 0 | 2 (T21-T22) |
| Interview-validatie | 0 | 2 (T23-T24) |
| End-to-end | 0 | 1 (T25) |

## 3. Vooraf-fixes (vóór ronde 1)

| Fix | Status | Bewijs |
|---|---|---|
| Hapax-markering in Blok B (`voorkomens <= 1` → "[hapax]" prefix met uncertainty-melding) | DONE | `skill_v5_blocks.py` regel 119-123 |
| Transcript-tuning naar 95+ woorden via reflectie-fallback | DONE | `skill_v5_transcript.py` `WORD_TARGET_MIN=95` |
| KJV-literal verwijderd uit JSONL (cleanup 2026-04-28) | DONE | 999.821 velden weg, snapshot in `legacy/old/snapshots/` |

## 4. Pass/Fail-rubric

| Status | Betekenis |
|---|---|
| PASS | Volledig voldoet aan pass-criterium. |
| PASS-met-noot | Werkt, maar er is een verbetering mogelijk (geen blocker). |
| FAIL | Functioneel afwijkend van verwachting; bug-fix nodig in dezelfde ronde. |
| BLOCKED | Test kon niet worden uitgevoerd (bv. afhankelijkheid kapot). |

**Definitieve PASS-conditie voor de skill:** alle 25 cases PASS of PASS-met-noot in een definitieve ronde.

## 5. Testcases (25)

### Validatie-dimensie 1 — Output-type correctheid (T01-T04)

**T01 — dossier op vers (NL, Grieks)**
- Input: `python3 skill/skill_v5_blocks.py --vers joh:3:16 --taal nl --blok ABCDE`
- Pass-checks: bevat `## Blok A`, `## Blok B`, `## Blok C`, `## Blok D`, `## Blok E`. Bevat tabel-header `| # | woord | translit | strong | parsing | NL-concordant |` (kolom heet `NL-concordant`, niet `literal`). Bevat geen woorden uit verboden vertaal-tradities-set (zie T07).

**T02 — summary (Blok A+E)**
- Input: `python3 skill/skill_v5_blocks.py --vers joh:3:16 --taal nl --blok AE`
- Pass-checks: bevat `## Blok A` en `## Blok E`. Bevat **geen** `## Blok B`, `## Blok C`, `## Blok D`.

**T03 — transcript (plain text, 95-125 woorden)**
- Input: `python3 skill/skill_v5_transcript.py --vers joh:3:16 --taal nl --json`
- Pass-checks: JSON-output is parseable. Veld `word_count` is 95 ≤ wc ≤ 125. Veld `transcript` bevat geen `#`, `|`, `**`, `_` (markdown-tekens).

**T04 — Strong-input ipv vers**
- Input: `python3 skill/skill_v5_blocks.py --strong G3056 --blok BCD --taal nl`
- Pass-checks: bevat `## Blok B`, `## Blok C`, `## Blok D`. Bevat **geen** `## Blok A` (geen vers-context). Blok B verwijst naar G3056.

### Validatie-dimensie 2 — Bron-discipline (T05-T08)

**T05 — geen verboden traditie in output bij dossier-vraag**
- Input: `python3 skill/skill_v5_blocks.py --vers joh:3:16 --taal nl --blok ABCDE`
- Pass-checks (objectief): output bevat geen substring uit `{Statenvertaling, NBG-51, NBG, NBV, HSV, Naardense, KJV, NIV, ESV, King James, Lutheran}` (case-insensitive). Master-toelichtingen mogen wel klassieke commentatoren noemen mits expliciet als externe referentie.

**T06 — bron-discipline-check exit 0 op schone Kennis**
- Input: `python3 skill/skill_v5_lookup.py --check-discipline`
- Pass-checks: stdout bevat `Bron-discipline OK`. Exit-code 0.

**T07 — JSONL bevat geen `literal` of `literal2` velden**
- Input: scan alle 140 jsonl in `Kennis/strong/` en `Kennis/puur/`, parse elk vers, check elk woord.
- Pass-checks: 0 woord-objecten met key `literal` of `literal2`.

**T08 — bron-discipline op verboden-pad-poging**
- Input: roep `lk.lookup_strong("G3056")` aan, monitor of de module ergens leest buiten `Kennis/`.
- Pass-checks: alle file-reads zijn binnen `Kennis/`. Module verifieert via `ROOT` constante.

### Validatie-dimensie 3 — Edge cases (T09-T15)

**T09 — Strong-code zonder diepte-notitie (Hebreeuws hapax)**
- Input: `python3 skill/skill_v5_blocks.py --strong H4536 --blok B --taal nl`
- Pass-checks: bevat `**[hapax]**` (markering door fix vooraf). Bevat melding `Geen diepte-notitie beschikbaar voor H4536`. Geen crash.

**T10 — G-prefix zonder LXX-mapping**
- Input: `python3 skill/skill_v5_blocks.py --strong G3056 --blok C --taal nl`
- Pass-checks: bevat `Geen LXX-mapping beschikbaar` melding. Cognaten worden wel getoond (uit diepte-laag). Geen crash.

**T11 — niet-bestaand vers (joh:99:99)**
- Input: `python3 skill/skill_v5_blocks.py --vers joh:99:99 --taal nl --blok A`
- Pass-checks: bevat `_Vers joh:99:99 niet gevonden._`. Geen Python stack-trace.

**T12 — hapax-markering bij voorkomens=1**
- Input: `python3 skill/skill_v5_blocks.py --strong H4536 --blok B --taal nl` (zelfde als T09)
- Pass-checks: bevat letterlijke string `[hapax]` en de zin `slechts 1x voor in het corpus`.

**T13 — vers met veel kernwoorden (Joh 3:16, 26 woorden)**
- Input: `python3 skill/skill_v5_blocks.py --vers joh:3:16 --taal nl --blok A`
- Pass-checks: tabel heeft 26 woord-rijen (één per woord). Elke rij heeft Strong-code + NL-concordant.

**T14 — vers met weinig woorden (Joh 11:35 "Jezus weende")**
- Input: `python3 skill/skill_v5_blocks.py --vers joh:11:35 --taal nl --blok A`
- Pass-checks: tabel heeft 3 woord-rijen. Geen crash bij minimaal-vers.

**T15 — onbekende CLI-vlag**
- Input: `python3 skill/skill_v5_lookup.py --bogus-flag 2>&1`
- Pass-checks: stderr bevat melding van onbekende vlag of vlag wordt genegeerd zonder crash.

### Validatie-dimensie 4 — Talen-handling (T16-T20)

**T16 — Hebreeuws vers (gen:1:1) dossier**
- Input: `python3 skill/skill_v5_blocks.py --vers gen:1:1 --taal nl --blok ABCDE`
- Pass-checks: bevat alle 5 blokken. Blok A heeft Hebreeuwse woorden in tabel met H-prefix Strong-codes. Blok C bevat LXX-tegenhangers (H-codes hebben mapping).

**T17 — Hebreeuws Strong-code H1697 (davar) volledige analyse**
- Input: `python3 skill/skill_v5_blocks.py --strong H1697 --blok BCD --taal nl`
- Pass-checks: bevat Blok B (woordstudie davar). Blok C bevat LXX-tegenhanger met geverifieerd top-3 (verwacht onder andere G3056 logos en G4487 rhema in top-3).

**T18 — Hebreeuws hapax met diepte aanwezig**
- Setup: zoek H-code met voorkomens=1 EN diepte-notitie. Anders: alleen master-data + hapax-melding.
- Pass-checks: hapax-markering aanwezig. Geen lege blok-secties.

**T19 — output-taal English voor labels**
- Input: `python3 skill/skill_v5_blocks.py --vers joh:3:16 --taal en --blok ABCDE`
- Pass-checks: blok-titels in EN: `## Block A — Verse context`, `## Block B — Word study`, etc. Tabel-header `| # | word | translit | strong | parsing | NL-concordant |` (NL-concordant blijft NL want EN-master niet gebouwd). Master-toelichtingen blijven NL.

**T20 — taal die nog niet gebouwd is (fr)**
- Input: simulatie via `lk.load_master(taal='fr', script='heb')` in Python.
- Pass-checks: NotImplementedError met expliciete melding `Master voor taal 'fr' nog niet gebouwd`.

### Validatie-dimensie 5 (extra) — Regressies, interview, end-to-end (T21-T25)

**T21 — regressie: pipeline-script werkt na reparatie 2026-04-28**
- Input: `python3 build-software/generate_diepte_template.py H559 --dry-run`
- Pass-checks: stdout bevat `Bestanden laden`, `Genereer 1 sjablonen`, `DRY-RUN H559.md` of `SKIP H559.md`.

**T22 — regressie: lxx-bron staat niet meer in Kennis/**
- Input: `ls Kennis/lxx-bron 2>&1`
- Pass-checks: melding "No such file or directory" of vergelijkbaar. Lxx-bron staat in `legacy/old/lxx-bron-archief/`.

**T23 — interview --auto correct gepased**
- Input: `python3 skill/skill_v5_interview.py --auto en,transcript,vers --json`
- Pass-checks: JSON `{"language": "en", "output_type": "transcript", "depth": "vers"}`.

**T24 — interview --infer met expliciete vraag**
- Input: `python3 skill/skill_v5_interview.py --infer "give me a transcript of Joh 3:16 in english" --json`
- Pass-checks: JSON `language: en`, `output_type: transcript`, `depth: vers`. Geen "unknown".

**T25 — end-to-end via SKILL.md instructies (mock Claude-flow)**
- Input: simuleer Claude die SKILL.md leest, voor vraag _"Geef Rom 5:18 als dossier in NL"_ de juiste bash-aanroep doet, en de output toont.
- Pass-checks: bash-commando is `python3 skill/skill_v5_blocks.py --vers rom:5:18 --taal nl --blok ABCDE`. Output bevat alle vijf blokken.

---

### Validatie-dimensie 5 — Typologie-laag (T26-T35)

Steekproef van tien typologie-entries verspreid over de acht categorieën, elk met een testvraag waarvan de preflight-trigger moet matchen op de bedoelde entry.

**T26 — typologie B_cijfer/120 (Pinksteren-getal)**
- Input: vraag in NL: "Wat betekent het getal 120 in Handelingen 1?"
- Pass-checks: `detect_typologie_entries()` retourneert lijst die `B_cijfer/120` bevat. Pad bestaat: `Kennis/typologie/B_cijfer/120.md`.

**T27 — typologie A_entiteit/adam (christustype)**
- Input: NL "Hoe wordt Adam een type van Christus?"
- Pass-checks: detectie bevat `A_entiteit/adam`. Pad bestaat.

**T28 — typologie C_tijd/derde-dag**
- Input: NL "Wat is de betekenis van de derde dag in Hosea 6 en bij de opstanding?"
- Pass-checks: detectie bevat `C_tijd/derde-dag`. Pad bestaat.

**T29 — typologie D_taal (paronomasie)**
- Input: NL "Welke paronomasie staat tussen dabar en devash?"
- Pass-checks: detectie bevat een entry uit `D_taal/`. Minstens één D_taal pad geactiveerd.

**T30 — typologie E_structuur (chiasme)**
- Input: NL "Welke chiastische structuur heeft het boek Esther?"
- Pass-checks: detectie bevat `E_structuur/chiasme-ester` of equivalent. Pad bestaat.

**T31 — typologie F_verhaal (eerstgeborene-omkering)**
- Input: NL "Waarom wordt steeds de jongere zoon gekozen boven de oudere?"
- Pass-checks: detectie bevat `F_verhaal/eerstgeborene-omkering`. Pad bestaat.

**T32 — typologie G_rol/drie-ambten-priester**
- Input: NL "Hoe is Christus priester naar de orde van Melchizedek?"
- Pass-checks: detectie bevat een G_rol-entry rond priester. Pad bestaat.

**T33 — typologie H_contrast/eerste-laatste-adam**
- Input: NL "Wat is het contrast tussen de eerste en laatste Adam?"
- Pass-checks: detectie bevat `H_contrast/eerste-laatste-adam`. Pad bestaat. N1-claim van Rom 5:14 expliciet detecteerbaar.

**T34 — typologie cross-categorie (cijfer + tijd + entiteit)**
- Input: NL "Wat betekent veertig dagen woestijn voor Mozes en voor Jezus?"
- Pass-checks: detectie bevat minstens twee categorieën — `B_cijfer/40` én `A_entiteit/mozes` of `C_tijd/jaren-veertig`.

**T35 — typologie negatief-pattern (false negative test)**
- Input: NL "Wat is het beste recept voor matzes?"
- Pass-checks: detectie retourneert lege lijst of alleen N3-vermoede patronen. Geen valse N1/N2 activatie op niet-typologische vraag.

### Validatie-dimensie 6 — Meertaligheid (T36-T40)

**T36 — dossier in Engels**
- Input: `python3 skill/skill_v5_blocks.py --vers joh:3:16 --taal en --blok ABCDE`
- Pass-checks: alle vijf blokken aanwezig. Tabel-header in EN ("EN-concordant" als kolomnaam, niet NL-concordant). Geen NL-tekst in body.

**T37 — dossier in Spaans**
- Input: `python3 skill/skill_v5_blocks.py --vers joh:3:16 --taal es --blok ABCDE`
- Pass-checks: alle vijf blokken aanwezig. Kolomnaam "ES-concordant". Bevat geen NL- of EN-strings in body.

**T38 — concordant master EN coverage**
- Input: scan `Kennis/masters/en/concordant-en-grieks.json` en `concordant-en-hebreeuws.json`
- Pass-checks: elke entry heeft non-null `nl` of `en` doelwoord en non-null rationale. Geen lege rendering-strings.

**T39 — concordant master ES coverage**
- Input: scan `Kennis/masters/es/concordant-es-grieks.json` en `concordant-es-hebreeuws.json`
- Pass-checks: elke entry heeft non-null doelwoord. Cross-validatie: dezelfde Strong-codes in ES-master als in NL-master (sets gelijk).

**T40 — taal-fallback bij ontbrekende ES-entry**
- Input: `python3 skill/skill_v5_blocks.py --strong G9999 --taal es` (Strong-code die niet in master staat)
- Pass-checks: skill faalt niet. Output bevat melding "concordant rendering not available for ES" of equivalent. Geen crash.

### Validatie-dimensie 7 — Fase 10 web-integratie (T41-T43)

**T41 — build_index.py produceert geldig _index.json**
- Input: `python3 skill/fase10/build_index.py`
- Pass-checks: exit-code 0. `Kennis/typologie/_index.json` is parseable JSON. Veld `stats.total_entries` ≥ 170. Veld `stats.total_unique_verzen` ≥ 3000. Stdout bevat "Geschreven:" met pad naar _index.json.

**T42 — check_xrefs.py rapporteert 0 broken-link regressies**
- Input: `python3 skill/fase10/check_xrefs.py`
- Pass-checks: exit-code 0. `Kennis/typologie/_xref_check.md` wordt geschreven. Stdout bevat "Gebroken links:" gevolgd door een getal. Het getal moet stabiel zijn over runs (geen non-determinisme).

**T43 — _index.json reverse-lookup correctheid**
- Input: open `_index.json`, kies een willekeurig vers (bv. Rom 5:14), check dat de lijst entries die ernaar verwijzen ten minste `A_entiteit/adam.md` en `H_contrast/eerste-laatste-adam.md` bevat.
- Pass-checks: beide paden in de vers-mapping. Reverse Strong-lookup voor G5179 (typos) bevat ten minste `H_contrast/eerste-laatste-adam.md`.

## 6. Pairwise-dekking-controle

Met 25 cases dekken we minstens elke combinatie van twee dimensie-waarden:

| Dimensie-paar | Voorbeelden in testset |
|---|---|
| Output-type × bron-discipline | T01 (dossier+clean), T05 (dossier+strikte-traditie-check) |
| Output-type × edge case | T03 (transcript+vers), T11 (Blok A+niet-bestaand), T14 (Blok A+kort-vers) |
| Output-type × taal | T01 (dossier+nl), T19 (dossier+en) |
| Output-type × Hebreeuws/Grieks | T01 (Grieks NT), T16 (Hebreeuws OT) |
| Bron-discipline × edge case | T07 (regressie cleanup), T08 (lookup-pad-check) |
| Bron-discipline × taal | T05 (NL+verboden-strings), T06 (folder-scan) |
| Edge case × taal | T09 (geen diepte+nl), T20 (fr+master-ontbreekt) |
| Hapax × diepte | T09 (hapax+geen-diepte), T18 (hapax+wel-diepte) |
| Regressie × bron-discipline | T22 (lxx-bron weg), T07 (literal-cleanup) |

## 7. Vervolg

Cowork voert nu ronde 1 uit. Per case PASS/FAIL met bewijs. Bugs worden binnen dezelfde ronde gefixt waar mogelijk; daarna regressie-pass. Definitieve PASS = volgende sessie of automatisch in test-runner.

---

_Document opgesteld door Claude — the maintainer — versie 2.0_
