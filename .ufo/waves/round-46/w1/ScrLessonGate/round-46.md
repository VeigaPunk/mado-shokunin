# Round 46 lesson — the input-device plane (2026-10-26, hyaku run 9, wave w1)

Lane mado-shokunin. Claims: C1 operability (capability acquisition) `tools/mado-devices.py`; C2 coverage (sourced)
`corpus/knowledge/hyprland-input-devices-r46.md`. Registration `.ufo/waves/round-46/registration.md` (freeze
`8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`). This draft carries the
three sections this seat owns; `## Mistakes` is another seat's.

## Gate

Candidates considered: the ten pins under `.ufo/waves/round-46/fetch/` (all fetched and opened by the L1 2026-10-26;
sha256 in `.ufo/waves/round-46/receipts/fetch-sha256.txt`), screened against the Hyprland tree at `efb50993` and the
hyprland-wiki at `ecc06f3` and at main (receipts `w1/ScrLessonGate/search-screen.txt` sections A-D2, plus
`w1/ScrLessonGate/registry-screen.txt` for the held-row screen).

Admitted: new rows S316-S325, tier A, status `mined`, opened 2026-10-26, used-by the entry; ten distinct receipts and
ten distinct quotes, each quote word-bounded and unique in its receipt with C/C++ comments removed (checks:
`w1/ScrLessonGate/quote-check.txt`, `QUOTE_CHECK: checked=10 failed=0`). Locators below are computed on the
whitespace-collapsed receipt (the counter's rule), never typed: the start line of the quote. S316 and S319 de-space a
source line, S320 spans `:769-770` and S325 spans `:67-68`; the start line is shown.

- S316 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/input/InputManager.cpp` (opened 2026-10-26) · `Hyprland-InputManager.cpp:1229` · `const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");` — the per-keyboard lookup reads the device block first and the global option second.
- S317 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` (opened 2026-10-26) · `Hyprland-ConfigManager.cpp:1119` · `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` — a block value the user did not set does not shadow the global option.
- S318 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp` (opened 2026-10-26) · `Hyprland-ConfigValues.cpp:272` · `MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",` — the built-in layout, while the other five keymap names default to the empty marker.
- S319 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.cpp` (opened 2026-10-26) · `Hyprland-IKeyboard.cpp:113` · `m_currentRules.layout = "us";` — the stored layout after a keymap that does not compile.
- S320 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp` (opened 2026-10-26) · `Hyprland-HyprCtl.cpp:769` · `"defaultSpeed": {:.5f}, "scrollFactor": {:.2f}` — the pointer fields the devices request prints, two decimals.
- S321 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp` (opened 2026-10-26) · `Hyprland-MiscFunctions.cpp:782` · `case ',': return '-';` — a comma in a kernel device name becomes a dash, so a block written with "Razer DeathAdder V2" never matches.
- S322 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/VirtualKeyboard.cpp` (opened 2026-10-26) · `Hyprland-VirtualKeyboard.cpp:41` · `m_keymapOverridden = true;` — set when a virtual keyboard's client sends its keymap.
- S323 · `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/VirtualKeyboard.cpp` (opened 2026-10-26) · `Hyprland-protocols-VirtualKeyboard.cpp:12` · `std::string name = "hl-virtual-keyboard";` — the name every virtual keyboard starts with; the process suffix is behind `misc:name_vk_after_proc`.
- S324 · `https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp` (opened 2026-10-26) · `hyprlang-config.cpp:435` · `special category's first value must be the key.` — the error a `device` block without a leading `name` gets; the same parser holds the continuation, `##` and bracket-key rules.
- S325 · `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Keywords.md` (opened 2026-10-26) · `wiki-Keywords.md:67` · `It's worth noting that ONLY values explicitly changed will be overwritten.` — the documented rule the set-by-user test implements; the name, the page says, comes from `hyprctl devices`.

GATE S316 receipt=.ufo/waves/round-46/fetch/Hyprland-InputManager.cpp sha256=feedf32e2e3d23aeaed7a02ef4ab94be2d66f4b22873b3166026da1e9ece4765 quote="const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");"
GATE S317 receipt=.ufo/waves/round-46/fetch/Hyprland-ConfigManager.cpp sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b quote="if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())"
GATE S318 receipt=.ufo/waves/round-46/fetch/Hyprland-ConfigValues.cpp sha256=a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754 quote="MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us","
GATE S319 receipt=.ufo/waves/round-46/fetch/Hyprland-IKeyboard.cpp sha256=8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d quote="m_currentRules.layout = "us";"
GATE S320 receipt=.ufo/waves/round-46/fetch/Hyprland-HyprCtl.cpp sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote=""defaultSpeed": {:.5f}, "scrollFactor": {:.2f}"
GATE S321 receipt=.ufo/waves/round-46/fetch/Hyprland-MiscFunctions.cpp sha256=065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9 quote="case ',': return '-';"
GATE S322 receipt=.ufo/waves/round-46/fetch/Hyprland-VirtualKeyboard.cpp sha256=bc6d984a4c9e62313501c1cdb4ace3659c16d3b77e029a3c082a77f21500ed86 quote="m_keymapOverridden = true;"
GATE S323 receipt=.ufo/waves/round-46/fetch/Hyprland-protocols-VirtualKeyboard.cpp sha256=43cbf7b39bf0910df6d933cef95f029fa336d5b432b0202280e6fc40d8db2f50 quote="std::string name = "hl-virtual-keyboard";"
GATE S324 receipt=.ufo/waves/round-46/fetch/hyprlang-config.cpp sha256=fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e quote="special category's first value must be the key."
GATE S325 receipt=.ufo/waves/round-46/fetch/wiki-Keywords.md sha256=11c0842cb31ddbfd55298c772bc44d9ad8d29c0c91c69bef6010e39b3ebaf51e quote="It's worth noting that ONLY values explicitly changed will be overwritten."

