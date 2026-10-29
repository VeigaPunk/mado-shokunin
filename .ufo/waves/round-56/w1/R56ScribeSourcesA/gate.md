# R56ScribeSourcesA — source gate for rows S383-S390

Access date registered for every row: 2026-10-28. Quotes were copied from the pinned bytes in
`.ufo/waves/round-56/fetch/` (sha256 equal to `frozen-tables.json` c1.pin_sha256 / host map) and
located by line number in that pin. Pinned tag/commit: efb50993780079460b0cbed1363e2166a2de1d9f (Hyprland v0.56.2).

| row | URL | access date | located quote (pin line) |
|---|---|---|---|
| S383 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/inotify/ConfigWatcher.cpp | 2026-10-28 | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` (Hyprland-ConfigWatcher.cpp line 34) |
| S384 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp | 2026-10-28 | `"If true, the config will not reload automatically on save."` (Hyprland-ConfigValues.cpp line 492) |
| S385 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.cpp | 2026-10-28 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` (line 148) and `Config::watcher()->update();` (line 149) |
| S386 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/eventLoop/EventLoopManager.cpp | 2026-10-28 | `wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` (Hyprland-EventLoopManager.cpp line 128) |
| S387 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp | 2026-10-28 | `Log::logger->log(Log::DEBUG, "CConfigManager: file {} modified, reloading", e.file);` (Hyprland-legacy-ConfigManager.cpp line 1080) and `Log::logger->log(Log::WARN, "source= skipping directory {}", value);` (line 1844) |
| S388 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp | 2026-10-28 | `static const char* const ENVHOME = getenv("HOME");` (Hyprland-MiscFunctions.cpp line 65) and `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` (line 68) |
| S389 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | 2026-10-28 | `if (COMMAND.contains("misc:disable_autoreload"))` (Hyprland-HyprCtl.cpp line 1223) and `Config::mgr()->reload();` (line 1276) |
| S390 | https://man7.org/linux/man-pages/man7/inotify.7.html | 2026-10-28 | `File opened for writing was closed.` (man7-inotify.7.html line 186) and `Don't dereference <i>pathname</i> if it is a symbolic link.` (line 262) |
