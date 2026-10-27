# Fixture B — four mapped propositions, one bound to a verbatim non-entailing quote

This fixture entry exists only to test the frozen C2 counter predicate. Every proposition
in the table carries a row, a pin path with a line span, a quote of at most twenty-five
words drawn verbatim from that span, and a written support rationale.

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
| 4 | The setSubmap action registers a previously unseen name as a submap, so a first switch always succeeds. | S402 | `Hyprland-ConfigActions.cpp:1664-1682` | `if (k->submap.name == submap)` | The scan walks the bind list and compares each stored submap name. |
