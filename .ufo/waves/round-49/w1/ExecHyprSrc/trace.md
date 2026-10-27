# Hyprland 0.56.2 `bind = MODS, KEY, dispatcher, arg` → key-press match: source trace

trace-of: Hyprland, tag `v0.56.2`, commit `efb50993780079460b0cbed1363e2166a2de1d9f` (the host's `hyprctl version` commit)
traced-at: 2026-10-27
scope: the hyprlang/legacy `bind` keyword, the key event path, and the keysym/modifier comparison. Lua `hl.bind` parsing is **not** traced (§9 L2); the matching half is shared (§5, [L01]/[L02]).
pins: `fetch/` — 13 upstream files + the GitHub commit listing, each with sha256 in `fetch/SHA256SUMS` and its commit URL in `fetch/URLS`. Note: `src/config/ConfigDescriptions.hpp` **does not exist at this commit** (HTTP 404 when fetched); the option registry with the `input:resolve_binds_by_sym` description is `src/config/values/ConfigValues.cpp` [C14]. `fetch/Hyprland-IKeyboard.cpp` is byte-equal to held row S319's pin (`8a800efe…`, verified) and is a copy for locator checking, not a new source.
locators: `locate.py` computes every line number below by regex over the pinned bytes and stores them in `locators.json`; `verify-quotes.py` re-checks each quote by line number (`QUOTES_VERIFIED 78/78`, `receipts/verify-quotes.txt`). No locator in this file is typed from memory.
executed evidence: `receipts/keysym-probes.txt` (judge + libxkbcommon probes on the host keymap), `receipts/bind-key-resolution.txt` (60 bind key names → keycode), `receipts/live-binds-shape.txt`, `receipts/live-version-option.txt`, `receipts/live-rmlvo.txt`.

---

## 1. The bind line becomes an `SKeybind`

| # | locator | verified quote | what it establishes |
|---|---|---|---|
| C01 | `Hyprland-ConfigManager.cpp:607` | `registerHandler(&::handleBind, "bind", {true});` | the hyprlang keyword `bind` (and each flag form, `true` = allow flags) is routed to `handleBind` |
| C02 | `Hyprland-ConfigManager.cpp:315` | `Config::Legacy::mgr()->handleBind(COMMAND, VALUE);` | the static wrapper forwards the keyword and the raw value to the legacy config manager |
| C03 | `Hyprland-ConfigManager.cpp:1492` | `CConfigManager::handleBind(const std::string& command, const std::string& value)` | the parser itself |
| C10 | `Hyprland-ConfigManager.cpp:1525` | `case 'i': ignoreMods = true; break;` | flag `i` = ignore modifiers; the rest are `l r e m n a t s o d p c g u k x` (same switch) |
| C08 | `Hyprland-ConfigManager.cpp:1575` | `g_pKeybindManager->stringToModMask(ARGS[0]);` | field 1 (MODS) is turned into the 8-bit `HL_MODIFIER_*` mask now, at config load |
| C09 | `Hyprland-ConfigManager.cpp:1569` | `KEYSYMS.emplace_back(xkb_keysym_from_name(splitKey.c_str(), XKB_KEYSYM_CASE_INSENSITIVE), 0);` | only the multi-key (`s`) form parses keysym names at load time, case-insensitively |
| C04 | `Hyprland-ConfigManager.cpp:1481` | `SParsedKey parseKey(const std::string& key)` | field 2 (KEY) is classified by one small function |
| C05 | `Hyprland-ConfigManager.cpp:1482` | `if (isNumber(key) && std::stoi(key) > 9)` | a bare number above 9 is a keycode |
| C06 | `Hyprland-ConfigManager.cpp:1484` | `key.starts_with("code:") && isNumber(key.substr(5))` | `code:N` is a keycode |
| C07 | `Hyprland-ConfigManager.cpp:1486` | `else if (key == "catchall")` | `catchall` is its own form |
| C11 | `Hyprland-ConfigManager.cpp:1621` | `catchall keybinds are only allowed in submaps.` | `catchall` outside a submap is a config error |
| C12 | `Hyprland-ConfigManager.cpp:1624` | `g_pKeybindManager->addKeybind(SKeybind{parsedKey.key,` | everything else stays the **string** in `SKeybind::key`; the keysym is resolved later, per key event |
| C17 | `Hyprland-KeybindManager.hpp:32` | `using KeybindKey = std::pair<xkb_keysym_t, xkb_keycode_t>;` | the pair used by the multi-key form |
| C18 | `Hyprland-KeybindManager.hpp:34` | `struct SKeybind {` | one struct carries `key`, `sMkKeys`, `keycode`, `catchAll`, `modmask`, `ignoreMods`, `submap`, `multiKey`, … |
| L01 | `Hyprland-LuaKeybind.cpp:180` | `void Objects::CLuaKeybind::push(lua_State* L, const SP<SKeybind>& keybind) {` | the Lua config hands out the same `SKeybind` type |
| L02 | `Hyprland-LuaKeybind.cpp:181` | `new (lua_newuserdata(L, sizeof(WP<SKeybind>))) WP<SKeybind>(keybind);` | … so §5/§6/§7 (matching) apply to Lua binds too; only §1/§4 (parsing) is the hyprlang path |

Consequence: `bind = SUPER, SLASH, …` stores `key = "SLASH"`, `modmask = 0x40`; `bind = SUPER, code:24, …` stores `keycode = 24`, `key = ""`. Nothing is resolved to a keysym until a key is pressed.

## 2. A key press reaches the bind matcher

| # | locator | verified quote | what it establishes |
|---|---|---|---|
| K01 | `Hyprland-Keyboard.cpp:34` | `m_keyboardEvents.key.emit(SKeyEvent{` | the device event is emitted **before** the xkb state is updated for that key |
| K02 | `Hyprland-Keyboard.cpp:41` | `updateXkbStateWithKey(event.key + 8, event.pressed);` | the state update follows the emit; `+8` is the libinput→xkb keycode offset |
| K03 | `Hyprland-InputManager.cpp:1639` | `g_pKeybindManager->onKeyEvent(event, pKeyboard)` | the input manager calls the bind manager for every keyboard key event |
| K04 | `Hyprland-KeybindManager.cpp:348` | `bool CKeybindManager::onKeyEvent(std::any event, SP<IKeyboard> pKeyboard) {` | the bind manager's entry point |
| K05 | `Hyprland-KeybindManager.cpp:367` | `e.keycode + 8; // Because to xkbcommon it's +8 from libinput` | the keycode compared everywhere below is the **xkb** keycode (evdev + 8) |
| K06 | `Hyprland-KeybindManager.cpp:369` | `xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE);` | **the one line that decides which keysym is compared** (§3) |
| K07 | `Hyprland-KeybindManager.cpp:370` | `xkb_state_key_get_one_sym(pKeyboard->m_xkbState, KEYCODE);` | a second, fully modifier-aware keysym is computed |
| K08 | `Hyprland-KeybindManager.cpp:377` | `handleInternalKeybinds(internalKeysym)` | the modifier-aware one is used only for internal keybinds (and the Escape/DnD abort), never for `bind` matching |
| K09 | `Hyprland-KeybindManager.cpp:380` | `const auto MODS = g_pInputManager->getModsFromAllKBs();` | the modifier mask compared against `SKeybind::modmask` (§6) |
| K10 | `Hyprland-KeybindManager.cpp:391` | `const auto KEY = SPressedKeyWithMods{` | the pressed-key record: keysym, keycode, modmask at press, submap at press, and **no key name** |
| K11 | `Hyprland-KeybindManager.cpp:392` | `.keysym             = keysym,` | the record carries the K06 keysym, not the K07 one |
| K12 | `Hyprland-KeybindManager.cpp:409` | `handleKeybinds(MODS, KEY, true, pKeyboard, pKeyboard).passEvent;` | on press, matching is `handleKeybinds(modmask, key, pressed, …)` |

## 3. Which keysym of the pressed key is compared

`xkb_state_key_get_one_sym` returns the single keysym of the level selected by the state's **modifiers and layout group** ([X06]); a state with no modifiers active selects the first level, which the probe below checks directly. ([X04] is the same function's note that it also applies keysym transformations.)

