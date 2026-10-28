source: S316, S317, S318, S319, S052 (existing registry rows), S378, S379, S380 (new rows, opened 2026-10-28, written by the L1 at integration); pins under .ufo/waves/round-55/fetch/ at efb50993780079460b0cbed1363e2166a2de1d9f; host pins fetch/host-input.conf and fetch/host-getoption.json
verified-at: 2026-10-28
recheck: on-release

# Hyprland 0.56.2 keyboard repeat rate, repeat delay and numlock (round 55)

## Scope

Source-level path, held at the pinned tag commit, from the `input:` config keys to the per-keyboard stored values and to the wl_keyboard repeat_info calls. Every K and H row is a frozen single-line quote. Nothing here is a claim about a running compositor, a keypress or a connected client: source-level behaviour is not promoted to a claim about the running host (QUALITY 104). Host rows H01-H06 are a declaration in a file and a read, not a delivery.

## What this entry settles (source-level)

- Declared table entries for the three keys: repeat_rate default 25 with min 0 and max 200 (K13); repeat_delay default 600 with min 0 and max 2000 (K14); numlock_by_default default false (K15). These are declarations; how the config layer enforces the range fields is UNKNOWN (below).
- Per-keyboard lookup: getConfigValueSafeDevice returns the global value when the device value is absent or not set by the user (K16, E12). applyConfigToKeyboard reads repeat rate, delay and numlock through getDeviceInt with that fallback (K01, K02, K03). IKeyboard::setKeymap reads numlock the same way (K08).
- applyConfigToKeyboard stores the rate and the delay as std::max(0, value) (K04, K05) and stores numlock unfloored (K06). The unchanged-config early return at line 1271 (K07) compares the config names with the stored fields.
- IKeyboard::setKeymap enters its NumLock lock block only when NUMLOCKON equals 1; the if has no else (K09).
- updateActiveKeyboardData sends the active keyboard's stored rate and delay to the seat protocol, and only inside its if (m_keyboard) guard (K10, E09). CWLSeatProtocol::updateRepeatInfo calls repeatInfo per keyboard resource when the seat has keyboard capability (E06, E07). CWLKeyboardResource::repeatInfo sends repeat_info only when the owner is present, the resource version is 4 or later, and the rate and delay are not both equal to the last sent values (K11, E10, K12).

## What stays UNKNOWN

- Whether any value reaches a client. No keypress, wl_keyboard event or client bind was observed; the host rows are not delivery receipts.
- How the hyprlang config layer enforces the min and max fields for the three keys (clamp, reject or ignore). The pins show the table declaration (K13, K14) and not the enforcement code.
- Whether a negative configured value can reach the early-return comparison at all. If it can, the stored clamped value and the unclamped config value differ, so the early return would not fire for it. That follows from K04, K05 and K07 and is [INFERENCE]; it is not exercised.
- Which keyboard is m_keyboard at runtime, and therefore which stored rate and delay the seat protocol sends.
- Whether any live client binds wl_keyboard at version 4 or later.
- What the NumLock lock does on the host's own XKB keymap: K09 pins only the set-up line, not the keymap.
- What the "set": true field in host-getoption.json means. The pin records it; no pinned source row defines it.

## Chain (each step cites its rows)

1. Declared keys and defaults: K13, K14, K15 (declarations).
2. Per-device override with global fallback: K16; getDeviceInt call sites K01, K02, K03, K08; E01 is the empty-value branch of getDeviceInt.
3. Apply path: applyConfigToKeyboard is called from setupKeyboard (E08); it clamps rate and delay (K04, K05), stores numlock (K06), and gates on the unchanged test (K07). Stored fields are declared in IKeyboard (K18, E03).
4. Numlock lock in the keymap set-up: IKeyboard::setKeymap (E02) with K08 and K09.
5. Seat push: K10 with E09 (guard), E06 and E07 (seat protocol), K11, E13, E10 and K12 (per resource), E04, E05 and K17 (the 1.26.0 wl_keyboard repeat_info event and its rate-zero and negative-value rules).

