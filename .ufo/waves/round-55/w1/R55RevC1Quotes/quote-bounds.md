# R55RevC1Quotes — quote bounds for frozen K01–K18 and H01–H06

Seat: R55RevC1Quotes (leaf, reviewer of C1 quotes). Base 3b55b6e91e40f455dd56b2985e4ffc087ada92d5.
Source of truth: `.ufo/waves/round-55/frozen-tables.json` `c1.k` / `c1.h`; bytes read from `.ufo/waves/round-55/fetch/`
(pins hash to `c1.pin_sha256`, all 10 OK). Checks run by my own script (`quote_check.py`, not `freeze-verify.py`);
receipts `quote-check.out` and `quote-locus.out` beside this file.

## Checks (all 24 rows)

- Substring at the stated line: 24/24 true (the quote is a byte substring of the 1-indexed pin line).
- Uniqueness: each quote occurs exactly once in its whole pin file (occurrence count 1 for 24/24; line count 1 for 24/24).
- Length: characters 12–112 (K06 = 12 shortest; K13 = 108, K14 = 112 longest). Byte length equals character length (ASCII).
- Line locus: WHOLE means the quote equals the stripped pin line; PARTIAL means text sits outside the quote (named below).

Proposition thresholds: K ≥ 40 chars, H ≥ 20 chars (registration §C1).

Flags:
- THIN = the quote cannot carry a ≥40-char proposition about its target without text from outside the quote or row.
- COND = the quote is a guard or condition; its effect sits on an adjacent line that no frozen row quotes.
- PARTIAL = the proposition is grounded, but a conjunct, mapping or snapshot caveat must narrow it.
- OK = grounded as stated, with only the scope caveats noted.

## K rows (Hyprland 0.56.2 pins at efb50993; wayland 1.26.0)

- K01 (InputManager.cpp:1220, len 58, PARTIAL-left: `const auto REPEATRATE  = Config::mgr()->` precedes) — MAY: "applyConfigToKeyboard reads repeat_rate through getDeviceInt(devname, …) with input:repeat_rate as the fallback key." MAY NOT: state the stored value, its clamp, or what getDeviceInt returns (its definition is not a frozen row). Flag: OK.
- K02 (InputManager.cpp:1221, len 60, PARTIAL-left) — MAY: "applyConfigToKeyboard reads repeat_delay through getDeviceInt(devname, …) with input:repeat_delay as the fallback key." MAY NOT: state the stored delay value or its clamp. Flag: OK.
- K03 (InputManager.cpp:1223, len 72, PARTIAL-left) — MAY: "applyConfigToKeyboard reads numlock_by_default through getDeviceInt(devname, …) with input:numlock_by_default as the fallback key." MAY NOT: claim numlock is engaged (the assignment is K06, and K06 is itself THIN). Flag: OK.
- K04 (InputManager.cpp:1282, len 24, PARTIAL-left: `pKeyboard->m_repeatRate  =` outside) — MAY: "the value stored is std::max(0, REPEATRATE), so REPEATRATE is floored at 0." MAY NOT: name the keyboard field the value is stored in, or claim an upper clamp (none in the quote; the 0–200 range is enforced at parse time, K13). Flag: THIN (target field outside quote).
- K05 (InputManager.cpp:1283, len 25, PARTIAL-left: `pKeyboard->m_repeatDelay =` outside) — MAY: "the value stored is std::max(0, REPEATDELAY), so REPEATDELAY is floored at 0." MAY NOT: name the field or claim an upper clamp (the 0–2000 range is enforced at parse time, K14). Flag: THIN (target field outside quote).
- K06 (InputManager.cpp:1284, len 12, PARTIAL-left: `pKeyboard->m_numlockOn` outside) — MAY: "the right-hand side of the numlock store is NUMLOCKON." MAY NOT: name m_numlockOn, or say numlock is engaged; a 40-char proposition is not supported by a 12-char fragment. Flag: THIN (too short; target outside quote).
- K07 (InputManager.cpp:1271, len 80, PARTIAL-both: NUMLOCKON check before, RULES/MODEL/… conjuncts after) — MAY: "the unchanged-config test on line 1271 includes REPEATDELAY == m_repeatDelay and REPEATRATE == m_repeatRate as two of its conjuncts." MAY NOT: say the test compares delay and rate alone; numlock, rules, model, layout, variant, options and file path are also conjuncts outside the quote. Flag: PARTIAL.
- K08 (IKeyboard.cpp:120, len 73, PARTIAL-left: `const auto NUMLOCKON = Config::mgr()->` outside) — MAY: "IKeyboard reads numlock_by_default through getDeviceInt(m_hlName, …) with input:numlock_by_default as the fallback key." MAY NOT: name the enclosing function (outside pin lines 113–129) or state the lock effect. Flag: OK.
- K09 (IKeyboard.cpp:122, len 21, WHOLE) — MAY: "IKeyboard branches on whether NUMLOCKON equals 1 before the numlock block." MAY NOT: say numlock is locked or engaged; the lock is at lines 124–127, which no frozen row quotes. Flag: COND (effect outside row) — 21 chars, cannot ground an engagement claim.
- K10 (SeatManager.cpp:177, len 83, WHOLE) — MAY: "updateActiveKeyboardData passes the active keyboard's m_repeatRate and m_repeatDelay to PROTO::seat->updateRepeatInfo." MAY NOT: say the call reaches a wl_keyboard resource (the fan-out at Seat.cpp:603–610 is not quoted by any frozen row), or claim the call is guarded by `if (m_keyboard)` (that guard is on line 176, outside the quote). Flag: OK for the sentence; middle hop unquoted (see report D3).
- K11 (Seat.cpp:442, len 25, PARTIAL-both: `if (!m_owner ||` before, `|| (rate == …)` after) — MAY: "repeatInfo's early-return guard includes m_resource->version() < 4 as one of its disjuncts." MAY NOT: say version < 4 is the only early-return condition, or that the function returns (the `return;` is on line 443, not quoted). Flag: COND (action outside row); 25 chars.
- K12 (Seat.cpp:447, len 42, WHOLE) — MAY: "repeatInfo forwards rate and delayMs to the resource through sendRepeatInfo." MAY NOT: say it sends on every call; the send at line 447 is reached only past the guard at 442–443. Flag: OK.
- K13 (ConfigValues.cpp:279, len 108, PARTIAL-both: `MS<Int>(` before, `, .refresh = …` after) — MAY: "input:repeat_rate is registered with default 25 and range 0 to 200, described as repeats per second." MAY NOT: claim the value applies per device (the refresh flag is outside the quote, and per-device semantics come from getDeviceInt, unquoted here). Flag: OK.
- K14 (ConfigValues.cpp:280, len 112, PARTIAL-left) — MAY: "input:repeat_delay is registered with default 600 and range 0 to 2000, described in milliseconds." MAY NOT: claim anything about per-device override. Flag: OK.
- K15 (ConfigValues.cpp:277, len 63, PARTIAL-both: `MS<Bool>(` before, `, {.refresh = …}` after) — MAY: "input:numlock_by_default is registered with default false and the description 'Engage numlock by default.'" MAY NOT: map false to 0 (the hyprlang mapping is not a c1 row) or claim the Bool type from the quote (`MS<Bool>` is outside it). Flag: OK for the default; the type is unquoted.
- K16 (legacy ConfigManager.cpp:1119, len 54, WHOLE) — MAY: "getConfigValueSafeDevice takes the fallback key when the device value is absent or not user-set and the fallback name is non-empty." MAY NOT: claim getDeviceInt uses this path (getDeviceInt at 1131–1132 is not a frozen row), or that the global value is returned (return on line 1120, outside the quote). Flag: COND.
- K17 (wayland-1.26.0-wayland.xml:2741, len 62, WHOLE on line 2741) — MAY: "the wayland 1.26.0 repeat_info text (line 2741) says the event disables any repeating, regardless of delay." The subject 'a rate of zero' is on line 2740 and is not in the quote, so it cannot be named from the row alone. MAY NOT: claim that rate zero disables repeating from K17 alone (it needs line 2740), and MAY NOT claim anything about Hyprland's compositor-side repeat timer, which no pin covers. Flag: THIN (subject split across the line break; the single-line rule forces this).
- K18 (IKeyboard.hpp:121, len 24, PARTIAL-left: `int` and padding before) — MAY: "IKeyboard declares the member m_repeatRate with initial value 0." MAY NOT: claim the value at runtime after applyConfigToKeyboard (K04 overwrites it), or the int type from the quote. Flag: OK.

