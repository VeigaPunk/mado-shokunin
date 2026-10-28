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

## Correction (round 55): P23 supersedes P19

This block is appended after the unchanged round-53 entry above. It adds one corrected proposition, P23, which supersedes P19 only. The original P19 row stays above as history and must not be used as current evidence. P20 through P22 and the rest of this entry are not changed here. The correction is source-level: it states what the pinned `Actions::pass` text in `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` tests and sends, and it makes no claim about a configured bind, a sent client event, or host behavior.

The P19 wording was false because it made the keyboard PRESSED send exclusive to the `m_passPressed == 1` branch. The pinned text shows the keyboard PRESSED call again in the arm that Q08 opens: Q09 sends a keyboard key PRESSED there, and Q10 sends the matching keyboard RELEASED, so a value that is neither 1 (Q02) nor 0 (Q05) reaches a keyboard PRESSED send. The old quote covered only the `== 1` text (Q01 to Q03), so it could not show the other two arms. P23 therefore states all three arms and the keyboard-versus-pointer split inside each.

Not claimed here: (a) where `m_passPressed` is set. The pin also writes it outside the quoted range: `sendKeyState` sets it to 1 or 0 around its `pass` calls (`Hyprland-ConfigActions.cpp:1603-1615`), and the header declares a default of -1 with the comment `-1 = dynamic (press+release)` (`Hyprland-ConfigActions.hpp:114`). This block does not say which setter reaches `pass` on any path. (b) which values reach the else arm. The else arm runs for any value other than 0 and 1; whether -1 or another value is stored when `pass` runs is not established here, and the `dynamic` comment is not evidence of it. (c) runtime delivery: that any send in any arm reaches a client, a focused window, or a keymap is not claimed. Pin sha256 is recorded in `verify.txt`; the non-author source-truth review named in the base entry is still required.

| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote | Support |
|---|---|---|---|---|---|---|
| P23 | P19 | `Actions::pass` sends modifier state (`sendKeyboardMods`) before its delivery branch and clears it after that branch. The branch tests `m_passPressed`. When `m_passPressed == 1`, a non-mouse key sends a keyboard key PRESSED and a mouse button sends a pointer button PRESSED. When `m_passPressed == 0`, a non-mouse key sends a keyboard key RELEASED and a mouse button sends a pointer button RELEASED. When `m_passPressed` is any other value (the `else` arm), a non-mouse key sends a keyboard key PRESSED and then a keyboard key RELEASED, and a mouse button sends a pointer button PRESSED and then a pointer button RELEASED. | S371 | Hyprland-ConfigActions.cpp:1554-1576 | Q01 to Q13 below | direct: Q01 to Q13 quote every call and branch test at the cited lines; runtime delivery not claimed. |

Branch table for P23 (keyboard and pointer split inside each branch):

| Branch | Non-mouse key (keyboard) | Mouse button (pointer) | Quotes |
|---|---|---|---|
| `m_passPressed == 1` | keyboard key PRESSED | pointer button PRESSED | Q02 to Q04 |
| `m_passPressed == 0` | keyboard key RELEASED | pointer button RELEASED | Q05 to Q07 |
| any other value (`else` arm) | keyboard key PRESSED, then keyboard key RELEASED | pointer button PRESSED, then pointer button RELEASED | Q08 to Q12 |

Quote rows for P23 (generated from `frozen-tables.json` `c3.q`; each quote is the stripped pin line):

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