## Source rows K01-K18

Cells are generated from `frozen-tables.json` `c1.k` and `c1.h`; propositions bind to their own quote only.

| ID | Proposition | Source | Pin:line | Quote |
|---|---|---|---|---|
| K01 | applyConfigToKeyboard reads the repeat rate through getDeviceInt with device key repeat_rate and global fallback input:repeat_rate. | S316 | Hyprland-InputManager.cpp:1220 | `getDeviceInt(devname, "repeat_rate", "input:repeat_rate");` |
| K02 | applyConfigToKeyboard reads the repeat delay through getDeviceInt with device key repeat_delay and global fallback input:repeat_delay. | S316 | Hyprland-InputManager.cpp:1221 | `getDeviceInt(devname, "repeat_delay", "input:repeat_delay");` |
| K03 | applyConfigToKeyboard reads numlock into NUMLOCKON through getDeviceInt with device key numlock_by_default and global fallback input:numlock_by_default. | S316 | Hyprland-InputManager.cpp:1223 | `getDeviceInt(devname, "numlock_by_default", "input:numlock_by_default");` |
| K04 | The stored repeat rate m_repeatRate is assigned std::max(0, REPEATRATE): floored at zero, with no upper bound applied on this line. | S316 | Hyprland-InputManager.cpp:1282 | `std::max(0, REPEATRATE);` |
| K05 | The stored repeat delay m_repeatDelay is assigned std::max(0, REPEATDELAY): floored at zero, with no upper bound applied on this line. | S316 | Hyprland-InputManager.cpp:1283 | `std::max(0, REPEATDELAY);` |
| K06 | The stored numlock state m_numlockOn is assigned NUMLOCKON directly on this line, with no max(0) floor and no range test. | S316 | Hyprland-InputManager.cpp:1284 | `= NUMLOCKON;` |
| K07 | The unchanged-config early return compares config names REPEATDELAY and REPEATRATE, unclamped in this expression, with stored m_repeatDelay and m_repeatRate. | S316 | Hyprland-InputManager.cpp:1271 | `REPEATDELAY == pKeyboard->m_repeatDelay && REPEATRATE == pKeyboard->m_repeatRate` |
| K08 | IKeyboard::setKeymap reads numlock_by_default into NUMLOCKON through getDeviceInt, keyed by the keyboard m_hlName with global fallback input:numlock_by_default. | S319 | Hyprland-IKeyboard.cpp:120 | `getDeviceInt(m_hlName, "numlock_by_default", "input:numlock_by_default");` |
| K09 | IKeyboard::setKeymap enters its NumLock lock block only when NUMLOCKON equals 1; the if at lines 122-131 has no else, so other values skip the block. | S319 | Hyprland-IKeyboard.cpp:122 | `if (NUMLOCKON == 1) {` |
| K10 | updateActiveKeyboardData passes m_keyboard's stored m_repeatRate and m_repeatDelay to PROTO::seat->updateRepeatInfo, and only inside the if (m_keyboard) guard on line 176 (no else). | S378 | Hyprland-SeatManager.cpp:177 | `PROTO::seat->updateRepeatInfo(m_keyboard->m_repeatRate, m_keyboard->m_repeatDelay);` |
| K11 | One of the three OR-joined conditions on the guard line of CWLKeyboardResource::repeatInfo is that the resource version is below 4; the return that follows is line 443 and is not quoted here. | S379 | Hyprland-protocols-core-Seat.cpp:442 | `m_resource->version() < 4` |
| K13 | The config table declares input:repeat_rate with default 25 and range fields min 0 and max 200. | S318 | Hyprland-ConfigValues.cpp:279 | `"input:repeat_rate", "The repeat rate for held-down keys, in repeats per second.", 25, {.min = 0, .max = 200` |
| K14 | The config table declares input:repeat_delay with default 600 and range fields min 0 and max 2000. | S318 | Hyprland-ConfigValues.cpp:280 | `"input:repeat_delay", "Delay before a held-down key is repeated, in milliseconds.", 600, {.min = 0, .max = 2000}` |
| K15 | The config table declares input:numlock_by_default as a Bool option with default false, described as engaging numlock by default. | S318 | Hyprland-ConfigValues.cpp:277 | `"input:numlock_by_default", "Engage numlock by default.", false` |
| K16 | On this line getConfigValueSafeDevice tests whether the device value pointer is absent or not set by the user, together with a non-empty fallback name; the fallback return that follows is line 1120 and is not quoted here. | S317 | Hyprland-legacy-ConfigManager.cpp:1119 | `!VAL->m_bSetByUser) && !fallback.empty())` |
| K17 | Continuing the sentence that line 2740 opens with "A rate of zero" (E11), the 1.26.0 wl_keyboard repeat_info description says it will disable any repeating regardless of the value of delay; the subject is on line 2740, the quote is line 2741. | S052 | wayland-1.26.0-wayland.xml:2741 | `will disable any repeating (regardless of the value of delay).` |
| K18 | IKeyboard declares the stored repeat-rate member m_repeatRate with the initializer 0, so its declared default value is zero. | S380 | Hyprland-IKeyboard.hpp:121 | `m_repeatRate        = 0;` |

