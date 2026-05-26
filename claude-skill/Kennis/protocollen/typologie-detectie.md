# Protocol — typologie-detectie en patroon-herkenning

Deze kennislaag legt vast hoe de godstruegospel skill typologische patronen in de Schrift detecteert, valideert en vastlegt. De typologie-laag is geen ornament en geen interpretatieve speculatie. Zij is een coherentie-check die de Schrift zelf legt door consistent woord-, cijfer-, naam-, plaats-, dag- en structuurgebruik. Patronen worden behandeld als watermerk van interne samenhang, niet als bewijs.

## Bron-discipline (HARDE REGEL)

Alle patronen in `Kennis/typologie/` worden uitsluitend opgebouwd uit:
- `Kennis/puur/[boek].jsonl` — Hebreeuwse en Griekse grondtekst
- `Kennis/strong/[boek].jsonl` — idem met Strong-codes
- `Kennis/diepte/[Strong].md` — woordstudie-laag
- `Kennis/index/strong-vers-{hebreeuws,grieks}.json` — omgekeerde index

Verboden bij opbouw van een typologie-entry:
- Buitenbijbelse bronnen (Bullinger's Number in Scripture, midrasj, kerkvaders, moderne typologen, concordant-agent, anderen)
- Geheugen-input vanuit Claude's training
- Patronen die in vertaling zichtbaar worden maar in de grondtekst verdwijnen
- Speculatieve verbindingen zonder grondtekst-tellingen

## Acceptatiedrempel: minstens twee getuigen

Een patroon wordt pas opgenomen wanneer:
1. Het in minimaal twee onafhankelijke passages of boeken voorkomt, EN
2. De voorkomens grondtekst-aantoonbaar zijn (Strong-code, Hebreeuwse of Griekse spelling, vers-referentie), EN
3. Het patroon door de tekst zelf wordt versterkt (door context, structuur, of expliciete cross-reference), EN
4. De skill kan tonen waarom het patroon coherentie suggereert in plaats van toeval.

Bij minder dan twee getuigen: niet opnemen. Wel noteren onder `Kennis/typologie/[categorie]/_kandidaten/` als hypothese voor latere verrijking.

## Vier patroon-soorten en hun zoekstrategie

**Soort 1 — Cijfer-typologie.**
Een cijfer komt herhaald voor in dezelfde betekenis-context door verschillende boeken. Voorbeelden van te onderzoeken cijfers: 3, 7, 8, 10, 12, 40, 50, 70, 120, 144, 153, 666, 1000.
Zoekstrategie: gebruik `skill/typologie_zoek.py --cijfer <waarde>` om alle voorkomens van een cijfer-combinatie te vinden in `Kennis/strong/`. Documenteer vers, context, betekenis-categorie.

**Soort 2 — Christustypen.**
Personen wiens leven, rol of functie een patroon vertoont dat bij Christus terugkomt. Voorbeelden: Adam, Noach, Abraham, Isaak, Jozef, Mozes, Jozua, Boaz, David, Salomo, Elia, Elisa, Jona, Simson, Gideon, Ehud, Melchizedek.
Zoekstrategie: leg het Hebreeuwse naamtype vast (Strong + betekenis), inventariseer rol-elementen (verworpen, sterven, opgewekt, redden, regeren), match tegen NT-uitspraken over Christus.

**Soort 3 — Naamlijnen.**
Namen die door hun betekenis een verhaal vertellen wanneer ze op volgorde worden gezet. Bekend voorbeeld is Genesis 5 (Adam → Noach), maar ook Ruth, of de twaalf stammen-namen.
Zoekstrategie: per naam de Hebreeuwse betekenis uit `Kennis/diepte/`, dan de naamvolgorde testen op coherent verhaal-narratief.

**Soort 4 — Plaats-typologie.**
Plaatsen waar herhaald gebeurtenissen plaatsvinden met patroon-betekenis. Voorbeelden: berg (Sinaï, Sion, Karmel, Tabor, Olijfberg), water (Rode Zee, Jordaan, Genesareth), woestijn, in-Israël/buiten-Israël, Hebron, Bethlehem, Jeruzalem.
Zoekstrategie: per plaats inventariseer alle vers-voorkomens via Strong-naam, groepeer naar gebeurtenis-type, zoek patroon.

**Soort 5 — Dag-typologie.**
"Eerste dag", "derde dag", "achtste dag", "zevende dag", enzovoort, als terugkerende markeringen. Bijvoorbeeld de derde dag (Gen 1:13, Gen 22:4, Hosea 6:2, opstanding).
Zoekstrategie: zoek alle voorkomens van dag-aanduidingen in grondtekst, groepeer per dag-nummer, signaleer betekenis-clusters.

**Soort 6 — Structurele typologie.**
Tabernakel/tempel als hemels patroon (Hebr 8:5), feestcyclus als heilshistorie, sabbatstructuur, chiasme, parallellisme. Vereist intensieve cross-tekstuele analyse.

**Soort 7 — Woordklank-verbanden.**
Hebreeuwse paronomasie (woordspel), alliteratie, polysemie. Voorbeeld: dabar (woord, H1697) en devash (honing, H1706) delen dalet-bet en worden expliciet verbonden in Psalm 19:11 en Psalm 119:103. Dit type patroon is alleen in de grondtekst zichtbaar en gaat in vertaling verloren.
Zoekstrategie: gebruik Strong-codes om wortel-verwantschap te vinden, controleer of de tekst de verwantschap bewust uitbuit door beide woorden in nabijheid te plaatsen.

## Werkwijze voor het opbouwen van een nieuwe typologie-entry

**Stap T1 — Hypothese.**
Formuleer het te onderzoeken patroon in één regel. Voorbeeld: "Het cijfer 120 markeert in de Schrift een grens of voltooiing van mensgerelateerde tijd."

**Stap T2 — Grondtekst-zoeken.**
Run `skill/typologie_zoek.py` of equivalente Strong-zoekquery om ALLE voorkomens te vinden. Geen samenvatting uit geheugen.

**Stap T3 — Inventarisatie.**
Voor elk voorkomen: vers-referentie, Hebreeuwse of Griekse vorm, context (wat gebeurt er), gebruik (cijfer als leeftijd, periode, aantal, enz.).

**Stap T4 — Categorisering.**
Groepeer de voorkomens naar betekenis-context. Welke clusters ontstaan? Vallen ze samen of zijn ze verstrooid?

**Stap T5 — Coherentie-toets.**
Wijst de cluster op een patroon dat de tekst zelf onderschrijft, of is het een toevallige opeenstapeling? Vraag: zou het patroon nog stand houden als ik één voorkomen wegneem?

**Stap T6 — Watermerk-verbinding.**
Hoe kan dit patroon dienen als coherentie-check elders in de skill? Bij chronologie? Bij naam-uitleg? Bij christus-type-herkenning?

**Stap T7 — Vastlegging.**
Schrijf de entry in `Kennis/typologie/[categorie]/[patroon].md` met: hypothese, alle voorkomens met grondtekst-citaat, clustering, coherentie-conclusie, waarschuwingen (waar werkt het niet, waar wordt het overbelast).

## Hoe de skill typologie inzet bij output

Bij elk antwoord:
1. Pre-flight detecteert of typologische scan relevant is (op basis van vraag-signalen: cijfer genoemd, persoon genoemd, plaats genoemd, dag-aanduiding, structuur-vraag).
2. Indien ja: laad relevante typologie-entries uit `Kennis/typologie/`.
3. In Blok C van de output: presenteer de typologische cross-references als afzonderlijke sectie.
4. In Blok E: gebruik typologie als coherentie-check ("watermerk"). Wanneer een directe lezing samenvalt met een typologisch patroon: markeer als bevestigend. Wanneer een directe lezing botst met een vast patroon: markeer als signaal voor heronderzoek.

Belangrijk: typologie is GEEN bewijsmiddel. De skill gebruikt patronen om coherentie te ondersteunen, nooit om een directe lezing te overrulen of te dwingen. Bij conflict tussen directe lezing en typologisch patroon wint altijd de directe lezing, met de vermelding van het conflict als signaal voor de gebruiker.

## Wat dit niet wordt

Een vergaarbak voor speculatieve symboliek. Een schaduw-corpus dat naast de grondtekst leeft. Een kanaal voor kerkelijke traditie via de achterdeur. Een verzameling van "leuke patronen" zonder grondtekst-onderbouwing.

Wat dit wel wordt: een progressieve, bron-onderbouwde inventaris van patronen die de Schrift zelf legt. Geen entry is af zonder grondtekst-referenties. Elke entry is openstaand voor uitbreiding wanneer nieuwe voorkomens worden gevonden.
