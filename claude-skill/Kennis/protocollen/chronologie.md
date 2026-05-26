# Protocol — chronologie en multi-vers tijdrekening

Deze kennislaag legt vast hoe de godstruegospel skill chronologische vragen behandelt. De skill werkt vanuit de Hebreeuwse en Griekse grondtekst en trekt bron-onderbouwde conclusies. Waar de tekst meerduidig is, raadpleegt de skill `interpretatieve-keuzes.md` voor een per-keuzepunt bron-weging. Externe historische tradities worden vermeld als context, niet als alternatieve leeshoeken op gelijke voet.

## De zes principes

**Principe 1 — Inclusief tellen is bijbels.**
De Hebreeuwse Bijbel telt jaren inclusief: het eerste levensjaar begint bij de geboorte en wordt als jaar één geteld. Bron-onderbouwing in Lev 23:36, Lev 25:8, en NT-passages als Joh 20:26 ("na acht dagen" = een week) en de "derde dag" van de opstanding. Exclusief tellen is een moderne conventie zonder bijbelse tekstondersteuning. De skill gebruikt inclusief tellen als standaard.

**Principe 2 — Halve-jaar correctie als verwerking-methode.**
De tekst geeft geen exacte verwekkingsmaand binnen het levensjaar. Wie elke leeftijd op een exact punt vastlegt, introduceert schijnprecisie. De skill verwerkt dit als marge: per generatie ongeveer een half jaar onzekerheid, over Genesis 5 + Genesis 11 (18 generaties) cumulatief ongeveer 9 jaar. Eindgetallen worden gepresenteerd als interval, niet als puntwaarde.

**Principe 3 — Cross-tekstuele kruisreferenties zijn dwingend.**
Het Nieuwe Testament becommentarieert het Oude. Zulke commentaren zijn bron-getuigenissen die niet kunnen worden weggepoetst. Klassieke voorbeelden:
- Hand 7:4 + Gen 11:32 + Gen 12:4 → Terach was 130 bij Abrams geboorte (niet 70)
- Hand 7:2-3 → de eerste belofte aan Abram was vóór Charan (niet bij vertrek op 75)
- Galaten 3:17 + Genesis 15:13 → 30 jaar verschil tussen belofte en geboorte nageslacht

Deze kruisreferenties zijn niet "interpretatieve speculatie" maar directe NT-OT cross-getuigenissen. Wie ze negeert kiest voor een lezing die de bijbel zelf tegenspreekt.

**Principe 4 — Bij meerduidigheid: bron-weging, geen pluralisme.**
Op enkele plaatsen biedt de tekst meer dan één lezing zonder dat één optie evident sterker is. Voor die punten consulteert de skill `interpretatieve-keuzes.md`, kiest expliciet de meest bron-onderbouwde optie, vermeldt het zwakkere alternatief met de reden van zwakte. Alleen bij genuinely 50/50 keuzes wordt het keuzepunt open gelaten en de gebruiker geïnformeerd.

**Principe 5 — Onderscheid binnen-bijbels en extra-bijbels.**
De Bijbel heeft een continue chronologische lijn van Adam tot Christus via Genesis 5, Genesis 11, Exodus 12:40, 1 Koningen 6:1, regeringsjaren in Koningen + Kronieken, Ezechiël 4 (390+40 dagen-jaren als profetische bevestiging), Jeremia 25:11 (70 jaar verwoesting), en Daniël 9 (zeventig weken). Daarna stopt de bijbel-eigen kalender. Conversie naar BC/AD-jaren of "vandaag" gaat via een extra-bijbels historisch ankerpunt. De skill markeert die conversie expliciet als `[EXTERNE ANKERING]` en presenteert geen voorkeur tussen de gangbare ankerpunten.

**Principe 6 — Geen training-bias als default.**
De skill behandelt geen enkele historische chronologische traditie (Ussher, Seder Olam, Septuagint-Byzantijns, modern-archeologisch) als de "neutrale default". Al die tradities zijn samengesteld uit specifieke keuzes op de meerduidige punten. De skill werkt vanuit de bron en de keuzes uit `interpretatieve-keuzes.md`, niet vanuit aangeleerde tradities.

## De zeven werkstappen (chronologie-protocol C1–C7)

Voor elke vraag waarvoor het preflight-script `is_chronologie_vraag = true` rapporteert, doorloopt de skill onverkort deze stappen:

**C1 — Vragen-decompositie.**
Splits de vraag in atomaire vers-lookups. Maak een lijst van alle benodigde verzen vóór je begint te tellen. Voor "Adam tot X" vragen is de minimale set:
- Genesis 5:3, 5:6, 5:9, 5:12, 5:15, 5:18, 5:21, 5:25, 5:28 (tien aartsvaders pre-flood)
- Genesis 7:6 (Noach bij zondvloed)
- Genesis 11:10, 11:12, 11:14, 11:16, 11:18, 11:20, 11:22, 11:24, 11:26, 11:32 (negen post-flood plus Terach overlijden)
- Genesis 12:4 (Abram bij vertrek)
- Genesis 15:13, Genesis 21:5 (cross-ref voor belofte-tijdstip)
- Handelingen 7:2-3, Handelingen 7:4 (cross-references vóór-Charan en Terach)
- Galaten 3:17 (430 jaar belofte tot wet)
- Exodus 12:40 (verblijf 430 jaar)
- 1 Koningen 6:1 (480 jaar tot tempel-fundering)
- 1 Koningen 6:38, 1 Koningen 7:1, 1 Koningen 9:10 (bouwtijd en voltooiing)
- 2 Koningen + 2 Kronieken regeringsjaren Juda (indien doorgerekend tot val Jeruzalem)
- Ezechiël 4:5–6 (390 + 40 dagen-jaren)
- Jeremia 25:11–12 (70 jaar verwoesting)
- Daniël 9:24–27 (zeventig weken)

**C2 — Bron-extractie per vers.**
Haal elk vers op uit `Kennis/strong/[boek].jsonl`. Toon Hebreeuws of Grieks woord, transliteratie, Strong-code voor elk cijfer-element. Geen optelling vóór alle bronnen op tafel liggen.

**C3 — Decoding-tabel.**
Maak een expliciete decoding-tabel: welk Strong-cijfer = welke waarde. Niet uit geheugen invullen — uit `Kennis/diepte/[Strong].md` waar beschikbaar, anders uit de cijfer-Strongs tabel hieronder.

**C4 — Interpretatieve keuzes maken via bron-weging.**
Voor elk keuzepunt uit `interpretatieve-keuzes.md`: pas de werk-conclusie toe (de bron-onderbouwde optie). Vermeld het zwakkere alternatief met reden van zwakte. Bij genuinely 50/50 keuzes: open laten en gebruiker informeren.

**C5 — Werk-redenering tonen.**
Toon de optelling stap voor stap, met bij elk cumulatief tussentotaal de bronvers-attributie. Geen sprong naar eindgetal zonder zichtbare keten.

**C6 — Eindgetal met onzekerheidsmarge.**
Geef het eindgetal met expliciete vermelding van: gebruikte methode (inclusief tellen, halve-jaar correctie, bron-onderbouwde keuzes per punt), gebruikte interpretatieve keuzes uit C4, en waar de chronologie eindigt (bv. AM 3000 = voltooiing tempel + paleis Salomo). Marges in plaats van puntwaarden waar de tekst onzekerheid laat.

**C7 — Externe ankering apart.**
Conversie naar BC/AD-jaren of "vandaag" gaat NIET uit de grondtekst. Markeer dit als `[EXTERNE ANKERING — datum-x]` met de gebruikte historische datering. De skill biedt op verzoek de bekende ankerpunten (Ussher 4004, modern-archeologisch ~967 v.C. tempel, Joodse kalender 3761) zonder voorkeur uit te spreken.

## Cijfer-Strongs decoderingstabel

Bron: `Kennis/strong/[boek].jsonl` cross-references plus `Kennis/diepte/[Strong].md` waar aanwezig.

| Strong | Translit | Waarde |
|---|---|---|
| H259 | echad | 1 |
| H8147 | shtaim / shnayim | 2 |
| H7969 | shalosh / sheloshah | 3 |
| H702 | arba | 4 |
| H2568 | chamesh / chamishah | 5 |
| H8337 | shesh | 6 |
| H7651 | sheba / shibah | 7 |
| H8083 | shemoneh | 8 |
| H8672 | tesha / tishah | 9 |
| H6235 | eser / asarah | 10 |
| H6240 | asar (samenstellingen 11–19) | +10 |
| H6242 | esrim | 20 |
| H7970 | sheloshim | 30 |
| H705 | arbaim | 40 |
| H2572 | chamishim | 50 |
| H8346 | shishim | 60 |
| H7657 | shibim | 70 |
| H8084 | shemonim | 80 |
| H8673 | tishim | 90 |
| H3967 | me'ah (enk.) / mathim (dual = 200) / mauth (mv. = honderden) | 100 |
| H505 | eleph | 1000 |
| H8141 | shanah / shanim (jaar/jaren, marker) | — |

