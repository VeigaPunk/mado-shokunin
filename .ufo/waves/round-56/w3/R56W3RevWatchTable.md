# R56W3RevWatchTable — running compositor watch table, attempt 2

## Attacked

Item: reconstruct the live inotify watch table of Hyprland pid 1622, compare it with both prior samples (w2 on 2026-10-28, the sibling R56W3RevProcFdinfo on 2026-10-30), explain how the table got its present shape, and state whether a reload since 2026-10-28 would have rewritten it and whether the journal shows one. Read-only. Nothing signalled, reloaded, restarted or written outside my deliverable directory and scratch.

Axes: coverage of the watch list (count, inodes, order), temporal stability, the reload-rewrite mechanism, journal evidence.

## Findings, by severity

1. **Weakens (sibling evidence): the journal query is the wrong unit and cannot show reloads.** `journalctl --user -u Hyprland --no-pager` returns no entries for any time (`-- No entries --`), because the compositor logs under `SYSLOG_IDENTIFIER=uwsm_hyprland.desktop`, `_PID=1622`. Separately, Hyprland disabled stdout logging at startup (`Disabling stdout logs (debug.enable_stdout_logs = 0). Further logs will be written to /run/user/1000/hypr/.../hyprland.log`), so reload lines (K18, `file ... modified, reloading`) never reach the journal. The sibling's `journal.txt` "no entries" must not be cited as evidence that no reload happened. The table is the evidence that carries this claim (below).
2. **Weakens (open item): six watchdog events on 2026-10-29 are unexplained.** `uwsm_hyprland.desktop[1617]: DEBUG from start-hyprland ]: got an event from hyprland` at 01:12:16, 01:22:11, 14:16:25, 14:18:12, 16:01:26, 16:26:47 (-03). Payload is not logged and the start-hyprland source is not pinned. The table argument below excludes them as reloads (a reload rebuilds the table), but only through the source chain. If that chain were wrong for these events, the conclusion "no reload since 2026-10-26" would fail. Closing this needs `hyprland.log` under `/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1793027319_436109330/`, which is outside this seat's allowed read set and was not read.
3. **Cosmetic (sibling report): "two descriptors, may be duplicates [INFERENCE]" is now a fact.** `/proc/1622/fdinfo/12` and `/proc/1622/fdinfo/86` both carry `pos:0 flags:02004000 mnt_id:19 ino:1094`, so they are one open file description and one inotify instance.
4. **No defect found in the pinned tool.** `tools/mado-watchplan.py` at the working path and at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` are byte-identical (sha256 `3ccf070841b3c0134a05f612a35e553364f318a9d36843455f4207df118f22b7`), give byte-identical output on the live config, `--selftest` gives `86/86 assertions passed`, and the `--getoption` join gives `AGREE`.
5. **No defect found in the three-sample agreement.** 40/40 watches at the same wd, the same inode and the same order in all three samples and in the current `lstat`.

## Observed result

- Hyprland pid 1622, `ps lstart` Mon Oct 26 12:08:39 2026 -03, unchanged for the whole interval (`hyprctl instances`: `pid: 1622`).
- One inotify instance: fds 12 and 86 (same open file description, `ino:1094`), each with 40 rows: wd 1..40 distinct, every mask `0x8` (IN_CLOSE_WRITE), ignored 0.
- The pinned tool predicts 40 primary watches, 0 canonical, `unsupported=0 errors=0`. wd k = predicted n k, inode for inode, for k = 1..40 (`receipts/table.md`, `ALL_MATCH True`).
- Against S1 (w2, 2026-10-28): identical 40/40, wd, inode and order. Against S2 (sibling, 2026-10-30 05:04:00Z): identical 40/40. Against the current `lstat` of each path: identical 40/40.
- `hyprctl getoption misc:disable_autoreload -j` → `int: 0`; the config has no value, so `verdict=AGREE`.
- Max mtime and max ctime across the 40 watched paths: 2026-10-17 17:05:14 -03, before process start. Each watched path's current inode equals its watched inode, so no watched file was replaced since the watches were built.

## Exact commands and decisive outputs

```text
pgrep -a Hyprland                          -> 1622 Hyprland --watchdog-fd 4
ps -o pid=,uid=,lstart=,etime=,comm= -p 1622  -> 1622 1000 Mon Oct 26 12:08:39 2026 ... Hyprland
ls -l /proc/1622/fd | grep inotify         -> 12 -> anon_inode:inotify ; 86 -> anon_inode:inotify
python3 -I receipts/capture.py 1622 > receipts/capture-a.json
    fd 12: 40 rows, wd 1..40 distinct, masks ['8'], ignored ['0']
    fd 86: 40 rows, wd 1..40 distinct, masks ['8'], ignored ['0']
