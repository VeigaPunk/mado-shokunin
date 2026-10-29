# Hyprland config auto-reload on 0.56.2: from `misc:disable_autoreload` through the inotify watch list to `CConfigManager::reload`, source-level

source: S383, S384, S385, S386, S387, S388, S389, S390 - Hyprland v0.56.2 at commit `efb50993780079460b0cbed1363e2166a2de1d9f` (legacy hyprlang config path): `src/config/shared/inotify/ConfigWatcher.cpp` (S383), `src/config/values/ConfigValues.cpp` (S384), `src/config/supplementary/propRefresher/PropRefresher.cpp` (S385), `src/managers/eventLoop/EventLoopManager.cpp` (S386), `src/config/legacy/ConfigManager.cpp` (S387), `src/helpers/MiscFunctions.cpp` (S388), `src/debug/HyprCtl.cpp` (S389); the inotify(7) man page (S390). Pins: `.ufo/waves/round-56/fetch/` (sha256 in `frozen-tables.json` `c1.pin_sha256` and `c1.host_pin_sha256`); host captures `host-getoption.json`, `host-sources.txt`, `host-version.json`, `host-watched-lstat.txt`.
verified-at: 2026-10-28
recheck: on-release - when Hyprland leaves `0.56.2` (commit `efb50993`) re-pull S383-S390 and re-read the chain below; when the host's `hyprctl version -j` commit, the `hyprctl getoption misc:disable_autoreload -j` value or the host source list changes, re-run the host join in How to verify.

Lane: mado-shokunin. Round: 56. Claim C1 (coverage, sourced). Every row below is a line of a pinned file; the quote cell is generated from the frozen table, and the proposition cell says what that one line shows.

## Scope

Settled at source level for the pinned commit `efb50993` (v0.56.2, the legacy hyprlang config path, the only path `dispatchKeyword` serves, HyprCtl lines 1162-1163):

- where `misc:disable_autoreload` is declared, how it is read, and what it does to the watch list (K01-K04);
- which config paths enter the watch list, with which inotify masks, and the symlink canonical watch (K05-K11, E11-E12);
- how an inotify event reaches the config callback (K12-K14, E08-E10);
- how that callback calls `reload()`, and how a reload schedules the prop refresh (K17-K19, E01-E07);
- how the refresh rebuilds the watch list when the watcher bit is set (K15-K16);
- how `hyprctl keyword misc:disable_autoreload` and `hyprctl reload` enter the same code (K27-K28, E13-E15);
- the host join: the live option value, the host source list and the build commit, against the pins (H01-H03 and How to verify).

UNKNOWN in this entry, and not observed:

- no filesystem event, reload or editor behaviour is observed. Nothing here says that saving a file produces an inotify event on the host, that Hyprland reloads on the host, or how long a reload takes. No `hyprctl keyword` and no `hyprctl reload` was run to write this entry; every host read is a read of a value.
- the values of `REFRESH_ALL` and `REFRESH_CONFIG_WATCHER` and the refresher header are not pinned, so whether a reload always reaches the watcher bit is an inference, not a read (see the chain, step 8).
- where `enterLoop` and `init` are called from, and whether the inotify fd is valid at that time on the host.
- the watch set the running host process holds: no inotify state was read.
- an editor's save method (in place, or by rename over the file).
- the Lua config provider; the pins cover the legacy path only.

## Chain

Source-level steps. Each step cites row ids; connective statements that go beyond the cited lines are marked [INFERENCE].

1. **Declaration.** `misc:disable_autoreload` is a boolean option (declared with `MS<Bool>`, default false) whose refresh action is `REFRESH_CONFIG_WATCHER` (K01, K02). Whether the refresh flag is applied when a config line sets the option is not in the pins; the chain below does not depend on it except where step 8 says so.

2. **The read.** `CConfigWatcher::update` reads the option into a static `CConfigValue` of type `Config::INTEGER` (K03). It passes an empty path list when the value is non-zero, and the manager's `getConfigPaths()` list otherwise (K04). A non-zero value therefore leaves the watch list empty.