Rejected:
- REJECT hyprland-wiki `content/Configuring/Keywords.md` at main: the path is gone (HTTP 404, `w1/ScrLessonGate/search-screen.txt` §B). The wiki's main branch has moved the config plane to Lua: `content/configuring/core/config.toml` and `content/configuring/core/config-options.md` (`hl.config({...})`) replace the page, and `content/configuring/core/devices.md:12-16` documents per-device config as `hl.device({ name = ..., sensitivity = ... })`, not as a `device { name = X }` block. The pin at `ecc06f3` is the last hyprlang-era statement. Flip: the host's main config becomes a `.lua` file.
- REJECT the same wiki's `content/Configuring/Variables.md` at `ecc06f3` as a second docs row: it prints the global option table (`kb_layout` default `us` at `:186`, `scroll_factor` at `:204`/`:265`) and delegates the per-device block to Keywords (`:311-313`); the census values the entry must carry are computed from the code by clause h, so a docs duplicate covers no surface the pin set lacks.
- REJECT Hyprland `src/devices/Keyboard.cpp` (56 lines): it wires aquamarine key and modifier events and calls `updateXkbStateWithKey`; zero hits for `getDeviceString|setKeymap|kb_layout|keymap` (`w1/ScrLessonGate/search-screen.txt` §D2). No config read, no keymap compile, so it cannot move any step of the chain.
- REJECT Hyprland `src/devices/Keyboard.hpp` (21 lines, 0 symbol hits) and `src/devices/IKeyboard.hpp` (137 lines, 9 hits): declarations only — `setKeymap` at `IKeyboard.hpp:68` and the `m_keymapOverridden` field at `:94` — while the behaviour that decides the dump is the definition in the pinned `IKeyboard.cpp` (S319). The field line is read as part of S319's scope instead of taking a row.
- REJECT Hyprland `src/config/ConfigManager.cpp` as a row: it is the manager selector — a `.lua` main config selects `Lua::CConfigManager`, otherwise `Legacy::CConfigManager` (`:33-50`, two Lua assignments at `:36` and `:47`) — and holds no device store or fallback. It does settle which manager this host runs (host `hyprland.conf` present, `hyprland.lua` absent, `search-screen.txt` §C), which is why the legacy pins are the live path here.
- REJECT Hyprland `src/config/lua/ConfigManager.cpp` as a row: the Lua manager re-implements the same device-first-then-global rule over its own store (`:983-1020`), so it is parallel semantics on the plane the entry excludes, not the host's path at `efb50993`.
- REJECT `src/managers/KeybindManager.cpp:296-313` as a row: it compiles the global `input:kb_*` options into the keybind translation state with no device lookup — the keybind keymap, not the rules the dump prints (this is also why a per-device layout leaves keybinds on the global keymap).
- REJECT `src/desktop/view/Window.cpp:1156-1161` and `src/desktop/rule/windowRule/WindowRuleApplicator.hpp:129-130` as rows: both consume the global `input:scroll_factor` as a window-scope scroll effect, and neither writes the pointer field the dump prints (`InputManager.cpp:1350-1383`).
- REJECT `src/devices/IPointer.hpp` as a row: `:116` holds `std::optional<float> m_scrollFactor = {}` — the storage that makes the nullopt branch print -1 is stated in the pinned `InputManager.cpp`/`HyprCtl.cpp` lines.
- REJECT the five accessor/value headers `src/config/ConfigManager.hpp:47-52`, `src/config/legacy/ConfigManager.hpp:52`, `src/config/lua/ConfigManager.hpp:67`, `src/config/values/ConfigValues.hpp:129`, `src/helpers/MiscFunctions.hpp:42`: pure-virtual accessors and value-table declarations whose definitions are pinned (S317, S318, S321); a row on a declaration would cite no behaviour.
- REJECT `src/config/lua/bindings/LuaBindingsConfigRules.cpp:257` as a row: the Lua-era option table's `scroll_factor` float bounds (0..100) restate a ceiling the dump's field obeys through the hyprlang clamp in S316's receipt.

