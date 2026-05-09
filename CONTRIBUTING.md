# Contributing

Thank you for considering a contribution. This project follows a strict sola-scriptura discipline. Before contributing, please read the architectural principles in `docs/godstruegospel-documentation.pdf` so that your work aligns with the methodology.

## Discipline (non-negotiable)

1. Every claim, pattern, or assertion in code, documentation, or typology entries must trace to a verse in the Hebrew, Aramaic, or Greek source text bundled in `Kennis/puur/` and `Kennis/strong/`. No claim may rest on translation alone, on a doctrinal school, on a church father, or on training-data echoes.

2. New typology entries must follow the V2 template at `Kennis/typologie/_entry-sjabloon.md` and pass the seven-step verification protocol at `Kennis/protocollen/typologie-detectie.md`. The two-witness threshold is required: at least two independent passages must support the pattern.

3. Strong-codes are tools for reproducible search, not typological elements in themselves. They appear in the `zoekquery_gebruikt` section of an entry, not as evidence in their own right.

4. New concordant-translation entries must include a rationale that explains the chosen target word for each source word, including the trade-offs against major Bible translations (KJV, NBG-1951, Reina-Valera, etc.). The choice is concordant, not paraphrastic.

## Workflow for a new typology entry

1. Open an issue describing the pattern hypothesis in one sentence.

2. Run the source-text search:

   ```
   python3 skill/typologie_zoek.py --strong G____    # for a Strong-code search
   python3 skill/typologie_zoek.py --cijfer N        # for a number-pattern search
   ```

3. Document every occurrence with verse reference, source-text form (with transliteration), brief context, and an N-level (N1 = explicit, N2 = inferable, N3 = clue).

4. Apply the coherence test (two-witness threshold, genre spread, removal test, NT-OT linkage).

5. Write the entry following the template, place it in the correct submap (`A_entiteit/`, `B_cijfer/`, etc.), and update `Kennis/typologie/README.md` status table.

6. Run the index rebuild and cross-reference check:

   ```
   python3 skill/fase10/build_index.py
   python3 skill/fase10/check_xrefs.py
   ```

7. Open a pull request that includes the new entry, updated status table, and updated index outputs.

## Workflow for a new concordant-translation language

See `docs/talen-uitbreiding-prompt.md` for the language-extension protocol. A new language goes through a TODO → IN-PROGRESS → COMPLETE pipeline with a pairwise-test pass requirement before merging.

## Code style

Python: PEP 8, type hints where useful, no external dependencies beyond the standard library for the skill scripts. The `build-software/` scripts may use additional libraries; declare them at the top of the script.

Markdown: short paragraphs, citable. Code blocks for shell commands. No unbroken paragraphs longer than ten lines.

JSON: indent with two spaces, keys sorted, UTF-8.

## Discipline checks before submitting

Run the verification scan before opening a PR:

```
grep -r "<your-name>" .          # confirm no personal names introduced
grep -r "AP/" .                  # confirm no path-prefix regression
```

Patches that introduce names of authors, churches, doctrinal schools, or modern typologists into the public artifacts will be rejected. The project's neutrality is part of its sola-scriptura position.

## Issues and discussion

Issues should reference verses directly. Avoid framing issues as "should we adopt teaching X"; instead frame them as "the source text at passage Y exhibits pattern Z, here is the evidence". The issue tracker is a research log, not a doctrinal forum.
