# ScoutRecheck - round-46 pin re-fetch and upstream-main comparison (2026-10-26)

Method: `curl -sfL` of each pin URL, `sha256sum`, compared to receipts/fetch-sha256.txt (and to the stored fetch/ copies). Main fetched from raw.githubusercontent.com `main`, plus GitHub API (tree, compare, tags). Scratch work deleted after copying. No host reads, no mutation.

## 1. Pin re-fetch: 10/10 IDENTICAL

| file | sha256 (first 16) | bytes | vs receipt |
|---|---|---|---|
| Hyprland-ConfigManager.cpp (src/config/legacy/) | 9db68cf44048d86557d8 | 90963 | SAME |
| Hyprland-ConfigValues.cpp | a76f05079454e1f6d440 | 59222 | SAME |
| Hyprland-HyprCtl.cpp (src/debug/) | 798b7c6c4c1684557842 | 97582 | SAME |
| Hyprland-IKeyboard.cpp | 8a800efe9baa7f375a3 | 15941 | SAME |
| Hyprland-InputManager.cpp | feedf32e2e3d23aeaed7 | 98845 | SAME |
| Hyprland-MiscFunctions.cpp | 065418241a3b40e21273 | 29785 | SAME |
| Hyprland-VirtualKeyboard.cpp (src/devices) | bc6d984a4c9e62313501 | 2253 | SAME |
| Hyprland-protocols-VirtualKeyboard.cpp | 43cbf7b39bf0910df6d9 | 6299 | SAME |
| hyprlang-config.cpp (v0.6.8) | fa1b6898f2f1676de73 | 43049 | SAME |
| wiki-Keywords.md (ecc06f3b...) | 11c0842cb31ddbfd55298 | 4810 | SAME |

Full 64-hex hashes matched the receipt lines; the stored fetch/ copies also match. Tag v0.56.2 resolves to commit efb50993780079460b0cbed1363e2166a2de1d9f (the pin commit); latest GitHub release is still v0.56.2 (2026-08-05); hyprlang latest tag still v0.6.8.

## 2. Upstream main (observed 2026-10-26; Hyprland main fb6e5380, hyprlang main 9508458b, wiki main 6d26139c)

Hyprland main vs the pin commit: `diverged`, 339 ahead / 36 behind (compare API). Main is a different line from the v0.56.2 release branch.

**Big finding: main is Lua-only for config.** `src/config/ConfigManager.cpp:31,34` builds `Lua::CConfigManager` in both branches; `src/config/legacy/` no longer exists in the tree (tree.json: 0 paths containing "legacy"). Hyprlang `hyprland.conf` `device {}` blocks do not exist on main; per-device config is `hl.device{...}`. The host (0.56.2) is still on the hyprlang/legacy path, so the entry's chain is correct for the host release and is NOT the main chain.

| item | v0.56.2 pin | main | verdict |
|---|---|---|---|
| applyConfigToKeyboard (InputManager.cpp pin:1213, main:1215) | - | logging swapped (`Log::logger->log`->`LOG`), the `activelayout` event now `IPC::Socket2::sock()->postEvent({"activelayout", "{},{}"})`; same getDeviceString(devname,"kb_*","input:kb_*") calls (main:1228-1233) | SEMANTICS UNCHANGED (diff of the function body: logging + event-post lines only) |
| device/global fallback getters | legacy ConfigManager | `Lua::CConfigManager::getDeviceString/Float` (src/config/lua/ConfigManager.cpp:~955-1000): device value used only if `setByUser()`, else global `input:*`; device name normalised ' '->'-' | same set-vs-unset rule; empty -> "" |
| device scroll_factor clamp (InputManager.cpp pin:1379-1380, main:1381-1382) | `std::clamp(...,0,100)` when explicitlySet, else -1 | identical | UNCHANGED |
| device-block scroll_factor | legacy default -1 (ConfigManager pin:545) | Lua field `{"scroll_factor", CLuaConfigFloat(1.F,0.F,100.F)}` (LuaBindingsConfigRules.cpp:262); parse-time range 0..100; -1 sentinel still comes from the explicitlySet gate | clamp same; default representation differs |
| GLOBAL `input:scroll_factor` / `input:touchpad:scroll_factor` max | `.max = 2` (ConfigValues.cpp pin:296,324) | `.max = 100` (main ConfigValues.cpp:380,409-410; wiki "[0 - 100]") | CHANGED on main. Pin's global max is 2, device clamp 100; the entry must not conflate them (census `scroll_factor_max=100` is the DEVICE clamp) |
| kb_layout/variant/options/rules/model/file defaults | in ConfigValues | diff of those lines: no change other than the scroll_factor max | UNCHANGED (Lua device `kb_layout` default "us", others empty, main LuaBindingsConfigRules.cpp:239-244) |
| devicesRequest (pin HyprCtl.cpp:748; main src/ipc/s1/Commands.cpp:781) | - | function body (178 lines) byte-identical (`diff` empty); incl. `"rules"`, `"layout"`, `scrollFactor {:.2f}` (main:803-823). File MOVED: src/debug/HyprCtl.cpp 404s on main, now src/ipc/s1/Commands.cpp; registered `legacyCommand("devices",...)` at :2000 | UNCHANGED, relocated |
| virtual naming | protocols/VirtualKeyboard.cpp:12 `name = "hl-virtual-keyboard"` | same line 12 | UNCHANGED (only include path `config/legacy/ConfigManager.hpp`->`config/ConfigManager.hpp`, LOGM->LOG, `isVirtual() const`) |
| IKeyboard.cpp | - | logging/ErrorOverlay formatting + one new include; setKeymap fallback logic untouched in the diff | UNCHANGED semantically |
| hyprlang main vs v0.6.8 | - | 8 commits ahead (d4037379..9508458b, 2026-01..08-11); config.cpp diff 95 lines: new `parseConfigName` (first '[' and "]:" instead of last ']') for `cat[key]:name` lines; `currentSpecialCategory = nullptr` reset after parse; `getAnyConfigValuePtr`; special-cat value erase | `device {}` block grammar not touched but the special-category reset and the `cat[key]:val` parse changed; the v0.6.8 pin is still right for the host (hyprlang 0.6.8-5) |
| Hyprland main hyprlang minimum | - | CMakeLists `HYPRLANG_MINIMUM_VERSION 0.6.7` still present | hyprlang still a dependency |
| wiki Keywords.md | content/Configuring/Keywords.md @ecc06f3b | 404 on main; wiki restructured to content/configuring/core/...; last change to old path 2026-04-26 e99eac80 "Update Configuration pages for the new lua configuration system (#1434)" | PIN MOVED/REMOVED upstream; pinned ecc06f3b URL still resolves |

