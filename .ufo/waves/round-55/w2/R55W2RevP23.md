# R55W2RevP23 — P23 sentence-to-pin audit (round 55, wave w2, falsify)

Deliverable: `.ufo/waves/round-55/w2/R55W2RevP23/p23-audit.md` (sentence table, 29 rows, fix set).
Receipts: `.ufo/waves/round-55/w2/R55W2RevP23/receipts/` (`p23-check.txt`, `sha256.txt`, `input-codes.txt`).
Lane: no tracked file edited; no git mutation (git used read-only: `show`, `cat-file`, `rev-parse`). No commits, no subagents, no hyprctl, no pacman, no installs.

## What ran

1. Base/lane byte check: `git show 3b55b6e:<path>` (3072 B), `git show 57584ed…:<path>` (8059 B); `cmp -n 3072` prefix equal; block 4987 B after base; worktree = 57584ed.
2. Pin hashes: `sha256sum` of `round-52/fetch/Hyprland-ConfigActions.{cpp,hpp}` = `SHA256SUMS` = S371 values.
3. Upstream re-fetch (network read, raw.githubusercontent.com, efb50993): `src/config/shared/actions/ConfigActions.{cpp,hpp}` → `cmp` equal to the pin files.
4. Q-row check: each of 13 rows vs pin line N with leading indentation removed (13/13 equal, no trailing ws, no CR); `frozen-tables.json` and `frozen-tables-v2.json` `c3.q` vs block rows (0 mismatches); `frozen-tables.json` byte-equal to its 54dacbd8 version.
5. Pin structure: `grep` of `sendKeyboardMods`, `m_passPressed`, `isMouse`, `Actions::pass` overloads; `KeybindManager.cpp:804/814` writers; `hpp:114`; `pressed` is `bool` in `handleKeybinds` (line 602).
6. Source header for key codes: `input-event-codes.h` from torvalds/linux tag v6.12 (network read, sha256 `f9889a73…`), `BTN_*` values for the `isMouse` range.

Command/output: `python3 -I $scratch/check.py` → `receipts/p23-check.txt` (all decisive lines are there, including the R5 listing of the two `Actions::pass` overloads).

## Verdict per target

| Target | Verdict | Evidence |
|---|---|---|
| Base bytes 0–3071 unchanged (3b55b6e → 57584ed) | SUPPORTED | R1 in `p23-check.txt`; base sha `764f4867…0b65` |
| P20–P22 rows unchanged | SUPPORTED (byte-unchanged only; truth not audited) | base lines 18–20 inside the prefix |
| Pin identity (cpp/hpp = efb50993 = SHA256SUMS = S371) | SUPPORTED | R2, R2b; `receipts/sha256.txt` |
| Q01–Q13 byte-equal to stripped pin lines | SUPPORTED | R3, all EQ; equal to `frozen-tables(-v2).json` c3.q (R4) |
| Three-branch description (== 1 / == 0 / else) | SUPPORTED for call content (1556–1572); HELD for the "non-mouse / mouse button" premise | rows 22–24 of audit |
| Keyboard/pointer split | HELD: `isMouse` (1534) and gates 1557/1562/1567 are not quoted; `isMouse` range 272–351 includes BTN_JOYSTICK/GAMEPAD/DIGI/WHEEL, so "mouse button" is the pin's label, not BTN_MOUSE | rows 10, 22; `receipts/input-codes.txt` |
| "Actions::pass sends … and clears it after that branch" | OVERREACH: true only of the 2-arg overload (1530–1599; clear at 1576). The 1-arg overload (1465–1528) sends at 1485 with no clear (R5) and branches on `m_passPressed` at 1487/1492 with a different split | row 20–21 |
| "Q01 to Q13 quote every call and branch test" | OVERREACH: all 10 calls and the three `m_passPressed` tests are quoted; the `if (!isMouse)` tests (1557, 1562, 1567) and their `else`s (1559, 1564, 1570) are not | row 26 |
| (a) setters: "sendKeyState sets it … 1603-1615" | HELD: sendKeyState part correct (1603/1606/1608/1615; calls 1610/1613). The list of outside-range writers omits KeybindManager.cpp:804 (`sc<int>(pressed)`) and :814 (`= -1`) | row 12 |
| hpp:114 default -1 and comment | SUPPORTED | row 13 |
| (b) "whether -1 … is stored when pass runs is not established here" | HELD: literally true, but the pin stores -1 at KeybindManager.cpp:814 after each keybind dispatch and the block does not say so | row 16 |
| (c) runtime delivery not claimed | SUPPORTED (non-claim) | row 17 |
| "Pin sha256 is recorded in `verify.txt`" | HELD: referent unnamed; sha is recorded in SHA256SUMS, SOURCES S371, and several verify.txt receipts under round-52/round-55 `w1` | row 18 |
| "The P19 wording was false because … exclusive to the == 1 branch" | SUPPORTED: base P19 says "only when m_passPressed == 1"; pin 1568 sends keyboard PRESSED in the else arm | row 6 |
| Non-author review still required | SUPPORTED (base line 24) | row 19 |
| Any sentence labelled UNSUPPORTED | none found | — |

Label definitions used (the brief did not define HELD): SUPPORTED = pinned bytes establish the sentence as written; HELD = true on the pin but rests on an unquoted premise or omits a qualifier; OVERREACH = goes beyond or is contradicted by the pin for the subject named; UNSUPPORTED = no pin basis.

Overall: the core content holds (13 quotes, branch outcomes, P19-falsity reason, setter facts). The defects are scope and naming: the overload ambiguity, the over-broad "every branch test" claim, the unquoted isMouse premise and "mouse button" label, the incomplete writer list (which omits the -1 store), and the unnamed verify.txt. Minimal fixes are in §3 of the audit. No change was made to the block.

## Not done / could not verify

- Runtime delivery: out of scope by the block's own non-claim; not tested. No hyprctl was run.
- P20–P22 truth against the pin: not audited (only unchanged-ness was in the brief).
- Whether -1 reaches `pass` on any real path (e.g. an IPC-dispatched `sendshortcut` outside a keybind): not established by the pin, and not tested.
- "Generated from frozen-tables.json c3.q": content equality verified; the generator itself not inspected.
- Key-code header: linux v6.12 `input-event-codes.h` used as an external reference for BTN_* values; Hyprland's build headers are not pinned, so the mapping is a reference, not a pin fact.
- Upstream fetch covered the two ConfigActions files only; KeybindManager and DispatcherTranslator upstream were not re-fetched.

## Tooling

No tool installed or upgraded. `curl` (already present) used for raw.githubusercontent.com reads (2 upstream files at efb50993; 1 header at linux v6.12). Python `python3 -I` for checks.

## Scratch

`/fast/scratch/hyaku/mado-r55/R55W2RevP23/` (base.md, lane.md, up/, input-event-codes.h, check.py) — removed before yield.
No mutation test was run; this audit is read-only, so nothing was mutated in or outside the lane.
