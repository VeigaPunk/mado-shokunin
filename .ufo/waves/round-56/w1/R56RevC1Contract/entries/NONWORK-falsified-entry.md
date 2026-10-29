# Hyprland config auto-reload chain on 0.56.2 - NON-WORK FIXTURE

source: S383, S384, S385, S386, S387, S388, S389, S390
verified-at: 2026-10-28
recheck: on-release

NON-WORK red-team fixture (seat R56RevC1Contract). Not a knowledge claim.

## Rows

| K01 | The declaration of misc:disable_autoreload defaults to false and documents that true stops reloading on save. | S384 | Hyprland-ConfigValues.cpp:492 | `"misc:disable_autoreload", "If true, the config will not reload automatically on save.", false` |
| K02 | The same declaration tags misc:disable_autoreload with the refresh flag REFRESH_CONFIG_WATCHER, routing changes to the watcher. | S384 | Hyprland-ConfigValues.cpp:492 | `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}` |
| K03 | The watcher reads misc:disable_autoreload as an INTEGER config value when it is constructed. | S383 | Hyprland-ConfigWatcher.cpp:33 | `CConfigValue<Config::INTEGER>("misc:disable_autoreload");` |
| K04 | When the disable flag is set, setWatchList keeps only the main config path and drops every sourced file. | S383 | Hyprland-ConfigWatcher.cpp:34 | `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` |
| K05 | Each existing watch is removed with inotify_rm_watch before the watch list is rebuilt. | S383 | Hyprland-ConfigWatcher.cpp:46 | `inotify_rm_watch(m_inotifyFd.get(), watch.wd);` |
| K06 | The path is classified as a directory with std::filesystem::is_directory using an error code out-parameter. | S383 | Hyprland-ConfigWatcher.cpp:54 | `std::filesystem::is_directory(path, ecDir);` |
| K07 | The file mask is set to IN_CLOSE_WRITE, so a write that closes the file produces an event. | S383 | Hyprland-ConfigWatcher.cpp:55 | `fileMask      = IN_CLOSE_WRITE` |
| K08 | directoryMask is assigned from fileMask, so directories share the same flag set. | S383 | Hyprland-ConfigWatcher.cpp:56 | `directoryMask = fileMask` |
| K09 | Each path is registered with inotify_add_watch using the mask chosen for its type. | S383 | Hyprland-ConfigWatcher.cpp:60 | `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |
| K10 | A symlink entry adds the extra canonical watch only when neither error code is set and IS_SYMLINK holds. | S383 | Hyprland-ConfigWatcher.cpp:67 | `if (!ec && !ec2 && IS_SYMLINK) {` |
| K11 | The canonical target gets its own inotify_add_watch with IN_CLOSE_WRITE as the only mask bit. | S383 | Hyprland-ConfigWatcher.cpp:69 | `inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE),` |
| K12 | Each inotify event is delivered to the stored m_watchCallback as an SConfigWatchEvent value. | S383 | Hyprland-ConfigWatcher.cpp:105 | `m_watchCallback(SConfigWatchEvent{` |
| K13 | wl_event_loop_add_fd registers the watcher descriptor as a writable source, so the loop wakes when it can be written. | S386 | Hyprland-EventLoopManager.cpp:128 | `m_configWatcherInotifySource = wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr);` |
| K14 | The event loop calls onInotifyEvent on the watcher when the inotify descriptor becomes readable. | S386 | Hyprland-EventLoopManager.cpp:71 | `Config::watcher()->onInotifyEvent();` |
| K15 | The refresher checks whether the REFRESH_CONFIG_WATCHER bit is set in its tripped property mask. | S385 | Hyprland-PropRefresher.cpp:148 | `if (m_propsTripped & REFRESH_CONFIG_WATCHER)` |
| K16 | When that bit is set the refresher calls update on the config watcher to rebuild its watch list. | S385 | Hyprland-PropRefresher.cpp:149 | `Config::watcher()->update();` |
| K17 | The legacy config manager registers an onChange callback on the watcher through setOnChange. | S387 | Hyprland-legacy-ConfigManager.cpp:1079 | `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {` |
| K18 | The callback logs that a config file was modified and that reloading follows, using that wording. | S387 | Hyprland-legacy-ConfigManager.cpp:1080 | `CConfigManager: file {} modified, reloading` |
| K19 | The reload path schedules a REFRESH_ALL refresh through the supplementary refresher scheduleRefresh call. | S387 | Hyprland-legacy-ConfigManager.cpp:1070 | `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);` |
| K20 | m_configPaths.clear() keeps the sourced paths and only resets the main config path before a parse. | S387 | Hyprland-legacy-ConfigManager.cpp:776 | `m_configPaths.clear();` |
| K21 | Each accepted source value is appended to m_configPaths with emplace_back during the parse. | S387 | Hyprland-legacy-ConfigManager.cpp:1836 | `m_configPaths.emplace_back(value);` |
| K22 | Only a regular file is appended as a parsed config path; is_regular_file checks the file status. | S387 | Hyprland-legacy-ConfigManager.cpp:1835 | `if (std::filesystem::is_regular_file(file_status)) {` |
| K23 | A source value that names a directory is skipped with a log line saying skipping directory. | S387 | Hyprland-legacy-ConfigManager.cpp:1844 | `"source= skipping directory {}", value);` |
| K24 | The source path is expanded with glob using GLOB_TILDE after absolutePath resolves it against the current path. | S387 | Hyprland-legacy-ConfigManager.cpp:1816 | `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())` |
| K25 | ENVHOME caches the HOME environment variable through getenv at first use. | S388 | Hyprland-MiscFunctions.cpp:65 | `static const char* const ENVHOME = getenv("HOME");` |
| K26 | The directory of the current file is the part of currentPath before its last slash, found with find_last_of. | S388 | Hyprland-MiscFunctions.cpp:68 | `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` |
| K27 | The hyprctl keyword handler checks whether the command contains misc:disable_autoreload before dispatch. | S389 | Hyprland-HyprCtl.cpp:1223 | `if (COMMAND.contains("misc:disable_autoreload"))` |
| K28 | The keyword path calls reload on the config manager, which rereads the configuration. | S389 | Hyprland-HyprCtl.cpp:1276 | `Config::mgr()->reload();` |
| K29 | A file opened for writing that is then closed produces the close-write event that the watcher subscribes to. | S390 | man7-inotify.7.html:186 | `File opened for writing was closed.` |
| K30 | The watch is not followed when pathname is a symbolic link, because inotify does not dereference symbolic links. | S390 | man7-inotify.7.html:262 | `Don't dereference <i>pathname</i> if it is a symbolic link.` |
| H01 | The live getoption dump reports misc:disable_autoreload with int 0 on the host. | host | host-getoption.json:1 | `"option": "misc:disable_autoreload", "int": 0` |
| H02 | The host config tree sources the omarchy theme file hyprland.conf through its source line. | host | host-sources.txt:10 | `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| H03 | The host version record names the commit that the pinned source files were fetched at, as a full identifier. | host | host-version.json:3 | `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"` |
