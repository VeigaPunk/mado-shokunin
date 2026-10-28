# R55W2AuditC report: sentence-to-pin audit of K09, K10, K18, E09, E13, E12

Scope: the six rows named in the seat spec, of `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` (scored lane revision 57584ed6). Deliverable: `.ufo/waves/round-55/w2/R55W2AuditC/audit.md` (one table row per audited row, fixes, neighbour finding). Receipts: `.ufo/waves/round-55/w2/R55W2AuditC/receipts.txt`.

## Verdicts

| Row | Label | Evidence pointer |
|---|---|---|
| K09 | SUPPORTED | audit.md row K09; fetch/Hyprland-IKeyboard.cpp:120-133 |
| K10 | SUPPORTED (clarify wording) | audit.md row K10 and fix 1; fetch/Hyprland-SeatManager.cpp:175-179 |
| K18 | SUPPORTED | audit.md row K18; fetch/Hyprland-IKeyboard.hpp:120-124 |
| E09 | SUPPORTED (type note) | audit.md row E09 and fix 2; fetch/Hyprland-SeatManager.cpp:176; upstream SeatManager.hpp:128 is `WP<IKeyboard> m_keyboard;` |
| E13 | SUPPORTED | audit.md row E13; fetch/Hyprland-protocols-core-Seat.cpp:441-448 |
| E12 | SUPPORTED | audit.md row E12; fetch/Hyprland-legacy-ConfigManager.cpp:1117-1122 |

No row is OVERREACH or UNSUPPORTED, so no corrected-sentence list is required beyond the two optional clarifications in audit.md (K10, E09).

## Findings beyond the six rows

- Neighbour omission (not an overreach): Hyprland-protocols-core-Seat.cpp:350 calls `repeatInfo(g_pSeatManager->m_keyboard->m_repeatRate, g_pSeatManager->m_keyboard->m_repeatDelay)` in the `CWLKeyboardResource` constructor (line 337), i.e. when a client obtains wl_keyboard. This second seat push reads the same stored fields and bypasses updateActiveKeyboardData and K10. The entry's chain step 5 and Scope do not cite it. Any sentence saying the seat sends repeat info only through updateActiveKeyboardData would be OVERREACH. Recommend a row (or chain note) for this path in the L1's next integration.

## What ran

- Upstream re-open at efb50993780079460b0cbed1363e2166a2de1d9f via curl of raw.githubusercontent.com: `src/devices/IKeyboard.cpp`, `src/devices/IKeyboard.hpp`, `src/managers/SeatManager.cpp`, `src/managers/SeatManager.hpp`, `src/protocols/core/Seat.cpp`, and `src/config/legacy/ConfigManager.cpp`. Full-file sha256 of each equals the committed pin in `.ufo/waves/round-55/fetch/` (receipts.txt). The committed `SHA256SUMS.txt` check (`sha256sum -c`, all rows) reports OK for every committed pin.
- Quote-substring checks (`grep -cF`): the K10 call line and the E12 return line each match once; `if (NUMLOCKON == 1) {` matches once; `if (m_keyboard)` matches twice in SeatManager.cpp (line 165 in setKeyboard, line 176 in updateActiveKeyboardData), so the E09 quote is the line 176 instance, which is the one cited.
- hyprutils WeakPtr semantics (needed for E09): curl of `include/hyprutils/memory/WeakPtr.hpp` at tags v0.14.0 (the CMake minimum, CMakeLists.txt:150), v0.14.3 (latest release) and main. `operator bool` = `valid()` = `impl_ && impl_->dataNonNull()` in all three; v0.14.0 vs v0.14.3 differ only in indentation.
- No host command was run for this seat. No hyprctl call, no config read.

## Not verified

- The hyprutils version Hyprland 0.56.2 actually links against is not in the pins. I checked the minimum (0.14.0) and two later references; the semantics relied on by E09 are the same in all three, but a version outside that range is UNVERIFIED.
- Runtime behaviour: none of the six rows is a runtime claim, and I did not test runtime behaviour.
- The wayland 1.26.0 XML was not in my six rows and was not audited.

## Mutations, scratch, writes

- No mutation test was run. No file in the lane was edited, and no git or jj command was run against the lane or the fleet repo.
- Writes: only `.ufo/waves/round-55/w2/R55W2AuditC/audit.md`, `.ufo/waves/round-55/w2/R55W2AuditC/receipts.txt` and this report.
- Scratch: `/fast/scratch/hyaku/mado-r55/R55W2AuditC/` (upstream downloads, under 1 MB). Removed before yield.
- Tools: none installed. curl (already present) was the only tool used for the upstream re-open. No pacman or uv action was taken.