## 3. Lua per-device input on main (the `device` search in src/config/lua)

- `hl.device(tbl)` registered at src/config/lua/bindings/LuaBindingsConfigRules.cpp:1369 (`setMgrFn(L, mgr, "device", hlDevice)`); implementation :1021-1075. `name` string required (error "'name' field is required"), spaces replaced with '-' (:1037-1038), unknown key -> `hl.device: unknown field` error (:1056-1058), then `scheduleRefresh(REFRESH_INPUT_DEVICES)`.
- Allowed fields = `DEVICE_FIELDS` (:235-...): sensitivity, accel_profile, rotation, kb_file, kb_layout, kb_variant, kb_options, kb_rules, kb_model, repeat_rate, repeat_delay, natural_scroll, tap_button_map, numlock_by_default, resolve_binds_by_sym, disable_while_typing, clickfinger_behavior, middle_button_emulation, tap_to_click, tap_and_drag, drag_lock, left_handed, scroll_method, scroll_button, scroll_button_lock, scroll_points, scroll_factor (0..100), output, enabled, keybinds, tags (plus others in the truncated rows, e.g. through line ~280).
- Lua object `hl.get_devices` (LuaBindingsQuery.cpp:451) and `HL.Device` userdata (objects/LuaDevice.cpp) expose runtime properties; wiki devices.md: "The `name` can be easily obtained by checking the output of `hyprctl devices`".
- Wiki (main content/configuring/core/devices.md): per-device keymap does not alter keybind keymap unless `resolve_binds_by_sym`.
- Config-file selection: `Jeremy::getMainConfigPath` (supplementary/jeremy/Jeremy.cpp) -> only a `recoverycfg.lua` special path and the regular path; no `.conf` string appears in Jeremy.cpp or src/config/ConfigManager.cpp.

## 4. Suggested recheck line for the entry
"Re-fetched 2026-10-26: all 10 pins hash-identical to the receipt. Upstream main (Hyprland fb6e5380, 339 commits ahead of efb50993 and 36 behind) is Lua-only (`hl.device{}`, no src/config/legacy, devicesRequest moved to src/ipc/s1/Commands.cpp, body identical); applyConfigToKeyboard and the device clamp 0..100 and the `hl-virtual-keyboard` name are unchanged; global input:scroll_factor max went 2 -> 100; hyprlang main is 8 commits past v0.6.8 (special-category parse changes). The chain documented applies to Hyprland 0.56.2 / hyprlang 0.6.8 only."

## 5. Unresolved
- Did not read the full DEVICE_FIELDS list past line ~262 nor whether main still ships a `.conf` converter. Not checked: other tags' contents.
- Main's VERSION file says 0.56.0 (observed `curl .../main/VERSION`), unexplained; do not cite it as a version.
- Tool state: no installs. Hashes of main files are not stored; re-derivable from the paths above.