| `input:resolve_binds_by_sym` | state object | modifiers ever applied | layout group | keysym compared |
|---|---|---|---|---|
| `0` (host: `int 0`, `set false`) | `CKeybindManager::m_xkbTranslationState` | **none** — `KeybindManager.cpp` contains zero `xkb_state_update_mask` calls (`receipts/translation-state.txt`: `grep -c` = 0, against 3 in `IKeyboard.cpp`) | **0**, never changed | level-1 keysym of the **first configured layout** (from `input:kb_*`), regardless of the active layout or the device |
| `1` | `IKeyboard::m_xkbSymState` | **none** — updated with zeros at both update sites | **active** group | level-1 keysym of the **active layout** |
| — | `IKeyboard::m_xkbState` | depressed/latched/locked | active | **not used for `bind`** (only K08) |

Evidence for the table:

| # | locator | verified quote | what it establishes |
|---|---|---|---|
| K26 | `Hyprland-KeybindManager.cpp:289` | `void CKeybindManager::updateXKBTranslationState() {` | the default state is built by the bind manager itself |
| K35 | `Hyprland-KeybindManager.cpp:296` | `CConfigValue<std::string>("input:kb_file");` | the default state's key source is the global `input:kb_*` block |
| K27 | `Hyprland-KeybindManager.cpp:315` | `xkb_keymap_new_from_names2(PCONTEXT, &rules, XKB_KEYMAP_FORMAT_TEXT_V2,` | compiled from those global names (or from `input:kb_file` when set) |
| K28 | `Hyprland-KeybindManager.cpp:332` | `m_xkbTranslationState = xkb_state_new(PKEYMAP);` | freshly created state: group 0, no modifiers; the manager never updates it afterwards |
| M02 | `Hyprland-IKeyboard.hpp:101` | `// same as static but gets layouts` | the per-device state that *does* follow the layout |
| M08 | `Hyprland-IKeyboard.cpp:382` | `xkb_state_update_mask(m_xkbSymState, 0, 0, 0, 0, 0, group);` | on a modifier event: all three modifier masks forced to 0, only the layout group is copied |
| M09 | `Hyprland-IKeyboard.cpp:422` | `xkb_state_update_mask(m_xkbSymState, 0, 0, 0, 0, 0, m_modifiersState.group);` | same on a key event (when the state changed) |
| X05 | `xkbcommon-xkbcommon.h:2021` | `xkb_state_update_mask(struct xkb_state *state,` | the API whose last three arguments are the layout indices; zeros above are literal |
| X06 | `xkbcommon-xkbcommon.h:2107` | `Get the single keysym obtained from pressing a particular key in a` | the function K06 calls; its result depends on the state's modifiers and group |
| C13 | `Hyprland-ConfigManager.cpp:533` | `addSpecialConfigValue("device", "resolve_binds_by_sym", Hyprlang::INT{0});` | default 0, registered as a **device** value |
| C14 | `Hyprland-ConfigValues.cpp:278` | `MS<Bool>("input:resolve_binds_by_sym", "Determines how keybinds act when multiple layouts are used."` | also an `input:` option, with the upstream one-line description |
| C15 | `Hyprland-InputManager.cpp:1224` | `getDeviceInt(devname, "resolve_binds_by_sym", "input:resolve_binds_by_sym");` | per-device value, falling back to the input option |
| C16 | `Hyprland-InputManager.cpp:1241` | `pKeyboard->m_resolveBindsBySym = RESOLVEBINDSBYSYM;` | copied onto the keyboard that K06 reads |

