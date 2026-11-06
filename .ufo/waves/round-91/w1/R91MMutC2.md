# R91MMutC2 — mutation probe of the C2 seat-report gate

Seat: R91MMutC2 (mutation-tester, round 91 wave w1). Owner of this file and of
`.ufo/waves/round-91/controls/seat-reports-mutants-r91-mc.json`.

Candidate under test: `.ufo/waves/round-91/build/check-seat-reports.c2.py`
**sha256 `189b143735499d703c25354bae7e860ec057c9652736875c103e258c193bc5c8`, 14765 bytes** (the bytes
present in the lane when this probe closed; re-hashed after the last run, unchanged).

Scratch: `$HYAKU_SCRATCH/mado-r91/R91MMutC2` (`/fast/scratch/hyaku/mado-r91/R91MMutC2`), deleted on exit.
No tool installed or upgraded. Nothing written outside this file and the mutants control file.

## 0. The candidate moved three times during the seat (record, not complaint)

| snapshot | sha256 | note |
|---|---|---|
| v1 | `732fcdad…` | first bytes I mutated (36 mutants, 12-check selftest) |
| v2 | `cde29cbb…` | symlinks -> SR03 both modes, `untrailed` counted in rc + summary, cat-file fallback dropped, 12 checks |
| v3/v4 | `189b1437…` | `--all` with no dispatch -> SETUP_ERROR, 3 rev-mode selftest cases, 16 checks |

The first full mutant sweep ran on v1; the final one on `189b1437`. Mutants were re-derived for the final
bytes (every `find` occurs exactly once there — re-checked, and the counter re-checks it and fails loudly
with `SETUP_ERROR mutant <id>: find occurs N times` if the bytes move again).

One real defect was observed live at v1 and is **closed** in `189b1437`: a symlinked report counted
*present* at `--rev` (git 120000 blob, size = len(target string)) and *missing* at `--worktree`. Evidence
(v1 harness, one fixture tree read two ways): `--rev` → `present=4 missing=2`, `--worktree` →
`present=3 missing=3` for the same commit. `189b1437` reports SR03 in both modes (fixture H01/`REVFIX`).

## 1. Method

47 mutants, single find/replace each, find exactly once (`mutants.py` in scratch; emitted to the control
file). Each mutant was run through three detector families and then through the round's own expectation
machinery:

- **(a)** the candidate's own `--selftest` (stdout compared verbatim, not only rc);
- **(b)** `--rev cc0381db --all`, `--rev cc0381db --round 90`, `--round 89`, `--round 91`, `--rev no-such-rev`,
  plus a rev-mode fixture repo (one 1-byte report, one 0-byte, one missing, one committed symlink, one report
  outside `.ufo/waves`, one trailer naming a tree);
- **(c)** 21 worktree fixtures (present, missing, empty, absolute, `../`, `a..b.md`, untrailed, plain
  residual trailer present/missing, rendered-beats-plain, first-vs-last trailer, inline mention, trailing
  prose, symlink, no dispatch, bad JSON, flat dispatch, non-list tasks, nested dispatch, two rounds,
  `--all` with no dispatch) plus the setup-error calls (no mode, `--all`+`--round`, missing repo);
- **(d) DRAFT** the real counter `quality/counters/c2-r91-seat-reports.py` with the generated set from
  `controls/gen-c2-set-r91.py` + `controls/seat-reports-labels-r91.json` (87 expectations: 46 revision,
  40 fixtures, 1 `--all`), `--draft-check` on the candidate and my mutants file pinned by sha256.

DRAFT label: the (d) run is a **draft measurement**, not a measurement; no receipts were written.

## 2. Baseline (pristine bytes), exact commands and exit codes