## H rows (host pins fetched 2026-10-28; read-only host snapshot)

- H01 (host-input.conf:14, len 16, WHOLE) — MAY: "the fetched host input.conf (pinned sha256) contains the line repeat_rate = 40." MAY NOT: claim the live effective rate (H04 is the only live row, a separate snapshot), or that the file is the active config (no include or source check). Flag: OK for the config text.
- H02 (host-input.conf:15, len 18, WHOLE) — MAY: "the fetched host input.conf contains the line repeat_delay = 250." MAY NOT: claim the live delay (H05). Flag: OK.
- H03 (host-input.conf:18, len 25, WHOLE) — MAY: "the fetched host input.conf sets numlock_by_default = true at line 18." MAY NOT: convert `true` to 1 from H03 alone (the hyprlang bool parse is cited only by the C2 spec, round-46 pin, not in this fetch); MAY NOT claim live numlock (H06). Flag: PARTIAL (value mapping unpinned in c1).
- H04 (host-getoption.json:1, len 40, PARTIAL-left: `{` before, `, "set": true }` after) — MAY: "the host-getoption pin records input:repeat_rate with int 40 and set true." MAY NOT: claim the value is live now (a snapshot with no timestamp inside the JSON), or define what "set": true means beyond its literal text. Flag: OK, snapshot caveat.
- H05 (host-getoption.json:2, len 42, PARTIAL-left/right) — MAY: "the host-getoption pin records input:repeat_delay with int 250 and set true." MAY NOT: as H04. Flag: OK, snapshot caveat.
- H06 (host-getoption.json:3, len 46, PARTIAL-left/right) — MAY: "the host-getoption pin records input:numlock_by_default with int 1 and set true." MAY NOT: map int 1 to "on" from H06 alone (K09 is the source-level test `NUMLOCKON == 1`; cite K09 for that), or claim live state. Flag: OK, snapshot caveat.

## Summary

- THIN: K04, K05, K06, K17.
- COND (guard quoted, effect unquoted): K09, K11, K16.
- PARTIAL: K07, H03 (and K15's Bool type is unquoted, noted, not flagged).
- OK: K01, K02, K03, K08, K10, K12, K13, K14, K15, K18, H01, H02, H04, H05, H06.
