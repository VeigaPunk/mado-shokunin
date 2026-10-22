# ReOracle21: C1 oracle guard at the committed tip (round-23, wave 2, falsify)

Seat: MadoR23.ReOracle21 (reviewer, leaf; no subagents). Judged on operability.
Guard: `round-22/replay.py --mode oracle`, which runs the round-21 oracle (52 frozen cases). Target: 35/35 + 17/17.
Object measured: committed tip `2f1134f38930fc8b067d2d7f5bba126338faabdd`, `tools/mado-tripwire.py` blob `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`.

## Verdict

PASS at the committed tip. Round-21 oracle: primary 35/35, supplemental 17/17 (52/52), replay exit 0, no timeout, no spawn or setup error, empty child stderr. Reproduced on the lane path (twice), from a clean clone of the tip, and from a different working directory.

This is a no-harm check, not a repair check:
- The base classifier `cd9da20c…` also passes 52/52, and its per-case payloads equal the tip's on all 52 cases.
- The 52 fixtures contain no `nonlocal` statement, no `global` statement and no `_getframe`, `f_back` or `currentframe` call (step 13).
- The guard is not vacuous. A classifier that reports no findings exits 1 and fails exactly the 23 cases that expect findings (step 8).

Per the L1's message, the lane working tree is being repaired in place and is not measured here. The fresh residual check must re-measure the repaired commit from a clean clone (procedure below).

No blocking finding at the committed tip. Operability hazards are listed under Findings.

## Commands run (exact)

Unless noted, cwd is `/home/vgpnk/Projects/shokunin/mado-shokunin` (the lane). Scratch root is `/fast/scratch/hyaku/mado-r23/ReOracle21/`.

1. Lane tool and tip, read-only: `sha256sum tools/mado-tripwire.py` gave `41489991…` (11:56 UTC). `git show 2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py | sha256sum` gave `41489991…`, a match. Also `git --no-optional-locks` log, show, diff, status and ls-files, and `jj --ignore-working-copy --no-pager -R <lane> op log -n 8`.
2. Guard, lane path (the assigned command, run from the lane root):
   `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/replay.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --mode oracle > <scratch>/guard-oracle-replay.json 2> <scratch>/guard-oracle-replay.stderr`
   Exit 0, 11:58:05.103 to 11:58:06.090 UTC.