3. **The path list.** `getConfigPaths` returns `m_configPaths` (E16). The legacy reset clears that list (K20) and seeds it with the main config path (seed at legacy line 779, not quoted). `handleSource` appends each matched regular file (K21), tests the file type (K22), and skips a directory or non-regular match with a WARN (K23). Each appended file is parsed recursively with `parseFile` (E17). The match set is `glob` over `absolutePath` with `GLOB_TILDE` (K24). `absolutePath` expands a leading tilde with `HOME` (K25) and resolves a relative path against the directory of the current file (K26; the function is `MiscFunctions.cpp` lines 61-83, read in full). For a `../` path it replaces two leading characters, with the length `2 + currentPath.empty()` (E18); the length is 2 whenever the current path is non-empty, which the main config path always is.

4. **The watch list.** `setWatchList` removes every previous watch (K05). For each path it asks `std::filesystem::is_directory` (K06). A file takes the mask `IN_CLOSE_WRITE` with `IN_DONT_FOLLOW` (K07). A directory takes that mask with `IN_CREATE`, `IN_DELETE`, `IN_MOVED_TO` and `IN_MOVED_FROM` added (K08). The watch is added with `inotify_add_watch` (K09). A symlink entry also gets a second watch on its canonical target with `IN_CLOSE_WRITE` alone (K10, K11). That second record carries the link's path in its `file` field (ConfigWatcher.cpp line 70, not quoted), so an event through the target is reported under the link's path. [INFERENCE: the canonical watch fires on writes to the target; the pins do not show the kernel behaviour.] A path that does not exist still gets a watch record whose `wd` is whatever `inotify_add_watch` returned, and that value is not checked (E12, K09). [INFERENCE: a failed add leaves a record that no event can match.] A directory entry can only be the main config path: `handleSource` appends regular files only (K21, K22), and the main path is seeded without a type test (legacy line 779, not quoted). [INFERENCE from those branches.]

5. **The event loop.** The inotify fd is created in the `CConfigWatcher` constructor; an invalid fd logs that the config will not be reloaded and returns (E11). `enterLoop` registers the fd on the Wayland event loop only when `getInotifyFD` reports it valid (E08, K13). `configWatcherWrite` calls `onInotifyEvent` (K14). `onInotifyEvent` reads one buffer, walks every event in it, finds the watch by `wd` (E10), and calls `m_watchCallback` with that watch's file (K12). The pinned loop has no mask or name filter: every event that matches a registered `wd` invokes the callback (E09, lines 80-110 read in full). [INFERENCE for the effect: an `IN_CLOSE_WRITE` on a registered watch reaches the callback.]

6. **The callback and the reload.** The legacy `init` installs the callback (K17). It logs at DEBUG (K18) and calls `reload()` (E02). `reload()` opens at E01; it resets the config, path list included (K20), parses the main file, and ends by calling `postConfigReload` with the parse result (`reload()` body, legacy lines 726-751; `postConfigReload` opens at E03). The parse rebuilds `m_configPaths` through `handleSource`.

7. **The refresh.** `postConfigReload` calls `scheduleRefresh(REFRESH_ALL)` (K19). `scheduleRefresh` ORs the requested bits into `m_propsTripped` (E04). If none was scheduled, it defers `refreshProp` through `doLater` (E05, E06), and `doLater` queues the function on the Wayland loop's idle source (E07). [INFERENCE: the refresh therefore runs as an idle callback after the current callback returns.]

8. **The watcher bit.** `refreshProp` opens the `REFRESH_CONFIG_WATCHER` branch on the bit (K15) and calls `Config::watcher()->update()` in it (K16). `update` rebuilds the watch list from the new `getConfigPaths()` (K04). **UNKNOWN here:** whether `REFRESH_ALL` (K19) includes the `REFRESH_CONFIG_WATCHER` bit; the refresher header is not pinned. If it does not, a reload does not rebuild the watch list by this route, and the chain stops at step 7 for the watch list. The chain as written assumes that it does.

9. **The keyword path.** `dispatchKeyword` refuses non-legacy providers (HyprCtl lines 1162-1163), splits `COMMAND` and `VALUE`, and calls `parseKeyword` before any of the option tests (E13). If `COMMAND` contains `misc:disable_autoreload`, it calls `update` on the watcher (K27). Because `update` reads the option's current value (K03, K04), a keyword that sets a non-zero value empties the watch list at once. [INFERENCE: the pins do not show how `parseKeyword` applies the value.] Whether the keyword's new value reaches the refresh bit is UNKNOWN for the same reason as step 8.

