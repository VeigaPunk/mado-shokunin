# Hyprland config auto-reload on 0.56.2 (critic junk control)

source: S383 S384 S385 S386 S387 S388 S389 S390
verified-at: 2026-10-28
recheck: 90d

## Rows

| id | proposition | src | pin:line | quote |
| --- | --- | --- | --- | --- |
| K01 | placeholder proposition text for row K01, not a claim about any source line | S384 | Hyprland-ConfigValues.cpp:492 | `"misc:disable_autoreload", "If true, the config will not reload automatically on save.", false` |
| K02 | placeholder proposition text for row K02, not a claim about any source line | S384 | Hyprland-ConfigValues.cpp:492 | `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}` |
| K03 | placeholder proposition text for row K03, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:33 | `CConfigValue<Config::INTEGER>("misc:disable_autoreload");` |
| K04 | placeholder proposition text for row K04, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:34 | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` |
| K05 | placeholder proposition text for row K05, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:46 | `inotify_rm_watch(m_inotifyFd.get(), watch.wd);` |
| K06 | placeholder proposition text for row K06, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:54 | `std::filesystem::is_directory(path, ecDir);` |
| K07 | placeholder proposition text for row K07, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:55 | `fileMask      = IN_CLOSE_WRITE` |
| K08 | placeholder proposition text for row K08, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:56 | `directoryMask = fileMask` |
| K09 | placeholder proposition text for row K09, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:60 | `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |
| K10 | placeholder proposition text for row K10, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:67 | `if (!ec && !ec2 && IS_SYMLINK) {` |
| K11 | placeholder proposition text for row K11, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:69 | `inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE),` |
| K12 | placeholder proposition text for row K12, not a claim about any source line | S383 | Hyprland-ConfigWatcher.cpp:105 | `m_watchCallback(SConfigWatchEvent{` |
| K13 | placeholder proposition text for row K13, not a claim about any source line | S386 | Hyprland-EventLoopManager.cpp:128 | `m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` |
| K14 | placeholder proposition text for row K14, not a claim about any source line | S386 | Hyprland-EventLoopManager.cpp:71 | `Config::watcher()->onInotifyEvent();` |
| K15 | placeholder proposition text for row K15, not a claim about any source line | S385 | Hyprland-PropRefresher.cpp:148 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` |
| K16 | placeholder proposition text for row K16, not a claim about any source line | S385 | Hyprland-PropRefresher.cpp:149 | `Config::watcher()->update();` |
| K17 | placeholder proposition text for row K17, not a claim about any source line | S387 | Hyprland-legacy-ConfigManager.cpp:1079 | `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {` |
| K18 | placeholder proposition text for row K18, not a claim about any source line | S387 | Hyprland-legacy-ConfigManager.cpp:1080 | `CConfigManager: file {} modified, reloading` |
| K19 | placeholder proposition text for row K19, not a claim about any source line | S387 | Hyprland-legacy-ConfigManager.cpp:1070 | `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` |
| K20 | placeholder proposition text for row K20, not a claim about any source line | S387 | Hyprland-legacy-ConfigManager.cpp:776 | `m_configPaths.clear();` |
| K21 | placeholder proposition text for row K21, not a claim about any source line | S387 | Hyprland-legacy-ConfigManager.cpp:1836 | `m_configPaths.emplace_back(value);` |
| K22 | placeholder proposition text for row K22, not a claim about any source line | S387 | Hyprland-legacy-ConfigManager.cpp:1835 | `if (std::filesystem::is_regular_file(file_status)) {` |
| K23 | placeholder proposition text for row K23, not a claim about any source line | S387 | Hyprland-legacy-ConfigManager.cpp:1844 | `"source= skipping directory {}", value);` |
| K24 | placeholder proposition text for row K24, not a claim about any source line | S387 | Hyprland-legacy-ConfigManager.cpp:1816 | `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())` |
| K25 | placeholder proposition text for row K25, not a claim about any source line | S388 | Hyprland-MiscFunctions.cpp:65 | `static const char* const ENVHOME = getenv("HOME");` |
| K26 | placeholder proposition text for row K26, not a claim about any source line | S388 | Hyprland-MiscFunctions.cpp:68 | `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` |
| K27 | placeholder proposition text for row K27, not a claim about any source line | S389 | Hyprland-HyprCtl.cpp:1223 | `if (COMMAND.contains("misc:disable_autoreload"))` |
| K28 | placeholder proposition text for row K28, not a claim about any source line | S389 | Hyprland-HyprCtl.cpp:1276 | `Config::mgr()->reload();` |
| K29 | placeholder proposition text for row K29, not a claim about any source line | S390 | man7-inotify.7.html:186 | `File opened for writing was closed.` |
| K30 | placeholder proposition text for row K30, not a claim about any source line | S390 | man7-inotify.7.html:262 | `Don't dereference <i>pathname</i> if it is a symbolic link.` |
| H01 | placeholder host proposition H01, not a read | host | host-getoption.json:1 | `"option": "misc:disable_autoreload", "int": 0` |
| H02 | placeholder host proposition H02, not a read | host | host-sources.txt:10 | `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| H03 | placeholder host proposition H03, not a read | host | host-version.json:3 | `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"` |
