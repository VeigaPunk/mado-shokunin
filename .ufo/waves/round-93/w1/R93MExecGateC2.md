# R93MExecGateC2 — C2 gate (check-selftest-strength + kill-set)

## Files
- `.ufo/waves/round-93/build/check-selftest-strength.c2.py` (326 lines, stdlib only)
- `.ufo/waves/round-93/build/check-seat-reports-kills.c2.json` (20 kills)
- This report: `.ufo/waves/round-93/w1/R93MExecGateC2.md`

## Gate (DRAFT runs only — labelled DRAFT; no receipts written)
Usage: `check-selftest-strength.py --tool PATH --kills JSON [--scratch-root DIR] [--timeout S] [--allow-sha-drift]`; `--selftest` hermetic (8 checks: OK/SURVIVED/WRONG_CHECK + 5 setup errors).
- (1) unmutated selftest must rc0 failed=0 else rc2; (2) each kill find exactly once in non-selftest code (before `def selftest(`) else rc2, run `python3 -I <copy> --selftest` with TMPDIR/fresh cwd, must rc!=0 and list must_fail among FAIL lines else SURVIVED/WRONG_CHECK; (3) `SELFTEST_STRENGTH: OK|WEAK tool=… kills=N held=H survived=S wrong_check=W` rc0/1/2.
- `tool_sha256` mismatch rc2 unless `--allow-sha-drift` (counter passes it when it applies weakenings).
- ASCII output.

DRAFT results (all runs `--timeout 5` unless noted):
- `python3 quality/check-seat-reports.py --selftest` → checks=23 failed=0 rc0.
- Gate on real tool+kill-set → `SELFTEST_STRENGTH: OK tool=quality/check-seat-reports.py kills=20 held=20 survived=0 wrong_check=0` rc0 (twice, rerun after fix).
- Gate on weakened copy (F3 check forced pass, `--allow-sha-drift`) → `SURVIVED k-round-dedup` + `SELFTEST_STRENGTH: WEAK tool=quality/check-seat-reports.py kills=20 held=19 survived=1 wrong_check=0` rc1.
- Gate `--selftest` → `SELFTEST_STRENGTH_SELFTEST: checks=8 failed=0` rc0.
- Mid-run bug found+fixed: relative `--tool` resolved under subprocess cwd → absolutised script path in run_selftest; missing `--scratch-root` dir → makedirs.

## Kill-set (20 kills, each unique)
tool_sha256 176fc066…1663a = `quality/check-seat-reports.py` at base rev.
Each kill's find/replace was verified in scratch probes: mutated copy's `--selftest` fails exactly {must_fail}; find occurs once in lines before `def selftest()` (check-seat-reports.py:259). Full table:

| id | must_fail (selftest label) |
|---|---|
| k-unsafe-abs | rev: absolute trailer path -> SR03 |
| k-tok-ascii | name with space and non-ASCII path -> ASCII tokens (F2) |
| k-round-dedup | repeated --round counts once (F3) |
| k-plain-prose | prose Report line is not a trailer -> SR04 |
| k-plain-no-M | plain residual trailer -> SR01 rc1 |
| k-missing-tasks † | missing -> SR01 rc1 |
| k-git-size | rev: present -> OK rc0 |
| k-rev-size-plus | rev: empty and missing -> SR02 SR01 rc1 |
| k-wt-size-plus | empty -> SR02 rc1 |
| k-all-rounds | --all scans every round |
| k-wt-islink-noleaf | symlinked report -> SR03 rc1 |
| k-wt-islink-noinside | worktree: report through a symlinked parent dir -> SR03 (F5) |
| k-git-islink | rev: symlinked report -> SR03 rc1 |
| k-git-check-dispatch-link | rev: symlinked dispatch -> rc2 (F1) |
| k-wt-check-dispatch-link | worktree: symlinked dispatch -> rc2 (F1) |
| k-nodispatch-filter | no dispatch for round -> rc2 |
| k-badjson-cont | bad dispatch json -> rc2 |
| k-all-nodispatch | --all with no dispatch -> rc2 |
| k-fifo-msg | worktree: FIFO dispatch -> rc2, no hang (F4) |
| k-found-last | last trailer wins |

† k-missing-tasks: `for t in tasks:` → `for t in (tasks if not isinstance(tree, WorkTree) else tasks[:1]):` — verified unique (worktree 2-task dispatch only occurs in `missing`; plain `tasks[:1]` also kills rev-empty-missing, so the WorkTree branch is needed). It is contrived (no natural off-by-one would branch on tree type); treat as a placeholder — a more natural unique killer for `missing` would need a fresh idea at freeze.

## Findings: 3 checks have NO achievable unique killer (L1 must decide before freeze)
1. `all present -> OK rc0` — its production path (WorkTree.size present + bad==0 + rc0) is shared with `missing`'s A seat (same file `x`, single round/wave). Every single-site mutant tried flips ≥1 other check: SR01-text (7 fails), size-None (8), present-in-bad (all+rev present), getsize+1 (empty), getsize−1 (missing+empty). Only separation is a contrived presence+mode branch.
2. `unsafe -> SR03 rc1` (worktree `../x.md`) — FULLY MASKED: `unsafe()` dotdot branch is redundant in worktree mode because `WorkTree.is_link()` → `inside()` rejects any `../` path first (removing dotdot → rc0, no fails). The `unsafe_false` mutant kills only `rev: absolute trailer path -> SR03`. In rev mode there is no `../` fixture, so the dotdot branch has zero observable coverage. Selftest-coverage defect in the tool (finding, not gate defect).
3. `untrailed -> SR04 rc1` — shares the `if not found` → SR04 branch with `prose Report line is not a trailer -> SR04` (the only two `found==[]` fixtures); SR04 first-token mutant fails both; SR04 text after first token is unchecked by the harness (`ids` compares first token only), so text mutants are silent (verified: removing `{name}` → rc0).

Also uncovered by design: `GitTree` tree-prefix dispatch-dir logic (check-seat-reports.py:88-92) and `WorkTree.paths` dir-named dispatch (line 147) have no fixtures at all (mutants → rc0/no fails); the `loads_type` list-check and `paths()` prefix filter are similarly unexercised (rc0). The gate cannot protect checks the tool's selftest never exercises — L1 may want fixtures, not kills.

## Notes for L1/counter
- Kill order is arbitrary; all 20 verified together by the gate (held=20).
- Gate reads kill-set `tool` field for the verdict tag only; `--tool` path is authoritative.
- No installs. Scratch `/fast/scratch/hyaku/mado-r93/R93MExecGateC2/` removed on exit (probes + weak.py + scratch/ deleted).

Report: write your scoped findings to .ufo/waves/round-93/w1/R93MExecGateC2.md
