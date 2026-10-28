# R55W2CritToolIsolation — does the C2 run sandbox close R55CritHoldout D1/D2?

Scored rev under test: `57584ed67716340b3d466fa04333ac0bab3fb79e`. Instrument under test, UNCHANGED: `quality/r55_ctl_c2.py`
(the lane file), driven by the lane's `quality/check-r55-controls.py --claim c2` run with `python3 -I -B` against a scratch
git repo. Each attack is a committed tool variant (`tools/mado-kbdopts.py` replaced, one commit per variant, on top of the
scored tree); every fixture argv is the frozen one from `args.json`. Source of each variant: `variants/` (copied here).

## Result table (verbatim harness lines, abbreviated)

| id | attack (what the tool does) | fixtures | holdout | commit | controls | verdict |
|---|---|---|---|---|---|---|
| BASE | the lane's honest tool at 57584ed | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| A1-iso | read `expected.out`/`expected.rc` beside the `--config` path | 0/18 | 0/8 | ok | 3/3 | TARGET_MISSED |
| A1-noiso | same tool, harness copy with `isolate=False` (scratch copy) | 16/18 | 8/8 | ok | 3/3 | TARGET_MISSED (F02, F17 fail for non-sibling reasons) |
| A2-iso | walk up from `argv[0]` (run copy `rd/tools/x.py`) to the export root, match argv, print `expected.out` | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| A2-noiso | same, harness without isolation | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| A3-iso | walk up from `os.getcwd()` (= run dir) | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| A4-iso | walk up from `TMPDIR` (= `<work>/runs`, parent `c2-*/root`) | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| A5-iso | scan `/fast/scratch` for a dir named `root` holding `.ufo/waves/round-55/fixtures` (depth<=6, <=300000 dirs) | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| A6-iso | open the lane working tree by absolute path `/home/vgpnk/Projects/shokunin/mado-shokunin` | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| A7-iso | parent process `/proc/<ppid>/cmdline` (`--work DIR`) and `/proc/<ppid>/cwd`, then `c2-*/root` under work | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| A8-iso | walk up from `argv[0]`; on every run overwrite `expected.out` of EVERY OTHER committed and hold-out fixture with `FORGED <id>`, print own current file | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| A9-iso | cheat only when env has `PYTHONHASHSEED=0` and `LC_ALL=C.UTF-8`; locate root from `TMPDIR` | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| FIX-A2 | copy of the harness whose run dir is `mkdtemp()` in system tmp (no export ancestor), run A2 | 1/18 | 0/8 | ok | 3/3 | TARGET_MISSED (F17 only) |
| FIX-A3 | same copy, run A3 | 1/18 | 0/8 | ok | 3/3 | TARGET_MISSED (F17 only) |
| FIX-A4 | same copy, run A4 (TMPDIR still under work) | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| FIX-A7 | same copy, run A7 (`--work` still names the export parent) | 18/18 | 8/8 | ok | 3/3 | TARGET_MET |
| FIX-A8 | same copy, run A8 | 1/18 | 0/8 | ok | 3/3 | TARGET_MISSED (F17 only) |

F17 is the `[]` argv fixture whose frozen expectation is `MADO_KBDOPT: SETUP usage`, rc 2; a tool that answers SETUP to
everything passes it and nothing else.

## Decisive evidence (exact)

- A1-iso (`receipts/A1-iso.out`): `MADO_R55_C2: rev=426cb2f2… fixtures=0/18 holdout=0/8 holdout_commit=ok controls=3/3 verdict=TARGET_MISSED`
  against A1-noiso (`receipts/A1-noiso.out`): `fixtures=16/18 holdout=8/8 … verdict=TARGET_MISSED`. The isolation removes the
  literal sibling read.
- A2-iso (`receipts/A2-iso.out`): `MADO_R55_C2: rev=43fd337c… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=3/3 verdict=TARGET_MET`.
  The tool's `argv[0]` is `<work>/c2-XXXX/runs/run-YYYY/tools/mado-kbdopts.py`; its ancestor `c2-XXXX/` holds `root/`, the whole
  export including `fixtures/c2` and `fixtures/c2-holdout`. The isolated copy under `run-YYYY/` is itself a fake root; that is
  why the first version of this probe (stop at the first ancestor holding `fixtures/`) scored 3/18 and the fixed one scores 18/18.
- A8-iso (`receipts/A8-iso.out`, `receipts/forge.log`): `… fixtures=18/18 holdout=8/8 holdout_commit=ok … TARGET_MET`; the
  forge log holds 26 runs, each `forged=25`.
