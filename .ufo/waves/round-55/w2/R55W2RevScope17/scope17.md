# R55W2RevScope17 — QUALITY 17 distinct-scope review of round-55 W04 warnings

Scored lane revision: 57584ed67716340b3d466fa04333ac0bab3fb79e. `corpus/SOURCES.md` in the working tree is byte-identical to that revision (`cmp`). Base: 3b55b6e.

## 1. Census run and diff

Command (read-only validation, no writes to the lane):

    /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado > .../w2/R55W2RevScope17/validate-now.txt

Exit status 0. Output has 27 W01/W04 lines plus the census summary (copy: `w2/R55W2RevScope17/validate-now.txt`).

Diff against `round-55/receipts/census-before.txt` (`diff`):

    26a27
    > mado	W04	S380 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.hpp across scopes
    28d28
    < exit=0

The `exit=0` removal is a capture artifact of the base receipt, not a census change. **The only new W01/W04 line since base is `S380` W04.** The other 26 lines (W04 for S030, S042, S045, S097, S119–S121, S303, S307, S317, S318, S320, S321, S324, S326, S327, S332, S353, S354, S364, S366, S368, S370, S371, S373; W01 for S277) are pre-existing.

The census keys W04 on (URL, scope string): it fires when a URL was already seen under a different scope string, and an identical (URL, scope) pair would give E04 instead. W04 is a warning and does not fail validation (census header line 33; `exit=0`).

## 2. S380 versus S363 (same URL, same bytes)

Both rows cite `src/devices/IKeyboard.hpp` at commit efb50993780079460b0cbed1363e2166a2de1d9f. The fetched pins are byte-identical (sha256 82e0bc9e1f31f6342f193b0981000245b932719cf406988d98aba64f0f716f05 for `round-50/fetch` and `round-55/fetch`). Anchors checked against the pin with `cat -n`:

| row | anchor lines | pin content at those lines | scope (registry cell) |
|---|---|---|---|
| S363 | 13-22 | `enum eKeyboardModifiers`, HL_MODIFIER_SHIFT=1<<0 … HL_MODIFIER_MOD5=1<<7 | bit values of Hyprland's modifier mask; where per-keyboard bind states and resolve flag live |
| S363 | 100-101 | `m_xkbStaticState`, `m_xkbSymState` | (same scope) |
| S363 | 124 | `bool m_resolveBindsBySym = false;` | (same scope) |
| S380 | 121-123 | `m_repeatRate = 0`, `m_repeatDelay = 0`, `m_numlockOn = -1` | storage members for repeat rate, repeat delay and numlock state |

**Verdict: scopes are distinct and the ranges are disjoint** (S363 covers 13-22, 100-101, 124; S380 covers 121-123; no line is in both). Distinct scope strings mean no E04, and the W04 warning is the correct classification. The precedent is S030, which was rejected for an *overlapping* scope duplicate with no `supersedes` link (`corpus/SOURCES.md` line 412). These do not overlap, so no rejection is warranted.

What each teaches: S363 teaches the modifier bit layout and where bind-state fields sit; S380 teaches the declared initial values of the repeat and numlock storage (0, 0, -1). The `teaches` cell of S380 matches the pin.

**Defect (BROKEN, scope cell only):** the S380 scope cell reads "per-keyboard storage members for repeat rate, repeat delay and numlock state, **read by `updateActiveKeyboardData` (S378)**". The S378 pin does not support the numlock part:

- `round-55/fetch/Hyprland-SeatManager.cpp:175-178` (`updateActiveKeyboardData`) reads only `m_keyboard->m_repeatRate` and `m_keyboard->m_repeatDelay` (line 177). `m_numlockOn` is not read there.
- `round-55/fetch/Hyprland-InputManager.cpp:1271` reads `m_numlockOn` (a comparison); `:1282-1284` writes `m_repeatRate`, `m_repeatDelay`, `m_numlockOn`. Neither is `updateActiveKeyboardData`.

The knowledge entry is correct: `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` K10 (line 52) and line 17 say only rate and delay go through `updateActiveKeyboardData`, and K06/E03 treat numlock separately. The overclaim is only in the registry scope cell. Per the `corpus/SOURCES.md` header (only `status`, `recheck`, `used-by` change in place), the cell cannot be corrected in place; the remedy is an append-only correction note (lesson or the knowledge entry), not a silent edit.

## 3. S378 / S379 URL duplication

Grep of the base registry (`git show 3b55b6e:corpus/SOURCES.md`) for `src/managers/SeatManager.cpp` and `src/protocols/core/Seat.cpp`: **0 hits each**. Grep of the scored registry: each URL appears exactly once, in its own new row (S378 line 328, S379 line 329). **No URL is already registered; the census confirms this (no W04 for S378/S379).**

Anchors checked against the pins:

