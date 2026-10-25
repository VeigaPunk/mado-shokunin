# ScribeScorecard — round-34 SCORECARD rows (draft)

Scope: draft the round-34 `SCORECARD.md` claim rows in the round-33 style
(`| Claim / axis | Before → after | Counting command | Author verdict |`),
one row per claim: C1 coverage `PRED-C1-r34-v1`, C2 calibration
`PRED-C2-r34-v1`. Before = pre-data control; after = lane-tree run. Axis named
by the surface moved, not the number.

**Deliverable: `.ufo/waves/round-34/scratch/ScribeScorecard/rows.md`** — the
4-column table plus a provenance preamble. Not applied to `SCORECARD.md`;
application is the integrator's (lane leaf seats do not mutate the card).

## Facts the rows carry (all re-run or re-read at write time)

- Freeze commit `3420e827bd7b21b1374b23245526554ffd20d096`; data commit
  `fa7ba11346116672352b5d41494141c5c4d738d0` (`fa7ba11`, also added the
  `r34-s189-line` publication line at `SCORECARD.md:2108` — `git show
  fa7ba11 -- SCORECARD.md`).
- C1 before: `controls/c1-donothing.txt` — `closed_entries=0 closed_rows=0
  open_cites=2 verdict=TARGET_MISSED`, exit 1 (frozen counter run on the lane
  tree before data; builder `build-controls.py:93`).
- C1 after, this seat's run 2026-10-24 at HEAD `fa7ba11`:
  `PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0
  verdict=TARGET_MET`, exit 0 — identical to `ExecC1Matrix`/`RevC1Matrix` row
  `lane`; every committed non-golden control misses identically `0/0/2`.
- C2 before: `controls/c2-donothing.txt` — `published=absent measured=169
  mismatch=1 verdict=TARGET_MISSED`, exit 1.
- C2 after, this seat's run: `PRED-C2-r34-v1 published=169 measured=169
  mismatch=0 verdict=TARGET_MET`, exit 0 — identical to `ExecC2Matrix` row 1
  and `RevC2Matrix` row 1. `RevC2Truth.md` confirms the ground truth
  (sha `eea605df…9540d`, line 169 strip-equals the literal, 128 does not) and
  names the limit: the marker is lane-local only.
- Axis naming: `registration.md:8-9` — "C1 on coverage, the axis round 33
  missed… C2 is calibration." Rows name the surface (event-socket client;
  SCORECARD publication vs pinned fetch), not `closed_rows=2` or `mismatch=0`.
- Predicate parity: `RevPredicateText.md` — both predicates byte-identical
  across `count.py` PREDICATE + docstring, `frozen.json`, `registration.md`.

## Embed hazard, checked

The C2 counter scores the LAST `SCORECARD.md` line containing
`r34-s189-line:` (`count.py:31,77-89`); a drafted row publishing a wrong tail
would flip the verdict on append. Checked:

- `grep -c 'r34-s189-line:' rows.md` → **0** — no drafted line carries the
  token sequence.
- Simulation: `SCORECARD.md` + the drafted rows appended to a scratch copy →
  `published=169 measured=169 mismatch=0 verdict=TARGET_MET`, exit 0.

## Row verdicts drafted

- C1: "target met on the lane tree" + limits (counts cites not content;
  missing root indistinguishable from broken tree; `TARGET_MET` is not a
  certification — round-33 lesson; predicate not rewritten after seats).
- C2: "target met" + kill controls and limits (last-marker-wins; lane-local
  publication; `measured` leg invariant).

Self-verdicts only; integrator's non-author verification pending.

Tools: none installed; system `python3`, `git`, `grep`, `sed`, `cp`.
