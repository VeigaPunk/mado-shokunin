# Keyboard repeat rate, repeat delay and numlock (round 55)

source: S316, S317, S318, S319, S378, S379, S380, S381
verified-at: 2026-10-28
recheck: on-release

| id | proposition | source | anchor | quote |
|---|---|---|---|---|
| K01 | Placeholder proposition for row K01 that pads the length check and asserts nothing about the pinned code at all. | S316 | Hyprland-InputManager.cpp:1220 | `getDeviceInt(devname, "repeat_rate", "input:repeat_rate");` |
| K02 | Placeholder proposition for row K02 that pads the length check and asserts nothing about the pinned code at all. | S316 | Hyprland-InputManager.cpp:1221 | `getDeviceInt(devname, "repeat_delay", "input:repeat_delay");` |
| K03 | Placeholder proposition for row K03 that pads the length check and asserts nothing about the pinned code at all. | S316 | Hyprland-InputManager.cpp:1223 | `getDeviceInt(devname, "numlock_by_default", "input:numlock_by_default");` |
| K04 | Placeholder proposition for row K04 that pads the length check and asserts nothing about the pinned code at all. | S316 | Hyprland-InputManager.cpp:1282 | `std::max(0, REPEATRATE);` |
| K05 | Placeholder proposition for row K05 that pads the length check and asserts nothing about the pinned code at all. | S316 | Hyprland-InputManager.cpp:1283 | `std::max(0, REPEATDELAY);` |
| K06 | Placeholder proposition for row K06 that pads the length check and asserts nothing about the pinned code at all. | S316 | Hyprland-InputManager.cpp:1284 | `= NUMLOCKON;` |
| K07 | Placeholder proposition for row K07 that pads the length check and asserts nothing about the pinned code at all. | S316 | Hyprland-InputManager.cpp:1271 | `REPEATDELAY == pKeyboard->m_repeatDelay && REPEATRATE == pKeyboard->m_repeatRate` |
| K08 | Placeholder proposition for row K08 that pads the length check and asserts nothing about the pinned code at all. | S319 | Hyprland-IKeyboard.cpp:120 | `getDeviceInt(m_hlName, "numlock_by_default", "input:numlock_by_default");` |
| K09 | Placeholder proposition for row K09 that pads the length check and asserts nothing about the pinned code at all. | S319 | Hyprland-IKeyboard.cpp:122 | `if (NUMLOCKON == 1) {` |
| K10 | Placeholder proposition for row K10 that pads the length check and asserts nothing about the pinned code at all. | S378 | Hyprland-SeatManager.cpp:177 | `PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);` |
| K11 | Placeholder proposition for row K11 that pads the length check and asserts nothing about the pinned code at all. | S379 | Hyprland-protocols-core-Seat.cpp:442 | `m_resource->version() < 4` |
| K12 | Placeholder proposition for row K12 that pads the length check and asserts nothing about the pinned code at all. | S379 | Hyprland-protocols-core-Seat.cpp:447 | `m_resource->sendRepeatInfo(rate, delayMs);` |
| K13 | Placeholder proposition for row K13 that pads the length check and asserts nothing about the pinned code at all. | S318 | Hyprland-ConfigValues.cpp:279 | `"input:repeat_rate", "The repeat rate for held-down keys, in repeats per second.", 25, {.min = 0, .max = 200` |
| K14 | Placeholder proposition for row K14 that pads the length check and asserts nothing about the pinned code at all. | S318 | Hyprland-ConfigValues.cpp:280 | `"input:repeat_delay", "Delay before a held-down key is repeated, in milliseconds.", 600, {.min = 0, .max = 2000}` |
| K15 | Placeholder proposition for row K15 that pads the length check and asserts nothing about the pinned code at all. | S318 | Hyprland-ConfigValues.cpp:277 | `"input:numlock_by_default", "Engage numlock by default.", false` |
| K16 | Placeholder proposition for row K16 that pads the length check and asserts nothing about the pinned code at all. | S317 | Hyprland-legacy-ConfigManager.cpp:1119 | `if ((!VAL \|\| !VAL->m_bSetByUser) && !fallback.empty())` |
| K17 | Placeholder proposition for row K17 that pads the length check and asserts nothing about the pinned code at all. | S052 | wayland-1.26.0-wayland.xml:2741 | `will disable any repeating (regardless of the value of delay).` |
| K18 | Placeholder proposition for row K18 that pads the length check and asserts nothing about the pinned code at all. | S380 | Hyprland-IKeyboard.hpp:121 | `m_repeatRate        = 0;` |
| H01 | Filler host row H01, padding text, no claim here at all. | host | host-input.conf:14 | `repeat_rate = 40` |
| H02 | Filler host row H02, padding text, no claim here at all. | host | host-input.conf:15 | `repeat_delay = 250` |
| H03 | Filler host row H03, padding text, no claim here at all. | host | host-input.conf:18 | `numlock_by_default = true` |
| H04 | Filler host row H04, padding text, no claim here at all. | host | host-getoption.json:1 | `"option": "input:repeat_rate", "int": 40` |
| H05 | Filler host row H05, padding text, no claim here at all. | host | host-getoption.json:2 | `"option": "input:repeat_delay", "int": 250` |
| H06 | Filler host row H06, padding text, no claim here at all. | host | host-getoption.json:3 | `"option": "input:numlock_by_default", "int": 1` |
