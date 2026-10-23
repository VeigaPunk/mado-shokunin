C2 JUDGMENT: unprovable-but-better — the ledger replaces the round-24 status table's 12-of-15 coverage, transcribed counter output, and unmarked stale rows with a complete 15-identity / 27-occurrence reconciled table whose statuses were re-derived by fresh sandbox runs at base `41cc04c8` (my own re-runs reproduced every row I spot-checked, including both stale rows), and it marks the two stale claims with in-section pointers.

# RevC2Judgment — named non-author review of `## Current state (round 25)` (SCORECARD.md, working tree)

Seat: `MadoR25A3.RevC2Judgment` (reviewer, residual attack call). I did not author the artifact or any of its
inputs; this is a recommendation, not an admission. Artifact under review: the appended section
`## Current state (round 25)` (working-tree `SCORECARD.md:1629-1668`), plus the two R6 pointer paragraphs at
working-tree `:440-443` and `:1350-1352`. Prior state: `41cc04c8:SCORECARD.md` (sha256
`6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08`, 1,618 lines), esp. the round-24 status table
at base `:1573-1596`.

## Acceptance test applied (CritC2Ledger §"Non-author acceptance test")

1. **Independent population recovery — PASS.** My own census script
   (`/fast/scratch/hyaku/mado-r25a3/res/RevC2Judgment/census.py`, pipe-table parse excluding fenced code,
   first-cell casefold == `capability`, run on the clone's base blob) reproduced the critic's census exactly:
   `markdown_tables=30, capability_tables=11, table_data_rows=28, placeholder_rows=1 (base :204),
   substantive_row_occurrences=27, distinct_names=15`. The 15 identities and all 27 occurrences (15 repertoire
   rows at base `:308-311, :437-438, :782, :919, :1020, :1158, :1342-1343, :1409-1410, :1464` + 12 lowercase
   status rows `:1575-1586`) are all accounted for in the ledger, either as primary rows or in its
   population/governs-now mapping. The ledger's own population sentence ("9 tables … a tenth … placeholder …
   plus 12 repeated status rows") reconciles correctly with the case-insensitive count of 11.
2. **Reconstruct and reproduce — PASS for the 6 rows I ran; ledger's coverage claim overstated for 3 rows
   (finding F1).** Sandbox: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone` of the lane to
   `/fast/scratch/hyaku/mado-r25a3/res/RevC2Judgment/lane`, detached at `41cc04c8` (`rev-parse HEAD` =
   `41cc04c8d593837a0d5078bffaacdaa163d12897`, `git status --porcelain` = 0 lines throughout). All runs
   `timeout 600 prlimit --as=4000000000`, `python3 -I -B`. Results below.
3. **Receipt provenance — PASS.** Every Cap receipt I re-derived produced revision-bound output that could not
   be a copy of an older receipt (registry counts `rows=168/collisions=4`, tool sha `cd9da20c…`, remote tip
   drift `2896dc4a → fa466833` in Rc1158). Fresh run vs transcribed status is detectable.
4. **Strongest local falsifiers — PASS.** The ledger itself forecloses each mistake the critique named: `:437`
   carries selftest-25/25-green alongside `corpus/SOURCES.md` `collisions=4` exit 1 (selftest alone cannot be
   used to call the row current); `:309` records the live arm actually observed, not `--no-live`; `:1342`
   distinguishes the historical pinned argument `28c6837` from the base run `41cc04c8`; `:1020` says "an exit-0
   reading of this row is wrong"; `:1409` records the `MemoryError` crash-flip caveat rather than letting a
   zero guard count stand unqualified.
5. **Authority and navigation — PASS.** The `governs now` column reconciles all 12 round-24 status rows and the
   round-24 scope note; rejected/harmed dispositions are preserved (H2 named at `:1342`, harm context pointer
   at `:1409`, r24's own `fails` row governs `:1342`); no score, admission, promotion or repaired-behavior
   credit is inferred — the section ends "Not claimed: any score change, admission or restored capability".
6. **Qualitative comparison — improvement named below.**

## Spot-checks I ran myself (clone at `41cc04c8`, 6 rows)

| Row | Ledger claim | My observation | Verdict |
|---|---|---|---|
| `:437` collision screen | fails as stated: selftest 25/25 exit 0; historical registry exit 1 S017→S030; current `corpus/SOURCES.md` exit 1 collisions=4 | **byte-identical**: PASS 25/25 exit 0; historical `FAIL rows=39 … collisions=1` exit 1; current `FAIL rows=168 urls=140 no_url=21 collisions=4 rejected_history=3 supersedes=7` exit 1 with the same four collision pairs (S111→S120, S111→S121, S117→S119, S120→S121) | correct |
| `:919` transcript tripwire | works, **command not runnable as written** (brace form exits 2); per-dir 9/9, 16/16, 33/33, 30/30 | multi-DIR `--selftest` exits 2 `{"error":"usage"}`; per-dir `SELFTEST_SUMMARY: 9/9, 16/16, 33/33, 30/30` all exit 0 | correct, and the unrunnable literal command is a real reader-facing defect the ledger honestly marks |
| `:1342` evidence marker | fails: P 66/66 but L 15/18 at base; literal command pins `28c6837` | my `tw-precision.py 41cc04c8` run (exit 0, 39,308 B — same byte count as both prior seats): score 9.4857, P 66/66, L 15/18, three L cases `exit 0` with `findings: []` vs a `lead` want; `tool_sha256 cd9da20c…` | correct |
| `:782` declared-action classifier | works: selftest 52/52 exit 0; `--frozen` `frozen_match` exit 0 | `SELFTEST_SUMMARY: 52/52 passed` exit 0; `MADO_PLAN: frozen_match` exit 0 | correct |
| `:1464` assessment integrity | works: selftest `pass=20 total=20`, exit 0 | `pass: 20, total: 20, code 0, assessment_oracle_match`, exit 0 | correct |
| `:308` sources registry | works: `mado ok` exit 0, 0 E-codes, 7 W04, 168 rows | `sources-census.sh validate --file corpus/SOURCES.md` → same 7 W04 rows + `file ok`, exit 0; **but the ledger's command cell is not runnable as written** (finding F2) | status correct; command cell wrong |

The remaining 9 rows were checked by reading both receipts (Cap*) and, where they exist, the independent
a3w2 re-derivations (Rc*), which all report byte-identical or revision-faithful agreement; see verification
gaps for what I did not run.

## The concrete improvement (why `unprovable-but-better`, not `unprovable`)

Prior state lacked a correct current-state surface in three specific ways, all fixed:

- **Coverage hole closed.** The round-24 status table (base `:1573-1596`) covered 12 of the 15 capability
  identities — my census confirms only 12 names in `:1575-1586`; rows `:437`, `:438`, `:782` were covered only
  by an appended scope correction that re-ran them once at `39c59630`, and registration admits the 12-row table
  "was itself a transcription of a counter" (round-24 closure §2.2). The ledger covers all 15 identities with a
  fresh run per row at base `41cc04c8` and maps every occurrence of all 27 substantive rows.
- **Present-tense staleness marked.** `:437`'s "current exits 0" (stale since rounds 21-22 added S117-S121) and
  `:1342`'s L 17/18 (measured at `28c6837`; L 15/18 at base, round-21 harm H2) sat unmarked until outside
  closures found them. The ledger marks both `fails` and the R6 pointer paragraphs (working-tree `:440-443`,
  `:1350-1352`) now stand in the stale sections themselves.
- **Misleading command/forms corrected.** The prior state recorded `:919` with a brace command that exits 2,
  `:1343` with a `HARNESS` placeholder, `:1020` in a way a reader could read as "exit 1 = broken", and `:309`
  exercised `--no-live` only with the live arm unobserved. The ledger names each defect and supplies the
  working form; `:309`'s live arm is now actually observed (`MADO_VERIFY: CLEAN (53 pass, 7 notes; file + live
  planes verified read-only)`), which the round-24 table explicitly lacked.

This is not "copied the old table with a nicer denominator": three rows carry new information (309 live arm,
1409 MemoryError finding, 919 usage defect), two rows are new fails with pointers, and the governs-now column
makes the older authority explicit rather than leaving a competing unmarked table. The artifact makes no score
or admission claim, so the remaining irreducibility (no counter, judged-by-reviewer) is the registered design,
not a defect: hence `unprovable-but-better`, not `unprovable`.

## Findings — rows the ledger gets wrong (none overturn a status)

- **F1 (minor, ledger preamble overclaim):** "each row was … re-derived independently by a wave-a3w2 reviewer
  seat" is false for **3 of 15 rows**: `:311`, `:1409`, `:1410`. The a3w2 registry contains exactly 12 `Rc*`
  seats and greps for `a2-guards|mutate-and-run|reached-body|removal-side|mutation regression` over
  `.ufo/waves/round-25/a3w2/` match nothing outside unrelated contexts; no `Rc*311*`, `Rc*1409*` or `Rc*1410*`
  report exists. Those three rows have only their a3w1 Cap runs. (The new `:1681` results row repeats "re-derived
  by a second seat" — same overclaim, outside the reviewed section.) Statuses themselves are unaffected.
- **F2 (minor, command cell wrong):** `:308`'s command `scripts/sources-census.sh validate --root <root>`
  does not exist at base — the script is outside the lane at
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, and the round-24 manifest's `<root>` is a scratch
  census-root dir (conf + `mado-shokunin` symlink), not the tree root. My literal run of the ledger's form:
  `No such file or directory`. The observed status is nonetheless right (my `--file corpus/SOURCES.md` run:
  `file ok`, 7 W04, exit 0).
- **F3 (minor, wrong shift arithmetic):** the population note says "this round inserted 5-line pointer
  paragraphs after `:438` and after `:1343` … rows after them shift by 10". `git diff 41cc04c8` shows the
  second insertion is 4 lines (+5/+4, both gaps consuming the preceding blank): base `:1342-1343` → `:1347-1348`
  is correct, but rows after `:1343` shift by **9** (status rows `:1575-1586` → `:1584-1595`), not 10.
- **F4 (minor, missing run-time datum):** `:1158`'s cell says "(remote tip observed at run time)" but records
  neither the observed tip nor the time. The receipts have it (`2896dc4a` at a3w1 time, `fa466833` at Rc time —
  real drift the Rc seat correctly dates); the ledger line itself does not pin the value, which is acceptable
  but means the ledger alone cannot anchor a later tip comparison.
- **F5 (trivial wording):** `:1410`'s "all guarded counters 0" is shorthand — `vcs_fp 26` is nonzero (the Cap
  report and round-24 manifest correctly scope `vcs_fp` outside this row's counters). `:1409`'s ledger cell is
  accurate including the memory-contingent `MemoryError` caveat.

## Verification gaps and residual risk

- I ran 6 of 15 rows myself (`:437`, `:919`, `:1342`, `:782`, `:1464`, `:308` via `--file`). For `:1409`/`:1410`
  I relied on the a3w1 run receipts (verbatim JSON in both Cap reports cross-agrees: `recall_lost 0`, `vcs_fp 26`,
  `crash_flip 1` at `a8960de` only); for `:309` the live gate run is session-dependent and unrepeatable by me in
  a reviewer seat (its `MADO_VERIFY` live-arm run touched the live compositor read-only — appropriate for an
  executor seat, not re-done here); `:310`, `:311`, `:438`, `:1020`, `:1158`, `:1343` each have one Cap run plus
  an agreeing Rc re-derivation for all but `:311` (F1).
- F1 means the two-second-seat claim should be corrected or three more Rc seats run; it does not change any
  observed status, and the residual call's job is to name it, not silently re-run.
- `:1409`'s `a8960de` `crash_flip 1` is memory-contingent (4 GB cap; the frozen round-20 receipt recorded
  `crash_flip 0` uncapped). The ledger carries the caveat; a future capped replay of `a8960de` is not a stable
  reference on this host.
- `:1158` and `:309` are time-bound observations (live remote tip, live session). The ledger says so; receipts
  carry the values. No regression risk to the verdict.
- Time skew while reviewing: the working tree gained a `## Round 25 — results and author verdicts` section
  (`:1672+`) during my review; the reviewed C2 section itself (`:1629-1668`) was stable. The `:1681` row repeats
  the F1 overclaim (noted above).

## Safety and tool record

Sandbox only under `/fast/scratch/hyaku/mado-r25a3/res/RevC2Judgment/` (`lane` clone, census.py, two receipt
JSONs); `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` unset for all clone operations; no git/jj writes in the lane or
fleet repo; no lane file edited except this report. No packages/services/`~/.config`/compositor state touched;
no `hyprctl` verb issued by me; no nested Hyprland started; no network fetch; all runs under `timeout` +
`prlimit`; `python3 -I -B` (no `__pycache__`). No tools installed or upgraded (git/python3/bash/coreutils already
present), so nothing to record under the tooling directive. An unrun check has not passed: rows I did not run
are reported above as read-from-receipt, not re-derived.
