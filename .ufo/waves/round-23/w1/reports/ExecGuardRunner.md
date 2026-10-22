# ExecGuardRunner — round-23 no-harm guard battery (C1 operability)

Seat: `MadoR23.ExecGuardRunner` (leaf executor). Scope: write one stdlib-only guard battery
script that runs the seven registered no-harm guards sequentially, one child at a time, and
reports exact argv / exit code / pass-total counts per guard; run it once against the base
classifier and save the receipt. No production file was edited.

## Files written (all inside my seat's out dir plus this report)

| Path | What |
|---|---|
| `.ufo/waves/round-23/w1/out/ExecGuardRunner/guards.py` | the guard battery (stdlib only, 33 507 bytes) |
| `.ufo/waves/round-23/w1/out/ExecGuardRunner/base-tool.py` | base classifier, `git show a28e4815aabfa85f55274884000fb2608355f8cf:tools/mado-tripwire.py` |
| `.ufo/waves/round-23/w1/out/ExecGuardRunner/base-guards.json` | **the required receipt** (base vs base) |
| `.ufo/waves/round-23/w1/out/ExecGuardRunner/base-guards-precision.json` | same run plus the precision guard (base revision reference) |
| `.ufo/waves/round-23/w1/out/ExecGuardRunner/clone-lane-guards.json` | same battery driven with `--lane <executor clone>` |
| `.ufo/waves/round-23/w1/out/ExecGuardRunner/logs/` | per-guard stdout/stderr/argv (raw evidence) |
| `.ufo/waves/round-23/w1/out/ExecGuardRunner/candidate.patch` | empty by design: this seat changed no `tools/` file |
| `.ufo/waves/round-23/w1/reports/ExecGuardRunner.md` | this report |

SHA256 of the final artifacts: `guards.py`
`4c4524404580317539e921c40a6601d9deab5c81e6bd766ddd479aa74b73256f`;
`base-guards.json` `5a755003849c1aee54efe96ebb6e206120b2d596ed12b6cae9cafcf4b847ed10`;
`base-tool.py` = `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` (equals the
registered base classifier digest).

## Exact commands

```bash
# base classifier extract (as instructed)
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show \
    a28e4815aabfa85f55274884000fb2608355f8cf:tools/mado-tripwire.py \
    > /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w1/out/ExecGuardRunner/base-tool.py

# the required run: tool and base-tool are both the base classifier
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-23/w1/out/ExecGuardRunner/guards.py \
    --tool   .ufo/waves/round-23/w1/out/ExecGuardRunner/base-tool.py \
    --base-tool .ufo/waves/round-23/w1/out/ExecGuardRunner/base-tool.py \
    > .ufo/waves/round-23/w1/out/ExecGuardRunner/base-guards.json
# exit 1 (guard failure, not a harness error): the base classifier is red on the repair set,
# which is exactly the registered "before" value 6/12.

# precision path (needs a commit): my clone carries an empty commit over the base bytes
python3 -I .ufo/waves/round-23/w1/out/ExecGuardRunner/guards.py \
    --tool …/base-tool.py --base-tool …/base-tool.py \
    --precision-rev 91ead70b63f3cab3291f68a22cd32ed9db04888e \
    --precision-repo /fast/scratch/hyaku/mado-r23/ExecGuardRunner/clone \
    > …/base-guards-precision.json

# L1 request: drive the battery from an executor clone instead of the production lane
python3 -I .ufo/waves/round-23/w1/out/ExecGuardRunner/guards.py \
    --lane /fast/scratch/hyaku/mado-r23/ExecGuardRunner/clone \
    --tool   /fast/scratch/hyaku/mado-r23/ExecGuardRunner/clone/tools/mado-tripwire.py \
    --base-tool /fast/scratch/hyaku/mado-r23/ExecGuardRunner/clone/tools/mado-tripwire.py \
    > …/clone-lane-guards.json
```

Clone used for the precision reference: `/fast/scratch/hyaku/mado-r23/ExecGuardRunner/clone`
(branch `r23/guard-runner`, commit `91ead70b63f3cab3291f68a22cd32ed9db04888e`, an empty commit
over the base bytes; `tools/mado-tripwire.py` digest unchanged). Nothing was pushed.

## Guard results at the base classifier (receipt `base-guards.json`)

Overall: `{"exit": 1, "verdict": "guard-failure"}` — 8 guards pass, 2 guards fail, 0 harness
errors. The two failures are the registered round-23 red (repair 6/12, residual 2/4), i.e. the
"before" values this round exists to repair.

