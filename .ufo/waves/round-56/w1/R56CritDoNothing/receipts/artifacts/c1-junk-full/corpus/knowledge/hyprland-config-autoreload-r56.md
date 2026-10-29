# Hyprland config auto-reload on 0.56.2 (critic junk control)

source: S383 S384 S385 S386 S387 S388 S389 S390
verified-at: 2026-10-28
recheck: 90d

## Rows

| id | proposition | src | pin:line | quote |
| --- | --- | --- | --- | --- |
| K01 | K01 pins line 492 of the pinned source and says that misc is part of the config reload path. | S384 | Hyprland-ConfigValues.cpp:492 | `"misc:disable_autoreload", "If true, the config will not reload automatically on save.", false` |
| K02 | K02 pins line 492 of the pinned source and says that refresh is part of the config reload path. | S384 | Hyprland-ConfigValues.cpp:492 | `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}` |
| K03 | K03 pins line 33 of the pinned source and says that CConfigValue is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:33 | `CConfigValue<Config::INTEGER>("misc:disable_autoreload");` |
| K04 | K04 pins line 34 of the pinned source and says that setWatchList is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:34 | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` |
| K05 | K05 pins line 46 of the pinned source and says that inotify_rm_watch is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:46 | `inotify_rm_watch(m_inotifyFd.get(), watch.wd);` |
| K06 | K06 pins line 54 of the pinned source and says that filesystem is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:54 | `std::filesystem::is_directory(path, ecDir);` |
| K07 | K07 pins line 55 of the pinned source and says that fileMask is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:55 | `fileMask      = IN_CLOSE_WRITE` |
| K08 | K08 pins line 56 of the pinned source and says that directoryMask is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:56 | `directoryMask = fileMask` |
| K09 | K09 pins line 60 of the pinned source and says that inotify_add_watch is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:60 | `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |
| K10 | K10 pins line 67 of the pinned source and says that IS_SYMLINK is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:67 | `if (!ec && !ec2 && IS_SYMLINK) {` |
| K11 | K11 pins line 69 of the pinned source and says that inotify_add_watch is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:69 | `inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE),` |
| K12 | K12 pins line 105 of the pinned source and says that m_watchCallback is part of the config reload path. | S383 | Hyprland-ConfigWatcher.cpp:105 | `m_watchCallback(SConfigWatchEvent{` |
| K13 | K13 pins line 128 of the pinned source and says that m_configWatcherInotifySource is part of the config reload path. | S386 | Hyprland-EventLoopManager.cpp:128 | `m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` |
| K14 | K14 pins line 71 of the pinned source and says that Config is part of the config reload path. | S386 | Hyprland-EventLoopManager.cpp:71 | `Config::watcher()->onInotifyEvent();` |
| K15 | K15 pins line 148 of the pinned source and says that m_propsTripped is part of the config reload path. | S385 | Hyprland-PropRefresher.cpp:148 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` |
| K16 | K16 pins line 149 of the pinned source and says that Config is part of the config reload path. | S385 | Hyprland-PropRefresher.cpp:149 | `Config::watcher()->update();` |
| K17 | K17 pins line 1079 of the pinned source and says that Config is part of the config reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1079 | `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {` |
| K18 | K18 pins line 1080 of the pinned source and says that CConfigManager is part of the config reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1080 | `CConfigManager: file {} modified, reloading` |
| K19 | K19 pins line 1070 of the pinned source and says that Config is part of the config reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1070 | `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` |
| K20 | K20 pins line 776 of the pinned source and says that m_configPaths is part of the config reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:776 | `m_configPaths.clear();` |
| K21 | K21 pins line 1836 of the pinned source and says that m_configPaths is part of the config reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1836 | `m_configPaths.emplace_back(value);` |
| K22 | K22 pins line 1835 of the pinned source and says that filesystem is part of the config reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1835 | `if (std::filesystem::is_regular_file(file_status)) {` |
| K23 | K23 pins line 1844 of the pinned source and says that source is part of the config reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1844 | `"source= skipping directory {}", value);` |
| K24 | K24 pins line 1816 of the pinned source and says that glob is part of the config reload path. | S387 | Hyprland-legacy-ConfigManager.cpp:1816 | `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())` |
| K25 | K25 pins line 65 of the pinned source and says that static is part of the config reload path. | S388 | Hyprland-MiscFunctions.cpp:65 | `static const char* const ENVHOME = getenv("HOME");` |
| K26 | K26 pins line 68 of the pinned source and says that auto is part of the config reload path. | S388 | Hyprland-MiscFunctions.cpp:68 | `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` |
| K27 | K27 pins line 1223 of the pinned source and says that COMMAND is part of the config reload path. | S389 | Hyprland-HyprCtl.cpp:1223 | `if (COMMAND.contains("misc:disable_autoreload"))` |
| K28 | K28 pins line 1276 of the pinned source and says that Config is part of the config reload path. | S389 | Hyprland-HyprCtl.cpp:1276 | `Config::mgr()->reload();` |
| K29 | K29 pins line 186 of the pinned source and says that File is part of the config reload path. | S390 | man7-inotify.7.html:186 | `File opened for writing was closed.` |
| K30 | K30 pins line 262 of the pinned source and says that dereference is part of the config reload path. | S390 | man7-inotify.7.html:262 | `Don't dereference <i>pathname</i> if it is a symbolic link.` |
| H01 | H01 is a host read of the pinned host dump and says that option is set in the live config. | host | host-getoption.json:1 | `"option": "misc:disable_autoreload", "int": 0` |
| H02 | H02 is a host read of the pinned host dump and says that source is set in the live config. | host | host-sources.txt:10 | `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| H03 | H03 is a host read of the pinned host dump and says that commit is set in the live config. | host | host-version.json:3 | `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"` |
