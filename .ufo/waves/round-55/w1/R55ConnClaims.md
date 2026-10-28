# R55ConnClaims — cross-claim consistency scan (round 55, wave w1)

Seat: leaf connector, no subagents, no lane edits, no git/jj mutation, no commits. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `3b55b6e`, lane HEAD at start `dbc2eefe` (freeze commit `54dacbd8` is its ancestor). Scratch `/fast/scratch/hyaku/mado-r55/R55ConnClaims/` (created, nothing written into it, removed before yield).

Deliverables (all under `.ufo/waves/round-55/w1/R55ConnClaims/`):
- `cross-claims.md` — the table `fact | C1 locator | C2 clause | agree?` (27 rows) plus defects D1–D12 and the not-checked list.
- `k-quote-check.py` — read-only script, substring test of all 24 frozen K/H quotes against their pin lines. Output in `k-quote-check.txt` (`bad 0`).
- `c1-locator-receipt.txt` — the pin line excerpts the table cites (ConfigValues, legacy ConfigManager, InputManager, wayland.xml, round-46 hyprlang-config.cpp).

## What I did

1. Read `claims-frozen.md` and `registration.md` (§C1, §C2, §C3, seat boundaries) and `frozen-tables.json` (c1.k, c1.h, c2 block).
2. Checked the pins: `sha256sum -c fetch/SHA256SUMS.txt` → all 10 `OK`.
3. Read every C1 locator the task names and the C2 config-model clauses; compared word for word in meaning.
4. Scanned `corpus/knowledge/hyprland-input-devices-r46.md`, `hyprctl-verification-layer.md`, `hyprland-synthetic-dispatch-r52-errata-r53.md`, plus `corpus/SOURCES.md` rows for S052/S215/S316/S317/S318.
5. Read-only host checks (allowed verbs only): `sha256sum ~/.config/hypr/input.conf`, `hyprctl version`, `hyprctl getoption input:repeat_rate|input:repeat_delay|input:numlock_by_default -j`.

Command outputs (trimmed):

```
$ sha256sum -c .../fetch/SHA256SUMS.txt | tail -12
Hyprland-ConfigValues.cpp: OK ... wayland-1.26.0-wayland.xml: OK   (10 of 10 OK)

$ python3 -I .../w1/R55ConnClaims/k-quote-check.py      (rc=0)
K01 ... 1220 substr=True ... H06 host-getoption.json 3 substr=True
bad 0

$ sha256sum ~/.config/hypr/input.conf
3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4   (= fetch/host-input.conf pin)

$ hyprctl version      -> Hyprland 0.56.2 ... commit efb50993780079460b0cbed1363e2166a2de1d9f clean
$ hyprctl getoption input:repeat_rate -j      -> {"option": "input:repeat_rate", "int": 40, "set": true }
$ hyprctl getoption input:repeat_delay -j     -> {"option": "input:repeat_delay", "int": 250, "set": true }
$ hyprctl getoption input:numlock_by_default -j -> {"option": "input:numlock_by_default", "int": 1, "set": true }

$ awk 'NR==277..280' fetch/Hyprland-ConfigValues.cpp
277 MS<Bool>("input:numlock_by_default", ..., false, {.refresh = ...})          <- no min/max
279 MS<Int>("input:repeat_rate", ..., 25, {.min = 0, .max = 200, ...})
280 MS<Int>("input:repeat_delay", ..., 600, {.min = 0, .max = 2000}),
$ awk 'NR==1282..1284' fetch/Hyprland-InputManager.cpp
pKeyboard->m_repeatRate  = std::max(0, REPEATRATE);
pKeyboard->m_repeatDelay = std::max(0, REPEATDELAY);
pKeyboard->m_numlockOn   = NUMLOCKON;
$ awk 'NR==1119' fetch/Hyprland-legacy-ConfigManager.cpp   (byte-identical to round-46 pin; same sha 9db68cf4...)
    if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())
$ awk 'NR>=1125 && NR<=1142' fetch/Hyprland-legacy-ConfigManager.cpp
int CConfigManager::getDeviceInt(...) { auto val = getConfigValueSafeDevice(dev, v, fallback); ... }
$ awk 'NR==2573 || NR==2741 || NR==2753' fetch/wayland-1.26.0-wayland.xml
        will disable any repeating (regardless of the value of delay).
$ grep -n '<interface name=' fetch/wayland-1.26.0-wayland.xml  -> 2573 wl_keyboard, 2754 wl_touch (wl_keyboard spans 2573-2753)
$ awk 'NR==259..262' round-46 hyprlang-config.cpp
 259 } else if (VALUE.starts_with("true") || VALUE.starts_with("on") || VALUE.starts_with("yes")) {
 260     return 1;   261 ... "false"/"off"/"no" ...   262     return 0;
```

## Findings (summary; full table in `cross-claims.md`)

