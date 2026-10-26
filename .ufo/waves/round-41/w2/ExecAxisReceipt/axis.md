# ExecAxisReceipt — round-41 w2 seat report (axis calibration attack)

Target: **calibration** — the published axis table must match the observed repo state.
Reproduce what `quality/check-axis-scores.py` derives at the DATA commit
`07f2641696b5ac73de1404ea737a9f27e9819aa1`; give the L1 the exact SCORECARD.md sentence that
makes the gate print `checked=3 mismatched=0` at the FINAL TIP (new indexed entry already in the
data commit; QUALITY.md gains criteria 69–72), and a ready-to-commit receipt.

All commands below were run on the lane at `/home/vgpnk/Projects/shokunin/mado-shokunin`
(read-only git; no tracked file edited; no mutating git). The final-tip calibration was simulated in
a disposable git fixture (`mktemp -d`, `git init`, toplevel verified, env-explicit identity, commits
inside the fixture only).

---

## F1 — Derived fractions at the DATA commit 07f2641 (reproduction)

Instrument runs (each verbatim):

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ python3 -I quality/check-index.py --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1 --repo .
MADO_INDEX: rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 indexed=59/59 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0

$ python3 -I .ufo/waves/round-31/c2/count.py 07f2641696b5ac73de1404ea737a9f27e9819aa1
counter=c2-grounding-r31-v2 rev=07f2641696b5ac73de1404ea737a9f27e9819aa1
METRIC literal lines=56/68 fraction=0.8235
METRIC superseded=[1, 2, 3, 4, 5, 18, 19, 20, 32, 38, 39, 40, 48]
METRIC active=55 resolved_active=55 fraction=1.0000
PRED-C2-r31-v2 verdict=TARGET_MET
exit=0

