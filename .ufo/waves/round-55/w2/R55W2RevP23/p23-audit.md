# P23 sentence-to-pin audit (round 55, seat R55W2RevP23)

Target: the appended block `## Correction (round 55): P23 supersedes P19` at the end of
`corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`, lane revision
`57584ed67716340b3d466fa04333ac0bab3fb79e` (line numbers below are that file's lines).
Pin: `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` (+ `.hpp`), upstream `efb50993780079460b0cbed1363e2166a2de1d9f`.

Labels: **SUPPORTED** = the pinned bytes directly establish the sentence as written.
**HELD** = true on the pin, but rests on an unquoted premise or omits a qualifier; the minimal fix is given.
**OVERREACH** = the sentence goes beyond, or is contradicted by, what the pin shows for the subject it names.
**UNSUPPORTED** = no pin basis.

## 0. Base unchanged and pin identity (receipts: `receipts/p23-check.txt`, `receipts/sha256.txt`)

| Check | Result |
|---|---|
| `git show 3b55b6e:<path>` = 3072 bytes; `57584ed:<path>` = 8059 bytes = working tree | base is a byte prefix of lane (`cmp -n 3072`), block = 4987 bytes after it. Base sha256 `764f4867…0b65` (equals `R55ScribeP19b/verify.txt` base_sha256). |
| P20, P21, P22 rows | present, at base lines 18–20, inside the unchanged 3072-byte prefix. Their truth is not audited here (out of scope); only byte-unchanged is confirmed. |
| `Hyprland-ConfigActions.cpp` sha256 | `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637` = `SHA256SUMS` = S371 row. |
| `Hyprland-ConfigActions.hpp` sha256 | `746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073` = `SHA256SUMS`. |
| Upstream re-fetch `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.{cpp,hpp}` | `cmp` equal to the pin files, both. |

## 1. Sentence audit

Line numbers are the errata file's lines.

| # | Line | Sentence (abridged where marked …) | Label | Evidence / fix |
|---|---|---|---|---|
| 1 | 28 | "This block is appended after the unchanged round-53 entry above." | SUPPORTED | Base prefix = 3072 bytes, cmp-equal (sec. 0). |
| 2 | 28 | "It adds one corrected proposition, P23, which supersedes P19 only." | SUPPORTED | One P23 row (line 36); P19 row kept at base line 17. |
| 3 | 28 | "The original P19 row stays above as history and must not be used as current evidence." | SUPPORTED | Base line 17 present, byte-identical. |
| 4 | 28 | "P20 through P22 and the rest of this entry are not changed here." | SUPPORTED | Base prefix identical. (P20–P22 content not audited.) |
| 5 | 28 | "The correction is source-level: it states what the pinned `Actions::pass` text … tests and sends, and it makes no claim about a configured bind, a sent client event, or host behavior." | HELD | P23 says "sends" for what are seat calls (`sendKeyboardKey`, `sendPointerButton`, `sendKeyboardMods`). Read as calls it holds; "a sent client event" is ambiguous with those calls. Fix: "…tests and calls (`sendKeyboardMods`, `sendKeyboardKey`, `sendPointerButton`), and it makes no claim about delivery to a client, a bind, or host behavior." |
| 6 | 30 | "The P19 wording was false because it made the keyboard PRESSED send exclusive to the `m_passPressed == 1` branch." | SUPPORTED | Base P19 says "only when `m_passPressed == 1`". Pin 1566–1569: `} else {` then `if (!isMouse) {` sends `sendKeyboardKey(…PRESSED)` at 1568, so the send is not exclusive to the `== 1` arm. |
| 7 | 30 | "The pinned text shows the keyboard PRESSED call again in the arm that Q08 opens: Q09 sends a keyboard key PRESSED there, and Q10 sends the matching keyboard RELEASED" | SUPPORTED | Pin 1566 `} else {`, 1568 PRESSED, 1569 RELEASED (receipts R3). The keyboard calls sit under the unquoted `if (!isMouse) {` at 1567 (see row 19). |
| 8 | 30 | "so a value that is neither 1 (Q02) nor 0 (Q05) reaches a keyboard PRESSED send." | SUPPORTED | Source-path claim only, and only for a non-mouse key (1567 gate). Not a runtime claim. |
| 9 | 30 | "The old quote covered only the `== 1` text (Q01 to Q03), so it could not show the other two arms." | SUPPORTED | Base P19 quote = pin 1554–1558 contiguous (1554, 1556, 1557 `if (!isMouse)`, 1558). It contains no `else`. |
| 10 | 30 | "P23 therefore states all three arms and the keyboard-versus-pointer split inside each." | HELD | The split is shown by which call appears in each arm (Q03/Q04, Q06/Q07, Q09–Q12). The condition that makes a key "non-mouse" is `if (!isMouse)` at 1557, 1562, 1567, and `isMouse` is defined at 1534; none is quoted. Fix: add Q rows for 1534 and 1557/1562/1567, or say the split is by the call only. |
| 11 | 32 | "(a) where `m_passPressed` is set." (non-claim) | SUPPORTED | Non-claim; consistent with pin. |
| 12 | 32 | "The pin also writes it outside the quoted range: `sendKeyState` sets it to 1 or 0 around its `pass` calls (`Hyprland-ConfigActions.cpp:1603-1615`)" | HELD | sendKeyState part is correct: 1603 saves, 1606 sets 1, 1608 sets 0, 1610 and 1613 call `pass`, 1615 restores the saved value. But "the pin also writes it" lists only one writer. The same pin also writes it in `Hyprland-KeybindManager.cpp:804` (`= sc<int>(pressed)`, i.e. 1 or 0) and `:814` (`= -1`, after the dispatcher call). Fix: add "and `Hyprland-KeybindManager.cpp:804` and `:814` (`sc<int>(pressed)`, then `-1`)". |
| 13 | 32 | "the header declares a default of -1 with the comment `-1 = dynamic (press+release)` (`Hyprland-ConfigActions.hpp:114`)" | SUPPORTED | hpp:114 `int m_passPressed = -1; // -1 = dynamic (press+release), 0 = released, 1 = pressed`. Upstream hpp identical. |
| 14 | 32 | "This block does not say which setter reaches `pass` on any path." | SUPPORTED | Self-description, true. |
| 15 | 32 | "(b) which values reach the else arm. The else arm runs for any value other than 0 and 1" | SUPPORTED | Logical consequence of 1556, 1561 and the `else` at 1566. |
| 16 | 32 | "whether -1 or another value is stored when `pass` runs is not established here, and the `dynamic` comment is not evidence of it." | HELD | Literally true for "when `pass` runs". But the pin does store -1 (KeybindManager.cpp:814) after each keybind dispatch, which the block omits; `handleKeybinds` takes `bool pressed`, so :804 stores 0/1. Fix: "the pin stores -1 at KeybindManager.cpp:814 after a keybind dispatch and stores 0/1 at :804; whether -1 is present when `pass` runs on any path is not established here." |
| 17 | 32 | "(c) runtime delivery: that any send in any arm reaches a client, a focused window, or a keymap is not claimed." | SUPPORTED | Non-claim. |
| 18 | 32 | "Pin sha256 is recorded in `verify.txt`;" | HELD | Referent unnamed. The pin sha (`a83abeb5…7637`) is recorded in `.ufo/waves/round-52/fetch/SHA256SUMS`, `corpus/SOURCES.md` S371, `.ufo/waves/round-55/w1/R55ScribeP19b/verify.txt` and `.ufo/waves/round-52/w1/C2EntryDraft/fetch/verify.txt`. No `verify.txt` lives beside the errata. Fix: name the path, e.g. "recorded in `.ufo/waves/round-52/fetch/SHA256SUMS` and `corpus/SOURCES.md` S371". |
| 19 | 32 | "the non-author source-truth review named in the base entry is still required." | SUPPORTED | Base line 24 names it. |
| 20 | 36 | P23 "`Actions::pass` sends modifier state (`sendKeyboardMods`) before its delivery branch and clears it after that branch." | OVERREACH | True of the two-argument overload `Actions::pass(uint32_t modMask, uint32_t key, …)` at 1530–1599: sends at 1554, clears at 1576. The one-argument overload `Actions::pass(std::optional<PHLWINDOW>)` at 1465–1528 sends at 1485 and has no clear (receipts R5: only sendKeyboardMods sites in that range are 1485). It is the one `DispatcherTranslator.cpp:528` calls. Fix: write the signature: "`Actions::pass(uint32_t modMask, uint32_t key, …)` (ConfigActions.cpp:1530) sends modifier state … and clears it at 1576." |
| 21 | 36 | "The branch tests `m_passPressed`." | SUPPORTED | 1556, 1561, 1566 (for 1530 overload). Note the 1-arg overload also tests it at 1487/1492 with a different split (`m_lastCode`), which the block does not mention; fix with row 20. |
| 22 | 36 | "When `m_passPressed == 1`, a non-mouse key sends a keyboard key PRESSED and a mouse button sends a pointer button PRESSED." | HELD | Calls SUPPORTED (Q02–Q04). "Non-mouse" and "mouse button" rest on `isMouse` (1534: `key >= 272 && key < 0x160; // mouse button range`), unquoted. The range 272–351 is not only BTN_MOUSE: per `input-event-codes.h` (linux v6.12 raw fetch, receipts `input-codes.txt`) it covers BTN_JOYSTICK 0x120, BTN_GAMEPAD 0x130, BTN_DIGI 0x140 and BTN_WHEEL 0x150. Fix: quote 1534 and say "a key code with 272 ≤ key < 352 (the pin's 'mouse button range')" in place of "a mouse button". |
| 23 | 36 | "When `m_passPressed == 0`, a non-mouse key sends a keyboard key RELEASED and a mouse button sends a pointer button RELEASED." | HELD | Calls SUPPORTED (Q05–Q07). Same isMouse premise as row 22. |
| 24 | 36 | "When `m_passPressed` is any other value (the `else` arm), a non-mouse key sends a keyboard key PRESSED and then a keyboard key RELEASED, and a mouse button sends a pointer button PRESSED and then a pointer button RELEASED." | HELD | Calls and order SUPPORTED (Q08–Q12, 1566–1572). Same isMouse premise as row 22. |
| 25 | 36 | "Q01 to Q13 below" (quote column) | SUPPORTED | 13 rows (lines 50–62). |
| 26 | 36 | Support: "direct: Q01 to Q13 quote every call and branch test at the cited lines" | OVERREACH | All 10 calls in 1554–1576 are quoted (1554, 1558, 1560, 1563, 1565, 1568, 1569, 1571, 1572, 1576). All three `m_passPressed` tests (1556, 1561, else 1566) are quoted. Not quoted: the three `if (!isMouse)` tests (1557, 1562, 1567) and the `else` keywords on 1559, 1564, 1570. Fix: "direct: Q01 to Q13 quote every call and every `m_passPressed` test; the `isMouse` gates at 1557, 1562, 1567 are not quoted (see row 10)." |
| 27 | 36 | Source row "S371"; pin anchor "Hyprland-ConfigActions.cpp:1554-1576" | SUPPORTED | `corpus/SOURCES.md` S371 names the same upstream path at `efb50993…`, the same sha `a83abeb5…`, and `ConfigActions.cpp:1530-1616`, which contains 1554–1576. |
| 28 | 38–44 | Branch table: `== 1` → keyboard PRESSED / pointer PRESSED (Q02–Q04); `== 0` → RELEASED / RELEASED (Q05–Q07); `else` → PRESSED then RELEASED for each (Q08–Q12) | SUPPORTED | Matches 1556–1576 calls. Inherits the isMouse premise of row 22 for the keyboard/pointer column wording. |
| 29 | 48–62 | "each quote is the stripped pin line" / "generated from `frozen-tables.json` `c3.q`" | SUPPORTED | All 13 rows equal the pin line with leading indentation removed (no trailing whitespace, no CR in the pin). `c3.q` in both `frozen-tables.json` and `frozen-tables-v2.json` has 13 entries identical to the block rows (line and text). `frozen-tables.json` is byte-identical to its 54dacbd8 version. "Generated by" is not separately verified; content is. |

## 2. Q-row verification

All 13 rows, each compared to `Hyprland-ConfigActions.cpp` line N with leading whitespace removed:
Q01 1554 `sendKeyboardMods(modMask, 0, 0, 0);`; Q02 1556 `if (S.m_passPressed == 1) {`;
Q03 1558 `sendKeyboardKey(… PRESSED)`; Q04 1560 `sendPointerButton(… PRESSED)`;
Q05 1561 `} else if (S.m_passPressed == 0) {`; Q06 1563 `sendKeyboardKey(… RELEASED)`;
Q07 1565 `sendPointerButton(… RELEASED)`; Q08 1566 `} else {`; Q09 1568 `sendKeyboardKey(… PRESSED)`;
Q10 1569 `sendKeyboardKey(… RELEASED)`; Q11 1571 `sendPointerButton(… PRESSED)`;
Q12 1572 `sendPointerButton(… RELEASED)`; Q13 1576 `sendKeyboardMods(0, 0, 0, 0);`. All EQ.

## 3. Minimal fix set (non-SUPPORTED rows)

1. Row 5: replace "sends" with "calls" and "a sent client event" with "delivery to a client".
2. Row 10, 22–24, 28: quote `isMouse` (1534) and the gates 1557, 1562, 1567 as Q rows, or qualify "non-mouse/mouse button" as "key code in 272–351 (the pin's 'mouse button range')".
3. Row 12 and 16: add KeybindManager.cpp:804 (`sc<int>(pressed)`) and :814 (`= -1`) to the writer list.
4. Row 18: replace "verify.txt" with the actual path(s).
5. Row 20 and 21: name the overload `Actions::pass(uint32_t modMask, uint32_t key, …)` at 1530; say the clear at 1576 is that overload only; mention the one-argument overload at 1465–1528 with its own `m_passPressed` branch.
6. Row 26: change "every call and branch test" to "every call and every `m_passPressed` test", and list the unquoted `isMouse` gates.

Changes to the block were NOT made; this audit did not edit any tracked file.

## 4. Verdict on the block

Core content holds on the pin: the three-arm behavior, the keyboard/pointer call pairs, the 13 Q rows, the P19-was-false reason, and the `hpp:114` and `1603-1615` setter facts all check out. The block's defects are scope and naming: an overload-name ambiguity that makes "clears it" wrong for one `Actions::pass`, an over-broad "every branch test" claim, an isMouse premise and "mouse button" label that are unquoted and broader than BTN_MOUSE, an incomplete writer list that omits KeybindManager.cpp:804/:814 (including the -1 store), and an unresolved "verify.txt" reference. None changes a Q row or a branch outcome.

Source-truth review is still required from a non-author before admission (base line 24). This audit is one such read; the block's own gate is not discharged by it alone.