So: **Shift/AltGr/Caps never change which keysym a `bind` sees.** Level 1 of the selected layout is the only keysym a key press can present to a keysym bind, under both settings. What `resolve_binds_by_sym` changes is only *which layout*.

Executed check on the host keymap (`receipts/keysym-probes.txt`; keymap `xkbcli compile-keymap --layout br --options compose:caps`, sha256 `efd487a3…`):

```
from_name Q       no_flags=0x0051(Q)  icase=0x0071(q)
from_name SLASH   no_flags=0x0000     icase=0x002f(slash)
key AD01 xkb= 24 zero-mod=0x0071(q)  mod5+levelthree=0x002f(slash)
key AB11 xkb= 97 zero-mod=0x002f(slash)  mod5+levelthree=0x00b0(degree)
```

A zero-modifier state (the state Hyprland matches with) reads `q` on AD01 and `slash` on AB11; AltGr+Q produces `slash` only in a state that carries Mod5|LevelThree, which is exactly the state Hyprland does not use here. `xkbcli how-to-type --keysym slash` on the same keymap prints the level-3/4 rows on `AD01` and the single level-1 row on `AB11` (`receipts/keysym-probes.txt`, `receipts/bind-key-resolution.txt`).

The judge's own row shape (used to read every receipt above): it walks keycodes and asks the keymap which modifier masks reach a level, then prints one row per mask.