## Host rows H01-H06

Pin and quote cells are generated from `frozen-tables.json` `c1.h`. H01 to H03 are the committed host config file; H04 to H06 are the committed read of `hyprctl getoption -j`. The file declares a value; the read returned a value; neither is delivery to a client.

| ID | Proposition | Source | Pin:line | Quote |
|---|---|---|---|---|
| H01 | The committed host input.conf declares repeat_rate = 40 in its input block; this is a declaration in the file, not a delivered value. | host | host-input.conf:14 | `repeat_rate = 40` |
| H02 | The committed host input.conf declares repeat_delay = 250 in its input block; this is a declaration in the file, not a delivered value. | host | host-input.conf:15 | `repeat_delay = 250` |
| H03 | The committed host input.conf declares numlock_by_default = true in its input block; this is a declaration in the file, not a delivered value. | host | host-input.conf:18 | `numlock_by_default = true` |
| H04 | The committed live hyprctl getoption read returned int 40 for input:repeat_rate; this read is not a delivery to any client. | host | host-getoption.json:1 | `"option": "input:repeat_rate", "int": 40` |
| H05 | The committed live hyprctl getoption read returned int 250 for input:repeat_delay; this read is not a delivery to any client. | host | host-getoption.json:2 | `"option": "input:repeat_delay", "int": 250` |
| H06 | The committed live hyprctl getoption read returned int 1 for input:numlock_by_default; this read is not a delivery to any client. | host | host-getoption.json:3 | `"option": "input:numlock_by_default", "int": 1` |

## Extra rows (not counted by the counter)

These support prose in Scope, Chain and Limits. Each quote is an exact substring of the named pin line (checked by the generator and by verify.py).

