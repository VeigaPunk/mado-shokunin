source: S052, S316, S317, S318, S319, S378, S379, S380 (host records: fetch/host-input.conf, fetch/host-getoption.json)
verified-at: 2026-10-28
recheck: on-release

# Keyboard repeat rate, repeat delay and numlock on Hyprland 0.56.2 (source plane and host join)

Pins: Hyprland commit efb50993780079460b0cbed1363e2166a2de1d9f (tag v0.56.2), wayland 1.26.0 wayland.xml, and two host files, all committed under .ufo/waves/round-55/fetch/ with sha256 values in SHA256SUMS.txt. Each proposition starts with a tag. HELD: the quote is on the cited pin line. INFERENCE: derived from held lines, not quoted. UNKNOWN: no pin settles it. Source-level behaviour is never a claim about what the running host did.

## What this entry settles

At source level (HELD on the rows K01-K18 and E rows): each keyboard's repeat rate, repeat delay and numlock value is read through getDeviceInt with the global key as fallback; the rate and delay are stored clamped at zero; numlock is stored and is also read a second time by the keymap step, which locks NumLock when that integer equals 1 (the only lock in the pinned keymap step); the stored rate and delay are forwarded to the seat protocol, and each wl_keyboard resource at protocol version 4 or later is asked to send them. The global defaults are 25, 600 and false, with ranges 0 to 200 for the rate and 0 to 2000 for the delay.

About the host (HELD on the declarations and the committed read): input.conf declares repeat_rate = 40, repeat_delay = 250 and numlock_by_default = true (H01-H03); the committed getoption record returned int 40, int 250 and int 1 (H04-H06). A declaration is not a delivery to clients.

## What stays UNKNOWN

- Whether any client received repeat_info on the running host. No run was observed.
- The effective value on each live keyboard. Only global values were read; getoption shows the global option and no device override, and device blocks outside input.conf were not read.
- Whether NumLock was locked on any live keyboard.
- Numlock values other than 0 or 1. No pin shows a Bool clamp; the K15 declaration has no min or max.
- Whether m_keymapOverridden is set on any live keyboard (E03).
- The meaning of the set flag in the getoption record.

## Chain

1. Options. Global defaults and ranges: K13, K14, K15, E10. A device lookup falls back to the global key when the device value is absent or not user-set (K16); a missing value reads as 0 (E02).
2. applyConfigToKeyboard reads the three values (K01, K02, K03), stores clamped rate and delay (K04, K05) and numlock (K06). It returns early when numlock, rate and delay and the rules are unchanged (K07 with line 1271 and lines 1272-1275; E05).
3. The keymap step, IKeyboard::setKeymap: a second numlock read (K08); the lock branch runs only when that value equals 1 (K09); the function returns early when the keymap is overridden (E03); when it completes it calls updateActiveKeyboardData (E04).
4. The seat. SeatManager::setKeyboard stores the new keyboard and calls updateActiveKeyboardData (E13). That function forwards the stored rate and delay (K10) to the protocol updateRepeatInfo, which returns early without the keyboard capability (E08) and otherwise calls repeatInfo on each keyboard resource (E09).
5. The client send. CWLKeyboardResource::repeatInfo returns early for version below 4 (K11) and when the values are unchanged (same line 442, not in the quote). Otherwise it calls sendRepeatInfo (K12). That the generated sender maps to the repeat_info event is INFERENCE from its name; the generator is not pinned.
6. Bind time. A new wl_keyboard resource sends the stored values once (E07). The protocol text says the event is sent after creation and before any key event (E11).
7. Storage defaults: m_repeatRate and m_repeatDelay start at 0 (K18); m_numlockOn starts at -1 (E14).
8. Protocol meaning: a rate of zero disables repeating whatever the delay (K17); negative values are illegal (E12). Lines 1282-1283 (K04, K05) store negatives as 0. Whether the sent value is the stored value is INFERENCE from steps 4 to 5. No pin here shows an upper bound enforced on the stored rate or delay; UNKNOWN.

