# ExecAxisBase — round 47 w1: base receipts for the harm watch

Target: the **base side** of round 47's no-harm comparison. Base = lane tip at round start
`60edb66e2f1cb90acc6e9442fc93ded0ca42d750` (lane HEAD while measuring was `c24adef2`, whose only
delta over base is untracked round-47 wave scaffolding plus committed `round-47/{claims.md,make-w1-spec.py,
w1-dispatch.json,w1-spec.json,receipts/census-before.txt,w1-run.err}`; `git diff --name-status base..HEAD -- tools quality`
is **empty**, so the tool/quality bytes measured here are base bytes).

Scratch: `/fast/scratch/hyaku/mado-r47/ExecAxisBase` (created, used as `TMPDIR`, deleted at the end; a base clone lived
there and was removed with it). Every number below was executed read-only in this session; nothing was installed
(no pacman, no uv — no tool was needed).

## Verdict

| gate | rc | summary |
|---|---|---|
| `quality/check-axis-scores.py --rev 60edb66… --repo .` | **0** | `MADO_AXIS: checked=3 mismatched=0` — nav 63/63, calibration 77/77, operability 12/12, all `MATCH` |
| `quality/check-session-material.py --repo . --rev 60edb66…` | **1** | `SESSION_MATERIAL: files=18371 findings=115` — **base-RED** (§C2) |
| uniform loop `for t in tools/mado-*.py; do python3 -I $t --selftest; done` | mixed | 13 tools: **6 rc=0, 7 rc=2** — the loop is not a uniform contract (§C3) |
| `bash tools/mado-verify.sh --selftest` | **0** | `MADO_SELFTEST: 460/460 assertions passed` |

Both assigned gates reproduce byte-identically on a fresh `git clone -q --shared` of base (§F), so the numbers below are
properties of committed bytes, not of the lane worktree.

## §A Every executed command (rc measured with redirect, never through a pipe)