10. **The reload command.** `reloadRequest` is registered under the command name `reload` (E15). A request ending in `full-reset` takes its own branch, which rebuilds the config manager (E14). Any other request calls `Config::mgr()->reload()` (K28), the same `reload()` that step 6 reaches. The two entry points therefore meet at `reload()`, `postConfigReload` and the refresh of steps 7 and 8.

11. **Inotify masks (man page).** `IN_CLOSE_WRITE` is the event for a file that was opened for writing and then closed (K29). `IN_DONT_FOLLOW` means a symbolic link is not dereferenced (K30). Together with step 4: the primary watch on a symlink entry is set on the link path itself with `IN_DONT_FOLLOW`, and the canonical watch names the target. [INFERENCE: which events a watch on the link inode itself delivers is not established by the pins.]

12. **Editor saves.** Whether an editor's save reaches the file watch depends on how the editor writes. The file mask has no `IN_MOVED_TO` and no `IN_CREATE` (K07); the directory mask has them (K08), but the directory mask is only used for a directory entry (step 4). A save by rename over the file therefore sits outside the file mask. [INFERENCE: this is what the masks say; which way a given editor writes is not observed here.]

## Host join

The host reads below are values read from the host, not reload behaviour.

- **H01, the live option.** The captured `hyprctl getoption misc:disable_autoreload -j` record gives `int` 0 with `set` false. With no `misc:disable_autoreload` line in the host config files (How to verify), the file-derived value is unset, which the watch-list rule treats as 0, so the watch list is non-empty under step 4. [INFERENCE from K03 and K04.]
- **H02, the host source list.** The main config's `source =` lines are the 18 lines in `host-sources.txt`; line 10 is the omarchy theme `hyprland.conf`.
- **H03, the build.** The captured `hyprctl version -j` commit is the pinned commit `efb50993780079460b0cbed1363e2166a2de1d9f` (`c1.commit`).

The live host read on 2026-10-28, with the How to verify commands: `misc:disable_autoreload` reports int 0; `hyprctl version -j` reports the pinned commit; the main config's `source` lines equal `host-sources.txt`; the 40 paths of `host-watched-lstat.txt` lstat as regular files; no host config file names `disable_autoreload`.

**How to read the join (AGREE and DIFFER).** The join rule of the round-56 watch-list predicate (registration §C2) sets `config` to 1 when the last accepted `misc:disable_autoreload` value in the file closure is non-zero, and to 0 otherwise (unset counts as 0). The live value is the `int` of the `getoption` record. `AGREE` means the live `int` equals `config`; `DIFFER` means they do not; `UNKNOWN` means no `getoption` record was read. `AGREE` says the file closure and the running option agree on the 0/1 reading; it does not say a watch is registered, that an event arrives, or that a reload runs. `DIFFER` points at a runtime change that the files do not hold (a keyword, which step 9 covers and the file-only rule does not model), a file set that differs from the one the host runs, or a value the rule does not parse. Either way the join is a check on inputs, not on reload.

## Rows: declaration, read and watch list

Counted rows. Quote cell = frozen quote; pin cell = frozen pin file and line; source cell = frozen source id.

