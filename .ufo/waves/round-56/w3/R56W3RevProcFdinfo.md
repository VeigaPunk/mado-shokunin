# R56W3RevProcFdinfo — second /proc capability sample

## Findings, by severity

No blocking, weakening, or cosmetic defect in the scoped watch-list prediction was established. Recommendation only: the second live sample supports the capability row, not admission of the whole frozen C2 predicate.

**Attacked:** predicted primary-watch count, inode set, registration-order consistency and masks against the operator's running compositor; longitudinal drift since the attempt-1 2026-10-28 receipt.

Axes: coverage (C1), operability/capability acquisition (C2, this seat), registry consistency/calibration (C3). Local comparison axes: count, inode identity, order, mask fidelity, temporal stability. Frozen predicates were not changed.

## Observed result

At `2026-10-30T05:04:00.275753+00:00`, own-user Hyprland PID **1622**, started `Mon Oct 26 12:08:38 2026`, had inotify tables exposed through fd **12** and **86**. Each contains exactly **40** rows, with identical wd/inode/mask values. They may be duplicate descriptors for one instance [INFERENCE]; descriptor identity was not established. They must not be summed as 80 independent config watches.

The pinned tool predicts **40 primary watches, zero canonical watches, unsupported=0, errors=0**. All **40/40** inodes match; no missing/extra inodes; wd 1–40 align with predicted n 1–40. All kernel event masks are `0x8` (`IN_CLOSE_WRITE`). `IN_DONT_FOLLOW` in the prediction is an add-watch path-resolution flag, not a persistent event-mask bit.

Both inotify snapshots, before and after the tool runs, are identical. Unrelated sync-file descriptors 165/172 varied; this is not watch-table drift. The inode sequence also exactly matches all 40 rows of the prior `w2/R56W2RevProcFdinfo/comparison.md` receipt.

## Exact commands and decisive outputs

```text
pgrep -a -u vgpnk -x Hyprland
1622 Hyprland --watchdog-fd 4

ps -o pid=,uid=,lstart=,etime=,comm= -p 1622
1622 1000 Mon Oct 26 12:08:38 2026 3-13:55:21 Hyprland

python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-watchplan.py --config /home/vgpnk/.config/hypr/hyprland.conf --home /home/vgpnk
MADO_WATCH: config=/home/vgpnk/.config/hypr/hyprland.conf autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0
MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=NONE

journalctl --user -u Hyprland --no-pager --since 2026-10-28
-- No entries --
```

All commands above returned 0. To bind evaluation to the assigned tree, `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:tools/mado-watchplan.py` exported the single tool to seat scratch. Its bytes exactly matched the working-path tool (sha256 `3ccf070841b3c0134a05f612a35e553364f318a9d36843455f4207df118f22b7`). Running the same arguments with `python3 -I /fast/scratch/hyaku/mado-r56/R56W3RevProcFdinfo/mado-watchplan.py` returned 0 and identical stdout. Exact argv/outputs are retained in `commands.json`.

Kernel acquisition used `Path('/proc/1622/fd').iterdir()` plus `os.readlink`, and `Path('/proc/1622/fdinfo').iterdir()` plus `Path.read_text()`, retaining only lines starting `inotify `. Each watch path was `os.lstat`-ed to compare primary inode identity. This is reproducible without touching compositor state:

```text
python3 -I -c 'import pathlib,os; p=pathlib.Path("/proc/1622"); print({f.name:os.readlink(f) for f in (p/"fd").iterdir()}); print({f.name:[s for s in f.read_text().splitlines() if s.startswith("inotify ")] for f in (p/"fdinfo").iterdir()})'
```

That standalone reproduction command was not separately run; the equivalent acquisition executed twice within the isolated sampling driver. Full raw snapshots are preserved. Derived masks were corrected from those raw bytes after discovering that an unbounded field regex also matched `ignored_mask`; the corrected whitespace-bounded parser and disclosure are in `comparison-a2.md`.

## Residual risk and verification gaps

- The requested journal command ran but returned no records. It cannot establish absence of reloads/coredumps during the intervening two days. No observed inode/order drift requires a causal explanation; process start predates both samples.
- Numeric wd ordering is consistent with registration order, not a historical syscall trace. Duplicate descriptor identity is unproven.
- This is one read-only live observation bracketed by two stable tables, not saturation or universal equivalence with Hyprland. C2 fixture/holdout/control harnesses and unrelated C1/C3 counters were not run by this seat.
- `read xd://lsp` returned `No such tool`; semantic references/definitions/diagnostics were unavailable. No grep output is presented as semantic proof.
- No compositor signals, reloads, host writes, runtime rerouting, resume operations, tracked-file edits, git mutations, installations, or delegated/background jobs occurred. Scratch was removed in `finally` after copying receipts.

## Deliverables

All paths below are relative to the lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`:

- `.ufo/waves/round-56/w3/R56W3RevProcFdinfo/comparison-a2.md` — side-by-side 40-row table, verdict and journal citations.
- `.ufo/waves/round-56/w3/R56W3RevProcFdinfo/sample.json` — raw before/after fd links and inotify lines, corrected parsed tables, path inode identities and summary.
- `.ufo/waves/round-56/w3/R56W3RevProcFdinfo/commands.json` — exact subprocess argv/exit/stdout/stderr.
- `.ufo/waves/round-56/w3/R56W3RevProcFdinfo/watchplan.txt` — complete pinned prediction.
- `.ufo/waves/round-56/w3/R56W3RevProcFdinfo/journal.txt` — requested journal window.

## Self-evaluation

Accuracy 4/5: raw evidence supports 40/40; historical syscall ordering remains inferential. Completeness 4/5: requested acquisition and longitudinal comparison complete, journal history unavailable despite executing the requested command. Clarity 4/5: distinction between fd duplication and independent watch instances is explicitly qualified. Actionability 4/5: raw receipts and reproduction method supplied; driver scratch intentionally removed. Conciseness 4/5: report and comparison repeat the key result for standalone usability. Overall 4.0/5. Highest-value improvements would require historical journal coverage and a registration trace, neither established by these allowed read-only observations. The user should agree with the scoped evidence and disclosed limits.
