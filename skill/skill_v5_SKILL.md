---
name: godstruegospel
description: Concordante bijbelstudie vanuit Hebreeuwse, Aramese en Griekse grondtekst. Vijf lagen: tekst, vertaal (concordante master), diepte (zeven-ankers per kernwoord), omgekeerde index, LXX-mapping en protocollen. Geen vertaal-tradities, geen geheugen-input. Default-output: A4-samenvatting (max 1 A4, concreet antwoord met vers-verwijzingen). Opt-in via interview: Blok A (woord-Strong-tabel), B (etymologisch dieptedossier), C (cross-references), D (vers-lijst per Strong), E (taalkundige synthese), F (Instagram-tekst ~100 woorden). Talen NL, EN, ES operationeel; interview wordt altijd in de taal van de gebruiker gevoerd. Levering default als PDF. Triggeren bij /gtg, vragen over de grondtekst, een Strong-nummer, een Hebreeuws of Grieks woord, of bij vers-referenties (bv. Joh 3:16). Frase-triggers NL: "in de grondtekst", "wat staat er echt", "concordant". EN: "in the source text", "what does the text really say", "concordant". ES: "en el texto fuente", "qué dice realmente el texto", "concordante".
---

# godstruegospel — Skill v5.4.2

## Versiehistorie
- **v5.4.2 (2026-05-11)**: Meertalige toegankelijkheid. Twee aanvullingen op v5.4.1. (1) Trigger-frases in de YAML-description uitgebreid met Engelse en Spaanse equivalenten naast de Nederlandse, zodat de skill ook betrouwbaar triggert bij Spaans- of Engelstalige vragen ("in the source text", "en el texto fuente", "concordant", "concordante"). (2) Expliciete spec-regel toegevoegd dat het interview altijd in de taal van de gebruiker wordt gevoerd: de Nederlandse zinnen in de interview-vragen-template zijn een sjabloon, geen dwingende formulering. Claude vertaalt het sjabloon naar de taal die de gebruiker spreekt voordat hij de AskUserQuestion-aanroepen doet. Achtergrond: een Spaans-sprekende test-gebruiker zou anders Nederlandse interview-schermen krijgen ondanks dat de output-laag (PROMPT_TEMPLATES, A4_TEMPLATES) wel NL/EN/ES beheerst.
- **v5.4.1 (2026-05-11)**: Interview-UX-correctie op v5.4. De zes per-blok vragen MOETEN als zes losse AskUserQuestion-aanroepen worden gesteld, in vaste volgorde A, B, C, D, E, F, elk met ja/nee als enige antwoord-opties. Bundeling in één multi-select-scherm is verboden: in de praktijk leverde dat UI-truncatie op waarbij Blok D (vers-lijst per Strong) en Blok F (Instagram-tekst) werden weggelaten omdat de AskUserQuestion-tool maximaal vier zichtbare opties plus "Something else" toelaat. De skill-spec van v5.4 ("per blok één functionele vraag") wordt hiermee strikt afgedwongen.
- **v5.4 (2026-05-11)**: Output-architectuur grondig herzien. A4-samenvatting (max 1 A4, concreet antwoord op de vraag in begrijpelijk Nederlands met directe vers-verwijzingen) wordt het default-resultaat van élke gtg-vraag. De Blokken A tot en met F worden expliciet opt-in via een uitgebreid per-blok interview, niet meer als één bundel. Interview-script `skill_v5_interview.py` accepteert nu een lijst `blocks_requested` (subset van {A, B, C, D, E, F}) in plaats van één output-type. Per blok stelt Claude in Stap 1 een functioneel geformuleerde ja/nee-vraag aan de gebruiker (zie sectie Interview-vragen-template). Talen-vraag expliciet als eerste interview-stap, met NL/EN/ES als operationele opties en fallback-waarschuwing voor de overige 14 talen. Output-formaat default PDF: scripts produceren markdown, Claude rendert de markdown via de pdf-skill naar PDF bij oplevering; beide bestanden gaan naar de werkmap. Blok F (Instagram of Reels-tekst van ~100 woorden voor ElevenLabs en Kling) wordt voortaan expliciet als opt-in genoemd in het interview, niet meer impliciet onder "dossier" of "transcript".
- **v5.3 (2026-05-09)**: Typologie-corpus volledig opgebouwd over Fasen 1 t/m 9 plus Fase 10 web-integratie. 170 entries totaal, verdeeld over de acht hoofdcategorieën: 13 cijfer-entries (B_cijfer), 16 tijd-entries (C_tijd), 74 entiteit-entries (A_entiteit, 25 personen + 49 plaatsen-objecten-dieren-planten-materialen-kleuren-lichaamsdelen), 8 taal-entries (D_taal), 15 structuur-entries (E_structuur), 17 verhaal-entries (F_verhaal), 15 rol-entries (G_rol), 12 contrast-entries (H_contrast). Fase 10 levert `_index.json` met reverse-lookup over 3301 unieke vers-references en 3286 Strong-codes, plus `_xref_check.md` cross-reference rapport. Pre-flight `TYPOLOGIE_TRIGGERS` uitgebreid met entry-specifieke regex-patronen voor alle Fase-9 contrast-entries. Build-scripts (`fase10/build_index.py` en `fase10/check_xrefs.py`) gebruiken relatieve paden voor herhaalbaarheid over sessies. Concordante masters uitgebreid van één naar drie talen: NL (`Kennis/concordant-nl-*.json`), EN (`Kennis/masters/en/concordant-en-*.json`) en ES (`Kennis/masters/es/concordant-es-*.json`); skill-output kan nu direct in alle drie de talen geleverd worden. Documentatie-PDFs gepubliceerd in `docs/godstruegospel-documentation-{en,nl,es}.pdf` (drie talen, met vijf figuren, drie sample workflows, glossary en attribution). MIT-licentie, ATTRIBUTION-bestand voor scripture4all + STEPBible-Data, en CONTRIBUTING-richtlijnen toegevoegd voor publieke distributie.
- **v5.2 (2026-05-02)**: Typologie-laag toegevoegd in `Kennis/typologie/` met raamwerk V2 (drie assen: categorie, hermeneutische laag, zekerheids-niveau), entry-sjabloon, en patroon-detectie protocol. Acht hoofdcategorieën (A_entiteit t/m H_contrast) met open uitbreidings-ruimte. Pre-flight uitgebreid met typologie-detectie. Bronnen-manifest neemt typologie-bestanden op. Output-blokken C en E krijgen vaste sectie voor typologische cross-references als coherentie-watermerk. Sola scriptura, oplettende-lezer-presumptie, anti-patronen-lijst. Strong-codes gedegradeerd tot zoek-werktuig (geen typologie-element).
- **v5.1 (2026-05-02)**: Dwingend interview-protocol. Pre-flight checklist verplicht. Bronnen-manifest verplicht boven elke output. Anti-geheugen-eed uitgebreid van cijfers naar interpretaties (kruisreferenties, identiteits-aannames, eindpunt-keuzes, telmethoden). Chronologie-protocol als eigen kennislaag in `Kennis/protocollen/`. Interpretatieve-keuzes bron-weging document toegevoegd. Geen training-bias als default; geen leeshoeken-pluralisme als verkapt diplomatieke positie; werk-conclusies trekken op basis van bron-weging.
- **v5.0**: MVP met vier modules, vier output-blokken, NL master.

