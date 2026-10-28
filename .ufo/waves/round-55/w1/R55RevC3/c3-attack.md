# R55RevC3 — C3 attack: Q rows, P23 bound on `S.m_passPressed`, lexical P23 leg

Seat: R55RevC3 (leaf reviewer, draft; L1 integrates). Base `3b55b6e91e40f455dd56b2985e4ffc087ada92d5`;
freeze `54dacbd843d64ba744cd3f1bdc2ec622e5010039`. Scratch `/fast/scratch/hyaku/mado-r55/R55RevC3/` (removed before yield).
Receipts copied next to this file: `c3check.py`, `c3check.out`, `passpressed-all.txt`, `pass-callers.txt`,
`efb-fetch-sha256.txt`, `lane-r55-files-at-freeze.txt`.

## 1. The 13 Q rows against the round-52 pin

Pin: `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`, sha256
`a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637` (= frozen `c3.pin_sha256`; MATCH).
No CR bytes; 71407 bytes; ends with LF. The same sha256 is produced by an independent fetch of
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp`,
so the pin is byte-identical to the tag-pinned commit.

`c3check.py` (own script, not the frozen freeze-verify) compares each `c3.q` row against line `line` of the pin:

```
Q01 L1554  stripped_eq=True substring=True indent=4 | g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
Q02 L1556  stripped_eq=True substring=True indent=4 | if (S.m_passPressed == 1) {
Q03 L1558  stripped_eq=True substring=True indent=12 | g_pSeatManager->sendKeyboardKey(... PRESSED);
Q04 L1560  stripped_eq=True substring=True indent=12 | g_pSeatManager->sendPointerButton(... PRESSED);
Q05 L1561  stripped_eq=True substring=True indent=4 | } else if (S.m_passPressed == 0) {
Q06 L1563  stripped_eq=True substring=True indent=12 | g_pSeatManager->sendKeyboardKey(... RELEASED);
Q07 L1565  stripped_eq=True substring=True indent=12 | g_pSeatManager->sendPointerButton(... RELEASED);
Q08 L1566  stripped_eq=True substring=True indent=4 | } else {
Q09 L1568  stripped_eq=True substring=True indent=12 | g_pSeatManager->sendKeyboardKey(... PRESSED);
Q10 L1569  stripped_eq=True substring=True indent=12 | g_pSeatManager->sendKeyboardKey(... RELEASED);
Q11 L1571  stripped_eq=True substring=True indent=12 | g_pSeatManager->sendPointerButton(... PRESSED);
Q12 L1572  stripped_eq=True substring=True indent=12 | g_pSeatManager->sendPointerButton(... RELEASED);
Q13 L1576  stripped_eq=True substring=True indent=4 | g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);
Q_RESULT ALL_OK   (13 ids, unique)
```

Result: all 13 rows are exact (stripped line equality, which is the frozen rule). No row is off by one line.
Note `Q08 "} else {"` is a non-unique text; it is accepted only because the id is bound to line 1566.

## 2. The function that owns lines 1554–1576 and the `m_passPressed` reads

Owner: `ActionResult Actions::pass(uint32_t modMask, uint32_t key, std::optional<PHLWINDOW> w)`, pin line 1530 to 1599
(`S = *Config::Actions::state()` at 1533; `isMouse` at 1534). Structure:

| lines | content |
|---|---|
| 1554 | `sendKeyboardMods(modMask,0,0,0)` |
| 1556 | `if (S.m_passPressed == 1)` → 1558 keyboard PRESSED, or 1560 pointer PRESSED (mouse) |
| 1561 | `else if (S.m_passPressed == 0)` → 1563 keyboard RELEASED, or 1565 pointer RELEASED |
| 1566 | `else` → 1568 keyboard PRESSED **then** 1569 keyboard RELEASED; 1571 pointer PRESSED **then** 1572 pointer RELEASED |
| 1576 | `sendKeyboardMods(0,0,0,0)` |

So the else arm is NOT a PRESSED-only arm. It issues a press/release pair. The P19 sentence "sends a PRESSED keyboard key only when `m_passPressed == 1`" is false at 1566–1569, which is the r54 routed defect 1.

## 3. Where `m_passPressed` is written (full tree at the pinned commit)

The tarball `codeload.github.com/hyprwm/Hyprland/tar.gz/efb50993780079460b0cbed1363e2166a2de1d9f` (sha256
`5b05ce7ba5296fa46e666852bf108ab5af121bf577f8043787e2d2c252d8f109`, 50812454 bytes) was extracted into scratch.
`grep -rn m_passPressed --include=*.cpp --include=*.hpp` returns 18 lines (`passpressed-all.txt`). Every write:

| file (efb50993) | line | write | committed pin? |
|---|---|---|---|
| `src/config/shared/actions/ConfigActions.hpp` | 114 | default `int m_passPressed = -1; // -1 = dynamic (press+release), 0 = released, 1 = pressed` | round-52 fetch `Hyprland-ConfigActions.hpp` (sha 746c6f…, matches tarball) |
| `src/managers/KeybindManager.cpp` | 804 | `m_passPressed = sc<int>(pressed);` (`handleKeybinds(..., bool pressed, ...)` at 602) → 1 or 0 | round-52 fetch `Hyprland-KeybindManager.cpp` (sha 8d8f35…, matches) |
| `src/managers/KeybindManager.cpp` | 814 | `m_passPressed = -1;` after `DISPATCHER->second(...)` (line 810/812) | same |
| `src/config/shared/actions/ConfigActions.cpp` | 1606 / 1608 | `sendKeyState`: 1 for keyState 1 or 2, else 0; both calls to `pass(3-arg)` at 1610/1613 | pin (S371) |
| `src/config/shared/actions/ConfigActions.cpp` | 1615 | restore `oldPassPressed` | pin (S371) |
| `src/config/legacy/DispatcherTranslator.cpp` | 615 / 617 / 624 | `sendkeystate`: 1 / 0, restore | S370 / round-52 fetch (sha 7248cb…, matches) |

