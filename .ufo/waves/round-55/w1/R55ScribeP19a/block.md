
## Correction (round 55): P23 supersedes P19

source: S371 — pin `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` (sha256 a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637), base blob 3b55b6e.
verified-at: 2026-10-28
recheck: on-release

Append-only. P19 above is kept unedited as history; this block supersedes P19 only. Basis: round-54 closure routed defect 1 (M54-5; QUALITY 104).

| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote | Support |
|---|---|---|---|---|---|---|
| P23 | P19 | `Actions::pass` calls `sendKeyboardMods(modMask, 0, 0, 0)`, then branches on `S.m_passPressed`. If `m_passPressed == 1`: `isMouse` false (keyboard) sends one PRESSED keyboard key (`key - 8`); `isMouse` true (pointer) sends one PRESSED pointer button. If `m_passPressed == 0`: keyboard sends one RELEASED keyboard key; pointer sends one RELEASED pointer button. Otherwise (any other value, the `else` arm): keyboard sends a PRESSED keyboard key then a RELEASED keyboard key; pointer sends a PRESSED pointer button then a RELEASED pointer button. It ends with `sendKeyboardMods(0, 0, 0, 0)`. This corrects P19: its `only when m_passPressed == 1` is false, the `else` arm also sends a PRESSED keyboard key. | S371 | Hyprland-ConfigActions.cpp:1554-1576 | `if (S.m_passPressed == 1) {` | direct: lines 1554-1576 are one contiguous excerpt with the three arms and the keyboard/pointer split; where `m_passPressed` is set and which values reach `else` are not in the excerpt (see Not claimed). |

### Pinned lines (Q01–Q13, byte-equal to the round-52 pin after strip)

| ID | Pin:line | Quote |
|---|---|---|
| Q01 | Hyprland-ConfigActions.cpp:1554 | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` |
| Q02 | Hyprland-ConfigActions.cpp:1556 | `if (S.m_passPressed == 1) {` |
| Q03 | Hyprland-ConfigActions.cpp:1558 | `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` |
| Q04 | Hyprland-ConfigActions.cpp:1560 | `g_pSeatManager->sendPointerButton(S.m_timeLastMs, key, WL_POINTER_BUTTON_STATE_PRESSED);` |
| Q05 | Hyprland-ConfigActions.cpp:1561 | `} else if (S.m_passPressed == 0) {` |
| Q06 | Hyprland-ConfigActions.cpp:1563 | `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_RELEASED);` |
| Q07 | Hyprland-ConfigActions.cpp:1565 | `g_pSeatManager->sendPointerButton(S.m_timeLastMs, key, WL_POINTER_BUTTON_STATE_RELEASED);` |
| Q08 | Hyprland-ConfigActions.cpp:1566 | `} else {` |
| Q09 | Hyprland-ConfigActions.cpp:1568 | `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` |
| Q10 | Hyprland-ConfigActions.cpp:1569 | `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_RELEASED);` |
| Q11 | Hyprland-ConfigActions.cpp:1571 | `g_pSeatManager->sendPointerButton(S.m_timeLastMs, key, WL_POINTER_BUTTON_STATE_PRESSED);` |
| Q12 | Hyprland-ConfigActions.cpp:1572 | `g_pSeatManager->sendPointerButton(S.m_timeLastMs, key, WL_POINTER_BUTTON_STATE_RELEASED);` |
| Q13 | Hyprland-ConfigActions.cpp:1576 | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` |

### Not claimed

- Where `m_passPressed` is assigned: the pin excerpt only reads it; no setter is in the pinned lines and none is claimed.
- Which values reach the `else` arm at runtime: the pin shows the arm exists, not that any caller passes a value other than 0 or 1.
- Runtime delivery: no client, compositor or host event is claimed; this correction is source-level only.
- P23 is not reviewed by a non-author; the review gate in the entry's Limits section still applies.
