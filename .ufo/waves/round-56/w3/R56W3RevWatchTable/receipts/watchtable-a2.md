# R56W3RevWatchTable — watch table comparison and timeline (attempt 2)

Read-only. Host: Hyprland pid 1622 (`Hyprland --watchdog-fd 4`, uid 1000, `ps lstart` = Mon Oct 26 12:08:39 2026 -03). Nothing was signalled, reloaded, restarted or written under `~/.config` or `~/.local`.
Live capture: 2026-10-30, about 05:05–05:08Z (`date -u` 05:06:53Z at the fd read; fdinfo read in the same minute).

## 1. Live watch table (fdinfo, read-only)

Command: `python3 -I receipts/capture.py 1622 > capture-a.json` (reads `/proc/1622/fd` and `/proc/1622/fdinfo/<fd>` for every fd whose link is `anon_inode:inotify`).

```
fd 12  -> anon_inode:inotify   40 watch rows, wd 1..40 distinct, mask 0x8, ignored 0
fd 86  -> anon_inode:inotify   40 watch rows, wd 1..40 distinct, mask 0x8, ignored 0
fdinfo 12 and 86: ino:1094  pos:0  flags:02004000  mnt_id:19   (same anon inode => same open file description)
fd12 wd->ino map == fd86 wd->ino map: True
```

Interpretation: one inotify instance (fds 12 and 86 are duplicates of one open file description; `ino:1094` is identical in both fdinfo files). The instance holds exactly 40 watches. No other inotify instance exists in the process. The 40 watches are the config watcher's list; no second source of watches is present.

Mask note: the kernel shows `mask:8` (IN_CLOSE_WRITE) on every row. `IN_DONT_FOLLOW` (0x02000000) is an add-time flag and is not reported back in fdinfo; the tool's predicted `IN_CLOSE_WRITE|IN_DONT_FOLLOW` is therefore compared on the kernel bit only.

## 2. Prediction (pinned tool)

Commands and output (decisive lines):

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-watchplan.py --config /home/vgpnk/.config/hypr/hyprland.conf --home /home/vgpnk
MADO_WATCH: config=/home/vgpnk/.config/hypr/hyprland.conf autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0
MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=NONE          (plan-a.txt)

hyprctl getoption misc:disable_autoreload -j
{"option": "misc:disable_autoreload", "int": 0, "set": false }         (getoption-a.json)
python3 -I .../mado-watchplan.py --config ... --home /home/vgpnk --getoption getoption-a.json
MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE
MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE

git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:tools/mado-watchplan.py | sha256sum
3ccf070841b3c0134a05f612a35e553364f318a9d36843455f4207df118f22b7   (identical to the working-path tool; its plan output is byte-identical: plan-at-0f3a.txt == plan-a.txt)
python3 -I tools/mado-watchplan.py --selftest  ->  MADO_WATCH_SELFTEST: 86/86 assertions passed
```

`hyprctl version -j`: `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"`, `"version": "0.56.2"`, `"dirty": false` (matches the entry's pin H03).

## 3. Three-sample comparison

Samples: S1 = `w2/R56W2RevProcFdinfo/comparison.md` (2026-10-28, 40 rows, wd|predicted n|inode); S2 = `w3/R56W3RevProcFdinfo/comparison-a2.md` (sibling, 2026-10-30 05:04:00Z by its own report); S3 = this seat (2026-10-30 ~05:06Z).

| check | S1 2026-10-28 | S2 sibling 2026-10-30 | S3 this seat 2026-10-30 |
|---|---|---|---|
| inotify instances in pid 1622 | not restated | 1 (two fds, same table) | 1 (fds 12, 86 = same open file, ino 1094) |
| watch count | 40 | 40 | 40 |
| wd values | 1..40 | 1..40 | 1..40 (distinct) |
| inode set | 40 inodes | 40 inodes | 40 inodes |
| wd -> inode, in order | = predicted n 1..40 | = predicted n 1..40 | = predicted n 1..40 |
| kernel mask | 0x8 ×40 | 0x8 ×40 | 0x8 ×40 |
| tool predicted paths | 40 | 40 | 40 (unsupported=0 errors=0) |
| canonical/symlink watches | 0 | 0 | 0 |

Row-level: `receipts/table.md` lists all 40 rows (wd, n, path, live inode, S1 inode, S2 inode, current lstat inode). Result: **ALL_MATCH True, 40/40 across all three samples and the current lstat.** Machine-checked by `python3 -I` comparing `capture-a.json`, the S1 comparison table, the S2 `comparison-a2.md` table (wd col 4, kernel inode col 5) and `os.lstat` of each predicted path.

