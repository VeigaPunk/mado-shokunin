# BaseCorpus: C1 no-harm baseline, corpus comparator with base on both sides

Seat: MadoR23.BaseCorpus (leaf, read-only on the lane). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base: commit `a28e4815aabfa85f55274884000fb2608355f8cf`; `tools/mado-tripwire.py` blob sha256
`cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`. The registration's base tip
`e33ea30461f6e9bbeee40beef19770a953f7a105` carries the same classifier bytes (checked with `git show | sha256sum`),
so the two base references do not conflict.

Raw receipts: `.ufo/waves/round-23/w1/out/BaseCorpus/`. Exact commands: `out/BaseCorpus/00-commands.log`.
Summary: `out/BaseCorpus/08-summary.json`.

## Verdict

Base-vs-base result: **0 removed and 0 added finding groups, 0 error flips** across 1356 files. Retained 1217 groups.
107 error pairs, identical on both sides. Each full comparator run took about 46 s. Three base-versus-base
runs (lane run 1, lane run 2, scratch cross-check) produced identical output. A positive control (a scratch
mutant) shows the comparator does detect a change, so the zero is not vacuous.

Operability verdict: **PARTIAL.** The comparator runs deterministically and fails closed on a mid-run tamper.
But the official entry point refuses any tool outside the lane tree (D1), its exit status is 1 at base so it
cannot gate (D2), and the worker's bytecode cache can write into the lane (D3) or execute stale code (D4).
Fixes and the decisions they need are below.

## Harness flags (checked first)

- `replay.py` (exit 0): `--tool TOOL`, `--mode {oracle,resource-api,resource-cli,corpus}`, `--before-tool` (required for corpus).
- `compare.py` (exit 0): `--before-tool`, `--after-tool`, `--worker` (internal; spawned per tool with a 600 s timeout).
- Harness hashes: `round-22/replay.py` 324e79861f4fe3f2a2b617786fae7652df861cfe09844e6609284ba2cdd3cfe4;
  `round-21/corpus/compare.py` 60cef7bebe6eef0bbf09448fec70f1b55375b5f511aad4c968dc22ee4036a653;
  `snapshot/manifest.json` 8e1cf206c85563b418630ef1d094559a9522431ff4e077ca1b51f249436a1377 (re-verified in every worker).

## Runs (sequential, one process at a time)

| Run | What | Exit | Result | Receipt (out/BaseCorpus/) |
|---|---|---|---|---|
| A | assignment command, scratch copy both sides | 2 | refused before any child: `ValueError: --tool must resolve inside the repository` | 01-replay-scratch-path.json |
| B | replay, lane path both sides (run 1) | 1 | files 1356, retained 1217, removed 0, added 0, error pairs 107, before≠after 0; harness wall 46.17 s; tool sha before and after cd9da20c | 02-replay-lane-run1.json |
| C | replay, lane path both sides (run 2) | 1 | comparator output identical to B (stdout sha256 4ae71da5db93cedc761565ddb872bdfeec17565758a02515032a6fa407857e30 both); 46.06 s | 04-replay-lane-run2.json |
| D | compare.py direct, scratch copy both sides (cross-check) | 1 | full output dict equal to B; 46.21 s wall | 03-compare-direct-scratch.json |
| E | positive control: base vs scratch mutant that drops each file's first finding | 1 | removed 634 (= base files with findings), added 0, retained 583, error pairs 107 unchanged; 46.14 s wall | 05-positive-control-mutant-direct.json |
| F | tamper: before-tool overwritten at t=8 s while the first worker runs | 1 | stdout empty; last stderr line `ValueError: selected tool changed during corpus run`; 23.18 s | 06-tamper-direct.stderr |
| G | bytecode and stale-cache probes (trivial module, scratch only) | n/a | see D3, D4 | 06-pyc-stale-probes.txt |

