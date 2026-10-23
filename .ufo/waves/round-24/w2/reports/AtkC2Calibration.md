# AtkC2Calibration — C2 after landing: status table vs observed repo state (round 24, wave 2)

Leaf critic. Attacked item: the landed SCORECARD table `### Capability status (round 24 re-demonstration)`
(SCORECARD.md:1566-1585, commit `81955bd5`, unchanged at tip `39c59630`) against AXES.md:15 calibration
("SHONEN.md/SCORECARD entries match observed repo state") and the prompt §6.9 rule that a calibration claim
counts mismatches between self-assessment and repo state. Question given: does the landed table make SCORECARD
match observed state, or did it only transcribe counter output — and would a closure call C2 calibration or
quality?

All commands were read-only. The C2 counter was run exactly once, at the landed tip, as allowed (900 s cap;
262 s wall). Scratch files live under `/fast/scratch/hyaku/mado-r24/w2/`. No lane file was edited except this
report; no lane/fleet git or jj write command was issued; no package, service, compositor or hyprctl operation
was performed; nothing was installed; every process I started has finished.

## A. The 12-row target at the actual landed tip — holds

```
$ timeout 900 python3 -I .ufo/waves/round-24/c2/count.py 39c596307333b8ca0a1e42b3f3b9a748bb8b208b
...
tripwire evidence marker	stated=fails	observed=fails	OK	exit=0
mismatches=0/12 revision=39c596307333b8ca0a1e42b3f3b9a748bb8b208b \
  manifest_sha256=e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02 \
  counter_sha256=a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8
exit=0
```

The after-receipt was taken at `81955bd5` (the commit that adds the table), not at the tip. My own run at
`39c59630` gives the same 0/12, so the target "mismatches=0 at the landed tip" is true, not only at the
receipt revision. The frozen manifest and counter hashes match the registration's `e02c76d1…` / `a2809501…`.
The per-row observed/exit values at the tip equal the base smoke's (`c2/smoke/base-8e5d9369.txt`): 11 `works`,
1 `fails` (`tripwire evidence marker`, exit 0), row 6 exit 1, row 7 exit 0.

## B. It is a transcription of the frozen observation — proven, 12/12

Mechanical comparison of the landed table's status column against the observed column of the pre-data base
smoke:

```
smoke rows 12 table rows 12
equal: True
diff: {}
```

Every status in the table is the observed value from the frozen do-nothing/base observation, including the
sole `fails`. The wave-1 draft that preceded it (`w1/reports/ScribeC2Evidence.md`) already listed
`status | observed=works|fails` for the same twelve rows. Nothing in the observed column changed from base to
tip; the only input that moved 1/12 → 0/12 is the `stated` column, i.e. the table itself. The after-value is
therefore guaranteed by construction. It is not evidence that the lane's self-assessment predicted reality;
the informative calibration evidence is the before value (`1/12`) and the honest, evidenced `fails` row. Note
also that at the landed tip the do-nothing condition now scores 0/12 (the table is the change), so the target's
after-value cannot distinguish a corrected scorecard from an artifact written from the answer.

## C. Does SCORECARD now match observed state? Only for the 12-row population

- The table's prose, "Each capability in the tables above was re-run with its frozen command", is false for
  three capability rows that are outside the counter's heading-restricted population (`^#{2,3} Capabilities`):
  `SCORECARD.md:437` source-fragment collision screen, `:438` digest-pinned frozen regression, `:782` finite
  declared-action classifier. Enumerating every SCORECARD table whose first header cell is `Capability` gives
  15 rows, not 12; the registration/manifest note "the 12 SCORECARD capability-table rows at base" is false
  under the frozen predicate's plain wording ("a capability named in a SCORECARD.md capability table").
- Two of the three match observation today, which I re-ran at the tip:
  - `python3 -I .ufo/waves/round-13/frozen/verify.py` → `MADO_FROZEN: MATCH`, exit 0.
  - `python3 -I tools/mado-action-plan.py --selftest` → `SELFTEST_SUMMARY: 52/52 passed`, exit 0.
