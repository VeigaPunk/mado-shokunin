# R56W2RevProcFdinfo — empirical check of the C2 watch model against the running compositor

Seat: R56W2RevProcFdinfo (leaf; read-only /proc; no hyprctl state change; no file under ~/.config or ~/.local written).
Subject: `tools/mado-watchplan.py` at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed (blob sha256 `ed6ee9f200cdc0646fb2f31898f37a2570318a7609d91c7cd730c501c1aa9379`, exported with `git show`), and the entry `corpus/knowledge/hyprland-config-autoreload-r56.md` as it bears on watches.
Receipts: `.ufo/waves/round-56/w2/R56W2RevProcFdinfo/` (`comparison.md` 40-row table, `fdinfo-capture.txt`, `plan.txt`, `tool-output.txt`, `getoption.json`, `rows.json`, `tool.sha256`, probe scripts).

## Verdict

On this host, at this moment, the C2 watch model predicts the compositor's live inotify watch set exactly: 40 predicted primary watches, 40 kernel watch registrations on the one inotify instance, the same 40 inode numbers, and the same watch-descriptor order. No extra watches, no missing watches, no event-mask disagreement on the bits fdinfo can show.

Three limits apply to that agreement:
- `IN_DONT_FOLLOW` is never visible in `/proc/<pid>/fdinfo` on this kernel (the kernel drops it from the printed mask). The predicted `IN_CLOSE_WRITE|IN_DONT_FOLLOW` can therefore be checked only as `IN_CLOSE_WRITE`; the `IN_DONT_FOLLOW` half is not confirmed by this seat's evidence.
- The canonical (symlink) branch and the missing-path branch are not exercised: on this host none of the 40 watched paths is a symlink and none is missing. Agreement says nothing about those branches.
- The check is one host, one tree, one snapshot. It shows the model is faithful for this tree; it does not verify the model for other trees.

## Attack items and results

### A1 — pid, fd identity, and watch count

Commands and trimmed output:
```
$ pgrep -o -x Hyprland
1622
$ ps -o lstart= -p 1622
Mon Oct 26 12:08:39 2026
$ ls -l /proc/1622/fd | grep inotify
lr-x------ ... 12 -> anon_inode:inotify
lr-x------ ... 86 -> anon_inode:inotify
$ cat /proc/1622/fdinfo/12   # header
flags: 02004000   (O_NONBLOCK|O_CLOEXEC; = inotify_init1(IN_NONBLOCK|IN_CLOEXEC))
ino: 1094
inotify wd:1 ino:21221 ... mask:8 ...  ...  (40 lines, wd 1..28 hex 1..1c.. see comparison.md)
$ diff <(head -4 fdinfo/12) <(head -4 fdinfo/86) -> identical headers
$ md5sum <(grep ^inotify fdinfo/12) <(grep ^inotify fdinfo/86) -> d3b61167548dd4ff817a65f4dae3db10 both
```

Two inotify fds (12 and 86) exist in the process. Their watch lists are byte-identical. Decisive test: `kcmp(KCMP_FILE)` with validated controls (my own `dup()` returns 0, an independent `open()` returns 1, both as expected), applied to the compositor:
```
kcmp(1622, 1622, KCMP_FILE, 12, 86) -> 0   => same open file description
```
So fd 86 is a duplicate of the one instance created by `inotify_init1` (the only `inotify_init1` call site in the binary, `CConfigWatcher` ctor, disassembly at 0x46622c). The dup is consistent with libwayland-server's `wl_event_loop_add_fd`, which calls `wl_os_dupfd_cloexec` (disassembly of `libwayland-server.so.0`; Hyprland registers the inotify fd at `Hyprland-EventLoopManager.cpp:128`). A direct probe of that dup path was inconclusive (the new fd was not present when I looked; I do not rely on it). The `kcmp` result is the evidence used.

The kernel registration count is 40 per fd (`kernel distinct inodes: 40 lines: 40`). The tool prints `watches=40`. The inode `ino:` field of fdinfo is the anon inode `1094` for every inotify fd, so it cannot tell instances apart; `kcmp` is the discriminator.

Process start: the first pass of this seat used `/proc/<pid>` ctime and printed Oct 27 18:57, which is wrong. Corrected from `/proc/<pid>/stat` starttime (1874 ticks after btime 1793027300) the start is 2026-10-26 12:08:38 -0300, matching `ps lstart` (12:08:39) and `uptime -s` (12:08:37). The earlier wrong value is corrected here; the conclusion in A3 holds on the correct basis.

### A2 — tool prediction vs kernel registrations (the join)

