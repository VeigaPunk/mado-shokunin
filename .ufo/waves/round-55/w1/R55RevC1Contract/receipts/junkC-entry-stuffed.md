# Keyboard repeat rate, repeat delay and numlock (round 55)

source: S316, S317, S318, S319, S378, S379, S380, S381
verified-at: 2026-10-28
recheck: on-release

| id | proposition | source | anchor | quote |
|---|---|---|---|---|
| K01 | compositor anchor value rate record seat pointer device names getDeviceInt and devname from Hyprland-InputManager.cpp:1220. | S316 | Hyprland-InputManager.cpp:1220 | `getDeviceInt(devname, "repeat_rate", "input:repeat_rate");` |
| K02 | config line keymap seat global record claim pointer names getDeviceInt and devname from Hyprland-InputManager.cpp:1221. | S316 | Hyprland-InputManager.cpp:1221 | `getDeviceInt(devname, "repeat_delay", "input:repeat_delay");` |
| K03 | index delay pointer row table device anchor seat names getDeviceInt and devname from Hyprland-InputManager.cpp:1223. | S316 | Hyprland-InputManager.cpp:1223 | `getDeviceInt(devname, "numlock_by_default", "input:numlock_by_default");` |
| K04 | row anchor record compositor claim keymap seat entry names REPEATRATE and REPEATRATE from Hyprland-InputManager.cpp:1282. | S316 | Hyprland-InputManager.cpp:1282 | `std::max(0, REPEATRATE);` |
| K05 | source seat row anchor device value pin delay names REPEATDELAY and REPEATDELAY from Hyprland-InputManager.cpp:1283. | S316 | Hyprland-InputManager.cpp:1283 | `std::max(0, REPEATDELAY);` |
| K06 | pin device timer keymap record anchor event default names value and line from Hyprland-InputManager.cpp:1284. | S316 | Hyprland-InputManager.cpp:1284 | `= NUMLOCKON;` |
| K07 | config keymap anchor compositor record line timer device names REPEATDELAY and REPEATRATE from Hyprland-InputManager.cpp:1271. | S316 | Hyprland-InputManager.cpp:1271 | `REPEATDELAY == pKeyboard->m_repeatDelay && REPEATRATE == pKeyboard->m_repeatRate` |
| K08 | value keymap seat layout config option event device names getDeviceInt and m_hlName from Hyprland-IKeyboard.cpp:120. | S319 | Hyprland-IKeyboard.cpp:120 | `getDeviceInt(m_hlName, "numlock_by_default", "input:numlock_by_default");` |
| K09 | index frame host numlock keymap claim line pin names if and NUMLOCKON from Hyprland-IKeyboard.cpp:122. | S319 | Hyprland-IKeyboard.cpp:122 | `if (NUMLOCKON == 1) {` |
| K10 | option source default repeat frame row pointer keymap names value and line from Hyprland-SeatManager.cpp:177. | S378 | Hyprland-SeatManager.cpp:177 | `PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);` |
| K11 | layout global option claim host buffer numlock pin names value and line from Hyprland-protocols-core-Seat.cpp:442. | S379 | Hyprland-protocols-core-Seat.cpp:442 | `m_resource->version() < 4` |
| K12 | value timer global delay default frame host record names rate and delayMs from Hyprland-protocols-core-Seat.cpp:447. | S379 | Hyprland-protocols-core-Seat.cpp:447 | `m_resource->sendRepeatInfo(rate, delayMs);` |
| K13 | record delay seat event pointer frame device keymap names repeat and rate from Hyprland-ConfigValues.cpp:279. | S318 | Hyprland-ConfigValues.cpp:279 | `"input:repeat_rate", "The repeat rate for held-down keys, in repeats per second.", 25, {.min = 0, .max = 200` |
| K14 | compositor host repeat line layout option keymap numlock names before and a from Hyprland-ConfigValues.cpp:280. | S318 | Hyprland-ConfigValues.cpp:280 | `"input:repeat_delay", "Delay before a held-down key is repeated, in milliseconds.", 600, {.min = 0, .max = 2000}` |
| K15 | value entry pointer quote option repeat event table names numlock and by from Hyprland-ConfigValues.cpp:277. | S318 | Hyprland-ConfigValues.cpp:277 | `"input:numlock_by_default", "Engage numlock by default.", false` |
| K16 | timer buffer repeat pin compositor keymap event numlock names if and if from Hyprland-legacy-ConfigManager.cpp:1119. | S317 | Hyprland-legacy-ConfigManager.cpp:1119 | `if ((!VAL \|\| !VAL->m_bSetByUser) && !fallback.empty())` |
| K17 | keymap repeat rate claim event line keyboard numlock names will and disable from wayland-1.26.0-wayland.xml:2741. | S381 | wayland-1.26.0-wayland.xml:2741 | `will disable any repeating (regardless of the value of delay).` |
| K18 | repeat default layout timer option seat config frame names m_repeatRate and m_repeatRate from Hyprland-IKeyboard.hpp:121. | S380 | Hyprland-IKeyboard.hpp:121 | `m_repeatRate        = 0;` |
| H01 | keymap value buffer row rate index option pointer names repeat_rate and repeat_rate from host-input.conf:14. | host | host-input.conf:14 | `repeat_rate = 40` |
| H02 | host numlock rate device quote value delay claim names repeat_delay and repeat_delay from host-input.conf:15. | host | host-input.conf:15 | `repeat_delay = 250` |
| H03 | device repeat delay line event rate row value names numlock_by_default and true from host-input.conf:18. | host | host-input.conf:18 | `numlock_by_default = true` |
| H04 | default record value row event claim keyboard option names value and line from host-getoption.json:1. | host | host-getoption.json:1 | `"option": "input:repeat_rate", "int": 40` |
| H05 | line quote pin keyboard value delay device record names value and line from host-getoption.json:2. | host | host-getoption.json:2 | `"option": "input:repeat_delay", "int": 250` |
| H06 | compositor anchor value repeat index global layout record names value and line from host-getoption.json:3. | host | host-getoption.json:3 | `"option": "input:numlock_by_default", "int": 1` |
