--- entry source line (r56 entry, line 1)
source: S383 (ConfigWatcher.cpp), S384 (ConfigValues.cpp), S385 (PropRefresher.cpp), S386 (EventLoopManager.cpp), S387 (legacy ConfigManager.cpp), S388 (MiscFunctions.cpp), S389 (HyprCtl.cpp), S390 (inotify(7) man page), S391 (PropRefresher.hpp); host captures cited as `host` in the H rows: host-getoption.json, host-version.json, host-sources.txt
--- registry rows S383-S391 (id/opened/expiry/usedby)
 S383  opened= 2026-10-28  expiry= on-release  usedby= corpus/knowledge/hyprland-config-autoreload-r56.md 
 S384  opened= 2026-10-28  expiry= on-release  usedby= corpus/knowledge/hyprland-config-autoreload-r56.md 
 S385  opened= 2026-10-28  expiry= on-release  usedby= corpus/knowledge/hyprland-config-autoreload-r56.md 
 S386  opened= 2026-10-28  expiry= on-release  usedby= corpus/knowledge/hyprland-config-autoreload-r56.md 
 S387  opened= 2026-10-28  expiry= on-release  usedby= corpus/knowledge/hyprland-config-autoreload-r56.md 
 S388  opened= 2026-10-28  expiry= on-release  usedby= corpus/knowledge/hyprland-config-autoreload-r56.md 
 S389  opened= 2026-10-28  expiry= on-release  usedby= corpus/knowledge/hyprland-config-autoreload-r56.md 
 S390  opened= 2026-10-28  expiry= 90d  usedby= corpus/knowledge/hyprland-config-autoreload-r56.md 
 S391  opened= 2026-10-28  expiry= on-release  usedby= corpus/knowledge/hyprland-config-autoreload-r56.md 
--- README index row line 82 (full)
| `knowledge/hyprland-config-autoreload-r56.md` (MADO-R56-1, round 56; config plane, Hyprland config auto-reload) | The Hyprland 0.56.2 (efb50993) chain from the `misc:disable_autoreload` declaration to the config watch list: `CConfigWatcher` registers the main config and every regular file its `source =` lines reach (glob and `~` rules), with file, directory and symlink-canonical inotify masks; a watched event leads through `CConfigManager::reload` to `REFRESH_ALL`. 30 upstream claims (K01-K30) and 3 host claims (H01-H03); each quote is byte-checked at its pin line, and sentence-to-pin entailment is not counted. Source-level and declared-config evidence only: no filesystem event was generated, no config file was saved and no reload was observed; the Lua config provider and runtime `hyprctl keyword` are outside the entry. | `source:` S383-S390 (opened 2026-10-28) in [SOURCES](SOURCES.md); pins under `.ufo/waves/round-56/fetch/`; host pins `.ufo/waves/round-56/fetch/host-version.json` and `.ufo/waves/round-56/fetch/host-getoption.json`; watch-list predictor `tools/mado-watchplan.py` (round-56 C2, read-only). |
--- README frontier bullet line 117 (full)
- Round 56 moves the Hyprland config auto-reload chain onto sourced ground ([config auto-reload](knowledge/hyprland-config-autoreload-r56.md), rows S383-S391 plus the host pins under `.ufo/waves/round-56/fetch/`): how `misc:disable_autoreload` reaches `CConfigWatcher`'s watch list (the main config and every regular file its `source =` lines reach, with glob and `~` rules), which inotify masks are registered for files, directories and symlink canonical targets, and how an event leads through `CConfigManager::reload` to `REFRESH_ALL` on Hyprland 0.56.2. A read-only join, `tools/mado-watchplan.py`, predicts the watch list from config bytes and joins the option to `hyprctl getoption -j`; constructs it does not model are reported `unsupported`, never guessed. Still open: no filesystem event was generated, no config file was saved and no reload was observed, so inotify delivery and the drawn effect of a reload stay unmeasured; the Lua config provider of later releases and runtime `hyprctl keyword misc:disable_autoreload` are outside this round.
--- entry K27/K28 rows
| K27 | The keyword dispatch guard tests whether COMMAND contains the misc:disable_autoreload text before it runs its body. | S389 | Hyprland-HyprCtl.cpp:1223 | `if (COMMAND.contains("misc:disable_autoreload"))` |
| K28 | The reload request handler calls reload on the object returned by Config::mgr() on this line. | S389 | Hyprland-HyprCtl.cpp:1276 | `Config::mgr()->reload();` |
--- entry E08/E09 rows
| E08 | The enum declares REFRESH_CONFIG_WATCHER as bit 8, the flag K02 attaches to misc:disable_autoreload and K15 tests in the refresher. | S391 | Hyprland-PropRefresher.hpp:18 | `REFRESH_CONFIG_WATCHER     = (1 << 8),` |
| E09 | REFRESH_ALL is defined as the maximum value of the enum's underlying type, which here is uint16_t, so every bit is set, including bit 8. | S391 | Hyprland-PropRefresher.hpp:21 | `REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),` |
--- counter frozen new_row_ids
['S383', 'S384', 'S385', 'S386', 'S387', 'S388', 'S389', 'S390'] denominator 8