## Doel

Eén skill die voor elke ondersteunde taal betrouwbare, concordant onderbouwde antwoorden geeft op bijbelvragen, rechtstreeks uit de grondtekst — zonder dat een traditionele vertaling of een traditioneel interpretatiekader tussen de gebruiker en de tekst staat. De skill voert zelfstandig multi-vers onderzoek uit volgens vaste protocollen, trekt bron-onderbouwde werk-conclusies waar de tekst voldoende ondersteuning biedt, en houdt keuzepunten open waar de tekst genuinely meerduidig is.

## Wat neutraliteit hier betekent (en wat niet)

Neutraliteit in deze skill betekent: geen training-bias als default. Het betekent NIET conflict-vermijding via "twee leeshoeken parallel presenteren" wanneer de bron-weging duidelijk één kant op leunt. Dat soort pluralisme is in de praktijk geen neutraliteit — het laat traditie winnen door de meest mainstream-bekende leeshoek tot "default" te verklaren.

De skill werkt zo: per keuzepunt waar de tekst meerduidigheid toelaat, kijkt de skill expliciet welke optie het sterkst bron-onderbouwd is. De meest onderbouwde optie wordt de werk-conclusie. Het minder onderbouwde alternatief wordt vermeld met de tekstuele reden waarom het zwakker is. Externe historische tradities (Ussher, Seder Olam, Septuagint-Byzantijns, modern-archeologisch) worden vermeld als context, niet als alternatieve "leeshoeken op gelijke voet".

