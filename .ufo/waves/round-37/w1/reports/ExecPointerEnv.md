# ExecPointerEnv — report (mado round 37 wave 1)

Seat: L1Mado37-2.ExecPointerEnv. Assignment: `…/w1/prompts/ExecPointerEnv.md`.
All runs at `cd /home/vgpnk/Projects/shokunin/mado-shokunin` (lane head `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`, git 2.56.0).
Transcripts: `.ufo/waves/round-37/w1/scratch/ExecPointerEnv/red-green.txt` (red/green + sweep + decoy + residual).
Cleanup: `/dev/shm/mado37-ExecPointerEnv` removed; scratch retained. No tool installs performed.

## (1) Red-before — PASS (proven)
`python3 -I quality/check-evidence-pointers.py --rev a5aaa09ad38bfd90c13d76ccf371e36c45a2697e`:

| env | verdict (summarized) | rc |
|---|---|---|
| plain | `PRED-PTR-r36-v1 rev=a5aaa09… pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=35 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET` | 0 |
| `GIT_DIR=/home/vgpnk/Projects/shokunin/.git` | `PRED-PTR-r36-v1 error=revision-not-readable:a5aaa09…` | 2 |
| `GIT_WORK_TREE=/dev/shm` | `… inherited_dirty=8 … verdict=TARGET_MISSED` (8 paths `D`) | 1 |

Quoted from red-green.txt (`=== RED …` blocks). The defect reproduces.

## (2) Fixed copy — PASS (three runs agree; only delta is GIT_* stripping)
Fixed copy: `scratch/ExecPointerEnv/check-evidence-pointers.py`. Delta vs original (diff in transcript):
`+import os`, `+GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}`, and `env=GIT_ENV` added to all three git subprocess sites:
`git()` `:75-79`, the `status --porcelain` rc probe `:171-175`, and `merge-base --is-ancestor` `:203-207` (original line numbers; the only edits).

Same three runs with the fixed copy: all print the plain verdict (`verdict=TARGET_MET` rc=0); the `GIT_DIR`+`GIT_WORK_TREE` combination also rc=0.

Able-to-fail (the gate can still go red): at `4243d031e3441f5063f92c33aa58377c6f9ff120` (round-35 spot-check, pre-round-36 sections) both scripts plain print `setup=missing-r36-sections … verdict=TARGET_MISSED` rc=1; under `GIT_DIR` the original rc=2, the fixed copy rc=1 — i.e. fixed copy agrees with plain instead of erroring.

## (3) Sweep — LANE/quality/*.py, LANE/tools/*.py, mado-verify.sh

Verdict legend: AFFECTED = ambient GIT_DIR changes output; LEAK = some GIT_* residual changes output; CLEAN = unaffected. Every run compared plain vs `GIT_DIR=/home/vgpnk/Projects/shokunin/.git` (plus extra vars where the script partially strips); `GIT_OPTIONAL_LOCKS=0` throughout.

