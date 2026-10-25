# ScoutRound35Defects — D-ledger report

Seat: scout, mado round 36 wave 1. Lane tip read: `dbf8b57` (freeze). No tool installs;
write scope: this report plus `scratch/ScoutRound35Defects/ledger.md`.

## Deliverable

The D-ledger is at `LANE/.ufo/waves/round-36/scratch/ScoutRound35Defects/ledger.md`
(copy of record). It maps every routed defect D1–D10 to round-36's disposition and the
artifact that shows it:

| Defect | Disposition | Artifact |
|---|---|---|
| D1 report-lands-last/tip citation | erratum naming `7a068cb…` in round-36 report (facts: `ScoutD1Facts`; draft `ScribeReportErrata`) | C2 subject (`registration.md:94`); round-36 report (pending) |
| D2 uncommitted closure work | resolved: ten inherited paths reverted — `git status --porcelain -- <10 paths>` empty; LOG disposition pending | C2 `inherited_dirty`; `before-pointers.txt` (`inherited_dirty=10`); `ScoutInheritedTen` |
| D3 C1 shape-scored | repaired `c1-idle-lock.py`: `and digest == receipt["sha256"]` (line ~194) + registry-section clause | C1; manifest rejects `c1-shape-only`/`c1-fabricated-payload`; criterion 57 draft (pending) |
| D4 C2 fail-open | repaired `c2-ledger.py`: frozen live-clause set, receipts must record `observed=TARGET_MISSED` and name clause, tip computed by one git rule | C1; ledger edit `RevFrozenBlobs-r36.md`; criterion 58 draft (pending) |
| D5 dangling LOG pointers | `old -> new` correction pairs in round-36 LOG entry (`SUPERSEDED_POINTERS`) | C2 `dangling_r35_closed`; before: `dangling_r35=2 closed=0` |
| D6 "four"→three rows | erratum with `git diff --numstat` `3 3` over S203–S205 | C2 subject; `ScoutD6Rows` (three rows confirmed); `ScribeReportErrata` (pending) |
| D7 stale count "38" | erratum naming per-revision counts 37/37/40 | C2 subject; `ScoutD7Counts` (D7 upheld); `ScribeReportErrata` (pending) |
| D8 cleanup claim vs 124 paths | `tracked paths=N` disposition sentence in round-36 lesson | C2 `scratch_disposition_ok`; `ScoutDisposition124` |
| D9 provenance trio | investigated only: append-only `## Provenance (normalized)` trailer policy proposed; boundary tested; **no gate observable, no owner for the edit, record edit pending** | `ScoutD9Provenance.md`, `CritD9Boundary.md` |
| D10 tip-revision axis transcript | committed `quality/receipts/axis-<40hex>.txt` with `mismatched=0 rev=<40hex>` | C2 `tip_axis_transcript`; `RevAxisTranscriptAsk`; before: `tip_axis_transcript=0` |

## Key evidence

- D2 resolution (this session): `git status --porcelain -- <the ten paths from
  `check-evidence-pointers.py:54-65`>`; no output, exit 0 (the before receipt records
  `inherited_dirty=10`; the round-36 gate requires 0).
- D3 repair bytes: `quality/counters/c1-idle-lock.py:193-194` — `and receipt["sha256"] in cs[5]`
  is now followed by `and digest == receipt["sha256"]`; header line 7-8 documents the bind.
- D4 repair bytes: `quality/counters/c2-ledger.py` — predicate (`:32`): live id set equals frozen
  expected set exactly; `receipt_observable` (`:94-95`) requires `clause=<id>` and
  `observed=TARGET_MISSED`; `compute_tip` (`:49`) derives the tip from `git log` by the frozen rule.
- Before receipts: `receipts/before-discrimination.txt` (`14/25` frozen) and
  `receipts/before-pointers.txt` (`verdict=TARGET_MISSED`, `dangling_r35=2`, `dangling_r35_closed=0`,
  `inherited_dirty=10` at first run, `scratch_disposition_ok=0`, `tip_axis_transcript=0`).

## Honest gaps

- Wave-1 build is in flight: all record edits (LOG correction pairs, scratch-disposition
  sentence, axis receipt, report errata) exist only as seat drafts; the C2 gate prints
  `TARGET_MISSED` until they land. Recorded as pending, not claimed done.
- D9 is the weakest-covered defect: it is in C2's subject list but no gate observable
  scores the corpus form and no seat owns the normalization application — an L1/round-end
  decision is owed (the scout's proposed trailer policy is ready).
