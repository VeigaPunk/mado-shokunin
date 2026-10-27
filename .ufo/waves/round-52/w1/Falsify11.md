# Falsify11 — C1 no-work control validity

Status: complete. Attacked the frozen round-52 C1 control (`controls/c1-do-nothing.md`) and the
demonstration clause that depends on it. All measurements run locally on source bytes at the
frozen base `85d57a818c3707397e21c840b6498b105ba798aa`, in scratch clones only. No claim,
predicate, control or tracked lane file was edited.

## Attacked clause

Three frozen sentences, quoted with their lines:

1. `registration.md:7` — "It must pass on the existing production ledger at the base revision
   and fail on `controls/c1-do-nothing.md` **specifically for self-pointer/context defects**."
2. `registration.md:15` — "C1 do-nothing control `controls/c1-do-nothing.md` **is the committed
   ledger shape** with only repeated generic self-pointers."
3. `claims-frozen.md:7` — the counter "distinguishes the production ledger from a no-work
   control of repeated generic self-pointers using unique population, non-self resolvable
   evidence targets, and instrument-specific context checks."

Attack surface: the control artifact's bytes and the base gate's own parse/evaluate path. This
is structural, not semantic entailment, and stays inside the claim's stated bound ("bounded
accountability checks, not prose entailment").

## Reproducible setup and command