| # | locator | verified quote | what it establishes |
|---|---|---|---|
| X07 | `xkbcommon-how-to-type.c:484` | `xkb_keymap_key_get_mods_for_level(` | the masks in the `MODIFIERS` column are `xkb_keymap_key_get_mods_for_level` results |
| X08 | `xkbcommon-how-to-type.c:527` | `printf("%-8u %-9s %-8u %-20s %-7u [ ",` | the printed `KEYCODE` is the xkb keycode — the same number `code:N` stores and `SKeybind::keycode` compares |

## 4. The key field, form by form

| form | stored in `SKeybind` | resolved when | compared against |
|---|---|---|---|
| `SLASH`, `F9`, `U002F`, … | `key` string | per key event, K20/K21 | `key.keysym` (§6) |
| `code:N` / bare `N` > 9 | `keycode` | never | `key.keycode` (K17) |
| `catchall` | `catchAll = true` | per event | "no other bind matched in this submap" (K18) |
| `mouse:NN` (`bindm`) | `key = "mouse:NN"` | per pointer event, as a **name** | string equality (K16) |
| `mouse_up` / `mouse_down` / `mouse_left` / `mouse_right` | `key` string | per axis event, as a name | string equality (K16) |
| `switch:on:…` / `switch:off:…` | `key` string | per switch event, as a name | string equality (K16) |
| `A&B` with flag `s` | `sMkKeys` (parsed keysyms) | per event | set match over pressed (keysym, keycode) pairs |

Name-carrying events, as built at their source:

| # | locator | verified quote | event |
|---|---|---|---|
| K29 | `Hyprland-KeybindManager.cpp:488` | `const auto KEY_NAME = "mouse:" + std::to_string(e.button);` | pointer button → `mouse:NN` |
| K30 | `Hyprland-KeybindManager.cpp:541` | `.keyName = "switch:on:" + switchName` | switch on/off |
| K31 | `Hyprland-KeybindManager.cpp:461` | `.keyName = "mouse_down"` | scroll wheel down (and the sibling up/left/right names) |
| K32 | `Hyprland-KeybindManager.cpp:620` | `m_mkKeys.emplace(key.keysym, key.keycode);` | the pressed-key set the multi-key form matches against |

Because these events carry a name and no keysym, the name branch (K16) wins before any keysym lookup.

## 5. The match loop

