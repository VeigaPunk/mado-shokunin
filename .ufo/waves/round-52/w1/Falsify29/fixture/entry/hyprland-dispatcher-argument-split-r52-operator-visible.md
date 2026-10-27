# Fixture entry (operator visible) — same false propositions, negation kept inside the quote

Fixture only: constructed in seat scratch to test whether the frozen C2 machine-checkable
conditions can be met by propositions the source contradicts. Not a candidate entry.

source: S380 - dispatcher table page (wiki) - `do not invoke any action immediately`(wiki-Dispatchers.md:15)
source: S381 - submap reset gate in the press path - `if (submapBefore == submapAfter)`(Hyprland-KeybindManager.cpp:822)

## Pin manifest

| pin | file | row |
|---|---|---|
| `wiki-Dispatchers.md` | content/Configuring/Dispatchers.md | S380 |
| `Hyprland-KeybindManager.cpp` | src/managers/KeybindManager.cpp | S381 |

## Propositions

| # | proposition | row | pin | quote | rationale |
|---|---|---|---|---|---|---|
| P1 | A dispatcher call returns a table and does not itself perform the action. | S380 | `wiki-Dispatchers.md:15` | `do not invoke any action immediately` | The quote carries the negation: the page says dispatchers do not invoke anything at return time, only produce a table. |
| P2 | A dispatcher invokes its action immediately when it is called. | S380 | `wiki-Dispatchers.md:15` | `do not invoke any action immediately` | The quote names invocation on call, which is what the proposition states. |
| P3 | The submap reset branch runs only when the submap name is unchanged across the dispatcher call. | S381 | `Hyprland-KeybindManager.cpp:822` | `if (submapBefore == submapAfter)` | The quote is the equality gate that guards the reset write. |
| P4 | A bind's reset submap is applied when the reset field is empty. | S381 | `Hyprland-KeybindManager.cpp:820` | `!k->submap.reset.empty()` | The quote names the reset field's empty test that opens the branch. |
| P5 | The reset target is written unconditionally after the dispatcher call. | S381 | `Hyprland-KeybindManager.cpp:820-823` | `if (submapBefore == submapAfter)` | The quote is the write itself, which the entry reads as the branch body. |