`python3 -I tool.py --config $HOME/.config/hypr/hyprland.conf --home $HOME --getoption getoption.json` (the spec command without `--getoption` yields identical watch lines; 3 runs byte-identical):
```
MADO_WATCH: config=/home/vgpnk/.config/hypr/hyprland.conf autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0
MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE
MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE
```
For each predicted path, `os.lstat(path).st_ino` (no dereference; `islink` is False for all 40):
```
predicted inode set size: 40   kernel inode set size: 40
PREDICTED-NOT-IN-KERNEL (0):
KERNEL-NOT-PREDICTED (0):
wd order == tool predicted order: True   (fd 12 and fd 86, all 40 lines)
```
Full table (wd, predicted n, inode, kernel mask, decoded, predicted mask, path): `receipts/comparison.md`. Predicted watch n=1 is `hyprland.conf` (wd 1, inode 21221); n=40 is `gkeep.conf` (wd 40, inode 26324557).

Missing-path check: 0 of 40 predicted paths are `type=missing`. Duplicate-path check: 40 distinct paths and 40 distinct inodes, so the duplicate-watch and duplicate-wd cases do not arise here.

Positive control for the detector (the comparison is able to fail): a mutated copy of the tool with nested `source` lines disabled (`tool_mut.py`, one changed line) predicts 1 watch; the same detector reports `missing=39` against the 40 kernel inodes (inodes 802, 803, 804, 806, 807, ...). The real tool reports 0.

### A3 — config mtimes against process start

Process start (correct basis): 2026-10-26 12:08:38 -0300 (epoch 1793027318). For all 40 watched paths, `lstat` mtime and ctime were compared with that epoch:
```
watched paths whose mtime is NEWER than the compositor start: NONE
watched paths whose ctime is newer than the compositor start: NONE
```
Newest watched mtime: `~/.config/hypr/gkeep.conf` 2026-10-17 17:05:14 (older than the start). No config changed since start, so the source set the compositor loaded is the source set the tool read.

### A4 — mask decoding

Kernel IN_* values read from `/usr/include/linux/inotify.h`: IN_CLOSE_WRITE=0x8, IN_MOVED_FROM=0x40, IN_MOVED_TO=0x80, IN_CREATE=0x100, IN_DELETE=0x200, IN_ONLYDIR=0x01000000, IN_DONT_FOLLOW=0x02000000, IN_EXCL_UNLINK=0x04000000.

Live fdinfo masks: all 40 watches print `mask:8` = IN_CLOSE_WRITE. The predicted primary file mask is `IN_CLOSE_WRITE|IN_DONT_FOLLOW` (0x2000008). Controlled probe (`maskprobe.py`, fresh instance per case, scratch files):
```
file IN_CLOSE_WRITE                        requested 0x00000008 -> fdinfo 0x00000008
file IN_CLOSE_WRITE|IN_DONT_FOLLOW         requested 0x02000008 -> fdinfo 0x00000008   (DONT_FOLLOW dropped)
file ...|IN_EXCL_UNLINK                    requested 0x06000008 -> fdinfo 0x04000008   (EXCL_UNLINK kept)
dir  ICW|DF|CREATE|DELETE|MOVED_TO|MOVED_FROM requested 0x020003c8 -> fdinfo 0x000003c8
```
So fdinfo prints event bits (and EXCL_UNLINK) but not the watch-flag `IN_DONT_FOLLOW`. Mask verdict: the event bit agrees for all 40 (8 = IN_CLOSE_WRITE); the IN_DONT_FOLLOW half of the predicted mask cannot be seen in /proc on this kernel. The directory mask (0x3c8) is consistent with the tool's directory mask minus DONT_FOLLOW; no live watch is a directory.

Symlink semantics of the flag (scratch tree, `symlinkprobe.py`): with `IN_DONT_FOLLOW` the kernel watched the link inode (ino of lstat); without it, the target inode. So the flag takes effect at the kernel, which supports the model's reading of the pin (K30). This was shown in a scratch tree, not on the live compositor, whose 40 watches are all regular files and therefore never reach that branch.

### A5 — other inotify users in the process, and the nested-source file

- Two fds, one instance (A1). No second instance; no other inotify user in the process: `inotify_init1` is called from exactly one site in `/usr/bin/Hyprland`; the system libraries that call `inotify_init1` (libgio, libudev, libmount, libsystemd) are not part of Hyprland's own watch set and their instances would appear as separate fds with separate watch lists; none exists in this process (`ls -l /proc/1622/fd | grep -c inotify` = 2, both the same description).
- Nested source: `~/.config/omarchy/current/theme/gum.env.conf` is watched (n=8, reached via `envs.conf:3`), inode 27329, present in the kernel list. Matches.