Base error population (107 pairs, identical on both sides):
83 `CouldNotEvaluate: unknown record shape`; 20 `RecursionError`; 1 `TimeoutError` (per-file 15 s deadline) on
`.ufo/waves/round-20/w2/AdvCrash/fixtures/huge_bash_cmd.jsonl` (2,000,199 bytes); 1 `CouldNotEvaluate: refused file name`;
1 `CouldNotEvaluate: invalid line (JSONDecodeError)`; 1 `CouldNotEvaluate: invalid line (ValueError)`.
Retained-plus-removed equals the base finding total (1217), so the comparator's accounting is consistent.

## Deviations from the assignment, and why

1. **Scratch path not usable with `replay.py` (D1).** For the official receipts I used the lane-path fallback the
   assignment names: lane `tools/mado-tripwire.py`, sha cd9da20c, byte-identical to base. I also ran the scratch copy
   through `compare.py` directly (run D), which produced identical output.
2. **Lane-path import can write bytecode (D3).** Before using the lane path I confirmed the lane's cached
   `tools/__pycache__/mado-tripwire.cpython-314.pyc` was current: its header magic matches
   `importlib.util.MAGIC_NUMBER`, and its recorded mtime (1792600104) and size (162432) equal the source's. So the import was a
   cache hit. Each lane-touching run was bracketed by sha256 and cache-listing snapshots; every diff exited 0
   (`02-`, `03-`, `04-`, `05-` state files).
3. **Positive control and tamper test ran through `compare.py` directly on scratch files**, so the lane was never involved.

## Harness defects (severity order)

**D1. The official entry point refuses any tool outside the lane tree. Blocking for the after-measurement workflow.**
Evidence: run A, exit 2, `setup_error` "--tool must resolve inside the repository". Cause: `replay.py`
`selected_file` (lines 39–45) requires `path.is_relative_to(REPO_ROOT)`, where `REPO_ROOT` is derived from
replay.py's own location. Consequences:
- A base copy outside the lane cannot be measured through `replay.py`.
- Executor candidates in `/fast/scratch` clones cannot be measured through `replay.py` at all. `compare.py` has no such check, so it still works (run D).
- After `tools/mado-tripwire.py` changes, no in-repo base exists. `git ls-files` matching `mado-tripwire` returns only `tools/mado-tripwire.py`, so `--before-tool <base>` has nothing to point at.
Fix options (not implemented; L1 decides): commit a base snapshot inside the repo but outside `tools/` (the C3 counter reads only tracked `tools/*.py|*.sh`, so it is unaffected), recording its sha256; or let `replay.py` accept an explicit read-only path.

**D2. The exit status cannot serve as the no-harm gate.**
`compare.py` line 114 returns `int(bool(errors))`, and `errors` lists every pair where either side errored, including
identical ones. Base versus base therefore exits 1 with 107 pairs (runs B–E). The replay receipt inherits that exit
code, so a `$?`-based gate fails the baseline. The meaningful gate is before≠after error pairs (0 at base), plus removed and
added group counts (0 and 0 at base).
Fix: exit nonzero only for before≠after pairs, or rename the field and report flips separately.

**D3. The worker can write bytecode into the lane tree.**
`compare.py` spawns the worker as `python3 -I` without `-B`. Probe A (`06-pyc-stale-probes.txt`): a module loaded by path under `-I` creates
`__pycache__`; probe B (`-I -B`) does not. The lane's cache is current, so none of my lane-path runs wrote anything. But the first
lane-path measurement after any edit to `tools/mado-tripwire.py` will write `tools/__pycache__/mado-tripwire.cpython-314.pyc`. The
directory is gitignored (`__pycache__/`), but it is still a write into the lane. `-B` alone is not a complete fix (D4).

**D4. Stale bytecode can execute old code while the harness reports the new hash.**
`compare.py` hashes the source bytes (`sha()`), then loads the tool through CPython's bytecode cache. The cache validates only on
source mtime (whole seconds) and size. Probe C: a source edited to a same-size value with its mtime restored still runs the old
code under `-I` (C2 prints `1`; the source says `2`). `-I -B` also prints `1` (C3), because `-B` only blocks writes and a valid
cache is still read. Compiling from the already-hashed bytes prints `2` (C4).
Fix: in the worker, `compile()` the bytes that were hashed, into a fresh namespace. That also closes the gap between the hash check and the load.
Likelihood is low in ordinary editing, but the failure is silent. The probe used a trivial module, not the classifier file; the
loader mechanism is the same.

