source: S383 (ConfigWatcher.cpp), S384 (ConfigValues.cpp), S385 (PropRefresher.cpp), S386 (EventLoopManager.cpp), S387 (legacy ConfigManager.cpp), S388 (MiscFunctions.cpp), S389 (HyprCtl.cpp), S390 (inotify(7) man page), S391 (PropRefresher.hpp), S392-S395 (extra-row anchors for E01, E03-E07); host captures cited as `host` in the H rows: host-getoption.json, host-version.json, host-sources.txt
verified-at: 2026-10-28
recheck: on-release

# Hyprland 0.56.2 config auto-reload: source chain (MADO-R56-C1)

## Scope

Pins: `.ufo/waves/round-56/fetch/` at commit `efb50993780079460b0cbed1363e2166a2de1d9f` (Hyprland v0.56.2, the host build recorded in `host-version.json`). Every K and H row below is generated from `frozen-tables-v2.json`; only the proposition cells are hand-written.

Settled at source level:
- the declaration of `misc:disable_autoreload` (Bool, default false) and what the flag does to the watch list;
- how `m_configPaths` is cleared, refilled and resolved: `resetHLConfig`, `handleSource`, glob, `~`, `./`, `../`, bare names, regular files, directories, non-regular files, recursion order, and what a `source` inside a nested file resolves against;
- which inotify masks each watch receives, and how an inotify event is routed to `CConfigManager::reload`.

UNKNOWN (stays open; nothing in this entry observes it): whether Hyprland reloads on this host after a save; what a given editor's save sequence does to these watches in the running compositor. The mask plane is partly answered: an in-place or truncating write closes a file opened for writing, which is the IN_CLOSE_WRITE event of K29 (the wave-1 lab saw one event per save on kernel 7.2.11, `w1/R56ScoutInotifyLab.md`). No reload, keyword, `hyprctl` state change or config write was made; the host was read only.

## Chain

1. **Declaration.** `misc:disable_autoreload` is a Bool with default false and refresh flag `Supplementary::REFRESH_CONFIG_WATCHER` (`Hyprland-ConfigValues.cpp:492`; K01, K02).
2. **Watch list.** `CConfigWatcher::update()` reads the cached value (`Hyprland-ConfigWatcher.cpp:33`; K03). A non-zero value passes an empty vector to `setWatchList`; otherwise it passes `Config::mgr()->getConfigPaths()` (line 34; K04). `getConfigPaths` returns `m_configPaths` (`Hyprland-legacy-ConfigManager.cpp:2133-2134`).
3. **Masks.** `setWatchList` removes every old watch (lines 45-47; K05), clears the list (49), then for each entry: `is_directory` (54; K06) feeds the selection at line 57 (`isDirectory ? directoryMask : fileMask`) between the directory mask (56; K08, the file mask plus IN_CREATE, IN_DELETE, IN_MOVED_TO, IN_MOVED_FROM) and the file mask (55; K07, IN_CLOSE_WRITE | IN_DONT_FOLLOW). The watch is added at line 60 (K09). If the entry `is_symlink` (66) and `canonical` succeeded (65, 67; K10), a second watch on the canonical target with mask IN_CLOSE_WRITE is added (69; K11). That second watch carries the link path in its `file` field.
4. **Event loop.** `CEventLoopManager::enterLoop` registers the inotify descriptor as a readable Wayland source (`Hyprland-EventLoopManager.cpp:127-128`; K13). The callback `configWatcherWrite` calls `onInotifyEvent` (lines 70-71; K14). `CConfigWatcher::onInotifyEvent` (`Hyprland-ConfigWatcher.cpp:80-111`) reads the events, finds each watch by `wd` (line 100), and calls the stored callback with that watch's `file` (lines 102-107; K12, E03). The event `name` field is never read, so the reported path is the watch's stored path, not the name the kernel reports.
5. **Callback.** `CConfigManager::init` installs the change callback (`Hyprland-legacy-ConfigManager.cpp:1079-1082`; K17). It logs (K18) and calls `reload()`.
6. **Reload.** `reload()` (`legacy:726-751`) calls `resetHLConfig()` (line 731), parses (743), and calls `postConfigReload` (750). `postConfigReload` schedules a refresh with `REFRESH_ALL` (line 1070; K19).
7. **Refresh.** The prop refresher calls `Config::watcher()->update()` only when the `REFRESH_CONFIG_WATCHER` bit is set (`Hyprland-PropRefresher.cpp:148-149`; K15, K16). `REFRESH_CONFIG_WATCHER` is bit 8 (`Hyprland-PropRefresher.hpp:18`; E08) and `REFRESH_ALL` is the maximum of the 16-bit underlying type (`Hyprland-PropRefresher.hpp:21`; E09), so it contains that bit (arithmetic on the two declarations); `scheduleRefresh` ORs its argument into `m_propsTripped` (`Hyprland-PropRefresher.cpp:31`) and, only when no refresh is already scheduled (`m_scheduled`, lines 33-40) and an event-loop manager exists, queues the refresh with `doLater` (34); refreshes can therefore coalesce. The watch list is rebuilt when a queued refresh runs, from the then-current `m_configPaths` (inference from these lines; no reload was observed).
8. **Other entry points.** A keyword that names `misc:disable_autoreload` calls `update()` at once (`Hyprland-HyprCtl.cpp:1223-1224`; K27). `hyprctl reload` reaches `Config::mgr()->reload()` (line 1276; K28).
9. **inotify semantics.** IN_CLOSE_WRITE is the event for a file opened for writing that was then closed (`man7-inotify.7.html:185-186`; K29). IN_DONT_FOLLOW says the pathname is not dereferenced when it is a symbolic link (lines 261-262; K30). Read together with step 3 they say what the two watches on a symlink entry cover: the link watch is on the link itself (IN_DONT_FOLLOW), the second watch is on the target; the wave-1 lab saw the link watch silent for a write through the link and the target watch fire (`w1/R56ScoutInotifyLab.md`). Why Hyprland added the second watch is its authors' design intent and is not in any pin.