Count / inodes / order versus prior samples: identical. A watch-list rebuild would have changed the wd values (section 5), so identical wd values across 2026-10-28 and 2026-10-30 are direct evidence that the table was not rebuilt in that interval.

## 4. Current state of the watched files (direct evidence, no reload needed)

`lstat-a.json`: for all 40 predicted paths, the max mtime and max ctime are **2026-10-17 17:05:14 -03**. Process start is 2026-10-26 12:08:39 -03. No watched path has mtime or ctime after process start. Each path's current inode equals the watched inode, so no watched path was atomically replaced (rename-over) since the watches were built.

## 5. Would a reload rewrite the table? (source chain + kernel test)

Chain (corpus entry `hyprland-config-autoreload-r56.md`, steps 4–7; K15, K16, K19, E09): an inotify event or `hyprctl reload` → `reload()` → `postConfigReload` → `scheduleRefresh(REFRESH_ALL)`; `REFRESH_ALL` = all 16 bits set, so it includes `REFRESH_CONFIG_WATCHER` (bit 8); the refresher calls `Config::watcher()->update()` → `setWatchList` removes every existing watch (K05) and then re-adds every entry.

Kernel behaviour of that sequence, tested on this host's kernel (`uname -r` = 7.2.11-arch1-1) with a **private inotify instance on 40 scratch files** (no Hyprland state touched):

```
first build wds:    [1, 2, 3, 4, 5] ... [38, 39, 40]   max 40 count 40 distinct 40
rm rc all zero:     True
rebuild wds:        [41, 42, 43, 44, 45] ... [78, 79, 80]   min 41 max 80
rebuild wds disjoint from first build: True
re-add of an already-watched inode returns existing wd: [41] == second[0] 41 True
rm of already-removed wd rc: -1 errno 22 (EINVAL)   (the unchecked duplicate rm of K05 fails, as the entry says)
```

Conclusion: **a reload (any path through `update()`) would rewrite the table**: the 40 old wds are removed and 40 new wds 41..80 are allocated in the same instance. Hyprland's wd allocation is monotonic per instance (kernel `idr_alloc_cyclic`, shown by the test; the source of the kernel is not pinned here).

Observed: the table is wd 1..40 in S1 (2026-10-28), S2 and S3 (2026-10-30); the maximum wd is 40 and no wd above 40 exists. The table was therefore built once, at startup, and never rebuilt through 2026-10-30 05:06Z. Under the chain, **no reload reached `update()` since process start**, including none since 2026-10-28. Every `hyprctl reload` path in the omarchy scripts would have produced wd 41+ (see section 7), so none ran in a way that reached the watcher.

Limit of this inference: it holds only if the running build reaches `update()` on reload (chain step 7, source-level; not observed at runtime). The kernel half is tested; the Hyprland half is source inference, as the entry says.

## 6. Timeline (all times -03 unless marked Z)

| time | event | evidence |
|---|---|---|
| 2026-10-03 .. 2026-10-17 | last modification of every watched file (max mtime 2026-10-17 17:05:14) | lstat-a.json |
| 2026-10-26 12:08:39 | uwsm/start-hyprland starts pid 1622; "Creating the ConfigManager", "[cfg] Regular config at .../hyprland.conf", "Using config: ..." | journal-hypr-filtered.txt (uwsm_hyprland.desktop[1622]) |
| 2026-10-26 12:08:39 | "Disabling stdout logs (debug.enable_stdout_logs = 0). Further logs will be written to /run/user/1000/hypr/efb5…_1793027319_436109330/hyprland.log" | journal line, same |
| 2026-10-26 12:08:39 (inferred) | `ConfigWatcher` created, one `setWatchList` pass: wd 1..40 in `m_configPaths` order | wd 1..40 contiguous in S1/S2/S3; order = plan n |
| 2026-10-26 12:08:40 | start-hyprland watchdog parent logs "got an event from hyprland" (1617) | journal |
| 2026-10-28 05:19:12 | pid 1622 stderr: "error marshalling arguments for leave (signature o): null value passed for arg 0" — a D-Bus/Wayland marshalling message, not a config event | journal (only post-start pid-1622 line besides startup) |
| 2026-10-28 22:50:25 -03 | S1 receipt (w2): 40 watches wd 1..40 at the same inodes | w2 fdinfo-capture.txt header |
| 2026-10-29 01:12:16, 01:22:11, 14:16:25, 14:18:12, 16:01:26, 16:26:47 | six "DEBUG from start-hyprland ]: got an event from hyprland" lines (watchdog parent 1617). Payload not logged; meaning NOT established (see section 8) | journal-hypr-filtered.txt |
| 2026-10-30 05:04:00Z | S2 sibling sample: wd 1..40 same inodes | comparison-a2.md |
| 2026-10-30 ~05:06Z | S3 (this seat): wd 1..40 same inodes; `hyprctl getoption` int 0 = AGREE | capture-a.json, getoption-a.json |

