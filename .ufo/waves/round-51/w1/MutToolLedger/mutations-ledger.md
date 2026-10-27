# Tool-ledger row grammar mutation probe

## Basis and boundary

No draft was present in `.ufo/waves/round-51/w1/ExecLedgerPopulation/`; grammar below is derived from frozen C1. C1 requires one row per tracked instrument (`tools/`, `quality/*.py`, `quality/counters/*.py`), a file, one-line non-empty description, and an accountability pointer naming an existing repo file that contains the instrument basename. The frozen checker/counter were not available as draft artifacts at probe time, so expected checker outcomes below are contract-derived expectations, not executed detector results. Verdict for every mutation is therefore **inconclusive** pending the actual checker and its bounded detector.

## Proposed row grammar

A Markdown table has exactly three semantic columns: `file | description | accountability pointer`. Each data row has exactly three fields; file and pointer are repo-relative file paths; description contains at least one non-whitespace character on one line. Each population file occurs exactly once; rows should be in deterministic lexicographic file-path order. Table-cell escaping for literal `|` is not specified by C1; this probe treats a literal pipe in a description as a field delimiter and rejects it (do not accept `\\|` absent an explicit escape rule). Basename need not be ASCII: Unicode filenames are valid if they belong to the population and the pointer file contains the exact basename.

## Mutations

| # | Mutation | Expected checker verdict | Rationale |
|---|---|---|---|
| 1 | Add a fourth column/cell to a data row | Reject | Violates three-field row grammar; avoids silently misreading the pointer. |
| 2 | Put an unescaped `|` in the description | Reject | In a Markdown table it creates an extra cell under this grammar. The C1 ledger is a census table, not a source-evidence table, but field delimiters still must be unambiguous; this is not a SOURCES-house ban imported on style grounds. |
| 3 | Description consists only of spaces/tabs | Reject | Frozen predicate demands non-empty description; whitespace-only has no content. |
| 4 | Pointer names an existing directory containing the basename in its path/name | Reject | C1 explicitly requires an existing repo *file* containing basename, not a directory. |
| 5 | Duplicate one population row | Reject | Exactly once is explicit in C1; duplicate should surface as duplicate/uncovered accounting. |
| 6 | Swap two rows so file paths are out of lexicographic order | Reject under proposed grammar; contract-derived, not frozen | Deterministic order aids review but C1 does not state ordering. This is a proposed checker constraint, not a claim frozen by predicate; unless checker specification adopts it, detector should accept this mutation. |
| 7 | Remove description field / leave it empty | Reject | Frozen predicate requires non-empty description (`empty_desc=0`). |
| 8 | Replace a population basename with a valid Unicode basename (and corresponding pointer contains it) | Accept | Unicode itself is not forbidden; exact path/basename membership and pointer containment determine validity. A non-population Unicode path should reject as dangling. |

## Execution status

No pristine/mutated/restored detector run was possible: the population seat directory was empty, and no checker/counter draft was supplied in scope. No bytes were mutated. This is a coverage finding, not evidence that a checker kills or survives any mutant. The observable detector outcomes and hashes remain unavailable; do not treat the expectations as measured outputs.