## The path list: how `m_configPaths` is built

Lifecycle:
- The constructor adds the main config path (`Hyprland-legacy-ConfigManager.cpp:485`) and calls `resetHLConfig()` (line 630; E05).
- `resetHLConfig()` (`legacy:764-786`) clears the list (776; K20), adds the main path (777-779), then runs `verifyConfigExists` and `reloadRuleConfigs`. Its callers in the pins are the constructor (630), `reload()` (731) and `verify()` (755). The list is rebuilt from nothing on every reload and verify; nothing is patched incrementally.
- `m_config->parse()` parses the main file. Each `source` keyword reaches `handleSource` through the handler registered at line 614 and the static wrapper at lines 359-369.

`handleSource` (`legacy:1802-1855`), in order:
1. RAW shorter than two bytes: error `bogus` (lines 1803-1806). Nothing is added. A lone `~` or `.` is therefore bogus.
2. Glob: `glob(absolutePath(RAW, cur), GLOB_TILDE, ...)` (line 1816; K24). Any non-zero result (no match, read error, out of memory) returns an error for the whole line (1817-1820). Nothing is added.
3. Matches are processed in the order glob returned them (line 1824). Each becomes `value = absolutePath(match, cur)` (1825; K21 is the append that follows). `std::filesystem::status(value, ec)` follows symlinks (1828). If it fails — for example for a dangling symlink that glibc returns as a match (observed by the wave-2 prose audit, `w2/R56W2RevProsePath.md` P13), or for a match removed between the glob and the status call, or for any other status error; the pins do not exclude other causes — the function returns "inaccessible" at once (1830-1833). A missing literal target never gets here: it ends at the no-match return of step 2. The rest of that line's matches are not processed, and the failed entry is not added.
4. Regular file (1835; K22): `m_configPaths.emplace_back(value)` (1836) runs before the file is parsed. `m_configCurrentPath` is set to `value` (1838; E06), `parseFile(value)` runs (1839), and the previous `cur` is restored (1840). The recursion has no depth check in these lines.
5. Directory (1843-1845; K23): warning, skipped, not added and so not watched. Any other status, such as a fifo, socket or device, is also a warning and a skip (1846-1848).