**D5. One timing-dependent error pair in the base.**
`.ufo/waves/round-20/w2/AdvCrash/fixtures/huge_bash_cmd.jsonl` hits the 15 s per-file deadline in all four comparator runs (B, C, D, E).
A candidate whose runtime on this file changes will flip that pair (before≠after) with no finding change, and the comparator will report
it as an error flip. The file's full duration is not measured, because measuring it would exceed the 15 s cap. Host load during the runs:
loadavg 5.31 / 7.30 / 6.88 on 32 CPUs.
Decision for L1: pre-register how deadline-only flips are adjudicated, or obtain a duration measurement through a separately sanctioned run.

**Minor and informational**
- m1. 20 `RecursionError` rows at base: a classifier crash path reported as error pairs. Identical at base, so any candidate that changes recursion behavior will flip them.
- m2. Replay receipts record `tool_sha256` and `tool_sha256_after` but do not assert equality. The comparator does assert within itself, and the tamper test (F) fails closed. Both values equal cd9da20c in B and C.
- m3. The field name `errors` is misleading: it lists identical pairs as well as flips.
- m4. The comparator parses worker stdout line by line with `json.loads` (line 79), so any stray print from a tool aborts the run. Not exercised. At base, `scan_file` contains no print calls (grep of the classifier; prints appear only in `emit`, `run_scan`, `selftest`, and `main`).

## Lane integrity

No lane file was written by me. Evidence:
- Lane state (sha256 of `tools/mado-tripwire.py` and the `.pyc`, plus `ls --full-time` of `tools/__pycache__`) was captured before and after every lane-touching run. All diffs exited 0 (`02-`, `03-`, `04-`, `05-` state files).
- `09-lane-final-state.txt` equals the first pre-run snapshot (`02-lane-pre-state.txt`), so nothing changed during the session.
- `git status --short -- tools/ .ufo/waves/round-23/w1` shows only `?? .ufo/waves/round-23/w1/`, the wave's untracked directory, which holds my out files and this report.
- Scratch-only artifacts live in `/fast/scratch/hyaku/mado-r23/BaseCorpus/`: `base-tool.py`, `mutant-drop-first.py` (control), `tamper-tool.py`, probe directories, and `__pycache__` files created by `python3 -I` runs in scratch.

Installs and updates: none. No pacman, no network, no package change. Python used: `/usr/bin/python3` 3.14.8.

## Residual risk and verification gaps

- One host, one window, loadavg about 5–7 on 32 CPUs. The deadline pair (D5) may behave differently under other load.
- Positive control tests removal detection only. Addition uses the same comparison code path but was not separately exercised.
- The worker's 600 s subprocess timeout and spawn-error paths were not exercised.
- D4 was demonstrated on a trivial module, not on the classifier file.
- Not run here (outside this item): oracle, resource, and precision harnesses; no candidate tree was measured.

## Recommendations for L1 (decisions, not implemented here)

1. Put a base snapshot inside the repo, outside `tools/`, before the landing commit, and point `--before-tool` at it (D1).
2. Gate on before≠after error pairs = 0, removed = 0 (or adjudicated), added = 0 (or adjudicated). Do not gate on exit status (D2).
3. Make the worker compile from the hashed bytes; keep `-B` as belt and braces (D3, D4).
4. Pre-register deadline-only flip handling for `huge_bash_cmd.jsonl` (D5).
5. Expected base-vs-base baseline for the after-measurement: removed 0, added 0, retained 1217, error pairs 107, error flips 0, exit 1. Compare candidate runs against these numbers.

Verdict: **PARTIAL (operability).** Base-vs-base corpus measurement is deterministic and non-vacuous: 0 removed, 0 added, 0 error flips, 107 identical error pairs, about 46 s, and tamper fails closed. But the official entry refuses out-of-lane tools (D1), the exit status cannot gate (D2), and the worker's bytecode cache can write into the lane (D3) or run stale code (D4).