| # | locator | verified quote | what it establishes |
|---|---|---|---|
| K13 | `Hyprland-KeybindManager.cpp:602` | `SDispatchResult CKeybindManager::handleKeybinds(const uint32_t modmask` | one pass over `m_keybinds` in config order |
| K14 | `Hyprland-KeybindManager.cpp:652` | `modmask != k->modmask && !k->ignoreMods` | **exact** mask equality unless flag `i`; submap and `shadowed` are checked in the same condition |
| K15 | `Hyprland-KeybindManager.cpp:671` | `!k->sMkKeys.empty() && key.keyName.empty()` | multi-key binds take their own branch |
| K16 | `Hyprland-KeybindManager.cpp:694` | `if (key.keyName != k->key)` | name-carrying events (mouse/scroll/switch) compare strings, case-sensitively |
| K17 | `Hyprland-KeybindManager.cpp:697` | `if (key.keycode != k->keycode)` | `code:N` binds compare keycodes only |
| K18 | `Hyprland-KeybindManager.cpp:699` | `} else if (k->catchAll) {` | catchall is the last fallback and only inside its submap |
| K19 | `Hyprland-KeybindManager.cpp:705` | `if (key.keysym == XKB_KEY_NoSymbol)` | a key with no single keysym cannot match a keysym bind |
| K20 | `Hyprland-KeybindManager.cpp:710` | `xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS);` | the bind's name is resolved **at match time**, exact case first |
| K21 | `Hyprland-KeybindManager.cpp:711` | `xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_CASE_INSENSITIVE);` | … then case-insensitively |
| K22 | `Hyprland-KeybindManager.cpp:724` | `if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)` | a keysym bind matches either resolution |
| K33 | `Hyprland-KeybindManager.cpp:855` | `void CKeybindManager::shadowKeybinds(` | after a press, binds whose key is *also* held are marked shadowed — except `transparent`/`global` and the key that just fired |
| K34 | `Hyprland-KeybindManager.cpp:781` | `for (const auto& k : bindsHit) {` | every bind that passed is dispatched — matching collects, it does not stop at the first |

Every bind that passes is collected and dispatched, so a `code:24` bind and a `SLASH` bind on `AB11` are independent: each fires when its own form matches. `shadowed` suppresses *other* keys held at the same time (chord suppression), not a duplicate bind on the same key.

## 6. Case, aliases, and what the name actually becomes

Config time resolves names only for the multi-key (`s`) form, and does so case-insensitively (C09); a single-key bind stores the raw string (C12) and the match loop resolves it in two steps, exact case first, then case-insensitively (K20, K21). libxkbcommon's rules, from the pinned source:

| # | locator | verified quote | what it establishes |
|---|---|---|---|
| X01 | `xkbcommon-keysym.c:242` | `bool icase = (flags & XKB_KEYSYM_CASE_INSENSITIVE);` | the flag is checked once and drives the slow path |
| X04 | `xkbcommon-xkbcommon.h:2050` | `This function performs Capitalization @ref keysym-transformations.` | the keysym getter itself applies transformations; Hyprland's states carry no modifiers for them to act on |
| X02 | `xkbcommon-keysym.c:268` | `The "best" case-insensitive match is the lower-case keysym name.` | when two names differ only by case, the case-insensitive lookup returns the **lower-case** keysym (`Q` → `q`, executed above) |
| X03 | `xkbcommon-keysym.c:305` | `if (*name == 'U' || (icase && *name == 'u')) {` | `U002F`-style Unicode notation is accepted by name resolution |