Driver: `.ufo/waves/round-52/w1/Falsify11/repro.sh` (scratch clone, toplevel asserted before
every commit; every write stays under `/fast/scratch/hyaku/mado-r52/Falsify11/repro/`).

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify11
./repro.sh
```

It clones the lane at base, commits the frozen control verbatim as `quality/tool-ledger.md` in
the clone, then commits three derived fixtures (schema-repaired control, deduped control,
population-shaped no-work ledger) and runs two instruments on each revision:

- `quality/check-tool-ledger.py` — the pre-existing committed gate at base (predicate
  `PRED-C1-r51`), unmodified.
- `Falsify11/min-counter.py` — a seat-local counter implementing **only** population
  completeness plus row uniqueness; it deliberately contains no non-self-pointer clause and no
  description/context clause.

Control pin: `.ufo/waves/round-52/controls/c1-do-nothing.md`, 337 bytes,
`sha256 ad72f72f64708d1b877d0f2233f32a065bd11689d644af669176d1844ba2eba6`.

Full transcript and exit statuses: `Falsify11/receipt-repro.txt`.

## Actual results

| Revision in the scratch clone | Instrument | Measured summary |
|---|---|---|
| base `85d57a8…` (production ledger) | `check-tool-ledger.py` | `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET` |
| control committed verbatim | `check-tool-ledger.py` | `population=82 ledger_rows=0 uncovered=82 dangling=2 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED` |
| control committed verbatim | `min-counter.py` | `population=82 ledger_rows=2 dup=0 uncovered=82 verdict=TARGET_MISSED` |
| schema-repaired control (3 cells, backticked self-pointer, both rows kept) | `check-tool-ledger.py` | `ledger_rows=2 uncovered=81 dangling=1 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED` |
| schema-repaired control, deduped to one row | `check-tool-ledger.py` | `ledger_rows=1 uncovered=81 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED` |
| population-shaped no-work ledger (82 unique rows, one repeated generic description, every pointer `` `quality/tool-ledger.md` ``) | `check-tool-ledger.py` | `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET` |
| same population-shaped no-work ledger | `min-counter.py` | `verdict=TARGET_MET` |

### F1 — the control is not the committed ledger shape (registration sentence 2 is false)

Bytes: header `| Tool | Reads | Writes | Owner and adjacent lanes |`, a 4-cell separator, and two
identical 4-cell rows. The committed ledger grammar (`quality/tool-ledger.md:11-20`) and the gate's
parser (`quality/check-tool-ledger.py:234-258`, "not exactly three cells" → malformed) require
exactly three cells. Measured: the control yields `ledger_rows=0, dangling=2
(row-malformed-cells-4-line-3, line-4), uncovered=82`. It is a different artifact schema, not the
committed ledger shape, and it carries rows for 1 of 82 population instruments.

### F2 — the pre-existing base gate already produces the required red/green demonstration

The unchanged counter that existed before round 52 returns `TARGET_MET` on the production ledger
and `TARGET_MISSED` on the control (rows 1 and 2 of the table). So the claim's required
demonstration — production pass, control fail — is already satisfied by an instrument that
implements **neither** distinguishing clause (non-self pointer, instrument-specific context).
"Fails on the control" therefore carries no information about the two clauses the round is
buying. In the same run, a counter with completeness+uniqueness only reproduces the identical
verdict pair.

Why: `bad_pointer=0` and `empty_desc=0` on the control. The control's two intended defects are
never evaluated — the rows fail parsing before pointer or description scoring, and the
completeness clause dominates. The failure is attributable to schema and population only.

### F3 — repairing the schema does not recover the intended defects

Rewriting the control's rows into the ledger's three-cell grammar, keeping both frozen defects
(self-pointer at `` `quality/tool-ledger.md` ``, generic repeated description), then deduping:
`uncovered=81, dangling=0, bad_pointer=0, empty_desc=0`. The existing predicate reports **zero**
self-pointer findings and **zero** description findings. The control's named defects are
invisible to the predicate at base; the only surviving signal is completeness, which the control
violates by 81 rows under any tree-derived population. The three frozen fixture defects
(non-grammar rows, duplicate rows, self-pointer, generic description, missing population) are
confounded and cannot be attributed clause-by-clause.

### F4 — the no-work class the claim names is accepted when it has the production shape

The class in `claims-frozen.md:7` is "a no-work control of repeated generic self-pointers". Built
at production shape (82 unique rows, one identical generic description repeated 82 times, every
pointer `` `quality/tool-ledger.md` ``, which names all 82 basenames), the existing gate returns
`TARGET_MET` — as does the minimal completeness-only counter. So the committed control does not
represent the bypass class it is named for; it is rejected for shape, while the shape-matched
version of the same no-work content passes. A public counter that adds a self-pointer clause will
reject the padded fixture, but nothing in the committed control demonstrates that it does.

### F5 — "instrument-specific context" has no measured operationalisation

Two cheap, non-semantic features separate the production ledger from the *committed* control:
description distinctness (production 82/82 distinct; the control's two rows share one 52-char
description) and a description-length floor above 52 chars (production minimum 92). Either alone
yields production pass / control fail with no notion of instrument-specific function. Against a
population-shaped no-work ledger, distinctness still separates (82/82 vs 1/82) while a 60-char
length floor does not (its rows are 91 chars) — so the required demonstration is satisfiable by a
one-line distinctness clause, and the control cannot indicate which feature fired. Separately, a
single non-self document already satisfies pointer accountability for most of the population:
`SCORECARD.md` names 60/82 basenames, `PROVINCE.md` 22/82, union 65/82 (census in
`receipt-repro.txt`). The frozen predicate gives no floor that would reject one shared document
as evidence for 60 instruments.

## Reproduced

Yes, deterministically: one end-to-end run of `repro.sh` plus repeated stepwise runs of the same
commands in the same scratch clone, all with identical summary lines (only fixture commit SHAs
vary with commit timestamps).

- Reproduced: control fails under the base gate **not** for self-pointer/context (0 pointer and
  0 description findings), but for malformed rows and uncovered population.
- Reproduced: the base gate — which implements neither new clause — already yields production
  `TARGET_MET` / control `TARGET_MISSED`.
- Reproduced: a partial counter with only completeness and uniqueness yields the same pair.
- Not reproduced: registration's claim that the control "is the committed ledger shape"
  (contradicted by its bytes and by `ledger_rows=0`).

## Evidence chain

- Control bytes and pin: `controls/c1-do-nothing.md` (337 B, sha256 `ad72f72f…4ba2eba6`),
  measured header and row cell counts.
- Frozen wording: `.ufo/waves/round-52/registration.md:7,15`;
  `.ufo/waves/round-52/claims-frozen.md:7`.
- Predicate at base: `quality/check-tool-ledger.py:163-171` (population from tree),
  `:214-231` (pointer tokens), `:234-258` (three-cell row grammar), `:268-330` (evaluate; a
  malformed row is counted as dangling and never scored for pointer or description).
- Production baseline: `receipts/c1-base.txt` (`population=82 ledger_rows=82 … TARGET_MET`),
  reproduced independently at the same revision.
- Measurements: `.ufo/waves/round-52/w1/Falsify11/receipt-repro.txt`.

Confidence: high for F1–F4 (structural, byte-level, reproduced). F5 is a bounded probe of
plausible lexical operationalisations, not a statement about any counter that does not yet exist.

## What a valid control set would have to look like (observation, not an amendment)

The committed control cannot test the clauses it is registered against. A population-shaped
pair is the minimum that isolates them: (a) 82 unique rows, generic repeated description, all
pointers at `quality/tool-ledger.md` (self-pointer only); (b) 82 unique rows, generic
descriptions, all pointers at one shared *non-self* document (context/evidence-specificity only).
Each defect must be single, so a failure can be attributed. I did not edit claims, predicates or
controls.

## Limits and non-claims

- I did not build the round-52 counter (not this seat's lane) and do not judge its design.
- F5 does not claim the eventual counter will use a distinctness feature; it shows the frozen
  text does not exclude one.
- No install, package query, host/config/service/compositor mutation, live read, input capture,
  screenshot or producer execution. Only `git` on a scratch clone and the lane's own committed
  checker were executed; the lane checkout was not written.
- Scratch `/fast/scratch/hyaku/mado-r52/Falsify11/` was removed after copying receipts.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify11.md`
- `.ufo/waves/round-52/w1/Falsify11/repro.sh`
- `.ufo/waves/round-52/w1/Falsify11/min-counter.py`
- `.ufo/waves/round-52/w1/Falsify11/build-fixture.py`
- `.ufo/waves/round-52/w1/Falsify11/receipt-repro.txt`

Report: .ufo/waves/round-52/w1/Falsify11.md
