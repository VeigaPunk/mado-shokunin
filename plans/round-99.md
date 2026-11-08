# mado round 99 — plan and pre-file amendments

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, base
`2cbaa141f42df9dfeee4d207cae6558a4dd59863` (round-98 closure tip). L1 `MadoR99` (attempt 4; the
inherited attempt-2/3 tree is reused after re-verification — the wave, its evidence and the
receipts were read back this attempt). The round contract is
`.ufo/waves/round-99/claims-declaration-r99.md`; this file records the round plan and every
amendment made under the pre-file falsification rule (lane addendum §8 / Amendment 59) BEFORE the
report was filed. Nothing in the declaration above its `## Freeze block` was rewritten; the
amendments below narrow what the round files, and each names the wave artifact that forced it.

## Round plan (as executed)

Two claims, two distinct axes, causally separable; no exploratory claim; `Assimilation: none`.

- **C1 — coverage (capability, new surface): the launch spawn environment.** Land
  `tools/mado-launchenv.py` (read-only model of the load gate, `Terminal=true` terminal selection
  and prepend, `Path=` working directory, post-prepend `argv[0]` lookup and
  `GIO_LAUNCHED_DESKTOP_FILE`), its oracle-labelled frozen case set (67 cases / 31 classes), the
  seeded fresh leg and the counted mutant population (69). Counter
  `quality/counters/c1-r99-launchenv.py`; predicate `PRED-C1-r99-v1`; measured at
  `56a9b2992f1bcd1a1752f77b5b8ce8c4bc8634ea`; receipt
  `.ufo/waves/round-99/receipts/c1-measured-r99.txt`; separability receipt
  `.ufo/waves/round-99/receipts/c1-at-base-r99.txt`.
- **C2 — operability: the harm watch as an instrument.** Land `quality/harm-watch.py` (frozen
  28-leg panel with per-leg `rc` + stdout marker expectations; census that fails closed on a leg
  the panel declares but does not carry; per-leg timeout and scratch isolation) and
  `quality/counters/c2-r99-harm-watch.py` (planted dropped-leg / extra-leg / wrong-expect /
  wrong-marker panels, a marker-blind gate copy, an always-OK stub, its own fixture selftest).
  Predicate `PRED-C2-r99-v1`; measured at `3b69f04113a235aace713bc1c84ea2b695606b6a`; receipt
  `.ufo/waves/round-99/receipts/c2-measured-r99.txt`; separability receipt
  `.ufo/waves/round-99/receipts/c2-at-base-r99.txt`.
