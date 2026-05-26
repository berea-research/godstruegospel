# Entry-sjabloon — vaste structuur voor typologie-entries

Dit is het verplichte sjabloon voor elke entry in `Kennis/typologie/`. Een entry die niet aan dit sjabloon voldoet wordt niet opgenomen. Het sjabloon waarborgt vergelijkbaarheid, doorzoekbaarheid en reproduceerbaarheid.

Iedere entry kopieert dit sjabloon en vult de velden in. Velden mogen niet worden weggelaten — als een veld niet van toepassing is, schrijf "niet van toepassing" met korte motivatie.

---

## SJABLOON BEGINT HIER

```
# [Categorie] — "[Patroon-naam]"

## Meta

- **Status:** [pilot / geverifieerd / openstaand / herzien / betwist]
- **Opgesteld:** [JJJJ-MM-DD]
- **Laatste herziening:** [JJJJ-MM-DD]
- **Bron-discipline:** uitsluitend `Kennis/puur/` en `Kennis/strong/` (70 boeken). Geen training-input. Geen externe bronnen. Sola scriptura.
- **As 1 (categorieën):** [primair, plus eventuele cross-tags, bv. B1, B2, C2]
- **As 2 (hermeneutische lagen):** [een of meer van L1, L2, L3, L4]
- **As 3 (algemeen zekerheids-niveau):** [N1 / N2 / N3 — gemiddelde over voorkomens; per voorkomen apart te markeren]
- **Tags:** [zoekbare trefwoorden, vrij tekst]
- **Zie ook:** [paden naar verwante entries, bv. ../dagen/derde-dag.md]

## Hypothese

[Eén regel die het patroon formuleert. Geen meer. Helder, toetsbaar.]

## Zoekquery gebruikt

[Reproduceerbare commando's, bv:]
```bash
python3 skill/typologie_zoek.py --cijfer 120 --json
python3 skill/typologie_zoek.py --strongs G1540,G1501 --nabijheid --json
```

## Voorkomens (per cluster)

### Cluster X — [naam]

**[Boek-afkorting] [hoofdstuk]:[vers]** [N-niveau] — Hebreeuws/Aramees/Grieks-citaat met transliteratie. Korte context-uitleg. Wat de tekst zelf zegt.

[Per voorkomen één blok. Geen lange exegese, alleen vers + grondtekst-vorm + context.]

[Herhaal voor alle clusters die de coherentie-toets doorstaan.]

## Coherentie-toets

**Twee-getuigen drempel.** [Hoeveel onafhankelijke voorkomens per cluster.]
**Verspreiding over genres.** [Welke boekgenres dragen het patroon.]
**Wegnemingstoets.** [Houdt het patroon stand als een voorkomen wegvalt.]
**NT-OT verbinding.** [Wordt het patroon ergens door de Schrift zelf verbonden, en zo ja, waar.]

## Watermerk-verbinding

[Hoe wordt deze entry door de skill gebruikt bij vraag-beantwoording. Welke vragen activeren hem. Welke andere entries krijgen er een cross-reference naar.]

## Waarschuwingen

[Wat het patroon NIET zegt. Waar overbelasting dreigt. Welke voorkomens zwakker staan dan andere.]

## Vervolgvragen

[Wat moet nog onderzocht worden. Welke kandidaat-voorkomens zijn nog niet bron-getoetst.]
```

## SJABLOON EINDIGT HIER

---

## Toelichting per veld

**Status.**
- `pilot` = eerste versie, sjabloon-geverifieerd, inhoud bron-onderbouwd, nog niet door cross-check.
- `geverifieerd` = pilot heeft cross-check doorstaan, geen conflicten met andere entries, gebruikt door skill in productie.
- `openstaand` = hypothese geformuleerd, bron-zoek begonnen, entry nog niet compleet.
- `herzien` = aanpassing na nieuwe bevindingen, oude versie in git-history.
- `betwist` = conflict met andere entry of met directe lezing, wacht op arbitrage.

**Bron-discipline.**
Verplichte vermelding bovenaan elke entry. Maakt voor de lezer expliciet dat alle inhoud uit de 70 boeken in `Kennis/` komt.

