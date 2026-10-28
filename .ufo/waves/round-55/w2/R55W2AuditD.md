# R55W2AuditD report (wave w2, sentence-to-pin audit of K11-K15)

Deliverable: `.ufo/waves/round-55/w2/R55W2AuditD/audit.md` (row table, adjacent findings, verification, not-verified list). Receipts: `.ufo/waves/round-55/w2/R55W2AuditD/receipts.txt` and `upstream-receipts/`.

## Verdicts per target

| Target | Verdict | Evidence |
|---|---|---|
| K11 (guard: version below 4 is one of three OR-joined conditions, line 442) | SUPPORTED | fetch/Hyprland-protocols-core-Seat.cpp:442; quote found once; byte-equal upstream |
| K12 (sendRepeatInfo call after early return and m_last update, line 447) | SUPPORTED | Seat.cpp:443-447; the wire-event mapping of `sendRepeatInfo` is not pinned (A3, HELD) |
| K13 (input:repeat_rate default 25, min 0, max 200) | SUPPORTED | fetch/Hyprland-ConfigValues.cpp:279; default link via upstream ConfigValues.hpp:111-113 and IntValue.cpp:5-6 (not lane-pinned) |
| K14 (input:repeat_delay default 600, min 0, max 2000) | SUPPORTED | fetch/Hyprland-ConfigValues.cpp:280 |
| K15 (input:numlock_by_default Bool, default false, "Engage numlock by default.") | SUPPORTED | fetch/Hyprland-ConfigValues.cpp:277 |

No row is OVERREACH or UNSUPPORTED. Rows K11-K15 stay inside their quotes.

## Adjacent prose findings (entry text tied to the K11/K12 chain)

- A1 OVERREACH: Chain step 5 and Scope line 17 present one seat-push route. Seat.cpp:350 (pinned, uncited) calls `repeatInfo` directly on `wl_keyboard` bind with the stored values, through the same guard. Minimal fix in audit.md A1.
- A2 OVERREACH: Scope line 17 "not both equal to the last sent values" is wrong before the first send. Seat.hpp:138-139 (upstream, not lane-pinned) initialises `m_lastRate` and `m_lastDelayMs` to 0, so the first comparison is against 0/0. Source-level consequence: a stored 0/0 suppresses the first repeat_info on both routes ([INFERENCE], not exercised). Minimal fix in audit.md A2.
- A3 HELD: the mapping of generated `sendRepeatInfo` to the `repeat_info` event is by naming convention, not pinned. Name it as an inference.
- A4 narrowing: upstream IntValue.cpp (not lane-pinned) stores min and max but `CIntValue::value()` does not test them; pinned ConfigValues.cpp:54/68/82 use them only in the descriptions dump. The enforcement UNKNOWN is therefore on the hyprlang side. Not an error in the entry.

## Commands and decisive output

- `sha256sum -c SHA256SUMS.txt` in fetch/: the three pins used here report OK.
- Upstream: `curl -sSfL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/core/Seat.cpp` (and `src/config/values/ConfigValues.cpp`, `src/managers/SeatManager.cpp`), then `cmp` against the pins: BYTE-EQUAL for all three; sha256 cc23bb8b…, a76f0507…, bd748553… matches SHA256SUMS.
- Quote check (python3 -I): each K11-K15 quote found exactly once, at the pinned line (442, 447, 279, 280, 277).
- Neighbour lines: `sed -n` and `read` on Seat.cpp 336-360, 441-447, 603-608 and ConfigValues.cpp 44-70, 276-281; grep for `m_lastRate`, `m_lastDelayMs`, `repeatInfo`, `repeat_rate`, `repeat_delay`, `numlock_by_default` across the pinned .cpp files.

## Could not verify

- hyprlang enforcement of min and max; CBoolValue parse path; generated wayland-scanner code. None are pinned or fetched.
- Any runtime behaviour. The audit is source-level only.

## Lane and host

- No lane file edited; no git or jj mutation; no hyprctl run (K11-K15 are source rows); no tool installed; no subagent used.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2AuditD/` removed after copying receipts.
- Writes: `w2/R55W2AuditD/` (audit.md, receipts.txt, upstream-receipts/) and this file.