Held rows on the same URLs, and why new rows rather than widened ones: `corpus/SOURCES.md` already holds three scopes on `debug/HyprCtl.cpp` — S018 (`getprop` dispatch, blob URL), S158 (raw URL; `clients` tags, `getprop`, `layers`), S307 (raw URL; the monitors request) — and two on `config/legacy/ConfigManager.cpp` — S162 (windowrule keyword handlers, named special-category reconstruction, reload traversal) and S303 (monitor line grammar); plus S215 on `config/values/ConfigValues.cpp` (the two log switches at `:629`/`:632`), S182 on `helpers/MiscFunctions.cpp` (workspace command normalizer, `:478-513`), S173 on the hyprlang `config.cpp` (RHS `{{…}}` expression parsing). The new S320 (devices request), S317 (the `device` category and the per-device fallback), S318 (the keyboard and scroll defaults at `:271-300`), S321 (the name normalizer at `:777-789`) and S324 (continuation, `##`, bracket key, first-value rule) sit on those files under scopes no held row names; five pins are first uses of their URL (InputManager.cpp, IKeyboard.cpp, devices/VirtualKeyboard.cpp, protocols/VirtualKeyboard.cpp, wiki Keywords.md). Widening a held row is not available to this predicate: clause c requires a held row's cells 1-9 to stay byte-equal (`quality/counters/c2-r46-input-device-entry.py:493-496`), so an edited scope cell would fail the round's own counter for the ids other entries cite. Cost, declared in the registration: two W04 duplicate-URL census warnings (S317 beside S162/S303; S320 beside S158/S307 — S018 carries a `github.com` blob URL, so the raw URL repeats only S158 and S307), the same class `receipts/census-before.txt` already prints at base for the round-45 rows.

## Registry changes