## Keymap rows K01-K18

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| K01 | HELD: applyConfigToKeyboard assigns REPEATRATE from getDeviceInt with the device name, the key repeat_rate, and input:repeat_rate as fallback key. | S316 | Hyprland-InputManager.cpp:1220 | `getDeviceInt(devname, "repeat_rate", "input:repeat_rate");` |
| K02 | HELD: applyConfigToKeyboard assigns REPEATDELAY from getDeviceInt with the device name, the key repeat_delay, and input:repeat_delay as fallback key. | S316 | Hyprland-InputManager.cpp:1221 | `getDeviceInt(devname, "repeat_delay", "input:repeat_delay");` |
| K03 | HELD: applyConfigToKeyboard assigns NUMLOCKON from getDeviceInt with the device name, the key numlock_by_default, and input:numlock_by_default as fallback key. | S316 | Hyprland-InputManager.cpp:1223 | `getDeviceInt(devname, "numlock_by_default", "input:numlock_by_default");` |
| K04 | HELD: the stored m_repeatRate receives std::max(0, REPEATRATE), so a negative value read from config is stored as 0; this line sets no upper bound. | S316 | Hyprland-InputManager.cpp:1282 | `std::max(0, REPEATRATE);` |
| K05 | HELD: the stored m_repeatDelay receives std::max(0, REPEATDELAY), so a negative value read from config is stored as 0; this line sets no upper bound. | S316 | Hyprland-InputManager.cpp:1283 | `std::max(0, REPEATDELAY);` |
| K06 | HELD: the stored m_numlockOn receives the NUMLOCKON integer on this line; this line does not lock NumLock (the lock is in IKeyboard::setKeymap). | S316 | Hyprland-InputManager.cpp:1284 | `= NUMLOCKON;` |
| K07 | HELD: this quote is the repeat delay and repeat rate part of the test, whose other conjuncts are on line 1271 and are not in this quote. | S316 | Hyprland-InputManager.cpp:1271 | `REPEATDELAY == pKeyboard->m_repeatDelay && REPEATRATE == pKeyboard->m_repeatRate` |
| K08 | HELD: IKeyboard::setKeymap reads numlock_by_default a second time through getDeviceInt with the keyboard m_hlName; the first reader is K03. | S319 | Hyprland-IKeyboard.cpp:120 | `getDeviceInt(m_hlName, "numlock_by_default", "input:numlock_by_default");` |
| K09 | HELD: the NumLock lock branch is entered only when the integer read at line 120 equals exactly 1; any other integer skips the branch at lines 123-131. | S319 | Hyprland-IKeyboard.cpp:122 | `if (NUMLOCKON == 1) {` |
| K10 | HELD: updateActiveKeyboardData passes the active keyboard's stored m_repeatRate and m_repeatDelay, not the config values, to updateRepeatInfo. | S378 | Hyprland-SeatManager.cpp:177 | `PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);` |
| K11 | HELD: CWLKeyboardResource::repeatInfo returns without sending when the resource version is below 4; this is one early-return condition (the other is on line 442). | S379 | Hyprland-protocols-core-Seat.cpp:442 | `m_resource->version() < 4` |
| K12 | HELD: after its early-return checks, CWLKeyboardResource::repeatInfo passes rate and delay to sendRepeatInfo on this resource; the generated sender is INFERENCE. | S379 | Hyprland-protocols-core-Seat.cpp:447 | `m_resource->sendRepeatInfo(rate, delayMs);` |
| K13 | HELD: the value table declares input:repeat_rate with default 25 and integer range minimum 0 and maximum 200 on this line. | S318 | Hyprland-ConfigValues.cpp:279 | `"input:repeat_rate", "The repeat rate for held-down keys, in repeats per second.", 25, {.min = 0, .max = 200` |
| K14 | HELD: the value table declares input:repeat_delay with default 600 and integer range minimum 0 and maximum 2000 on this line. | S318 | Hyprland-ConfigValues.cpp:280 | `"input:repeat_delay", "Delay before a held-down key is repeated, in milliseconds.", 600, {.min = 0, .max = 2000}` |
| K15 | HELD: the value table declares input:numlock_by_default with default false on this line; the quoted declaration carries no min or max. | S318 | Hyprland-ConfigValues.cpp:277 | `"input:numlock_by_default", "Engage numlock by default.", false` |
| K16 | HELD: getConfigValueSafeDevice returns the global fallback value when the device value is absent or was not set by the user and a fallback key is given. | S317 | Hyprland-legacy-ConfigManager.cpp:1119 | `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` |
| K17 | HELD: the wayland 1.26.0 repeat_info text says repeating is disabled regardless of the delay value; its subject a rate of zero is on line 2740, outside this quote. | S052 | wayland-1.26.0-wayland.xml:2741 | `will disable any repeating (regardless of the value of delay).` |
| K18 | HELD: the IKeyboard member m_repeatRate has in-class initial value 0 in its declaration on this line, before any applyConfigToKeyboard write. | S380 | Hyprland-IKeyboard.hpp:121 | `m_repeatRate        = 0;` |

