source: S383 — `src/config/shared/inotify/ConfigWatcher.cpp` (Hyprland efb5099, fetch/Hyprland-ConfigWatcher.cpp); S384 — `src/config/values/ConfigValues.cpp` (fetch/Hyprland-ConfigValues.cpp); S385 — `src/config/supplementary/propRefresher/PropRefresher.cpp` (fetch/Hyprland-PropRefresher.cpp); S386 — `src/managers/eventLoop/EventLoopManager.cpp` (fetch/Hyprland-EventLoopManager.cpp); S387 — `src/config/legacy/ConfigManager.cpp` (fetch/Hyprland-legacy-ConfigManager.cpp); S388 — `src/helpers/MiscFunctions.cpp` (fetch/Hyprland-MiscFunctions.cpp); S389 — `src/debug/HyprCtl.cpp` (fetch/Hyprland-HyprCtl.cpp); S390 — inotify(7), man7 HTML copy (fetch/man7-inotify.7.html)
verified-at: 2026-10-28
recheck: on-release

# Hyprland config auto-reload on 0.56.2: sourced chain (MADO-R56-C1)

Pins: Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2, the host build per the host version record). Frozen pin files and their sha256 are in `.ufo/waves/round-56/frozen-tables.json`.

## Scope

Settled at source level, in the pinned files:
- the declaration, default and refresh flag of `misc:disable_autoreload`, and where its value is read;
- how the watch list is built from the config path list: empty when the option is non-zero; one primary watch per path with a file or directory mask; a second canonical watch when the path is a symlink;
- how an inotify event reaches the reload callback, how the refresher and the hyprctl keyword branch reach `update()`, and how a reload ends in `postConfigReload` with `REFRESH_ALL`;
- how `source =` lines fill the path list, and the inotify(7) meaning of `IN_CLOSE_WRITE`, `IN_DONT_FOLLOW` and inode-based monitoring.

UNKNOWN in this entry. No filesystem event, reload or editor behaviour is observed, and the following are not settled by the pinned files:
- whether `REFRESH_ALL` includes `REFRESH_CONFIG_WATCHER`, so whether a reload rebuilds the watch list;
- where a parsed change to `misc:disable_autoreload` trips the refresh bit (ConfigValue headers are not pinned);
- what a text editor writes on save (in place, or by rename);
- the watch set the running host actually holds; the host pins are a getoption dump, a sources list and lstat results, not a watch list.

## Chain

Labels: [OBS] the pinned line shows it; [INF] follows from pinned lines by reasoning, not observed; [UNKNOWN] not settled by the pins.