| id | proposition | src | pin:line | quote |
|---|---|---|---|---|
| K01 | Line 492 registers the option misc:disable_autoreload as MS<Bool> with the description 'If true, the config will not reload automatically on save' and default false. | S384 | Hyprland-ConfigValues.cpp:492 | `"misc:disable_autoreload", "If true, the config will not reload automatically on save.", false` |
| K02 | Line 492 sets the refresh field of misc:disable_autoreload to the flag REFRESH_CONFIG_WATCHER, which is the refresh action this option carries. | S384 | Hyprland-ConfigValues.cpp:492 | `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}` |
| K03 | Line 33 reads the option misc:disable_autoreload into a static CConfigValue of type Config::INTEGER, so the watcher takes its value as an integer. | S383 | Hyprland-ConfigWatcher.cpp:33 | `CConfigValue<Config::INTEGER>("misc:disable_autoreload");` |
| K04 | Line 34 passes an empty list to setWatchList when PDISABLEAUTORELOAD is non-zero, and the list from Config::mgr()->getConfigPaths() otherwise. | S383 | Hyprland-ConfigWatcher.cpp:34 | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` |
| K05 | Line 46 calls inotify_rm_watch on the inotify fd for each existing watch.wd, removing the previous watch descriptors before the list is rebuilt. | S383 | Hyprland-ConfigWatcher.cpp:46 | `inotify_rm_watch(m_inotifyFd.get(), watch.wd);` |
| K06 | Line 54 tests path with std::filesystem::is_directory and stores the answer in isDirectory, which chooses between the file and directory masks. | S383 | Hyprland-ConfigWatcher.cpp:54 | `std::filesystem::is_directory(path, ecDir);` |
| K07 | Line 55 starts the file mask fileMask with IN_CLOSE_WRITE and OR-s IN_DONT_FOLLOW onto it on the same line. | S383 | Hyprland-ConfigWatcher.cpp:55 | `fileMask      = IN_CLOSE_WRITE` |
| K08 | Line 56 defines directoryMask from fileMask and OR-s IN_CREATE, IN_DELETE, IN_MOVED_TO and IN_MOVED_FROM onto it on the same line. | S383 | Hyprland-ConfigWatcher.cpp:56 | `directoryMask = fileMask` |
| K09 | Line 60 adds an inotify watch on path with mask on the watcher inotify fd, and the returned descriptor is stored as the wd of that watch entry. | S383 | Hyprland-ConfigWatcher.cpp:60 | `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |
| K10 | Line 67 takes the branch for a second watch only when both error codes are clear and IS_SYMLINK holds, which is the symlink case. | S383 | Hyprland-ConfigWatcher.cpp:67 | `if (!ec && !ec2 && IS_SYMLINK) {` |
| K11 | Line 69 adds a second watch on CANONICAL, the resolved target of a symlink, with the mask IN_CLOSE_WRITE alone and no IN_DONT_FOLLOW. | S383 | Hyprland-ConfigWatcher.cpp:69 | `inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE),` |

## Rows: event loop, callback and refresh

