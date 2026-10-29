source: S383 (ConfigWatcher.cpp), S384 (ConfigValues.cpp), S385 (PropRefresher.cpp), S386 (EventLoopManager.cpp), S387 (legacy ConfigManager.cpp), S388 (MiscFunctions.cpp), S389 (HyprCtl.cpp), S390 (inotify(7) man page); host captures cited as `host` in the H rows: host-getoption.json, host-version.json, host-sources.txt
verified-at: 2026-10-28
recheck: on-release

# Hyprland 0.56.2 config auto-reload: source chain (MADO-R56-C1)

## Scope

Pins: `.ufo/waves/round-56/fetch/` at commit `efb50993780079460b0cbed1363e2166a2de1d9f` (Hyprland v0.56.2, the host build recorded in `host-version.json`). Every K and H row below is generated from `frozen-tables.json`; only the proposition cells are hand-written.

Settled at source level:
- the declaration of `misc:disable_autoreload` (Bool, default false) and what the flag does to the watch list;
- how `m_configPaths` is cleared, refilled and resolved: `resetHLConfig`, `handleSource`, glob, `~`, `./`, `../`, bare names, regular files, directories, non-regular files, recursion order, and what a `source` inside a nested file resolves against;
- which inotify masks each watch receives, and how an inotify event is routed to `CConfigManager::reload`.

UNKNOWN (stays open; nothing in this entry observes it): whether a filesystem event occurs when a config file is saved; whether Hyprland reloads on this host after a save; how an editor's write (in-place, truncate, rename, atomic save) reaches the watches; whether `REFRESH_ALL` carries the `REFRESH_CONFIG_WATCHER` bit that rebuilds the watch list. No reload, keyword, `hyprctl` state change or config write was made; the host was read only.

## Chain

1. **Declaration.** `misc:disable_autoreload` is a Bool with default false and refresh flag `Supplementary::REFRESH_CONFIG_WATCHER` (`Hyprland-ConfigValues.cpp:492`; K01, K02).
2. **Watch list.** `CConfigWatcher::update()` reads the cached value (`Hyprland-ConfigWatcher.cpp:33`; K03). A non-zero value passes an empty vector to `setWatchList`; otherwise it passes `Config::mgr()->getConfigPaths()` (line 34; K04). `getConfigPaths` returns `m_configPaths` (`Hyprland-legacy-ConfigManager.cpp:2133-2134`).
3. **Masks.** `setWatchList` removes every old watch (lines 45-47; K05), clears the list (49), then for each entry: `is_directory` (54; K06) selects the directory mask (56; K08, the file mask plus IN_CREATE, IN_DELETE, IN_MOVED_TO, IN_MOVED_FROM) or the file mask (55; K07, IN_CLOSE_WRITE | IN_DONT_FOLLOW). The watch is added at line 60 (K09). If the entry `is_symlink` (66) and `canonical` succeeded (65, 67; K10), a second watch on the canonical target with mask IN_CLOSE_WRITE is added (69; K11). That second watch carries the link path in its `file` field.
4. **Event loop.** `CEventLoopManager::enterLoop` registers the inotify descriptor as a readable Wayland source (`Hyprland-EventLoopManager.cpp:127-128`; K13). The callback `configWatcherWrite` calls `onInotifyEvent` (lines 70-71; K14). `CConfigWatcher::onInotifyEvent` (`Hyprland-ConfigWatcher.cpp:80-111`) reads the events, finds each watch by `wd` (line 100), and calls the stored callback with that watch's `file` (lines 102-107; K12, E03). The event `name` field is never read, so the reported path is the watch's stored path, not the name the kernel reports.
5. **Callback.** `CConfigManager::init` installs the change callback (`Hyprland-legacy-ConfigManager.cpp:1079-1082`; K17). It logs (K18) and calls `reload()`.
6. **Reload.** `reload()` (`legacy:726-751`) calls `resetHLConfig()` (line 731), parses (743), and calls `postConfigReload` (750). `postConfigReload` schedules a refresh with `REFRESH_ALL` (line 1070; K19).
7. **Refresh.** The prop refresher calls `Config::watcher()->update()` only when the `REFRESH_CONFIG_WATCHER` bit is set (`Hyprland-PropRefresher.cpp:148-149`; K15, K16). The pins do not show whether `REFRESH_ALL` sets that bit: UNKNOWN. If it does not, the watch list built by the previous refresh stays in place until some other `update()` call (inference).
8. **Other entry points.** A keyword that names `misc:disable_autoreload` calls `update()` at once (`Hyprland-HyprCtl.cpp:1223-1224`; K27). `hyprctl reload` reaches `Config::mgr()->reload()` (line 1276; K28).
9. **inotify semantics.** IN_CLOSE_WRITE is the event for a file opened for writing that was then closed (`man7-inotify.7.html:185-186`; K29). IN_DONT_FOLLOW says the pathname is not dereferenced when it is a symbolic link (lines 261-262; K30). Together these explain why a symlink entry gets a watch on the link and a second watch on its canonical target (step 3).