1. **Declaration.** [OBS] K01–K02: `misc:disable_autoreload` is a Bool option with default false (line 492) whose metadata carries the refresh flag `REFRESH_CONFIG_WATCHER`. [UNKNOWN] where a parsed value change trips that flag.
2. **Value read and watch-list rule.** [OBS] K03–K04: `CConfigWatcher::update` (line 32) reads the option as an integer into a static pointer and passes an empty list to `setWatchList` when it is non-zero, otherwise `Config::mgr()->getConfigPaths()`. [OBS] E04: that list is `m_configPaths`, returned by const reference. So `autoreload=off` means an empty watch set, not a different mask.
3. **Watch construction.** [OBS] K05 and E07: old watches are removed, then the list is cleared. [OBS] K06: each path is classified with `std::filesystem::is_directory`. [OBS] K07–K08: a file mask `IN_CLOSE_WRITE | IN_DONT_FOLLOW`; a directory mask adds `IN_CREATE`, `IN_DELETE`, `IN_MOVED_TO` and `IN_MOVED_FROM`. [OBS] K09: `inotify_add_watch` is called per path and its result is stored in `wd` (lines 59–62) with no check. [INF] a failed add stays in the list as an entry with the failure value; no log line for it appears in the pinned file.
4. **Symlink canonical watch.** [OBS] K10–K11, E08–E09: when `canonical` succeeds and `is_symlink` is true, one more watch is added on the resolved path with `IN_CLOSE_WRITE` alone. [OBS] K30: the man page says `IN_DONT_FOLLOW` makes the call not dereference a symbolic link. [INF] Together, the primary watch of a symlink path is on the link itself, not its target, and the canonical watch is the one that observes the target file, which is where a write through the link lands. The canonical watch lacks `IN_DONT_FOLLOW`; for a resolved path that has no link component this should make no difference.
5. **Path list.** [OBS] E15 and E03: the main config path is the first entry, set in the constructor and again after each reset. [OBS] K20: `resetHLConfig` clears the list. [OBS] K21–K22: a `source =` match is appended only when `is_regular_file` holds for its `file_status`, and before its recursive parse. [OBS] K23: a directory match is logged and skipped. [OBS] K24–K26 and E17: the source path goes through `absolutePath` (a leading tilde from `getenv("HOME")`, a relative path against the directory of the current file) and then `glob` with `GLOB_TILDE`. [OBS] E11: the file type comes from `std::filesystem::status`. [INF] `status` follows symbolic links, a C++ standard library rule not shown in a pin; so a link to a regular file is appended under its link path, because the value at line 1825 is the un-resolved match. That link path is what steps 3 and 4 build the watches from. [OBS] E12: a match whose status call fails returns an error and the rest of the matches on that line are not parsed. [OBS] E13: the `source` keyword is registered with the static `handleSource` wrapper (line 614), which forwards to the legacy manager.
6. **Event to reload.** [OBS] E16 and K13: the watcher descriptor is a loop source only when valid, and `enterLoop` registers `configWatcherWrite` as its callback. [OBS] K14: `configWatcherWrite` calls `onInotifyEvent`. [OBS] K12: `onInotifyEvent` maps the event's `wd` to a stored watch and calls `m_watchCallback` with that watch's path; an unknown `wd` is logged as an error. [OBS] K17–K18: `CConfigManager::init` installs the callback, which logs and calls `reload()` (line 1081). The callback does not look at the event kind, so any matched event reloads.
7. **Reload.** [OBS] E14: `reload()` calls `resetHLConfig()`, which rebuilds the path list, then parses the config (line 743) and calls `postConfigReload` (line 750). [OBS] K19: `postConfigReload` calls `scheduleRefresh(REFRESH_ALL)`. [UNKNOWN] `REFRESH_ALL` is not defined in the pinned files, so whether it contains `REFRESH_CONFIG_WATCHER` is not settled. [INF] If it does not, the watch set is rebuilt only by a later `update()` call, and a `source =` file added by the reload is not watched until then. This is the chain's largest open point.
8. **Refresher and keyword paths.** [OBS] E10: `scheduleRefresh` sets the requested bit in `m_propsTripped`. [OBS] K15–K16: `refreshProp` calls `Config::watcher()->update()` when `REFRESH_CONFIG_WATCHER` is set. [OBS] E02 and K27: a hyprctl keyword whose text contains `misc:disable_autoreload` calls `update()` directly. [OBS] E01 and K28: the hyprctl request `reload` calls `Config::mgr()->reload()` on its non-full-reset path.
9. **Editor and kernel semantics.** [OBS] K29: `IN_CLOSE_WRITE` reports a file opened for writing that was closed. [OBS] E18: the man page says monitoring is inode-based: when a file is monitored (not the directory containing it), activity on any link to the file can generate an event. [INF] A file path gets a file-mask watch only, and no watch is set on its parent directory (K08 applies only to directories). An editor that saves by writing a new file and renaming it over the config would therefore produce no event on the watched inode, and E19 would then apply to the old inode once it is deleted. [UNKNOWN] not observed. [INF] For a directory path, the directory mask also sees children (K08, E20), so any file written in a watched directory reloads the config.

## Host reads (H rows)

