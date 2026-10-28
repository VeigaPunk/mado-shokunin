# Round 55 w1 — R55ConnClaims cross-claim table (C1 K/H locators vs C2 config-model clauses)

Scope: frozen text only (`registration.md` §C1, §C2; `frozen-tables.json` c1.k / c1.h), pins in `.ufo/waves/round-55/fetch/`,
and the three knowledge files. At lane HEAD `dbc2eefe` neither `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`
nor `tools/mado-kbdopts.py` exists, so C1 is compared by its frozen quotes/locators and C2 by its frozen spec text
(registration §C2), not by written K-row propositions or tool output. All 24 K/H quotes are single-line substrings of their
pin line (`k-quote-check.txt`, bad 0).

Pin paths are relative to `.ufo/waves/round-55/fetch/`. Knowledge paths are relative to the lane root.

| # | fact | C1 locator | C2 clause | agree? |
|---|---|---|---|---|
| F1 | `input:repeat_rate` built-in default is 25 | K13 `Hyprland-ConfigValues.cpp:279` (`…, 25, {.min = 0, .max = 200`) | §C2 "built-in defaults 25 / 600 / 0 — ConfigValues.cpp:277-280" | AGREE |
| F2 | `input:repeat_delay` built-in default is 600 | K14 `Hyprland-ConfigValues.cpp:280` (`…, 600, {.min = 0, .max = 2000}`) | same clause | AGREE |
| F3 | `input:numlock_by_default` built-in default is `false`, i.e. 0 | K15 `Hyprland-ConfigValues.cpp:277` (`…, false`) | same clause ("0") | AGREE (the `false`→0 step is inferred; C2 does not write it) |
| F4 | `repeat_rate` range 0..200 | K13 `Hyprland-ConfigValues.cpp:279` `{.min = 0, .max = 200` | §C2 "`repeat_rate` 0..200" | AGREE |
| F5 | `repeat_delay` range 0..2000 | K14 `Hyprland-ConfigValues.cpp:280` `{.min = 0, .max = 2000}` | §C2 "`repeat_delay` 0..2000" | AGREE |
| F6 | `numlock_by_default` range 0..1, sourced to ConfigValues.cpp:277-280 | K15 `Hyprland-ConfigValues.cpp:277` is `MS<Bool>(…, false, {.refresh = …})`: **no min/max on the line**; no K row carries a numlock range | §C2 "`numlock_by_default` 0..1" under "Range (ConfigValues.cpp:277-280 pin …)" | **DISAGREE** — the cited pin does not state the range; the 0..1 bound is unsourced (see D1) |
| F7 | out-of-range values are dropped (`unsupported +1`, line ignored) | none; the only apply-time bound is K04 `Hyprland-InputManager.cpp:1282` / K05 :1283 `std::max(0, …)`, a LOWER bound only | §C2 "an out-of-range value → unsupported +1, line ignored" | NOT COVERED — no pin shows hyprlang rejecting or clamping a value above `.max`; C1 must not say "clamped to 200/2000" (D6) |
| F8 | negative rate/delay reaches the apply path and is clamped to 0 | K04 :1282, K05 :1283 `std::max(0, REPEATRATE/REPEATDELAY)`; wayland K17 `wayland.xml:2740` "Negative values … are illegal" (not quoted in a K row) | §C2 sign tokens → unsupported, "never guessed"; clamp "a no-op on the modelled range" | AGREE (scoped). Whether hyprlang's `isNumber(VALUE,false)` (round-46 `hyprlang-config.cpp:265`, definition not pinned) accepts `-` is UNVERIFIED (D10) |
| F9 | a device value wins only when the user set it, else the global option | K01–K03 `Hyprland-InputManager.cpp:1220,1221,1223` (`getDeviceInt(devname, "…", "input:…")`); K08 `Hyprland-IKeyboard.cpp:120`; K16 `Hyprland-legacy-ConfigManager.cpp:1119` `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` | §C2 "a device key sets the CURRENT device's value … `getDeviceInt` uses the device value when the user set it, else the global option — legacy ConfigManager.cpp:1115-1123" | AGREE on the rule. Citation gap: the function C2 names, `getDeviceInt`, is at legacy `:1131-1137`; `:1115-1123` is only its helper `getConfigValueSafeDevice` (D5) |
| F10 | numlock is read per keyboard (device name, global fallback) and gates the keymap numlock bit | K08 `Hyprland-IKeyboard.cpp:120` (`m_hlName`), K09 :122 `if (NUMLOCKON == 1) {`; K06 `Hyprland-InputManager.cpp:1284` `= NUMLOCKON;` | §C2 emits `numlock=<0|1>` per keyboard; says nothing about the keymap | AGREE (C2 silent on lock application, no conflict) |
| F11 | applied rate/delay are clamped at 0 | K04 :1282, K05 :1283 | §C2 "`applyConfigToKeyboard` clamps the stored rate and delay with `std::max(0, …)` — InputManager.cpp:1282-1283, a no-op on the modelled range" | AGREE |
| F12 | keyboard member defaults before any apply: `m_repeatRate = 0`, `m_numlockOn = -1` | K18 `Hyprland-IKeyboard.hpp:121` `m_repeatRate        = 0;` (`:123` `m_numlockOn = -1` is pinned but not quoted in a K row) | §C2 "built-in defaults 25 / 600 / 0" | AGREE at different stages, but the word "default" collides (25 config default vs 0 member default). The C1 prose must qualify which one (D7) |
| F13 | `true`/`on`/`yes` prefix → 1 | H03 `host-input.conf:18` `numlock_by_default = true`; H06 `host-getoption.json:3` `"int": 1`; round-46 `hyprlang-config.cpp:259-260` | §C2 "starts with `true`, `on` or `yes` → 1 (checked first)" cites hyprlang-config.cpp:259-262 | AGREE (the pin lines 259-262 match the clause; checked) |
| F14 | host values: repeat_rate 40, repeat_delay 250, numlock on | H01 `host-input.conf:14`, H02 :15, H03 :18; H04–H06 `host-getoption.json:1-3` | §C2 F02 consumes `fetch/host-input.conf` and `fetch/host-getoption.json` | AGREE. Re-read 2026-10-28: `~/.config/hypr/input.conf` sha256 `3769c92a…` equals the pin; `hyprctl getoption` → 40 / 250 / 1 |
| F15 | `hyprctl getoption input:*` values are the GLOBAL option, not a per-keyboard value | H04–H06 are global `input:` options; no K row gives a per-keyboard getoption | §C2 `MADO_KBDOPT_LIVE … config=<global effective value>`; `DONE … live=AGREE` | AGREE with C2's own text. Risk: `live=AGREE` certifies the global only; the per-keyboard live value stays UNKNOWN (D11) |
| F16 | device block matches the keyboard by exact normalised name | K01/K08 use `devname` / `m_hlName`; r46 doc `hyprland-input-devices-r46.md:36` (step 7) exact-key compare | §C2 "device value if set for NAME" (NAME verbatim, no normalisation) | AGREE. A caller must pass the normalised name; C2 does not normalise (r46 step 7 is the source) |
| F17 | a `device` key before any `name` line | not a K row; r46 `hyprland-input-devices-r46.md:48` (OBS S324) cites hyprlang-config.cpp:435, `result.setError("special category's first value must be the key…")` (pin verified: round-46 `:435`) | §C2 "a `device`-block key line seen before any `name` line … → unsupported +1, ignored" | PARTIAL. Hyprland raises a parse error; C2 counts it and ignores it. This is a model convention and must not be presented as Hyprland's behaviour (D8) |
| F18 | `device[X]` bracket forms reach the per-device store | not a K row; r46 `hyprland-input-devices-r46.md:31` (step 2: three spellings reach the same store) | §C2 "a KEY starting with `device[` … adds one to `unsupported` and is not modelled" | AGREE-scoped: C2 declares them unmodelled, so a device override written that way is invisible to the tool |
| F19 | rate 0 disables repeating | K17 `wayland-1.26.0-wayland.xml:2741` ("A rate of zero will disable any repeating") | §C2 allows `repeat_rate` 0; assigns it no meaning | AGREE (silent). Registry locator gap: S052 cites wl_keyboard `:2573-2699`, but the event sits at :2741 (interface runs to :2753) (D3) |
| F20 | `numLock` field of `hyprctl devices -j` is lock state, not the option | not a K row; r46 `hyprland-input-devices-r46.md:34` (step 5) says exactly this | §C2 numlock comes from config text only | AGREE. The entry must not map the dump's `numLock` to `numlock_by_default` |
| F21 | keyboard-level repeat/numlock values are UNK for the dump join | not a K row; r46 `hyprland-input-devices-r46.md:70` "they are UNK for this join" | §C2 live verdict is global only | AGREE. Per-keyboard live stays UNK in the entry too |
| F22 | host repeat/numlock rows are "agreement" in the live layer | H01–H03; `hyprctl-verification-layer.md:132-134` (`L-IN:14=40`, `L-IN:15=250`, `L-IN:18=true` → `int 40/250/1`, agreement) | §C2 F02 / global join | AGREE. The doc declares no `D-IN` repeat/numlock row; whether omarchy's default `input.conf` declares them is UNVERIFIED (not read; outside allowed host reads) |
| F23 | a later declaration wins; files read in order | not a K row; `hyprctl-verification-layer.md:39-42` (last declarer wins); r46 `hyprland-input-devices-r46.md:88` erratum E1 (two input files) | §C2 "files are read in argument order … later key wins" | AGREE |
| F24 | the set-by-user test is what selects device vs global | K16 `Hyprland-legacy-ConfigManager.cpp:1119`; r46 `hyprland-input-devices-r46.md:31` cites `Hyprland-ConfigManager.cpp:1115-1123` (same file, round-46 pin name) | §C2 same citation | AGREE (r46 and C2 cite the same lines; the r46 pin's `:1119` is byte-identical to the round-55 K16 line) |
| F25 | errata P19: `Actions::pass` sends PRESSED "only when `m_passPressed == 1`" | not a C1 row (no K row touches `pass()`); round-52 pin `Hyprland-ConfigActions.cpp:1566-1569` sends PRESSED in the `else` arm; `hyprland-synthetic-dispatch-r52-errata-r53.md:17` | none | NOT C1 SCOPE — contradicted by the pin; C3 owns it. P19's quote also joins lines 1554 and 1556-1558 with spaces, which is not a single-line quote (C3 seat) |
| F26 | registry S215 is the source for ConfigValues rows K13–K15 | `registration.md` §C1 "Existing rows reused … S318/S215 (ConfigValues.cpp)"; S215 row in `corpus/SOURCES.md` cites only `ConfigValues.cpp:629` and `:632` (debug log switches) | §C2 cites ConfigValues.cpp:277-280 directly | DISAGREE with registry scope: S215 does not cover :277-280; S318 does (`:271-279`, `:296`) — use S318 (D4) |
| F27 | registry S052 is the source for K17 (wayland 1.26.0) | `registration.md` §C1 "S052 (wayland 1.26.0 wayland.xml)"; S052 URL is `…/1.26.0/protocol/wayland.xml`, no `efb50993`, range `:2573-2699` | none | DISAGREE with the frozen `source_cell` rule ("URL … contains the frozen commit") and with the K17 locator `:2741` (D2, D3) |

## Defects found (frozen text; reported, not edited)

- **D1** F6: §C2 gives `numlock_by_default 0..1` and cites ConfigValues.cpp:277-280; line 277 has no range. A C2 implementation following §C2 has no source for the numlock bound.
- **D2** F27: §C1 `source_cell` requires the URL to "contain the frozen commit" (`efb50993…`); the reused S052 row is the tag `1.26.0` URL. The rule and the reuse of S052 for K17 cannot both hold as written.
- **D3** F19/F27: S052 cites `wl_keyboard :2573-2699`; the `repeat_info` event is at `:2741` (wl_keyboard runs to `:2753`).
- **D4** F26: S215 is scoped to debug log switches (`:629/:632`), not ConfigValues `:277-280`; S318 is the matching row.
- **D5** F9: §C2 attributes `getDeviceInt` semantics to `:1115-1123`; `getDeviceInt` is `:1131-1137`.
- **D6** F7: the "out-of-range → unsupported, line ignored" rule is a model choice; no pin shows Hyprland's handling above `.max`.
- **D7** F12: "default" is used for 25/600/0 (config) and for `m_repeatRate = 0` (member, K18); the entry must name the stage.
- **D8** F17: C2 counts and ignores a `device` key before `name`; hyprlang sets a parse error (round-46 `hyprlang-config.cpp:435`).
- **D9** `*` ambiguity: the no-`--keyboard` label `*` is also used as the NAME for the device lookup; a `device { name = * }` block would be read as the device. §C2 does not decide this.
- **D10** F8: `isNumber(VALUE, false)` (round-46 `hyprlang-config.cpp:265`) is not pinned; C2's "sign → unsupported" may differ from hyprlang if `isNumber` accepts `-`. Unverified.
- **D11** F15: the capability wording "join them to `hyprctl getoption`" covers only global options; per-keyboard live values are not observable from the given pins.
- **D12** F25 (C3 seat): errata P19 contradicted by pin `:1566-1569`; quote not single-line.

## Not checked

- K-row propositions (the entry does not exist at HEAD) and tool output (tool does not exist at HEAD): not compared.
- `hyprctl devices -j` keyboard fields for the host: not read (not needed for the table).
- omarchy default `input.conf` (`D-IN`): not read; outside the allowed host reads.
- `isNumber` definition: not in any pin.
- Counters and harness (`check-r55-controls.py`, `c1-r55-kbd-entry.py`): not run (not this seat's assignment).
- Hold-out fixtures: not looked for, not used.
