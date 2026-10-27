# Falsify10 — C1 uniqueness/population falsification

## Deliverables
- `.ufo/waves/round-52/w1/Falsify10.md` — source-only attack finding and reproduction status.

## Finding
**Attacked item/predicate:** C1, specifically population-row uniqueness and whether the frozen no-work control actually exercises the population accounting predicate.

**Concrete control defect observed:** `controls/c1-do-nothing.md` has exactly two data rows, and both use the identical population key `tools/mado-verify.sh`; it does not enumerate the production population. This is a useful duplicate-row negative example, but it cannot independently establish that the new counter accounts for the complete requested-revision population or detects missing population entries. The control needs to be evaluated as a deliberately partial/duplicate ledger, not treated as evidence for full-population coverage.

**Source basis:** frozen registration requires row uniqueness and identifies this control as repeated generic self-pointers (`.ufo/waves/round-52/registration.md`, “Frozen controls”); the actual two-row control is at `.ufo/waves/round-52/controls/c1-do-nothing.md`. The prior counter's population is selected from the pinned tree by `population(paths)` and deduplicated with `sorted(set(pop))`; rows are parsed separately by `parse_rows`; duplicate in-population rows are detected in `describe()` (`quality/counters/c1-r51-ledger.py`, lines 127–183, 214–239). This is source inspection, not a claim about the absent round-52 implementation.

**Reproduction setup/command:** read the two-line data table at `controls/c1-do-nothing.md` and count its first-cell key occurrences: `tools/mado-verify.sh` occurs twice, while the file contains no rows for the rest of the pinned population. No producer/counter was executed; round-52 `SKILL.md` explicitly forbids producer execution (lines 39–44).

**Actual result:** the named control visibly violates uniqueness (one key appears twice) and is incomplete relative to the production population, so it is suitable as a negative duplicate/self-pointer sample, not as a population-completeness positive or comprehensive population control. **Reproduced: no** — static inspection only; runtime execution was prohibited. I did not assess a new round-52 counter because no such implementation is in the frozen base evidence available to this seat.

## Limitations
- No claim that the planned new counter passes or fails: only the frozen control and prior counter source were inspected.
- No package queries, live reads, producer execution, host mutation, or tool installation.
- No scratch fixture was necessary for this source-only control finding.

## Report
`.ufo/waves/round-52/w1/Falsify10.md` (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`)
