# ExecK2Receipts — round-32 C2 do-nothing controls, reproduced (round-33)

Date: 2026-10-24. Scope: reproduce the K2 control receipts that
`.ufo/waves/round-32/registration.md` §C2 (lines 132–138) promised under
`.ufo/waves/round-32/c2/controls/`. **The directory exists but holds no C2 receipts** —
only `c1-predicate-attack/` fixture trees (C1 controls, mis-nested). This report re-runs
the three controls on scratch clones under
`.ufo/waves/round-33/scratch/ExecK2Receipts/` and pastes the outputs verbatim.

Gate under test: `python3 -I quality/check-axis-scores.py` (frozen counter from the
round-32 registration §C2). No edits to the gate or to the lane `SCORECARD.md`
(`git status --porcelain SCORECARD.md quality/check-axis-scores.py` → clean).

## Method

Each control is an independent `git clone` of the lane at HEAD
(`9a46ccf3282117f960b8d53cd71599a91f388ee3`), so derived values at every tested rev are
the tip's: navigation 46/46, calibration resolved_active/active 41/41, operability
selftest 12/12. Only the SCORECARD publication text varies. Clones:

- `a-stale/` — last `Axis table re-derived` sentence rewritten to the round-31 text
  verbatim ("navigation 43/43 …; calibration resolved-active 39/40 = 0.9750 (lowest —
  criterion 35's mis-scoped M23-7); sourced-art 1.0; operability selftest 9/9 = 1.0."),
  committed `4590b9803cbbb276f942054d2120d54c4851c757` (lane identity).
- `b-rederived/` — untouched clone; run at `9a46ccf` (the clone tip already publishes
  the re-derived values — the (b) substitution is a no-op at this tip).
- `c-perturb/` — `resolved-active 41/41` → `40/41`, no other change, committed
  `a3a79cee6a48e9a7294edce538ee410a12f5d402` (lane identity).

All runs from the clone root (`--repo .` default), rev = clone HEAD.

## (a) Stale publication — required `mismatched>=1`

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-axis-scores.py
MADO_AXIS_ROW: axis=navigation published=43/43 derived=46/46 verdict=STALE
MADO_AXIS_ROW: axis=calibration published=39/40 derived=41/41 verdict=STALE
MADO_AXIS_ROW: axis=operability published=9/9 derived=12/12 verdict=STALE
MADO_AXIS: checked=3 mismatched=3 rev=4590b9803cbbb276f942054d2120d54c4851c757
exit=1
```

## (b) Re-derived text — required `mismatched=0`

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-axis-scores.py
MADO_AXIS_ROW: axis=navigation published=46/46 derived=46/46 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=41/41 derived=41/41 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=9a46ccf3282117f960b8d53cd71599a91f388ee3
exit=0
```

## (c) Perturb calibration 41/41 → 40/41 — required `mismatched=1`

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-axis-scores.py
MADO_AXIS_ROW: axis=navigation published=46/46 derived=46/46 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=40/41 derived=41/41 verdict=STALE
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=1 rev=a3a79cee6a48e9a7294edce538ee410a12f5d402
exit=1
```

## Verdict

All three controls reproduce as specified: **(a) mismatched=3 ≥ 1**, **(b) mismatched=0**,
**(c) mismatched=1 exactly**. The gate is not vacuous — a single-fraction perturbation
is detected while the other two axes still match, and a publication left at the r31
text is flagged stale on all three checked axes.

Receipts live under `.ufo/waves/round-33/scratch/ExecK2Receipts/{a-stale,b-rederived,c-perturb}/`
(uncommitted scratch per lane hygiene). The promised-but-empty location
`.ufo/waves/round-32/c2/controls/` remains as found — named here as the missing-receipt
defect; backfilling a closed round's wave tree is an operator call.

Caveat noted at run time: `SCORECARD.md` cites r31 base as `25622288`, which does not
resolve as a git object at the current tip (`git rev-parse --verify 25622288^{commit}` →
"Needed a single revision") — a stale short-rev citation, not a gate failure.