Reads: 1487, 1492, 1556, 1561 (pass(w) and pass(3-arg)), 1634 (global), 1640 (mouse), and the 3-arg else arm.
No other writer exists in the tarball (`grep` is literal `m_passPressed`; no alias or macro writes it).

Consequence: the only values ever stored are {-1, 0, 1}; `sc<int>(bool)` cannot yield anything else. The else arm
(`!= 1` and `!= 0`) therefore sees **-1 only**, and only when `pass(3-arg)` is entered outside a `sendKeyState`/
`sendkeystate` call and outside the KeybindManager dispatch window 804–814.

## 4. Callers of `pass(3-arg)` (where -1 can reach the else arm)

`grep -rn "Actions::pass\|pass(" src` restricted to the call sites (`pass-callers.txt`):

- `src/config/legacy/DispatcherTranslator.cpp:588` — `sendshortcut` legacy dispatcher, `return wrap(Actions::pass(MOD, keycode, PWINDOW));`. Reached from:
  - the keybind window (804: 0/1 set first) → else NOT reached;
  - `sendkeystate` (93–98: 0/1 set first) → else NOT reached;
  - **`hyprctl dispatch sendshortcut …`**: `src/debug/HyprCtl.cpp:1149–1154` calls `m_dispatchers` directly and writes no m_passPressed → else **reached** (-1);
  - **long-press/release re-dispatch**: `src/managers/KeybindManager.cpp:131` and `:154` call `DISPATCHER->second(...)` with no m_passPressed write → else reached (-1) for those paths.
- `src/config/lua/bindings/LuaBindingsDispatchers.cpp:420` — `dsp_sendShortcut` → `CA::pass(modMask, keycode, window)` (no write before the call). Inside a Lua keybind callback the value is 0/1 (window 804–814); outside any keybind window it is -1 → else reached.
- `ConfigActions.cpp:1610, 1613` — `sendKeyState` (0/1 set first) → else NOT reached.

Paths 1 (hyprctl), 2 (KeybindManager long-press lines 131/154), and the Lua path outside a keybind window are
**source-derived only** from tarball lines I read. HyprCtl.cpp, KeybindManager lines 131/154, and
LuaBindingsDispatchers.cpp are not in any committed round-52/55 pin and have no SOURCES row. Nothing was dispatched
or run on the host.

## 5. What the value -1 is, and what it is not

- `ConfigActions.hpp:114` comment says "-1 = dynamic (press+release)". That is a comment in a committed round-52 pin,
  not a behavioural observation. It must not be cited as proof of runtime behaviour.
- The else arm sends PRESSED then RELEASED for a keyboard key (`key - 8`) or a pointer button; it does not say
  which physical key or event produced the call.

## 6. Bound: what the P23 proposition may say about `S.m_passPressed`

Frozen P23 cell: `| P23 | P19 | <proposition> | S371 | Hyprland-ConfigActions.cpp:1554-1576 | … |`. Its only
registry row is S371 (`ConfigActions.cpp`, anchor 1530–1616). Any claim outside that row needs its own row.

MAY say (supported by S371 lines 1530–1576 alone):
1. `Actions::pass` (the three-argument overload at 1530) sends modifier state, then delivers the key through a branch on
   `S.m_passPressed`, then clears modifier state.
2. `== 1` → PRESSED only (keyboard `key - 8` or pointer button); `== 0` → RELEASED only.
3. Any other value (the else arm, 1566) → for a keyboard key a PRESSED call followed by a RELEASED call for the same
   `key - 8`; for a mouse button a PRESSED then RELEASED pointer call.