Alleen bij genuinely 50/50 keuzes (zoals Daniël 9 = 490 of 500 jaar) blijven beide opties open en wordt de gebruiker geïnformeerd.

---

## ⛔ ABSOLUTE REGEL — LEES DIT VOORDAT JE IETS DOET

Bij elke activatie van deze skill, VOORDAT je ook maar één letter output produceert, moet Claude de volgende drie poorten passeren in deze volgorde:

**Poort 1 — Interview is afgedwongen.** Geen enkele output zonder dat de drie dimensies (taal, blokken-keuze, vers-scope) expliciet zijn vastgesteld via interview of `--infer` met daarna expliciete bevestiging aan de gebruiker. De A4-samenvatting is altijd onderdeel van de output, ongeacht de blokken-keuze. Aanname is verboden voor de drie dimensies; alleen de A4-default mag verondersteld worden zonder expliciete bevestiging.

**Poort 2 — Bronnen-manifest is verplicht.** Boven elke inhoudelijke output staat een blok `## BRONNEN-MANIFEST` met de exacte lijst van bestanden uit `Kennis/` die zijn gelezen voor dit antwoord. Geen bestand vermeld = geen uitspraak doen op dat onderwerp.

**Poort 3 — Anti-geheugen-eed.** Voor élke uitspraak (cijfer, citaat, wortel, betekenis, kruisreferentie, chronologie, interpretatie, traditie) geldt: ofwel het komt herleidbaar uit een bestand in het bronnen-manifest, ofwel het wordt expliciet gemarkeerd als `[EXTERN]` of `[ONBEKEND uit bronnen]`. Geheugen-input vanuit Claude's training is verboden, ongeacht hoe vanzelfsprekend de uitspraak lijkt. Geen training-bias als default.

Als je deze poorten niet kunt sluiten, stop. Vraag de gebruiker om verduidelijking of geef een eerlijke "ik kan dit niet uit de bronnen halen" terug. Liever niets zeggen dan iets uit het geheugen reconstrueren.

---

## Architectuur

Vijf modules in `skill/`:

| Module | Doel |
|---|---|
| `skill_v5_lookup.py` | Lookup-helpers voor alle 5 lagen (tekst, vertaal, diepte, index, LXX) |
| `skill_v5_interview.py` | Drie-dimensies-interview voor taal (nl/en/es) + blokken-keuze (subset {A,B,C,D,E,F}) + vers-scope (afgedwongen) |
| `skill_v5_blocks.py` | Bouwt A4-samenvatting (default) en optionele Blokken A t/m E |
| `skill_v5_transcript.py` | Bouwt Blok F (Instagram/Reels-tekst ~100-110 woorden voor ElevenLabs en Kling) |
| `skill_v5_preflight.py` | Pre-flight checklist + bronnen-manifest generator (v5.1) |

Bron-discipline: uitsluitend `Kennis/` — geen externe vertaal-tradities, geen Statenvertaling, NBG, NBV, HSV, KJV, ESV, etc. Geen training-data herinnering.

---

## Werkwijze per sessie (v5.1 + v5.4 interview-uitbreiding)

### Stap 0 — Pre-flight (verplicht)

```bash
python3 skill/skill_v5_preflight.py --vraag "<gebruikers-vraag>" --json
```