## Host rows H01-H06

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| H01 | HELD (declared): input.conf line 14 declares repeat_rate = 40 in the input block; a declaration in the file is not a delivery to clients. | host | host-input.conf:14 | `repeat_rate = 40` |
| H02 | HELD (declared): input.conf line 15 declares repeat_delay = 250 in the input block; this is file text, not a delivered value. | host | host-input.conf:15 | `repeat_delay = 250` |
| H03 | HELD (declared): input.conf line 18 declares numlock_by_default = true; the spelling true is file text and the integer read is H06. | host | host-input.conf:18 | `numlock_by_default = true` |
| H04 | HELD (live read, committed record): the getoption record for input:repeat_rate holds int 40; this is the global option, not a device value. | host | host-getoption.json:1 | `"option": "input:repeat_rate", "int": 40` |
| H05 | HELD (live read, committed record): the getoption record for input:repeat_delay holds int 250; this is the global option, not a device value. | host | host-getoption.json:2 | `"option": "input:repeat_delay", "int": 250` |
| H06 | HELD (live read, committed record): the getoption record for input:numlock_by_default holds int 1; INFERENCE: the integer form of the declared true. | host | host-getoption.json:3 | `"option": "input:numlock_by_default", "int": 1` |

## Extra rows E01-E15

Facts beyond the frozen anchors. The counter ignores these rows; verify_entry.py checks each quote against its pin line.