[OBS] H01–H03 are reads of files fetched from the host: a getoption dump, a `source =` list and the version record. They are snapshots of files, not live reads of the compositor. [UNKNOWN] whether the running watch set matches the chain above.

## Rows

Rows are K (source: Hyprland pins and the inotify(7) man page), H (host), and E (extra facts beyond the frozen anchors; the counter ignores E rows).

### Declaration and watch list (K01–K11)

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| K01 | The misc:disable_autoreload option is declared with the description that a true value stops the config from reloading automatically on save, and its default is false. | S384 | Hyprland-ConfigValues.cpp:492 | `"misc:disable_autoreload", "If true, the config will not reload automatically on save.", false` |
| K02 | The misc:disable_autoreload declaration gives the option a refresh flag that names Supplementary::REFRESH_CONFIG_WATCHER. | S384 | Hyprland-ConfigValues.cpp:492 | `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}` |
| K03 | CConfigWatcher::update binds misc:disable_autoreload as an INTEGER config value, held in a static pointer named PDISABLEAUTORELOAD. | S383 | Hyprland-ConfigWatcher.cpp:33 | `CConfigValue<Config::INTEGER>("misc:disable_autoreload");` |
| K04 | The list passed to setWatchList is an empty vector when PDISABLEAUTORELOAD is non-zero, and the config paths otherwise. | S383 | Hyprland-ConfigWatcher.cpp:34 | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` |
| K05 | setWatchList removes each stored watch with inotify_rm_watch on the inotify descriptor before the watch list is rebuilt. | S383 | Hyprland-ConfigWatcher.cpp:46 | `inotify_rm_watch(m_inotifyFd.get(), watch.wd);` |
| K06 | setWatchList classifies each configured path with std::filesystem::is_directory and an error code before it chooses a mask. | S383 | Hyprland-ConfigWatcher.cpp:54 | `std::filesystem::is_directory(path, ecDir);` |
| K07 | The fileMask value for a non-directory watch starts with IN_CLOSE_WRITE, and the full line also ORs in IN_DONT_FOLLOW. | S383 | Hyprland-ConfigWatcher.cpp:55 | `fileMask      = IN_CLOSE_WRITE` |
| K08 | The directoryMask is derived from fileMask, so a directory watch carries the file bits plus the create, delete and move events on the same line. | S383 | Hyprland-ConfigWatcher.cpp:56 | `directoryMask = fileMask` |
| K09 | Each configured path is registered with inotify_add_watch on the inotify descriptor, using the mask chosen for that path. | S383 | Hyprland-ConfigWatcher.cpp:60 | `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |
| K10 | A second watch is added only when the canonical lookup reports no error and IS_SYMLINK is true for the path, so a plain file gets one watch. | S383 | Hyprland-ConfigWatcher.cpp:67 | `if (!ec && !ec2 && IS_SYMLINK) {` |
| K11 | The second watch for a symlink registers the CANONICAL target path with IN_CLOSE_WRITE alone, without the IN_DONT_FOLLOW bit of the primary watch. | S383 | Hyprland-ConfigWatcher.cpp:69 | `inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE),` |

