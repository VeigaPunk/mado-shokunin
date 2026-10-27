# Fixture entry (truthful) — same predicate verdict, propositions that hold

Fixture only. Same shape as the elided entry, same machine-checkable bindings, but every
proposition is one the located source actually states.

source: S380 - dispatcher table page (wiki) - `do not invoke any action immediately`(wiki-Dispatchers.md:15)
source: S381 - submap reset gate in the press path - `if (submapBefore == submapAfter)`(Hyprland-KeybindManager.cpp:822)

## Pin manifest

| pin | file | row |
|---|---|---|
| `wiki-Dispatchers.md` | content/Configuring/Dispatchers.md | S380 |
| `Hyprland-KeybindManager.cpp` | src/managers/KeybindManager.cpp | S381 |

## Propositions

| # | proposition | row | pin | quote | rationale |
|---|---|---|---|---|---|
| P1 | A dispatcher call returns a table and does not itself perform the action. | S380 | `wiki-Dispatchers.md:15` | `do not invoke any action immediately` | The negated predicate is inside the span, so the quote states the proposition directly. |
| P2 | Dispatcher table contents are not promised to be stable. | S380 | `wiki-Dispatchers.md:16` | `contents are not guaranteed to be stable at all` | The span carries the "not guaranteed" predicate that the proposition repeats. |
| P3 | The submap reset branch runs only when the submap name is unchanged across the dispatcher call. | S381 | `Hyprland-KeybindManager.cpp:822` | `if (submapBefore == submapAfter)` | The quote is the equality gate that guards the reset write. |
| P4 | The reset branch requires the reset field to be non-empty. | S381 | `Hyprland-KeybindManager.cpp:820` | `!k->submap.reset.empty()` | The negated emptiness test is inside the span, matching the proposition. |
| P5 | A reset is not applied by the submap dispatcher itself. | S381 | `Hyprland-KeybindManager.cpp:820` | `k->handler != "submap"` | The span carries the handler inequality the proposition states. |