Agreements (C1 locator and C2 clause say the same fact): defaults 25/600/0 (F1–F3); ranges 0..200 and 0..2000 (F4–F5); device-value-only-if-set-by-user and global fallback (F9, F24, citing K16 `:1119`); the `std::max(0,…)` clamp (F11); `true`/`on`/`yes` → 1 (F13, round-46 `:259-262`); host values 40/250/1 (F14, verified live today); later declaration wins (F23).

Contradiction or unsourced fact:

- **D1 (F6, DISAGREE).** `registration.md` §C2 states `numlock_by_default` range `0..1` and cites `Hyprland-ConfigValues.cpp:277-280`. Line 277 is `MS<Bool>("input:numlock_by_default", …, false, {.refresh = …})` with no `.min`/`.max`. No K row gives a numlock range. A C2 implementation has no source for the bound.
- **D2 (F27, registry contract conflict).** §C1 `source_cell` requires a registry URL that "contains the frozen commit" (`efb50993…`). The reuse of S052 for K17 (wayland 1.26.0) has the URL `…/1.26.0/protocol/wayland.xml`, which does not contain `efb50993`. The frozen rule and the frozen reuse cannot both pass for K17 as written.
- **D3 (F19/F27, locator).** S052's cited range `wl_keyboard :2573-2699` does not contain K17's `:2741`; the interface runs to `:2753`.
- **D4 (F26).** §C1 reuses S215 for ConfigValues K13–K15. The S215 row covers `ConfigValues.cpp:629/632` (debug log switches) only. S318 is the matching row (`:271-279`, `:296`).
- **D5 (F9).** §C2 attributes the `getDeviceInt` semantics to `legacy ConfigManager.cpp:1115-1123`. `getDeviceInt` is at `:1131-1137`; `:1115-1123` is its helper.
- **D6 (F7).** §C2 "out-of-range → unsupported, line ignored" is a model choice. Pins show only a lower-bound clamp (K04/K05). No pin shows Hyprland's handling above `.max`. The C1 entry must not say "clamped to 200/2000".
- **D7 (F12).** "Default" means 25/600/0 (config) and `m_repeatRate = 0` (member, K18 `Hyprland-IKeyboard.hpp:121`). The entry must name the stage.
- **D8 (F17).** §C2 counts and ignores a `device` key before `name`. Round-46 `hyprlang-config.cpp:435` (S324 in `hyprland-input-devices-r46.md:48`) makes hyprlang set a parse error. This is a model convention, not Hyprland behaviour.
- **D9 (ambiguity).** The no-`--keyboard` label `*` is also the NAME fed to the device lookup. A `device { name = * }` block would match it. §C2 does not decide this.
- **D10 (unverified).** `isNumber(VALUE, false)` (round-46 `hyprlang-config.cpp:265`) is not pinned. If it accepts `-`, C2's "sign → unsupported" diverges from hyprlang for negative values.
- **D11 (capability wording).** `MADO_KBDOPT_LIVE`/`live=AGREE` compares only the global option. A keyboard-level value is not observable from the pins. The SCORECARD phrase "join them to `hyprctl getoption`" must not read as per-keyboard.
- **D12 (C3 seat, reported only).** Errata P19 (`hyprland-synthetic-dispatch-r52-errata-r53.md:17`) says PRESSED only when `m_passPressed == 1`. Round-52 pin `Hyprland-ConfigActions.cpp:1566-1569` sends PRESSED in the else arm. P19's quote also joins lines 1554 and 1556–1558 with spaces, so it is not a single-line quote. Not a C1 contradiction; C3 owns it.

Knowledge docs vs the new entry (no contradiction, but the entry must keep these):
- `hyprland-input-devices-r46.md:70` lists repeat/numlock as UNK "for this join". The entry supersedes the *source* status only; per-keyboard live values stay UNK.
- `hyprland-input-devices-r46.md:34` says the dump's `numLock` is lock state, not the `numlock_by_default` option. The entry must not conflate them.
- `hyprctl-verification-layer.md:132-134` rows (`L-IN:14/15/18` → 40/250/1, agreement) match H01–H03 and today's host read.
- `hyprctl-verification-layer.md` declares no `D-IN` repeat/numlock row. Whether omarchy's default `input.conf` declares them was NOT read (outside the allowed host reads).

## Verification and limits

- Ran: read-only greps, awk line reads, `sha256sum`, `python3 -I k-quote-check.py` (rc 0, bad 0), host `hyprctl version` and three `getoption -j`. Host config sha matches the pin.
- Not run: `c1-r55-kbd-entry.py`, `check-r55-controls.py` (not this seat's job). No tool or entry exists at HEAD, so no tool output and no K-row prose were compared.
- Not read: hold-out fixtures (not looked for, not used; none encountered), omarchy default `input.conf`, `isNumber` definition.
- No installs, no tool upgrades (none needed for the scan). No host mutation. No tracked-file edits. Scratch dir removed before yield.
