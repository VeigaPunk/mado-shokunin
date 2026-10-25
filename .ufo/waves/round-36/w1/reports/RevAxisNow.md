# RevAxisNow — axis-table gate at master, read-only

Seat: `L1Mado36.RevAxisNow` (reviewer). Round 36, wave 1.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Assignment: run `python3 -I quality/check-axis-scores.py --repo . --rev master`,
record full output and exit code, state which of the three published axis
fractions it checks, and whether the round-35 publication (`navigation 50/50`,
`calibration resolved-active 43/43`, `operability selftest 12/12`) still
re-derives at `master`.

## Items and verdicts

| # | Item | Verdict |
|---|------|---------|
| 1 | Gate runs at `--rev master`, records full output + exit code | PASS — exit `0`, `checked=3 mismatched=0` |
| 2 | Which published fractions are checked | All three: navigation, calibration, operability |
| 3 | Round-35 publication still re-derives at `master` | PASS — all three rows `MATCH` at `dbf8b579` (= the round-36 freeze commit) |
| 4 | Gate is discriminating, not a tautology | PASS — `STALE` and `NOT-PUBLISHED` rows + exit 1 observed at older revs |

## Command run and full output

From `/home/vgpnk/Projects/shokunin/mado-shokunin`:

    python3 -I quality/check-axis-scores.py --repo . --rev master; echo "EXIT=$?"

stdout (verbatim, complete):

    MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
    MADO_AXIS_ROW: axis=calibration published=43/43 derived=43/43 verdict=MATCH
    MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
    MADO_AXIS: checked=3 mismatched=0 rev=dbf8b579aeac0f023aaf595770f1cb0049e4baa2
    EXIT=0

## Which of the three published fractions it checks

All three. `quality/check-axis-scores.py` takes the **last unquoted**
`"Axis table re-derived at"` marker in `SCORECARD.md` at the revision under test
(`published_fractions`, quality/check-axis-scores.py:36-69; quote/backtick-prefixed
markers are skipped so errata quotations cannot shadow the live publication) and
re-derives each axis by running the **committed bytes at `<rev>`** of that axis's
own instrument (`derive`, :125-159):

- `navigation` — `quality/check-index.py --rev <rev> --repo .` → `indexed=A/B`
- `calibration` — `.ufo/waves/round-31/c2/count.py <rev>` → `resolved_active=A active=B`
- `operability` — `quality/check-index.py --selftest` → `A/B assertions passed`

Comparison is exact string equality on the `A/B` fraction (`compare`, :72-94);
a missing publication, missing instrument, or unparsable cell counts as a
mismatch, not a pass. `checked=3` confirms none of the three was skipped.

Which marker it parsed at `master`: `git show master:SCORECARD.md` has three
`Axis table re-derived at` markers — lines 2110 (`navigation 47/47`), 2179
(`navigation 50/50; calibration 43/43; operability 12/12`), and 2230 (`navigation
50/50; calibration resolved-active 43/43; operability selftest 12/12`). The gate
selected the last one (line 2230): its calibration row only parses via the
`"calibration resolved-active N/N"` regex (:63), and the run printed
`published=43/43` — impossible from line 2179's `"calibration 43/43"` phrasing.

## Does the round-35 publication still re-derive at master?

**Yes.** `master` resolves to `dbf8b579aeac0f023aaf595770f1cb0049e4baa2`
("round-36: freeze both predicates, the control manifest, the cribs and the
before receipts") — exactly the round-36 freeze commit, one commit after
round-35 close. All three published fractions re-derive identical there.

Independent re-derivations (worktree copies; `git status --porcelain` on
`quality/check-axis-scores.py`, `quality/check-index.py`, `count.py`,
`SCORECARD.md` is empty and `git diff master --` on both instruments is 0 lines,
so worktree == committed bytes):

    python3 -I quality/check-index.py --rev master --repo .
    # MADO_INDEX: rev=master indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10   (exit 0)

    python3 -I .ufo/waves/round-31/c2/count.py master
    # METRIC active=43 resolved_active=43 fraction=1.0000
    # PRED-C2-r31-v2 verdict=TARGET_MET            (exit 0)

    python3 -I quality/check-index.py --selftest
    # MADO_INDEX_SELFTEST: 12/12 assertions passed (exit 0)

## Discrimination evidence (the MATCH is earned, not hardcoded)

- Gate selftest: `python3 -I quality/check-axis-scores.py --selftest` →
  `MADO_AXIS_SELFTEST: 18/18 assertions passed`, exit 0.
- Negative control at `4f35c80` (a commit SCORECARD:2230 itself records as
  reading `mismatched=2`):

      MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
      MADO_AXIS_ROW: axis=calibration published=- derived=43/43 verdict=NOT-PUBLISHED
      MADO_AXIS_ROW: axis=operability published=- derived=12/12 verdict=NOT-PUBLISHED
      MADO_AXIS: checked=3 mismatched=2 rev=4f35c80ed31b4745a462c0216187583528393620
      EXIT=1

  Reproduces the recorded `mismatched=2` exactly, including the oddity that
  navigation "published" 50/50 there (an earlier marker already carried the
  newer navigation number while calibration/operability phrasing was still
  unparsable).
- STALE path live at `02088b4dff0da153df30ff174611d1257c92d0cd` (the commit the
  round-35 errata names as its base, where the index had already grown but the
  publication still said 47/47):

      MADO_AXIS_ROW: axis=navigation published=47/47 derived=50/50 verdict=STALE
      MADO_AXIS_ROW: axis=calibration published=41/41 derived=41/43 verdict=STALE
      MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
      MADO_AXIS: checked=3 mismatched=2 rev=02088b4dff0da153df30ff174611d1257c92d0cd
      EXIT=1

- Forward control at `7b745a1d943e5db5e8b9f8a7f4bee7af65b13990` (the commit the
  live publication cites as its derivation point): all three MATCH, exit 0 —
  consistent with SCORECARD:2230's claim that this is "the first commit whose
  publication the gate parses" cleanly.

## Findings

None blocking. One observation: the publication line at SCORECARD:2230 says the
table was "re-derived at `7b745a1d…`" while the gate's verdict at `master` is
"not stale" — the gate checks that published *numbers* still match derived
numbers, not that the derivation-point commit named in the prose equals the rev
under test. That is the documented contract ("must equal the re-derived
fraction", :16) and held; but a publication could cite an older derivation commit
and stay green indefinitely as long as the underlying counts don't move — the
named commit in the prose is informational only.

## Scope compliance

- Read-only on every production file; the only write is this report. No scratch
  files were needed (all evidence is inline above).
- No installs or tool updates needed or performed (stock `python3`, `git`).
- No `model` parameter; no compositor/config/service mutation; no sibling-lane,
  fleet-root, or freeze-path writes.

## Verification gaps / residual risk

- The gate re-derives only the three frozen axes; it does not check other
  numbers that appear in SCORECARD prose.
- Fraction comparison is string equality — format drift (e.g. `50/50` vs
  `050/50`) would read as STALE, which fails closed.
- `--rev` accepts any revision; a caller could pass a rev whose SCORECARD
  publication and instruments are self-consistent but not HEAD. That is the
  documented interface, not a defect.
