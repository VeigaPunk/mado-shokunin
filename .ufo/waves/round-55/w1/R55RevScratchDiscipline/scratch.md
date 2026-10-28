# Round 55 w1 — scratch and /tmp discipline audit (R55RevScratchDiscipline)

Read-only audit against the §7 scratch rule as quoted in the seat context (the SCRATCH paragraph) and `registration.md` lines 11–13. No tracked file, git state, host config or compositor was changed. No tool was installed or upgraded. Receipts: `receipts.txt` in this directory.

## 1. Scratch-dir naming rule the L1 should require of every integrated instrument and seat

1. **Round root.** `/fast/scratch/hyaku/mado-r55/` = `$HYAKU_SCRATCH/<lane>-r<round>`. This is the exact directory `disk-guard.sh purge-lane mado 55` removes at round close (only when no live process is inside). Nothing an instrument writes may land outside it.
2. **Seat dir.** `/fast/scratch/hyaku/mado-r55/<SeatName>/`, `SeatName` exactly as in the roster (CamelCase). Created with `mkdir -p`.
3. **Temp names.** `<purpose>` is a short lowercase noun (`c1b`, `c2`, `c3-selftest`, `freeze-selftest`, `repo`). Shell: `mktemp -d -p "$WORK" <purpose>.XXXXXX`. Python: `tempfile.mkdtemp(prefix="<purpose>-", dir=WORK)`. A bare `mkdtemp()`, `mktemp -d` without `-p`, or `gettempdir()` is forbidden.
4. **`--work` is mandatory.** `argparse` `required=True`, no default, no `None` fallback. The instrument runs `os.makedirs(work, exist_ok=True)`, takes `os.path.realpath`, and refuses (SETUP, exit 2) when that path lies under the `--repo` toplevel, so a run never dirties the lane tree.
5. **Every git child.** `-C <repo>` or `-C <scratch>`; `TMPDIR=<work>`, `HOME=<work>`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`. A scratch repo is `git -C "$D" init -q`, then `rev-parse --show-toplevel` must equal `realpath($D)` before the first commit, and commits use `-c user.name=ctl -c user.email=ctl@ctl`.
6. **Cleanup on exit.** Each run creates one owned child `D` under `--work` and removes only that child, in `try/finally` with `shutil.rmtree(D, ignore_errors=True)`. It must never remove `--work` itself and never a fixed-name path under it (`cli-work`, `selftest-<pid>` are not allowed; use `mkdtemp`). Shell seats: `S=/fast/scratch/hyaku/mado-r55/<SeatName>; trap 'rm -rf -- "$S"' EXIT`, with receipts copied out first. `disk-guard` is the backstop after a SIGKILL (IDLE_MIN 45).
7. **/tmp.** Only regular files under 50 MB. No directories, no clones, no default.
8. **Runtime writes.** Counters and harnesses write only under `--work`. They never write into `quality/`, `tools/`, `corpus/`, `.ufo/` or the fleet.
9. **Tools that take no `--work`.** `tools/mado-kbdopts.py` is contractually two-token and read-only; it rejects `--work` as usage. The harness must not pass it.

## 2. Hardcoded /tmp

Result: **no hardcoded /tmp in code**. Checked: `registration.md`, `claims-frozen.md`, `freeze-verify.py`, `ctl/*.py`, `quality/check-r55-controls.py` (untracked), and every `*.py`/`*.sh` under `w1/R55Exec*`, `R55Scribe*`. The only `/tmp` strings are rule text, prompt text and receipts (see `receipts.txt`). Every `tempfile.mkdtemp` in the drafts carries `dir=`.

One rule deviation in a receipt, not code: `w1/R55ScribeSources/receipts/SOURCES.candidate-rows-inserted.md:526` says "For S094 a /tmp clone at the tag gave tree ids". The seat's own exit line (`R55ScribeSources.md:78`) names only `/fast/scratch/hyaku/mado-r55/R55ScribeSources/`. Whether that /tmp clone was removed is not verified. Its size is unknown.

## 3. --work coverage per instrument

| Instrument (path) | --work | temp handling | cleanup | verdict |
|---|---|---|---|---|
| `freeze-verify.py` (committed) | none; no args | no temp files | n/a | no /tmp use. Reads the working tree via `os.getcwd()`, not git objects. Rule-scope note only (see D8). |
| `ctl/const-host.py`, `ctl/empty.py` (committed) | none | none; reads fixtures via `Path(__file__)` | n/a | OK |
| `ctl/lookup-committed.py` (committed) | none | none; fixtures resolved from `__file__` | n/a | OK only if run from the exported tree (registration §C2). Run from the lane it reads the lane's fixtures. |
| `quality/check-r55-controls.py` (untracked) | delegated | none itself | n/a | cannot run: imports `r55_ctl_c1/c2/c3`, none present (D6) |
| `R55ExecC1CounterA/c1-r55-kbd-entry.py` | required | `mkdtemp(dir=base)`, base under `--work`; HOME=TMPDIR=work | rmtree per case; selftest base rmtree at :749, not in `finally` | OK. Minor (D4). |
| `R55ExecC1CounterB/c1-r55-kbd-entry.py` | **optional** (`:816`) | normal mode builds `Git(repo, None)`; `TMPDIR` set only `if work:` (`:72`) | selftest `D` in `finally` | **D1** |
| `R55ExecC1Harness/r55_ctl_c1.py` | required | `mkdtemp` child of `--work`; HOME=TMPDIR=work | `finally` rmtree of the child (`:311–315`) | OK |
| `R55ExecC2Harness/r55_ctl_c2.py` | required (`:205`) | `mkdtemp(prefix="c2-", dir=work)`; `TemporaryFile(dir=work)` | `finally` rmtree of scratch (`:303–305`) | OK. `--holdout DIR` override is outside the frozen predicate (D7). |
| `R55ExecC3CounterA/c3-r55-p19.py` | required in `main` (`:540`) | `mkdtemp(dir=work)`; `Repo` sets TMPDIR only `if work and isdir(work)` (`:75`) | `finally` rmtree (`:513–514`) | OK. Silent TMPDIR fallback is low (D5). |
| `R55ExecC3CounterB/c3-r55-p19.py` | required (`:531`); `prepare_work` creates it | `mkdtemp(dir=work)` for `D` | `finally` rmtree `D` and fixed `work/cli-work` (`:512`) | **D3** |
| `R55ExecC3Harness/r55_ctl_c3.py` | required (`:328`) | fixed `work/c3-ctl-<pid>`, `makedirs` without `exist_ok` (`:350–351`, before the `try`) | `finally` rmtree of root (`:418–419`) | OK. Setup OSError escapes outside the try (D6b). `--counter` override is outside the predicate (D7). |
| `R55ExecFreezeOrder/check-freeze-order.py` | **optional** in check mode (`:364–369`); required in selftest | `git_env(None)` leaves TMPDIR unset (`:44–45`); selftest `mkdtemp(dir=work)` | selftest `rmtree(base_dir)` at `:340`, **not in `finally`** | **D2** |
| `R55ExecTool1..4/mado-kbdopts.py` | must not take `--work` | no `tempfile`, `subprocess`, `open(...,"w")`, sockets | n/a | correct by construction |
| `R55ScribeSources/verify-r55-seat-sources.py` | required, unused | none | n/a | OK |
| `R55ScribeEntryB/verify.py`, `R55ScribeIndex/verify-drafts.py` | required (argparse) | documented as writes only under `--work` | not read in full | argparse checked only |

## 4. Findings

| ID | Sev | Where | Evidence | Fix the L1 should require |
|---|---|---|---|---|
| D1 | medium | `R55ExecC1CounterB/c1-r55-kbd-entry.py:816,822–824,72` | `--work` optional; with no `--work` git children get no `TMPDIR`. Sibling CounterA has `required=True` (`:764`). Probe P1 with `TMPDIR=<probe>`: 0 entries written. | `required=True`; keep the CounterA form. |
| D2 | medium | `R55ExecFreezeOrder/check-freeze-order.py:364–369, 38–45, 340` | check mode accepts no `--work`; `git_env(None)` leaves TMPDIR unset. Probe P2 with `TMPDIR=<probe>` and no `--work`: 0 entries, rc 1. Probe P3 (`--selftest` with no `--work`) → `SETUP usage` rc 2. Selftest `rmtree(base_dir)` at `:340` is not in `finally`; an assertion at `:184` leaves `freeze-selftest-*` under `--work`. It also refuses a missing `--work` where C1A, C2, C3B create it. | `--work` required in both modes; create it with `makedirs(exist_ok=True)`; wrap selftest cleanup in `finally`. |
| D3 | low | `R55ExecC3CounterB/c3-r55-p19.py:487,512` | fixed-name `work/cli-work` created and `rmtree`'d by name, so a caller-owned `cli-work` under `--work` is deleted. | use `mkdtemp(dir=work)`. |
| D4 | low | `R55ExecC1CounterA/c1-r55-kbd-entry.py:554,749` | selftest base is `work/selftest-<pid>`; removed at `:749` outside any `finally`. | use `mkdtemp(dir=work)` in `try/finally`. |
| D5 | low | `R55ExecC3CounterA/c3-r55-p19.py:75–76` | `Repo` sets TMPDIR only `if work and isdir(work)`, so a bad dir falls back silently to the inherited TMPDIR. Reachable only through selftest with a bad dir; `main` requires `--work`. | raise SETUP instead of falling back. |
| D6 | high (integration) | `quality/check-r55-controls.py` (untracked, mtime 19:05) | the dispatcher imports `r55_ctl_c1/c2/c3`; none exists in `quality/` (probe P9). Corroborates ScribeIndex D3. | integrate the three modules and the counters, or the predicate cannot pass. |
| D6b | low | `R55ExecC3Harness/r55_ctl_c3.py:350–352` | `os.makedirs(root)` runs before the `try`; a pid-name collision surfaces as a traceback, not `SETUP` rc 2. | `exist_ok` plus SETUP inside the try. |
| D7 | medium (contract) | `R55ExecC1Harness` usage (`--counter PATH`), `R55ExecC3Harness/r55_ctl_c3.py:323`, `R55ExecC2Harness/r55_ctl_c2.py:206` (`--holdout DIR`), `quality/check-r55-controls.py:4` | registration frozen predicates pass only `--repo --rev --work`. A `--counter` override lets a substitute counter be graded; `--holdout` lets a caller swap the hold-out. | remove both overrides, or record them in the registration. An override must not change the frozen predicate. |
| D8 | low (contract) | `registration.md:13` cites "§7.4" for the scratch rule | no §7.4 found in lane or fleet markdown (`grep §7` hits are unrelated sections). The only text of the rule is the seat-spec SCRATCH paragraph (`make-w1-spec.py:12`). | cite the rule text by file and line, or add the section. |
| D9 | low (rule scope) | `freeze-verify.py` | reads the working tree through `os.getcwd()`, not git objects (registration §Rules says all counters read git objects). It is a freeze proof, not a counter, and it uses no temp. | state the exemption in the registration or read via `git show`. |
| D10 | observation (receipt) | `R55ScribeSources/receipts/...:526` | a /tmp clone at the tag was used for S094; removal not verified. | confirm the clone is gone; do not reuse /tmp for clones. |

No seat or instrument in the wave writes outside `--work` or the seat dir, apart from D6.

## 5. Disk and /tmp state (disk-guard status, read-only)

- `/tmp` 21 % (101.7 G free), `/var/tmp` 38 %, `/fast/scratch/hyaku` 44 %. All below SOFT 70 %; no pressure.
- `/fast/scratch/hyaku/mado-r55`: 110.9 M, idle 0 (live, in use). Nothing else in the top 15 of `/tmp` or `/var/tmp` is named for mado or round 55.
- Unattributed `/tmp` entries newer than 18:30 (not named for this wave, not touched): `/tmp/cl40` (187 MB, 18:37), `/tmp/r51cl` (200 KB), `/tmp/r51-closure.json`, `/tmp/idx_full.json`, `/tmp/map_hash_before|after`, `/tmp/wr_smoke.log`, `/tmp/x` (19:55), `/tmp/r41c1-*`. `cl40` is over 50 MB, which the /tmp rule forbids for a round-55 seat; its owner is unknown.

## 6. Misrooted or untracked paths

Lane `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain`:

- All `?? .ufo/waves/round-55/w1/<seat>` and `<seat>.md` paths sit in the correct seat root. None is misrooted.
- `.ufo/waves/round-55/w1.ready` and `w1.ready.dispatched`: dispatch files at the wave root. Expected.
- **`quality/check-r55-controls.py` (untracked, 19:05)**: written into the tracked `quality/` tree, outside every seat directory, after the freeze. It is the contract's named harness path, but no seat subdirectory holds it, so it breaks the seat boundary. Reported only; not moved or deleted.

Fleet `git -C /home/vgpnk/Projects/shokunin status --porcelain`: no path named for round 55. Non-wave items, reported only:

- `.scratch/closure-r54/{lane,work-c2,work-c2-base/clone,work-c2/clone}/`: round-54 clones inside the fleet tree, not under `/fast/scratch/hyaku`.
- ` A` entries (intent-to-add; blob `e69de29`, stage 0; `git diff --cached` is empty): `o.bin`, `oldrep1.out`, `oldrep2.out`, `.scratch/source-routing-queue.md`, the `.scratch/closure-*` bytecode and json files, and `__pycache__/*.pyc` under `.scratch/closure-r54/work-c*`.
- `lane3/` (nested git repo), `tools/round-49/` (fleet root, not mado), `.ufo/waves/round-56/w3/T56W3Led13.md` (round 56), `.scratch/kasegi-r44/`.

## 7. Could not verify

- The dispatcher end to end (modules absent, D6). I did not run the seat drafts' selftests; those are other seats' jobs.
- Whether `disk-guard.sh status` appends to `disk-guard.log`. The tail shows check-type `ok` lines at 22:54Z, which I cannot attribute. Status is documented as table-only.
- Whether the S094 /tmp clone (D10) still exists.
- Owner of `/tmp/cl40`, `/tmp/x`, `/tmp/map_hash_*`.
- Pacman, host and tool state: not touched. No installs. No `hyprctl` read was needed.
- No hold-out path was opened or used. I saw no hold-out path.

Scratch: `/fast/scratch/hyaku/mado-r55/R55RevScratchDiscipline/` (probe dir only) is removed before yield.
