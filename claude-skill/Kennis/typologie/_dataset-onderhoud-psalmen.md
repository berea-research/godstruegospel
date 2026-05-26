# Dataset-onderhoud — Psalmen-tagging-issue

> Verzameld in Fase 10 web-integratie op 2026-05-08.
> Patroon: Psalmen-tagging in `Kennis/strong/psa-*.jsonl` is structureel onvolledig. Sleutelpassages met typologische lading zijn niet via standaard Strong-grep vindbaar; geverifieerd via directe woord-controle of NT-citaat.

## Probleem-omschrijving

Tijdens Fase 1 cijfer-typologie V2-herziening (2026-05-08) zijn meerdere Psalmen-passages niet teruggekomen via standaard zoekquery's. Sleutel-Strong-codes (H505 elef, H7651 sheva, H7657 shiv'im, H7659 shiv'atayim) ontbreken in deze verzen, terwijl de Hebreeuwse tekst zelf de cijfers wel bevat. Dit is een structureel-onderhouds-issue van de `Kennis/strong/psa-*.jsonl` bestanden, niet een entry-issue.

## Geïdentificeerde gemiste passages

| Vers | Verwacht Strong | Cijfer | Entry-relevantie | Symptoom |
|---|---|---|---|---|
| Ps 12:6 | H7659 shiv'atayim | 7 (zevenmaal-gelouterd zilver) | `./B_cijfer/7.md` Cluster F + `./B_cijfer/zilver` cross-link | Niet via grep H7659 vindbaar |
| Ps 50:10 | H505 elef | 1000 (vee op 1000 bergen) | `./B_cijfer/1000.md` Cluster C | Niet via grep H505 vindbaar |
| Ps 79:12 | H7659 of H7651 | 7 (zevenvoudig vergelden) | `./B_cijfer/7.md` Cluster F | Niet via grep vindbaar |
| Ps 90:4 | H505 elef | 1000 (1000 jaar als dag) | `./B_cijfer/1000.md` Cluster B | Niet via grep H505; geverifieerd via 2 Pet 3:8 NT-citaat |
| Ps 90:10 | H7657 shiv'im | 70 (mensenleven 70 jaar) | `./B_cijfer/70.md` Cluster J | Niet via grep H7657 vindbaar |
| Ps 105:8 | H505 elef | 1000 (1000 geslachten verbond) | `./B_cijfer/1000.md` Cluster D | Niet via grep H505 vindbaar |

Verzameling van zes structurele gevallen — vermoedelijk meer als systematisch wordt onderzocht.

## Mogelijke oorzaken (te verifiëren)

1. **Tagging-fout in S4A-broncoderingen** — sommige Strong-codes ontbreken in `psa-*.jsonl` waar ze in andere boeken wel staan.
2. **Vorm-variatie**: Hebreeuwse cijfers hebben varianten die mogelijk onder andere Strong-codes vallen. Bv `chamishshim shanah` (50 jaar) versus `chamishshim` los (50 algemeen).
3. **Samenstelling-filter te streng**: cijfers binnen samenstellingen (bv "70 jaar" als één term in Hebreeuws) worden door samenstelling-filter weggehaald.

## Aanbevolen acties (toekomstige Fase 10 dataset-sessie)

1. **Systematische audit van Psalmen-tagging**: alle Strong-codes voor cijfers (H8147, H7969, H702, H2568, H8337, H7651, H8083, H8672, H6235, H6240, H6242, H7970, H705, H2572, H8346, H7657, H8084, H4948, H3967, H8175, H505) crosschecken tegen Hebreeuwse tekst voor minstens deze 6 verzen.

2. **Bredere check**: zelfde audit voor andere boeken die mogelijk ook missing tagging hebben (Eze 43:27 voor cijfer 8 was eerder al gemarkeerd; 2 Kn 5:10/14 voor cijfer 7 was eerder al gemarkeerd).

3. **Update audit-script** `audit_v2.py` met een tagging-completeness-check per Strong-code.

## Andere dataset-issues uit Fase 10

### Op 21:19-20 12 edelstenen
Mogelijk samenstelling-filter te streng voor Op 21:19-20 vermelding van twaalf specifieke edelstenen. Te onderzoeken in dataset-sessie.

### Samengestelde getalswoorden Grieks
Joh 21:11 `pentēkontatriōn` (= 153) wordt door `--cijfer 153` algoritme niet automatisch herkend. Bredere klasse: `decapent` (15), `tessareskaideka` (14). Verbetering vereist samenstelling-detectie.

### Aramees voor 70
Daniël heeft delen Aramees. Mogelijk H7240 of vergelijkbaar voor 70 in Aramese passages. Te onderzoeken voor compleetheid.

### Status-marker D_taal entries
Alle 8 D_taal entries (gematria-inventaris, hapax-overzicht, paronomasie-dabar-devash, paronomasie-shalom-shalem, polysemie-elohim, wortel-chesed, wortel-rua, wortel-tsedek) hebben status `pilot · Opgesteld 2026-05-05` zonder `bron-geverifieerd 2026-05`-marker. Deze entries volgen V1-sjabloon, niet de strikte V2-discipline van 2026-05-07/08. Ze zijn in eerdere actieplan-rondes als "Fase 5 voltooid" gemarkeerd, maar voor compleetheid van Fase 10 is een **eigen V2-herzieningsronde voor D_taal** aanbevolen.

### Cross-reference asymmetrie
138 asymmetrische cross-refs tussen entries. 76 entries zonder inkomende cross-refs (60% van entries is "eiland" qua inkomende refs). Dit is normaal voor entries die alleen via hun eigen ankers worden bereikt, maar kandidaten voor cross-link-toevoegingen kunnen handmatig worden geïdentificeerd.

## Status

Document opgesteld op 2026-05-08 als onderdeel van Fase 10 web-integratie. Niet uitgevoerd; verzameling van issues voor toekomstige onderhouds-sessie.