**As 1 — Categorieën.**
Codes uit het raamwerk (`_raamwerk.md`). Een entry kan meerdere categorieën dragen. Eerste-genoemde is primair (bepaalt in welke submap het bestand staat). Verdere categorieën zijn secundair.

**As 2 — Hermeneutische lagen.**
L1 t/m L4. Een entry mag op meerdere lagen tegelijk werken. Bij elk voorkomen kan een specifieke laag worden aangewezen indien dat verheldert.

**As 3 — Zekerheids-niveau.**
Algemeen niveau staat in meta. Per voorkomen kan ook een specifiek N-niveau worden aangegeven in vierkante haken. De oplettende-lezer-presumptie geldt: N2-verbanden tellen volwaardig mee.

**Tags.**
Vrij-tekst trefwoorden voor doorzoekbaarheid. Bijvoorbeeld: "Mozes", "opstanding", "tempel", "jubelcyclus", "uittocht".

**Zie ook.**
Relatieve paden naar andere entries. Maakt het web zichtbaar.

**Hypothese.**
Eén regel. Geen "deze studie onderzoekt of mogelijk wellicht" — directe formulering. Toetsbaar.

**Zoekquery gebruikt.**
Letterlijke commando's. Wie morgen het script opnieuw runt vindt dezelfde verzen. Reproduceerbaar.

**Voorkomens per cluster.**
Per voorkomen: vers-referentie + grondtekst-citaat (Hebreeuws / Aramees / Grieks) + transliteratie + N-niveau in vierkante haken + korte context. Geen Strong-codes in de tekst zelf — die zitten in de zoekquery. Hooguit een appendix-veld voor wie de query wil reproduceren.

**Coherentie-toets.**
Vier vaste sub-velden: twee-getuigen, verspreiding over genres, wegnemingstoets, NT-OT verbinding. Maakt de robuustheid expliciet.

**Watermerk-verbinding.**
Hoe wordt deze entry actief gebruikt. Welke skill-output kan ervan profiteren. Verwijzingen naar Blok C en E in dossier-output.

**Waarschuwingen.**
Wat de typologie NIET zegt. Waar de skill moet stoppen. Welke voorkomens zwakker zijn. Voorkomt overbelasting van de typologische lading.

**Vervolgvragen.**
Wat de huidige sessie niet heeft kunnen doen. Wat de volgende ronde mag oppikken. Houdt het werk-traject zichtbaar.

## Niet-velden — wat NIET in een entry hoort

- Theologische conclusies ("dit bewijst dat ..." in stichtelijke zin).
- Buitenbijbelse referenties (kerkvaders, midrasj, traditie, moderne uitleggers).
- Strong-codes in de hoofdtekst (alleen in zoekquery-veld, optioneel als technische voetnoot).
- Geheugen-gestaafde uitspraken zonder bron-citaat.
- Cross-vertaling-gestaafde verbanden (alleen wat in grondtekst werkt).
- Lange exegetische uitwijdingen — entries blijven kort en citeerbaar.

## Voorbeeld-skelet (leeg) voor een nieuwe entry

```
# Tijd-typologie — "achtste dag"

## Meta
- Status: pilot
- Opgesteld: 2026-XX-XX
- Laatste herziening: 2026-XX-XX
- Bron-discipline: uitsluitend Kennis/puur/ en Kennis/strong/ (70 boeken). Sola scriptura.
- As 1 (categorieën): C1 (dagen), F (verhaal-typologie raakvlak)
- As 2 (hermeneutische lagen): L1, L2, L3
- As 3 (algemeen zekerheids-niveau): N1
- Tags: achtste-dag, besnijdenis, nieuwe schepping, opstanding-na-sabbat
- Zie ook: ../dagen/derde-dag.md, ../cijfers/8.md (toekomstig)

## Hypothese
De achtste dag markeert een nieuw begin na de zevenvoudige scheppings-cyclus.

## Zoekquery gebruikt
[commando's]

## Voorkomens
...
```

Dit skelet wordt per entry gekopieerd en gevuld. Geen entry zonder dit skelet.