### Event loop, refresh and reload (K12–K19)

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| K12 | onInotifyEvent calls m_watchCallback with an SConfigWatchEvent for each inotify event whose watch descriptor matches a stored watch. | S383 | Hyprland-ConfigWatcher.cpp:105 | `m_watchCallback(SConfigWatchEvent{` |
| K13 | enterLoop registers the watcher inotify descriptor as a readable wl_event_loop source whose callback is configWatcherWrite. | S386 | Hyprland-EventLoopManager.cpp:128 | `m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` |
| K14 | configWatcherWrite passes the readable event to Config::watcher()->onInotifyEvent and then returns 0 to the event loop. | S386 | Hyprland-EventLoopManager.cpp:71 | `Config::watcher()->onInotifyEvent();` |
| K15 | refreshProp runs the config watcher step only when the REFRESH_CONFIG_WATCHER bit is set in the m_propsTripped mask. | S385 | Hyprland-PropRefresher.cpp:148 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` |
| K16 | When the config watcher bit is tripped, the refresher calls Config::watcher()->update() as its config watcher step. | S385 | Hyprland-PropRefresher.cpp:149 | `Config::watcher()->update();` |
| K17 | CConfigManager::init installs its change handler with Config::watcher()->setOnChange, passing a lambda that captures this. | S387 | Hyprland-legacy-ConfigManager.cpp:1079 | `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {` |
| K18 | The change handler logs a DEBUG message reading CConfigManager: file modified, reloading, and it then calls reload. | S387 | Hyprland-legacy-ConfigManager.cpp:1080 | `CConfigManager: file {} modified, reloading` |
| K19 | postConfigReload calls scheduleRefresh with the REFRESH_ALL bit on the Supplementary refresher. | S387 | Hyprland-legacy-ConfigManager.cpp:1070 | `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` |

### Config path list and source handling (K20–K26)

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| K20 | resetHLConfig empties the m_configPaths list at the start of its paths section, before it adds the main config path again. | S387 | Hyprland-legacy-ConfigManager.cpp:776 | `m_configPaths.clear();` |
| K21 | handleSource appends each accepted regular-file match to m_configPaths before it parses that file recursively. | S387 | Hyprland-legacy-ConfigManager.cpp:1836 | `m_configPaths.emplace_back(value);` |
| K22 | handleSource parses a glob match only when is_regular_file is true for its file_status, which is computed from the match value. | S387 | Hyprland-legacy-ConfigManager.cpp:1835 | `if (std::filesystem::is_regular_file(file_status)) {` |
| K23 | A glob match that is a directory is logged with the message source= skipping directory and is not added to the path list. | S387 | Hyprland-legacy-ConfigManager.cpp:1844 | `"source= skipping directory {}", value);` |
| K24 | handleSource builds the glob pattern with absolutePath applied to rawpath and the current config path, then calls glob with GLOB_TILDE. | S387 | Hyprland-legacy-ConfigManager.cpp:1816 | `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())` |
| K25 | absolutePath reads the HOME environment variable through getenv into ENVHOME, which it uses for a leading tilde in the path. | S388 | Hyprland-MiscFunctions.cpp:65 | `static const char* const ENVHOME = getenv("HOME");` |
| K26 | For a relative path, absolutePath takes currentDir as everything before the last slash of currentPath, using substr and find_last_of. | S388 | Hyprland-MiscFunctions.cpp:68 | `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` |

### hyprctl keyword and reload (K27–K28)

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| K27 | The hyprctl keyword handler tests whether COMMAND contains misc:disable_autoreload, and the branch guards the watcher update on the next line. | S389 | Hyprland-HyprCtl.cpp:1223 | `if (COMMAND.contains("misc:disable_autoreload"))` |
| K28 | reloadRequest calls Config::mgr()->reload() on its non-full-reset path, after the full-reset branch has returned. | S389 | Hyprland-HyprCtl.cpp:1276 | `Config::mgr()->reload();` |

### inotify(7) semantics (K29–K30)

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| K29 | The inotify man page text attached to IN_CLOSE_WRITE says the event reports a file that was opened for writing and has been closed. | S390 | man7-inotify.7.html:186 | `File opened for writing was closed.` |
| K30 | The inotify man page entry for IN_DONT_FOLLOW says the flag stops inotify from dereferencing pathname when pathname is a symbolic link. | S390 | man7-inotify.7.html:262 | `Don't dereference <i>pathname</i> if it is a symbolic link.` |

### Host (H01–H03)

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| H01 | The host hyprctl getoption dump reports misc:disable_autoreload with integer value 0. | host | host-getoption.json:1 | `"option": "misc:disable_autoreload", "int": 0` |
| H02 | The host sources list contains a source line that reaches the omarchy theme hyprland.conf through the home config directory. | host | host-sources.txt:10 | `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| H03 | The host version record names the build commit efb50993780079460b0cbed1363e2166a2de1d9f, the commit this entry pins. | host | host-version.json:3 | `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"` |

