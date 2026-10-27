# Falsify22 fixture entry: a proposition map with a smuggled unmapped claim

This fixture demonstrates that the frozen C2 predicate's counter checks
(proposition count, row/pin/quote bindings, index) all pass while a material
factual proposition outside the declared map — a false one — goes undetected.
It reuses round-51-opened rows S364-S367 and the round-51 fetch pins because the
demonstration is about the check machinery, not about round-52 novelty.

lane: mado-shokunin. seat: Falsify22. fixture: yes, not a corpus candidate.

## Propositions

| # | proposition | row | pin | quote | rationale |
|---|---|---|---|---|---|
| P1 | The keybind manager populates its dispatch table in the constructor, one closure per name, forwarding every name to the legacy translator. | S364 | Hyprland-KeybindManager.cpp | `m_dispatchers[name] = [n = std::string(name)](std::string args) -> SDispatchResult { return Config::Legacy::translator()->run(n, args); };` | Brace-list population loop at src/managers/KeybindManager.cpp:42-113 assigns the same translator-forwarding lambda to every name; the table exists before any config is read. |
| P2 | A config-time bind line validates its dispatcher word against the same table a press consults, rejecting an unknown name before any press. | S368 | Hyprland-legacy-ConfigManager.cpp | `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER);` | The parse path looks the folded word up at src/config/legacy/ConfigManager.cpp:1594 and rejects a miss at :1598, so an accepted name is a config-time commitment. |
| P3 | The hyprctl socket verb enters the same table: it splits the request at the first space and looks the leading word up directly. | S366 | Hyprland-HyprCtl.cpp | `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);` | dispatchRequest at src/debug/HyprCtl.cpp:1143-1149 takes the head before the first space as the name and finds it in m_dispatchers, the same member the press path uses. |
| P4 | Resetting the current submap writes the empty string into one process-wide field owned by the actions state. | S367 | Hyprland-ConfigActions.cpp | `Config::Actions::state()->m_currentSubmap = "";` | The submap action's reset form assigns the empty literal at src/config/shared/actions/ConfigActions.cpp:1666 to the shared state field, so every keyboard observes the same value. |

## Observations

**OBS** S366: `return res.success ? "ok" : res.error;` (Hyprland-HyprCtl.cpp:1157) - the
socket answer is the dispatcher's own text.
**OBS** S364/S366: Both front doors normalize the dispatcher name the same way: the
socket verb lowercases the name before the table lookup, so
`hyprctl dispatch EXEC xterm` reaches the same callable as `hyprctl dispatch exec
xterm`.
