# Sentence-to-pin audit (QUALITY 104): K04, K05, K06, K07, E03, E10

Seat R55W2AuditB, round 55 wave 2. Entry: `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` (C1). Pins: `.ufo/waves/round-55/fetch/` at efb50993780079460b0cbed1363e2166a2de1d9f. Lane was read only; no lane file was edited. Receipts: `receipts.txt` in this directory.

Labels: SUPPORTED (the quoted line entails the proposition), HELD (stated as held/unknown/inference with the boundary named), OVERREACH (stronger than the quote), UNSUPPORTED.

## Method

1. Each proposition cell was read from the entry, and its pin line was opened from `fetch/`. The quote was matched as a substring of that line by script (all six PASS).
2. Neighbouring lines were read: 1270-1276 and 1282-1286 for applyConfigToKeyboard; 121-124 for IKeyboard.hpp; 441-447 for repeatInfo; 118-135 for setKeymap.
3. Every read or write of `m_numlockOn`, `m_lastDelayMs`, `sendRepeatInfo` and `repeatInfo(` was grepped across all 8 pinned C++ / header files (this grep covers the pins only, not the whole upstream tree).
4. Upstream re-fetch: `curl -sSfL` of the four Hyprland raw files at efb50993780079460b0cbed1363e2166a2de1d9f (`src/managers/input/InputManager.cpp`, `src/devices/IKeyboard.hpp`, `src/protocols/core/Seat.cpp`, `src/managers/SeatManager.cpp`). All four sha256 values equal the committed pins and `SHA256SUMS.txt`, and `cmp` reports IDENTICAL for all four (InputManager.cpp 98845 B; IKeyboard.hpp 4816 B; Seat.cpp 21117 B; SeatManager.cpp 26074 B). The wayland 1.26.0 XML was not re-fetched; no row in this audit cites it.

## Table

| Row | Proposition (verbatim cell) | Pin:line and quote check | Neighbour lines that matter | Label | Boundary / evidence |
|---|---|---|---|---|---|
| K04 | The stored repeat rate m_repeatRate is assigned std::max(0, REPEATRATE): floored at zero, with no upper bound applied on this line. | Hyprland-InputManager.cpp:1282 `pKeyboard->m_repeatRate  = std::max(0, REPEATRATE);`; quote substring PASS; upstream identical | 1220 REPEATRATE = getDeviceInt(...,"input:repeat_rate") (raw, int); 1271-1275 early return, which runs before the assignment; 1283 same form for delay; 1284 numlock | SUPPORTED | The line sets a floor of 0 and no upper bound. Whether the config layer clamps to max 200 (K13) is not claimed by K04 and is UNKNOWN per the entry's own UNKNOWN list. |
| K05 | The stored repeat delay m_repeatDelay is assigned std::max(0, REPEATDELAY): floored at zero, with no upper bound applied on this line. | Hyprland-InputManager.cpp:1283 `pKeyboard->m_repeatDelay = std::max(0, REPEATDELAY);`; quote substring PASS; upstream identical | 1221 REPEATDELAY raw getDeviceInt; 1271 early return; 1282 and 1284 | SUPPORTED | Same as K04, for the delay key (K14 range 0..2000 is declaration only; no clamp claimed). |
| K06 | The stored numlock state m_numlockOn is assigned NUMLOCKON directly on this line, with no max(0) floor and no range test. | Hyprland-InputManager.cpp:1284 `pKeyboard->m_numlockOn   = NUMLOCKON;`; quote substring PASS; upstream identical | 1223 NUMLOCKON = getDeviceInt(...,"numlock_by_default"), raw; 1282-1283 are floored (the contrast is real); 1286 setKeymap. Pin-wide grep: m_numlockOn is read only at 1271 (early-return test). IKeyboard.cpp reads numlock fresh at line 120 and does not read the stored field. | SUPPORTED | "On this line" scopes both negatives. The stored field does not drive the lock: setKeymap's lock block (IKeyboard.cpp:122-131) uses a fresh getDeviceInt (K08), so no sentence in the entry says the stored value drives the lock. Scope is the pinned files only. |
| K07 | The unchanged-config early return compares config names REPEATDELAY and REPEATRATE, unclamped in this expression, with stored m_repeatDelay and m_repeatRate. | Hyprland-InputManager.cpp:1271; quote `REPEATDELAY == pKeyboard->m_repeatDelay && REPEATRATE == pKeyboard->m_repeatRate` is a substring; quote PASS; upstream identical | 1270 `try {`; 1271-1273 is one `&&` chain of nine terms (NUMLOCKON, REPEATDELAY, REPEATRATE, RULES, MODEL, LAYOUT, VARIANT, OPTIONS, FILEPATH); 1274-1275 log and `return;`; 1277-1280 catch | SUPPORTED | The row says "compares"; the line does compare those two terms, and the values on the right are the stored fields that K04/K05 assign. The early return fires only when all nine terms hold, so the two-term description is a true partial, not a claim that the early return fires on a rate or delay change alone. Optional tightening: "is one of nine conjuncts of the early-return test". The negative-value consequence is already labelled [INFERENCE] in the entry's UNKNOWN list. |
| E03 | IKeyboard declares m_numlockOn with initializer -1 on this line, so the declared numlock default is -1 and not 0 or 1. | Hyprland-IKeyboard.hpp:123 `int                            m_numlockOn         = -1;`; quote `= -1;` substring PASS; upstream identical; class IKeyboard spans lines 24-137, so the member is IKeyboard's | 121-122 `m_repeatRate`/`m_repeatDelay` initialised to 0 (K18); 124 m_resolveBindsBySym; pin-wide grep: no constructor assignment of m_numlockOn in any pinned file (IKeyboard.cpp, InputManager.cpp only at 1284). InputManager.cpp:1284 overwrites the member when applyConfigToKeyboard runs. K15 at ConfigValues.cpp:277 declares input:numlock_by_default with default false. | OVERREACH | The quote proves the member initializer is -1, and that is all it proves. The phrase "the declared numlock default" sits beside K15 ("numlock_by_default ... default false"), and a reader can take it as the config option default, which the pins contradict (K15 is false; -1 appears in no config table entry). The sentence also states a value for a field that applyConfigToKeyboard overwrites at 1284. A subclass constructor could override the initializer; subclass files are not pinned, so that is UNVERIFIED. See the correction below. |
| E10 | repeatInfo records the delay argument in m_lastDelayMs on this line, before the sendRepeatInfo call that K12 cites. | Hyprland-protocols-core-Seat.cpp:445 `m_lastDelayMs = delayMs;`; quote substring PASS; upstream identical | 442 guard `if (!m_owner || m_resource->version() < 4 || (rate == m_lastRate && delayMs == m_lastDelayMs))`; 443 `return;`; 444 `m_lastRate    = rate;`; 447 `m_resource->sendRepeatInfo(rate, delayMs);` (the only sendRepeatInfo call in the pins, grep). | SUPPORTED | The write is reached only when the guard at 442 is false (owner present, version 4 or later, and the rate or delay differs). The proposition does not say "always" or "every call", so it is not an overreach; the boundary is K12's "after the early return" wording, which is correct. Line 445 precedes line 447 in the same function, so "before" holds. Adjacent: Seat.cpp:350 calls repeatInfo directly from the CWLKeyboardResource constructor (a second caller, not through updateRepeatInfo); it also reaches line 445 through the same guard. This does not change E10's label. |