### Extra facts (E01–E20, ignored by the counter)

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| E01 | The command table binds the hyprctl request named reload to the handler reloadRequest. | S389 | Hyprland-HyprCtl.cpp:2028 | `registerCommand(SHyprCtlCommand{"reload", false, reloadRequest});` |
| E02 | Inside the misc:disable_autoreload branch of the keyword handler, Config::watcher()->update() is called directly, not through the refresher. | S389 | Hyprland-HyprCtl.cpp:1224 | `Config::watcher()->update();` |
| E03 | resetHLConfig adds the main config path back as the first entry of m_configPaths after clearing the list. | S387 | Hyprland-legacy-ConfigManager.cpp:779 | `m_configPaths.emplace_back(mainConfigPath);` |
| E04 | getConfigPaths returns m_configPaths by const reference, the list that CConfigWatcher::update passes to setWatchList. | S387 | Hyprland-legacy-ConfigManager.cpp:2134 | `return m_configPaths;` |
| E05 | The watcher constructor creates its inotify descriptor with inotify_init1 and the IN_NONBLOCK flag. | S383 | Hyprland-ConfigWatcher.cpp:21 | `m_inotifyFd(inotify_init1(IN_NONBLOCK` |
| E06 | When inotify_init1 fails, the watcher constructor logs that config will not be automatically reloaded and returns. | S383 | Hyprland-ConfigWatcher.cpp:23 | `Log::logger->log(Log::ERR, "CConfigWatcher couldn't open an inotify node. Config will not be automatically reloaded");` |
| E07 | setWatchList clears the m_watches vector after removing the old watches, before it adds the new entries. | S383 | Hyprland-ConfigWatcher.cpp:49 | `m_watches.clear();` |
| E08 | CANONICAL is the result of std::filesystem::canonical on the configured path, the target that the second watch registers. | S383 | Hyprland-ConfigWatcher.cpp:65 | `CANONICAL  = std::filesystem::canonical(path, ec);` |
| E09 | IS_SYMLINK is computed with std::filesystem::is_symlink on the configured path itself, the test that gates the canonical second watch. | S383 | Hyprland-ConfigWatcher.cpp:66 | `IS_SYMLINK = std::filesystem::is_symlink(path, ec2);` |
| E10 | scheduleRefresh takes a PropRefreshBits argument named prop, which the body then sets in the m_propsTripped mask. | S385 | Hyprland-PropRefresher.cpp:29 | `void CPropRefresher::scheduleRefresh(PropRefreshBits prop) {` |
| E11 | The match is classified through a status call on value, and the is_regular_file test reads the result of that status call. | S387 | Hyprland-legacy-ConfigManager.cpp:1828 | `file_status = std::filesystem::status(value, ec);` |
| E12 | A failed status call on a match returns the inaccessible message for that file, and the rest of the glob matches are not parsed. | S387 | Hyprland-legacy-ConfigManager.cpp:1832 | `return "source= file " + value + " is inaccessible!";` |
| E13 | The Hyprlang config registers the source keyword with the static handleSource wrapper, which forwards to the legacy manager. | S387 | Hyprland-legacy-ConfigManager.cpp:614 | `m_config->registerHandler(&::handleSource, "source", {false});` |
| E14 | reload calls resetHLConfig before it parses the config, so the path list is rebuilt on every reload. | S387 | Hyprland-legacy-ConfigManager.cpp:731 | `resetHLConfig();` |
| E15 | The constructor seeds m_configPaths with m_mainConfigPath before it creates the Hyprlang config object. | S387 | Hyprland-legacy-ConfigManager.cpp:485 | `m_configPaths.emplace_back(m_mainConfigPath);` |
| E16 | enterLoop registers the watcher descriptor as a loop source only when getInotifyFD returns a valid descriptor. | S386 | Hyprland-EventLoopManager.cpp:127 | `if (const auto& FD = Config::watcher()->getInotifyFD(); FD.isValid())` |
| E17 | For a leading dot-dot path, absolutePath replaces 2 characters, plus one when currentPath is empty. | S388 | Hyprland-MiscFunctions.cpp:73 | `value.replace(0, 2 + currentPath.empty(), parentDir);` |
| E18 | The inotify man page says monitoring is inode-based: watching a file, and not its containing directory, can report activity on any link to it. | S390 | man7-inotify.7.html:225 | `Inotify monitoring is inode-based: when monitoring a file (but not` |
| E19 | The inotify man page says a watched file or directory that is deleted yields IN_DELETE_SELF, after which the watch is reported as ignored. | S390 | man7-inotify.7.html:200 | `Watched file/directory was itself deleted.` |
| E20 | The inotify man page says IN_MOVED_FROM is generated for the directory containing the old filename when a file is renamed. | S390 | man7-inotify.7.html:215 | `Generated for the directory containing the old filename` |

