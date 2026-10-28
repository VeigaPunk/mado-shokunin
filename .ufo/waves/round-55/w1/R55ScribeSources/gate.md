# Gate block — round 55 new source rows (seat R55ScribeSources draft)

Opened 2026-10-28 from immutable commit `efb50993780079460b0cbed1363e2166a2de1d9f`; each quote re-opened from the pin named in the row's anchor cell (`.ufo/waves/round-55/fetch/`, SHA256 checked against `SHA256SUMS.txt`).

### S378 — admit

- URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/SeatManager.cpp
- Access date: 2026-10-28
- Located: `Hyprland-SeatManager.cpp:177` (upstream `src/managers/SeatManager.cpp:177`, inside `updateActiveKeyboardData` at :175-178)
- Quote: `PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);`
- Teaches: the active keyboard's stored repeat rate and delay are handed to the seat protocol inside `updateActiveKeyboardData`, and only when a keyboard is set; no host event asserted

### S379 — admit

- URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/core/Seat.cpp
- Access date: 2026-10-28
- Located: `Hyprland-protocols-core-Seat.cpp:442` (upstream `src/protocols/core/Seat.cpp:442`, guard of `CWLKeyboardResource::repeatInfo` at :441-448)
- Quote: `if (!m_owner || m_resource->version() < 4 || (rate == m_lastRate && delayMs == m_lastDelayMs))`
- Teaches: wl_keyboard repeat info is sent only to keyboard resources of version 4 or later, and only when the rate or delay differs from the last pair sent

### S380 — admit

- URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.hpp
- Access date: 2026-10-28
- Located: `Hyprland-IKeyboard.hpp:121` (upstream `src/devices/IKeyboard.hpp:121`; members at :121-123)
- Quote: `m_repeatRate        = 0;`
- Teaches: each keyboard header declares its repeat rate and repeat delay as int fields initialised to 0, and its numlock state as an int initialised to -1
