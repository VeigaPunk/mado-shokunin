
## Errata (round 47, 2026-10-26; append-only — the text above stands as landed at 4d22eeb)

- E1 — line 84, locator. The monitor-added emit is reached only by the fall-through that sets `m_enabled = true;`
  (Hyprland-Monitor.cpp:302) and fires at Hyprland-Monitor.cpp:389; the veto is the disabled branch,
  `if (monitorRule.m_disabled) {` (Hyprland-Monitor.cpp:275) through `m_enabled = false;` (:283) and `return;` (:286).
  The landed citation `Hyprland-Monitor.cpp:264` is the already-enabled path of `CMonitor::onConnect`
  (Hyprland-Monitor.cpp:108), which applies the rule and returns at :271 before the emit. Corrected citation:
  Hyprland-Monitor.cpp:275-287 and :389 (fresh pin: Hyprland-Monitor-efb5099.hpp:357, `m_enabled = false;`).
  The claim is unchanged.
- E2 — line 96, provenance. The cited receipt `.ufo/waves/round-45/receipts/live-monitors-host-l1.txt` is a run of
  `l1-draft/mado-monitors.py` (`# tool sha256 c6ac5fc2…`, line 4), not of `tools/mado-monitors.py`. The landed tool
  at 4d22eeb is sha256 2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609, and its receipt
  `.ufo/waves/round-45/receipts/live-monitors-host-r45.txt` prints the same lines (`verdict=AGREE` line 7,
  `verdict=OK` line 8, `exit=0` line 9, `# tool sha256 2f007417…` line 4). Corrected citation: that receipt.
- E3 — line 98, claim. The custom-mode push is guarded by three negated strict bounds of 1 px / 1 px / 1 Hz
  (Hyprland-Monitor.cpp:836-837; Hyprland-macros.hpp:40). With the rule at 3440x1440@100 and the applied mode at
  99.997 Hz, |99.997 - 100.000| = 0.003 < 1 and both pixel dimensions match exactly, so the push at
  Hyprland-Monitor.cpp:838-839 cannot execute: the requested 100 Hz counted as close and no custom mode was tried
  (an accepted custom mode would have set Hyprland-Monitor.cpp:903 to 100.000). The branch is determined by source
  plus dump, not open; only the UNK at line 100 remains.
- E4 — line 18, pin. "Upstream main already drops the legacy hyprlang manager" is pinned at
  a9902ea65f461af868497c4e74fed798ade0b1b0, 2026-07-22T16:35:10Z, "config: remove legacy config support (#15539)":
  it removes src/config/legacy/ConfigManager.cpp (2184 deletions) and the `Legacy`/`CONFIG_LEGACY` selection in
  src/config/ConfigManager.cpp (which now instantiates only `Lua::CConfigManager`); the raw file 404s at that
  commit. Claim stands.
- E5 — line 106, claim. At aquamarine v0.15.1 neither the Wayland nor the headless backend sets a description:
  src/backend/Wayland.cpp and src/backend/Headless.cpp contain no occurrence of the field (they set only the
  output name), src/output/Output.cpp sets none, and `name, description, make, model, serial;` are default-empty
  strings (include/aquamarine/output/Output.hpp:258); only src/backend/drm/DRM.cpp:2101 assigns one. So a
  non-DRM output reaches Hyprland-Monitor.cpp:250 with an empty description and an empty short description
  (:255-256) — the backends build none, rather than building one differently. Not observed on this host, whose
  only output is DRM. Original wording replaced by this sentence.
- E6 — line 107, pin and scope. Same commit as E4 removes the file that carries the `monitor` keyword handler
  (the handler row the entry's source list cites), so the `monitor =` line form is gone on main. Monitor rules
  are not: the Lua binding still parses them (src/config/lua/bindings/LuaBindingsConfigRules.cpp:80,
  `MONITOR_FIELDS[]` feeding `CMonitorRuleParser`) and the Lua manager still drives the rule manager
  (src/config/lua/ConfigManager.cpp:809-810). Claim stands with that scope.