| # | command (CWD = lane root) | rc | summary line |
|---|---|---|---|
| 1 | `python3 -I quality/check-axis-scores.py --rev 60edb66… --repo .` | 0 | `MADO_AXIS_ROW: axis=navigation published=63/63 derived=63/63 verdict=MATCH` (×3, all MATCH) + `MADO_AXIS: checked=3 mismatched=0 rev=60edb66…` |
| 2 | `python3 -I quality/check-session-material.py --repo . --rev 60edb66…` | 1 | `SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=29 R2_PROC_TABLE=31 R3_MONITOR_IDENT=53 R4_HOME_LISTING=2` / `SESSION_MATERIAL: files=18371 findings=115 rev=60edb66…` |
| 3 | `bash tools/mado-verify.sh --selftest` | 0 | `MADO_SELFTEST: 460/460 assertions passed` |
| 4 | uniform `--selftest` loop over `tools/mado-*.py` | 6×0 / 7×2 | zeros: action-plan `SELFTEST_SUMMARY: 52/52 passed`, devices `59/59`, geometry `94/94`, globals `63/63`, monitors `48/48`, options `211/211` |
| 5 | `tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures` | 0 | `{'code': 0, 'result': 'selftest', 'pass': 20, 'total': 20}` |
| 6 | `tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures` (lane worktree) | 0 | `{'code': 0, 'result': 'clean', 'total': 46}` |
| 7 | same, on the **base clone** (committed bytes only) | **2** | `{'code': 2, 'result': 'could-not-evaluate', 'error': 'FileNotFoundError'}` (§C4) |
| 8–11 | `tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening,w2-regressions}` | 0,0,0,0 | `9/9`, `16/16`, `33/33`, `30/30 passed failed=[]` |
| 12 | `python3 -I quality/check-index.py --rev 60edb66… --repo .` | 0 | `MADO_INDEX: rev=60edb66… indexed=63/63 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| 13 | `python3 -I .ufo/waves/round-31/c2/count.py 60edb66…` | 0 | `METRIC literal lines=74/90 fraction=0.8222` · `METRIC active=77 resolved_active=77 fraction=1.0000` · `PRED-C2-r31-v2 verdict=TARGET_MET` |
| 14 | `python3 -I quality/check-index.py --selftest` | 0 | `MADO_INDEX_SELFTEST: 12/12 assertions passed` |
| 15 | `python3 -I quality/check-axis-scores.py --selftest` | 0 | `MADO_AXIS_SELFTEST: 18/18 assertions passed` |
| 16 | `python3 -I quality/check-session-material.py --selftest` | 0 | `SELFTEST: passed=22/22 failed=0` |
| 17 | `python3 -I quality/check-index-rows.py --rev 60edb66… --repo .` | 0 | `MADO_INDEX_ROWS: rev=60edb66… rows=63 errors=0 warns=3` |
| 18 | `python3 -I quality/check-locators.py --selftest` | 0 | `SELFTEST: cases=18 passed=18 locators=19 miss=6` · `teeth flipped_table_broken=yes flips=11 ok_to_miss=4 miss_to_ok=5` · `SELFTEST: PASS` |

Rows 5–11 are the **correct-form** selftest invocations, read from each tool's own usage text, because row 4 shows the
assigned bare form cannot run them: `mado-assessment.py` and `mado-evidence-audit.py` declare `--selftest` as
`type=Path` (`tools/mado-assessment.py:214`, `tools/mado-evidence-audit.py:271`), `mado-tripwire.py` as
`--selftest DIR` (`tools/mado-tripwire.py:132`), and `mado-anims.py`, `mado-binds.py`, `mado-eventq.py`, `mado-wsrules.py`
have **no selftest at all** (`grep -c -i selftest` = 0 each).

## §B What each axis row's counting rule actually reads

The gate re-derives only three axes (`AXES` at `quality/check-axis-scores.py:32`); `sourced-art` is parsed off the
publication and deliberately not re-derived. The publication it reads is the last unquoted `Axis table re-derived at`
window (2000 chars) of `SCORECARD.md` at the rev — at base that is **`SCORECARD.md:2646`**, which publishes
`navigation 63/63; calibration resolved-active 77/77; operability selftest 12/12`.

| axis | published cell read by (regex) | derived cell read from | what is being counted |
|---|---|---|---|
| navigation | `check-axis-scores.py:60` `navigation (\d+)/(\d+)` | `check-axis-scores.py:134` `indexed=(\d+)/(\d+)` over `MADO_INDEX: … indexed=covered/total` (`quality/check-index.py:137`) | index rows in the corpus index whose anchor exists at the rev — `covered/total`, with `missing=0 dangling=0 duplicates=0`; 63/63 at base |
| calibration | `check-axis-scores.py:63` `calibration resolved-active (\d+)/(\d+)` | `check-axis-scores.py:144` `resolved_active=(\d+)` + `\bactive=(\d+)` over `METRIC active=… resolved_active=…` (`.ufo/waves/round-31/c2/count.py:330`) | **line-counting of `corpus/QUALITY.md` criteria**: `active` = non-superseded criterion lines (90 lines − 13 superseded = 77); `resolved_active` = those whose grounding is literal (`literal lines=74/90` is the all-lines fraction 0.8222, a different numerator); 77/77 |
| operability | `check-axis-scores.py:66` `operability selftest (\d+)/(\d+)` | `check-axis-scores.py:155` `(\d+)/(\d+) assertions passed` over `MADO_INDEX_SELFTEST: passed/len(checks)` (`quality/check-index.py:330`) | **only `quality/check-index.py`'s own internal assertion battery** — 12 fixed assertions at base. It never invokes `tools/mado-*.py` |

Mechanics worth knowing when reading a mismatch: each instrument is run as a **temp copy of the rev's bytes**
(`git show <rev>:<path>`) under `sys.executable -I` with `cwd=repo` and all `GIT_*` variables stripped
(`check-axis-scores.py:110-124`), inside `tempfile.TemporaryDirectory(prefix="mado-axis-")` — so the gate honours
`TMPDIR`, cannot be steered by `GIT_DIR`, and a dirty worktree instrument cannot flatter the result.

## §C What the harm watch must not misread (each item measured)

**C1 — the operability axis is blind to `tools/`.** Since row `operability` counts `check-index.py`'s 12 internal
assertions (§B), adding `tools/mado-terminal.py` (this round's C1) moves **no** axis row, and a broken new tool cannot
turn `check-axis-scores.py` red at all. Any w1/w2 receipt claiming "axis coverage" for the new tool is miscounting:
only the w2 counters (and the tool's own `--selftest`) can see it. Supporting evidence: the axis gate's three derived
instruments are `check-index.py` (×2) and `count.py`; `grep -c 'tools/mado-' quality/check-axis-scores.py` = 0.

**C2 — `check-session-material` is base-RED and must be compared by count, not by rc.** rc=1 with
`files=18371 findings=115` (R1=29, R2=31, R3=53, R4=2) at base, identical on the clone. Harm rule for the integration:
the tuple `(files=18371, findings=115)` and the per-rule tally must not grow; no w1 seat file may contribute a new
`(file, rule)` pair. My own seat files pass a same-shape self-check: `grep -rl '"title"|users:((' `
`.ufo/waves/round-47/w1/ExecAxisBase` = 0 hits, home-path-only lines = 0 (approximation of R1/R2/R4; the real gate only
sees tracked files at a rev).

**C3 — the assigned uniform selftest loop is not a uniform contract.** 13 tools → 6 rc=0, 7 rc=2, and the rc=2s are
*contract mismatches, not failures*: 4 tools have no selftest, 3 require an argument. Baseline numbers that can be
compared across waves are rows 5–11 of §A: `verify 460/460`, `action-plan 52/52`, `assessment 20/20`, `devices 59/59`,
`evidence-audit 46` (worktree only, see C4), `geometry 94/94`, `globals 63/63`, `monitors 48/48`, `options 211/211`,
`tripwire 9/9 + 16/16 + 33/33 + 30/30`. A wave that prints "all tool selftests pass" from the bare loop is either
ignoring seven rc=2s or silently shrinking the set.

**C4 — `mado-evidence-audit.py --selftest` is worktree-green / clone-red at base.** Committed bytes have **0** tracked
entries under the two fixture paths that the manifest declares as *directories*
(`git ls-tree -r --name-only 60edb66… | grep -cE 'AuditRawPathEscape/root/|AuditRawPathDotDotInternal/root/sub/'` = 0),
while the lane worktree holds both as untracked empty dirs (`entries=0`). Measured A/B on the base clone: with the dirs
absent → rc=2 `could-not-evaluate / FileNotFoundError`; after `mkdir -p` of just those two → rc=0 `{'code': 0,
'result': 'clean', 'total': 46}` with `git status --porcelain` still empty. This is the round-44 §F1 property, unchanged;
the base row is **clone-red**. Any later receipt calling it green must name where it got the two directories.

**C5 — `tools/mado-verify.sh --selftest` hardcodes `/tmp` and leaks leftover fixture trees.** `mktemp -d
/tmp/w5-mado-m52-selftest.XXXXXX` (`tools/mado-verify.sh:418`; also documented at `:24`, `:123`, `:271`), so it does not
honour `TMPDIR` — a committed-bytes contradiction of round 47's scratch directive for anything the w1/w2 waves write.
Host state while measuring (read-only observation): **304** ` /tmp/w5-mado-m52-selftest.*` dirs, **80,256 KB** total,
timestamps 12:50–14:36 today, i.e. today's runs leak on the non-success paths (my own run left none: 304 before, 304
after). Not introduced by w1; recorded so a later wave does not attribute the growth to itself or delete a live
sibling's scratch. I deleted nothing there.

## §D Receipts (all under `.ufo/waves/round-47/w1/ExecAxisBase/receipts/`)

| file | sha256 (first 16) | content |
|---|---|---|
| `axis-scores-base.txt` | `ec344e699ebad558` | the three `MADO_AXIS_ROW` lines + `MADO_AXIS` + `rc=0` |
| `axis-navigation-instrument.txt` | `c33cf4c02221e3c8` | `MADO_INDEX … indexed=63/63 … coverage=10.0000/10`, rc=0 |
| `axis-calibration-instrument.txt` | `5db94542b601c3cd` | `METRIC literal 74/90` · `active=77 resolved_active=77` · `TARGET_MET`, rc=0 |
| `axis-operability-instrument.txt` | `f248c726dc3d774a` | `check-index --selftest 12/12` + base `SCORECARD.md` publication locators (13 markers, last at line 2646) |
| `session-material-base.txt` | `d41afd2d7a33c7cf` | 115 `FINDING` lines + per-rule tally + summary + `rc=1` |
| `tools-selftests-base.txt` | `27165c46587f57dc` | the assigned uniform loop: per-tool rc + summary |
| `tool-selftest-surface.txt` | `325ee08a372bea3c` | `selftest` mention count + locators per tool (0 for anims/binds/eventq/wsrules) |
| `tool-selftests-correct-form.txt` | `61f8823a33024b91` | assessment/evidence-audit(+clone A/B)/tripwire×4 with true rcs |
| `mado-verify-selftest-base.txt` | `034a6241a05fca82` | `MADO_SELFTEST: 460/460 assertions passed`, rc=0 |
| `quality-gate-selftests-base.txt` | `3f37e7f079785868` | axis-scores `18/18`, session-material `22/22` |
| `extra-quality-gates-base.txt` | `3fe964c101d3c10b` | `MADO_INDEX_ROWS rows=63 errors=0 warns=3`; check-locators `PASS` |
| `base-blob-hashes-and-contracts.txt` | `70752886c6ab844f` | blob sha256 at base for the 5 instruments + SCORECARD, and the per-tool argparse modes |

Base blob sha256 (full) for drift detection: `check-axis-scores.py 461f913a4d1dc8ba…9ce8dde`,
`check-session-material.py 889f8f057bf04fc7…4646e3fb`, `check-index.py 2c8798ce27e71f86…23c5f684`,
`round-31/c2/count.py 59899256de17f467…00d4a94`, `mado-verify.sh 050efc720599345a…156703f1`,
`SCORECARD.md 18d3119ff2778396…1d8e488`.

## §E Scope and process notes

- Wrote only `.ufo/waves/round-47/w1/ExecAxisBase/` and this report. No tracked file touched, no git/jj mutation
  (read-only `rev-parse`, `show`, `ls-tree`, `diff`, `clone --shared`, `checkout --detach` inside my own scratch clone).
- No subagent, no background job, no labrat probe was needed. No package installed. `pacman` untouched.
- Scratch removed: `rm -rf /fast/scratch/hyaku/mado-r47/ExecAxisBase` (clone included); every citation above points at
  the seat directory.