| ID | Proposition | Source | Pin:line | Quote |
|---|---|---|---|---|
| E01 | getDeviceInt returns the empty brace value (0 for an int) when its lookup yields no value pointer (the if at line 1133); whether any of the three keys reaches it is not shown by these pins. | S317 | Hyprland-legacy-ConfigManager.cpp:1134 | `return {};` |
| E02 | IKeyboard::setKeymap begins on this line, so the numlock read in K08 and the lock block in K09 sit inside that function. | S319 | Hyprland-IKeyboard.cpp:60 | `void IKeyboard::setKeymap(const SStringRuleNames& rules) {` |
| E03 | IKeyboard declares m_numlockOn with initializer -1 on this line, so the declared numlock default is -1 and not 0 or 1. | S380 | Hyprland-IKeyboard.hpp:123 | `= -1;` |
| E04 | The wl_keyboard repeat_info event is declared with since 4 on this line of the 1.26.0 protocol. | S052 | wayland-1.26.0-wayland.xml:2732 | `<event name="repeat_info" since="4">` |
| E11 | The repeat_info description opens the sentence that K17 finishes with the words `A rate of zero` at the end of this line. | S052 | wayland-1.26.0-wayland.xml:2740 | `A rate of zero` |
| E12 | When the K16 condition holds, getConfigValueSafeDevice returns the global option looked up by the fallback name. | S317 | Hyprland-legacy-ConfigManager.cpp:1120 | `return m_config->getConfigValuePtr(fallback.c_str());` |
| E13 | The guard line of repeatInfo is followed by a return on this line, so a true guard ends the call before the send. | S379 | Hyprland-protocols-core-Seat.cpp:443 | `return;` |
| E05 | The repeat_info description states, on this line, that negative values for rate or delay are illegal. | S052 | wayland-1.26.0-wayland.xml:2740 | `Negative values for either rate or delay are illegal.` |
| E06 | CWLSeatProtocol::updateRepeatInfo tests whether m_currentCaps includes HID_INPUT_CAPABILITY_KEYBOARD on this line before its loop. | S379 | Hyprland-protocols-core-Seat.cpp:604 | `if (!(m_currentCaps & eHIDCapabilityType::HID_INPUT_CAPABILITY_KEYBOARD))` |
| E07 | CWLSeatProtocol::updateRepeatInfo calls repeatInfo with rate and delayMs for each keyboard resource in the m_keyboards loop on this line. | S379 | Hyprland-protocols-core-Seat.cpp:608 | `k->repeatInfo(rate, delayMs);` |
| E08 | setupKeyboard passes its keeb argument to applyConfigToKeyboard on this line, one of the callers of the function in K01 to K07. | S316 | Hyprland-InputManager.cpp:1195 | `applyConfigToKeyboard(keeb);` |
| E09 | updateActiveKeyboardData tests m_keyboard for a non-null value on this line before the repeat update that K10 cites. | S378 | Hyprland-SeatManager.cpp:176 | `if (m_keyboard)` |
| E10 | repeatInfo records the delay argument in m_lastDelayMs on this line, before the sendRepeatInfo call that K12 cites. | S379 | Hyprland-protocols-core-Seat.cpp:445 | `m_lastDelayMs = delayMs;` |

## Joining the declaration to the live read (the round-55 tool)

`tools/mado-kbdopts.py` (round 55, claim C2) models the config half of this chain for config text a caller supplies — device
value when the block set it, else the global option, else the table default (K16, K13-K15), integers as the hyprlang parser
reads them — and joins the result to the JSON that `hyprctl getoption <name> -j` prints. Receipt, read-only, 2026-10-28:
`.ufo/waves/round-55/receipts/live-kbdopts.txt`. For `~/.config/hypr/input.conf` (byte-equal to the committed pin, `cmp`) and
two keyboard names from `hyprctl devices -j` it prints `repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0`
for both and `AGREE` three times against the live read (the committed H04-H06 lines).

How to read that output without overclaiming:

- The host config holds no `device` block (`grep -rnE 'device\[|device \{|device\{' ~/.config/hypr` → no match, receipt
  `.ufo/waves/round-55/w1/R55ScoutHost/receipts-cmp-grep.txt`), so by K16 every keyboard resolves to the global value; the two
  per-keyboard lines are what the source implies for those names, not an observed per-keyboard value.
- `getoption` returns an option by name. [INFERENCE] It takes no device argument, so `AGREE` says the running compositor's
  global option equals the declared one; it cannot show a device override (the reply forms are held in
  `hyprctl-getoption-native-forms-r40.md`, not re-claimed here).
- The `numLock` field of `hyprctl devices -j` is lock state, not this option (`hyprland-input-devices-r46.md` step 5); the
  tool never compares them.
- `hyprland-input-devices-r46.md:70` lists these three options as applied per device and printed by no dump; K01-K03 and K08
  now show the per-device read at source level and that sentence stays as history. Nothing here makes the dump print them.
- The tool's `unsupported` count is its honesty valve: a value outside the modelled token set (`$` variables, `device[...]`
  bracket forms, hex or signed numbers, out-of-range values, `##`) is counted, not guessed. The numlock 0..1 range is the
  lane's modelling rule, not a source range (K15 declares a Bool without min or max).