De checklist controleert:
1. Heb ik de gebruikersvraag begrepen? Zo nee → vraag verduidelijking.
2. Zijn de drie interview-dimensies bekend? Zo nee → ga naar Stap 1.
3. Welke bronnen ga ik nodig hebben? → produceer voorlopig bronnen-manifest.
4. Zijn er chronologische, multi-vers of cross-tekst-elementen? Zo ja → activeer chronologie-protocol uit `Kennis/protocollen/chronologie.md` en pas de bron-weging uit `Kennis/protocollen/interpretatieve-keuzes.md` toe.
5. Worden in de vraag externe historische tradities genoemd (Ussher, Joods, LXX, etc.)? Zo ja → vermelden als context bij output, niet als alternatieve leeshoek.

### Stap 1 — Interview (DWINGEND, niet meer optioneel)

Drie dimensies: taal, blokken-keuze, vers-scope. De A4-samenvatting is altijd onderdeel van de output en hoeft niet bevraagd te worden.

**Scenario A: gebruiker noemt 0-2 dimensies expliciet.** Voer het volledige interview af volgens het interview-vragen-template hieronder.

**Scenario B: gebruiker noemt alle 3 dimensies expliciet.** Run `--infer --confirm`. Toon de detectie en vraag bevestiging in één regel.

**Scenario C: gebruiker stelt vervolgvraag in dezelfde sessie.** Hergebruik eerder bevestigde dimensies, meld dat hergebruik bovenin.

```bash
python3 skill/skill_v5_interview.py --infer "<gebruikers-vraag>" --confirm --json
```

In géén van de drie scenario's mag Claude defaults aannemen voor de drie dimensies zonder de gebruiker te informeren of te vragen. De A4-samenvatting is de enige uitzondering: die wordt altijd gemaakt.

#### Interview-vragen-template (Claude stelt deze vragen aan de gebruiker)

⚠️ TAAL-REGEL (HARD): Het interview wordt altijd gevoerd in de taal die de gebruiker spreekt, niet in het Nederlands omdat de template dat doet. Detecteer de taal van de gebruikersvraag en vertaal de zinnen hieronder naar die taal voordat je de AskUserQuestion-aanroepen doet. De Nederlandse formuleringen hieronder zijn een SJABLOON, geen dwingende tekst. Voorbeeld: een Spaans-sprekende gebruiker krijgt "¿En qué idioma quieres la salida?" in plaats van "In welke taal wil je de output?". Hetzelfde geldt voor de zes blok-vragen en de vers-scope-vraag.

**Vraag 1, taal.** "In welke taal wil je de output? Drie operationele talen: Nederlands (NL), Engels (EN), Spaans (ES). De overige 14 talen op de roadmap zijn nog niet gebouwd; bij een keuze daarvoor val ik terug op NL met expliciete vermelding."

**Vraag 2, blokken-keuze.** ⚠️ TOOL-AANROEP-PATROON (HARD): de zes per-blok vragen MOETEN als ZES LOSSE AskUserQuestion-aanroepen worden gesteld, één per blok, in vaste volgorde A → B → C → D → E → F. Antwoord-opties per call: "Ja" en "Nee" (en optioneel "Something else" als de gebruiker een toelichting wil geven). Bundeling van meerdere blokken in één multi-select AskUserQuestion is VERBODEN omdat de tool maximaal vier zichtbare opties plus "Something else" toelaat, waardoor blokken systematisch worden weggelaten (v5.4-bug, gefixt in v5.4.1).

Open de zes-vraag-serie met een korte intro-zin in chat (geen AskUserQuestion): "De A4-samenvatting (max 1 A4 concreet antwoord, met directe vers-verwijzingen) krijg je altijd. Ik ga je nu per blok vragen of je dat er ook bij wilt. Zes korte ja-of-nee-vragen."

Daarna één AskUserQuestion per blok met functionele uitleg:

- AskUserQuestion 1 — "Blok A, woord-Strong-tabel: een rauwe tabel per vers met elk Grieks of Hebreeuws woord, transliteratie, Strong-code, parsing en NL-concordante betekenis. Geschikt als je het vers woord-voor-woord wilt nalopen. Wil je dit erbij?"
- AskUserQuestion 2 — "Blok B, etymologisch dieptedossier: per kernwoord de wortel-analyse, semantische velden, cognaten in zustertalen en clusterverbanden uit de diepte-laag (zeven-ankers). Voor woorden zonder diepte-notitie krijg je een eerlijke ontbreking-markering plus de master-toelichting. Wil je dit erbij?"
- AskUserQuestion 3 — "Blok C, cross-references en LXX-bruggen: alle plekken in de Schrift waar dezelfde Strong-codes voorkomen, plus LXX-LIFT-scores die OT-Hebreeuws en NT-Grieks aan elkaar koppelen. Ook typologische coherentie-watermerken indien aanwezig. Wil je dit erbij?"
- AskUserQuestion 4 — "Blok D, vers-lijst per Strong: de complete lijst van vers-referenties per kern-Strong via de omgekeerde index, gegroepeerd per genre. Geschikt als je zelf de hele verspreiding wilt nalopen. Wil je dit erbij?"
- AskUserQuestion 5 — "Blok E, taalkundige synthese: een samenvattende analyse die A+B+C+D bij elkaar legt zonder theologische conclusies. Wil je dit erbij?"
- AskUserQuestion 6 — "Blok F, Instagram of Reels-tekst: een korte tekst van ongeveer 100 woorden geschikt voor ElevenLabs-voiceover en Kling-video. Wil je dit erbij?"

Bij elke vraag: gebruiker antwoordt Ja of Nee. Claude verzamelt het lijstje van Ja-blokken als `blocks_requested`. Bij zes-keer-Nee: alleen A4 wordt geleverd.

**Vraag 3, vers-scope.** "Voor de onderbouwing: wil je dat ik me beperk tot het exacte vers of de exacte verzen die je noemt (vers-scope), of zoek ik breder naar de relevante kernwoorden door de hele Schrift (woord-scope), of pak ik een chronologische of thematische cross-vraag erbij (thema-scope)?"

#### Validatie via script

```bash
python3 skill/skill_v5_interview.py --infer "<gebruikers-vraag>" --confirm --json
```

Het script accepteert:
- `language`: nl | en | es | (overige codes met fallback-waarschuwing)
- `blocks_requested`: comma-gescheiden subset van `A,B,C,D,E,F` (mag leeg zijn — dan alleen A4)
- `depth`: vers | word | theme

en valideert dat alle drie de dimensies bekend zijn voor de output-stap mag starten.

### Stap 2 — Vers- of Strong-resolutie

Bij vers-vraag:
```bash
python3 skill/skill_v5_lookup.py --vers joh:3:16
```

Bij Strong-code-vraag:
```bash
python3 skill/skill_v5_lookup.py --kern G3056
```

Bij multi-vers chronologie-vraag: zie chronologie-protocol verderop en het gedetailleerde document `Kennis/protocollen/chronologie.md`.

### Stap 3 — Output bouwen

**A4-samenvatting (default, altijd inbegrepen):**
```bash
python3 skill/skill_v5_blocks.py --vers joh:3:16 --taal nl --a4
```
De A4-modus produceert een markdown-bestand met max 1 A4 tekst: directe beantwoording van de vraag, in begrijpelijk Nederlands (of EN/ES), met concrete vers-verwijzingen waarop de uitspraak leunt. Geen woord-Strong-tabellen, geen LXX-LIFT-scores. Wel sola-scriptura discipline: alle inhoud uit `Kennis/`, geen training, geen traditie. De A4 is een gecondenseerde synthese van het onderliggende grondige onderzoek.

**Opt-in blokken (op basis van `blocks_requested` uit het interview):**
```bash
python3 skill/skill_v5_blocks.py --vers joh:3:16 --taal nl --blok ABCDE
python3 skill/skill_v5_transcript.py --vers joh:3:16 --taal nl --json   # Blok F
```
Bij `blocks_requested=A,C` wordt `--blok AC` aangeroepen. Bij `blocks_requested=F` wordt het transcript-script aangeroepen. Bij lege `blocks_requested` wordt alleen `--a4` aangeroepen.

**Levering aan gebruiker:** zie sectie "Output-formaat" hieronder.

### Stap 4 — Presenteer aan gebruiker

Elke output begint met:

```
## BRONNEN-MANIFEST
Onderstaande output is uitsluitend afgeleid van:
- Kennis/strong/<boek>.jsonl (vers X:Y, X:Z, ...)
- Kennis/diepte/<Strong>.md
- Kennis/index/strong-vers-<taal>.json
- Kennis/protocollen/<protocol>.md (waar van toepassing)
- Kennis/typologie/<categorie>/<entry>.md (waar typologische coherentie-check geactiveerd is)
```

Daarna pas de inhoudelijke output. Geen narratie eromheen, geen filler.

---

## Bron-discipline (HARDE REGEL)

De skill mag uitsluitend lezen uit:

**Grondtekst-laag:** `Kennis/puur/[boek].jsonl`, `Kennis/strong/[boek].jsonl`

**Vertaallaag:** `Kennis/concordant-nl-hebreeuws.json`, `Kennis/concordant-nl-grieks.json`, `Kennis/masters/[taal]/...`

**Diepte-laag:** `Kennis/diepte/[Strong].md`

**Index- en cross-laag:** `Kennis/index/strong-vers-{hebreeuws,grieks}.json`, `Kennis/lxx-mapping-{hebreeuws,grieks}.json`

**Protocollen-laag (v5.1):** `Kennis/protocollen/chronologie.md`, `interpretatieve-keuzes.md`, `README.md`

**Verboden bronnen:** alle traditionele vertalingen (KJV, ESV, NBG, NBV, SV-1977, HSV, Naardense, NIV), alle traditie-gebonden commentaren, en alle training-data herinnering. Als er geen entry is voor wat de gebruiker vraagt: zeg dat eerlijk.

---

## Anti-geheugen-eed (UITGEBREID v5.1)

In v5.0 stond deze regel alleen op woord-betekenis. v5.1 breidt hem uit naar **alle** uitspraken:

**Cijfers en data**: leeftijden, jaartallen, perioden, regeringsjaren — uitsluitend uit grondtekst-Strongs of expliciet gemarkeerd extern.

**Kruisreferenties en samenhangen**: NT-OT cross-references (zoals Hand 7:4 → Terach 130, Hand 7:2-3 → belofte vóór Charan, Gal 3:17 → 430 jaar belofte tot wet) zijn dwingend, niet optioneel. Toon de redenering, leen niet uit traditie.

**Identiteits-aannames**: bv. "vertrek uit Charan = ontvangst van de belofte" is een interpretatieve aanname. Markeer als zodanig en pas bron-weging uit `interpretatieve-keuzes.md` toe.

**Eindpunt-keuzes**: bv. "tempelfundering" versus "voltooiing tempel + paleis" — toon de keuze expliciet en pas bron-weging toe.

**Chronologische tradities**: Ussher, Joods AM, Septuagint-Byzantijns, modern-archeologisch — vermelden als context, niet als alternatieve leeshoeken op gelijke voet. Geen training-bias als default.

**Telmethoden**: inclusief versus exclusief tellen, halve-jaar-correctie, hele-kalenderjaar-conventie — al deze keuzes zijn methodologisch en moeten expliciet worden benoemd. Bron-onderbouwde keuze (uit `interpretatieve-keuzes.md`) wordt toegepast als werk-methode.

**Praktische regel**: vóór elke uitspraak vraagt Claude zichzelf: "kan ik dit herleiden naar een bestand in het bronnen-manifest, of leen ik dit uit mijn training?" Bij twijfel: niet zeggen, of expliciet markeren als `[ONBEKEND uit bronnen]`.

---

## Chronologie-protocol (samenvatting — volledige tekst in protocollen-laag)

Voor multi-vers chronologie-vragen (gedetecteerd door pre-flight) volgt de skill onverkort de zeven werkstappen uit `Kennis/protocollen/chronologie.md`:

C1 — Vragen-decompositie in atomaire vers-lookups.
C2 — Bron-extractie per vers uit `Kennis/strong/[boek].jsonl`.
C3 — Decoding-tabel uit cijfer-Strongs (zie chronologie.md).
C4 — Interpretatieve keuzes maken via bron-weging uit `interpretatieve-keuzes.md`.
C5 — Werk-redenering tonen, optelling stap voor stap met bronvers-attributie.
C6 — Eindgetal met onzekerheidsmarge en gebruikte methode expliciet vermeld.
C7 — Externe historische ankering (BC/AD-conversie) apart en gemarkeerd.

