# Fixture entry — proposition-map completeness attack (seat Falsify14, round 52)

This is a seat-local synthetic fixture. Rows S900-S903 are fixture-only stubs and
never enter the lane registry. Pin bytes are byte-copies of the round-51 fetched
pins at Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` (see fixture/pins/SHA256SUMS).

source: S900 - dispatcher population forwarder - fixture stub - code - one closure stored for every name - `m_dispatchers[name] = [n = std::string(name)](std::string args) -> SDispatchResult { return Config::Legacy::translator()->run(n, args); };`(Hyprland-KeybindManager.cpp:113)
source: S901 - press-time lookup - fixture stub - code - stored handler name is the map key, mouse binds rewrite to "mouse" - `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`(Hyprland-KeybindManager.cpp:785)
source: S902 - dispatch result defaults - fixture stub - code - passEvent defaults false - `bool        passEvent = false;`(Hyprland-SharedDefs.hpp:53)
source: S903 - long-press timer call - fixture stub - code - closure called with stored arg outside the press loop - `DISPATCHER->second(m_lastLongPressKeybind->arg);`(Hyprland-KeybindManager.cpp:131)

## Proposition map

| id | proposition | row | pin:line | quote | support rationale |
|---|---|---|---|---|---|
| P1 | Every dispatcher name in the population is stored with the same forwarder closure | S900 | Hyprland-KeybindManager.cpp:113 | `m_dispatchers[name] = [n = std::string(name)](std::string args) -> SDispatchResult { return Config::Legacy::translator()->run(n, args); };` | the assignment is the single population statement and names no per-name branch |
| P2 | A press looks up the stored handler name in m_dispatchers, rewriting mouse binds to the name mouse | S901 | Hyprland-KeybindManager.cpp:785 | `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);` | the find's key expression is exactly the stored handler or the literal mouse |
| P3 | A dispatcher result defaults passEvent to false, so a default return does not swallow the event | S902 | Hyprland-SharedDefs.hpp:53 | `bool        passEvent = false;` | the field's declared default is the value a nothing-returning dispatcher leaves behind |
| P4 | The long-press timer calls the dispatcher closure with the stored argument, bypassing the press loop | S903 | Hyprland-KeybindManager.cpp:131 | `DISPATCHER->second(m_lastLongPressKeybind->arg);` | the call passes the stored arg and sits in the long-press callback, not the press path |

## Chain

1. **Population.** Every name shares one closure (P1, S900).
2. **Press lookup.** The press path resolves the stored name, with the mouse rewrite (P2, S901).
3. **Result defaults.** An empty return leaves passEvent at its false default (P3, S902).
4. **Repeat behaviour.** The repeat timer also calls the closure directly
   `DISPATCHER->second(k->arg);` (Hyprland-KeybindManager.cpp:154), and neither timer writes the
   press field, so a repeated or long-held bind replays its dispatcher with the press field left
   at the cleared sentinel - meaning a repeated `pass` replays both key edges regardless of the
   edge that fired the repeat.
5. **Long press.** The long-press timer path bypasses the press loop with the stored argument (P4, S903).

## Limits

- Fixture only; rows S900-S903 are stubs. Quotes are byte-copies from the pinned round-51 fetch.