3. Rerun, same command: exit 0, 11:58:30.368 to 11:58:31.408 UTC (`guard-oracle-replay-2.json`).
4. Refusal: the replay with a scratch copy of the base classifier as `--tool` exited 2 with `setup_error: "ValueError: --tool must resolve inside the repository"` (`refusal-replay.json`).
5. Clean clone of the tip: `git clone -q --no-checkout <lane> <scratch>/clone-tip`, then `git -C <scratch>/clone-tip checkout -q --detach 2f1134f38930fc8b067d2d7f5bba126338faabdd`. HEAD verified; tool blob `41489991`. Then `python3 -I <scratch>/clone-tip/.ufo/waves/round-22/replay.py --tool <scratch>/clone-tip/tools/mado-tripwire.py --mode oracle`: exit 0, 11:59:06.051 to 11:59:07.079 UTC (`clone-guard-oracle.json`).
6. Other cwd: the lane replay of step 2, run with cwd set to `<scratch>`: exit 0, 11:59:07.110 to 11:59:08.137 UTC (`cwd-scratch-guard-oracle.json`).
7. Base control, direct runner (the replay refuses tools outside the lane, so the base copy lives in scratch): `cp .ufo/waves/round-23/evidence/tool-base-cd9da20c.py <scratch>/base/`, then `python3 -I .ufo/waves/round-21/oracle/measure.py --tool <scratch>/base/tool-base-cd9da20c.py`. Exit 0, 52/52 (`control-base-oracle.json`).
8. Negative control, direct runner, against a scratch classifier whose `main` prints empty findings (`<scratch>/negative/empty-tool.py`): `python3 -I .ufo/waves/round-21/oracle/measure.py --tool <scratch>/negative/empty-tool.py`. Exit 1; primary 19/35, supplemental 10/17; 23 cases fail (the cases that expect findings) and 29 pass (`negative-oracle.json`).
9. Lane states during the window, each measured as a scratch copy with the same runner: state `8975a4da…` (copied 11:59:51 UTC) gave exit 0, 35/35 + 17/17 (`state-1159-oracle.json`). State `82d5ffa8…` (copied after 12:01:03 UTC; lane sha checked before and after the copy) gave exit 0, 35/35 + 17/17 (`inflight-oracle.json`).
10. Bytecode probe: `PYTHONDONTWRITEBYTECODE=1 python3 -I -c 'import sys; print(sys.dont_write_bytecode)'` printed `False`. Loading a scratch copy of the tool through the oracle wrapper's loader wrote `<scratch>/bytecode-probe/__pycache__/tool-probe.cpython-314.pyc`.
11. Frozen-expectation and receipt checks (read-only JSON parse, no classifier run): see the Frozen expectations section.
12. Landed range: `git log --oneline 6b383c465779be3a620905590ae56554e434c395..2f1134f38930fc8b067d2d7f5bba126338faabdd` lists five commits (a28e481, 4de4464, 2e592af, c8cb393, 2f1134f). `git --no-pager diff --stat 6b383c46… 2f1134f3… -- .ufo/waves/round-21 .ufo/waves/round-22 tools` shows only `tools/mado-tripwire.py` (257 insertions, 21 deletions). `git log -- .ufo/waves/round-21/oracle/expected.json` and `…/oracle/measure.py` each show only `b96d1b8` (the round-21 seal).
13. Coverage search (case-insensitive) of `round-21/oracle/inputs` for `nonlocal|global |_getframe|f_back|currentframe|callback`: only `CallbackBoundArgs.jsonl` and `CallbackGlobal.jsonl` matched, both on their `Callback…` ids. Validation: the pattern `nonlocal` over `round-22/oracle/inputs` matched `CX4NonlocalMutation.jsonl`, so the search works.

Installs or updates: none. Existing tools used: `/usr/bin/python3` (3.14.8), git, `jj` (`/home/vgpnk/.local/bin/jj`, read-only), sha256sum, find, stat.

Writes by me: scratch only (`/fast/scratch/hyaku/mado-r23/ReOracle21/`) and this report. One `rm -rf` ran on `<scratch>/clone-tip` before the clone; that path did not exist, so nothing was removed. A lane-wide `find -newer` check run after the guard runs listed only other seats' paths (`w2/out/AttackPerf/…`, `w2/reports/*.md`, `w1/reports/…`). The `tools/__pycache__` rewrite below was seen separately, by `stat`.

## Receipts (scratch)

| Run | Tool sha (before / after) | Exit | Totals (primary / supplemental) | Receipt sha256 (prefix) |
|---|---|---|---|---|
| Guard, lane path | 41489991 / 41489991 | 0 | 35/35 / 17/17 | afc99023… (guard-oracle-replay.json) |
| Guard rerun, lane path | 41489991 / 41489991 | 0 | 35/35 / 17/17 | 7259f990… (guard-oracle-replay-2.json) |
| Guard, clean clone of tip | 41489991 / 41489991 | 0 | 35/35 / 17/17 | 58e034b5… (clone-guard-oracle.json) |
| Guard, other cwd | 41489991 / 41489991 | 0 | 35/35 / 17/17 | 8d7f5af2… (cwd-scratch-guard-oracle.json) |
| Refusal, out-of-lane tool | n/a | 2 | setup_error | 8e17ad0f… (refusal-replay.json) |
| Base control, runner direct | cd9da20c / cd9da20c | 0 | 35/35 / 17/17 | d98ab799… (control-base-oracle.json) |
| Negative control, runner direct | b5bce35e (empty classifier) | 1 | 19/35 / 10/17 | not hashed (negative-oracle.json) |
| Lane state 8975a4da, scratch copy | 8975a4da | 0 | 35/35 / 17/17 | 32da232b… (state-1159-oracle.json) |
| Lane state 82d5ffa8, scratch copy | 82d5ffa8 | 0 | 35/35 / 17/17 | e06a66f8… (inflight-oracle.json) |

