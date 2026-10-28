# R55RevScratchDiscipline — report (round 55, w1, reviewer, read-only)

Deliverable: `.ufo/waves/round-55/w1/R55RevScratchDiscipline/scratch.md` (full audit: naming rule, per-instrument table, findings D1–D10, disk state, misrooted paths, unverified items). Receipts with trimmed command output: `.ufo/waves/round-55/w1/R55RevScratchDiscipline/receipts.txt`. Both are under the lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.

## What I did

1. Read `registration.md`, `claims-frozen.md`, `ctl/*.py`, `freeze-verify.py`, `receipts/freeze-verify.txt`, `receipts/before.txt`, and the seat-spec SCRATCH paragraph (the §7 rule text in context).
2. `disk-guard.sh status` (read verb). The first run was backgrounded and truncated; the complete run (60.65 s) is at `artifact://82151`.
3. Grepped the round-55 tree and every seat draft for `/tmp`, `mktemp`, `mkdtemp`, `tempfile`, `TMPDIR`, `gettempdir`, `rmtree`, `finally`, `--work`.
4. Read the cleanup and `--work` paths of each draft instrument (C1 counters A/B, C1 harness, C2 harness, C3 counters A/B, C3 harness, freeze-order checker, tool drafts 1–4).
5. Ran read-only probes: C1 counter B and freeze-order checker in normal mode with no `--work` and `TMPDIR` pointed at a probe dir; freeze-order `--selftest` with no `--work`; committed `freeze-verify.py` from the lane root; `git diff --stat 54dacbd8..HEAD` over the frozen paths; `/tmp` and `/var/tmp` listing newer than 18:30.
6. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain` and `git -C /home/vgpnk/Projects/shokunin status --porcelain` (read-only; nothing moved or deleted).

No host reads (`hyprctl`, `input.conf`) were needed. No installs or upgrades. No git mutation. No write outside this report, its deliverable directory, and my scratch dir (`/fast/scratch/hyaku/mado-r55/R55RevScratchDiscipline/`, removed before yield). No hold-out path was opened or used.

## Key results

- **No hardcoded `/tmp` in code.** `registration.md`, `claims-frozen.md`, `freeze-verify.py`, `ctl/*.py`, `quality/check-r55-controls.py` and every round-55 `*.py`/`*.sh` draft have zero `/tmp` code hits. Every `mkdtemp` carries `dir=`. Text-only hits are rule text, prompt text, and one receipt that used a "/tmp clone" for S094 (`R55ScribeSources/receipts/...:526`).
- **Freeze intact.** `freeze-verify.py` → `FREEZE_VERIFY: bad=0 … OK` (rc 0). `git diff --stat 54dacbd8..HEAD` over the frozen paths is empty.
- **Disk not under pressure.** `/tmp` 21 %, `/var/tmp` 38 %, `/fast/scratch/hyaku` 44 %; SOFT is 70 %. `/fast/scratch/hyaku/mado-r55` is 110.9 M, idle 0 (live).
- **Naming rule for the L1** (scratch.md §1): round root `/fast/scratch/hyaku/mado-r55/` (the exact dir `disk-guard.sh purge-lane mado 55` removes at round close); seat dir `…/mado-r55/<SeatName>/`; every temp is `mkdtemp(prefix=…, dir=<--work>)` or `mktemp -d -p`; `--work` mandatory and refused under the `--repo` toplevel; git children get `TMPDIR`/`HOME` under `--work`; each run removes only its own child in `finally`; shell seats use `trap 'rm -rf -- "$S"' EXIT`.

## Defects (full evidence in scratch.md §4)

- **D1 (medium)** C1 counter B, `c1-r55-kbd-entry.py:816,822–824,72`: `--work` optional; normal mode runs git without `TMPDIR`. CounterA has `required=True` (`:764`). Probe P1: no entry written (no leak observed in that run; the path is still unscoped).
- **D2 (medium)** freeze-order checker, `check-freeze-order.py:364–369,38–45,340`: `--work` optional in check mode; selftest cleanup not in `finally`. P2 and P3 confirm the optional path and `SETUP usage`.
- **D3 (low)** C3 counter B, `:487,512`: fixed-name `work/cli-work` created and `rmtree`'d by name; can delete a caller-owned dir.
- **D4 (low)** C1 counter A, `:554,749`: `selftest-<pid>` base removed outside `finally`.
- **D5 (low)** C3 counter A, `:75–76`: silent TMPDIR fallback on a bad work dir.
- **D6 (high, integration)** `quality/check-r55-controls.py` is untracked, sits in the tracked `quality/` tree outside every seat directory (mtime 19:05, after the freeze), and imports `r55_ctl_c1/c2/c3`, none of which exists. Probe P9: empty. It is the only misrooted wave artifact I found; reported, not moved.
- **D6b (low)** C3 harness `:350–352`: `makedirs(root)` before the `try`; a collision gives a traceback, not SETUP rc 2.
- **D7 (medium, contract)** `--counter PATH` (C1 and C3 harnesses) and `--holdout DIR` (C2 harness) are not in the frozen predicate. A `--counter` override can grade a substitute counter. Remove or record.
- **D8 (low, contract)** `registration.md:13` cites "§7.4"; no such section exists in lane or fleet markdown. The only text is the seat-spec SCRATCH paragraph.
- **D9 (low)** `freeze-verify.py` reads the working tree via `os.getcwd()`, not git objects. Freeze proof, not a counter, no temp use. State the exemption or change it.
- **D10 (observation)** S094 /tmp clone (`R55ScribeSources` receipt `:526`): removal not verified.

## Misrooted or untracked paths (read-only)

- Lane: all `??` under `.ufo/waves/round-55/w1/` are correctly rooted. `w1.ready` and `w1.ready.dispatched` are wave-root dispatch files (expected). **`quality/check-r55-controls.py`** is the one candidate misrooted artifact (D6).
- Fleet: no round-55 path. Non-wave items reported only in scratch.md §6: round-54 clones under `.scratch/closure-r54/…/clone/` (inside the fleet tree), intent-to-add entries (`o.bin`, `oldrep1.out`, `oldrep2.out`, `.scratch/*`, `__pycache__/*.pyc`), `lane3/`, `tools/round-49/`, `.ufo/waves/round-56/w3/T56W3Led13.md`.

## Could not verify

- The dispatcher end to end (modules absent). I did not run the seat drafts' selftests; those belong to other seats.
- Whether `disk-guard.sh status` appends to `disk-guard.log`. The log tail shows check-type `ok` lines at 22:54Z that I cannot attribute.
- Whether the S094 /tmp clone still exists (D10).
- Owners of unattributed `/tmp` entries, notably `/tmp/cl40` (187 MB, 18:37), which exceeds the 50 MB /tmp rule for a round-55 seat.
- Argparse only, for `R55ScribeEntryB/verify.py` and `R55ScribeIndex/verify-drafts.py`; their bodies were not read in full.
- No installs, no pacman or host state changes, no hold-out access.