Process identity across the interval: same pid 1622, `lstart` unchanged (`Mon Oct 26 12:08:39 2026`), `hyprctl instances`: `instance efb50993…_1793027319_436109330: pid: 1622`. So there is no compositor restart between S1 and S3 and the inotify instance is the same.

## 7. Journal: what it shows and what it cannot show

- `journalctl --user -u Hyprland --no-pager` returns **no entries** (the sibling's `--since 2026-10-28` likewise). The compositor does not log under a unit named `Hyprland`; its lines carry `SYSLOG_IDENTIFIER=uwsm_hyprland.desktop`, `_PID=1622`. The `-u` query is therefore not evidence of anything: it would return nothing even if reloads were logged.
- The journal **cannot show config reloads**: at startup Hyprland disabled stdout logging (`debug.enable_stdout_logs = 0`), so the reload log line (`CConfigManager: file ... modified, reloading`, K18) and any `reload` message go to `/run/user/1000/hypr/<instance>/hyprland.log`, not to the journal. Absence of such lines in the journal is not evidence of absence of a reload.
- Journal lines for pid 1622 after startup: one (2026-10-28T05:19:12, the marshalling error above). Journal lines for `uwsm_hyprland.desktop[1617]` after startup: the six watchdog events.
- `journalctl --user -b 0 -t uwsm_hyprland.desktop` is the compositor's stdout identifier. Pid 1622 has nothing after its startup block except the 2026-10-28 marshalling line; pid 1617 (start-hyprland) has the six 2026-10-29 watchdog events.
- Coredumps: the boot journal's coredumps that I inspected are chromium, sasquatch-v4be, sim, probe and gcc16/clang23/bw12 builds. The hyprlang stack trace I read is from `probe`, not from pid 1622. I did not grep every coredump line for Hyprland; no Hyprland coredump is implied by any observed line, and pid 1622 is the same process throughout.

Omarchy scripts that call a reload (read under `~/.local/share/omarchy/bin`; their execution in the window is not recorded):
`omarchy-hyprland-monitor-internal:27` and `-mirror:33` (`hyprctl reload`), `omarchy-hyprland-toggle:32`, `omarchy-remove-preinstalls:13`, `omarchy-restart-hyprctl:5`, `omarchy-update-git:17`. Keyword calls that are not `misc:disable_autoreload` (`omarchy-hyprland-monitor-scaling-cycle`, `omarchy-hyprland-workspace-layout-toggle`, toggles) do not reach `update()` by the chain (K27 only covers that one option), so the table cannot show them and they are not excluded by it.

## 8. Unexplained (not resolved by allowed reads)

- Six watchdog-parent events on 2026-10-29 (and one on 10-26 12:08:40). The start-hyprland source is not pinned; the journal line does not say what the event is. If any were a reload, the table would have been rebuilt (section 5), and it was not; the most consistent reading is that they are not config reloads. This is an inference, not an observation.
- The decisive source — `hyprland.log` under `/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1793027319_436109330/` — would show `modified, reloading` and reload lines directly. It is outside the seat's allowed read set and was **not read**. Authorization to read it would close section 8.

## 9. Verdict

- Watch table (count 40, inodes 40/40, order by wd = predicted n, masks 0x8): identical across 2026-10-28 (S1), 2026-10-30 (S2) and 2026-10-30 (S3). Verified against the tool at `0f3a5436…` (identical bytes and identical output) and the working-path tool.
- The table was built once at process start and has never been rebuilt (wd never exceeds 40). Under the source chain, no reload reached the watcher since 2026-10-26 12:08:39, including the whole interval since 2026-10-28.
- Corroborated independently by: no watched file mtime/ctime after process start; every watched path's current inode equals its watched inode.
- The journal does not show reloads at all (stdout logs disabled); the `-u Hyprland` query is the wrong unit and returns nothing by construction.