Consequences. Each point is read from the lines above; the points marked inference are not shown directly.
- Order is depth-first and pre-order. The main path comes first. For each `source` line in file order, the matched file is appended, then its own nested entries follow, then the next `source` line is processed. Within one line the glob order decides.
- No deduplication. `emplace_back` at 1836 has no membership test, so a file reached twice is listed twice. `setWatchList` records one `m_watches` entry per list entry (52-73), so the same file appears twice in `m_watches`; the kernel keeps one watch per inode, the second add returns the same descriptor and modifies the watch (inotify(7) lines 90-92 and 296-302; the wave-2 prose audit saw wd 1 returned three times), and the duplicate `inotify_rm_watch` of the next rebuild fails unchecked (K05).
- A missing `source` target never enters the list. The nomatch return at 1816-1820 comes before the append at 1836. Only `m_configPaths` entries are watched, and no parent directory is ever watched, so a target created after the parse is not seen by the watcher (inference).
- A symlink to a regular file enters the list under the link path. `status` follows the link (1828) but `value` is not resolved. Its watches are the link watch and the canonical watch (step 3).
- A symlink to a directory is a directory match and is skipped (1843-1845).
- The main config path is added even when the file is missing (779). Its watch is then built by the same loop; the result of `inotify_add_watch` is not checked (line 60; E02).
- Cycles: no visited set and no depth limit appear in lines 1802-1855. A file that sources itself would recurse without a bound, and each level also appends one list entry (1836), so the growth is stack and heap; which gives out first is not in the pins (inference from the absent guard; not exercised).