Consequences, all checked by probe:
- `bind = SUPER, Q, …` resolves to `XKB_KEY_Q` (0x51) exactly and `q` (0x71) case-insensitively, and the level-1 press presents `q` → the bind fires. **The letter case in the key field does not matter** for a level-1 press.
- `bind = SUPER, SLASH, …` resolves only through the case-insensitive step (`SLASH` is not a keysym name; `slash` is). Same for `RETURN`, `BACKSPACE`, `ESCAPE`, `COMMA`, `PERIOD`, `TAB`, `SPACE`, the four arrows, `PRINT` and `DELETE` — 14 of the host's 60 distinct bind keys need the icase step (`receipts/bind-key-resolution.txt`).
- This is a **Hyprland-only** leniency: `xkbcli how-to-type` resolves `--keysym` without the flag, so the same names fail there — `--keysym SLASH` and `--keysym RETURN` both print `ERROR: Failed to convert argument to keysym` and exit 2 on the same keymap (`receipts/keysym-probes.txt`, lines 58 and 111). A C1 contract that accepts a bind-style uppercase name is wider than the judge.

## 7. Modifier comparison

| # | locator | verified quote | what it establishes |
|---|---|---|---|
| M03 | `Hyprland-IKeyboard.hpp:124` | `m_resolveBindsBySym = false;` | the per-keyboard switch defaults off |
| M01 | `Hyprland-IKeyboard.hpp:14` | `HL_MODIFIER_SHIFT = (1 << 0),` | the mask is a private 8-bit vector: SHIFT,CAPS,CTRL,ALT,MOD2,MOD3,META,MOD5 |
| K23 | `Hyprland-KeybindManager.cpp:221` | `uint32_t CKeybindManager::stringToModMask(std::string mods) {` | config mod names → that mask |
| K24 | `Hyprland-KeybindManager.cpp:223` | `std::ranges::transform(mods, mods.begin(), ::toupper);` | names are upper-cased first, so `super` = `SUPER` |
| K25 | `Hyprland-KeybindManager.cpp:236` | `mods.contains("SUPER")` | names are **substring** matches: `SUPER`, `WIN`, `LOGO`, `MOD4`, `META` all set the same bit, and any unknown residue around a known name is ignored |
| M06 | `Hyprland-IKeyboard.cpp:139` | `m_modIndexes[i] = xkb_map_mod_get_index(m_xkbKeymap, MODNAMES[i]);` | xkb modifier indices are mapped onto HL bit positions once per keymap |
| M07 | `Hyprland-IKeyboard.cpp:19` | `XKB_MOD_NAME_SHIFT, XKB_MOD_NAME_CAPS, XKB_MOD_NAME_CTRL, XKB_MOD_NAME_ALT` | MODNAMES order = HL bit order (then Num, Mod3, Logo, Mod5) |
| M04 | `Hyprland-IKeyboard.cpp:359` | `uint32_t IKeyboard::getModifiers() {` | per-keyboard contribution |
| M05 | `Hyprland-IKeyboard.cpp:360` | `m_modifiersState.depressed | m_modifiersState.latched;` | **only depressed and latched** — locked modifiers are excluded |
| M10 | `Hyprland-InputManager.cpp:1709` | `const auto ALLMODS = shareModsFromAllKBs(MODS.depressed);` | merged across keyboards |
| M11 | `Hyprland-InputManager.cpp:1711` | `MODS.depressed; // for hyprland keybinds use; not for sending to seat` | the merged result is what binds see |
| M12 | `Hyprland-InputManager.cpp:1887` | `uint32_t CInputManager::getModsFromAllKBs() {` | … and it is what K09 reads |

Therefore:
- The comparison is **exact equality** of the whole mask (K14); a bind with `SUPER` does not fire with `SUPER SHIFT` unless it lists `SHIFT` or uses flag `i`.
- **Caps Lock and Num Lock are not in the mask at all**: they are *locked* modifiers, and M05 keeps only depressed|latched. `bind = CAPS, …` or `bind = MOD2, …` can therefore not be triggered by the lock being on. (CAPS/MOD2 names still parse — K25 — they just never appear in the compared mask.)
- Empty mods (`bind = , X, …`) is legal: `MODSTR` empty skips the "invalid mod" error, and the mask compared is `0`.

## 8. The IPC surface this explains