## The path list: how `m_configPaths` is built

Lifecycle:
- The constructor adds the main config path (`Hyprland-legacy-ConfigManager.cpp:485`) and calls `resetHLConfig()` (line 630; E05).
- `resetHLConfig()` (`legacy:764-786`) clears the list (776; K20), adds the main path (777-779), then runs `verifyConfigExists` and `reloadRuleConfigs`. Its callers in the pins are the constructor (630), `reload()` (731) and `verify()` (755). The list is rebuilt from nothing on every reload and verify; nothing is patched incrementally.
- `m_config->parse()` parses the main file. Each `source` keyword reaches `handleSource` through the handler registered at line 614 and the static wrapper at lines 359-369.

`handleSource` (`legacy:1802-1855`), in order:
1. RAW shorter than two bytes: error `bogus` (lines 1803-1806). Nothing is added. A lone `~` or `.` is therefore bogus.
2. Glob: `glob(absolutePath(RAW, cur), GLOB_TILDE, ...)` (line 1816; K24). Any non-zero result (no match, read error, out of memory) returns an error for the whole line (1817-1820). Nothing is added.
3. Matches are processed in the order glob returned them (line 1824). Each becomes `value = absolutePath(match, cur)` (1825; K21 is the append that follows). `std::filesystem::status(value, ec)` follows symlinks (1828). If it fails, for a missing target or a dangling symlink, the function returns "inaccessible" at once (1830-1833). The rest of that line's matches are not processed, and the failed entry is not added.
4. Regular file (1835; K22): `m_configPaths.emplace_back(value)` (1836) runs before the file is parsed. `m_configCurrentPath` is set to `value` (1838; E06), `parseFile(value)` runs (1839), and the previous `cur` is restored (1840). The recursion has no depth check in these lines.
5. Directory (1843-1845; K23): warning, skipped, not added and so not watched. Any other status, such as a fifo, socket or device, is also a warning and a skip (1846-1848).

Consequences. Each point is read from the lines above; the points marked inference are not shown directly.
- Order is depth-first and pre-order. The main path comes first. For each `source` line in file order, the matched file is appended, then its own nested entries follow, then the next `source` line is processed. Within one line the glob order decides.
- No deduplication. `emplace_back` at 1836 has no membership test, so a file reached twice is listed twice. `setWatchList` adds one watch per entry (52-73), so the same file is watched twice (inference from 52-73, which has no test either).
- A missing `source` target never enters the list. The nomatch return at 1816-1820 comes before the append at 1836. Only `m_configPaths` entries are watched, and no parent directory is ever watched, so a target created after the parse is not seen by the watcher (inference).
- A symlink to a regular file enters the list under the link path. `status` follows the link (1828) but `value` is not resolved. Its watches are the link watch and the canonical watch (step 3).
- A symlink to a directory is a directory match and is skipped (1843-1845).
- The main config path is added even when the file is missing (779). Its watch is then built by the same loop; the result of `inotify_add_watch` is not checked (line 60; E02).
- Cycles: no visited set and no depth limit appear in lines 1802-1855. A file that sources itself would recurse until the stack is exhausted (inference from the absent guard; not exercised).

Path resolution: `absolutePath` (`Hyprland-MiscFunctions.cpp:61-83`). `cur` is the file being parsed.
- `~`: the first byte is replaced by the value of `HOME` (lines 64-66; K25, E01). So `~/x` becomes `$HOME/x`, and `~user/x` becomes `$HOME` followed directly by `user/x`: there is no user lookup and no slash is inserted. The `GLOB_TILDE` flag (line 1816) never sees a leading tilde, because `absolutePath` has already replaced it. If `HOME` is unset, `getenv` returns null and the string construction at line 66 is undefined behaviour (source reading; not exercised).
- Leading `/`: unchanged.
- `./x`: `curdir` + `/x` (lines 74-75).
- `../x`: the parent of `curdir` + `/x` (lines 71-73).
- Other names starting with `.` (`.hidden`, `..x`, a bare `..`): `curdir` + `/` + RAW (line 77).
- Bare names: `curdir` + `/` + RAW (line 79).
- `curdir` is `cur` cut at its last `/` (line 68; K26). No normalisation is done: `.` and `..` segments already in `cur` stay as text, and no `realpath` appears in these lines.
- `$VAR` in RAW is not expanded by these lines. Whether hyprlang expands `$` before the handler runs is not in the pins: UNKNOWN.

Resolution base:
- Main config: `m_configCurrentPath` is set to the main path (`legacy:736` and `756`), so relative `source` lines in the main file resolve against the main file's directory, not the working directory.
- Nested file: while a nested file is parsed, `m_configCurrentPath` is that file's `value` path (1838; E06). A `source` inside it therefore resolves against the nested file's directory, not the main file's directory and not the working directory. The previous value is restored after the nested parse (1840).
- A symlinked nested file resolves against the link's directory, because `value` is the link path and is not canonicalised.

