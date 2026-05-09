# Data License — biblical source-text and derived data files

This file documents the license that applies to the **data files** in this repository. The code in this repository (Python scripts, build tooling, documentation, tests) is licensed separately under the MIT License — see `LICENSE` in the repository root.

The MIT License does **not** apply to the data files described below. Those files retain the licenses of their upstream sources, which are compatible with the MIT License of the code (both are permissive open-source licenses) but have their own attribution and modification-disclosure requirements.

## What counts as "data" in this repository

The following directories and files contain data derived from upstream open-source projects and are subject to the licenses below:

```
Kennis/puur/                  Source text per Bible book (JSONL)
Kennis/strong/                Source text + Strong-code annotation (JSONL)
Kennis/index/                 Reverse Strong-to-verse indexes (JSON)
Kennis/lxx-mapping-grieks.json
Kennis/lxx-mapping-hebreeuws.json
```

The following directories contain **project-original work** licensed under MIT (the same license as the code):

```
Kennis/diepte/                Word studies authored by this project
Kennis/masters/               Concordant translation masters authored by this project
Kennis/protocollen/           Methodological protocols authored by this project
Kennis/typologie/             Typology corpus authored by this project
```

## License terms per upstream source

### STEPBible-Data (Kennis/strong/)

The Strong-code annotated source text under `Kennis/strong/` is derived from **STEPBible-Data**, published by **Tyndale House, Cambridge**.

- Source: https://github.com/STEPBible/STEPBible-Data
- License: **Creative Commons Attribution 4.0 International (CC BY 4.0)**
- License text: https://creativecommons.org/licenses/by/4.0/legalcode

Under CC BY 4.0 you are free to:

- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

**Changes made by this project** to the upstream STEPBible-Data: the original tab-separated text format has been parsed and re-serialized as line-delimited JSON (`.jsonl`) with one verse object per line and per-word fields preserved. Verse identifiers, Hebrew/Greek/Aramaic text, transliterations, Strong codes and parsing tags carry the same semantics as the upstream source. No interpretive content was added or removed.

### scripture4all (Kennis/puur/)

The transliterated source text under `Kennis/puur/` is derived from publicly available interlinear data prepared by the **scripture4all project**.

- Source: https://www.scripture4all.org/
- License: free for non-commercial study and research use as published by the scripture4all project.

**Changes made by this project**: the scripture4all interlinear data has been extracted into a structured JSONL format. The transliteration convention published by scripture4all is preserved.

### Septuagint editions (Kennis/lxx-mapping-*)

The Hebrew-to-Greek lexical mapping under `Kennis/lxx-mapping-*` is a **derivative statistical artefact**, not a redistribution of any specific Septuagint edition. It records co-occurrence frequencies between Strong-coded Hebrew and Greek lexical items as observed in publicly available Septuagint editions.

The aggregation methodology and source manifest are documented in:

- `build-software/build_lxx_mapping_grieks.py`
- `build-software/build_lxx_mapping_hebreeuws.py`
- `build-software/aggregate_lxx_mapping_hebreeuws.py`

The output files contain only statistical relationships, not source-text content from any single edition.

## Compatibility statement

The MIT License (covering this project's code and project-original data) and the Creative Commons Attribution 4.0 International License (covering the STEPBible-derived data) are mutually compatible:

- Both are widely used permissive open-source licenses.
- Both permit commercial use.
- Both permit modification.
- Both permit redistribution.
- Both require attribution to the original authors.
- Neither imposes a copyleft obligation on derivative works.

A redistribution of this project as a whole is therefore permitted, provided the requirements of both licenses are observed: (1) preserve the MIT license notice for the code, (2) preserve the CC BY 4.0 attribution and modification disclosure for the STEPBible-derived data, (3) preserve the scripture4all attribution for the transliterated source text, and (4) preserve this `LICENSE-DATA.md` document together with `ATTRIBUTION.md` and `LICENSE`.

## Practical guidance for redistributors

If you fork, mirror, or rebundle this repository:

1. Keep `LICENSE`, `LICENSE-DATA.md`, and `ATTRIBUTION.md` together at the repository root.
2. If you modify any data file under `Kennis/puur/`, `Kennis/strong/`, `Kennis/index/`, or `Kennis/lxx-mapping-*`, document your change in a `MODIFICATIONS.md` note alongside the file or in your fork's release notes (CC BY 4.0 requires "indicate if changes were made").
3. If you ship the code only (without the data directories), you may license your distribution under MIT alone; the CC BY 4.0 obligations only apply when you redistribute the data.
4. If you ship the data only (e.g. as a separate dataset publication), preserve the CC BY 4.0 license and attribution; the MIT license does not apply to data-only distributions.

## Questions

If you have questions about the licensing scope of a specific file, open an issue on the repository's tracker. We will respond with a clarification or, where appropriate, update this document to remove ambiguity.