Guard receipt fields (run 2 of the lane path): schema `mado-r22-replay-receipt-v1`; mode `oracle`; argv `['/usr/bin/python3', '-I', '<lane>/.ufo/waves/round-21/oracle/measure.py', '--tool', '<lane>/tools/mado-tripwire.py']`; timeout_seconds 810; timed_out false; spawn_error null; setup_error null; runner_sha256 `4eb893d2…`; replay_sha256 `324e7986…`; inner expected_sha256 `fd2bfbc8…`; inner totals `{"primary": {"pass": 35, "total": 35}, "supplemental": {"pass": 17, "total": 17}}`. Each run took about one second (52 sequential children).

## Frozen expectations

- `round-21/oracle/expected.json` has sha256 `fd2bfbc86897e1ee7a79302f6ccf6c3403709b132180864a0674f8212925576f`, equal to `expected.sha256`.
- 52 cases: group `primary` has 35, group `supplemental` has 17. Ids are unique. All 52 fixture sha256 values match.
- I re-derived the pass rule from the raw receipts (the rule at `measure.py` lines 61 to 64) without running any classifier. All 52 pass flags reproduce. Unparsed counters sum to 0. Child stderr is empty for all cases. No error fields. Child exit codes are 0 for the 29 cases with no expected findings and 1 for the 23 with expected findings.

## Clean-clone comparison

The clone's receipt equals the lane receipt except for 76 leaves. All 76 are `payload.files[].path` or `payload.findings[].file`, which hold the absolute input path (clone root versus lane root). Totals, pass flags, exit codes and findings are identical. The clone's runner sha (`4eb893d2…`) equals the lane runner's.

## Bytecode and lane state

- `tools/__pycache__/mado-tripwire.cpython-314.pyc` predates my session. It was created 08:51:18 local (-03), which is 11:51:18 UTC, at 245849 bytes with sha `a4d96614…`. It is gitignored (`.gitignore:3`) and untracked. My guard runs did not change it: sha was identical before and after the first run, and mtime and size were unchanged after the rerun.
- It was rewritten at 09:00:32 local (12:00:32 UTC) to 249423 bytes, sha `c2e01e5f…`. Its header records source mtime 1792670354 (11:59:14 UTC) and size 175636, which matched the lane file at that time. That rewrite came from a lane-path import I did not run.
- Why lane-path runs write bytecode: `-I` does not disable bytecode writing (step 10), and the oracle wrapper loads the tool by path. A missing or stale pyc is rewritten into the lane's `tools/__pycache__`.
- The lane holds 13 `__pycache__` directories. Five were created today, none by my commands: `tools` (11:51 UTC), `round-23/w1/out/CritFrameNeighbour` (11:03), `round-23/c2` (11:44), `round-23/evidence` (11:57) and `round-23/w2/out/AttackPerf` (11:58). I do not know their creators.
- Lane file states seen during the window (`tools/mado-tripwire.py`):

| State | Bytes | Lane mtime (UTC) | Oracle result |
|---|---|---|---|
| 41489991 (committed tip blob) | 173707 | 11:49:30; unchanged through at least 11:59:08 | lane runs, 35/35 + 17/17 |
| 8975a4da | 175636 | 11:59:14 | scratch copy, 35/35 + 17/17 |
| 82d5ffa8 | 174005 | 12:01:03 | scratch copy, 35/35 + 17/17 |
| 1cef299f | 176243 | 12:04:03 | not measured (L1 repair in progress; outside my assignment) |

The L1 reports these edits as its in-place repair. The verdict above is for the committed object only.

## Findings by severity