| id | proposition | src | pin:line | quote |
|---|---|---|---|---|
| K12 | Line 105 invokes the stored m_watchCallback with an SConfigWatchEvent whose file is the file of the matched watch entry. | S383 | Hyprland-ConfigWatcher.cpp:105 | `m_watchCallback(SConfigWatchEvent{` |
| K13 | Line 128 registers the watcher inotify fd on the Wayland event loop for readability, with configWatcherWrite as the callback. | S386 | Hyprland-EventLoopManager.cpp:128 | `m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` |
| K14 | Line 71 is the body of configWatcherWrite and calls onInotifyEvent on the config watcher singleton. | S386 | Hyprland-EventLoopManager.cpp:71 | `Config::watcher()->onInotifyEvent();` |
| K15 | Line 148 tests whether m_propsTripped carries the REFRESH_CONFIG_WATCHER bit, which opens the watcher branch of refreshProp. | S385 | Hyprland-PropRefresher.cpp:148 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` |
| K16 | Line 149 calls update on the config watcher singleton, the body of the branch that line 148 opens. | S385 | Hyprland-PropRefresher.cpp:149 | `Config::watcher()->update();` |
| K17 | Line 1079 registers a lambda with setOnChange on the config watcher, capturing this and taking the SConfigWatchEvent by reference. | S387 | Hyprland-legacy-ConfigManager.cpp:1079 | `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {` |
| K18 | Line 1080 logs at DEBUG level the message that a file was modified and reloading, from inside the setOnChange lambda. | S387 | Hyprland-legacy-ConfigManager.cpp:1080 | `CConfigManager: file {} modified, reloading` |
| K19 | Inside postConfigReload, line 1070 calls scheduleRefresh with REFRESH_ALL on the refresher singleton, after the plugin loads. | S387 | Hyprland-legacy-ConfigManager.cpp:1070 | `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` |

## Rows: path list and source closure

| id | proposition | src | pin:line | quote |
|---|---|---|---|---|
| K20 | Line 776 clears m_configPaths at the start of resetHLConfig, before the main config path is added again. | S387 | Hyprland-legacy-ConfigManager.cpp:776 | `m_configPaths.clear();` |
| K21 | Line 1836 appends the resolved value path to m_configPaths inside handleSource, for each matched regular file. | S387 | Hyprland-legacy-ConfigManager.cpp:1836 | `m_configPaths.emplace_back(value);` |
| K22 | Line 1835 branches on std::filesystem::is_regular_file applied to file_status, so only regular files reach the parse. | S387 | Hyprland-legacy-ConfigManager.cpp:1835 | `if (std::filesystem::is_regular_file(file_status)) {` |
| K23 | Line 1844 logs a WARN message that source= skips a directory match, in the branch that handles directories. | S387 | Hyprland-legacy-ConfigManager.cpp:1844 | `"source= skipping directory {}", value);` |
| K24 | Line 1816 passes absolutePath of rawpath to glob with the flag GLOB_TILDE, the pattern expansion behind each source= line. | S387 | Hyprland-legacy-ConfigManager.cpp:1816 | `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())` |
| K25 | Line 65 reads the HOME environment variable with getenv into the static ENVHOME, which absolutePath uses for a leading tilde. | S388 | Hyprland-MiscFunctions.cpp:65 | `static const char* const ENVHOME = getenv("HOME");` |
| K26 | Line 68 sets currentDir to the part of currentPath before its last slash, the directory that relative paths resolve against. | S388 | Hyprland-MiscFunctions.cpp:68 | `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` |

## Rows: hyprctl, inotify(7), host

| id | proposition | src | pin:line | quote |
|---|---|---|---|---|
| K27 | Line 1223 tests whether the keyword COMMAND contains misc:disable_autoreload and, if it does, calls update on the config watcher. | S389 | Hyprland-HyprCtl.cpp:1223 | `if (COMMAND.contains("misc:disable_autoreload"))` |
| K28 | Line 1276 calls reload on the config manager singleton, the branch of reloadRequest that is taken for a hyprctl reload request. | S389 | Hyprland-HyprCtl.cpp:1276 | `Config::mgr()->reload();` |
| K29 | The inotify man page describes IN_CLOSE_WRITE on line 186 as: a file opened for writing was closed. | S390 | man7-inotify.7.html:186 | `File opened for writing was closed.` |
| K30 | The inotify man page on line 262 states that IN_DONT_FOLLOW means pathname is not dereferenced when it is a symbolic link. | S390 | man7-inotify.7.html:262 | `Don't dereference <i>pathname</i> if it is a symbolic link.` |
| H01 | The captured hyprctl getoption record reports misc:disable_autoreload with int 0 and set false on the host. | host | host-getoption.json:1 | `"option": "misc:disable_autoreload", "int": 0` |
| H02 | Line 10 of the host source capture lists the omarchy theme hyprland.conf as a source line of the main config. | host | host-sources.txt:10 | `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| H03 | The captured hyprctl version record gives the build commit efb50993780079460b0cbed1363e2166a2de1d9f on line 3, the pinned commit. | host | host-version.json:3 | `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"` |

## Extra rows (not counted by the frozen predicate)

These rows give source facts the frozen anchors do not carry: the function openings and call sites the chain above cites. The quote is the pinned line itself; the counter ignores E rows.

