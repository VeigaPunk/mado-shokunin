# R55W2AuditE report: sentence-to-pin audit of K16, K17, E04, E05, E06, E07, E11

Deliverable: `.ufo/waves/round-55/w2/R55W2AuditE/audit.md` (one table row per audited row, plus extra row X1). Receipts: `.ufo/waves/round-55/w2/R55W2AuditE/receipts/`.

## What ran

- Read the committed entry `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` (read-only) and the pins under `.ufo/waves/round-55/fetch/` with `sed -n`, `grep -n`, `cat`.
- `sha256sum -c .ufo/waves/round-55/fetch/SHA256SUMS.txt`: all 10 files OK.
- Line anchors: `sed -n '1119p;1120p' Hyprland-legacy-ConfigManager.cpp`; `sed -n '604p;605p;607p;608p' Hyprland-protocols-core-Seat.cpp`; `sed -n '2732p;2740p;2741p' wayland-1.26.0-wayland.xml`. Output matched the table lines.
- Neighbour lines read for each row: pin lines 1105-1135 (legacy ConfigManager), 596-612 and 436-450 (Seat.cpp), 2726-2748 (wayland xml).
- Machine check `receipts/check_rows.py` (python3 -I, read-only): for each of the 7 rows, confirms the quote is an exact substring of the named pin line and prints the previous and next line; also confirms the wl_keyboard interface spans 2573-2752 (E04 and K17 lines are inside it). Output `receipts/check_rows.out`: 7/7 substring True.
- Upstream re-open (curl, read-only): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` and `.../src/protocols/core/Seat.cpp` (both HTTP 200), and `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` (HTTP 200). `cmp` against the committed pin bytes: equal for all three (`receipts/upstream-cmp.txt`; sha256 9db68cf4…, cc23bb8b…, cc860987… match the SHA256SUMS). Note: the pin filenames are flattened (`Hyprland-legacy-ConfigManager.cpp` = `src/config/legacy/ConfigManager.cpp`; `Hyprland-protocols-core-Seat.cpp` = `src/protocols/core/Seat.cpp`); that mapping is my inference from the path probes returning 200 and byte-equality, which is what is verified.
- Not run: any hyprctl keyword/dispatch/reload; any command that changes state; no git/jj; no subagents; no tool installs (none needed; curl and python3 only).

## Verdict per row

| Row | Label | Evidence pointer |
|---|---|---|
| K16 | SUPPORTED | audit.md row K16; pin 1119, neighbour 1120 |
| K17 | SUPPORTED | audit.md row K17; wayland 2740-2741 |
| E04 | SUPPORTED | audit.md row E04; wayland 2732, inside wl_keyboard 2573-2752 |
| E05 | SUPPORTED | audit.md row E05; wayland 2740 |
| E06 | SUPPORTED | audit.md row E06; Seat.cpp 604, neighbours 605 and 607 |
| E07 | OVERREACH (citation scope; the claim is true) | audit.md row E07; the "for each ... loop on this line" part belongs to the loop header on line 607; line 608 is only the call. Fix: "calls `k->repeatInfo(rate, delayMs)` on line 608 once per element `k` of the `m_keyboards` loop opened on line 607." |
| E11 | SUPPORTED | audit.md row E11; wayland 2740 ends "A rate of zero" |

Extra (outside the counted rows, found while reading K16 and E12's neighbourhood): X1, the sentence in "What this entry settles" that reads "getConfigValueSafeDevice returns the global value when the device value is absent or not set by the user (K16, E12)." is OVERREACH: pin 1119 also requires `!fallback.empty()`. Minimal fix in audit.md X1. Call sites all pass non-empty fallbacks, so behaviour as described in K01-K03 is unchanged; only the sentence is unconditional.

Counts: SUPPORTED 6, OVERREACH 1 (E07), UNSUPPORTED 0, HELD 0; extra OVERREACH 1 (X1).

## Adjacent items checked (not in my assignment; no finding)

- The "What this entry settles" sentence on `CWLKeyboardResource::repeatInfo` ("sends repeat_info only when the owner is present, the resource version is 4 or later, and the rate and delay are not both equal to the last sent values"): the upstream guard at Seat.cpp:442 is `!m_owner || m_resource->version() < 4 || (rate == m_lastRate && delayMs == m_lastDelayMs)`, return at 443, and the last-value assignments at 445-446. The sentence matches. Not audited per row.

## Not verified

- Runtime behaviour of any of these rows (no client, no compositor state). Source-level only, as the entry states.
- Whether the `m_currentCaps` value at runtime has the KEYBOARD bit (E06 is the test, not its outcome).
- The `!fallback.empty()` branch's reachability for the three keys is not needed for X1's correction; callers pass non-empty names (K01-K03, K08).

## Scratch and lane

- Scratch: `/fast/scratch/hyaku/mado-r55/R55W2AuditE/` (upstream fetch copies, check script) — removed before yield.
- Lane: no tracked file was edited, no git/jj command was run in the lane or fleet repo, no commit, no subagent, no background job. The only writes are under `.ufo/waves/round-55/w2/R55W2AuditE/` and this report file.
