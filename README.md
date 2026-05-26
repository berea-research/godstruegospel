# godstruegospel — Concordant Bible-study corpus

A sola-scriptura research toolkit for studying the Hebrew, Aramaic and Greek source text of the Bible. The corpus produces text-grounded answers based exclusively on the original languages and a concordant translation discipline. It avoids confessional traditions, training-data echoes, and translation bias as primary inputs.

This repository hosts the corpus in two complementary forms. A **Claude Skill** with Python scripts and methodological protocols, packaged for use with Anthropic's Claude (or any other LLM that can mount a project folder). A **NotebookLM bundle set** of 25 large markdown files, ready to upload into Google NotebookLM for those who want to use the corpus without installing anything locally.

## What this project is

A computational corpus for biblical research that follows three rules without exception. First, every claim is traceable back to a verse in the Hebrew, Aramaic, or Greek source text bundled with this project. Second, all word-level analysis uses a concordant translation discipline: one source word is rendered consistently across passages so that the reader sees the underlying linguistic continuity, even where it diverges from common translations such as the KJV, NBG-1951 or Reina-Valera. Third, no theological school, church father, midrash tradition, or modern typologist is consulted; if a pattern is real, the source text itself must show it.

The corpus operates in three modes. A passive mode that answers questions about the Bible by retrieving the relevant verses, lexical entries and typological cross-references. An active mode that builds new typology entries through a seven-step protocol with verse-level proof. A cross-check mode that audits the corpus for internal consistency.

## How this project is used

This project offers three ways to consume the same underlying corpus. Pick the one that fits your tooling.

**1. The Python scripts** (`claude-skill/skill/`, `claude-skill/build-software/`)
Direct command-line access to the corpus: search by Strong-code, search by number-pattern, build reverse-lookup indexes, audit cross-references. These work standalone, no LLM required.

**2. The Claude Skill** (`claude-skill/skill/skill_v5_*.py`, `claude-skill/Kennis/protocollen/`)
A set of methodological protocols and trigger-detection logic designed to be loaded into an LLM-based assistant. The skill instructs the assistant to follow strict source-text discipline when answering Bible questions: every claim must trace back to a verse in `claude-skill/Kennis/puur/` or `claude-skill/Kennis/strong/`, no theological schools or training-data echoes are consulted.