| id | proposition | source | pin:line | quote |
|---|---|---|---|---|
| E01 | HELD: getDeviceInt returns the stored value by std::any_cast to Hyprlang::INT, so the caller receives an integer; INFERENCE: a Bool option is read through the same cast. | S317 | Hyprland-legacy-ConfigManager.cpp:1136 | `return std::any_cast<Hyprlang::INT>(val->getValue());` |
| E02 | HELD: when getConfigValueSafeDevice yields no value (the branch at line 1133), getDeviceInt returns a value-initialized int, so a missing value reads as 0. | S317 | Hyprland-legacy-ConfigManager.cpp:1134 | `return {};` |
| E03 | HELD: when m_keymapOverridden is set, setKeymap logs and returns (lines 62-63, outside this quote), so the numlock read at line 120 and the lock at lines 122-131 are not reached. | S319 | Hyprland-IKeyboard.cpp:61 | `if (m_keymapOverridden) {` |
| E04 | HELD: the last statement of setKeymap (its closing brace is line 148) calls updateActiveKeyboardData, forwarding the stored repeat values to the seat protocol (K10). | S319 | Hyprland-IKeyboard.cpp:147 | `g_pSeatManager->updateActiveKeyboardData();` |
| E05 | HELD: the stored m_numlockOn is compared with NUMLOCKON as one conjunct of the early-return test at line 1271; in the pinned files m_numlockOn is read only there and written only at line 1284. | S316 | Hyprland-InputManager.cpp:1271 | `NUMLOCKON == pKeyboard->m_numlockOn` |
| E06 | HELD: the seat setKeyboard call follows the applyConfigToKeyboard(keeb) call at line 1195, so the stored values are applied before the keyboard becomes the seat's active keyboard. | S316 | Hyprland-InputManager.cpp:1197 | `g_pSeatManager->setKeyboard(keeb);` |
| E07 | HELD: the constructor of a new wl_keyboard resource sends the active keyboard's stored repeat rate and delay once through repeatInfo; line 350 is outside S379's listed anchors. | S379 | Hyprland-protocols-core-Seat.cpp:350 | `repeatInfo(g_pSeatManager->m_keyboard->m_repeatRate, g_pSeatManager->m_keyboard->m_repeatDelay);` |
| E08 | HELD: CWLSeatProtocol::updateRepeatInfo returns before forwarding anything when the seat's current capabilities lack the keyboard bit. | S379 | Hyprland-protocols-core-Seat.cpp:604 | `if (!(m_currentCaps & eHIDCapabilityType::HID_INPUT_CAPABILITY_KEYBOARD))` |
| E09 | HELD: CWLSeatProtocol::updateRepeatInfo calls repeatInfo once for each keyboard resource in m_keyboards, with the same rate and delay. | S379 | Hyprland-protocols-core-Seat.cpp:608 | `k->repeatInfo(rate, delayMs);` |
| E10 | HELD: at this line input:numlock_by_default is declared with the template type Bool (MS<Bool>), not Int, in the global value table. | S318 | Hyprland-ConfigValues.cpp:277 | `MS<Bool>("input:numlock_by_default"` |
| E11 | HELD: the wayland 1.26.0 repeat_info description says the event is sent as soon as the wl_keyboard object has been created; lines 2737-2738 add that it precedes any key event. | S052 | wayland-1.26.0-wayland.xml:2736 | `This event is sent as soon as the wl_keyboard object has been created,` |
| E12 | HELD: the wayland 1.26.0 repeat_info description declares negative values for either rate or delay illegal. | S052 | wayland-1.26.0-wayland.xml:2740 | `Negative values for either rate or delay are illegal.` |
| E13 | HELD: SeatManager::setKeyboard calls updateActiveKeyboardData at this line after storing the new active keyboard (line 167); line 172 is outside S378's listed anchor 175-178. | S378 | Hyprland-SeatManager.cpp:172 | `updateActiveKeyboardData();` |
| E14 | HELD: the IKeyboard member m_numlockOn has in-class initial value -1 on this line, so the first early-return comparison at line 1271 compares against -1. | S380 | Hyprland-IKeyboard.hpp:123 | `= -1;` |
| E15 | HELD: applyConfigToKeyboard takes the device name from the keyboard m_hlName at this line; the same name is used by the second numlock reader K08. | S316 | Hyprland-InputManager.cpp:1214 | `auto       devname = pKeyboard->m_hlName;` |

## Host join: numlock and the repeat values