- S378 `SeatManager.cpp:175-178`: function at 175, repeat hand-off at 177, `if (m_keyboard)` guard at 176. Matches.
- S379 `Seat.cpp:441-448` (`repeatInfo`: version < 4 gate and change suppression at 442, `sendRepeatInfo` at 447) and `:603-609` (`updateRepeatInfo`: keyboard-capability gate at 604). Matches.

## 4. S052 (wl_keyboard :2573-2699) versus K17 (line 2741)

Pin: `round-55/fetch/wayland-1.26.0-wayland.xml`; sha256 cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07, equal to the value S052 records.

- `<interface name="wl_keyboard" version="11">` opens at **2573** and closes at **2752** (`</interface>`). S052's anchor stops at **2699** (the `key` event's end).
- The `repeat_info` event (`since="4"`) spans **2732-2751**. Line 2740 is "…are illegal. A rate of zero", line 2741 is "will disable any repeating (regardless of the value of delay)." K17's quote and subject line match the pin exactly.

**Conclusion: S052's anchor does not cover K17 (2741), E04 (2732) or E05 (2740).** The row remains accurate for its own range.

What the entry does about it: `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` line 138 says "Registry anchor gaps (registry rows are append-only … so they are recorded here rather than widened): … S052 records wl_keyboard :2573-2699, which does not reach K17 at line 2741 or E04 and E05 … (the wl_keyboard interface runs 2573-2752 in the pin)", and that the counter would not catch it. **So the gap is disclosed, not repaired.** K17, E04 and E05 are still cited to S052 in their table rows, and the registry has no row covering 2732-2751. The text of K17 is correct (I verified it against the pin); what is missing is a registry anchor for it.

Remedy options (none applied, since I edit nothing in the lane): (a) a new distinct-scope row for the same URL and tag covering `wl_keyboard repeat_info` 2732-2751 — this yields one more W04, the same as S380; or (b) keep the disclosure and state in the lesson that K17/E04/E05 are unregistered-anchor. Option (a) is what the S363/S380 pattern already does.

## 5. S215 versus S318 (same ConfigValues.cpp URL)

- Same file: S215 records the sha prefix `a76f05079454e1f6`; S318 records the full sha `a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754`. The pin `round-55/fetch/Hyprland-ConfigValues.cpp` (59222 B) hashes to that value. Prefix consistent.
- Anchors disjoint (checked on the pin):
  - S215: `:629` `MS<Bool>("debug:disable_logs", …, true)`; `:632` `MS<Bool>("debug:enable_stdout_logs", …, false)`.
  - S318: `:271-279` input kb_* options, `:277` numlock_by_default, `:279` repeat_rate; `:296` scroll_factor.
- Scopes distinct (log switches vs keyboard names/scroll factor): no E04, no overlap, no `supersedes` needed.
- **Pre-existing, not introduced this round:** the W04 for S318 is in `census-before.txt`; S215 is the first-registered row, so the census flags only the second.

Duplication matters only for maintenance: a re-pin of ConfigValues.cpp must re-anchor both rows, and S215 carries only a sha prefix. It does not produce a wrong claim. **SURVIVES (no action required).**

Side note on S318: its anchor ends at 279 and does not reach `input:repeat_delay` at 280; the knowledge entry already discloses that at line 138 (K14).

## Summary table

| target | verdict | evidence |
|---|---|---|
| New W01/W04 since base = S380 W04 only | SURVIVES (as warning) | census diff; validate exit 0 |
| S380 vs S363 distinct scopes | SURVIVES | pin `IKeyboard.hpp` 13-22, 100-101, 124 vs 121-123; scope cells differ |
| S380 scope cell "numlock read by updateActiveKeyboardData" | BROKEN (registry scope cell overclaim; knowledge entry K10 correct) | pin `SeatManager.cpp:177` reads rate/delay only; `InputManager.cpp:1271,1284` numlock |
| S378/S379 URLs not already registered | SURVIVES | base grep 0 hits; scored grep one hit each; anchors match pins |
| S052 `:2573-2699` covers K17 `:2741` | BROKEN (anchor does not cover; disclosed at knowledge line 138, not repaired) | pin `wayland-1.26.0-wayland.xml` interface 2573-2752, repeat_info 2732-2751 |
| S215 vs S318 duplication | SURVIVES (distinct scopes, disjoint anchors, pre-existing) | pin `ConfigValues.cpp` 629/632 vs 271-279/296 |

## Not verified / limits

- I did not re-open the wider knowledge entry claims beyond those listed (K10, K17, E04, E05, line 138, line 17).
- No mutation test and no fixture were run; the census was run read-only against the working tree (identical to 57584ed).
- No hyprctl, no network, no installs, no lane writes. Receipts: `w2/R55W2RevScope17/validate-now.txt`.
