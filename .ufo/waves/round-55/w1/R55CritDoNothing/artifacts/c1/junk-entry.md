source: S316, S317, S318, S319, S378, S379, S380, S381
verified-at: 2026-10-28
recheck: on-release

# Keyboard repeat rate, repeat delay and numlock (do-nothing control)

Frozen-table transcription only: no pin was opened to write these rows.

| ID | Proposition | Source | Pin:anchor | Quote |
|---|---|---|---|---|
| K01 | placeholder K01: transcribed row, proposition text not checked against pin | S316 | Hyprland-InputManager.cpp:1220 | `getDeviceInt(devname, "repeat_rate", "input:repeat_rate");` |
| K02 | placeholder K02: transcribed row, proposition text not checked against pin | S316 | Hyprland-InputManager.cpp:1221 | `getDeviceInt(devname, "repeat_delay", "input:repeat_delay");` |
| K03 | placeholder K03: transcribed row, proposition text not checked against pin | S316 | Hyprland-InputManager.cpp:1223 | `getDeviceInt(devname, "numlock_by_default", "input:numlock_by_default");` |
| K04 | placeholder K04: transcribed row, proposition text not checked against pin | S316 | Hyprland-InputManager.cpp:1282 | `std::max(0, REPEATRATE);` |
| K05 | placeholder K05: transcribed row, proposition text not checked against pin | S316 | Hyprland-InputManager.cpp:1283 | `std::max(0, REPEATDELAY);` |
| K06 | placeholder K06: transcribed row, proposition text not checked against pin | S316 | Hyprland-InputManager.cpp:1284 | `= NUMLOCKON;` |
| K07 | placeholder K07: transcribed row, proposition text not checked against pin | S316 | Hyprland-InputManager.cpp:1271 | `REPEATDELAY == pKeyboard->m_repeatDelay && REPEATRATE == pKeyboard->m_repeatRate` |
| K08 | placeholder K08: transcribed row, proposition text not checked against pin | S319 | Hyprland-IKeyboard.cpp:120 | `getDeviceInt(m_hlName, "numlock_by_default", "input:numlock_by_default");` |
| K09 | placeholder K09: transcribed row, proposition text not checked against pin | S319 | Hyprland-IKeyboard.cpp:122 | `if (NUMLOCKON == 1) {` |
| K10 | placeholder K10: transcribed row, proposition text not checked against pin | S378 | Hyprland-SeatManager.cpp:177 | `PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);` |
| K11 | placeholder K11: transcribed row, proposition text not checked against pin | S379 | Hyprland-protocols-core-Seat.cpp:442 | `m_resource->version() < 4` |
| K12 | placeholder K12: transcribed row, proposition text not checked against pin | S379 | Hyprland-protocols-core-Seat.cpp:447 | `m_resource->sendRepeatInfo(rate, delayMs);` |
| K13 | placeholder K13: transcribed row, proposition text not checked against pin | S318 | Hyprland-ConfigValues.cpp:279 | `"input:repeat_rate", "The repeat rate for held-down keys, in repeats per second.", 25, {.min = 0, .max = 200` |
| K14 | placeholder K14: transcribed row, proposition text not checked against pin | S318 | Hyprland-ConfigValues.cpp:280 | `"input:repeat_delay", "Delay before a held-down key is repeated, in milliseconds.", 600, {.min = 0, .max = 2000}` |
| K15 | placeholder K15: transcribed row, proposition text not checked against pin | S318 | Hyprland-ConfigValues.cpp:277 | `"input:numlock_by_default", "Engage numlock by default.", false` |
| K16 | placeholder K16: transcribed row, proposition text not checked against pin | S317 | Hyprland-legacy-ConfigManager.cpp:1119 | `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` |
| K17 | placeholder K17: transcribed row, proposition text not checked against pin | S381 | wayland-1.26.0-wayland.xml:2741 | `will disable any repeating (regardless of the value of delay).` |
| K18 | placeholder K18: transcribed row, proposition text not checked against pin | S380 | Hyprland-IKeyboard.hpp:121 | `m_repeatRate        = 0;` |
| H01 | placeholder H01: host row transcribed, not checked against host pin | host | host-input.conf:14 | `repeat_rate = 40` |
| H02 | placeholder H02: host row transcribed, not checked against host pin | host | host-input.conf:15 | `repeat_delay = 250` |
| H03 | placeholder H03: host row transcribed, not checked against host pin | host | host-input.conf:18 | `numlock_by_default = true` |
| H04 | placeholder H04: host row transcribed, not checked against host pin | host | host-getoption.json:1 | `"option": "input:repeat_rate", "int": 40` |
| H05 | placeholder H05: host row transcribed, not checked against host pin | host | host-getoption.json:2 | `"option": "input:repeat_delay", "int": 250` |
| H06 | placeholder H06: host row transcribed, not checked against host pin | host | host-getoption.json:3 | `"option": "input:numlock_by_default", "int": 1` |
