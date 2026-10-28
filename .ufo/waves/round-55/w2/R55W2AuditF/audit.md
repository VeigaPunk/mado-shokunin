# R55W2AuditF: sentence-to-pin audit (QUALITY 104)

Scope: rows H01-H06 of `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`, and the two prose sections
`Joining the declaration to the live read` (rows P1-P15) and `Adjacent ground` (rows A1-A4). Each row: the proposition
cell, the cited pin line, its neighbouring lines, and a label.

Labels: SUPPORTED = the quote itself entails the proposition. HELD = stated as held, unknown or [INFERENCE] with the
boundary named. OVERREACH = stronger than the quote (always/only/never without the branch set, a runtime claim, a
neighbour line's effect). UNSUPPORTED = no pin or observation behind it.

Pin paths: `P` = `.ufo/waves/round-55/fetch/`. "Upstream" = `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/` (checked byte-equal, see section 4).
Receipts: `.ufo/waves/round-55/w2/R55W2AuditF/receipts/`.

## 1. Host rows H01-H06

| Row | Proposition (cell, abridged) | Pin:line | Neighbour lines read | Label | Evidence and note |
|---|---|---|---|---|---|
| H01 | input.conf declares `repeat_rate = 40` in its input block; a declaration, not a delivered value | `P/host-input.conf:14` `  repeat_rate = 40` | :3 `input {` opens the block, :42 closes it; :13 comment, :15 repeat_delay | SUPPORTED | Line 14 sits inside the `input {` block at :3-:42. Byte-equal to `~/.config/hypr/input.conf` (`cmp`, rc 0, this run). "Not a delivered value" is a boundary statement, HELD by construction. |
| H02 | input.conf declares `repeat_delay = 250` in its input block | `P/host-input.conf:15` `  repeat_delay = 250` | :14 repeat_rate, :16 blank | SUPPORTED | Same block and byte-equality as H01. |
| H03 | input.conf declares `numlock_by_default = true` in its input block | `P/host-input.conf:18` `  numlock_by_default = true` | :17 `# Start with numlock on by default` (a comment, states intent, not effect), :19 blank | SUPPORTED | The comment does not add an effect claim. The row claims only the declaration. |
| H04 | the committed live `hyprctl getoption` read returned `int 40` for `input:repeat_rate`; not a delivery to any client | `P/host-getoption.json:1` `"option": "input:repeat_rate", "int": 40` | :2, :3 (other two options, same shape, `"set": true`) | HELD | "returned int 40" is SUPPORTED. The word "live" is not in the pin bytes; its provenance is `.ufo/waves/round-55/receipts/live-kbdopts.txt:1` (cmp against a live capture). This run: `hyprctl getoption input:repeat_rate -j` printed the identical line (cmp of the three concatenated reads, rc 0). "Not a delivery to any client" is a boundary the pin cannot show either way. |
| H05 | the committed live read returned `int 250` for `input:repeat_delay`; not a delivery | `P/host-getoption.json:2` `"option": "input:repeat_delay", "int": 250` | :1, :3 | HELD | Same as H04: value SUPPORTED, "live" provenance is in the receipt not the pin, delivery boundary HELD. Current run identical (cmp rc 0). |
| H06 | the committed live read returned `int 1` for `input:numlock_by_default`; not a delivery | `P/host-getoption.json:3` `"option": "input:numlock_by_default", "int": 1` | :1, :2 | HELD | Same as H04. The pin records `int 1` for a Bool; the row does not claim what 1 means for a Bool, and does not need to. Current run identical (cmp rc 0). |

Frozen-table check: `frozen-tables.json` and `frozen-tables-v2.json` `c1.h` are identical (`v1==v2: True`), and each of the six quotes is a substring of its named pin line (checked by script, all six `substring-ok`).

## 2. Prose section: `Joining the declaration to the live read`

| Row | Proposition (sentence or clause) | Pin:line | Neighbour lines read | Label | Evidence and note |
|---|---|---|---|---|---|
| P1a | `tools/mado-kbdopts.py` (C2) models the config half of this chain for config text a caller supplies | `tools/mado-kbdopts.py` docstring, lines 1-60 | `read_regular` (:85) opens with O_RDONLY, `parse_config` (:153) | SUPPORTED | File exists. The tool models caller-supplied config text and was run here (receipt `tool-run.txt`). |
| P1b | device value when the block set it, else the global option, else the table default (K16, K13-K15) | `P/Hyprland-legacy-ConfigManager.cpp:1119` `if ((!VAL \|\| !VAL->m_bSetByUser) && !fallback.empty())`; defaults `P/Hyprland-ConfigValues.cpp:277` (`numlock false`), `:279` (`repeat_rate 25`), `:280` (`repeat_delay 600`) | :1120 `return m_config->getConfigValuePtr(fallback.c_str());`, :1122 `return VAL;`; :278, :281 | SUPPORTED | The precedence is what K16 and the three default declarations show. The tool's `DEFAULTS` are 25/600/0, matching. |
| P1c | integers as the hyprlang parser reads them | none in this entry's rows. The tool docstring cites `hyprlang-config.cpp:259-262` (round-46 pin); the pin is `.ufo/waves/round-46/fetch/hyprlang-config.cpp` | pin :259-262 (`starts_with("true"/"on"/"yes")` → 1, `("false"/"off"/"no")` → 0); :265-271 (`isNumber` then `std::stoll`) | HELD | The prefix rule is pinned at round-46 :259-262 and is byte-equal to upstream hyprlang v0.6.8 `src/config.cpp` (S324). The prose cites only K16 and K13-K15, so the clause has no cell in this entry. Correction: "integers and booleans as hyprlang 0.6.8 `configStringToInt` reads them (round-46 `hyprlang-config.cpp:259-262`; the tool models the decimal branch only)." |
| P1d | joins the result to the JSON that `hyprctl getoption <name> -j` prints | tool `parse_getoption` (:217) | none | SUPPORTED | The tool joins by the `option` field of each JSON line; the three lines come from the three calls. |
| P2 | Receipt, read-only, 2026-10-28: `.ufo/waves/round-55/receipts/live-kbdopts.txt` | the receipt file exists | receipt :1-:11 | SUPPORTED | The file exists at that path. Note for the wave: the brief named `corpus/knowledge/receipts/...`; the real path is `.ufo/waves/round-55/receipts/`, and the entry cites the right one. The tool writes nothing (docstring, and no write call in the code). |
| P3a | for `~/.config/hypr/input.conf` it is byte-equal to the committed pin (`cmp`) | `P/host-input.conf` | n/a | SUPPORTED | `cmp ~/.config/hypr/input.conf P/host-input.conf`: identical, rc 0 (this run). |
| P3b | two keyboard names from `hyprctl devices -j` | `receipts/devices.json` | n/a | SUPPORTED | `hp--inc-hyperx-alloy-origins-core` and `hl-virtual-keyboard-fcitx5` both appear in this run's `hyprctl devices -j` (keyboards list). |
| P3c | it prints `repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0` for both | tool output | n/a | SUPPORTED | Run here: `MADO_KBDOPT: keyboard=hp--inc-hyperx-alloy-origins-core repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0` and the same for `hl-virtual-keyboard-fcitx5` (`receipts/tool-run.txt`). |
| P3d | `AGREE` three times against the live read | tool output `MADO_KBDOPT_LIVE` lines | n/a | SUPPORTED | Run here: three `verdict=AGREE` lines and `DONE keyboards=2 unsupported=0 live=AGREE`. The "live read" is this run's `hyprctl getoption` output, byte-identical to the committed `host-getoption.json`. |
| P4 | the host config holds no `device` block (`grep -rnE 'device\[\|device \{\|device\{' ~/.config/hypr` → no match) | host file | n/a | SUPPORTED | Pattern matched nothing. Run here inside a broader grep over `~/.config/hypr` (see report, disclosure). The L1 receipt `w1/R55ScoutHost/receipts-cmp-grep.txt` shows rc=1 for the exact command. Limit: file state only. See P5. |
| P5 | "so by K16 every keyboard resolves to the global value" | K16 `P/Hyprland-legacy-ConfigManager.cpp:1119` | :1120 fallback | OVERREACH | K16 gives the resolution rule for a config where no device value is set. It does not show the running compositor's state. A device value can reach the running daemon without a file block, e.g. through a runtime `hyprctl keyword` (named as a runtime path in `hyprland-input-devices-r46.md:62`), and nothing in this check reads it. The entry's own text says `getoption` cannot show a device override. Correction: "The config file holds no device block, so under K16 each keyboard resolves to the global value as the file declares it; a device value set at runtime is not excluded by this read." |
| P6 | `getoption` returns an option by name. [INFERENCE] It takes no device argument, so AGREE says the running global equals the declared one; it cannot show a device override | the r40 note `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` (cited, not re-verified here) | n/a | HELD | Tagged [INFERENCE] with the boundary stated. Not re-verified: `hyprctl getoption -h` is outside the allowed host reads. |
| P7 | AGREE says the running compositor's global option equals the declared one | tool `report` (:239-263) | n/a | HELD | The tool's `config` value is the file value only when the line parsed (`unsupported=0`). When a line is unsupported the value is the fallback (see P14), so for that key AGREE compares against the fallback, not the declared value. The sentence holds for `unsupported=0` runs only. |
| P8 | the numLock field of `hyprctl devices -j` is lock state, not this option (`hyprland-input-devices-r46.md` step 5); the tool never compares them | `corpus/knowledge/hyprland-input-devices-r46.md:34` (step 5: "`numLock` (locked-modifier state, not the `numlock_by_default` option)") | :33, :35 | SUPPORTED | Step 5 says it. The tool reads only `--config` and `--getoption` (`parse_args`, :108-:132), never `devices`. |
| P9 | `hyprland-input-devices-r46.md:70` lists these three options as applied per device and printed by no dump | `corpus/knowledge/hyprland-input-devices-r46.md:70` "applied per device too but the dump prints none of them" | :69, :71 | OVERREACH | Line 70 says "the dump" (the `hyprctl devices -j` dump, step 5). This entry's own H04-H06 show `hyprctl getoption -j` printing all three values. Correction: "printed by no `hyprctl devices -j` dump". |
| P10 | K01-K03 and K08 now show the per-device read at source level; that sentence stays as history | `P/Hyprland-InputManager.cpp:1220-1223`; `P/Hyprland-IKeyboard.cpp:120` | :1219, :1224; :119, :121 | SUPPORTED | Both call sites are `getDeviceInt(<device>, <key>, "input:<key>")`. Byte-equal to upstream (section 4). |
| P11 | nothing here makes the dump print them | tool source | n/a | SUPPORTED | The tool does not read `devices`, and the r46 line stays unchanged. |
| P12 | the tool's `unsupported` count is its honesty valve: a value outside the modelled token set (`$`, `device[...]`, hex or signed numbers, out-of-range, `##`) is counted, not guessed | tool docstring "Declared limit" and "Ranges" (lines 38-46, 60); frozen `claims-frozen.md` C2 "never guessed" | n/a | OVERREACH (reproduced) | The count is produced, but the line is dropped and the output falls back to the next value (device, then global, then default), and the verdict is still printed. "Not guessed" is contradicted by the output. Evidence: section 6, attacks A, B, D. Correction: "A value outside the modelled token set is counted in `unsupported` and its line is dropped; the printed value is then the device, global or default value (e.g. 25/600/0 when nothing else is set) and AGREE/DIFFER can still be printed for it. A non-zero `unsupported` means the verdict for that key is not evidence about the config text." |
| P13 | the numlock 0..1 range is the lane's modelling rule, not a source range (K15 declares a Bool without min or max) | tool docstring lines 9-12 ("the lane's modelling rule"); `P/Hyprland-ConfigValues.cpp:277` | :276 `kb_file`, :278 `resolve_binds_by_sym` | SUPPORTED | Line 277 has `{.refresh = ...}` and no `.min`/`.max`. The tool docstring states the rule. |

## 3. Prose section: `Adjacent ground`

| Row | Proposition | Pin:line | Neighbour lines read | Label | Evidence and note |
|---|---|---|---|---|---|
| A1 | the XKB compile of kb_layout/kb_options is `hyprland-input-devices-r46.md` and `xkb-keymap-compile-r48.md` | pointer to two knowledge files | n/a | HELD | Both files exist. Their content was not audited here (pointer only). |
| A2 | "K09 only pins that numlock is set on the keymap state after that compile." | K09 `P/Hyprland-IKeyboard.cpp:122` `if (NUMLOCKON == 1) {` | :115 compile, :118 `updateXKBTranslationState`, :120 read, :123-:131 block body, :124 `xkb_map_mod_get_index`, :126 `if (IDX != XKB_MOD_INVALID)`, :127 `|=` into `m_modifiersState.locked`, :130 `updateModifiers(...)`; upstream :379 `xkb_state_update_mask(m_xkbState, ...)` | OVERREACH | K09 pins the gate only; "numlock is set" is the body (:123-:130), which the row does not cite. The set is conditional on the NumLock modifier index being valid (:126). "keymap state" is the xkb state object written by `updateModifiers` (:379). The "after that compile" part is correct (:115 then :118 then :122). Correction: "K09 pins only the gate `if (NUMLOCKON == 1)` (IKeyboard.cpp:122). Its body (:123-130, not pinned by K09) ORs the NumLock bit into `m_modifiersState.locked` only when `xkb_map_mod_get_index` returns a valid index (:124-127), then calls `updateModifiers` (:130), which applies it to the xkb state (:379). Whether the host keymap has a NumLock modifier is not pinned." |
| A3 | a sibling sweep (`w1/R55ScoutAdjacency.md`) found no sibling lane holding `repeat_rate`, `repeat_delay`, `numlock_by_default` or `repeat_info` | `.ufo/waves/round-55/w1/R55ScoutAdjacency.md` lines 16-20 (`TERM=... files=0`) | :34 "No sibling holds ..." | SUPPORTED (as to the cited report) | The report's counts are 0 for all four terms. I did not re-run the sibling sweep. The mado repo itself was excluded by the sweep, and this sentence does not claim otherwise. |
| A4 | the host readback 40 / 250 / 1 was already held (`hyprctl-verification-layer.md:132-134`, `config-health-report-r3.md:546-548`); H01-H06 add the source chain, not a new host fact | `corpus/knowledge/hyprctl-verification-layer.md:132-134`, `corpus/knowledge/config-health-report-r3.md:546-548` | :131, :135; :545, :549 | SUPPORTED | Lines 132-134 read `input:repeat_rate \| L-IN:14 = 40 \| int: 40`, `repeat_delay \| L-IN:15 = 250 \| int: 250`, `numlock_by_default \| L-IN:18 = true \| int: 1`. Lines 546-548 read the same three values as `set`/`agreement`. The "not a new host fact" clause is HELD by the same reasoning as H04-H06. |

## 4. Upstream re-open (independent of the committed pins)

Each upstream file was fetched with `curl -sS -f` at `efb50993780079460b0cbed1363e2166a2de1d9f`, and compared with the committed pin bytes by `cmp` (all BYTE-EQUAL). Sha256 values match `P/SHA256SUMS.txt`.

| Upstream path (under `src/`) | Pin | Result |
|---|---|---|
| `managers/input/InputManager.cpp` | `P/Hyprland-InputManager.cpp` (feedf32e…) | BYTE-EQUAL; lines 1220-1223, 1271, 1282-1284 read upstream, same text as pin |
| `devices/IKeyboard.cpp` | `P/Hyprland-IKeyboard.cpp` (8a800efe…) | BYTE-EQUAL; lines 120-122, 130, 379 read upstream |
| `managers/SeatManager.cpp` | `P/Hyprland-SeatManager.cpp` (bd748553…) | BYTE-EQUAL; lines 176-177 read upstream |
| `config/values/ConfigValues.cpp` | `P/Hyprland-ConfigValues.cpp` (a76f0507…) | BYTE-EQUAL |
| `config/legacy/ConfigManager.cpp` | `P/Hyprland-legacy-ConfigManager.cpp` (9db68cf4…) | BYTE-EQUAL |
| `protocols/core/Seat.cpp` | `P/Hyprland-protocols-core-Seat.cpp` (cc23bb8b…) | BYTE-EQUAL |
| `devices/IKeyboard.hpp` | `P/Hyprland-IKeyboard.hpp` (82e0bc9e…) | BYTE-EQUAL |
| wayland 1.26.0 `protocol/wayland.xml` (gitlab raw) | `P/wayland-1.26.0-wayland.xml` (cc860987…) | BYTE-EQUAL; lines 2740-2741 read upstream |
| hyprlang v0.6.8 `src/config.cpp` (S324) | `.ufo/waves/round-46/fetch/hyprlang-config.cpp` (fa1b6898…) | BYTE-EQUAL |

The H rows have no upstream pin (they are host files). The re-open above covers the pins that the prose sections cite (P1b, P9-P10, A2) and the round-46 hyprlang pin cited by P1c.

## 5. Corrections, in one list

1. P5 (runtime overreach): "so by K16 every keyboard resolves to the global value" → "the config file holds no device block, so under K16 each keyboard resolves to the global value as the file declares it; a device value set at runtime is not excluded by this read."
2. P9 (scope of "dump"): "printed by no dump" → "printed by no `hyprctl devices -j` dump".
3. P12 (honesty valve, reproduced): see section 6 attacks A, B, D; correction text in the table.
4. A2 (K09 attribution and the unconditional set): see the table text.
5. P1c (no cell): add the round-46 hyprlang pin `hyprlang-config.cpp:259-262` next to "integers as the hyprlang parser reads them".

## 6. Reproduced attack on the honesty-valve claim (P12)

Inputs (`receipts/oor.conf`, `receipts/oor1.conf`, `receipts/nl2.conf`, `receipts/ok200.conf`, live reads in `receipts/*-live.txt`). Tool unchanged: `python3 -I tools/mado-kbdopts.py ...`, run from scratch. Full output in `receipts/attack-runs.txt`.

Attack A, the file `oor.conf` holds `repeat_rate = 201`, `repeat_delay = 2001`, `numlock_by_default = 2`; live reads are the defaults 25/600/0:

```
MADO_KBDOPT: keyboard=kbX repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=3
MADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=25 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:repeat_delay config=600 live=600 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:numlock_by_default config=0 live=0 verdict=AGREE
MADO_KBDOPT: DONE keyboards=1 unsupported=3 live=AGREE
```

Attack B, `oor1.conf` holds `repeat_rate = 201`; live `repeat_rate` is 25: the printed config value is 25 and the verdict is AGREE with `unsupported=1`.

Attack D, `nl2.conf` holds `numlock_by_default = 2`; live numlock is 1: the printed config value is 0, `unsupported=1`, and the verdict is DIFFER.

Control, `ok200.conf` holds `repeat_rate = 200` (in range), live 25: `repeat_rate=200 ... unsupported=0` and `verdict=DIFFER`. The in-range path does not guess.

These inputs are in the frozen C2 input grammar: the frozen declared limit names out-of-range values as the `unsupported` case, so this is not a syntactic rejection (QUALITY 105). The instrument's behaviour, not its parser, is what is shown wrong. The knowledge note itself says the range enforcement site is UNKNOWN (its UNKNOWN list), so the fallback to the default is a guess about hyprlang's behaviour that the pins do not show.