## Limits

- The K and H rows prove quote identity at a pinned line, registry binding and lexical grounding (an identifier shared with the quote, no number absent from the quote). They do not prove that a proposition is entailed by its quote. That is the sentence-to-pin audit and the non-author closure.
- The pins are the fetched files at efb5099, each sha256 frozen in `frozen-tables.json`. They were not re-fetched upstream for this entry.
- The pinned provider path is `src/config/legacy/ConfigManager.cpp`. Nothing pinned shows that the host's Hyprland 0.56.2 build takes this provider path (registration §C2 describes a hyprlang `configProvider`). [UNKNOWN]
- Not in the pins, so not stated as fact: the definitions of `REFRESH_ALL` and `REFRESH_CONFIG_WATCHER`; the trip logic of ConfigValue on parse; what `inotify_add_watch` does on failure beyond the code shown; glob collation; C++ `std::filesystem` rules (cited as [INF]).
- Declared divergences of the C2 watch model (depth cap, glob order, `~user`, the Lua provider, runtime keyword) apply to the tool, not to this entry.
- No event was generated, no reload was observed, no file in any config tree was written, and no compositor state was changed.

## How to verify

Read-only commands. Freeze commit `3423ae285676c2a10273000f4519163472b443db`; lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
L=/home/vgpnk/Projects/shokunin/mado-shokunin
R=3423ae285676c2a10273000f4519163472b443db
P=.ufo/waves/round-56/fetch
git -C "$L" show "$R:.ufo/waves/round-56/frozen-tables.json" | sha256sum      # d50d2b7b...f9af
git -C "$L" show "$R:$P/Hyprland-ConfigWatcher.cpp" | sha256sum               # 8383b8ab...d516c
git -C "$L" show "$R:$P/Hyprland-ConfigWatcher.cpp" | sed -n '33,34p'         # K03, K04
git -C "$L" show "$R:$P/Hyprland-ConfigValues.cpp" | sed -n '492p'           # K01, K02
git -C "$L" show "$R:$P/Hyprland-legacy-ConfigManager.cpp" | sed -n '1816p;1835,1836p'   # K24, K22, K21
git -C "$L" show "$R:$P/man7-inotify.7.html" | sed -n '186p;262p'            # K29, K30
cat "$L/$P/host-getoption.json"                                                # H01
sed -n '10p' "$L/$P/host-sources.txt"                                          # H02
sed -n '3p' "$L/$P/host-version.json"                                          # H03
grep -c '^| [KH][0-9][0-9] | ' corpus/knowledge/hyprland-config-autoreload-r56.md   # expect 33 once the entry is in the lane
hyprctl getoption misc:disable_autoreload -j
hyprctl version -j
stat -c '%F %n' ~/.config/hypr/hyprland.conf
readlink -f ~/.config/hypr/hyprland.conf
```
