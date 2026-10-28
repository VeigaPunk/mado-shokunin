# Correction to synthetic-dispatch propositions P16–P18

source: S370, S371; correction basis S374 — the round-52 non-author source-truth review. See `corpus/SOURCES.md` and the pins under `.ufo/waves/round-52/fetch/`.
verified-at: 2026-10-27
recheck: on-release

## Gate

This is a new, append-only correction to `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`; its original P16–P18 text is preserved as history and must not be used as current evidence. The original 15 propositions P01–P15 remain separate. The correction is source-level only; it makes no claim about a configured bind, a sent client event, or host behavior.

S374 re-opened this round: `corpus/lessons/round-52-verifier-spotcheck.md` §2 lines 38–40 says P16's quote was spliced, P17 misattributed, and P18 mislocalized. Its exact quote at §2 line 38, “P16 fails — the space-joined quote” (6 words), grounds the need for this correction, not the corrected Hyprland behavior.

## Corrected propositions

| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote (≤25 words) | Support |
|---|---|---|---|---|---|---|
| P19 | P16 | `Actions::pass` sends modifier state before its delivery branch; it sends a PRESSED keyboard key only when `m_passPressed == 1` and the key is not a mouse button. | S371 | Hyprland-ConfigActions.cpp:1554-1558 | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | direct — one contiguous excerpt carries the call order and branch condition. |
| P20 | P16 | After the key/button delivery branch, `Actions::pass` clears modifier state. | S371 | Hyprland-ConfigActions.cpp:1576 | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | direct — the clear call follows the delivery block. |
| P21 | P17 | `sendkeystate` calls `sendshortcut` again when its state is `repeat` and the first call succeeds. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:619-622 | `auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` | direct — the repeat branch is inside `sendkeystate` (lines 591–627); `sendshortcut` ends at line 589. |
| P22 | P18 | When key resolution leaves `keycode` unset after the scan, `sendshortcut` returns the `key not found` error from its cache-miss branch. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:573-574 | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` | direct — the scan ends at line 571, before this return. |

## Limits and review state

The four quotes are bounded to the cited lines and are intended as source facts, not proof of runtime delivery. A non-author reviewer must still verify each corrected proposition against the pinned bytes before this entry is admitted. The round-53 wave seats are lane-dispatched and do not provide that independent review. The r52 entry's original table is not rewritten; this note supersedes only P16–P18, not the rest of that entry.

## Correction (round 55)

| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote (≤25 words) | Support |
|---|---|---|---|---|---|---|
| P23 | P19 | `Actions::pass` sends modifier state before its delivery branch; it sends a PRESSED keyboard key only when `m_passPressed == 1` and the key is not a mouse button. The `== 0` arm sends a RELEASED key; `otherwise` (any other value) sends no key, and the `else` arm is not a PRESSED path. | S371 | Hyprland-ConfigActions.cpp:1554-1576 | … | direct |

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