| # | locator | verified quote | what it establishes |
|---|---|---|---|
| H02 | `Hyprland-HyprCtl.cpp:1066` | `"modmask": {},` | `hyprctl binds -j` prints the parsed 8-bit mask, not the config text |
| H03 | `Hyprland-HyprCtl.cpp:1069` | `"key": "{}",` | the JSON key field is `SKeybind::key` — empty for `code:N` / `catchall` binds, whose form is then only visible in `keycode`/`catch_all` |
| H01 | `Hyprland-HyprCtl.cpp:1048` | `modmask: {}` | the text form prints the same fields |

Live shape (`receipts/live-binds-shape.txt`, `hyprctl binds -j`, 192 binds): 146 keysym, 42 keycode-only, 2 mouse, 2 switch; mask histogram `0x40`×42, `0x41`×37, `0x44`×26, `0x0`×23, `0x49`×22, `0x48`×19, `0x8`×7, `0x4c`×6, `0x45`×3, `0x1`×2, `0xc`×2, `0x9`×2, `0xd`×1. Every observed mask fits the 8-bit vector, and `0x40` alone is the largest single group — bare `SUPER`.

Live option (`receipts/live-version-option.txt`): `input:resolve_binds_by_sym` → `{"int": 0, "set": false}`. Live RMLVO (`receipts/live-rmlvo.txt`): layout `br`, variant empty, options `compose:caps`, model and rules empty.

## 9. Consequence on this host, and limits

On the host keymap (`br`, `compose:caps`), 58 of the 60 distinct keysym-bind key names resolve to at least one keycode at level 1; the two that do not (`mouse_up`, `mouse_down`) are scroll pseudo-keys matched by name, and they account for 4 of the 146 keysym-class bind rows, so 142 rows resolve. Example from `receipts/bind-key-resolution.txt`:

```
SLASH  exact=0x0000 icase=0x002f keys=AB11(97)
RETURN exact=0x0000 icase=0xff0d keys=RTRN(36)
A      exact=0x0041 icase=0x0061 keys=AC01(38)
```

So `bind = SUPER, SLASH, …` fires from **AB11 only** — the physical slash key — never from AltGr+Q on AD01, even though AltGr+Q produces `slash`, because the matched state carries no modifiers (§3). Symmetrically, `bind = SUPER, Q, …` fires from AD01's level-1 `q`, not from a shifted press.

Limits:
- **L1** Nothing here was executed against a live Hyprland: no bind was dispatched, reloaded or mutated. The keysym half is executed against libxkbcommon on the host keymap; the dispatch half is read from source only.
- **L2** Lua `hl.bind` key-field parsing is not traced (files not pinned). The *matching* half is shared ([L01]/[L02] hold the same `SKeybind`), so §5–§7 apply; the Lua builder may accept different spellings.
- **L3** `switch:` / `mouse:` name matching is exact string equality (K16) and therefore case- and space-sensitive; this is read from code, not tested against a device.
- **L4** `shadowKeybinds` (K33) interacts with chords; this trace states its rule from source and does not measure a chord case.
- **L5** The `input:kb_file` branch of K27 (a keymap file instead of RMLVO names) was not exercised. The five `input:kb_*` values read from the host are in `receipts/live-rmlvo.txt`; `input:kb_file` was not queried, so an empty `kb_file` on the host is an assumption, not a measurement.

---

## Reproduction

```sh
cd .ufo/waves/round-49/w1/ExecHyprSrc
(cd fetch && sha256sum -c SHA256SUMS) # pins intact
python3 locate.py                      # LOCATED 78/78 (recomputes locators.json)
python3 verify-quotes.py               # QUOTES_VERIFIED 78/78
python3 check-trace.py                 # TRACE_ROWS_CHECKED 78/78 (table numbers == computed locators)
# live, read-only:
hyprctl version -j | grep -E '"(commit|tag)"'
hyprctl getoption input:resolve_binds_by_sym -j
hyprctl binds -j | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))'
grep -c xkb_state_update_mask fetch/Hyprland-KeybindManager.cpp   # 0
```
