# Pins fetched by ScrErrataR45 (round-47 w1, R4b) — URL, sha256, and what each pins

All fetched 2026-10-26 with `curl -sSL`. Files live in this seat's `pins/`; every sha256 below is
recomputed in `receipts/verify-locators.txt` (last section). Nothing was installed; no package manager was run.

| file | url | sha256 | pins what |
|---|---|---|---|
| `hyprland-commit-a9902ea.json` | https://api.github.com/repos/hyprwm/Hyprland/commits/a9902ea65f461af868497c4e74fed798ade0b1b0 | `c33ba383407febf3133a3b86b018e180d98e22d354fb442384a20456bca00639` | commit date 2026-07-22T16:35:10Z, message `config: remove legacy config support (#15539)`, the file list and per-file patches (removal of `src/config/legacy/ConfigManager.cpp`, drop of `CONFIG_LEGACY` and of the `Legacy::CConfigManager` selection) |
| `legacy-cfg-a9902ea.txt` | https://raw.githubusercontent.com/hyprwm/Hyprland/a9902ea65f461af868497c4e74fed798ade0b1b0/src/config/legacy/ConfigManager.cpp | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` (14 bytes: `404: Not Found`) | the legacy line-form parser is gone at that commit |
| `hyprland-main-cfg-a9902ea.cpp` | https://raw.githubusercontent.com/hyprwm/Hyprland/a9902ea65f461af868497c4e74fed798ade0b1b0/src/config/ConfigManager.cpp | `41cecfacc1f988c58e787a489fcd54ad8e25279e39dfa6a491f06c4bb2648927` | only `Lua::CConfigManager` is instantiated (lines 30, 33); zero `Legacy` occurrences |
| `hyprland-lua-cfg-a9902ea.cpp` | https://raw.githubusercontent.com/hyprwm/Hyprland/a9902ea65f461af868497c4e74fed798ade0b1b0/src/config/lua/ConfigManager.cpp | `0dae53f27c5b5a1318be6fc5d5d679039d0738c5c5e4f5309b6ce1e2b2fb3435` | the rule manager is still driven on main (lines 809-810) |
| `hyprland-LuaBindingsConfigRules-a9902ea.cpp` | https://raw.githubusercontent.com/hyprwm/Hyprland/a9902ea65f461af868497c4e74fed798ade0b1b0/src/config/lua/bindings/LuaBindingsConfigRules.cpp | `87476570743302f8709f0168c50a22c5d035cb890490876f3ce575f5b60d0c7b` | monitor rules persist as Lua fields (`MONITOR_FIELDS[]`, line 80) feeding `CMonitorRuleParser` |
| `Hyprland-Monitor-efb5099.hpp` | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/output/Monitor.hpp | `4e9d88475f614f83015ed799d31425e35b47eb796dd91a4d8ec8f8ae88442621` | `m_enabled = false;` default (line 357) — a fresh monitor is disabled, so the enabled path is the `:302` fall-through |
| `aqua-DRM-v0.15.1.cpp` | https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/drm/DRM.cpp | `ff9b19d823a0f2f8b365ba7efd4b09bf9515fcfcdb10f3b1ae505abd6d1977b3` (byte-identical to the round-45 pin) | the only description assignment (`:2101`) |
| `aqua-Wayland-v0.15.1.cpp` | https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/Wayland.cpp | `1dd79e1cf212f5d13447c848fb83845d5d0491dfc897dce838165fe9449608fe` | zero `description` occurrences; `createOutput` sets the name only (168-181) |
| `aqua-Headless-v0.15.1.cpp` | https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/Headless.cpp | `2ecc7f54d033a85f6a7c5fa0e4eb14fc9e5e563be2146488e47b82a6358cbf02` | zero `description` occurrences; `createOutput` sets the name only (187-200) |
| `aqua-Output-v0.15.1.cpp` | https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/output/Output.cpp | `bb9351ba01ae04e2389763c8261ea5ba9ecc5de7f42ab9dff6566323cdc098ea` | zero `description` occurrences at the shared output layer |
| `aqua-Output.hpp` | https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/include/aquamarine/output/Output.hpp | `1568dcf54e01fc42079b5d68d7189d135f3a2c57aceed9cd0d3f58c964a5a37d` | `name, description, make, model, serial;` are default-empty (line 258) |
| `aqua-tree-v0.15.1.json` | https://api.github.com/repos/hyprwm/aquamarine/git/trees/v0.15.1?recursive=1 | `993c6284254cf6bc65d2430c15147107d286134040b012f67e3f77f0530e7cb5` | file listing used to locate the backend and output sources |
| `hyprland-config-contents.json` | https://api.github.com/repos/hyprwm/Hyprland/contents/src/config?ref=a9902ea65f461af868497c4e74fed798ade0b1b0 | `c664e891bb59444fba66c482303aeb63a2651482ecbc0122e77d01e147362d11` | `src/config/legacy` is absent at that commit |
| `hyprland-config-lua-contents.json` | https://api.github.com/repos/hyprwm/Hyprland/contents/src/config/lua?ref=a9902ea65f461af868497c4e74fed798ade0b1b0 | `cca2ee34528ef98a13c91501acd575a0f10f3b1f3938af057abe13f24edba00c` | lua config tree as fetched |
| `hyprland-lua-bindings-contents.json` | https://api.github.com/repos/hyprwm/Hyprland/contents/src/config/lua/bindings?ref=a9902ea65f461af868497c4e74fed798ade0b1b0 | `d492c4b402e82d9bc569b623b68b290ddc298b1fad105c728151e6ae2b9fdc13` | locates `LuaBindingsConfigRules.cpp` |
| `hyprland-config-tree.json` | https://api.github.com/repos/hyprwm/Hyprland/git/trees/81e755dfbfbae4ef3fb7551df1da262a43382f72 | `030874aee3d1073641a8d0af6052fdc390c57dd39f170ec17fe82c05cb86d3a5` | the **commit root** tree (not `src/config`; kept as fetched, superseded by the contents listings above) |

Related probes:

- `receipts/90d-probe.txt` — `GET /repos/hyprwm/Hyprland/commits/90d` -> 422 `No commit found for SHA: 90d`;
  full 40-hex sha -> 200.
- `receipts/pin-manifest-check.txt` — the fourteen round-45 pins on disk match
  `.ufo/waves/round-45/receipts/fetch-sha256.txt` (14/14 OK), so this errata reads the same bytes the entry was
  written against.