grep -E '^(pos|flags|mnt_id|ino):' /proc/1622/fdinfo/12 /proc/1622/fdinfo/86
    ino: 1094 (both)
python3 -I tools/mado-watchplan.py --config /home/vgpnk/.config/hypr/hyprland.conf --home /home/vgpnk > receipts/plan-a.txt
    MADO_WATCH: config=/home/vgpnk/.config/hypr/hyprland.conf autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0
    MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=NONE
hyprctl getoption misc:disable_autoreload -j  -> {"option": "misc:disable_autoreload", "int": 0, "set": false }
python3 -I tools/mado-watchplan.py ... --getoption getoption-a.json
    MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE
    MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:tools/mado-watchplan.py > /fast/scratch/hyaku/mado-r56/R56W3RevWatchTable/mado-watchplan.at-0f3a.py   (read-only git)
sha256sum (both)  -> 3ccf070841b3c0134a05f612a35e553364f318a9d36843455f4207df118f22b7 (both)
cmp plan-a.txt plan-at-0f3a.txt -> identical
python3 -I tools/mado-watchplan.py --selftest -> MADO_WATCH_SELFTEST: 86/86 assertions passed
hyprctl version -j -> "version": "0.56.2", "commit": "efb50993780079460b0cbed1363e2166a2de1d9f", "dirty": false
hyprctl instances -> instance efb50993780079460b0cbed1363e2166a2de1d9f_1793027319_436109330: time 1793027319, pid 1622, wl socket wayland-1
stat / lstat of the 40 predicted paths -> receipts/lstat-a.json: max mtime 2026-10-17 17:05:14 -03, max ctime same; NONE after process start
journalctl --user -u Hyprland --no-pager                     -> -- No entries --
journalctl --user -b 0 --no-pager _PID=1622 -o short-iso    -> 52 lines; startup block 2026-10-26T12:08:39; the only later line is 2026-10-28T05:19:12 "error marshalling arguments for leave (signature o): null value passed for arg 0"
journalctl --user -b 0 -o short-iso | grep 'Disabling stdout' -> uwsm_hyprland.desktop[1622]: DEBUG ]: Disabling stdout logs (debug.enable_stdout_logs = 0). Further logs will be written to /run/user/1000/hypr/efb5..._436109330/hyprland.log
journalctl ... -t uwsm_hyprland.desktop / start-hyprland watchdog 1617 -> six "got an event from hyprland" on 2026-10-29 (listed in finding 2)
```

Wd-allocation test (the reload-rewrite question). A private inotify instance on 40 scratch files in `/fast/scratch/hyaku/mado-r56/R56W3RevWatchTable/`, run with `python3 -I` and ctypes (`inotify_init1`, `inotify_add_watch` with `IN_CLOSE_WRITE|IN_DONT_FOLLOW`, `inotify_rm_watch`), then removed:

```text
first build wds: [1..40]  max 40 count 40 distinct 40
rm rc all zero: True
rebuild wds: [41..80]  min 41 max 80
rebuild wds disjoint from first build: True
re-add of an already-watched inode returns existing wd: [41] == second[0] 41 True
rm of already-removed wd rc: -1 errno 22
uname -r: 7.2.11-arch1-1
```

Reading: a `setWatchList` pass (remove 40, re-add 40) on this kernel would leave the table at wd 41..80. The live table is at wd 1..40 in S1, S2 and S3. Therefore, under the entry's chain (`reload` → `REFRESH_ALL` → `update()` → `setWatchList`, steps 6–7), no reload has reached the watcher since the table was built at process start on 2026-10-26 12:08:39. Limit: the Hyprland half of that chain is source-level inference and is not observed at runtime; the kernel half is tested.

## How the table got its present shape

1. 2026-10-26 12:08:39 -03: start-hyprland → Hyprland pid 1622. ConfigManager reads `/home/vgpnk/.config/hypr/hyprland.conf` (journal: `[cfg] Regular config`, `Using config`).
2. ConfigWatcher is created and one `setWatchList` pass registers the 40 entries of `m_configPaths` in order (main file first, then depth-first). Registration order = wd order = predicted n. This pass is inferred (no journal line for it); its signature is the contiguous wd 1..40 with the correct inode order.
3. No later pass has happened: a later pass would have produced wd 41+. The three samples show the same wd 1..40 on 2026-10-28 22:50 -03 (S1), 2026-10-30 05:04Z (S2) and 2026-10-30 ~05:06Z (S3).
4. Nothing in the journal changes the table: the only post-startup pid-1622 line is the 2026-10-28 D-Bus/Wayland marshalling error, not a config event.

## Timeline

Summarised in `receipts/watchtable-a2.md` section 6 (2026-10-03..10-17 last file writes; 2026-10-26 12:08:39 start; 2026-10-28 05:19:12 marshalling error; 2026-10-28 22:50 S1; 2026-10-29 six watchdog events; 2026-10-30 05:04Z S2; 2026-10-30 ~05:06Z S3).

## Could not verify

- Whether any reload happened: not observable in the journal (stdout logs disabled). The decisive log (`hyprland.log` under `/run/user/1000/hypr/...`) is outside the allowed read set and was not read.
- The payload and meaning of the six `start-hyprland` watchdog events of 2026-10-29 (finding 2).
- The runtime form of chain step 7 (`reload` → `update()`) in this build; only the kernel allocation half was exercised.
- Whether any `omarchy-*` script that calls `hyprctl reload` ran in the window (scripts located and read under `~/.local/share/omarchy/bin`; their execution is not recorded).
- `hyprctl keyword` calls other than `misc:disable_autoreload` do not reach the watcher by the chain, so the table cannot show them.

## Tools installed or updated

None. No install, upgrade or package operation was run.

## Deliverables

All under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevWatchTable/receipts/`:

- `watchtable-a2.md` — comparison (three samples) and timeline, reload analysis, journal analysis, unexplained items.
- `table.md` — 40-row wd / n / path / inode table across S1, S2, S3 and current lstat, `ALL_MATCH True`.
- `capture.py`, `capture-a.json` — live fdinfo capture (fd 12, fd 86).
- `plan-a.txt`, `plan-at-0f3a.txt`, `getoption-a.json`, `lstat-a.json` — tool output at the working path and at 0f3a; the live option; per-path lstat.
- `journal-pid1622.txt`, `journal-hypr-filtered.txt` — journal windows for pid 1622 and the uwsm/start-hyprland identifiers.

Scratch `/fast/scratch/hyaku/mado-r56/R56W3RevWatchTable/` is removed after these copies.

## Self-evaluation

Accuracy: the watch table, the three-sample comparison and the tool outputs were checked by machine and reproduce. The reload conclusion depends on a source-level chain that is not observed at runtime; that is stated as a limit. Completeness: all requested steps ran; the decisive reload log was not read because it is outside the allowed reads. Clarity: findings are separated from inferences. Calibration: "no reload since start" is conditional on the chain; "table never rebuilt since start" is observed.