| # | Guard id | Exact argv | Exit | Pass/total | Verdict |
|---|---|---|---|---|---|
| 1 | `repair-12` | `python3 -I <lane>/.ufo/waves/round-23/repair/measure.py --tool <TOOL>` | 1 | **6 / 12** | fail (registered before value; target 12/12) |
| 2 | `residual-truth` | `python3 -I <lane>/.ufo/waves/round-22/residual-truth/measure.py --tool <TOOL>` | 1 | **2 / 4** | fail (registered H3 before value) |
| 3 | `r22-oracle-57` | `python3 -I <lane>/.ufo/waves/round-22/oracle/measure.py --tool <TOOL>` | 0 | 57 / 57 | pass |
| 4 | `r21-oracle-replay` | `python3 -I <lane>/.ufo/waves/round-22/replay.py --tool <TOOL> --mode oracle` | 0 | 52 / 52 (primary 35/35 + supplemental 17/17) | pass |
| 5 | `legacy-selftests` | `prlimit --as=402653184 --cpu=15 python3 -I <TOOL> --selftest <suite dir>` (11 children) | 0 | 247 / 247 | pass |
| 6 | `corpus-comparator` | `python3 -I <lane>/.ufo/waves/round-22/replay.py --tool <TOOL> --mode corpus --before-tool <BASE>` | 1 (comparator: 107 pre-existing shared errors) | 0 added / 0 removed / 0 flips | pass |
| 7 | `resource-closure-module-main` | `python3 -I <lane>/.ufo/waves/round-22/resource-closure-measure.py --tool <TOOL> --mode module-main` | 0 | 3 / 3 | pass |
| 7 | `resource-closure-cli` | same harness `--mode cli` | 0 | 3 / 3 | pass |
| 7 | `resource-r21-module-main` | `python3 -I <lane>/.ufo/waves/round-21/resource/measure.py --tool <TOOL> --mode module-main` | 0 | 3 / 3 | pass |
| 7 | `resource-r21-cli` | same harness `--mode cli` | 0 | 3 / 3 | pass |

Guard 5 child suites (all `prlimit --as=402653184 --cpu=15 python3 -I <TOOL> --selftest DIR`,
parsed from `SELFTEST_SUMMARY: N/M passed failed=[]`):
`round-17/tripwire/core` 9/9, `round-17/tripwire/compound` 16/16, `round-17/tripwire/hardening`
33/33, `round-17/tripwire/w2-regressions` 30/30, `round-18/tripwire/r18-failsafe` 1/1,
`round-18/tripwire/frozen` 31/31, `round-19/tripwire/r19-bashcvar` 45/45,
`round-19/tripwire/r19-helperfn` 34/34, `round-19/tripwire/r19-vcs` 17/17,
`round-19/tripwire/r19-frozen-f1f2` 13/13, `round-19/tripwire/r19-installers` 18/18 —
sum 247/247, every child exit 0. (Per-suite numbers are recomputed from the receipt
`detail.suites[]`; the eleven suite names come from
`.ufo/waves/round-22/evidence/resume/legacy-selftests-summary.json` and each name maps to
`<lane>/.ufo/waves/<suite>/expected.json`, the `--selftest DIR` contract of the classifier.)

Guard 6 detail at base-vs-base over the 1356-file corpus: 0 added groups, 0 removed groups,
0 error flips, 107 shared errors (identical before and after strings — 85 malformed-JSON
`CouldNotEvaluate`, 20 `RecursionError`, 1 refused file name, 1 per-file 15 s deadline). The
comparator's own exit is 1 because it reports *any* error row; the battery judges the guard on
added/removed/flip counts, not on that exit. 1217 findings retained.

### Per-file unparsed counter changes (L1 request)

The comparator keeps both scans (`runs.before` / `runs.after`); the battery now diffs the
per-file counters `eval_unparsed` and `unparsed_spawns` for all 1356 files and reports
`path` + before/after for every file whose counters differ, in
`detail.unparsed_counter_changes` (split into `unparsed_counters_reduced` and
`unparsed_counters_increased`). A **reduction** is reported and does not fail the guard (the
round-22 replay recorded eight reduced counters as an acceptable change); an **increase or a
mixed change** fails the guard, because the scanner would be parsing less than the base.
At base-vs-base: 1356 files compared, 0 changed, 0 reduced, 0 increased.

### Precision (L1 request: compare against the base revision)

`--precision-rev <commit> --precision-repo <dir>` runs
`python3 -I <repo>/.ufo/waves/round-20/tw-precision.py <rev>` from that repository and then runs
the same counter on the base revision `a28e4815aabfa85f55274884000fb2608355f8cf`, comparing the
two passing-name sets.

Measured on the base bytes (`base-guards-precision.json`):

- base revision: **166 / 175** (families P 66/66, S 17/17, W 21/22, H 47/52, L 15/18)
- candidate commit: **166 / 175**, `identical_passing_set: true`,
  `tool_sha256_matches_candidate: true`, `reasons: []`
- `only_in_candidate: []`, `only_in_base: []`

The guard fails when the passing set differs from the base revision, when the commit's
`tools/mado-tripwire.py` bytes differ from the `--tool` bytes, or when the counter itself
errors (exit 2 → fail closed).

## `--lane` support (L1 request)

