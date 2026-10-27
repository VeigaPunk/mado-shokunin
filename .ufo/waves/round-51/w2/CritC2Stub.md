# CritC2Stub — C2 semantic-stub falsification

## Frozen finding

**C2 predicate verdict: MISS for semantic sufficiency; literal counter verdict: not run for the constructed fixture.** The frozen predicate is structural/lexical: indexing, at least two row-to-pin quoted-line correspondences, a per-file 8-gram overlap cap, and held key-token presence. None entails that the entry's prose truthfully explains dispatcher dispatch or provides useful domain coverage. A `TARGET_MET` proves the enumerated conditions only, not semantic entailment.

Do not treat this as an observed counter false-green: no successful run of the constructed fixture was obtained. The fixture sketch is not yet executable because its source refs/quotes and pin manifest must be validated against the authoritative data. The W1 draft is documented as `clauses_met=4/TARGET_MET` in `registration.md:17`, but that is the substantive entry, not this stub.

## Evidence and pointers

- Exact frozen sentence and clauses: `claims.md:53-63`; C2 kill controls: `claims.md:65-69`.
- Registration's declared residuals include generic held token `[the]`, candidate-bearing-report omissions, and that a low-overlap generic stub does not establish coverage: `registration.md:19`.
- W1 draft illustrating the broad mechanistic claims and its source/pin/held structure: `w1/ScrDispatchEntry/hyprland-dispatcher-dispatch-r51.md:1-24,26-68`.
- Adversarial, different-surface schematic with two required new source-row slots and three held references: `w2/CritC2Stub/semantic-stub.md`.

No command was run for the fixture. A future executable attack should copy valid row/quote/pin data from the frozen S364–S379 rows and fetch pins, preserve exact C2 predicate, then run `TMPDIR=<private-scratch> python3 -I quality/counters/c2-r51-dispatch-entry.py --repo <fixture-lane> --rev <fixture-rev>`. Do not report a pass unless that exact run emits the frozen final line.

## Axes and smallest safe correction

- **Coverage:** lexical novelty and citation presence are not domain coverage.
- **Operability:** counter can prove only its formal clauses; no domain-truth test is present.
- **Smallest safe correction:** future amendment should either scope the claim explicitly to structural/lexical admission or add an independent, auditable semantic review criterion. This is advisory only; frozen claim and lane files remain unchanged.

## Deliverables
- `w2/CritC2Stub/semantic-stub.md` — adversarial semantic-stub sketch and clause analysis.

Report: `.ufo/waves/round-51/w2/CritC2Stub.md`