$ python3 -I quality/check-index.py --selftest
MADO_INDEX_SELFTEST: 12/12 assertions passed
exit=0
```

Derived fractions at 07f2641: **navigation 59/59, calibration resolved-active 55/55, operability
selftest 12/12**.

## F2 — Gate reading at the DATA commit (what the gate prints there)

```
$ python3 -I quality/check-axis-scores.py --repo . --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1
MADO_AXIS_ROW: axis=navigation published=58/58 derived=59/59 verdict=STALE
MADO_AXIS_ROW: axis=calibration published=55/55 derived=55/55 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=1 rev=07f2641696b5ac73de1404ea737a9f27e9819aa1
exit=1
```

The last publication SCORECARD.md holds at 07f2641 is the round-40 axis line (SCORECARD.md:2493):
"Axis table re-derived at `3c80537a54b4fd3b534f5cc3496a4bdc37c11371` plus the round-40 axis-line
commit (two new indexed entries): navigation 58/58; calibration resolved-active 55/55; operability
selftest 12/12." The data commit added one indexed note
(`corpus/knowledge/hyprland-focus-grab-r41.md`, row in `corpus/README.md`), so navigation derives
59/59 vs published 58/58 → STALE. This is the expected data-stage "red half" (precedent:
`quality/receipts/red-axis-publication-stale-at-data-commit.txt` for round 36: the data commit is red
until the records commit lands the publication). No defect in the data or the predicate: the
publication is a records-commit artifact by design. Same reading (mismatched=1, navigation STALE) at
HEAD `9919e1694e6d9296d3052ddcaa2ae83bf3d535c4` (the w2-dispatch commit adds no corpus/QUALITY
change).

## F3 — Final-tip calibration count with criteria 69–72 appended (simulation)

Fixture: fresh `mktemp -d` git repo seeded with the lane's HEAD blobs (corpus/, SCORECARD.md,
quality/check-index.py, quality/check-axis-scores.py, .ufo/waves/round-31/c2/count.py); the four
drafted criterion paragraphs (single lines starting "69. ", "70. ", "71. ", "72. ") extracted
byte-exact from `.ufo/waves/round-41/w1/ScrQualityCriteria/criteria.md` appended to
`corpus/QUALITY.md` (file ends at criterion 68, no renumbering); committed; counter run at the
fixture tip:

```
$ python3 -I .ufo/waves/round-31/c2/count.py HEAD            # cwd = fixture
counter=c2-grounding-r31-v2 rev=HEAD
METRIC literal lines=60/72 fraction=0.8333
METRIC superseded=[1, 2, 3, 4, 5, 18, 19, 20, 32, 38, 39, 40, 48]
METRIC active=59 resolved_active=59 fraction=1.0000
PRED-C2-r31-v2 verdict=TARGET_MET
exit=0
```

So at the final tip the calibration counter reads **resolved-active 59/59**: active 59 = 68 − 13
superseded + 4 new; none of 69–72 supersedes, and all four resolve — 69/70 cite the bare non-empty
`lessons/round-40-verifier-spotcheck.md`; 71/72 cite `lessons/round-40.md#mistakes` with `M40-6` /
`M40-1` present inside the `## Mistakes` section (verified: section slug "mistakes"; each id appears
once in that section's scope). Index and selftest are unchanged by the append: indexed=59/59,
selftest 12/12.

**Integrator note (conditional):** the draft's own "Notes for the L1" suggests extending the lesson
parentheticals with `…; lessons/round-41.md#mistakes M41-n` if the round-41 lesson records `M41-n`.
The 59/59 reading is valid for the draft **as-is**. Each such extension must itself resolve at the tip
(round-41.md would need a #mistakes section carrying the cited ids), or the calibration count drops
below 59/59; re-derive before landing if any extension is added.

## F4 — The exact SCORECARD.md sentence that makes the gate green at the final tip

Append (as the last publication; the parser takes the last unquoted "Axis table re-derived at",
so it supersedes the round-40 line at SCORECARD.md:2493):

```
Axis table re-derived at `<TIP>` plus the round-41 records commit (one new indexed entry, criteria 69-72): navigation 59/59; calibration resolved-active 59/59; operability selftest 12/12.
```

`<TIP>` = the final records-commit hash (`git rev-parse HEAD` at commit time). This exact sentence
was appended to the fixture's SCORECARD.md and the gate rerun at the fixture tip — verified output:

```
MADO_AXIS_ROW: axis=navigation published=59/59 derived=59/59 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=59/59 derived=59/59 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=<fixture tip>
exit=0
```

## F5 — Ready-to-commit receipt `quality/receipts/axis-<tip>.txt`

Pattern mirrors `quality/receipts/axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt`. Body (the L1
reruns verbatim at the real tip and substitutes the printed rev; expected lines shown as validated by
the fixture run):

```
# axis + index + suite transcript at the round-41 records commit <TIP>
# produced 2026-10-25 by the lane's own instruments, read-only

$ python3 -I quality/check-axis-scores.py --repo . --rev <TIP>
MADO_AXIS_ROW: axis=navigation published=59/59 derived=59/59 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=59/59 derived=59/59 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=<TIP>
exit=0

$ python3 -I quality/check-index.py --rev <TIP> --repo .
MADO_INDEX: rev=<TIP> indexed=59/59 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0

$ python3 -I quality/check-index.py --selftest
MADO_INDEX_SELFTEST: 12/12 assertions passed
exit=0
```

(Optional companion transcript for the calibration leg, same style as the axis receipt's instrument
section:

```
$ python3 -I .ufo/waves/round-31/c2/count.py <TIP>
counter=c2-grounding-r31-v2 rev=<TIP>
METRIC literal lines=60/72 fraction=0.8333
METRIC superseded=[1, 2, 3, 4, 5, 18, 19, 20, 32, 38, 39, 40, 48]
METRIC active=59 resolved_active=59 fraction=1.0000
PRED-C2-r31-v2 verdict=TARGET_MET
exit=0
```

## Attacked items and verdicts (each: what + command + outcome)

1. Instrument self-consistency — `python3 -I quality/check-axis-scores.py --selftest` → 18/18
   assertions passed, exit 0 (parse rules for navigation/calibration/operability, quoted-marker
   shadow rule, long-publication window, stale detection). No defect.
2. Calibration predicate at DATA commit — `count.py 07f2641…` → 55/55, TARGET_MET, exit 0. No
   defect.
3. Calibration predicate at simulated final tip (criteria 69–72 appended) — fixture `count.py HEAD`
   → 59/59, TARGET_MET, exit 0. No defect (as drafted).
4. Navigation predicate at DATA and tip — `check-index.py --rev …` → 59/59 at both, missing=0,
   dangling=0, duplicates=0. No defect; the 58→59 step is exactly the new entry, already committed
   in the data tree.
5. Operability predicate at DATA and tip — `check-index.py --selftest` → 12/12. No defect.
6. Publication-vs-repo staleness at DATA commit (the attack axis) — gate at 07f2641 → mismatched=1
   (navigation STALE), expected red half (round-36 precedent), not a data/predicate defect; the L1's
   records commit carrying F4's sentence flips it to checked=3 mismatched=0 (proven end-to-end in the
   fixture).

## Tooling record

No tools installed or updated; no package transactions (pacman untouched). No host-service,
compositor, Wayland or input paths touched; no journal writes.

## Risks

- If the L1 appends criteria 69–72 with any edits beyond the draft's exact paragraphs (e.g. the M41-n
  lesson extensions), the calibration reading must be re-derived; the sentence numbers in F4 apply to
  the draft as-is.
- The receipt's rev tokens must be filled by the real run at the tip; the validated fixtures is
  byte-identical modulo the rev token (verified by the fixture run).