`replay.py` and the round-22 resource driver both refuse a scanner that does not resolve
inside *their own* repository, so a candidate that lives in an executor clone needs the
harnesses to come from that clone too. `guards.py` therefore takes `--lane DIR` (alias
`--lane-root`, default the production lane) and resolves **every** harness path
(`repair/measure.py`, `residual-truth/measure.py`, `round-22/oracle/measure.py`,
`round-22/replay.py`, `round-21/resource/measure.py`, `round-21/corpus/compare.py` via replay,
`round-22/resource-closure-measure.py`, `round-20/tw-precision.py`, the legacy selftest
summary and the eleven suite directories) inside that tree, and runs every child with
`cwd = <lane>`. A scanner that is already inside the lane is used in place; a scanner outside
it is copied into `<lane>/.ufo/waves/round-23/w1/out/ExecGuardRunner/` (never anywhere else)
so the replay/resource drivers accept it.

Verified: the clone-lane run (`clone-lane-guards.json`) reproduces the production-lane numbers
exactly — repair 6/12, residual 2/4, oracle 57/57, replay 52/52, selftests 247/247, corpus
0/0/0 with 1356 files compared, resource 3/3 in all four modes.

## Safety properties

- **Writes only inside the out dir.** The script creates at most: its own out dir, the
  `logs/` subdir, and (only when the scanner is outside the lane) a staged copy inside the
  lane's `…/w1/out/ExecGuardRunner/`. Nothing else is created, edited or removed. The raw
  evidence is written to `logs/<guard>.stdout.txt`, `logs/<guard>.stderr.txt`,
  `logs/<guard>.argv.json`.
- **Fail closed.** Any harness error (spawn failure, wall-clock timeout, unparsable stdout,
  missing harness, setup error inside a replay receipt) sets `harness_error` and forces the
  overall exit to **2**. A plain guard failure is exit **1**; all guards passing is exit **0**.
  Verified:
  - `--lane /tmp` → `{"harness_error": "lane root is not the mado lane: /tmp"}`, exit 2.
  - `--tool /tmp/nope.py` → `{"harness_error": "cannot stage tools: [Errno 2] …"}`, exit 2.
  - a fake lane whose repair harness prints non-JSON → mid-run stop, exit 2,
    `summary.harness_error = "repair-12: stdout is not JSON …"`.
- **One child at a time.** Guards run strictly sequentially; each harness keeps its own
  one-child-at-a-time design (384 MiB / 15 s caps are the harness's, untouched).
- No `jj` command was run; no git write was performed in the lane (read-only `git show`,
  `ls-files`, `status`, `rev-parse`, `log`). The lane working copy is unchanged apart from
  my untracked out dir and this report. `git status --porcelain` shows only
  `.ufo/waves/round-23/w1*` (my seat's files inside the wave dir).
- Side effect to be aware of: the harnesses import the scanner with `importlib`, which writes
  `__pycache__/mado-tripwire.cpython-314.pyc` next to the scanned file. In the production lane
  that lands in `tools/__pycache__/` (already covered by the repo's `__pycache__/` ignore
  rule); in a clone it lands in the clone. No tracked file is affected.

## Tooling

No package was installed or upgraded; the battery uses only the Python 3 standard library
(`python3 -I`, interpreter `/usr/bin/python3.14`) plus `prlimit` (util-linux, already present)
and `git` (already present).

## Risks / open items

1. **Guard 6 is strict.** The battery fails the corpus guard on *any* added or removed finding
   group and on *any* unparsed-counter increase. The registration asks for every such group to
   be "adjudicated" by a human; the machine verdict here is "not identical to base". The lists
   are in the receipt so the L1 can adjudicate group by group.
2. **Guard 7 is a measurement, not a score.** The round-22 closure harness states
   "Descriptive measurements only; this artifact does not score detector correctness". The
   battery therefore judges each case on the harness's own `expected` block (exit, finding
   count, unparsed totals, no timeout, no spawn error, ≤ 15 s) and reports `wait4_ru_maxrss_kib`
   per case; it does not invent a memory ceiling of its own.
3. The aggregate `legacy-selftests` guard has no single argv; the receipt carries all eleven
   child commands in `detail.child_argv` (and `detail.suites[].argv`).
4. `base-guards.json` was produced with the *base* classifier as both `--tool` and
   `--base-tool`, so guards 1 and 2 are expected to be red (6/12, 2/4). The receipt is a
   "before" measurement, not a failure of the battery.
5. The precision guard needs a commit; with `--precision-rev` alone the battery cannot
   evaluate precision and reports nothing for it (the flag is optional by design).

## Verdict

**Delivered and exercised.** The battery exists, runs the seven no-harm guards sequentially
with exact argv/exit/counts per guard, reports the corpus added/removed finding groups, the
error flips and the per-file unparsed-counter changes, compares precision against the base
revision `a28e4815…`, accepts `--lane <clone>`, writes only inside its out dir, and fails
closed with exit 2 on any harness error. Measured on the base classifier: repair 6/12 (red as
registered), residual 2/4 (red as registered), round-22 oracle 57/57, round-21 oracle
35/35 + 17/17, selftests 247/247, corpus 0 added / 0 removed / 0 flips over 1356 files with
0 unparsed-counter changes, and the four resource populations 3/3 clean under 384 MiB / 15 s;
precision 166/175 with the identical passing-name set.