| # | command | rc | output |
|---|---|---|---|
| 1 | `check-seat-reports.c2.py --selftest` | 0 | `SEAT_REPORTS_SELFTEST: checks=16 failed=0` |
| 2 | `--rev cc0381db… --all` | 1 | `rounds=46 waves=61 seats=1732 trailered=1732 present=1599 missing=133 empty=0 unsafe=0 untrailed=0 verdict=MISSING` (133 SR01) |
| 3 | `--rev cc0381db… --round 90` | 1 | SR01 `R90MScoutSources`, SR01 `R90MScoutCases`; `seats=13 trailered=13 present=11 missing=2` |
| 4 | `--rev cc0381db… --round 89` | 0 | `seats=16 trailered=16 present=16 verdict=OK` |
| 5 | `--rev no-such-rev --all` | 2 | `SETUP_ERROR not a commit: no-such-rev` |
| 6 | `--rev cc0381db… --round 91` | 2 | `SETUP_ERROR round 91: no <wave>-dispatch.json in .ufo/waves/round-91/` |
| 7 | `--rev cc0381db… --round 13` | 2 | `SETUP_ERROR round 13: …` (legacy dispatch invisible — finding F8) |
| 8 | `harness.py` (47 mutants × 36 calls) | — | 44 killed, 3 equivalent survivors (§3) |
| 9 | `c2-r91-seat-reports.py --draft-check … --mutants seat-reports-mutants-r91-mc.json` | 3 | `DRAFT_TARGET_MISSED … expectations=87 met=87 selftest_rc=0 mutants=47 killed=34 base_met=0 always_ok_met=4 always_missing_met=0 receipt_presence_met=7` |

## 3. Per-mutant verdicts

Legend: `killed@L1-rc` = a detector separates it on exit code; `L2-rc+ids` = on the finding-id list;
`L3-summary-text` = only on the summary line text (rc and ids agree). `pass` = that detector family does
not separate it. `(+n)` = further calls in the same family also kill it.

