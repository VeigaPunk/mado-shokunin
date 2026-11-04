# R70ExecCadence — harm-watch and publication cadence, round 70

Seat: `R70ExecCadence` (leaf; read-only battery, no production draft, no scoring run of C1/C2).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Assigned scored rev: `5144a6b5f43225d8021a469f4d24c19558026b9e`.
Live lane HEAD at last check: `f754347a` (HEAD advanced mid-run by jj export: `5144a6b5 ->
9508e878 -> 5adba5a9 -> 71caa8b7 -> 3aea1e10 -> f754347a`; instrument bytes at the last two equal
`71caa8b7`, and the lane is still being edited by sibling scribe seats). Both revs measured where
the difference matters.
Evidence transcript: `.ufo/waves/round-70/w1/R70ExecCadence/cadence-r70.txt`, sha256
`47adb786ce0ed3eb4b289a80d1a80987f50912a517d331d6524b902f20e8759f`.

## Deliverables

- `cadence-r70.txt`

## Findings

1. **Hermetic gate green.** `bash tools/mado-verify.sh --selftest` rc 0,
   `MADO_SELFTEST: 460/460 assertions passed`.

2. **The assigned landing command is a setup failure, not a leg result.** With the literal
   arguments (`--round 69`, no `--citecheck-paths`) it exits 2 before any leg:
   `landing-counters.sh: citecheck path missing: .../.ufo/waves/round-69/receipts`. That default
   directory is not committed at 5144a6b, at HEAD, or at any earlier commit (no deletion in
   history; round-69's tree has no `receipts/` member), and `.ufo/waves/round-70/receipts` is
   absent too, so `--round 70` dies identically. An explicit clean path is mandatory.
   With `--citecheck-paths .ufo/waves/round-69/claims-declaration-r69.md` at 5144a6b: rc 1,
   `MADO_LANDING_COUNTERS: RED (nav=0 usedby=0 ledger=1 citecheck=0)`. nav `indexed=81/81` rc 0,
   usedby `rows=375` rc 0, citecheck `citations=11 resolved=11` rc 0; ledger rc 1,
   `population=119 ledger_rows=116 uncovered=3` naming exactly the three new r70 counters.
   At HEAD the same command is GREEN: all four legs rc 0, `population=119 ledger_rows=119
   uncovered=0`, `rev=71caa8b7`. The literal default-path form still exits 2 at HEAD.

3. **Axis table not stale at the assigned rev, stale at the integrated content.**
   `check-axis-scores.py --repo . --rev 5144a6b` rc 0: navigation 81/81, calibration 86/86,
   operability 12/12, `checked=3 mismatched=0`; identical at `71caa8b7`. The gate derives only
   from `check-index.py --rev`, `.ufo/waves/round-31/c2/count.py` and `check-index.py --selftest`;
   no rule reads the three new instruments, so their arrival cannot stale the table.
   At the later integrated content `f754347a` (two knowledge entries + registry/index/scorecard
   rows) it is **stale**: `navigation published=81/81 derived=83/83 verdict=STALE`,
   `checked=3 mismatched=1`, rc 1. The published round-70 block still reads "navigation 81/81;
   calibration resolved-active 86/86; operability selftest 12/12, ledger 119/119" while
   `check-index` is 83/83. This is publication order, not an instrument effect; re-publish
   navigation 83/83 before closure.

4. **All nine assigned instrument selftests green, rc 0** (plus the landing instrument's own
   selftest as an extra): r69 paired-recipes 28/28, r69 landing-controls 59/59, r69
   guard-dominance 43/43, r70 landing-controls 68/68, r70 real-children 26/26, r70 carriers 49/49,
   check-wave-done 62/62, check-tool-ledger 54/54, mado-receipt-citecheck 12/12, landing-counters
   62/62. Every `--scratch-root` consumer requires a pre-existing directory (rc 2 otherwise) and
   was given one under the seat scratch; none was given an inherited TMPDIR.
   Because HEAD had moved past the assigned rev, the two r70 counters were also re-tested from
   their committed 5144a6b blobs (`git cat-file blob`): 26/26 rc 0 and 49/49 rc 0. The frozen
   round-69 harm-watch scoring leg also holds: `MADO_R69_PAIRED_RECIPES: killed=3/3 applied=3/3
   base=0/3 verdict=TARGET_MET rev=5144a6b`, rc 0.

5. **Criterion 107 green.** `check-anchor-cover.py --repo . --rev 5144a6b --entry
   corpus/knowledge/gate-guard-dominance-r69.md` rc 0: `CHECK107: rows=8 covered=8 miss=0
   verdict=OK`. The tool emits no `entries=` token; `rows` is the entry count.

6. **Contract gates at 5144a6b: three green, one pre-existing red.**
   `check-evidence-pointers.py --repo . --rev 5144a6b --branch master` rc 0,
   `dangling_r36=0 inherited_dirty=0 scratch_disposition_ok=1 tip_axis_transcript=1
   verdict=TARGET_MET` (lane HEAD is detached; the local `master` branch contains the rev).
   `check-landed-contract.py --frozen-rev 5144a6b --frozen tools/mado-terminal.py --landed
   tools/mado-terminal.py` rc 0, `CHECK96: frozen=9 landed=9 added=0 removed=0 unregistered=0
   verdict=OK` — the lane's only contract-bearing docstrings are `tools/mado-terminal.py` and the
   gate itself, and no round-70 tool adds a contract list.
   `check-index.py --repo . --rev 5144a6b` rc 0, `indexed=81/81 missing=0 dangling=0
   duplicates=0 coverage=10.0000/10`.
   `check-deliverables.py --repo . --rev 5144a6b --report <12 committed round-69 seat reports>`
   rc 1, `reports=12 declared=5 exists=4 absent=1 undeclared=8 verdict=FAIL`: the ABSENT is
   `R69MutBattery`'s trailer carrying a leading `mado-shokunin/` (resolver doubles the seat
   prefix), and 8 reports carry no `Report:` trailer. Same historical grammar class as the
   round-69 seat's round-68 measurement; not round-70 harm.

