# Keyboard repeat rate, repeat delay and numlock on Hyprland 0.56.2 (attack fixture, not evidence)

source: S316, S317, S318, S319, S378, S379, S380, S381
verified-at: 2026-10-28
recheck: on-release

| id | proposition | source | anchor | quote |
|---|---|---|---|---|
| K01 | Restates the quoted identifiers devname getDeviceInt repeat_rate without stating a keyboard fact about K01. | S316 | Hyprland-InputManager.cpp:1220 | `getDeviceInt(devname, "repeat_rate", "input:repeat_rate");` |
| K02 | Restates the quoted identifiers devname getDeviceInt repeat_delay without stating a keyboard fact about K02. | S316 | Hyprland-InputManager.cpp:1221 | `getDeviceInt(devname, "repeat_delay", "input:repeat_delay");` |
| K03 | Restates the quoted identifiers devname getDeviceInt numlock_by_default without stating a keyboard fact about K03. | S316 | Hyprland-InputManager.cpp:1223 | `getDeviceInt(devname, "numlock_by_default", "input:numlock_by_default");` |
| K04 | Restates the quoted identifiers REPEATRATE without stating a keyboard fact about K04. | S316 | Hyprland-InputManager.cpp:1282 | `std::max(0, REPEATRATE);` |
| K05 | Restates the quoted identifiers REPEATDELAY without stating a keyboard fact about K05. | S316 | Hyprland-InputManager.cpp:1283 | `std::max(0, REPEATDELAY);` |
| K06 | Restates the quoted identifiers NUMLOCKON without stating a keyboard fact about K06. | S316 | Hyprland-InputManager.cpp:1284 | `= NUMLOCKON;` |
| K07 | Restates the quoted identifiers REPEATDELAY REPEATRATE m_repeatDelay m_repeatRate pKeyboard without stating a keyboard fact about K07. | S316 | Hyprland-InputManager.cpp:1271 | `REPEATDELAY == pKeyboard->m_repeatDelay && REPEATRATE == pKeyboard->m_repeatRate` |
| K08 | Restates the quoted identifiers getDeviceInt m_hlName numlock_by_default without stating a keyboard fact about K08. | S319 | Hyprland-IKeyboard.cpp:120 | `getDeviceInt(m_hlName, "numlock_by_default", "input:numlock_by_default");` |
| K09 | Restates the quoted identifiers NUMLOCKON without stating a keyboard fact about K09. | S319 | Hyprland-IKeyboard.cpp:122 | `if (NUMLOCKON == 1) {` |
| K10 | Restates the quoted identifiers m_keyboard m_repeatDelay m_repeatRate updateRepeatInfo without stating a keyboard fact about K10. | S378 | Hyprland-SeatManager.cpp:177 | `PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);` |
| K11 | Restates the quoted identifiers m_resource version without stating a keyboard fact about K11. | S379 | Hyprland-protocols-core-Seat.cpp:442 | `m_resource->version() < 4` |
| K12 | Restates the quoted identifiers delayMs m_resource sendRepeatInfo without stating a keyboard fact about K12. | S379 | Hyprland-protocols-core-Seat.cpp:447 | `m_resource->sendRepeatInfo(rate, delayMs);` |
| K13 | Restates the quoted identifiers repeat repeat_rate repeats second without stating a keyboard fact about K13. | S318 | Hyprland-ConfigValues.cpp:279 | `"input:repeat_rate", "The repeat rate for held-down keys, in repeats per second.", 25, {.min = 0, .max = 200` |
| K14 | Restates the quoted identifiers before milliseconds repeat_delay repeated without stating a keyboard fact about K14. | S318 | Hyprland-ConfigValues.cpp:280 | `"input:repeat_delay", "Delay before a held-down key is repeated, in milliseconds.", 600, {.min = 0, .max = 2000}` |
| K15 | Restates the quoted identifiers Engage default numlock numlock_by_default without stating a keyboard fact about K15. | S318 | Hyprland-ConfigValues.cpp:277 | `"input:numlock_by_default", "Engage numlock by default.", false` |
| K16 | Restates the quoted identifiers fallback m_bSetByUser without stating a keyboard fact about K16. | S317 | Hyprland-legacy-ConfigManager.cpp:1119 | `if ((!VAL \|\| !VAL->m_bSetByUser) && !fallback.empty())` |
| K17 | Restates the quoted identifiers disable regardless repeating without stating a keyboard fact about K17. | S381 | wayland-1.26.0-wayland.xml:2741 | `will disable any repeating (regardless of the value of delay).` |
| K18 | Restates the quoted identifiers m_repeatRate without stating a keyboard fact about K18. | S380 | Hyprland-IKeyboard.hpp:121 | `m_repeatRate        = 0;` |
| H01 | Restates the quoted identifiers repeat_rate without stating a keyboard fact about H01. | host | host-input.conf:14 | `repeat_rate = 40` |
| H02 | Restates the quoted identifiers repeat_delay without stating a keyboard fact about H02. | host | host-input.conf:15 | `repeat_delay = 250` |
| H03 | Restates the quoted identifiers numlock_by_default without stating a keyboard fact about H03. | host | host-input.conf:18 | `numlock_by_default = true` |
| H04 | Restates the quoted identifiers option repeat_rate without stating a keyboard fact about H04. | host | host-getoption.json:1 | `"option": "input:repeat_rate", "int": 40` |
| H05 | Restates the quoted identifiers option repeat_delay without stating a keyboard fact about H05. | host | host-getoption.json:2 | `"option": "input:repeat_delay", "int": 250` |
| H06 | Restates the quoted identifiers numlock_by_default option without stating a keyboard fact about H06. | host | host-getoption.json:3 | `"option": "input:numlock_by_default", "int": 1` |
