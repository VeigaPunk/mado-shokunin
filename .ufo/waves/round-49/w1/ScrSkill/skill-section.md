## Binds, keysyms and the keymap (round 49)

`bind = MODS, key, dispatcher, params` (`wiki-Binds-legacy.md:9`) names the key in one of three ways, and the three do not share
a resolver: a keysym name (`SLASH`), a keycode — `code:N`, or any bare number above 9 (`legacy-ConfigManager.cpp:1482-1485`) —
or an event name (`mouse:272`, `mouse_down`, `switch:on:<name>`, `catchall`; `legacy-ConfigManager.cpp:1486-1489`). On this host
142 of 192 binds name a keysym, 42 carry an empty `key` with a `keycode`, 2 are `mouse:N`, 4 are `mouse_*` and 2 are `switch:`
(`.ufo/waves/round-49/w1/ScrSkill/receipts/binds-summary.txt`; `hyprctl binds -j`, read-only). A press matches a keysym bind
when the keysym Hyprland derives for the pressed keycode equals the bind's name **and** the modifier mask equals the bind's
mask bit for bit (`KeybindManager.cpp:652`, `:710-724`). The bind name and the pressed keycode are both keymap questions, so the pinned `xkbcli-how-to-type`
answers them off-compositor on the keymap `xkbcli compile-keymap` produced (`corpus/knowledge/xkb-keymap-compile-r48.md`).

    # the tool (round-49 C1 deliverable; Python 3 stdlib, no process, no socket, writes nothing):
    # stdout and exit status equal the judge's, byte for byte
    python3 tools/mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG
    # the judge (libxkbcommon 1.13.2-1, /usr/lib/xkbcommon/xkbcli-how-to-type, sha256 f6c0b122…)
    /usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG
    # FILE is compile-keymap's stdout from RMLVO names, not a raw keymap with includes
    /usr/lib/xkbcommon/xkbcli-compile-keymap --layout br --options compose:caps > FILE

    # host keymap (sha256 efd487a3…): --keysym slash -> AD01 levels 3/4 under Mod5/LevelThree and AB11 level 1 `[ ]`;
    # --keysym Return -> RTRN level 1; --keysym nosuchsym -> "ERROR: Failed to convert argument to keysym" + usage, rc 2.
    # ARG forms the judge takes: slash, 0x2f, U002F and 47 all print "keysym: slash (0x002f)";
    # XKB_KEY_a, U+002F and 0X2F exit 2 (receipts/keysym-how-to-type-sample.txt)

The tool refuses (exit 2) without `--disable-compose` **and** without `--keysym`, and that is the contract: without `--keysym`
the argument is read as a character or code point first — `0x100` prints `Amacron (0x03c0)`, not keysym `0x0100` — and without
`--disable-compose` the output gains an `=== Access via Compose sequences ===` section (`how-to-type.c:286-301`, `:711-712`;
`receipts/keysym-how-to-type-sample.txt`). The rest is the judge's own text: the `keysym: <name> (%#06x)` line
(`how-to-type.c:625`), the header (`:626-627`), one row per (keycode, layout, level, mask) with layout and level printed
1-based (`:527-536`), and every mask `xkb_keymap_key_get_mods_for_level` returns printed as its own row — no collapsing
(`:697-703`).

### A bind on keysym X does not fire on layout L — check, in this order