Host reads (read only; no write, no reload). `~/.config/hypr/hyprland.conf` holds 18 `source =` lines (`grep -c '^source'`). Its lines 4-12 name files under `~/.local/share/omarchy/default/hypr/` and line 13 names the theme file (H02's text). Nested: `~/.local/share/omarchy/default/hypr/envs.conf` line 3 sources `~/.config/omarchy/current/theme/gum.env.conf`, a `~` reference that the host's lstat capture (`host-watched-lstat.txt`) lists as a regular file.

Glob semantics: `glob(3)` is called without `GLOB_NOSORT`, so the match order is the C library's collation. The pins do not show that collation. The watch-plan model sorts bytewise; that is a declared divergence, not a fact of this entry. Whether a leading-dot name matches a `*` pattern is library behaviour and is not in the pins: UNKNOWN.

## Rows

Frozen anchors (K01-K30, one row per frozen quote; proposition is the bounded reading of that single line):

{{K_TABLE}}

Host captures (H01-H03; `host` is the source cell, the pin is the captured file):

{{H_TABLE}}

Extra rows (not counted; facts beyond the frozen anchors, each with its own pin line):

{{E_TABLE}}

## Limits

- Source level only. No filesystem event was generated, no inotify descriptor was read, no config file was saved, and no reload, keyword or `hyprctl` state change was made. Nothing here says that a save reloads Hyprland.
- Pins are the frozen single-line quotes plus the surrounding functions read from the pin files. Declarations outside the pins are UNKNOWN: `REFRESH_ALL` membership, the `m_configPaths` declaration, `ConfigWatcher.hpp`, `getMainConfigPath`, `Supplementary::Jeremy`, hyprlang's `parseFile` and `source` pre-processing, comment stripping before the handler, and the Lua config provider.
- Failure paths: if `inotify_init1` fails, the constructor logs and returns (`Hyprland-ConfigWatcher.cpp:21-26`), and the event loop does not register a descriptor (`Hyprland-EventLoopManager.cpp:127`). A failed `inotify_add_watch` is not checked (line 60; E02). `onInotifyEvent` has no `IN_Q_OVERFLOW` branch.
- Reload per event: `onInotifyEvent` calls the callback once per event (lines 87-110). No coalescing appears, so one save that produces several events could call `reload()` several times (inference; no save observed).
- Inode-based watches: inotify(7) says file monitoring follows the inode (`man7-inotify.7.html:225-228`). An editor that replaces a file by rename would leave the old inode's watch behind (inference from the man page; not observed).
- Runtime `source` keyword: `hyprctl keyword source <path>` reaches `parseKeyword` (E04). That `parseDynamic` then invokes the registered `handleSource` handler (line 614) is inference: `parseDynamic` is not in the pins. The handler appends to `m_configPaths` without clearing it (1836). The `source` branch of the keyword dispatcher (`Hyprland-HyprCtl.cpp:1194-1208`) does not call the watcher's `update()`, so the new path is not watched until a later `update()` call (inference from the branch; not run).
- Host records: H01 and H03 are captures from this host; they show values at capture time, not reload behaviour. H02 is a line of a captured listing; the live file's line 13 holds the same text.
- The watch-plan model's declared divergences (depth cap 16, bytewise glob order, `~user` forms, Lua provider, runtime keyword) belong to that tool and are not facts of this entry.
- Not checked: `HOME` unset, the `full-reset` branch of `reloadRequest` (`Hyprland-HyprCtl.cpp:1262-1274`), and the tail of `verify()`.

## How to verify (read-only)

```bash
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
REV=$(git -C "$LANE" rev-parse HEAD)
# frozen tables and pins at the revision (never the working tree)
git -C "$LANE" show "$REV:.ufo/waves/round-56/frozen-tables.json" | sha256sum    # expect d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af
git -C "$LANE" ls-tree -r --name-only "$REV" -- .ufo/waves/round-56/fetch/ | head -20
# quote spot checks (each line must contain the frozen quote)
git -C "$LANE" show "$REV:.ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp" | sed -n '33,34p;54,56p;60p;67p;69p;105p'
git -C "$LANE" show "$REV:.ufo/waves/round-56/fetch/Hyprland-legacy-ConfigManager.cpp" | sed -n '776p;1816p;1835,1836p;1844p;1838p'
git -C "$LANE" show "$REV:.ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp" | sed -n '64,66p;68p'
# handleSource and absolutePath bodies
git -C "$LANE" show "$REV:.ufo/waves/round-56/fetch/Hyprland-legacy-ConfigManager.cpp" | sed -n '1802,1855p'
git -C "$LANE" show "$REV:.ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp" | sed -n '61,83p'
# host, read only
hyprctl getoption misc:disable_autoreload -j
hyprctl version -j | sed -n '3p'
stat -c '%F %n' ~/.config/hypr/hyprland.conf
grep -c '^source' ~/.config/hypr/hyprland.conf
# counter and harness of the round: the C1 counter is the wave's deliverable and is run only where it exists at REV
python3 -I "$LANE/quality/counters/c1-r56-autoreload-entry.py" --repo "$LANE" --rev "$REV" --work "$(mktemp -d)"
```

