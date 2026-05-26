# Actiepunten masters (NL/EN/ES)

> Status per 2026-05-09. Alle drie actiepunten afgerond.

## Actiepunt 1 — EN Grieks bouwen — VOLTOOID

**Voor:** 0/5482 entries (master-bestand bestond, maar `entries` was leeg).
**Na:** 5482/5482 entries, alle uniek, theology-vrij, gemiddelde toelichting 116 chars.

**Aanpak:** NL→EN auto-translator met 270 hand-curated Strong#-overrides voor de meest frequente woorden (lidwoorden, voornaamwoorden, voorzetsels, kernwoorden zoals theos, kurios, logos, pneuma, christos, ekklesia, aionios, daimon). Component-mapping op preposities (samen→together, neder→down, voor→before) en woordstammen (blijven→remain, spreken→speak). Theology blocklist actief: hell→Sheol-Hades, eternal→eonian, church→called-out, demon→daimon, devil→calumniator.

**Batches:** eg_batch_001 t/m eg_batch_022 (21 × 250 + 1 × 232).

## Actiepunt 2 — ES Grieks staart upgrade — VOLTOOID

**Voor:** 2732 entries met translit-codes in formaat `gr-{translit}-g{nummer}` (batches g_012 t/m g_022).
**Na:** 2732 entries met Spaanse concordante labels via NL→ES auto-translator. Alle 5482 ES Grieks entries uniek, theology-vrij.

**Aanpak:** NL→ES auto-translator met 60 prefix-mappings (samen→co, neder→abajo, voor→antes) en 280 woordstem-mappings. Translit-suffix als fallback waar Spaans equivalent ontbreekt voor traceerbaarheid.

**Resultaat:** Hybride mix van schone Spaanse vertalingen (`agua`, `libro-biblos`, `torre-purgos`, `talento-talanton`) en Spaans-met-translit waar de dict niet dekte (`recto-euthus`, `noveno-enatos`).

## Actiepunt 3 — ES Hebreeuws toelichting-diepte — VOLTOOID

**Voor:** Gemiddelde toelichting 64 chars (eerste 30 batches diep, batches 035-050 ondieper).
**Na:** Gemiddelde toelichting 163 chars (vs NL 161 / EN 148).

**Aanpak:** 3627 shortcut-entries (< 100 chars) hebben een toegevoegde sectie ` | NL-trad-anclas: ...` met de NL zeven-anker analyse via NL→ES auto-translator. Bestaande Spaanse RV60-conventies en hapax-info blijven intact aan de voorkant. Versreferenties (Gen 25:4, 1Cr 1:33) en Strong# refs (H1, H5278) beschermd via placeholder-mechanisme. Theology blocklist actief.

**Vocabulair:** 600+ NL→ES woordmappings. Output is hybride Spaans-Nederlands waar de auto-translator niet alle NL termen kon dekken.

---

## Eindstand drietalige master

| Taal | Hebreeuws | Grieks | Totaal | Avg toel He / Gr |
|------|-----------|--------|--------|------------------|
| NL   | 9510      | 5482   | 14992  | 161 / 230 chars  |
| EN   | 9510      | 5482   | 14992  | 148 / 116 chars  |
| ES   | 9510      | 5482   | 14992  | 163 / 90 chars   |

**Totaal: 44976 entries over drie talen × twee testaments.**

---

## Kwaliteits-tiers per master-onderdeel

**Tier 1 — Volledige zeven-anker hand-curated:**
- NL Hebreeuws (9510)
- NL Grieks (5482)
- EN Hebreeuws (9510)

**Tier 2 — Hand-curated met shortcuts:**
- ES Hebreeuws batches 1-30 (~3500 entries diep)
- ES Grieks batches g_001 t/m g_011 (2750 entries Spaanse labels)

**Tier 3 — Auto-translate met overrides:**
- EN Grieks (5482, met 270 hand-overrides voor top-frequentie)
- ES Hebreeuws toelichting-aanvulling (3627 shortcut-entries)
- ES Grieks staart g_012 t/m g_022 (2732 entries hybride Spaans-translit)

---

## Toekomstige verbeter-punten (geen actie nu)

- ES Grieks staart en ES Hebreeuws toelichting-aanvulling: Spanglish-fragmenten waar NL→ES dict niet alles dekt. Kan worden opgeschoond met (a) uitgebreidere dict, (b) handmatige doorloop, of (c) LLM-translation pass per entry.
- EN Grieks: enkele ouderwetse component-mappings tonen NL-leakage (bv. "toe-overhellen" werd al hersteld naar "toward-incline" maar er kunnen meer zitten).
- Een full uniqueness-en-theology audit over alle 44976 entries is wenselijk vóór productie-gebruik.

---

## Bestandslocaties

- `Kennis/concordant-nl-hebreeuws.json`
- `Kennis/concordant-nl-grieks.json`
- `Kennis/masters/en/concordant-en-hebreeuws.json`
- `Kennis/masters/en/concordant-en-grieks.json`
- `Kennis/masters/es/concordant-es-hebreeuws.json`
- `Kennis/masters/es/concordant-es-grieks.json`

## Build-scripts

- `build-software/append_batch_en.py` (append validator/writer, ondersteunt --taal en/es)
- `outputs/auto_translate_en_grieks.py` (NL→EN translator)
- `outputs/auto_translate_es_grieks.py` (NL→ES translator voor labels)
- `outputs/upgrade_es_grieks_staart.py` (ES Grieks staart upgrade)
- `outputs/translate_es_h_toelichting.py` (ES Hebreeuws toelichting-translator)
