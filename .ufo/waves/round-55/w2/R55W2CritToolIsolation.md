# R55W2CritToolIsolation — report (wave w2, falsify; C2 harness isolation)

Deliverable: `.ufo/waves/round-55/w2/R55W2CritToolIsolation/isolation.md` (full table and evidence). Receipts:
`.ufo/waves/round-55/w2/R55W2CritToolIsolation/receipts/`; attack variants: `.../variants/` (A1–A9 and lookup notes).

## Attacked

Target: `quality/r55_ctl_c2.py` at `57584ed67716340b3d466fa04333ac0bab3fb79e`, specifically `run_isolated` (lines 182–203)
and the hold-out commitment check (lines 276–286). Questions: which of R55CritHoldout D1/D2 the isolation closes.

## What ran (commands, decisive output)

1. Scratch base repo: `git -C "$D" init -q`, `git -C "$D" fetch -q --no-tags /home/vgpnk/Projects/shokunin/mado-shokunin 57584ed…`
   (read of the lane; `git -C <lane> rev-parse HEAD` → `721ba9c1…`, not the scored rev; `git -C <lane> status --short` and
   `git -C <lane> log` were read at the start, `status` may refresh the lane's index stat cache; no lane file was written).
2. Baseline: `python3 -I -B /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-r55-controls.py --claim c2 --repo $D --rev 57584ed… --work $W/work-base`
   → `MADO_R55_C2: rev=57584ed… fixtures=18/18 holdout=8/8 holdout_commit=ok controls=3/3 verdict=TARGET_MET`, exit 0.
3. Variants: scratch clone `vrepo` of the base repo; per variant `git -C vrepo checkout -q --detach 57584ed…`, replace
   `tools/mado-kbdopts.py`, `git -C vrepo add`, `git -c user.name=ctl -c user.email=ctl@ctl commit`; then the lane's checker
   on `--repo vrepo --rev <variant sha>`. Toplevel asserted before the first commit (`git -C vrepo rev-parse --show-toplevel`).
4. Mutated harness copies (scratch only, never the lane): `noiso/quality/` (`isolate=False` on the two `score(...)` calls, lines
   296–297) and `fixcopy/quality/` (run dir `mkdtemp(prefix="run-")` in system tmp, line 188). Both run through their own copy of
   `check-r55-controls.py`.
5. Demo: one run of the A8 tool from a pristine export; committed F02 `expected.out` vs printed output; the hold-out
   commitment computed by importing the lane's `holdout_commitment` read-only (`python3 -I -B`, `sys.path` pointing at the lane
   quality dir; `-B` writes no bytecode) before and after the run.

## Results (fixtures / holdout / controls / verdict)

| variant | route | fixtures | holdout | controls | verdict |
|---|---|---|---|---|---|
| BASE | honest tool | 18/18 | 8/8 | 3/3 | TARGET_MET |
| A1-iso | beside `--config` | 0/18 | 0/8 | 3/3 | TARGET_MISSED |
| A1-noiso (copy) | beside `--config` | 16/18 | 8/8 | 3/3 | TARGET_MISSED |
| A2-iso | walk up from argv[0] | 18/18 | 8/8 | 3/3 | TARGET_MET |
| A2-noiso (copy) | walk up from argv[0] | 18/18 | 8/8 | 3/3 | TARGET_MET |
| A3-iso | walk up from cwd | 18/18 | 8/8 | 3/3 | TARGET_MET |
| A4-iso | TMPDIR env | 18/18 | 8/8 | 3/3 | TARGET_MET |
| A5-iso | scan /fast/scratch (bounded) | 18/18 | 8/8 | 3/3 | TARGET_MET |
| A6-iso | lane absolute path | 18/18 | 8/8 | 3/3 | TARGET_MET |
| A7-iso | parent /proc cmdline + cwd | 18/18 | 8/8 | 3/3 | TARGET_MET |
| A8-iso | walk up + forge others' expected.* | 18/18 | 8/8 | 3/3 | TARGET_MET (holdout_commit=ok) |
| A9-iso | env gate PYTHONHASHSEED/LC_ALL | 18/18 | 8/8 | 3/3 | TARGET_MET |
| FIX-A2/A3/A8 (copy) | run dir outside export ancestry | 1/18 | 0/8 | 3/3 | TARGET_MISSED (F17 only) |
| FIX-A4/A7 (copy) | TMPDIR / --work still inside | 18/18 | 8/8 | 3/3 | TARGET_MET |

## Verdicts

- **D1 literal (sibling `expected.*` beside `--config`): SURVIVES.** The isolation closes it (A1-iso 0/18, 0/8 vs A1-noiso 16/18, 8/8).
- **D1 general and D2 ancestor walk (A2, A3, A4, A8): BROKEN.** The run directory is inside the export's work tree; the export
  root is an ancestor of the tool. The docstring claim "cannot read … from its own location" is false.
- **D2 filesystem scan, absolute path, parent process (A5, A6, A7): BROKEN, within the declared-limit text** ("outside the run
  directory"), except A7 which reads the harness's own `--work` and cwd.
- **Write into export (A8) and one-shot hold-out commitment: BROKEN, new.** Expectation files are read lazily and rewritten by
  the tool; the commitment is checked once at line 286, before any tool runs. Demo: pristine match `True`, after one run `False`;
  the tool printed `FORGED F02` for F02. The harness still reports `holdout_commit=ok`.
- **Env sniffing (A9): BROKEN, within E9 declared limit.**
- **Controls (3/3 under every attack): cannot detect any of the above.** Not evidence for the isolation.
- **Run-dir relocation (FIX copy): PARTIAL.** Closes A2, A3, A8; not A4, A7. A5, A6 not re-run on the copy.

## Not verified / declared

- Only BASE among honest-tool runs; no other honest tool was run.
- A5 bounded (depth<=6, <=300000 dirs) because `/fast/scratch` is 254G; the whole tree was not scanned.
- FIX copy: A5/A6 unmeasured.
- Single run per variant on this host (Python 3.14.8).
- No tool installed or updated (no pacman, uv or npm action). Python 3 `-I` only.
- Lane `quality/__pycache__/` entries exist; this seat did not create them (all lane invocations used `-B`).
- Scratch removed before yield; receipts copied to the deliverable directory first.