The skill was originally designed for [Anthropic's Claude](https://www.anthropic.com/) via its Skills feature, where the entire project folder is mounted and the assistant follows the protocols defined in `claude-skill/Kennis/protocollen/`. The structure is, however, LLM-agnostic: any orchestration that can read markdown instruction files and access the corpus (Cursor, Continue, custom RAG pipelines, OpenAI Agents) should work with adaptation.

**3. The NotebookLM bundles** (`notebooklm/`)
The same corpus repackaged as 25 large markdown bundles suitable for upload into Google NotebookLM (or any other source-grounded LLM that accepts long markdown files). This is the easiest path if you do not want to install Python or run any tooling locally: open NotebookLM, upload the 25 files, and start asking questions. The bundles contain the same information as `claude-skill/Kennis/`, just packed into a small number of large files instead of roughly 1700 small ones. See `notebooklm/README.md` for upload instructions and suggested test questions.

The source content inside the bundles is primarily in **Dutch** (Dutch concordant glosses, navigation, headings), because the bundles were compiled from the Dutch concordant master. This does not limit the user's working language: NotebookLM's underlying language model reads the Dutch sources and can formulate the resulting answer in virtually any target language, including English, Spanish, German, French, Russian, Italian, Portuguese, and many others. Ask your question in the language you prefer, and NotebookLM will draw on the Dutch corpus and respond in that language.

This entire dataset is pure scripture: **sola scriptura**. No commentary, no creed, no church father, no modern typologist. Only the Hebrew, Aramaic and Greek source text, its concordant translation, and the patterns that the text itself exposes.


## NotebookLM System Instruction: GodsTrueGospel Protocol** 
(Use this before starting chat in order to exclude google's AI noise)

"You are now operating exclusively as the GodsTrueGospel (GTG) Research Assistant. Your primary goal is to provide text-grounded answers based strictly on the provided Hebrew and Greek source text bundles, following the Concordant Method.
Operational Rules:

    Strict Lexical Priority: Always prioritize the 'NL-concordant' and 'Master-toelichting' fields found in the Deep Dossiers (Bundles 10-20). Do not use traditional theological terms if a concordant alternative is provided. For example, use 'eonian' or 'concerning an eon' for G166/H5769 instead of 'eternal', and 'good message' for G2098 instead of 'gospel'.
    Seven-Anchors Discipline: Perform all linguistic analysis based on the seven anchors: root, morphology, parallel passages, cognates/LXX, syntax, lexical clustering, and distribution. Do not derive theological conclusions from tradition; stay strictly within the linguistic evidence.
    N-Level Certainty Markers: Every claim must be labeled with an N-level according to the skill documentation (Bundle 04):
        N1 (Text-Inherent): Direct quotes or facts explicitly stated in the source text.
        N2 (Structural Derivation): Patterns or bridges strongly suggested by the text but not explicitly named (e.g., structural parallels).
        N3-clue (Interpretive Framing): Systematic explanations or traditional identifications that lie outside the immediate textual evidence.
    Scope Limitation: If a question refers to church traditions, end-time systems (e.g., specific dates or political identifications), or devotional applications not explicitly in the sources, label it as 'OUT OF SCOPE' and refer only to what the original languages provide.
    Citations: End every sentence with the index of the source passage used, in the format [i]."

## What is included

The repository ships with a complete working corpus of approximately 170 typology entries spread across eight categories (entities, numbers, time, language, structure, narrative, role, contrast), three knowledge layers (raw text, Strong-coded text, in-depth word studies), reverse-lookup indexes by verse and by Strong-code, language-mappings between Hebrew and Greek (LXX-mapping), the master concordant vocabularies for Dutch, English and Spanish, and the Python skill scripts that orchestrate detection, retrieval and output.

For end-to-end documentation including the architectural principles, functional walkthrough, technical schemas, and the concordant-translation rationale, the project ships a full PDF in three languages:

- English: `claude-skill/docs/godstruegospel-documentation-en.pdf`
- Dutch: `claude-skill/docs/godstruegospel-documentation-nl.pdf`
- Spanish: `claude-skill/docs/godstruegospel-documentation-es.pdf`

The default `claude-skill/docs/godstruegospel-documentation.pdf` is a copy of the English version.

## Repository layout

```
claude-skill/              The Claude Skill: Python + protocols + canonical corpus
  Kennis/                  Knowledge corpus
    puur/                  Raw Hebrew/Aramaic/Greek text per Bible book (70 books)
    strong/                Source text annotated with Strong-codes
    diepte/                In-depth word studies per Strong-code
    masters/               Concordant translation masters (NL, EN, ES)
    index/                 Reverse indexes Strong -> verses
    protocollen/           Methodological protocols
    typologie/             Typology entries (170 entries across 8 categories)
  skill/                   Skill scripts
    skill_v5_preflight.py  Question-detection and trigger logic
    typologie_zoek.py      Source-text search helper
    fasen/                 Phase-specific skill manifests
    fase10/                Web-integration scripts (index builder, xref checker)
  docs/                    Documentation (PDF in EN/NL/ES, architecture notes)
  build-software/          Corpus-construction scripts (LXX mapping, batch tooling)
  Testen/                  Test suite (pairwise testset, runner, round reports)

notebooklm/                Same corpus repackaged as 25 large markdown bundles
                           for upload into Google NotebookLM (alternative usage path)

ATTRIBUTION.md             Upstream credits for the source texts
CONTRIBUTING.md            Contributor guide
LICENSE                    MIT license (project code and protocols)
LICENSE-DATA.md            Licensing details for the source-text data
publish.ps1                One-shot publish helper (maintainer tooling)
```

## Quick start

The skill scripts run on Python 3.10 or higher. No external services are required; all data is local to the repository.

To search a specific number-pattern across the source text:

```
python3 claude-skill/skill/typologie_zoek.py --cijfer 120
```

To search occurrences of a Strong-code:

```
python3 claude-skill/skill/typologie_zoek.py --strong G5179
```

To rebuild the reverse-lookup index after adding entries:

```
python3 claude-skill/skill/fase10/build_index.py
```

To audit cross-references between typology entries:

```
python3 claude-skill/skill/fase10/check_xrefs.py
```

To use the NotebookLM path instead, follow the upload instructions in `notebooklm/README.md`.

## Source-text attribution

The Hebrew, Aramaic and Greek source texts in `claude-skill/Kennis/puur/` and `claude-skill/Kennis/strong/` are derived from open-source biblical text projects. See `ATTRIBUTION.md` for full credits and licensing of the underlying text data.

## License

This project is released under the MIT License. See `LICENSE`.

## Contributing

Contributions follow the sola-scriptura discipline that defines the project. New typology entries must follow the V2 template under `claude-skill/Kennis/typologie/_entry-sjabloon.md` and pass the seven-step verification protocol in `claude-skill/Kennis/protocollen/typologie-detectie.md`. See `CONTRIBUTING.md`.