- The third does not. `SCORECARD.md:437` asserts the screen's evidence as "current exits 0". Observed at the
  tip:

  ```
  $ python3 -I .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md
  MISTAKE_FIX: COLLISION S120 -> S121 :: same canonical URL among active rows; ...
  MISTAKE_FIX: FAIL registry=corpus/SOURCES.md rows=168 urls=140 no_url=21 collisions=4 \
    rejected_history=3 supersedes=7 errors=0
  exit=1
  ```

  The selftest still passes 25/25; only the registry evidence is stale. This is not a wave-1 regression: the
  same command on a scratch copy of `git show 8e5d9369:corpus/SOURCES.md` gives exit 1, `collisions=4`, and
  `git diff 8e5d9369 39c59630 -- corpus/SOURCES.md` contains no S120/S121/executionmodel change. It is a
  pre-existing SCORECARD-vs-repo disagreement that the C2 landing neither counts nor scopes.
- One further narrowness, disclosed in the cell but not encoded in the status: row 2 `verdict gate (live + file
  plane)` is `works` on `--no-live` only; the evidence cell itself says "live layer not exercised". The live
  half of the named capability was not re-demonstrated, so 0/12 cannot be read as "all twelve fully
  re-demonstrated".
- Row 6 `tripwire frozen replay (gate entry)` is correctly `works` at exit 1: the round-18 row's own contract is
  0 match / 1 mismatch / 2 tampered, and round 19 records the pin's expected mismatch. No finding there.
- No false-provenance finding in the table's evidence cells: the 1/12 before value and the two L cases are
  confirmed by `w1/reports/ScribeC2Evidence.md` (base 166/175, L 15/18; `28c6837` L 17/18).

## D. Calibration or quality?

The axis is **calibration**, but only as a state-accuracy/bookkeeping correction, and only for the 12 counted
rows. The declared observable (mismatch count between SCORECARD self-assessment and the frozen observation)
moved 1 → 0, and an overclaim was replaced by an explicit, evidenced `fails`. That is the AXES calibration
signal operating on the document. The fleet has an equivalent state-accuracy calibration precedent (kengaku
round-24 C2, `kengaku.md:226`, score held 8→8); admissibility of that species is itself an open fleet L0
question, so it is not settled for mado either.

It is **not a quality repair**, and must not be booked as one: the tripwire evidence marker still fails
(L 15/18, round-21 harm H2, the table says so itself), and the collision registry still exits 1 with four
collisions. Those are quality/corpus defects and belong on the repair route, not in the calibration column.

The statement a closure may make and survive re-reading: "C2: twelve-row population, 0/12 at tip
(`39c59630`); the scorecard now states the observed statuses instead of implying `works`, with the one failing
capability recorded and evidenced; the failure itself is unchanged and is a quality harm." The statement it may
not make is "SCORECARD now matches observed repo state": the table is a transcription of the frozen observed
column, its prose claims three capability rows were re-run when they were not, and one of those rows
(`SCORECARD.md:437`) still contradicts current observation.

## E. Impacted axes and smallest safe correction

- Impacted axes: calibration (primary, partial); quality/operability (the documented H2 failure remains);
  freshness (the stale collision-screen evidence at `SCORECARD.md:437`). No axis is harmed by the append
  itself, and the frozen counters/manifest and `tools/` bytes are untouched.
- Smallest safe correction (post-freeze disposition; no predicate, target or manifest change, no SCORECARD row
  deletion — append only):
  1. Append one scoping/correction line under the round-24 table: it covers the twelve rows under `Capabilities`
     headings counted by `c2/manifest.json`; the three other capability rows (`SCORECARD.md:437-438`, `:782`)
     are outside that population — frozen regression and action-plan pass at `39c59630`; the collision
     screen's "current exits 0" evidence is stale (current registry exits 1, `collisions=4`, S120→S121).
  2. Record in LOG/round report that C2 is state-accuracy calibration over the 12-row population, target met at
     tip, and route the collision-registry defect plus H2 to a later round's quality/coverage work.
  3. If a document-wide calibration claim is wanted, it needs an extended population and a fresh control wave
     in a later round; do not extend the frozen predicate now.

VERDICT: partial — the 12-row counter target holds at the landed tip (0/12, my own run), but the landing only
transcribes the frozen observed column (12/12 statuses equal the base smoke), its prose overstates coverage by
three capability rows, and one uncounted capability entry (`SCORECARD.md:437`, current registry exits 1 with
four collisions, S120→S121) still contradicts observed repo state at base and tip. A closure may call C2
calibration in the narrow state-accuracy sense; it may not call the scorecard matched, nor the failing
capability repaired.