| check | first read | the rule behind it | next step |
|---|---|---|---|
| does X sit at a modifier-free level of its key? | the how-to-type rows for X: `LEVEL#` and `MODIFIERS` | the bind-side sym is read from a state created with no modifiers (`KeybindManager.cpp:332`) and never given one — the file's only reads of it are `:280` and `:369` (grep in `receipts/locators.txt`), so only a level whose mask is empty can match; the wiki states the same requirement and the AZERTY example (`wiki-Binds-legacy.md:80`, `:91`) | if every row carries `Shift`/`Mod5`/`LevelThree`, bind the key's modifier-free sym, or put the level's modifiers in MODS — never the shifted symbol itself |
| which layout does the bind name resolve in? | `input:kb_layout` and `input:resolve_binds_by_sym` | the bind keymap is built from `input:kb_file` else the five `input:kb_*` names (`KeybindManager.cpp:296-314`); with `resolve_binds_by_sym` false — default 0 (`legacy-ConfigManager.cpp:533`), `ConfigValues.cpp:278`, live `{"int": 0, "set": false}` in `receipts/hyprctl-version-options.txt` — the state stays on the first layout (`wiki-Variables-legacy.md:181`) | with `kb_layout = a,b` and X only in `b`: put `b` first, or set `input:resolve_binds_by_sym = 1`, after which the sym comes from the device keymap's active group at a modifier-free level (`KeybindManager.cpp:369`, `IKeyboard.cpp:218`, `:382`) |
| does the device's own layout differ from `input:kb_layout`? | the per-device blocks and `hyprctl devices -j` | the bind keymap never reads `device:<name>:kb_layout`; it reads the `input:` names only (`KeybindManager.cpp:299` against `InputManager.cpp:1229`), while each device applies its own with that fallback (`InputManager.cpp:1224-1241`) | bind the majority keyboard's syms, or bind `code:N`, which compares the keycode alone (`KeybindManager.cpp:696-698`) |
| did the bind-side compile fall back? | a deliberate failing compile of the expected names (`--layout zz` rc 1, `SKILL.md:2226` matrix) | a failed compile retries with an all-empty RMLVO set (`KeybindManager.cpp:326-328`), so binds are compared against a keymap built from the library's defaults rather than the config's names, while the device may show the round-46 `FALLBACK` shape (`corpus/knowledge/hyprland-input-devices-r46.md`, S319) | fix the names; to see the fallback keymap, run how-to-type with no `--layout`/`--options` and compare its rows with the configured compile |
| is the key field a keycode rather than a name? | `hyprctl binds -j`: `key: ""` with a non-zero `keycode` is a keycode bind (42 here) | `code:N` and any bare number > 9 store `keycode` (`legacy-ConfigManager.cpp:1482-1485`) and match `key.keycode` only (`KeybindManager.cpp:696-698`), against `e.keycode + 8` (`:367`) — the same numbering as the how-to-type `KEYCODE` column | read X's keycode off the how-to-type row and write `code:<that>`; a bare numeric key field is a keycode, never a keysym value |
| does the mask equal the bind's mask? | the bind's `modmask` (host: 64 = SUPER, 65 = SUPER\|SHIFT, 68 = SUPER\|CTRL) and the row's `MODIFIERS` | equality, not subset (`KeybindManager.cpp:652`); the bind mask is substring-matched on the uppercased mod string (`:221-240`), the pressed mask is depressed-or-latched real mods merged over all keyboards (`IKeyboard.cpp:359-370`, `InputManager.cpp:1711`, `:1915-1931`) — a locked Caps/Num adds nothing, so how-to-type's `Lock` rows are not bind masks | hold exactly the modifiers the mask names (AltGr is MOD5, `IKeyboard.hpp:21`; SHIFT is bit 0, `:14`); `i` drops the mask comparison (`legacy-ConfigManager.cpp:1525`, `KeybindManager.cpp:652`) |
| does the name resolve at all? | `mado-keysym.py … --keysym NAME`: rc 2 means NoSymbol | the name is resolved twice — exact, then case-insensitive (`KeybindManager.cpp:710-711`) — and either value matches (`:724`); case-insensitive picks the lower-case variant where names differ only by case (`keysym.c:242`, `:268`), which is why `SLASH` and `slash` both work | fix the spelling; `XKB_KEY_` is not part of the name (`wiki-Binds-legacy.md:62`; `--keysym XKB_KEY_a` → rc 2, `receipts/keysym-how-to-type-sample.txt`) |
| does the key still carry X after `kb_options`? | how-to-type for the key's own sym, then the compiled keymap | an option can replace a key's syms: `compose:caps` (`~/.config/hypr/input.conf:11`) makes `<CAPS>` carry `Multi_key` at both levels (`host-br.xkb:1581-1584` in the receipt), so `Caps_Lock` has no position and `Multi_key` has keycode 66 | bind the sym the compiled keymap carries; `--keysym <the key's label>` finds nothing and says so with rc 0 plus an empty table |
| is the bind in this submap, and is another bind on the same key? | `hyprctl binds -j` `submap` (host: all 192 empty) and the bind list | the submap name must match (`KeybindManager.cpp:652`), `catchall` exists only inside a submap (`:700`, `legacy-ConfigManager.cpp:1619-1621`), and every match in one event is collected and dispatched (`:773`, `:781-812`) — so a `code:` bind and a keysym bind on one physical key both run | `u` makes a bind submap-universal (`wiki-Binds-legacy.md:150`); `s` combines keys across mod/key pairs (`legacy-ConfigManager.cpp:1526`) |

### Error patterns