7. **Scope: no write outside the seat dir; status not empty for reasons outside this seat.**
   Snapshot method: `date +%s` before the first run (23:32:14 -0300), then a full
   `find -printf '%T@ %p'` snapshot (45,997 files), repeated at the end with `.git`/`.jj` pruned
   and the seat path filtered: 30 paths changed in the window, all L1 or sibling-seat material
   (L1 commits 5adba5a9/71caa8b7; scribe notes and `SCORECARD.md`/`SOURCES.md` edits; sibling
   seats `R70ExecC2Rule`, `R70ExecHarness`, `R70ScoutCensus`, `R70ScoutSources`,
   `R70ScribeEntryC1/C2`, `R70ScribeRowLesson`), plus three ignored `__pycache__` files from
   concurrent executions that import the modules (a directly executed script is never cached as
   `__main__`; mtimes 23:32:56 / 23:36:12 / 23:37:29). No production source path was written by
   this seat. `git status --porcelain` is **not empty**: at the last check before yield (HEAD
   `f754347a`) it reads `M corpus/SOURCES.md`,
   `M corpus/knowledge/guard-carrier-shapes-r70.md`,
   `M corpus/knowledge/landing-kill-credit-real-children-r70.md`, `?? .ufo/waves/round-70/w1/`,
   `?? corpus/lessons/round-70.md` — all sibling/L1 scribe work; the lane is under active
   concurrent edit, so that line is a timestamp (a check seconds later also showed
   `M quality/counters/c2-r70-carriers.py`). No tracked path was modified by this seat.

## Risks for the L1

- **Rev pinning.** `git diff --stat 5144a6b..HEAD` shows post-freeze edits to
  `c1-r70-real-children.py` (+1 line), `c2-r70-carriers.py` (8 lines) and `tool-ledger.md` (+3).
  Selftests pass on both sides, but the claim's counting command must name the final content
  commit explicitly. `--rev HEAD` at measurement time is not the frozen 5144a6b bytes. At the
  last check the worktree also carried an uncommitted `M quality/counters/c2-r70-carriers.py`
  (sibling edit), so even HEAD's bytes were not yet stable: pin the rev only once
  `git status --porcelain` is clean for `quality/`.
- **Landing invocation.** The declaration's harm-watch sentence `quality/landing-counters.sh
  --round 69` cannot pass as written at any rev; the L1 must add `--citecheck-paths` (as
  round-69's own GREEN receipt implies) or commit a clean `receipts/` directory.
- **Axis publication stale after the entries landed.** At `f754347a` `check-index` is 83/83
  (rc 0) but the published round-70 axis block still says navigation 81/81, so
  `check-axis-scores.py --rev f754347a` reads `checked=3 mismatched=1`, rc 1 (navigation STALE).
  Re-publishing navigation 83/83 is required before closure; at `5144a6b` and `71caa8b7` the same
  gate was 3/3 MATCH, so this is publication order, not the new instruments.
- **Round-70 report grammar.** Criterion 101 will fail the wave if seat reports omit the
  `Report:` trailer or use lane-relative rather than seat-dir-relative `## Deliverables` bullets
  (this report uses a seat-dir-relative bullet and a lane-relative trailer).

## What to re-run at the final measured content

`bash quality/landing-counters.sh --repo . --rev <final-content-sha> --round 69 --scratch-root
<dir> --citecheck-paths <clean committed artifact(s)>` plus
`python3 quality/check-axis-scores.py --repo . --rev <final>`,
`python3 quality/check-index.py --repo . --rev <final>`, `bash tools/mado-verify.sh --selftest`,
and the six counter selftests — with `--rev` pinned to the final commit, never `HEAD`;
`check-index` must read 83/83 and the published axis line must read navigation 83/83.

## Resources

No tools installed or upgraded (pacman paused; nothing needed). No desktop, compositor, service,
session or package probe. Scratch `/fast/scratch/hyaku/mado-r70/R70ExecCadence` removed and
verified absent before yield. No credential material, no screenshots, no sibling-lane write.

Report: .ufo/waves/round-70/w1/R70ExecCadence.md