- The file line 18 is numlock_by_default = true (H03). The hyprlang spelling true reads as integer 1 (INFERENCE from the round-46 hyprlang pin, hyprlang-config.cpp:259-260, which is not a row of this entry). The getoption record returns int 1 (H06), consistent with that integer path.
- Why the integer matters: getDeviceInt returns the stored value as an integer (E01), so NUMLOCKON is an integer and the lock test K09 compares it with 1. A string comparison of the word true with the digit 1 would differ; AGREE or DIFFER compares integers.
- Two readers, one value at lock time: K03 (InputManager) and K08 (IKeyboard) both call getDeviceInt for numlock_by_default with the same key and fallback; K08 names the device through m_hlName (E15). The lock is applied from the K08 read. The stored m_numlockOn is compared only in the early-return test (E05), so storing it locks nothing.
- Global versus device: getoption returns the global option. INFERENCE: the command form takes no device argument, and the hyprctl source is not pinned here. getoption does not show a device override (INFERENCE, same source), so AGREE says the global value in input.conf equals the live global option; it does not say that any keyboard's effective value equals it.
- Reading the verdict: config is the global value computed from input.conf (default when the key is unset, the word true as 1). AGREE: every live integer equals its config value. DIFFER: a live integer differs (INFERENCE: the file was edited after the last reload; no reload was observed). UNKNOWN: a live record is missing for an option.

## Limits

- Source-level only. No keypress, no client delivery and no keyboard LED state was observed.
- The pins are at the v0.56.2 commit. A live hyprctl version read on 2026-10-28 reports the same commit; that read is not a pinned row.
- The live host read by this entry's seat on 2026-10-28 returned int 40, int 250 and int 1 from getoption, and ~/.config/hypr/input.conf hashes to the committed host-input.conf pin. It is not a pinned row.
- Cross-line propositions: K07, K11, K17, E03, E07 and E11 bind their quote to one line and name a neighbouring line in parentheses only.
- Registry anchors that do not list the cited line (the L1 must widen the row or replace it): S318 lists ConfigValues.cpp 271-279 and 296, so K14 (line 280) is outside it; S052 lists wl_keyboard 2573-2699, so K17 (2741), E11 (2736) and E12 (2740) are outside it; S316 lists 1213-1295, so E06 (1197) is outside it; S319 lists 60-145, so E04 (147) is outside it; S378 (175-178) and S379 (441-448, 603-609) are pending, so E13 (172) and E07 (350) are outside them.
- The 0 to 1 range for numlock_by_default is not shown by this pin (E10, K15). Values other than 0 and 1 are UNKNOWN here.
- Hyprlang parsing of true, on and yes as 1 is cited from the round-46 pin only.
- The sender name sendRepeatInfo to the repeat_info event is INFERENCE.
- K16 quote contains two pipe characters (||). The registration forbids pipes inside cells, but the frozen bytes are kept byte-equal, so that row does not render as a GFM table row; the L1 must decide between the frozen bytes and the cell rule.

## How to verify

Run from the lane root /home/vgpnk/Projects/shokunin/mado-shokunin.

```
sha256sum .ufo/waves/round-55/fetch/Hyprland-InputManager.cpp .ufo/waves/round-55/fetch/Hyprland-IKeyboard.cpp .ufo/waves/round-55/fetch/host-input.conf .ufo/waves/round-55/fetch/host-getoption.json
sed -n '1213,1214p;1220,1224p;1271p;1282,1284p' .ufo/waves/round-55/fetch/Hyprland-InputManager.cpp
sed -n '120p;122p' .ufo/waves/round-55/fetch/Hyprland-IKeyboard.cpp
sed -n '14p;15p;18p' .ufo/waves/round-55/fetch/host-input.conf
cat .ufo/waves/round-55/fetch/host-getoption.json
python3 -I quality/counters/c1-r55-kbd-entry.py --repo . --rev HEAD --work "$(mktemp -d -p /fast/scratch/hyaku/mado-r55)"
python3 -I quality/check-r55-controls.py --claim c1 --repo . --rev HEAD --work "$(mktemp -d -p /fast/scratch/hyaku/mado-r55)"
```

Host, read-only (no keyword, dispatch or reload):

```
hyprctl getoption input:repeat_rate -j
hyprctl getoption input:repeat_delay -j
hyprctl getoption input:numlock_by_default -j
diff ~/.config/hypr/input.conf .ufo/waves/round-55/fetch/host-input.conf && echo IDENTICAL
```