## Adjacent ground (reported, not absorbed)

- The XKB compile of `kb_layout`/`kb_options` is `hyprland-input-devices-r46.md` and `xkb-keymap-compile-r48.md`; K09 only
  pins that numlock is set on the keymap state after that compile.
- What a client does with `repeat_info`, and any input-method (fcitx5) interaction, is outside the province; a sibling sweep
  (`.ufo/waves/round-55/w1/R55ScoutAdjacency.md`) found no sibling lane holding `repeat_rate`, `repeat_delay`,
  `numlock_by_default` or `repeat_info`.
- The host readback 40 / 250 / 1 was already held (`hyprctl-verification-layer.md:132-134`, `config-health-report-r3.md:546-548`);
  H01-H06 add the source chain around it, not a new host fact.

## Limits

- Source-level only, at the pinned tag commit efb50993780079460b0cbed1363e2166a2de1d9f. No row is a claim about the running compositor; the host rows are a declaration and a read.
- QUALITY 104 checks: the "only" in K09 was checked against the if block at IKeyboard.cpp:122-131 (no else branch). The "only" in K10 was checked against the single-statement if at SeatManager.cpp:176-177. "Floored at zero" in K04 and K05 is the std::max(0, x) expression on that line; the line sets no upper bound.
- K07 is stated as what the line shows: it names the config values and the stored fields and does not state a runtime outcome. The consequence for negative values is [INFERENCE] (see UNKNOWN).
- getDeviceInt's empty-value branch (E01) is shown by the source; whether the three keys ever reach it is UNKNOWN.
- A quote proves that the cited text is at the cited line; it does not prove that a proposition sentence is entailed by it. Entailment is the independent sentence-to-pin audit, not this entry's counter.
- The wl_keyboard protocol text (K17, E04, E05) is the 1.26.0 specification; it is cited for the event contract and not for Hyprland's implementation of it, which is K11 and K12.
- Registry anchor gaps (registry rows are append-only, CORPUS rule 2, so they are recorded here rather than widened): S318 records ConfigValues.cpp:271-279, which does not reach K14 at line 280; S052 records wl_keyboard :2573-2699, which does not reach K17 at line 2741 or E04 and E05 at lines 2732 and 2740 (the wl_keyboard interface runs 2573-2752 in the pin); S316 records applyConfigToKeyboard at 1213-1295, which does not reach E08 at line 1195. The counter checks only the S-id URL suffix and status, so it would not catch these.

## How to verify

Run from the repository root. Each command reads committed files or a read-only host query.

```
sha256sum .ufo/waves/round-55/fetch/*
python3 -I .ufo/waves/round-55/freeze-verify.py
sed -n '1220,1223p;1271p;1282,1284p' .ufo/waves/round-55/fetch/Hyprland-InputManager.cpp
sed -n '120,122p' .ufo/waves/round-55/fetch/Hyprland-IKeyboard.cpp
sed -n '176,177p' .ufo/waves/round-55/fetch/Hyprland-SeatManager.cpp
cat .ufo/waves/round-55/fetch/host-input.conf | sed -n '14,15p;18p'
cat .ufo/waves/round-55/fetch/host-getoption.json
hyprctl getoption input:repeat_rate -j
hyprctl getoption input:repeat_delay -j
hyprctl getoption input:numlock_by_default -j
```

The first command must match `c1.pin_sha256` in `frozen-tables.json`. The `freeze-verify.py` line must end `OK`. The three `hyprctl getoption` commands are read-only; compare them with H04 to H06 by eye. A mismatch is a host fact, not an entry defect.


<!-- note --> <!--
| K12 | After the early return and the update of m_lastRate and m_lastDelayMs, repeatInfo calls sendRepeatInfo with its rate and delayMs arguments. | S379 | Hyprland-protocols-core-Seat.cpp:447 | `m_resource->sendRepeatInfo(rate, delayMs);` |
-->