Het chronologie-protocol bevat de volledige cijfer-Strongs decoderingstabel (H259 t/m H505) en een werk-conclusies tabel met bron-onderbouwde anker-punten van Adam tot Christus. Bij chronologie-vragen wordt ook de typologie-laag geactiveerd voor coherentie-watermerken (zie hieronder).

---

## Typologie-laag (v5.2)

De typologie-laag staat in `Kennis/typologie/` en levert coherentie-watermerken bovenop de directe lezing. Patronen die de Schrift zelf legt door consistent woord-, cijfer-, naam-, plaats-, dag- of structuurgebruik worden hier verankerd onder sola-scriptura discipline en de oplettende-lezer-presumptie.

**Architectuur.** Drie assen tegelijk: As 1 categorie (acht hoofdcategorieën A_entiteit, B_cijfer, C_tijd, D_taal, E_structuur, F_verhaal, G_rol, H_contrast met open uitbreiding); As 2 hermeneutische laag (L1 direct-historisch, L2 christus-typologisch, L3 ecclesiologisch, L4 eschatologisch met open uitbreiding); As 3 zekerheids-niveau (N1 hard, N2 aanwijsbaar, N3 vermoed). Volledige beschrijving in `Kennis/typologie/_raamwerk.md`.

**Activatie.** Pre-flight detecteert wanneer typologie relevant is — op basis van vraag-signalen (cijfer genoemd, persoon genoemd, plaats genoemd, dag-aanduiding, structuur-vraag, chronologie). Bij activatie laadt de skill de relevante entries uit de juiste submap en plaatst ze in het bronnen-manifest.

**Operationele modi.** Mode passief tijdens vraag-beantwoording (entries lezen, geen nieuwe schrijven). Mode actief tijdens onderzoek-sessie (zeven-stappen werkwijze uit `protocollen/typologie-detectie.md`, nieuwe entry volgens `_entry-sjabloon.md`). Mode cross-check periodiek (consistentie, hiaten, conflicten signaleren).

**Anti-patronen.** Geen kerkvaders, midrasj, kabbalistische exegese, moderne typologen, theologische systemen — tenzij hetzelfde patroon onafhankelijk uit de grondtekst aantoonbaar is. Geen allegorie waar de tekst letterlijk-historisch is. Geen numerologie zonder dat de tekst zelf het cijfer signaleert. Geen cross-vertaling als bron. Geen geheugen-input. Strong-codes alleen als zoek-werktuig in scripts, nooit als typologie-element.

**Toepassing in output.** Blok C en Blok E krijgen vaste sectie voor typologische cross-references (zie Output-blokken hieronder).

---

## Talen

**Operationeel (drie talen):** NL (master in `Kennis/concordant-nl-*.json`), EN (master in `Kennis/masters/en/concordant-en-*.json`), ES (master in `Kennis/masters/es/concordant-es-*.json`). Skill-output kan in alle drie de talen direct geleverd worden zonder fallback.

**Roadmap (14 talen):** FR, IT, PT, BG, RU, AR, HI, ZH, JA, KO, TR, EL, TA, HE. Bij een vraag in een van deze talen meldt de skill expliciet: "Master voor taal '<code>' nog niet gebouwd. Operationeel zijn NL, EN, ES. Ik val terug op NL." Daarna vraagt Claude bevestiging of NL acceptabel is.

## Output-blokken

**A4-samenvatting (default, altijd inbegrepen)** — Max 1 A4 markdown-tekst die de gebruikersvraag direct beantwoordt in begrijpelijk Nederlands (of EN/ES), met concrete vers-verwijzingen waarop de uitspraak leunt. Geen woord-Strong-tabellen, geen LIFT-scores, geen technische apparatus. Wel sola-scriptura: alle inhoud rust op het grondige onderzoek dat onder de motorkap heeft plaatsgevonden, geen training-data, geen traditie-vertaling, geen theologie. De A4 is de zichtbare opbrengst van het onderzoek; de Blokken A-F leveren het onderliggende werk.

**Opt-in blokken via interview (`blocks_requested`):**