| mutant | defect class | (a) --selftest | (b) --rev cc0381db calls | (c) my fixtures |
|---|---|---|---|---|
| C2M01 | trailer regex (first vs last match) | killed@L1-rc | pass | killed@L1-rc (+1) |
| C2M02 | plain fallback dropped | killed@L1-rc | killed@L2-rc+ids (+1) | killed@L2-rc+ids (+1) |
| C2M03 | rendered trailer not preferred (plain first) | pass | pass | killed@L1-rc |
| C2M04 | empty file counted present | killed@L1-rc | killed@L2-rc+ids (+2) | killed@L1-rc |
| C2M05 | empty reported as SR01 | killed@L1-rc | killed@L2-rc+ids (+2) | killed@L2-rc+ids |
| C2M06 | unsafe+link check dropped | killed@L1-rc | killed@L2-rc+ids (+2) | killed@L2-rc+ids (+2) |
| C2M07 | unsafe check partial (absolute only) | killed@L1-rc | pass | killed@L2-rc+ids |
| C2M08 | unsafe check partial ('..' only) | pass | pass | killed@L2-rc+ids |
| C2M09 | unsafe check over-broad (substring) | pass | pass | killed@L1-rc |
| C2M10 | symlink check dropped (unsafe kept) | killed@L1-rc | killed@L2-rc+ids (+2) | killed@L2-rc+ids |
| C2M11 | unsafe check dropped (symlink kept) | killed@L1-rc | pass | killed@L2-rc+ids (+1) |
| C2M12 | worktree islink guard in size() dropped (**equivalent**) | pass | pass | pass |
| C2M13 | worktree is_link() stubbed false | killed@L1-rc | killed@L2-rc+ids | killed@L2-rc+ids |
| C2M14 | rev link mode typo (120000 -> 12000) | killed@L1-rc | killed@L2-rc+ids (+1) | pass |
| C2M15 | rev paths() .ufo/waves filter dropped (**equivalent**) | pass | pass | pass |
| C2M16 | ls-tree size off by one | killed@L1-rc | killed@L2-rc+ids (+1) | pass |
| C2M17 | ls-tree not recursive (no -r) | killed@L1-rc | killed@L1-rc (+4) | pass |
| C2M18 | ls-tree sizes column not requested (no -l) | killed@L1-rc | killed@L2-rc+ids (+5) | pass |
| C2M19 | rev blob type filter dropped (**equivalent**) | pass | pass | pass |
| C2M20 | rev size defaults missing to 0 | killed@L1-rc | killed@L2-rc+ids (+3) | pass |
| C2M21 | --all truncated to first round | killed@L1-rc | killed@L1-rc | killed@L1-rc |
| C2M22 | named round without dispatch is not a setup error | killed@L1-rc | killed@L1-rc | killed@L1-rc |
| C2M23 | setup error exits 0 | killed@L1-rc | killed@L1-rc (+1) | killed@L1-rc (+4) |
| C2M24 | setup error exits 1 | killed@L1-rc | killed@L1-rc (+1) | killed@L1-rc (+4) |
| C2M25 | exit code counts SR01 only | killed@L1-rc | pass | killed@L1-rc (+6) |
| C2M26 | exit code ignores SR03 | killed@L1-rc | pass | killed@L1-rc (+2) |
| C2M27 | exit code ignores SR04 | killed@L1-rc | pass | killed@L1-rc (+2) |
| C2M28 | exit code inverted | killed@L1-rc | killed@L1-rc (+5) | killed@L1-rc (+16) |
| C2M29 | summary verdict always OK | pass | killed@L3-summary-text (+4) | killed@L3-summary-text (+10) |
| C2M30 | summary rounds count dropped | pass | killed@L3-summary-text (+5) | killed@L3-summary-text (+16) |
| C2M31 | summary waves count dropped | pass | killed@L3-summary-text (+5) | killed@L3-summary-text (+16) |
| C2M32 | summary trailered includes untrailed | pass | pass | killed@L3-summary-text (+2) |
| C2M33 | summary present double-counted with missing | pass | killed@L3-summary-text (+4) | killed@L3-summary-text (+3) |
| C2M34 | summary present includes empty files | pass | killed@L3-summary-text (+2) | killed@L3-summary-text |
| C2M35 | summary untrailed field dropped | pass | killed@L3-summary-text (+5) | killed@L3-summary-text (+16) |
| C2M36 | missing and empty confused | killed@L1-rc | killed@L2-rc+ids (+2) | killed@L2-rc+ids |
| C2M37 | untrailed not counted (SR04 printed, summary 0) | killed@L1-rc | pass | killed@L1-rc (+2) |
| C2M38 | trailer regex not line-anchored | pass | pass | killed@L1-rc |
| C2M39 | trailer regex end-of-line anchor dropped | pass | pass | killed@L1-rc |
| C2M40 | dispatch regex wave segment accepts slashes | pass | killed@L2-rc+ids | killed@L1-rc |
| C2M41 | flat dispatch (no taskCall) accepted | pass | pass | killed@L1-rc |
| C2M42 | non-list tasks coerced instead of setup error | pass | pass | killed@L1-rc |
| C2M43 | --selftest short-circuits to success | killed@L3-summary-text | pass | pass |
| C2M44 | no-mode setup error exits 0 | pass | pass | killed@L1-rc |
| C2M45 | --round/--all exclusivity exits 0 | pass | pass | killed@L1-rc |
| C2M46 | --all with no dispatch returns success | killed@L1-rc | pass | pass (see F3) |
| C2M47 | selftest rev cases run in worktree mode | killed@L1-rc | pass | pass |

`pass` in column (a) for a mutant means the selftest does not reach it (worktree-only cases, or a
selftest-body edit); it does **not** mean the selftest is wrong.

## 4. Survivors under the round's own machinery (DRAFT) and the cheapest killing expectation

(d) killed **34 / 47**. 13 survived all 87 expectations. Three can never be killed (equivalent mutants);
ten need one expectation each:

| survivor | what it breaks | cheapest expectation that kills it (expected vs mutant) |
|---|---|---|
| MC12 | worktree `islink` guard in `size()` — unreachable now | **equivalent**: `check()` rejects links with `tree.is_link(rp)` (candidate:168) before `size()` (candidate:174) is called |
| MC15 | `paths()` `.ufo/waves` filter | **equivalent**: `DISPATCH.match` is anchored at `.ufo/waves/round-` (candidate:45) |
| MC19 | rev blob-type filter | **equivalent**: `ls-tree -r` emits only blobs and symlinks, symlinks taken by the `120000` branch (candidate:72) |
| MC09 | `unsafe()` over-broad: `".." in path` rejects a legitimate name | fixture `{".ufo/waves/round-7/w1-dispatch.json": trailer -> ".ufo/waves/round-7/w1/a..b.md", "…/a..b.md": "x"}` → **rc 0, ids []**; mutant **rc 1, ids [SR03]** |
| MC29 | summary `verdict` always `OK` | add `"verdict": "MISSING"` to a fixture's `expected_summary` (the labels already carry `expected_summary`, gen passes it, but no fixture pins `verdict`; candidate prints `verdict=MISSING`, mutant `verdict=OK` for F02) |
| MC38 | `TRAILER` not line-anchored | fixture `"see above; Report: write your scoped findings to <path>"` (mention mid-line, file present) → **rc 1, ids [SR04]**; mutant **rc 0, ids []** |
| MC39 | `TRAILER` end-of-line anchor dropped | fixture `"Report: write your scoped findings to <path> (see note)"` → **rc 1, ids [SR04]**; mutant **rc 0, ids []** |
| MC42 | `taskCall.tasks` non-list coerced | fixture `{"taskCall": {"tasks": {"a": 1}}}` → **rc 2, ids []**; mutant **rc 1, ids [SR04]** |
| MC43 | `--selftest` returns 0 without running checks | know-answer on selftest output: `SEAT_REPORTS_SELFTEST: checks=16 failed=0`; mutant prints nothing (rc 0 either way) |
| MC44 | `main()` no-mode error exits 0 | fixture with `argv ["--worktree"]` (gen yields rounds `[]` → the check gets no scope) → **rc 2**; mutant **rc 0** |
| MC45 | `--all` + `--round` exclusivity exits 0 | fixture with `argv ["--worktree", "--all", "--round", "7"]` → **rc 2**; mutant **rc 0** (needs gen to pass the labels' `argv` through instead of rebuilding it, F1) |
| MC46 | `--all` on a dispatch-free tree returns success | fixture `{"files": {}, "dirs": [".ufo/waves/round-914/w1"], "argv": ["--worktree", "--all"]}` → **rc 2, ids []**; mutant **rc 0, rounds=0 verdict=OK** (labels `fx12b` is *not* dispatch-free — it carries a round-900 dispatch, so it does not separate this) |
| MC47 | selftest rev cases silently run in worktree mode | selftest itself: pristine `checks=16 failed=0` rc 0, mutant `checks=16 failed=3` rc 1 — invisible to the set because the counter runs `--selftest` only on the pristine candidate |

## 5. Findings (file:line + reproducing input)

- **F1 — the set rebuilds argv instead of using it** (`controls/gen-c2-set-r91.py:96-98`). Labels fixtures
  already carry `argv` and `mode`; gen keeps only `--all`/`--round`, so fixtures cannot express
  "no scope" or "--all with --round". Cost: MC44/MC45 survive. Cheapest fix: pass `g["argv"]` through
  (strip `--worktree`, map `--rev` to a git fixture), 3 lines, no counter change.
- **F2 — selftest-body defects are invisible** (`quality/counters/c2-r91-seat-reports.py:199-200` runs
  `--selftest` only for the pristine candidate; per-mutant kill is `mm < total`). A mutant confined to
  `selftest()` passes all 87 expectations (MC43, MC47; MC47 makes the candidate's own selftest print
  `failed=3`). Cheapest fix: require, per mutant, `--selftest` rc 0 **and** the `checks=16 failed=0` line.
- **F3 — `--all` on a dispatch-free tree** is covered by the candidate's selftest (v4 added it) but not by
  the set: labels `fx12b-round-without-dispatch-all` has `dirs` *and* a round-900 dispatch, so the tree is
  not empty. Cheapest fix: a labels fixture with `files: {}`, `dirs: [".ufo/waves/round-914/w1"]`,
  `argv: ["--worktree", "--all"]`, `expected_rc: 2` (this is why MC46 survives).
- **F4 — three mutants are behaviour-equivalent on every reachable input** (MC12, MC15, MC19); they can
  never fail an expectation. PRED-C2's "every mutant fails at least one expectation" therefore needs the
  equivalence carve-out (the mutant file marks them `equivalent` non-null) or they must be dropped before
  the freeze, otherwise `killed == len(mutants)` can never hold.
- **F5 — trailer anchoring is untested.** `fx15-prose-report-no-trailer` ("Report: findings go in the
  usual place") does not separate `^`/`$` anchoring: MC38 (drop `^`) and MC39 (drop `\s*$`) both pass it,
  because prose after `Report: ` never matches the single-token `PLAIN` form either way. Two fixtures in
  §4 (inline mention, trailing prose) kill them at rc+ids.
- **F6 — unsafe over-broadness** (`candidate:125-126`): `".." in path` and `".." in path.split("/")`
  differ only for a *name* containing `..`; no fixture tests it (MC09). One fixture (§4) kills it.
- **F7 — non-list `taskCall.tasks`** (candidate:147-149): the set has `fx11` (no `taskCall`) but not
  `tasks` as an object; MC42 coerces and returns rc 1 [SR04] instead of rc 2.
- **F8 — observation, not a mutant: 13 dispatches are invisible.** `DISPATCH` (candidate:45) only matches
  `<wave>-dispatch.json`; `git ls-tree -r --name-only cc0381db -- .ufo/waves | grep -cE 'dispatch\.json$'`
  → 75 files, 61 matched, 54 round directories hold one, `--all` reports `rounds=46`. The 13 unmatched
  legacy files (`.ufo/waves/round-{13..20}/w?/dispatch.json`) hold **849 seats, every one with a
  `Report:` trailer**; `--round 13` exits 2 ("no <wave>-dispatch.json"). The docstring says `--all` covers
  "every round directory holding a dispatch", so either the docstring or the regex is wrong. The one nested
  match candidate (`.ufo/waves/round-50/w1/ScrQualityR50/fixtures/w1-dispatch.json`) is correctly ignored
  by `189b1437` — and MC40 shows a loosened regex would read it as a real dispatch (`--all` SR01 count
  changes; the `--all` expectation kills MC40).

## 6. Controls and restoration

- DRAFT counter controls (same run): `base_met=0` (`quality/check-seat-reports.py` absent at `cc0381db`),
  `always_ok_met=4`, `always_missing_met=0`, `receipt_presence_met=7` — all below `expectations=87`.
- Restoration: mutants were written only under scratch and under
  `.ufo/waves/round-91/controls/seat-reports-mutants-r91-mc.json`; `build/`, `quality/`, `receipts/` were
  never written. Candidate re-hashed after the last run: `189b1437…` (unchanged). Fixture repositories were
  created under scratch with `git -C "$D" init -q` and `rev-parse --show-toplevel` verified before the first
  commit; no mutating git ran in the lane.
- Dead step: the first sweep (v1 bytes, 36 mutants, 2 harnesses, ~40 min total including two candidate
  revisions) is superseded but kept as evidence for the symlink divergence that `189b1437` closes.
- Files written: this report; `.ufo/waves/round-91/controls/seat-reports-mutants-r91-mc.json` (47 mutants,
  schema `seat-reports-mutants-r91-v1`, `tool_sha256` = the bytes above, `equivalent` marked for MC12/15/19).