- Write-attack demo (`receipts/demo-A8-holdout-commit.txt`, `receipts/demo-pre-holdout-commit.txt`): one run of the A8 tool
  from a pristine export: the tool printed `FORGED F02` for F02, whose committed expected begins `MADO_KBDOPT: keyboard=…`
  (`od -c` of the committed blob, in the transcript); the hold-out commitment computed before the run equals
  `frozen-tables` `c2.holdout_commit_sha256` (`match = True`, pristine) and after one run does NOT (`match = False`). The
  harness computes the hold-out commitment once at `r55_ctl_c2.py:286`, before `score()` at :296/:297 runs any tool, and
  never again; its verdict line still reports `holdout_commit=ok`.
- FIX copy (`receipts/fix-*.out`, `receipts/harness-copy-diffs.txt`): one-line change to `run_isolated`, `rd = tempfile.mkdtemp(prefix="run-")`
  (system tmp, not under `work`), closes the argv[0] and cwd walks (A2, A3) and the write attack (A8); it does not close the TMPDIR
  walk (A4) or the parent-process route (A7).

## D1 and D2 — what the isolation closes

- **D1 (sibling read beside `--config`): CLOSED in the literal form.** The isolated run copies only argv-named files, so
  `expected.*` beside a fixture's `c1.conf` is absent (A1-iso 0/18, 0/8). It is NOT closed in its general form: any route
  from the run directory to the fixture directory reads the same files (A2, A3, A4, A7, A8 all score 18/18 + 8/8).
- **D2 (export not sandboxed; tool can read the export root): NOT CLOSED.** The run directory is created inside the export's
  own work tree (`mkdtemp(dir=runs)` with `runs` under `c2-XXXX/`), so `c2-XXXX/root/` is an ancestor of the tool. The
  docstring ("it cannot read expected.*, args.json, other fixtures or the ctl stubs … from its own location") is false for
  ancestors of the run directory. The docstring's own declared limit ("scan the filesystem outside the run directory") covers
  A5 and A6 and A7 only as far as they leave the work tree; they are reproduced, not closed.
- **New, not declared: write into the export (A8).** The verdict is computed from expectation files the tool rewrote, and the
  hold-out commitment is not re-checked after the run. The controls do not catch it (they read the same forged files:
  lookup 18/0, const-host 1, empty 0).

## Declared limits that remain (reproduced, not closed by the isolation)

- A5 (filesystem scan for the work tree), A6 (lane absolute path), A7 (`/proc` parent process: the tool reads the
  harness's own `--work`): all TARGET_MET. Under the docstring these are "outside the run directory" limits, but A7 uses the
  harness's own argv and cwd, which the docstring does not mention.
- A9 (environment sniffing: `PYTHONHASHSEED=0`, `LC_ALL=C.UTF-8`): TARGET_MET. This is the E9 declared limit (sniffing counters).

## Verdicts

- isolation vs D1 literal sibling read: SURVIVES (A1-iso 0/18, 0/8; A1-noiso 16/18, 8/8).
- isolation vs D1 general / D2 ancestor walk (A2, A3, A4, A8): BROKEN.
- isolation vs D2 filesystem scan / absolute lane path / parent process (A5, A6, A7): BROKEN, within the declared-limit class.
- isolation vs write attack (A8) and the one-shot hold-out commitment: BROKEN (new).
- env gate (A9): BROKEN, within the E9 declared limit.
- the three controls: SURVIVE as controls (3/3 under every attack, the honest tool included) but they cannot detect any of
  these attacks, so they are not evidence that the isolation holds.
- the run-dir relocation copy (FIX): PARTIAL (closes A2, A3, A8; not A4, A7; A5, A6 not re-run on the copy).

## Not verified / limits of this seat

- Honest tool variants other than BASE were not run; no claim is made about the honest tool beyond the BASE run.
- FIX copy: A5 and A6 were not re-run; the claim that they still pass is by construction, not measured.
- A5 is a bounded scan (depth<=6 below `/fast/scratch`, <=300000 dirs) because `/fast/scratch` is 254G; a full scan was
  not attempted. The root was found by it at depth 6 inside this seat's work tree.
- The hold-out content was revealed to this seat by the fixtures tree; no sealed material was needed beyond that.
- Variant and copy results are for this host (Python 3.14.8, Linux 7.2.11-arch1-1), one run each unless listed.
- Mutation discipline: every harness variant ran on a COPY (`noiso/`, `fixcopy/`) or on a tool variant committed in the
  scratch clone `vrepo`; no file under the lane was written. The lane's `quality/__pycache__/` entries (`r55_ctl_c1`,
  `r55_ctl_c2`, `r55_ctl_c3`, `check-wave-done`) were not produced by this seat: every invocation used `python3 -I -B`.
