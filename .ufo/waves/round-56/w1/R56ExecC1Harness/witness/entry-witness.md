# Witness: Hyprland config auto-reload

source: S383 S384 S385 S386 S387 S388 S389 S390
verified-at: 2026-10-28
recheck: on-release

| id | proposition | src | pin:line | quote |
|---|---|---|---|---|
| K01 | Row K01 witnesses the identifier misc in the pinned line for this entry | S384 | Hyprland-ConfigValues.cpp:492 | `"misc:disable_autoreload", "If true, the config will not reload automatically on save.", false` |
| K02 | Row K02 witnesses the identifier refresh in the pinned line for this entry | S384 | Hyprland-ConfigValues.cpp:492 | `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}` |
| K03 | Row K03 witnesses the identifier CConfigValue in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:33 | `CConfigValue<Config::INTEGER>("misc:disable_autoreload");` |
| K04 | Row K04 witnesses the identifier setWatchList in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:34 | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` |
| K05 | Row K05 witnesses the identifier inotify_rm_watch in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:46 | `inotify_rm_watch(m_inotifyFd.get(), watch.wd);` |
| K06 | Row K06 witnesses the identifier filesystem in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:54 | `std::filesystem::is_directory(path, ecDir);` |
| K07 | Row K07 witnesses the identifier fileMask in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:55 | `fileMask      = IN_CLOSE_WRITE` |
| K08 | Row K08 witnesses the identifier directoryMask in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:56 | `directoryMask = fileMask` |
| K09 | Row K09 witnesses the identifier inotify_add_watch in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:60 | `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |
| K10 | Row K10 witnesses the identifier IS_SYMLINK in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:67 | `if (!ec && !ec2 && IS_SYMLINK) {` |
| K11 | Row K11 witnesses the identifier inotify_add_watch in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:69 | `inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE),` |
| K12 | Row K12 witnesses the identifier m_watchCallback in the pinned line for this entry | S383 | Hyprland-ConfigWatcher.cpp:105 | `m_watchCallback(SConfigWatchEvent{` |
| K13 | Row K13 witnesses the identifier m_configWatcherInotifySource in the pinned line for this entry | S386 | Hyprland-EventLoopManager.cpp:128 | `m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` |
| K14 | Row K14 witnesses the identifier Config in the pinned line for this entry | S386 | Hyprland-EventLoopManager.cpp:71 | `Config::watcher()->onInotifyEvent();` |
| K15 | Row K15 witnesses the identifier m_propsTripped in the pinned line for this entry | S385 | Hyprland-PropRefresher.cpp:148 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` |
| K16 | Row K16 witnesses the identifier Config in the pinned line for this entry | S385 | Hyprland-PropRefresher.cpp:149 | `Config::watcher()->update();` |
| K17 | Row K17 witnesses the identifier Config in the pinned line for this entry | S387 | Hyprland-legacy-ConfigManager.cpp:1079 | `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {` |
| K18 | Row K18 witnesses the identifier CConfigManager in the pinned line for this entry | S387 | Hyprland-legacy-ConfigManager.cpp:1080 | `CConfigManager: file {} modified, reloading` |
| K19 | Row K19 witnesses the identifier Config in the pinned line for this entry | S387 | Hyprland-legacy-ConfigManager.cpp:1070 | `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` |
| K20 | Row K20 witnesses the identifier m_configPaths in the pinned line for this entry | S387 | Hyprland-legacy-ConfigManager.cpp:776 | `m_configPaths.clear();` |
| K21 | Row K21 witnesses the identifier m_configPaths in the pinned line for this entry | S387 | Hyprland-legacy-ConfigManager.cpp:1836 | `m_configPaths.emplace_back(value);` |
| K22 | Row K22 witnesses the identifier filesystem in the pinned line for this entry | S387 | Hyprland-legacy-ConfigManager.cpp:1835 | `if (std::filesystem::is_regular_file(file_status)) {` |
| K23 | Row K23 witnesses the identifier source in the pinned line for this entry | S387 | Hyprland-legacy-ConfigManager.cpp:1844 | `"source= skipping directory {}", value);` |
| K24 | Row K24 witnesses the identifier glob in the pinned line for this entry | S387 | Hyprland-legacy-ConfigManager.cpp:1816 | `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())` |
| K25 | Row K25 witnesses the identifier static in the pinned line for this entry | S388 | Hyprland-MiscFunctions.cpp:65 | `static const char* const ENVHOME = getenv("HOME");` |
| K26 | Row K26 witnesses the identifier auto in the pinned line for this entry | S388 | Hyprland-MiscFunctions.cpp:68 | `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` |
| K27 | Row K27 witnesses the identifier COMMAND in the pinned line for this entry | S389 | Hyprland-HyprCtl.cpp:1223 | `if (COMMAND.contains("misc:disable_autoreload"))` |
| K28 | Row K28 witnesses the identifier Config in the pinned line for this entry | S389 | Hyprland-HyprCtl.cpp:1276 | `Config::mgr()->reload();` |
| K29 | Row K29 witnesses the identifier File in the pinned line for this entry | S390 | man7-inotify.7.html:186 | `File opened for writing was closed.` |
| K30 | Row K30 witnesses the identifier dereference in the pinned line for this entry | S390 | man7-inotify.7.html:262 | `Don't dereference <i>pathname</i> if it is a symbolic link.` |
| H01 | Row H01 witnesses the identifier option in the pinned line for this entry | host | host-getoption.json:1 | `"option": "misc:disable_autoreload", "int": 0` |
| H02 | Row H02 witnesses the identifier source in the pinned line for this entry | host | host-sources.txt:10 | `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| H03 | Row H03 witnesses the identifier commit in the pinned line for this entry | host | host-version.json:3 | `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"` |