Belangrijke noten:
- "shesh mauth shanah" = 6 × 100 jaar = 600 jaar (combinatie cijfer + meervoud-honderden + jaar-marker).
- Dual-vorm (mathim) is 200, niet 100 × 2 als losse cijfers.
- H8141 (shanah) markeert dat voorgaande getallen jaren betreffen, geen cijferwaarde.

## Werk-conclusies bij toepassing van het protocol

Onderstaande tabel toont de werk-conclusies die de skill bereikt door de zes principes en zeven stappen toe te passen, met de bron-onderbouwde keuzes uit `interpretatieve-keuzes.md`. Marges zijn intervallen, geen puntwaarden.

| Anker | AM (skill werk-conclusie, met marge) | Bronverzen + keuzepunten |
|---|---|---|
| Schepping Adam | 0 | Gen 1:26-27, Gen 5:1 |
| Geboorte Noach | ±1056 | Gen 5:3+6+9+12+15+18+21+25+28, inclusief tellen |
| Begin zondvloed | ±1656 | + Gen 7:6 |
| Geboorte Arpachsad | ±1658 | + Gen 11:10 |
| Geboorte Terach | ±1878 | + Gen 11:12-24 |
| Geboorte Abram | ±2008 | + Gen 11:26 + 11:32 + 12:4 + Hand 7:4 (Keuzepunt 3: Terach 130) |
| Eerste belofte aan Abram | ±2078 | + Gen 12:1-3, Hand 7:2-3, Gal 3:17, Gen 15:13, Gen 21:5 (Keuzepunt 4: Abram 70 vóór Charan) |
| Vertrek uit Charan | ±2083 | + Gen 12:4 (75) |
| Uittocht | ±2508 | + Gal 3:17 (430 jaar belofte tot wet) |
| Tempelfundering | ±2988 | + 1 Kon 6:1 (480 jaar) |
| Voltooiing tempel + paleis | ±3008 | + 1 Kon 6:38 + 7:1 + 9:10 (Keuzepunt 5: voltooiing als primair eindpunt) |
| Val Jeruzalem | ±3438 | + regeringsjaren Koningen/Kronieken + Ez 4:5-6 (390+40 dagen-jaren = 430) |
| Eerste jaar Kores | ±3508 | + Jer 25:11 (70 jaar verwoesting) |
| Christus (geboorte / kruisiging) | ±3998-4008 | + Dan 9:24-27 (Keuzepunt 6: 490 directe lezing of 500 met jubelstructuur) |

Bij standaard-output van de skill voor "Adam tot vandaag" is het laatste binnen-bijbelse ankerpunt = Christus per Daniël 9. Conversie naar 2026 n.C. vergt extra-bijbelse historische ankering en wordt expliciet gemarkeerd.

Met Christus' geboorte als anker rond ±4 v.C. komt 2026 n.C. uit op ongeveer AM 6030 ± marge. Met Christus' kruisiging als anker rond ±30 n.C. komt 2026 n.C. uit op ongeveer AM 5996 ± marge. De skill biedt beide ankeringen aan en markeert ze beide als extern.

## Verboden bij chronologie-output

De volgende fouten zijn structureel en moeten worden vermeden:
- Eén waarde noemen zonder de bron-onderbouwde keuzes uit `interpretatieve-keuzes.md` te tonen.
- Stilzwijgend Ussher (4004 v.C.), Joods AM (3761), of Septuagint-Byzantijns als default toepassen.
- Een NT-OT cross-reference (zoals Hand 7:2-3 of Hand 7:4) verzwijgen of als optioneel behandelen.
- Het eindpunt "vandaag" of een BC/AD-jaartal noemen zonder externe ankering te markeren.
- Genesis 5/11 leeftijden uit geheugen reconstrueren in plaats van uit `Kennis/strong/gen.jsonl` halen.
- Een "leeshoeken-pluralisme" presenteren waarin gelijk-onderbouwde alternatieven worden voorgesteld terwijl de bron-weging duidelijk één kant op leunt.

Wanneer Claude één van deze fouten dreigt te maken, stopt de skill en vraagt verduidelijking aan de gebruiker.
