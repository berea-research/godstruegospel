# godstruegospel — Concordant Bible-study skill

A sola-scriptura research toolkit for studying the Hebrew, Aramaic and Greek source text of the Bible. The toolkit produces text-grounded answers based exclusively on the original languages and a concordant translation discipline. It avoids confessional traditions, training-data echoes, and translation bias as primary inputs.

## What this project is

A computational corpus and skill for biblical research that follows three rules without exception. First, every claim is traceable back to a verse in the Hebrew, Aramaic, or Greek source text bundled with this project under `Kennis/puur/` and `Kennis/strong/`. Second, all word-level analysis uses a concordant translation discipline — one source word is rendered consistently across passages so that the reader sees the underlying linguistic continuity, even where it diverges from common translations such as the KJV, NBG-1951 or Reina-Valera. Third, no theological school, church father, midrash tradition, or modern typologist is consulted; if a pattern is real, the source text itself must show it.

The skill operates in three modes. A passive mode that answers questions about the Bible by retrieving the relevant verses, lexical entries and typological cross-references from the corpus. An active mode that builds new typology entries through a seven-step protocol with verse-level proof. A cross-check mode that audits the corpus for internal consistency.

## What is included

The repository ships with a complete working corpus of approximately 170 typology entries spread across eight categories (entities, numbers, time, language, structure, narrative, role, contrast), three knowledge layers (raw text, Strong-coded text, in-depth word studies), reverse-lookup indexes by verse and by Strong-code, language-mappings between Hebrew and Greek (LXX-mapping), the master concordant vocabularies for Dutch, English and Spanish, and the Python skill scripts that orchestrate detection, retrieval and output.

For end-to-end documentation including the architectural principles, functional walkthrough, technical schemas, and the concordant-translation rationale, the project ships a full PDF in three languages:

- English: `docs/godstruegospel-documentation-en.pdf`
- Dutch: `docs/godstruegospel-documentation-nl.pdf`
- Spanish: `docs/godstruegospel-documentation-es.pdf`

The default `docs/godstruegospel-documentation.pdf` is a copy of the English version.

## Repository layout

```
Kennis/                  Knowledge corpus
  puur/                  Raw Hebrew/Aramaic/Greek text per Bible book (70 books)
  strong/                Source text annotated with Strong-codes
  diepte/                In-depth word studies per Strong-code
  masters/               Concordant translation masters (NL, EN, ES)
  index/                 Reverse indexes Strong → verses
  protocollen/           Methodological protocols
  typologie/             Typology entries (170 entries across 8 categories)
skill/                   Skill scripts
  skill_v5_preflight.py  Question-detection and trigger logic
  typologie_zoek.py      Source-text search helper
  fasen/                 Phase-specific skill manifests
  fase10/                Web-integration scripts (index builder, xref checker)
docs/                    Documentation
  godstruegospel-documentation.pdf       Full English documentation
  architectuur-v2.0.md                   Architecture notes
build-software/          Corpus-construction scripts (LXX mapping, batch tooling)
Testen/                  Test suite (pairwise testset, runner, round reports)
```

## Quick start

The skill scripts run on Python 3.10 or higher. No external services are required; all data is local to the repository.

To search a specific number-pattern across the source text:

```
python3 skill/typologie_zoek.py --cijfer 120
```

To search occurrences of a Strong-code:

```
python3 skill/typologie_zoek.py --strong G5179
```

To rebuild the reverse-lookup index after adding entries:

```
python3 skill/fase10/build_index.py
```

To audit cross-references between typology entries:

```
python3 skill/fase10/check_xrefs.py
```

## Source-text attribution

The Hebrew, Aramaic and Greek source texts in `Kennis/puur/` and `Kennis/strong/` are derived from open-source biblical text projects. See `ATTRIBUTION.md` for full credits and licensing of the underlying text data.

## License

This project is released under the MIT License. See `LICENSE`.

## Contributing

Contributions follow the sola-scriptura discipline that defines the project. New typology entries must follow the V2 template under `Kennis/typologie/_entry-sjabloon.md` and pass the seven-step verification protocol in `Kennis/protocollen/typologie-detectie.md`. See `CONTRIBUTING.md`.