| id | proposition | src | pin:line | quote |
|---|---|---|---|---|
| E01 | Line 726 opens the definition of CConfigManager::reload, the function the watcher callback calls on a change. | S387 | Hyprland-legacy-ConfigManager.cpp:726 | `void CConfigManager::reload() {` |
| E02 | Line 1081 calls reload inside the watcher callback, after the DEBUG log line, so each callback invocation runs reload. | S387 | Hyprland-legacy-ConfigManager.cpp:1081 | `reload();` |
| E03 | Line 970 opens postConfigReload, which reload calls with the parse result and which ends by scheduling the refresh of K19. | S387 | Hyprland-legacy-ConfigManager.cpp:970 | `void CConfigManager::postConfigReload(const Hyprlang::CParseResult& result) {` |
| E04 | Line 29 opens scheduleRefresh, which ORs the requested prop bits into m_propsTripped before it defers the refresh. | S385 | Hyprland-PropRefresher.cpp:29 | `void CPropRefresher::scheduleRefresh(PropRefreshBits prop) {` |
| E05 | Line 33 tests m_scheduled and the event loop pointer before the refresh is deferred, so a second call does not queue a second callback. | S385 | Hyprland-PropRefresher.cpp:33 | `if (!m_scheduled && g_pEventLoopManager) {` |
| E06 | Line 34 defers refreshProp through an event-loop doLater callback when no refresh is already scheduled. | S385 | Hyprland-PropRefresher.cpp:34 | `m_scheduledRefreshSeq = g_pEventLoopManager->doLater([this, weak = WP<CPropRefresher>{refresher()}] {` |
| E07 | Line 215 opens CEventLoopManager::doLater, which queues the function as an idle callback and returns a sequence number. | S386 | Hyprland-EventLoopManager.cpp:215 | `uint64_t CEventLoopManager::doLater(const std::function<void()>& fn) {` |
| E08 | Line 127 registers the watcher inotify fd only when getInotifyFD returns a valid descriptor, so the check precedes the registration on line 128. | S386 | Hyprland-EventLoopManager.cpp:127 | `if (const auto& FD = Config::watcher()->getInotifyFD(); FD.isValid())` |
| E09 | Line 80 opens onInotifyEvent, which reads the inotify buffer and calls the change callback for each event it matches. | S383 | Hyprland-ConfigWatcher.cpp:80 | `void CConfigWatcher::onInotifyEvent() {` |
| E10 | Line 100 finds the m_watches entry for each event by comparing the wd field alone, so the callback receives only the matched file. | S383 | Hyprland-ConfigWatcher.cpp:100 | `const auto WD = std::ranges::find_if(m_watches, [wd = ev->wd](const auto& e) { return e.wd == wd; });` |
| E11 | Line 22 tests m_inotifyFd for validity right after the constructor's inotify_init1 call and returns early when it is not valid. | S383 | Hyprland-ConfigWatcher.cpp:22 | `if (!m_inotifyFd.isValid()) {` |
| E12 | Line 59 appends a SInotifyWatch record to m_watches, and the wd field is filled from the inotify_add_watch call on line 60. | S383 | Hyprland-ConfigWatcher.cpp:59 | `m_watches.emplace_back(SInotifyWatch{` |
| E13 | Line 1190 applies the keyword through mgr->parseKeyword before the misc:disable_autoreload test that K27 covers in the same function. | S389 | Hyprland-HyprCtl.cpp:1190 | `std::string retval = mgr->parseKeyword(COMMAND, VALUE);` |
| E14 | Line 1262 branches on a request that ends with full-reset, the branch that rebuilds the config manager instead of calling reload. | S389 | Hyprland-HyprCtl.cpp:1262 | `if (request.ends_with("full-reset")) {` |
| E15 | Line 2028 registers the hyprctl command named reload with the handler reloadRequest, the path a hyprctl reload request takes. | S389 | Hyprland-HyprCtl.cpp:2028 | `registerCommand(SHyprCtlCommand{"reload", false, reloadRequest});` |
| E16 | Line 2133 opens getConfigPaths, the accessor that returns m_configPaths and that the watcher update passes to setWatchList. | S387 | Hyprland-legacy-ConfigManager.cpp:2133 | `const std::vector<std::string>& CConfigManager::getConfigPaths() {` |
| E17 | Line 1839 parses the sourced regular file with parseFile, the recursive parse that follows the append on line 1836. | S387 | Hyprland-legacy-ConfigManager.cpp:1839 | `const auto THISRESULT        = m_config->parseFile(value.c_str());` |
| E18 | Line 73 replaces the leading two characters of value with parentDir for a ../ path, using the length 2 plus currentPath.empty(). | S388 | Hyprland-MiscFunctions.cpp:73 | `value.replace(0, 2 + currentPath.empty(), parentDir);` |

## Limits