## Overreach found: E03

- **Exact sentence:** "IKeyboard declares m_numlockOn with initializer -1 on this line, so the declared numlock default is -1 and not 0 or 1." (entry row E03, line 83 of the entry).
- **Cited line:** Hyprland-IKeyboard.hpp:123 `int m_numlockOn = -1;`.
- **Neighbouring lines that matter:** InputManager.cpp:1284 `pKeyboard->m_numlockOn   = NUMLOCKON;` (overwrites the member when applyConfigToKeyboard runs). ConfigValues.cpp:277 (K15, `"input:numlock_by_default", "Engage numlock by default.", false`), so the config default is false.
- **Why it is an overreach:** "the declared numlock default" can be read as the numlock_by_default config default. The quote supports only the member initializer. The pins do not support -1 as a default for any config option.
- **Minimal corrected wording:** "IKeyboard declares the member m_numlockOn with initializer -1 (Hyprland-IKeyboard.hpp:123), so a keyboard's stored numlock value starts at -1, not 0 or 1, until applyConfigToKeyboard assigns it (Hyprland-InputManager.cpp:1284). This member initializer is not the numlock_by_default config default, which ConfigValues.cpp:277 declares as false (K15)."

## Other labels with a wording option (not overreach)

- K07: "Optional tightening: 'is one of nine conjuncts of the early-return test (InputManager.cpp:1271-1273)'." The proposition as written is SUPPORTED.

## Adjacent findings outside the six rows (reported, not counted)

1. Seat.cpp:350 (`repeatInfo(g_pSeatManager->m_keyboard->m_repeatRate, g_pSeatManager->m_keyboard->m_repeatDelay);`, inside the CWLKeyboardResource constructor) is a second caller of CWLKeyboardResource::repeatInfo. It bypasses CWLSeatProtocol::updateRepeatInfo and its keyboard-capability gate (Seat.cpp:604). The entry's Chain step 5 describes the seat push through updateRepeatInfo only and does not mention this bind-time path. No sentence in the audited rows says the path is exclusive, so there is no overreach here. Any future sentence saying repeat_info reaches a client only via updateRepeatInfo would be an OVERREACH. The entry should name this path (completeness gap, for the L1).
2. Line 17 of the entry says repeatInfo "sends repeat_info only when" the owner is present, version 4 or later, and values differ. Within the pins that holds: sendRepeatInfo appears only at Seat.cpp:447. This is a pin-scoped claim; the grep covers the pins, not the whole tree.

## Could not verify

- Subclass constructors of IKeyboard (for E03): not pinned, so whether any subclass overrides m_numlockOn's initializer is UNVERIFIED.
- Whether the config layer clamps values to the K13/K14 ranges: not pinned (the entry already says UNKNOWN); not used by any audited row.
- Whole-tree uniqueness of any claim: all greps were over the pinned files only.
- Wayland 1.26.0 raw re-fetch: not performed, since none of the six rows cites the XML.
- Hyprland host state: no hyprctl command was run in this audit; the host rows are outside these six rows.

## Summary

| Row | Label |
|---|---|
| K04 | SUPPORTED |
| K05 | SUPPORTED |
| K06 | SUPPORTED |
| K07 | SUPPORTED (optional tightening) |
| E03 | OVERREACH (wording: "declared numlock default"); corrected wording above |
| E10 | SUPPORTED |