| file:line | git child calls | result |
|---|---|---|
| `quality/check-evidence-pointers.py` `:75-79,:171-175,:203-207` | all 3 inherit env | AFFECTED (fixed in (2)) |
| `quality/check-axis-scores.py` `:97-98` git(), `:118-119` spawns child instruments | inherit env (children also inherit) | AFFECTED — plain `MADO_AXIS: checked=3 mismatched=0 rev=80b83c85…` rc=0; GIT_DIR `MADO_AXIS: checked=3 mismatched=3 rev=a409e65d…` rc=1 (the gate then measures the FLEET head) |
| `quality/check-index.py` `:48-52` `_git` | inherit env | AFFECTED — plain `MADO_INDEX: rev=master indexed=50/50 … coverage=10.0000/10` rc=0; GIT_DIR `SETUP_ERROR: fatal: Not a valid object name a409e65d…:corpus/knowledge` rc=2 |
| `quality/check-index-rows.py` `:55-59` `_git` | inherit env | AFFECTED — plain `MADO_INDEX_ROWS: rev=master rows=50 errors=0 warns=3` rc=0; GIT_DIR `SETUP_ERROR: fatal: path 'corpus/README.md' exists on disk, but not in 'a409e65d…'` rc=2 |
| `quality/check-control-receipts.py` `:60-65` git() | pops only GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE | LEAK — GIT_DIR: IDENTICAL rc=1 (guard works); `GIT_COMMON_DIR` and `GIT_OBJECT_DIRECTORY` each: `UNEVALUABLE bad tip 2fdca5ca` rc=2 vs plain rc=1 |
| `quality/counter-selftest.py` `:480-481` (pops 3), loads counters in-process | round-26 counters call git in-process: `.ufo/waves/round-26/c1/count-v2.py:280,294`, `c2/count.py:128,142` | LEAK — GIT_DIR: pass=59/59 rc=0 (diff is only random mkdtemp scratch names, checked); `GIT_OBJECT_DIRECTORY` / `GIT_COMMON_DIR` residual probe: `SELFTEST pass=1 total=59` rc=1 |
| `quality/check-counter-discrimination.py` `:122-124` | full strip, then sets `GIT_DIR` to repo | CLEAN — plain/GIT_DIR/GIT_COMMON_DIR all IDENTICAL rc=0 `MADO_DISCRIMINATION: profile=r36 … correct=25/25 verdict=TARGET_MET` |
| `quality/population-suite.py` `:346` (env PATH/HOME/TMPDIR) | spawns only the checker, no git | CLEAN (no git subprocess exists) |
| `tools/mado-action-plan.py` `:525` | minimal `{PATH}` env | CLEAN (GIT_* cannot be inherited) |
| `tools/mado-assessment.py` `:194-195` | spawns itself (`-I … --root --check`) | CLEAN (no git child; env inherited but harmless) |
| `tools/mado-evidence-audit.py` `:244-245` | spawns itself (`-I … --check`) | CLEAN (same) |
| `tools/mado-verify.sh` live arm `:3773,3813,3823,3827,3829,3830,3848,3858,3886` | real `tmo git -C "$tree" …` (symbolic-ref, for-each-ref, rev-parse, describe, show), no GIT_* scrubbing | AFFECTED — plain omarchy rows all PASS `HELD: v3.8.4 exactly at refs/heads/master`, `HELD: 8fcc9d60…`, `worktree == HEAD blob`; GIT_DIR: tag `UNKNOWN git describe failed (rc=128)`, head `FAIL MOVED: HEAD → 'a409e65d…' != pin 8fcc9d60…`, vs_head `UNKNOWN cannot read HEAD:… (rc=128)`; `GIT_WORK_TREE=/dev/shm`: IDENTICAL to plain (read verbs don't consult the worktree). Non-omarchy diff = 3 lines, exactly the counts/MADO_VERIFY summary carrying the divergence |
| `tools/mado-tripwire.py`, `mado-binds.py`, `mado-wsrules.py` | static analyzers; no git subprocess | not applicable (no git child processes) |

### Extra finding (same defect class, write-side)
`check-index.py` `:278-288` and `check-index-rows.py` `:401-411` `--selftest` fixtures run `git init/add/commit` with `env=dict(os.environ, …)` — the three popped variables are NOT stripped there. Decoy proof (decoy.txt): with `GIT_DIR=<decoy>/.git` each selftest still reports `12/12` / `10/10` PASS while the decoy repo gains a commit and 3 index entries (commit count 1→2; index entries 0→3). Under an ambient GIT_DIR these selftests silently WRITE into the named repo — reported as a static finding; no fleet/lane repo was touched.

## Hygiene
- Lane `.git/index` sha256 stayed `53c85c246d68cc3f3fed7a9e0b4a6c0e49824a7f341652aaf81f1c1c6983b9db` across every run (recorded before/after in red-green.txt; lane git/gg state untouched).
- The fleet `.git/index` sha changed between runs (`9e443386…` → `50af9f37…`) from sibling concurrency; my runs used read verbs only (`ls-tree/show/rev-parse/status` — status runs had `GIT_OPTIONAL_LOCKS=0`) and never wrote it.
- Tools: `sed`/`grep` used for ranged reads (the harness Read tool failed on small-file ranges; no report_issue device mounted).
- Privacy: report quotes verdict lines and digests only; full outputs live in `sweep-out/` and `red-green.txt`.

## Verdicts
- (1) red-before: **PASS** — three distinct outcomes quoted.
- (2) fixed copy + green: **PASS** — three runs agree; able-to-fail at 4243d03 demonstrated.
- (3) sweep: **PASS** — defect class confirmed at `check-axis-scores.py:97-98`, `check-index.py:48-52`, `check-index-rows.py:55-59`, `mado-verify.sh:3773-3886`; residual GIT_* leaks at `check-control-receipts.py:60-65` and `counter-selftest.py:480-481` (via in-process counters); selftest fixture-write hazard at `check-index.py:278-288` / `check-index-rows.py:401-411`; `check-counter-discrimination.py:122-124` and `population-suite.py:346` are clean; tools/*.py other than mado-verify.sh have no git children.
- No blockers; nothing left reachable. Main-agent checks to run: review `red-green.txt` (225 lines, sha `8f295674c361f80d02ce37ca4489ef6fac38bf767282ee04bc585eb14dde86d8`), apply the same GIT_ENV pattern to the four AFFECTED files noted above (out of my write scope).
