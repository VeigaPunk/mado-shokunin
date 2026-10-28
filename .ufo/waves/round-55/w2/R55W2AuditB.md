# R55W2AuditB report: sentence-to-pin audit of K04, K05, K06, K07, E03, E10

Deliverable: `.ufo/waves/round-55/w2/R55W2AuditB/audit.md` (table, one row per audited row). Receipts: `.ufo/waves/round-55/w2/R55W2AuditB/receipts.txt`.

## What ran

- Read the six entry rows in `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` and opened each pin line plus neighbours from `.ufo/waves/round-55/fetch/`.
- Matched every quote as a substring of its pin line by script: all six PASS.
- Grepped all pinned files for reads and writes of `m_numlockOn`, `m_lastDelayMs`, `sendRepeatInfo` and `repeatInfo(`.
- Re-fetched the four Hyprland raw files at efb50993780079460b0cbed1363e2166a2de1d9f with curl (InputManager.cpp, IKeyboard.hpp, Seat.cpp, SeatManager.cpp). All four are byte-identical to the committed pins (`cmp`) and match `SHA256SUMS.txt` (sha256 in receipts.txt).
- No hyprctl command was run. No lane file was edited. No git command was run. Scratch was used only under /fast/scratch/hyaku/mado-r55/R55W2AuditB/ and was removed before this yield. No tool was installed.

## Verdicts

| Target | Verdict | Evidence |
|---|---|---|
| K04 | SUPPORTED | InputManager.cpp:1282 `m_repeatRate  = std::max(0, REPEATRATE);`; no upper bound on the line |
| K05 | SUPPORTED | InputManager.cpp:1283 `m_repeatDelay = std::max(0, REPEATDELAY);` |
| K06 | SUPPORTED | InputManager.cpp:1284 `m_numlockOn   = NUMLOCKON;`; the stored field is read only at 1271 in the pins |
| K07 | SUPPORTED (optional tightening) | InputManager.cpp:1271-1273: the two terms are one conjunct of a nine-term `&&` early-return test |
| E03 | OVERREACH (wording) | IKeyboard.hpp:123 `m_numlockOn = -1;` supports the member initializer only; "declared numlock default" reads as the config default, which K15 (ConfigValues.cpp:277, default false) contradicts. Corrected wording in audit.md |
| E10 | SUPPORTED | Seat.cpp:445 `m_lastDelayMs = delayMs;`, after the guard at 442-443 and before the send at 447 |

Upstream re-open: InputManager.cpp, IKeyboard.hpp, Seat.cpp and SeatManager.cpp are IDENTICAL to their pins, so the pin bytes are the upstream bytes at efb50993780079460b0cbed1363e2166a2de1d9f.

## Findings

1. E03 is an OVERREACH by wording. The sentence "so the declared numlock default is -1 and not 0 or 1" must become "IKeyboard declares the member m_numlockOn with initializer -1 (Hyprland-IKeyboard.hpp:123), so a keyboard's stored numlock value starts at -1, not 0 or 1, until applyConfigToKeyboard assigns it (Hyprland-InputManager.cpp:1284). This member initializer is not the numlock_by_default config default, which ConfigValues.cpp:277 declares as false (K15)."
2. Adjacent, not in my rows: Seat.cpp:350 is a second caller of repeatInfo (bind-time push from the CWLKeyboardResource constructor). It bypasses updateRepeatInfo and its keyboard-capability gate at Seat.cpp:604. The entry's Chain step 5 omits this path. This is a completeness gap for the L1, not an overreach in the six rows.

## Could not verify

- Whether any IKeyboard subclass constructor overrides the m_numlockOn initializer: subclass files are not pinned. This is UNVERIFIED and affects only the E03 wording's "starts at -1" phrase; the corrected wording says "until applyConfigToKeyboard assigns it".
- Whether the config layer clamps the K13/K14 ranges: not pinned; the entry already marks it UNKNOWN. No audited row depends on it.
- Whole-tree uniqueness: all greps covered only the pinned files.
- The wayland 1.26.0 XML was not re-fetched: none of the six rows cites it.
- Host state: not checked in this seat.
