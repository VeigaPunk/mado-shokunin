# Hyprland config auto-reload chain on 0.56.2 - NON-WORK FIXTURE

source: S383, S384, S385, S386, S387, S388, S389, S390
verified-at: 2026-10-28
recheck: on-release

NON-WORK red-team fixture (seat R56RevC1Contract). Not a knowledge claim.

## Rows

| K01 | Line 492 of the pinned file holds misc, which this row cites for the reload path. | S384 | Hyprland-ConfigValues.cpp:492 | `"misc:disable_autoreload", "If true, the config will not reload automatically on save.", false` |
| K02 | Line 492 of the pinned file holds refresh, which this row cites for the reload path. | S384 | Hyprland-ConfigValues.cpp:492 | `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}` |
| K03 | Line 33 of the pinned file holds CConfigValue, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:33 | `CConfigValue<Config::INTEGER>("misc:disable_autoreload");` |
| K04 | Line 34 of the pinned file holds setWatchList, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:34 | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` |
| K05 | Line 46 of the pinned file holds inotify_rm_watch, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:46 | `inotify_rm_watch(m_inotifyFd.get(), watch.wd);` |
| K06 | Line 54 of the pinned file holds filesystem, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:54 | `std::filesystem::is_directory(path, ecDir);` |
| K07 | Line 55 of the pinned file holds fileMask, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:55 | `fileMask      = IN_CLOSE_WRITE` |
| K08 | Line 56 of the pinned file holds directoryMask, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:56 | `directoryMask = fileMask` |
| K09 | Line 60 of the pinned file holds inotify_add_watch, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:60 | `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |
| K10 | Line 67 of the pinned file holds IS_SYMLINK, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:67 | `if (!ec && !ec2 && IS_SYMLINK) {` |
| K11 | Line 69 of the pinned file holds inotify_add_watch, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:69 | `inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE),` |
| K12 | Line 105 of the pinned file holds m_watchCallback, which this row cites for the reload path. | S383 | Hyprland-ConfigWatcher.cpp:105 | `m_watchCallback(SConfigWatchEvent{` |
| K13 | Line 128 of the pinned file holds m_configWatcherInotifySource, which this row cites for the reload path. | S386 | Hyprland-EventLoopManager.cpp:128 | `m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` |
| K14 | Line 71 of the pinned file holds Config, which this row cites for the reload path. | S386 | Hyprland-EventLoopManager.cpp:71 | `Config::watcher()->onInotifyEvent();` |
| K15 | Line 148 of the pinned file holds m_propsTripped, which this row cites for the reload path. | S385 | Hyprland-PropRefresher.cpp:148 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` |
| K16 | Line 149 of the pinned file holds Config, which this row cites for the reload path. | S385 | Hyprland-PropRefresher.cpp:149 | `Config::watcher()->update();` |
| K17 | Line 1079 of the pinned file holds Config, which this row cites for the reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1079 | `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {` |
| K18 | Line 1080 of the pinned file holds CConfigManager, which this row cites for the reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1080 | `CConfigManager: file {} modified, reloading` |
| K19 | Line 1070 of the pinned file holds Config, which this row cites for the reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1070 | `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` |
| K20 | Line 776 of the pinned file holds m_configPaths, which this row cites for the reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:776 | `m_configPaths.clear();` |
| K21 | Line 1836 of the pinned file holds m_configPaths, which this row cites for the reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1836 | `m_configPaths.emplace_back(value);` |
| K22 | Line 1835 of the pinned file holds filesystem, which this row cites for the reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1835 | `if (std::filesystem::is_regular_file(file_status)) {` |
| K23 | Line 1844 of the pinned file holds source, which this row cites for the reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1844 | `"source= skipping directory {}", value);` |
| K24 | Line 1816 of the pinned file holds glob, which this row cites for the reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1816 | `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())` |
| K25 | Line 65 of the pinned file holds static, which this row cites for the reload path. | S388 | Hyprland-MiscFunctions.cpp:65 | `static const char* const ENVHOME = getenv("HOME");` |
| K26 | Line 68 of the pinned file holds auto, which this row cites for the reload path. | S388 | Hyprland-MiscFunctions.cpp:68 | `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` |
| K27 | Line 1223 of the pinned file holds COMMAND, which this row cites for the reload path. | S389 | Hyprland-HyprCtl.cpp:1223 | `if (COMMAND.contains("misc:disable_autoreload"))` |
| K28 | Line 1276 of the pinned file holds Config, which this row cites for the reload path. | S389 | Hyprland-HyprCtl.cpp:1276 | `Config::mgr()->reload();` |
| K29 | Line 186 of the pinned file holds File, which this row cites for the reload path. | S390 | man7-inotify.7.html:186 | `File opened for writing was closed.` |
| K30 | Line 262 of the pinned file holds dereference, which this row cites for the reload path. | S390 | man7-inotify.7.html:262 | `Don't dereference <i>pathname</i> if it is a symbolic link.` |
| H01 | Host capture H01 records option on line 1 of the host pin. | host | host-getoption.json:1 | `"option": "misc:disable_autoreload", "int": 0` |
| H02 | Host capture H02 records source on line 10 of the host pin. | host | host-sources.txt:10 | `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| H03 | Host capture H03 records commit on line 3 of the host pin. | host | host-version.json:3 | `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"` |
