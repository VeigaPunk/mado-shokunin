# Fixture A — four mapped propositions and one material proposition held only in prose

This fixture entry exists only to test the frozen C2 counter predicate. It states four
propositions in the table below. One further material proposition is held in prose without
a table row. The socket dispatch request never writes the press-state field, so a pass
issued from the socket replays both key edges of the event.

source: S401 - fixture socket dispatch request - pins/Hyprland-HyprCtl.cpp:1143-1157 - code - fixture
source: S402 - fixture submap action - pins/Hyprland-ConfigActions.cpp:1664-1682 - code - fixture
lane: fixture. round: 52. verified-at: 2026-10-27

## Pin manifest

| pin | file | row |
|---|---|---|
| `Hyprland-HyprCtl.cpp` | src/debug/HyprCtl.cpp | S401 |
| `Hyprland-ConfigActions.cpp` | src/config/shared/actions/ConfigActions.cpp | S402 |

## Propositions

| # | proposition | row | pin | quote | rationale |
|---|---|---|---|---|---|
| 1 | The socket dispatch request resolves the dispatcher name through the keybind manager's dispatcher map. | S401 | `Hyprland-HyprCtl.cpp:1149` | `g_pKeybindManager->m_dispatchers.find(DISPATCHSTR)` | The lookup names the keybind manager's map as the table searched. |
| 2 | An unmapped dispatcher name over the socket is answered with the literal text Invalid dispatcher. | S401 | `Hyprland-HyprCtl.cpp:1151` | `return "Invalid dispatcher"` | The miss branch returns that literal string to the caller. |
| 3 | A successful socket dispatch replies ok, and a failed one replies the dispatcher's own error text. | S401 | `Hyprland-HyprCtl.cpp:1157` | `return res.success ? "ok" : res.error` | The ternary selects the literal ok or the result's error field. |
| 4 | A named submap accepted by the scan is written into the process-wide current-submap field. | S402 | `Hyprland-ConfigActions.cpp:1674` | `Config::Actions::state()->m_currentSubmap = submap` | The assignment target is the process-wide action state field. |