| surface | old | new |
|---|---|---|
| `corpus/SOURCES.md` | 252 rows, last `S315` at line 264 | 262 rows; `S316`-`S325` appended after the last `S` row (`.ufo/waves/round-46/l1-draft/build-pos.py:87-92`), each 11 cells, tier `A`, `mined`, opened `2026-10-26`, recheck `90d`, used-by `corpus/knowledge/hyprland-input-devices-r46.md` |
| `corpus/README.md` | 62 knowledge-index rows, last the round-45 row at line 73 | 63 rows; one three-cell row inserted after it, naming the entry, `draft`, and `S316-S325` (`build-pos.py:102-103`) |
| `corpus/knowledge/` | 62 files | 63 files (the entry) |
| `corpus/lessons/` | 66 files | 67 files (this lesson; `build-pos.py:94-98` writes a Gate-only positive-control copy — the integrator merges this draft's prose around those ten lines) |
| `tools/` | 13 files, `mado-monitors.py` the newest | 14 files (`mado-devices.py`; C1's surface, no registry row) |
| held rows `S018`, `S158`, `S162`, `S173`, `S182`, `S215`, `S303`, `S307` | cells 1-10 unchanged | unchanged; only the census gains the two W04 lines above |
| new duplicate-URL census lines | 0 for these URLs | 2 expected (`S317`, `S320`) |

## Search log

Question: how does Hyprland 0.56.2 at `efb50993` turn the `input` block and a `device` block into the XKB names a
keyboard stores and the scroll factor a pointer reports, and which files must a row cite to bind each step?

Where searched: the Hyprland tree at the host revision (blobless clone at tag `v0.56.2`, `rev-parse HEAD` =
`efb50993780079460b0cbed1363e2166a2de1d9f`); hyprlang `v0.6.8`; the hyprland-wiki at `ecc06f3` and at main; the lane's
registry `corpus/SOURCES.md`; the host read-only (`hyprctl` reads and the existence of the two config-manager
selectors); `receipts/` and `quality/counters/c2-r46-input-device-entry.py` for what the predicate can see.

Identified: 799 files under `src` at `efb50993`; 217 match a name filter (`input|keyboard|device|hyprctl|config|virtual`);
20 files under `src` carry at least one symbol of the plane, independently of the name filter (`getDeviceString`,
`getConfigValueSafeDevice`, `scrollFactor`, `scroll_factor`, `m_keymapOverridden`, `deviceConfigExists`,
`deviceNameToInternalString`, `addSpecialConfigValue("device"`, `virtualKeyboardNameForWlClient`, `"input:kb_`,
`hl-virtual-keyboard`; `w1/ScrLessonGate/search-screen.txt` §A). Out of the tree: 7 more candidates probed (§B-D2).

Screened: 27 probed files — the 20 symbol-bearing files read at their symbol lines and the 7 out-of-tree probes —
plus the 2 pins outside the Hyprland tree (hyprlang `v0.6.8` `config.cpp`, the wiki `Keywords.md` pin): 29 candidates,
and the Gate's Admitted and Rejected lists account for all 29.

Included: 10 — new rows S316-S325: 8 of the 20 (`InputManager.cpp`, legacy `ConfigManager.cpp`, `ConfigValues.cpp`,
`IKeyboard.cpp`, `HyprCtl.cpp`, `MiscFunctions.cpp`, devices/`VirtualKeyboard.cpp`, protocols/`VirtualKeyboard.cpp`) and
the 2 candidates outside the Hyprland tree (hyprlang `v0.6.8` `config.cpp`, the wiki `Keywords.md` pin).

Excluded: 19. Of the 20 symbol files, 12: seven declaration headers (`ConfigManager.hpp`, legacy `ConfigManager.hpp`,
lua `ConfigManager.hpp`, `ConfigValues.hpp`, `IKeyboard.hpp`, `IPointer.hpp`, `MiscFunctions.hpp`); the Lua manager and
its option-table binding (lua `ConfigManager.cpp`, `LuaBindingsConfigRules.cpp`; parallel semantics on the `.lua` path);
the two window-scope scroll consumers (`Window.cpp`, `WindowRuleApplicator.hpp`); the keybind translation state
(`KeybindManager.cpp`). Of the 7 probes, all 7: wiki main `Keywords.md` (404), wiki main `devices.md` and
`config-options.md` (Lua plane), wiki `Variables.md` at the pin (global table only), `Keyboard.cpp`, `Keyboard.hpp`, and
the manager selector `config/ConfigManager.cpp` (read as context, not a row). Each exclusion names its decisive line in
the Gate's Rejected block.

Registry screen: 252 rows at the freeze; the ten pin URLs are already held by S018, S158, S162, S173, S182, S215, S303
and S307 in eight other scopes, and by no row for the five first-use URLs (`w1/ScrLessonGate/registry-screen.txt`).

Stop: every step the tool compares — parse (S324), device category and fallback (S317), per-keyboard lookup (S316),
global defaults (S318), compile and the `us` fallback (S319), the dump fields (S320), the virtual name and its override
(S322, S323), the name normalizer (S321), the documented block (S325) — has a pinned line, and the remaining
symbol-bearing files are declarations, the Lua manager, or window/keybind consumers of the same global options; none of
them adds a step between the config and the printed fields. Re-open the search when `hyprctl version` leaves `efb50993`,
when hyprlang leaves 0.6.8, or when the host's main config becomes a `.lua` file (the Lua manager path becomes live and
this entry's form no longer describes it).
