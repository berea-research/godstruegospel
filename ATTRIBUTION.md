# Attribution and upstream credits

This project bundles biblical source-text data derived from open-source upstream projects. We acknowledge the original sources below and retain all required licensing attribution for the underlying text data.

## License scope

This repository contains two distinct kinds of material with different licenses:

- **Code** (the Python skill scripts under `skill/`, the build tooling under `build-software/`, the documentation under `docs/`, and the test suite under `Testen/`) is licensed under the **MIT License**. See `LICENSE`.
- **Data** (the source-text JSONL files under `Kennis/puur/` and `Kennis/strong/`, the Strong-code reverse indexes under `Kennis/index/`, and the LXX co-occurrence mappings under `Kennis/lxx-mapping-*`) is derived from upstream projects and remains under their original licenses. See `LICENSE-DATA.md` for the data-specific license terms.

The MIT license (code) and the upstream Creative Commons licenses (data) are compatible: you may redistribute this project as a whole provided you preserve attribution for each upstream data source. Modifying the data files (re-deriving, reformatting, extending) is permitted by the upstream licenses; modifications must be documented as required by CC BY 4.0.

## Upstream source-text data

### scripture4all (Hebrew/Greek interlinear with transliteration)

Portions of the source-text data in `Kennis/puur/` were derived from publicly available interlinear data prepared by the scripture4all project (https://www.scripture4all.org/). The transliteration conventions in our `.jsonl` files reflect their published interlinear convention.

**Modifications made by this project:** the original scripture4all interlinear PDF/web data has been parsed, normalized to per-verse JSON-line format, and stored with explicit verse references and per-word transliteration. The original word identity and ordering are preserved.

### STEPBible-Data (Strong-code annotated text)

The Strong-code annotated source text in `Kennis/strong/` is derived from STEPBible-Data, an open-data project distributing tagged Hebrew and Greek texts under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**. STEPBible-Data is published by Tyndale House, Cambridge.

- Repository: https://github.com/STEPBible/STEPBible-Data
- License: https://creativecommons.org/licenses/by/4.0/
- Citation: "Tyndale House, Cambridge — STEPBible-Data, available at https://github.com/STEPBible/STEPBible-Data, licensed under CC BY 4.0."

**Modifications made by this project:** the original STEPBible-Data files (in their native tab-separated `TXTSouls`, `TFSouls` and similar formats) have been parsed and re-serialized as line-delimited JSON with one verse object per line. Per-word fields (Hebrew/Greek text, transliteration, Strong code, parsing tag) are preserved with their original semantics. No interpretive content was added or removed; the modification is purely a format conversion to facilitate programmatic search by the skill scripts. The verse-by-verse structure and the per-word Strong tagging remain identical to the upstream source.

### Septuaginta (LXX) lexical mapping

The Hebrew-to-Greek lexical mapping in `Kennis/lxx-mapping-grieks.json` and `Kennis/lxx-mapping-hebreeuws.json` was constructed by aggregating co-occurrence frequencies across openly available Septuagint editions of the Greek Old Testament. The mapping is purely statistical and is intended as a research aid for cross-language word-study, not as an authoritative translation tool.

**Modifications made by this project:** the LXX mapping is a derivative computational artifact, not a direct redistribution of any single Septuagint edition. It records statistical co-occurrence relationships only, not the source text itself. The aggregation methodology is documented in `build-software/build_lxx_mapping_grieks.py` and `build-software/build_lxx_mapping_hebreeuws.py` for reproducibility.

## Concordant translation masters (project-original work)

The concordant translation vocabulary masters in `Kennis/masters/` (Dutch, English, Spanish) were built by this project itself through systematic word-by-word translation review. Where a master entry refers to a known reference work (such as Strong's Hebrew and Greek Dictionaries), the reference is cited within the entry's rationale field. The masters themselves are released under the MIT license alongside the rest of the project's source code.

## Skill scripts and typology corpus (project-original work)

The Python skill scripts under `skill/` and the typology corpus under `Kennis/typologie/` are original work produced by this project, released under MIT (see `LICENSE`). The corpus does not redistribute any third-party copyrighted commentary; it contains only references to verses in the source text plus original analytical entries written by the project.

## License compliance for redistribution

If you redistribute this project (in whole or in part), you must:

1. Preserve this `ATTRIBUTION.md` file together with the data it describes.
2. For STEPBible-derived files in `Kennis/strong/`: preserve the CC BY 4.0 attribution and a link back to https://github.com/STEPBible/STEPBible-Data.
3. For scripture4all-derived files in `Kennis/puur/`: preserve attribution with a link back to https://www.scripture4all.org/.
4. For the LXX mapping: preserve attribution to the published Septuagint editions used in the aggregation; consult `build-software/` for the construction scripts and source manifest.
5. Document any further modifications you make to the data files (CC BY 4.0 requirement).
6. For the code under MIT: preserve the MIT license text from `LICENSE`.

## Reporting attribution issues

If you identify a missing or inaccurate credit, please open an issue on this repository's tracker. Attribution corrections are treated as priority bugs.
