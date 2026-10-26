# Pins fetched by ExecErrataR45 (round-47 w2, R4b) — URL, sha256, what each pins

Fetched 2026-10-26 with `curl -sSL`. Nothing was installed; no package manager was run.
Every sha256 below is recomputed by `../verify-r45-errata.py` (pin table at the top of its output).

| file | url | sha256 | pins what |
|---|---|---|---|
| `aquamarine-v0.15.1.tar.gz` | https://codeload.github.com/hyprwm/aquamarine/tar.gz/refs/tags/v0.15.1 | `2f9de98c0bd1b7b1b09c576e390a2fef436449762fb334163c414f0c300296f2` | the whole v0.15.1 source tree, so E5's "only DRM assigns a description" is checked over every `.cpp`/`.hpp` in the tag (3 hits: `Output.hpp:258` declaration, `DRM.cpp:2101` assignment, `DRM.cpp:2104` log) |
| `aquamarine-Null-v0.15.1.cpp` | https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/Null.cpp | `9989fb17e3f95e22678b69c3683d74112c756155d36d8c4fa0c646a560c587b5` | the null backend sets no description (0 occurrences) — E5 universality |
| `aquamarine-Backend-v0.15.1.cpp` | https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/Backend.cpp | `4908c6f81e8183274c906eff4e0545555a7ac5842ba5a96df54c2383ec2620f7` | the backend base sets no description (0 occurrences) — E5 universality |
| `hyprland-ConfigManager-hpp-a9902ea.hpp` | https://raw.githubusercontent.com/hyprwm/Hyprland/a9902ea65f461af868497c4e74fed798ade0b1b0/src/config/ConfigManager.hpp | `389365c493c2507fe5be7f1c20670ef0af5308b585a3e71ad3fd3851009d9712` | at a9902ea the enum keeps `CONFIG_LUA` only (line 27): the `CONFIG_LEGACY` enumerator was removed from the **header**, not the `.cpp` — the E4 locator correction |

Also used read-only from the w1 seat (committed in the lane; `git ls-files` counts 22 files):
`.ufo/waves/round-47/w1/ScrErrataR45/pins/` — 16 files, all 16 sha256 match that seat's
`receipts/PINS.md` (recomputed in `../receipts/verify-r45-errata.txt`).