1. **Medium, operability: lane-path guard runs write bytecode into the lane.** The oracle child loads the tool by path under `-I`, so a stale or missing pyc is rewritten into `tools/__pycache__`. The lane pyc was rewritten at 12:00:32 UTC by a lane-path import I did not run. Mitigation: measure from a clean clone, which writes only into the clone. This is what I did. A harness fix (add `-B` to the child argv, or set `sys.dont_write_bytecode = True` in the wrapper) changes the runner sha recorded in receipts, so it needs an append-only note from the L1. I did not apply it.
2. **Medium, measurement identity (process): the lane tool is not a committed object during the repair.** Receipts record the sha of the file on disk. The lane file changed three times between 11:59:14 and 12:04:03 UTC. Any lane-path run during the repair measures uncommitted bytes. The committed-tip verdict does not depend on this, because the clean clone compiled the tip bytes fresh (the clone had no pyc before its run).
3. **Low, theoretical receipt gap.** CPython's timestamp-based pyc check (header flags 0) compares source mtime at whole-second resolution and source size. A same-second, same-size rewrite could leave stale bytecode running while the receipt reports the new file's sha. Not observed. A clean clone or `-B` removes the question.
4. **Low, coverage: this guard has no case for the regressions the L1 named.** Base and landed payloads are identical on all 52 cases. The inputs contain no `nonlocal` statement, no `global` statement and no `_getframe`, `f_back` or `currentframe` call (step 13), so none of the 52 cases exercises a global or nonlocal callback store or frame reuse in the forms I searched for. The guard is a no-harm check for these 52 fixtures. Its comparison covers only (class, command, evidence) rows, unparsed counters and exit codes in {0, 1}; it does not look at stderr or other payload fields. Discriminating evidence for global/nonlocal callback stores and frame reuse must come from the 12-case repair set and the wave-2 counterexamples, re-run on the repaired commit.
5. **Info: pre-existing pycache.** `tools/__pycache__/` predates my session, is gitignored, and was not touched by me. I did not delete anything. Cleanup is the L1's call.
6. **Info: process observations for the L1.** (a) The jj op log shows `git push --remote origin --bookmark master` (op `ff539ef6d931`) about 11 minutes before my check, after `jj bookmark set master -r 2f1134f3…` (op `ab9b1bc8aa4f`). Origin may already hold the tip. (b) Other seats wrote receipts and reports into the lane's `w2` tree during this window (for example `w2/out/AttackPerf/receipts-series`, `w2/reports/*.md`). I did not measure these.

## Residual risk and verification gaps

- Not run (outside my assignment): primary 57/57, precision 166/175, the corpus comparator, the eleven selftest suites, resource guards, and the 12-case repair set.
- The verdict covers commit `2f1134f3` and blob `41489991` only. The repaired commit needs its own run (procedure below).
- The `8975a4da` and `82d5ffa8` results are from scratch copies, not from the lane file at a stable moment. Only the `41489991` results come from the lane file itself.
- I did not judge the correctness of any repair or of the wave-2 counterexamples. This report covers the oracle guard's operability only.

## Procedure for the fresh residual check

1. `git clone -q --no-checkout <lane> <scratch>/<name>`
2. `git -C <scratch>/<name> checkout -q --detach <commit>`, then confirm `rev-parse HEAD` and the tool's sha.
3. Run the clone's own replay, not the lane's: `python3 -I <scratch>/<name>/.ufo/waves/round-22/replay.py --tool <scratch>/<name>/tools/mado-tripwire.py --mode oracle`. The replay refuses tools outside its own repository root. Expect exit 0 and `{"primary": {"pass": 35, "total": 35}, "supplemental": {"pass": 17, "total": 17}}`.
4. Avoid lane-path runs while the lane is being edited.

## Verdict

PASS: the C1 oracle guard at committed tip `2f1134f3` (tools blob `41489991`) gives 35/35 primary and 17/17 supplemental, with replay exit 0. It reproduces from the lane, a clean clone and a second cwd. The result is no-harm only: the base classifier passes identically, the fixtures contain none of the `nonlocal`, `global` or frame-introspection constructs I searched for, and the guard fails a classifier that reports nothing (negative control exit 1; 19/35 and 10/17). Operability hazards: lane-path runs write bytecode into the lane, and the lane tool is an uncommitted, moving file during the repair.