Path resolution: `absolutePath` (`Hyprland-MiscFunctions.cpp:61-83`). `cur` is the file being parsed.
- `~`: the first byte is replaced by the value of `HOME` (lines 64-66; K25, E01). So `~/x` becomes `$HOME/x`, and `~user/x` becomes `$HOME` followed directly by `user/x`: there is no user lookup and no slash is inserted. The `GLOB_TILDE` flag (line 1816) never sees a leading tilde, because `absolutePath` has already replaced it. If `HOME` is unset, `getenv` returns null and the string construction at line 66 violates the `std::string` precondition; libstdc++ throws `std::logic_error` (observed in the wave-2 prose audit, R06), and `handleSource` has no catch in 1802-1855. What Hyprland's own build does is not in the pins.
- Leading `/`: unchanged.
- `./x`: `curdir` + `/x` (lines 74-75).
- `../x`: the parent of `curdir` + `/x` (lines 71-73).
- Other names starting with `.` (`.hidden`, `..x`, a bare `..`): `curdir` + `/` + RAW (line 77).
- Bare names: `curdir` + `/` + RAW (line 79).
- `curdir` is `cur` cut at its last `/` (line 68; K26). No normalisation is done: `.` and `..` segments already in `cur` stay as text, and no `realpath` appears in these lines.
- `$VAR` in RAW is not expanded by these lines. Hyprlang (the round-46 pin `.ufo/waves/round-46/fetch/hyprlang-config.cpp`, byte-identical to v0.6.8, the host's `buildHyprlang`) replaces `$NAME` in a value with environment variables and earlier `$NAME = ...` lines before the handler runs (that file lines 737-745 and 872); this round's pins do not show that the running Hyprland links that version.

Resolution base:
- Main config: `m_configCurrentPath` is set to the main path (`legacy:736` and `756`), so relative `source` lines in the main file resolve against the main file's directory, not the working directory.
- Nested file: while a nested file is parsed, `m_configCurrentPath` is that file's `value` path (1838; E06). A `source` inside it therefore resolves against the nested file's directory, not the main file's directory and not the working directory. The previous value is restored after the nested parse (1840).
- A symlinked nested file resolves against the link's directory, because `value` is the link path and is not canonicalised.

Host reads (read only; no write, no reload). `~/.config/hypr/hyprland.conf` holds 18 `source =` lines (`grep -c '^source'`). Its lines 4-12 name files under `~/.local/share/omarchy/default/hypr/` and line 13 names the theme file (H02's text). Nested: `~/.local/share/omarchy/default/hypr/envs.conf` line 3 sources `~/.config/omarchy/current/theme/gum.env.conf`, a `~` reference that the host's lstat capture (`host-watched-lstat.txt`) lists as a regular file.

Glob semantics: `glob(3)` is called without `GLOB_NOSORT`, so the matches are sorted by the libc's `strcoll`-style order: bytewise under the C locale and locale-dependent otherwise (glibc, observed by the wave-2 prose audit, G02). Whether Hyprland calls `setlocale` and which libc it links are not in the pins. The watch-plan model sorts bytewise; that is a declared divergence, not a fact of this entry. For glibc a `*` pattern does not return a leading-dot name and a `.*` pattern returns `.`, `..` and the dot-file (observed, G05); the model's python glob omits `.` and `..`.

## Rows

Frozen anchors (K01-K30, one row per frozen quote; proposition is the bounded reading of that single line):

| id | proposition | src | pin:line | quote |
|---|---|---|---|---|
| K01 | The misc:disable_autoreload option is declared as a Bool with help text saying the config will not reload automatically on save, with false as its third argument; what that argument means (the default) is not shown by the pinned line. | S384 | Hyprland-ConfigValues.cpp:492 | `"misc:disable_autoreload", "If true, the config will not reload automatically on save.", false` |
| K02 | The declaration sets its refresh field to the flag Supplementary::REFRESH_CONFIG_WATCHER on this line. | S384 | Hyprland-ConfigValues.cpp:492 | `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}` |
| K03 | The update function caches the misc:disable_autoreload option as a CConfigValue of the INTEGER type on this line. | S383 | Hyprland-ConfigWatcher.cpp:33 | `CConfigValue<Config::INTEGER>("misc:disable_autoreload");` |
| K04 | When the cached PDISABLEAUTORELOAD value is non-zero, setWatchList is given an empty vector; otherwise it is given the getConfigPaths() result. | S383 | Hyprland-ConfigWatcher.cpp:34 | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` |
| K05 | This loop calls inotify_rm_watch once per watch-list entry with that entry's wd and does not check the return value, so a wd listed twice is removed twice and the second call fails (inference from the inotify man page). | S383 | Hyprland-ConfigWatcher.cpp:46 | `inotify_rm_watch(m_inotifyFd.get(), watch.wd);` |
| K06 | This line calls std::filesystem::is_directory on path and passes the error code ecDir to it. | S383 | Hyprland-ConfigWatcher.cpp:54 | `std::filesystem::is_directory(path, ecDir);` |
| K07 | The fileMask variable is assigned the IN_CLOSE_WRITE inotify event bit in this declaration; the same source line also ORs in IN_DONT_FOLLOW, which the quoted prefix does not show. | S383 | Hyprland-ConfigWatcher.cpp:55 | `fileMask      = IN_CLOSE_WRITE` |
| K08 | The directoryMask variable is initialised from fileMask on this line and, on the same source line, ORs in IN_CREATE, IN_DELETE, IN_MOVED_TO and IN_MOVED_FROM, which the quoted prefix does not show. | S383 | Hyprland-ConfigWatcher.cpp:56 | `directoryMask = fileMask` |
| K09 | This line calls inotify_add_watch on path.c_str() with the mask variable on the m_inotifyFd inotify instance and stores the returned descriptor. | S383 | Hyprland-ConfigWatcher.cpp:60 | `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |
| K10 | This condition requires both error codes to be clear and IS_SYMLINK to hold. | S383 | Hyprland-ConfigWatcher.cpp:67 | `if (!ec && !ec2 && IS_SYMLINK) {` |
| K11 | A watch is added on CANONICAL.c_str() with IN_CLOSE_WRITE as the only mask argument. | S383 | Hyprland-ConfigWatcher.cpp:69 | `inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE),` |
| K12 | On this line the event handler calls m_watchCallback with a newly built SConfigWatchEvent; the matching condition that guards this call is the preceding lines'. | S383 | Hyprland-ConfigWatcher.cpp:105 | `m_watchCallback(SConfigWatchEvent{` |
| K13 | This line registers the FD descriptor with the Wayland event loop as a readable source that calls configWatcherWrite. | S386 | Hyprland-EventLoopManager.cpp:128 | `m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` |
| K14 | On this line the event-loop callback calls onInotifyEvent on the watcher returned by Config::watcher() with no arguments; the callback passes none of its fd, mask or data arguments on. | S386 | Hyprland-EventLoopManager.cpp:71 | `Config::watcher()->onInotifyEvent();` |
| K15 | The guard enters its branch only when the m_propsTripped bit mask contains REFRESH_CONFIG_WATCHER. | S385 | Hyprland-PropRefresher.cpp:148 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` |
| K16 | The guarded statement calls update on the object returned by Config::watcher(); that function's body lives in ConfigWatcher.cpp and is not pinned by this row. | S385 | Hyprland-PropRefresher.cpp:149 | `Config::watcher()->update();` |
| K17 | The init function registers a change callback with setOnChange on the config watcher, taking an SConfigWatchEvent argument. | S387 | Hyprland-legacy-ConfigManager.cpp:1079 | `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {` |
| K18 | The debug line logs a reload message for the modified config file and passes the event's file field as its argument. | S387 | Hyprland-legacy-ConfigManager.cpp:1080 | `CConfigManager: file {} modified, reloading` |
| K19 | This line schedules a refresh with the flag REFRESH_ALL on the Supplementary refresher. | S387 | Hyprland-legacy-ConfigManager.cpp:1070 | `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` |
| K20 | resetHLConfig empties the m_configPaths list on this line, discarding the previous list. | S387 | Hyprland-legacy-ConfigManager.cpp:776 | `m_configPaths.clear();` |
| K21 | This line appends value to m_configPaths with emplace_back; the regular-file guard, the parse order and the skipped branches are established by the surrounding handleSource lines, not this line alone. | S387 | Hyprland-legacy-ConfigManager.cpp:1836 | `m_configPaths.emplace_back(value);` |
| K22 | This condition tests file_status with std::filesystem::is_regular_file, the regular-file branch of handleSource. | S387 | Hyprland-legacy-ConfigManager.cpp:1835 | `if (std::filesystem::is_regular_file(file_status)) {` |
| K23 | The warning logged on this line says the source= match value is skipped because it is a directory. | S387 | Hyprland-legacy-ConfigManager.cpp:1844 | `"source= skipping directory {}", value);` |
| K24 | The glob call takes absolutePath of rawpath resolved against m_configCurrentPath and the GLOB_TILDE flag. | S387 | Hyprland-legacy-ConfigManager.cpp:1816 | `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())` |
| K25 | The static ENVHOME pointer takes its value from getenv of the HOME variable on this line. | S388 | Hyprland-MiscFunctions.cpp:65 | `static const char* const ENVHOME = getenv("HOME");` |
| K26 | currentDir is the currentPath text cut with substr at its last slash found by find_last_of on this line. | S388 | Hyprland-MiscFunctions.cpp:68 | `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` |
| K27 | The keyword dispatch guard tests whether COMMAND contains the misc:disable_autoreload text; when it does, the next line calls Config::watcher()->update(). The quoted line does not show that body. | S389 | Hyprland-HyprCtl.cpp:1223 | `if (COMMAND.contains("misc:disable_autoreload"))` |
| K28 | The reload request handler calls reload on the object returned by Config::mgr() on this line. | S389 | Hyprland-HyprCtl.cpp:1276 | `Config::mgr()->reload();` |
| K29 | The description text says a file opened for writing and then closed produces this event, the write-close case. | S390 | man7-inotify.7.html:186 | `File opened for writing was closed.` |
| K30 | The description says the pathname is not dereferenced when it is a symbolic link. | S390 | man7-inotify.7.html:262 | `Don't dereference <i>pathname</i> if it is a symbolic link.` |

Host captures (H01-H03; `host` is the source cell, the pin is the captured file):

| id | proposition | src | pin:line | quote |
|---|---|---|---|---|
| H01 | The captured hyprctl getoption record reports misc:disable_autoreload with an int value of zero on this host. | host | host-getoption.json:1 | `"option": "misc:disable_autoreload", "int": 0` |
| H02 | The captured host source list names the omarchy theme file hyprland.conf as a source line target. | host | host-sources.txt:10 | `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| H03 | The captured version record gives the commit field of the running Hyprland build on this host. | host | host-version.json:3 | `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"` |

Extra rows (not counted; facts beyond the frozen anchors, each with its own pin line):

| id | proposition | src | pin:line | quote |
|---|---|---|---|---|
| E01 | This call replaces one byte at offset zero of value with std::string(ENVHOME); the complete function contains no user lookup, so the resolution of a ~user prefix is not modelled by any pinned line. | S393 | Hyprland-MiscFunctions.cpp:66 | `value.replace(0, 1, std::string(ENVHOME));` |
| E02 | The return value of inotify_add_watch is stored unchecked in the .wd field of the SInotifyWatch emplaced into m_watches; the function never tests it, so a failed add (for example a missing path) still leaves an entry whose .wd is -1. Whether a later event can match such an entry is not decided by the pins: IN_Q_OVERFLOW events carry wd = -1, and matching is by wd only. | S383 | Hyprland-ConfigWatcher.cpp:60 | `.wd   = inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask),` |
| E03 | This line copies WD->file, the path stored in the watch matched by wd, into the SConfigWatchEvent that m_watchCallback receives; that the kernel's event name is dropped is a negative read of the handler body, not shown by this line. | S392 | Hyprland-ConfigWatcher.cpp:106 | `.file = WD->file,` |
| E04 | This line passes COMMAND and VALUE to the legacy config manager's parseKeyword, the call a runtime hyprctl keyword request reaches through dispatchKeyword; the legacy-only restriction (dispatchKeyword otherwise returning a keyword-cannot-work message) is established elsewhere in the same dispatcher function, not by this line. | S394 | Hyprland-HyprCtl.cpp:1190 | `std::string retval = mgr->parseKeyword(COMMAND, VALUE);` |
| E05 | The constructor calls resetHLConfig on this line; the function's clearing and re-adding of m_configPaths and its reload() caller are other lines of this file. | S395 | Hyprland-legacy-ConfigManager.cpp:630 | `resetHLConfig();` |
| E06 | On this line m_configCurrentPath becomes the nested file's own path before parseFile(value) runs; the relative-resolution consequence is an inference from the absolutePath helper, not from this assignment alone. | S395 | Hyprland-legacy-ConfigManager.cpp:1838 | `m_configCurrentPath          = value;` |
| E07 | On this line the legacy manager's getConfigPaths returns m_configPaths, the vector that resetHLConfig clears and handleSource appends to; ConfigWatcher reaches it through Config::mgr(), whose interface declaration is not in the pins. | S395 | Hyprland-legacy-ConfigManager.cpp:2134 | `return m_configPaths;` |
| E08 | The enum declares REFRESH_CONFIG_WATCHER as bit 8, the flag K02 attaches to misc:disable_autoreload and K15 tests in the refresher. | S391 | Hyprland-PropRefresher.hpp:18 | `REFRESH_CONFIG_WATCHER     = (1 << 8),` |
| E09 | REFRESH_ALL is the maximum of the enum's underlying type (uint16_t, declared on an earlier line of the same header), so every one of its 16 bits is set, including bit 8. | S391 | Hyprland-PropRefresher.hpp:21 | `REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),` |

## Limits

- Source level for every K, H and E row. No config file was saved and no reload, keyword or `hyprctl` state change was made by this round. Nothing here says that a save reloads Hyprland.
- Host observation (wave 2, read-only `/proc`, not a row): on 2026-10-28 the running Hyprland (pid 1622, started 2026-10-26) held one inotify instance (two descriptors, one open file description) with 40 watches, whose inode numbers and registration order equal the 40 primary watches that `tools/mado-watchplan.py` predicts for `~/.config/hypr/hyprland.conf` (`w2/R56W2RevProcFdinfo/comparison.md`, `fdinfo-capture.txt`). The kernel shows mask 0x8 (IN_CLOSE_WRITE) on each; IN_DONT_FOLLOW is an add flag and does not appear there, so that half of the mask is not confirmed by observation. None of the 40 paths is a symlink or missing, so the canonical-watch and missing-path branches were not exercised. One host, one tree, one moment.
- Pins are the frozen single-line quotes plus the surrounding functions read from the pin files. Declarations outside the pins are not shown by them: the `m_configPaths` declaration, `ConfigWatcher.hpp`, `getMainConfigPath`, `Supplementary::Jeremy` and the config-manager selection (upstream files at the same commit, fetched by the wave-2 prose audit F4/F5, state that the Lua manager is chosen only for a main path ending in `.lua` and that `m_configPaths` is a `std::vector<std::string>`; they are not pinned this round), hyprlang's `parseFile` and `source` pre-processing and comment stripping (the round-46 hyprlang pin holds them; whether the running build links that version is not pinned), and the Lua config provider. The chain assumes the legacy (hyprlang) config manager, as K27/E04 require.
- Failure paths: if `inotify_init1` fails, the constructor logs and returns (`Hyprland-ConfigWatcher.cpp:21-26`), and the event loop does not register a descriptor (`Hyprland-EventLoopManager.cpp:127`). A failed `inotify_add_watch` is not checked (line 60; E02). `onInotifyEvent` has no `IN_Q_OVERFLOW` branch.
- Reload per event: `onInotifyEvent` calls the callback once per complete event whose `wd` matches a current `m_watches` entry (lines 87-110; the `wd` lookup is line 100) and never reads the event mask, so every mask kind, including the kernel's IN_IGNORED, reaches `reload()` while its `wd` still matches; events whose `wd` matches nothing — for example `IN_Q_OVERFLOW`, whose `wd` is -1, or a watch already dropped by a rebuild — are logged instead. No coalescing appears in the handler, so one save that produces several matching events could call `reload()` several times (the refresh scheduling of step 7 can still merge the resulting work); the wave-1 lab saw one event per save for an in-place or truncating write — and no event for a touch-only `utimensat` — on kernel 7.2.11 (`w1/R56ScoutInotifyLab/raw-output.txt`, cases a1/a2 versus a5), which is the kernel plane only.
- Inode-based watches: inotify(7) says file monitoring follows the inode (`man7-inotify.7.html:225-228`). Two cases from the wave-1 lab with Hyprland's exact masks (kernel 7.2.11, `w1/R56ScoutInotifyLab/raw-output.txt`; not Hyprland itself): an editor that replaces the file by renaming a temporary file over it makes the kernel remove the file watch and deliver IN_IGNORED (K05 shows `setWatchList` would then try to remove it again, unchecked); a file moved away keeps its watch on the moved inode, which still fires on a later write to that inode. Because the callback reads no mask (step 4) and matches by `wd` only, the first case reaches `reload()` while the removed watch's `wd` is still in `m_watches` — before any rebuild drops the entry, after which the same event would be logged instead; what that reload does to the path list is steps 6-7 (a path that no longer matches leaves the list at the no-match return) and is inference, not observed in Hyprland.
- Runtime `source` keyword: `hyprctl keyword source <path>` reaches `parseKeyword` (E04). That `parseDynamic` then invokes the registered `handleSource` handler (line 614) is inference: `parseDynamic` is not in the pins. The handler appends to `m_configPaths` without clearing it (1836). The `source` branch of the keyword dispatcher (`Hyprland-HyprCtl.cpp:1194-1208`) does not call the watcher's `update()`, so the new path is not watched until a later `update()` call (inference from the branch; not run).
- Host records: H01 and H03 are captures from this host; they show values at capture time, not reload behaviour. H02 is a line of a captured listing; the live file's line 13 holds the same text.
- The watch-plan model's declared divergences (registration-v2 E8 and the tool docstring: HOME from `--home`, bytewise glob order and the `.`/`..` difference, the depth cap of 16, the canonical watch printed as the realpath, duplicate watches and attempt counts, Lua provider and runtime keyword, the hyprlang subset) belong to that tool and are not facts of this entry.
- Not checked: the `full-reset` branch of `reloadRequest` (`Hyprland-HyprCtl.cpp:1262-1274`, which resets and re-initialises the config manager; the pins hold it, this entry does not trace it), the registration of the `reload` command (`Hyprland-HyprCtl.cpp:2028`), and the tail of `verify()`.

## How to verify (read-only)

```bash
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
REV=28fc86ac2359ec27406d8a2c63bef82ea6e947ed   # the content revision this entry was audited at; use a later commit to check the current tree
# frozen tables and pins at the revision (never the working tree)
git -C "$LANE" show "$REV:.ufo/waves/round-56/frozen-tables-v2.json" | sha256sum    # expect 9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2
git -C "$LANE" ls-tree -r --name-only "$REV" -- .ufo/waves/round-56/fetch/ | head -20
# quote spot checks (each line must contain the frozen quote)
git -C "$LANE" show "$REV:.ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp" | sed -n '33,34p;54,56p;60p;67p;69p;105p'
# the C1 harness (12 controls) needs the round base 13f0acbe readable in $LANE (it is) and a scratch work dir
python3 -I "$LANE/quality/check-r56-controls.py" --claim c1 --repo "$LANE" --rev "$REV" --work "${TMPDIR:-/tmp}/r56-c1-ctl.$$"
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
python3 -I "$LANE/quality/counters/c1-r56-autoreload-entry.py" --repo "$LANE" --rev "$REV" --work /fast/scratch/hyaku/mado-r56/verify-autoreload   # a scratch directory you remove afterwards
```