- The predicate proves quote identity at an exact pin line, the registry binding and the scope of each row, and lexical grounding (an identifier shared with the quote; no number that the quote does not carry). It does not prove that a proposition follows from its quote. The sentence-to-pin audit and the non-author closure carry that, and are not counted here.
- No filesystem event, reload, `hyprctl keyword`, `hyprctl reload` or editor save was run or observed. The host reads are reads of recorded values.
- Pinned files are the eight files in `fetch/`. Not pinned: the refresher header (`REFRESH_ALL`, `REFRESH_CONFIG_WATCHER` values), `ConfigWatcher.hpp`, the event loop header, `Supplementary::Jeremy::getMainConfigPath`, `verifyConfigExists`, the hyprlang parser (`parseFile`, `parseDynamic`), and the callers of `enterLoop` and `init`. Steps 5, 7 and 8 rest on those gaps where they say UNKNOWN or INFERENCE.
- The round-56 watch-list rule has a depth cap of 16 (registration §C2). The read lines of `handleSource` (legacy lines 1802-1855) show recursion (E17) and no depth test. That absence is a statement about those lines only.
- `K03` reads a value declared as `MS<Bool>` (K01) through a `CConfigValue<Config::INTEGER>`. What the accessor does with a declared Bool is not pinned; the entry does not rely on it beyond the 0/non-zero test in K04.
- `hyprctl keyword` refuses non-legacy providers (HyprCtl lines 1162-1163); the Lua provider is outside this entry.
- The `host-watched-lstat.txt` capture has no recorded producer in the lane. The live re-lstat on 2026-10-28 agrees for all 40 entries (How to verify), and the entry does not use the file for any counted row.
- The counter for this entry (`quality/counters/c1-r56-autoreload-entry.py`) and the registry rows for S383-S390 land in other seats. The rows here are checked against the pins; the registry legs (`source_cell`, `scope`, `new_rows`) are checked only after integration.

## How to verify

Read-only commands. `LANE` names the lane root; `W` is its round directory; `WORK` is a scratch directory created under the seat's scratch root.

```bash
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
W=$LANE/.ufo/waves/round-56
REV=$(git -C "$LANE" rev-parse HEAD)

# 1. pins and frozen tables (freeze-verify reads the lane tree and writes nothing)
(cd "$LANE" && python3 -I "$W/freeze-verify.py" | tail -1)
(cd "$W/fetch" && sha256sum Hyprland-*.cpp man7-inotify.7.html host-*.json host-*.txt)

# 2. one counted row against its pin line, byte for byte (K13 and H03 here)
sed -n '128p' "$W/fetch/Hyprland-EventLoopManager.cpp"
sed -n '3p' "$W/fetch/host-version.json"

# 3. the chain's call sites in the pins
grep -n 'configWatcherWrite\|onInotifyEvent\|m_watchCallback' "$W/fetch/Hyprland-EventLoopManager.cpp" "$W/fetch/Hyprland-ConfigWatcher.cpp"
grep -n 'REFRESH_CONFIG_WATCHER\|REFRESH_ALL\|scheduleRefresh\|postConfigReload(' "$W/fetch/Hyprland-PropRefresher.cpp" "$W/fetch/Hyprland-legacy-ConfigManager.cpp"
grep -n 'reloadRequest\|"reload"\|misc:disable_autoreload' "$W/fetch/Hyprland-HyprCtl.cpp"

# 4. the committed counter, when it is in the lane (it was not at the freeze)
WORK=/fast/scratch/hyaku/mado-r56/c1-verify-$$; mkdir -p "$WORK"
if test -f "$LANE/quality/counters/c1-r56-autoreload-entry.py"; then
  python3 -I "$LANE/quality/counters/c1-r56-autoreload-entry.py" --repo "$LANE" --rev "$REV" --work "$WORK"
else
  echo "counter not present at $REV"
fi

# 5. host join: the live option, the version commit, the source list, the config files
hyprctl getoption misc:disable_autoreload -j
hyprctl version -j | grep '"commit"'
diff <(grep '^source' ~/.config/hypr/hyprland.conf) "$W/fetch/host-sources.txt" && echo "SOURCES SAME"
grep -rln 'disable_autoreload' ~/.config/hypr ~/.config/omarchy ~/.local/share/omarchy ~/.local/state/omarchy 2>/dev/null || echo "no host config names disable_autoreload"

# 6. the captured watched closure against the live filesystem (lstat only)
W="$W" python3 -I -c 'import os,stat;H=os.path.expanduser("~");L=[l.split("|",1)[1].strip().strip(chr(39)) for l in open(os.environ["W"]+"/fetch/host-watched-lstat.txt") if l.startswith("regular file|")];print(sum(stat.S_ISREG(os.lstat(p.replace("~",H,1)).st_mode) for p in L),"of",len(L),"regular")'
```
