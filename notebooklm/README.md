# NotebookLM bundles

This folder contains the **same knowledge as the rest of this repository**, repackaged as 25 large markdown bundles that can be uploaded directly to Google NotebookLM (or any other source-grounded LLM that accepts long markdown files).

> Important: no new information lives here. Every bundle is a recompilation of the source data in `../claude-skill/Kennis/` (depth dossiers, typology entries, source text per Bible book, Strong-code indexes). If you want the canonical, file-per-entry view of the corpus, use the main repository layout. If you want the corpus packed into a small number of large sources suitable for upload into NotebookLM, use this folder.

## Why this exists

NotebookLM and similar tools impose limits on the number of sources per notebook (typically tens, not thousands) and benefit from large, semantically coherent source files. The canonical corpus under `../claude-skill/Kennis/` contains roughly 1700 files — too many to upload one-by-one. These 25 bundles consolidate the corpus into a size and shape that NotebookLM can index without losing the source-text discipline of the project.

## What is in this folder

25 markdown bundles, total about 29 MB. Largest bundle: about 3.4 MB. All bundles stay under NotebookLM's 500,000-word per-source limit.

### Depth dossiers (5 bundles)

| File | Contents |
|---|---|
| `10-Diepte-Hebreeuws-H1-tm-H2000.md` | 196 depth dossiers, Hebrew Strong-codes H1 to H2000 |
| `11-Diepte-Hebreeuws-H2001-tm-H4000.md` | 231 depth dossiers, Hebrew Strong-codes H2001 to H4000 |
| `12-Diepte-Hebreeuws-H4001-tm-H6000.md` | 209 depth dossiers, Hebrew Strong-codes H4001 to H6000 |
| `13-Diepte-Hebreeuws-H6001-en-hoger.md` | 279 depth dossiers, Hebrew Strong-codes H6001 and above |
| `20-Diepte-Grieks-Alle-Strong-Codes.md` | 272 depth dossiers, all Greek Strong-codes |

### Typology (8 bundles)

| File | Contents |
|---|---|
| `30-Typologie-A-Entiteit.md` | 74 entries — Christ-types as entities |
| `31-Typologie-B-Cijfer.md` | 13 entries — number-pattern typology |
| `32-Typologie-C-Tijd.md` | 16 entries — day and time patterns |
| `33-Typologie-D-Taal.md` | 8 entries — word-sound and paronomasia |
| `34-Typologie-E-Structuur.md` | 15 entries — tabernacle and feast-cycle structures |
| `35-Typologie-F-Verhaal.md` | 17 entries — narrative patterns |
| `36-Typologie-G-Rol.md` | 15 entries — priest, king, prophet roles |
| `37-Typologie-H-Contrast.md` | 12 entries — Adam-Christ, flesh-spirit contrasts |

### Source text per Bible-book group (9 bundles)

| File | Contents |
|---|---|
| `40-Grondtekst-Pentateuch.md` | Genesis through Deuteronomy |
| `41-Grondtekst-Geschiedenis-OT.md` | Joshua through Esther |
| `42-Grondtekst-Wijsheid-OT.md` | Job, Psalms, Proverbs, Ecclesiastes, Song of Songs |
| `43-Grondtekst-Profeten-Groot.md` | Isaiah through Daniel |
| `44-Grondtekst-Profeten-Klein.md` | Hosea through Malachi |
| `50-Grondtekst-Evangelien.md` | Matthew through John |
| `51-Grondtekst-Handelingen.md` | Acts |
| `52-Grondtekst-Brieven-Paulus.md` | Romans through Hebrews |
| `53-Grondtekst-Algemene-Brieven-en-Openbaring.md` | James through Revelation |

### Strong-code lookup indexes (3 bundles)

| File | Contents |
|---|---|
| `60-Strong-Index-Hebreeuws.md` | Hebrew Strong-codes H1 to H4000 with Dutch concordant gloss and all occurrences |
| `61-Strong-Index-Hebreeuws-H4001-en-hoger.md` | Hebrew Strong-codes H4001 and above with Dutch gloss and occurrences |
| `62-Strong-Index-Grieks.md` | All Greek Strong-codes with Dutch gloss and occurrences |

Across the three index bundles, 14,984 Strong-codes are individually addressable with their Dutch concordant rendering and full verse-occurrence list.

## Language note

The bundles themselves are written in **Dutch** (filenames, glosses, navigation text), because they were compiled from the Dutch concordant master. The underlying Hebrew, Aramaic and Greek source text inside the bundles is unchanged from the canonical corpus.

This does not limit the working language of the user. NotebookLM's underlying language model reads the Dutch sources and can formulate the resulting answer in virtually any target language, including English, Spanish, German, French, Russian, Italian, Portuguese, and many others. Ask your question in the language you prefer; NotebookLM will draw on the Dutch corpus and respond in that language.

If you need a pre-rendered English or Spanish concordant set instead of relying on translation at query-time, regenerate the bundles from the corresponding master in `../claude-skill/Kennis/masters/`.

## How to use these in NotebookLM

1. Open NotebookLM and create a new notebook (suggested name: "godstruegospel knowledge base" or similar).
2. Click "Add source" and upload all 25 bundles from this folder.
3. Wait for NotebookLM to process each bundle. The larger bundles (over 200,000 words) can take a few minutes.
4. Start asking questions. The notebook is grounded in the source corpus only; NotebookLM will cite which bundle each claim comes from.

## Suggested test questions

After upload, validate the notebook with questions across the four layers:

Method and philosophy (covered by depth dossiers and typology bundles):

- What is the seven-anchor method used in this corpus?
- How does the chronology protocol work for source-text dating?

Concrete word-level questions (depth dossiers, bundles 10-20):

- What does G1085 *genos* mean and how is it rendered concordantly?
- What is the difference between G1074 *genea* and G1085 *genos*?

Typological questions (bundles 30-37):

- Where is Abraham used as a type of Christ?
- What is the meaning of the number 40 in the source text?

Source-text questions (bundles 40-53):

- What does the source text of Genesis 1:1 literally say?
- Which Strong-codes appear in John 1:1?

Distribution and lookup (bundles 60-62):

- Where does H4194 *mawet* (death) occur in the Old Testament? List all occurrences.
- In which New Testament books does G2222 *zoe* (life) appear most often?
- Which Strong-codes are concordantly translated "covenant"?

If the answers come back well-cited from the appropriate bundles, the notebook is set up correctly.

## Regenerating the bundles

The bundles are derived from the canonical corpus under `../claude-skill/Kennis/`. A regeneration script that rebuilds all 25 bundles from the source data lives outside this folder (private to the project maintainer); the script is not shipped publicly because it depends on intermediate working files not in this repository. If you want to regenerate the bundles yourself after editing the corpus, open an issue on the repository — instructions can be shared.

## License

Same MIT license as the rest of the repository. See `../LICENSE`.