| symptom | first read | the rule behind it | next step |
|---|---|---|---|
| the bind is listed by `hyprctl binds -j` and never fires | the `key` string and whether it is a name the header carries | a name that resolves to NoSymbol twice is skipped per event (`KeybindManager.cpp:705`, `:714-724`), and no parse-time error is raised for it — the config manager's only `xkb_keysym_from_name` calls belong to the `s` multi-key path (`legacy-ConfigManager.cpp:1569-1572`) | `--keysym <key>`: rc 2 is the silent skip made visible; the header's name is the segment after `XKB_KEY_` (`wiki-Binds-legacy.md:62`; rc 2 on `XKB_KEY_a`, `receipts/keysym-how-to-type-sample.txt`) |
| a bind on `SLASH`, `ampersand`, `0`–`9` or another shifted character never fires | the level rows for that sym | the compared sym is the modifier-free one, so the shifted symbol of a key is not addressable (`KeybindManager.cpp:332`, `:369`; `wiki-Binds-legacy.md:80`) | bind the key's modifier-free sym (on this host `slash` is AB11 level 1, `[ ]`) and put SHIFT/MOD5 in MODS if the combination needs it |
| a bind fires on an unexpected physical key, or stops firing after an option edit | the option list in `input.conf` and the compiled keymap | options rewrite syms at compile time — `compose:caps` moved `Caps_Lock` to `Multi_key` on this host (receipt `host-br.xkb:1581-1584`) | re-derive the key with how-to-type on the *current* keymap, never from the keycap label |
| a numeric key field binds something unrelated | the key field and the `keycode` field | a bare number > 9 is a keycode (`legacy-ConfigManager.cpp:1482-1483`); keysym values are spelled `0x…` or by name (`keysym.c:325`; how-to-type takes decimal keysyms only with `--keysym`, `how-to-type.c:291`) | use `code:<n>` for a keycode and `0x<hex>` for a keysym value |
| a bind on a keysym that lives in the second layout never fires, or fires only after the layout is switched | `input:resolve_binds_by_sym` and the active group | false (the default) resolves against the first layout whatever the active group is (`wiki-Variables-legacy.md:181`; live `int 0`) | set it globally, or per device, and accept that the sym then follows the active layout (`KeybindManager.cpp:369`) |
| Caps Lock or Num Lock being on/off changes nothing (or you expect it to) | the `modmask` and the level rows | locked mods are not part of the compared mask (`IKeyboard.cpp:360`), and `Lock` rows in how-to-type are level masks, not Hyprland bits | treat locks as irrelevant to bind matching; bind the lock key by its sym or keycode if it must do something |
| `unbind = SUPER, Tab` leaves `SUPER, TAB` bound | both lines' key spelling | removal compares the stored strings exactly (`KeybindManager.cpp:197-198`); the wiki says the same (`wiki-Binds-legacy.md:111`) | write the same case in `unbind` as in `bind` |
| a `bind` on `mouse:272` does nothing while `bindm` works | the bind line's flags | the `m` flag is what routes the handler to `mouse` (`legacy-ConfigManager.cpp:1589`, `:1594`; `wiki-Binds-legacy.md:144`) | use `bindm`, or bind `mouse_down`/`mouse_up`/`mouse_left`/`mouse_right` for the wheel, which arrives as those names (`KeybindManager.cpp:461-468`) |

Notes: the pins are `efb50993780079460b0cbed1363e2166a2de1d9f` (Hyprland 0.56.2 — the host's `hyprctl version`,
`receipts/hyprctl-version-options.txt`) and `xkbcommon-1.13.2`, listed with sha256 in
`.ufo/waves/round-49/w1/ScrSkill/pins/PINS.txt`; the wiki is pinned at
`78e64e80f4e84634744cd49728a198a7ebaf579a`, the hyprlang-era `Binds.md` (its successor `e99eac80…` documents the lua
configuration, also pinned), because this host's config plane is hyprlang (`SKILL.md:49-50`, `~/.config/hypr/input.conf:10-11`). The
Hyprland reads cover the legacy config manager (`src/config/legacy/ConfigManager.cpp`) only — 0.56.2 also carries a Lua
manager (`src/config/ConfigManager.cpp:36-50`, pinned) whose bind handler this section does not read. The host has
one layout (`kb_layout = br`), so the multi-layout rows rest on source and wiki, not on a live observation. No input is
injected in this lane, so "a bind fires" is never observed live: what is measured is the keymap half (how-to-type) and the
bind table (hyprctl). `mado-keysym.py` is the round-49 C1 deliverable; until the L1 commits it, the judge line is the
answer. The keymap digest `efd487a3…` reproduces the round-48 receipt's digest for the same RMLVO, so the two rounds compare
on identical bytes.