- **Frontier step (§2b).** `corpus/SOURCES.md` 466 → 469 rows (S532 `gio-tool-launch.c`, S533
  `gutils.c`, S534 the Desktop Entry Specification's recognised keys), all opened this round with
  located quotes in `corpus/lessons/round-99.md` `## Gate`; census start/end rc 0
  (`receipts/census-start-r99.txt`, `receipts/census-end-r99.txt`); mistakes M99-1..M99-3; the
  sourced claim is C1 (S532/S533/S534).
- **Record repairs (not claims):** the eight round-98 spot-check defects D1–D8, answered in
  `.ufo/waves/round-99/w1/R99MReviewRecords.md` and in the report.
- **Wave:** one v1 wave `w1`, 12 seats (1 scout, 1 scribe, 1 connector, 4 executors, 2
  reviewers, 1 critic, 2 mutation-testers; attack 6/12 = 50 %). No planner seat in the wave —
  the L1 holds the canonical planner seat; the bounded planning data-walk rode the scout and the
  records reviewer. No residual call. No dead seats.

## Pre-file amendments (Amendment 59)

Each amendment is the choice "amend the frozen claim down to the enforceable property, citing the
artifact", taken at the freeze/closure boundary before the report. The artifact paths are
lane-relative under `.ufo/waves/round-99/`.

### A1 — C1's before-state named a primitive that already existed

- **Trigger:** `.ufo/waves/round-99/w1/R99MReviewRecords.md` §9.11 (records reviewer). The C1
  claim said "at the base revision no lane tool answers ... the post-prepend `argv[0]` program
  lookup"; `tools/mado-mime.py` at the base already models `g_find_program_for_path` for its own
  resolver (`git show 2cbaa141:tools/mado-mime.py`, `find_program` at `:467`, doc line `:45`).
- **Narrowed sentence (filed):** "At the base revision no lane tool answers the *launch spawn
  environment* — the composite of the load gate, `Terminal=true` terminal selection and prepend,
  `Path=` cwd, post-prepend `argv[0]` lookup and `GIO_LAUNCHED_DESKTOP_FILE` — for one desktop
  file, a list of arguments and a PATH string. The `g_find_program_for_path` primitive exists in
  the base tree (`tools/mado-mime.py:467`); the composite and its four refusal causes do not."
- **Counter/predicate:** unchanged (`PRED-C1-r99-v1`); the measured number is unaffected.

### A2 — C1's declaration line citations (errata, not a target change)

- **Trigger:** `w1/R99MReviewRecords.md` §9.1–§9.2. R4's spawn call is
  `gdesktopappinfo.c:3134`, not `:3116-3126`; R7's `!IS_DIR` load-gate test is `gutils.c:340`
  (the PATH-walk test is `:487`), not `:352-356`.
- **Filed:** the rules' semantics stand as measured; the report and the entry cite `:3134` and
  `:340`/`:487`. The declaration's line labels are corrected in the record, not re-frozen.

### A3 — C2's `selftest_checks` is the counter's selftest, not the gate's

- **Trigger:** `w1/R99MCriticC2.md` F3 and `w1/R99MMutC2.md` F3/F4. The predicate's
  `selftest_checks >= 12 AND selftest_failed == 0` is the *counter's* fixture pipeline
  (`quality/counters/c2-r99-harm-watch.py:298`, 17 checks at the frozen bytes); the gate's own
  `HARM_WATCH_SELFTEST: checks=26 failed=0` is never run by the counting command, and 19 of the
  mutation seat's 51 kills are visible only there.
- **Narrowed sentence (filed):** the predicate's `selftest_checks`/`selftest_failed` are the
  counting command's own fixture selftest. The gate's `--selftest` is a separate, unscored check
  (named limit); a gate whose `--selftest` is vacuous is not excluded by `PRED-C2-r99-v1`.

### A4 — C2's "every leg runs" holds on the measured panel, not on a setup-error panel

- **Trigger:** `w1/R99MCriticC2.md` F9. Measured on planted fixtures: a per-leg setup failure
  prints that leg's `LEG` line with `rc=SETUP`, then `HARM_WATCH: setup-error leg=<id> detail=…`
  and exits 2 without running the remaining legs.
- **Narrowed sentence (filed):** "the panel's 28 legs run once each on the measured panel; a leg
  that hits a setup error aborts the remaining panel and exits 2 (measured on planted fixtures)".
  The frozen run has no setup error (`legs_run=28`).

### A5 — C2's "the two dropped legs were noticed only by the outside spot-check" is half wrong

- **Trigger:** `w1/R99MReviewRecords.md` §8 (D5's first-run claim) and the committed bytes:
  `.ufo/waves/round-98/receipts/harm-final-r98.txt:41-43` already names `r97c2_counter_selftest`'s
  omission and its placeholder; that note landed at `fa4445af`, before the spot-check at
  `2cbaa141`.
- **Narrowed sentence (filed):** "`r97c1_filetype` was noticed only by the outside spot-check;
  `r97c2_counter_selftest` was already named in the lane's own final round-98 watch receipt. The
  instrument that would have caught both — a frozen panel with declared legs — lands this round."

### A6 — C2's census checks beyond the declared-but-absent leg

- **Trigger:** `w1/R99MMutC2.md` F4. `PANEL_LEG_COUNT`, `PANEL_DUPLICATE` and
  `PANEL_ROUND_MISSING` are implemented and exercised by the gate's `--selftest` only; the
  round counter's planted panels do not exercise them (the explained-delta rule keeps the
  dropped-leg and extra-leg plants at exactly one finding).
- **Narrowed sentence (filed):** the counter-verified census property is "fails closed on a leg
  the panel declares but does not carry" (plus the extra-row refusal). The count/duplicate/
  round-missing checks are gate behaviour, exercised by the gate's own selftest, not by
  `PRED-C2-r99-v1`.

### A7 — C2's r97 leg is a base-rev replay, not a measured-tree leg

- **Trigger:** `w1/R99MCriticC2.md` F5/§3.2. `r97c2_counter_selftest` pins `--rev 2cbaa141…` and
  the base pins by its own row construction; with the r97 pins it prints `SETUP_ERROR`. It is
  green at the base and is the only panel row that does not exercise the measured tree.
- **Filed:** the report and the panel note call it a historical base-rev replay; the other 27
  rows run at the measured revision.

### A8 — C1's R6 unset-PATH default is modelled but unobservable on the frozen plane (named limit)

- **Trigger:** `w1/R99MMutC1.md` §2 and Findings 6. The counter always passes `--path` and the
  probe always sets `PATH`, so the `/bin:/usr/bin:.` default branch is unreachable; both mutant
  directions are recorded as non-killers with their arguments.
- **Filed:** added to C1's named limits. The claim's five scored surfaces are unaffected; no
  case claims to verify the unset-PATH branch.

### A9 — C2's frozen number is unmet at the frozen per-leg cap: the claim files as an honest stop

- **Trigger:** the attempt-4 re-derivation of the frozen counting command
  (`.ufo/waves/round-99/receipts/c2-measured-r99.txt`) scored `mismatches=2`: `r92_gate_defects`
  and `r97c1_filetype` both hit the panel's frozen 600 s per-leg cap (`rc=124`,
  `timeout-after-600s`) under fleet-wide host load (load average 327 on 32 cores). The two-leg
  probe at a short scratch root (`receipts/c2-probe-r99.txt`) reproduces both timeouts; the
  earlier full-panel run's `r97c1_filetype` `rc=2` was the AF_UNIX path-length failure of its
  fresh generator, fixed by the short scratch root (the probe rules it out).
- **Pre-freeze warning:** `w1/R99MMutC2.md` F5 named exactly this class — the panel's per-leg cap
  has no headroom, so a lowered cap turns a slow leg into a red panel (the cap was re-frozen
  3600 s → 600 s at `e39cd5e0`, before the wave returned).
- **Filed (binary choice taken):** **honest stop**. `PRED-C2-r99-v1` is not narrowed and its
  target is not moved: at the measured revision the frozen predicate is unmet (26/28 legs green,
  two timeouts) on this host. The round's deliverable is the instrument plus this diagnosis; the
  repair is routed to round 100 (re-freeze the panel with a per-leg cap above the measured worst
  leg plus headroom, or declare a per-leg expected timeout), never applied after data. The
  declaration's attempt-3 `TARGET_MET` line carries no receipt; the attempt-4 re-derivation is the
  measured value and is the one reported.

## Filing rule

The report files the narrowed sentences (A1, A3, A4, A5, A6), keeps `PRED-C1-r99-v1` exactly as
frozen, files C2 as the A9 honest stop on the unchanged `PRED-C2-r99-v1`, and records A2/A7/A8 as
errata/named limits. The pre-file falsification ledger
`.ufo/waves/round-99/claim-falsification.tsv` points here.
