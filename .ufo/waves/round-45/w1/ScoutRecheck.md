# ScoutRecheck report (round 45 w1)

Findings: `.ufo/waves/round-45/w1/ScoutRecheck/drift.md`; pins of what was fetched: `.ufo/waves/round-45/w1/ScoutRecheck/fetch-main-sha256.txt` (files in `fetch-main/`, all at Hyprland main commit fb6e5380 / wiki main 6d26139c).

- Host = pins: `hyprctl version` commit efb50993..., pacman hyprland 0.56.2-4, hyprutils 0.14.2-1. v0.56.2 is still the newest release tag.
- Parser.cpp, MonitorRule.hpp, MonitorPositionController.cpp, MonitorRuleManager.cpp and the Monitor.cpp rule code: no semantic change on main (logging spelling; layer re-arrange removed after apply; transformed-size redraw).
- Structural: main removed the legacy hyprlang manager (a9902ea, 2026-07-22, #15539, not in v0.56.2): the `monitor =` handler (S303) is gone, Lua `hl.monitor{}` only, `sdr_eotf` is a Lua field; HyprCtl.cpp moved to ipc/s1/Commands.cpp (JSON + `hardwareDetails`); wiki Monitors.md moved and is Lua-only, no line form documented.
- Proposed `recheck:` text and the stale entry sentences are in drift.md sections 3-4.
- Scratch /fast/scratch/hyaku/mado-r45/ScoutRecheck removed on exit. No tools installed.