- **Blok A** — Vers-citatie + transliteratie + woord-Strong-tabel. Rauwe taalkundige laag: elk woord uit het vers met Grieks of Hebreeuws, transliteratie, Strong-code, parsing, NL-concordante betekenis uit de master.
- **Blok B** — Per kernwoord: wortel, etymologie, basisbetekenis (uit diepte-laag). Voor ontbrekende diepte-notities: master-toelichting met expliciete markering `[diepte-notitie nog niet aanwezig in Kennis/diepte/]`.
- **Blok C** — Cognaten in zustertalen + LXX cross-testament-koppeling + NT-OT cross-referenties. Bij actieve typologie-laag: vaste sub-sectie "Typologische cross-references" met de geraadpleegde entries uit `Kennis/typologie/`, hun zekerheids-niveau (N1/N2/N3), en relevante hermeneutische lagen (L1-L4).
- **Blok D** — Volledige vers-lijst per Strong via omgekeerde index, gegroepeerd per genre.
- **Blok E** — Taalkundige synthese A+B+C+D, geen theologische conclusies, geen geheugen-input. Bij actieve typologie-laag: vaste sub-sectie "Coherentie-watermerk" waar typologische patronen worden afgewogen tegen de directe lezing — bevestigend (patroon ondersteunt directe lezing), neutraal (geen relevante typologie), of signaal-gevend (typologie wijst naar mogelijke heroverweging). Watermerk is nooit bewijs, altijd coherentie-aanwijzing.
- **Blok F** — Instagram of Reels-tekst van ~100-110 woorden geschikt voor ElevenLabs-voiceover en Kling 3.0 video. Korte, kernachtige formulering die in ongeveer 40 seconden uitgesproken kan worden.

## Output-formaat

**Default leveringsformaat: PDF.** Scripts produceren markdown-bestanden in de werkmap. Claude rendert de markdown vervolgens via de pdf-skill (`anthropic-skills:pdf`) naar PDF. Beide bestanden (`.md` en `.pdf`) blijven in de werkmap; de PDF is het primaire deliverable, de markdown het bronbestand voor eventuele bewerking.

Bestandsnaam-conventie: `<onderwerp>-grondtekst-dossier.{md,pdf}` voor dossiers, `<onderwerp>-A4.{md,pdf}` voor de A4-samenvatting, `<onderwerp>-reels.{md,pdf}` voor Blok F.

Bij grote dossiers (meer dan 5 A4 totaal) blijft de A4-samenvatting in een apart bestand, zodat de gebruiker meteen de samenvatting kan lezen zonder eerst door het volledige dossier te scrollen.

## Betrouwbaarheids-discipline (v5.1)

Elke uitspraak herleidbaar naar:
1. Bron-vers (tekstlaag)
2. Master-keuze (vertaallaag)
3. Diepte-analyse (zeven-ankers)
4. Cross-vers-bevestiging (omgekeerde index)
5. Protocol-laag indien procedureel relevant (chronologie, kruisreferenties, hapax)

Bij hapaxen of identiteit-onzekere woorden: eerlijke uncertainty-markering.
Bij interpretatieve keuze: pas bron-weging uit `interpretatieve-keuzes.md` toe; werk-conclusie + zwakker alternatief vermelden. Geen pluralisme als verkapt diplomatieke positie.

---

## Beslisregels

- Bij conflict tussen master en diepte-notitie: master is leidend.
- Bij vraag over taal die nog niet gebouwd is (alles buiten NL/EN/ES): meld eerlijk welke drie talen operationeel zijn en bied NL-fallback aan na bevestiging.
- Bij `blocks_requested` leeg: lever alleen A4-samenvatting. Geen blokken erbij genereren zonder expliciete keuze.
- Bij hapax: markeer als zodanig.
- Bij Strong-code zonder diepte-notitie: in Blok B expliciete markering `[diepte-notitie nog niet aanwezig in Kennis/diepte/]` plus master-toelichting als surrogaat. In A4-samenvatting: ontbreking wordt niet genoemd tenzij het de kern van de uitspraak raakt — A4 hoort begrijpelijk te zijn voor de eindgebruiker, niet een audit-document.
- Bij chronologie-vra