### A6 — host options

`hyprctl getoption misc:disable_autoreload -j` → `{"option": "misc:disable_autoreload", "int": 0, "set": false }`. `grep -rn disable_autoreload ~/.config/hypr ~/.config/omarchy/current` finds nothing. The tool's live join `live=0 config=0 AGREE` agrees; the watch list is non-empty (`autoreload=on`), consistent with 40 live registrations.

`hyprctl version -j`: branch v0.56.2, commit efb50993780079460b0cbed1363e2166a2de1d9f, dirty false. Matches the pin commit.

### A7 — process argv and environment

`/proc/1622/exe` → `/usr/bin/Hyprland`; cmdline `Hyprland --watchdog-fd 4`. Compositor environment `HOME=/home/vgpnk`, matching the `--home` argument used. The tool's `~` expansion (from `--home`) and Hyprland's `getenv("HOME")` agree here, so divergence (1) of E8 does not bite on this host.

## Defects and findings

1. **[weakens the entry's Limits, not a predicate]** The entry's Limits say "no filesystem event was generated, no inotify descriptor was read". The second half is true of event reads but not of watch registrations: `/proc/<pid>/fdinfo` shows the compositor's live watch set (40 lines) without generating an event. The Limits sentence should say that the registration set was observed through fdinfo and that events were not. Entry not edited (frozen-tree rule).
2. **[weakens the mask leg, minor]** `IN_DONT_FOLLOW` is not representable in fdinfo (A4). Any claim that the live primary watches carry `IN_DONT_FOLLOW` rests on the pin text (K07) and the kernel's behaviour in a scratch tree (A4), not on the compositor's own readout. Cosmetic for C2, since the tool's predicted list is the same either way; it matters only if an entry claims the flag was observed live.
3. **[cosmetic]** Two inotify fds in the process (12, 86), one open file description (`kcmp`). The second is a dup from the wayland event-loop registration. The tool is not wrong to predict one watch set; it does not model fd duplication, and the model does not need to.
4. **[not a defect; my own error, recorded]** An interim reconciliation printed "52 files" for `~/.local/state/omarchy/toggles/hypr/*.conf`. That was a bug in my script (`sorted()` over a string, counting characters). The directory holds 2 files (`flags.conf`, `window-no-gaps.conf`), matching the tool's n=37 and n=38.
5. **[not a defect; recorded]** Process start first computed from `/proc/<pid>` ctime (A1 correction). Corrected; conclusion unchanged.
6. **[not verified]** The canonical (symlink) watch and the missing-path watch are not exercised live on this host (A2). The `inotify_add_watch` return value that the entry says is unchecked (K09/E02) cannot be tested from fdinfo here: I did not run a failing add on the live instance, and the live list contains no missing-path entry to show what a failed add leaves behind. The live list therefore neither confirms nor refutes E02.
7. **[not verified]** The wayland dup (A1) is supported by the `kcmp` result and a disassembly reading; a direct runtime probe of `wl_event_loop_add_fd` did not produce a usable result (the duplicated fd was not present when listed). Not relied on for any count.

## Commands with no defect found (null results)

- Extra watches not predicted by the tool: set difference of the 40 kernel inodes against the 40 predicted inodes is empty (`KERNEL-NOT-PREDICTED (0)`, A2).
- Missing predicted watches: `PREDICTED-NOT-IN-KERNEL (0)`, A2.
- Missing predicted paths on disk: `type=missing` count 0 in `plan.txt` (A2).
- Config changed after start: none newer by mtime or ctime (A3).
- Second instance / foreign inotify user: one `inotify_init1` site in the binary; two fds share one description per `kcmp` (A1, A5).
- Watch-count mismatch: 40 tool, 40 kernel (A1, A2).

## Limits of this seat

- One host, one snapshot (pid 1622, started 2026-10-26 12:08:38). The result is a fact about this tree on this host.
- Live fdinfo is read through `/proc` only. No `hyprctl keyword/dispatch/reload` was run; no file under `~/.config` or `~/.local` was written.
- The compositor's watch list is observed; its event delivery is not (no save was made). The entry's UNKNOWN items on event delivery and reload-on-save remain open.
- `IN_DONT_FOLLOW` on the live primary watches is not verified (finding 2).

## Tooling

No tool was installed or upgraded. Read-only use of `objdump`, `nm`, `ldd`, `kcmp` through ctypes, and the Python 3.14 stdlib. Scratch: `/fast/scratch/hyaku/mado-r56/R56W2RevProcFdinfo/`, removed before yield; receipts copied to the deliverable directory first.