4. The one-line header fact that the value is "-1 by default" needs a row for `ConfigActions.hpp` (line 114). Without
   that row, the default may only be stated as "the value is not 0 or 1 in this excerpt", not as "the default".

Suggested P23 wording that stays inside those bounds (for the L1/w2 audit to check, not adopted here):

> Actions::pass sends modifier state, then delivers the key on a branch over S.m_passPressed: when it equals 1 it sends PRESSED only; when it equals 0 it sends RELEASED only; for any other value it sends a keyboard PRESSED followed by a RELEASED for the same key (pointer PRESSED then RELEASED for a mouse button); it clears modifier state after the branch.

This passes the lexical leg (it names `m_passPressed`, `== 1`, `== 0`, `PRESSED`, `RELEASED` and `any other`).

MUST NOT claim:
- That PRESSED is sent "only when" `m_passPressed == 1` (P19's false exclusivity). The else arm also sends PRESSED.
- That the else arm sends PRESSED alone. It sends PRESSED then RELEASED (1568–1569; 1571–1572).
- That `m_passPressed` takes only -1, 0 or 1 "in the protocol" or "always". That is the full-tree write list (section 3), not a
  registry row; without a KeybindManager/DispatcherTranslator/ConfigActions.hpp row it is an unsourced universal.
- That the else arm is reached by a specific bind, dispatcher, Lua call or `hyprctl dispatch` path. Section 4 is
  source-derived; the S371 pin does not show any caller.
- That a physical key press produces the else arm ("dynamic press+release" is a header comment, not an observation).
  The keybind window at 804–814 sets 0/1, so a keybind-initiated call does not reach the else arm.
- Anything about delivery to Wayland clients, focus, the compositor, or a host event. The entry is source-level only.
- Anything about `Actions::pass(std::optional<PHLWINDOW>)` at 1465–1505: it has its own `m_passPressed` branch (1487–1503)
  with its own else arm (sends PRESSED then RELEASED too). It is a different overload and not covered by Q01–Q13.
- That P19's first clause ("sends modifier state before its delivery branch") or its mouse clause is wrong. Those are
  not in scope of the else-arm correction.

## 7. Lexical P23 leg on three junk propositions

Leg per registration §C3 `p23`: P23 cell must contain `m_passPressed`, `== 1`, `== 0`, `PRESSED`, `RELEASED` and one of
`otherwise` / `any other` / `else`; and the Supersedes cell must equal `P19`. Run in `c3check.py` (substring, case-sensitive):

| proposition | result | missing |
|---|---|---|
| J1 `m_passPressed == 1 == 0 PRESSED RELEASED otherwise` (token salad) | **ok** | none |
| J2 `Actions::pass sends nothing in its else arm; m_passPressed == 1 and m_passPressed == 0 are the only arms that send PRESSED or RELEASED; any other value is dead code` (false) | **ok** | none |
| J3 `Actions::pass is a function about window focus and clipboard handling` | bad | all tokens + alternative |

Additional: the actual P19 sentence (base errata line 17) is **bad** (missing `== 0`, `RELEASED`, alternative). Appending
` RELEASED == 0 else` to the P19 sentence makes it **ok** while it remains false. So the leg admits false propositions
and is satisfied by padding; it proves presence of tokens, not truth. The truth test is the independent sentence audit
(w2) and the non-author closure. The registration's declared limit says this, but the `p23=ok` leg must not be read as
evidence that P23 is correct.

## 8. Other C3 contract observations (attack notes)

- C3-CTL-1 (absent block) expects "`prefix`-clean but `rows`+`p23` missed". At base the README row (corpus/README.md:81)
  names the errata file but not P23, so the `readme` leg also misses. The control text does not list `readme`, and the
  leg name form (`rows` vs `rows:<id>`) is ambiguous. The harness must define whether it checks subset or exact set.
- C3 counter `quality/counters/c3-r55-p19.py` and harness `quality/check-r55-controls.py` are not in the freeze commit
  `54dacbd` (`lane-r55-files-at-freeze.txt` lists only the three round-55 contract files). The C3 predicate therefore
  cannot run at the freeze; it is a wave deliverable. I did not run it.
- The `.ufo/waves/round-52/fetch/` pin and the tarball agree byte-for-byte for ConfigActions.cpp, KeybindManager.cpp,
  DispatcherTranslator.cpp and ConfigActions.hpp (sha256 in `efb-fetch-sha256.txt`).

## 9. Verdict for C3 attack

- Q rows: 13/13 exact against the pin (no defect).
- P23 bound: the else arm must be described as PRESSED then RELEASED; `-1` is the only value reaching it in the full tree;
  the caller-reachability statements need rows the registry does not yet have.
- Lexical leg: passes a false proposition (J2) and a padded P19 (defect of the leg, declared limit).
- Ambiguity: C3-CTL-1 leg list and `rows` naming (section 8).
