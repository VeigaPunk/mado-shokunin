# Hyprland 0.56.2: from the key field of a `bind` line to the keysym a key press matches

source: S352 - Hyprland 0.56.2 src/config/legacy/ConfigManager.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - how the key field becomes a keycode, a catchall or a keysym name, and where a catchall is refused
source: S353 - Hyprland 0.56.2 src/managers/KeybindManager.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - which keysym of a key event is compared, and how the modifier mask and the key forms are matched
source: S354 - xkbcommon/libxkbcommon src/keysym.c @ xkbcommon-1.13.2 - the case-insensitive name lookup and the canonical-name choice of libxkbcommon 1.13.2
source: S355 - mado host, read-only `hyprctl binds -j` and `hyprctl getoption input:resolve_binds_by_sym -j` capture (own-work) - this host's bind shape by key form and the resolve setting
verified-at: 2026-10-27
recheck: on-release - when Hyprland leaves 0.56.2 or efb50993780079460b0cbed1363e2166a2de1d9f, or libxkbcommon leaves xkbcommon-1.13.2, re-pull S352-S354 and re-run the round-49 capture
ground: held open at base - the round-46 entry leaves bind resolution outside its join (`corpus/knowledge/hyprland-input-devices-r46.md:71`); the held row S319 is cited here, never re-registered.

## Steps

1. **The key field is parsed into one of four forms.** `SParsedKey parseKey(const std::string& key) {` (Hyprland-legacy-ConfigManager.cpp:1481) is the only parse: `if (isNumber(key) && std::stoi(key) > 9)` (Hyprland-legacy-ConfigManager.cpp:1482) makes a bare number above 9 a keycode, `else if (key.starts_with("code:") && isNumber(key.substr(5)))` (Hyprland-legacy-ConfigManager.cpp:1484) is the explicit keycode form, `else if (key == "catchall")` (Hyprland-legacy-ConfigManager.cpp:1486) is the catchall form, and every other string stays a **name**.
2. **`bind` hands the key field to that parse and stores the result.** `SParsedKey parsedKey = parseKey(KEY);` (Hyprland-legacy-ConfigManager.cpp:1617); a catchall outside a submap is refused, because `Catchall not allowed outside of submap!` (Hyprland-legacy-ConfigManager.cpp:1620).
3. **The modifier field becomes an integer mask at parse time, not a keysym list.** `const auto MOD    = g_pKeybindManager->stringToModMask(ARGS[0]);` (Hyprland-legacy-ConfigManager.cpp:1575) - the mask is what the match compares, so a modifier name is resolved once per bind line.
4. **The multi-key flag is the one parse-time name-to-keysym resolve.** `KEYSYMS.emplace_back(xkb_keysym_from_name(splitKey.c_str(), XKB_KEYSYM_CASE_INSENSITIVE), 0);` (Hyprland-legacy-ConfigManager.cpp:1569) asks libxkbcommon for the lower-case name; the plain path defers the name to press time.
5. **A key press is translated by one keysym source, chosen per keyboard at press time.** `const xkb_keysym_t keysym         = xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE);` (Hyprland-KeybindManager.cpp:369) reads the shared translation state when `input:resolve_binds_by_sym` is 0, else the keyboard's own sym state.
6. **The modifier mask is compared exactly, unless the bind ignores mods.** `(modmask != k->modmask && !k->ignoreMods)` (Hyprland-KeybindManager.cpp:652) - the comparison is equality against the mask built from the pressed keys, with the `i` flag as the only escape, and Caps/NumLock are part of the mask the compositor compares.
7. **A named bind is resolved at match time, first exactly and then case-insensitively.** `xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS)` (Hyprland-KeybindManager.cpp:710) resolves the bind's own name without flags, and `if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)` (Hyprland-KeybindManager.cpp:724) accepts the pressed keysym against either the exact or the lower-case resolve.
8. **A keycode bind and a catchall are matched on different fields.** The name form is compared with `if (key.keyName != k->key)` (Hyprland-KeybindManager.cpp:694), the keycode form with `if (key.keycode != k->keycode)` (Hyprland-KeybindManager.cpp:697), and a catchall with `} else if (k->catchAll) {` (Hyprland-KeybindManager.cpp:699) inside a submap.
9. **The case-insensitive flag is what makes the second resolve useful.** `bool icase = (flags & XKB_KEYSYM_CASE_INSENSITIVE);` (xkbcommon-keysym.c:242); the lookup then reports `The "best" case-insensitive match is the lower-case keysym name.` (xkbcommon-keysym.c:268), so a bind written `Return` and a press resolving `RETURN` can still meet.
10. **Not every keysym has a name.** `get_unicode_name(ks, buffer, size);` (xkbcommon-keysym.c:90) is the Unicode fallback and `return snprintf(buffer, size, "0x%08x", ks);` (xkbcommon-keysym.c:93) the unnamed non-Unicode one, so a bind name that resolves to `XKB_KEY_NoSymbol` is dropped rather than matched.

## Live host capture (read-only, 2026-10-27)

The host runs Hyprland 0.56.2 built at commit efb50993780079460b0cbed1363e2166a2de1d9f. A read-only `hyprctl binds -j` capture returns 192 binds (142 named, 42 code/keycode-carried, 6 mouse:, 2 switch:, no catchall), 90401 bytes of JSON, sha256 9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779 (receipt `.ufo/waves/round-49/receipts/hyprctl-binds-r49.txt`). `hyprctl getoption input:resolve_binds_by_sym -j` returns int 0 (set false), so a bind name is matched against the shared translation state, not a per-keyboard sym state.

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| which forms the key field takes | step 1 | sourced |
| when a catchall is refused | step 2 | sourced |
| which keysym of a press is compared | step 5 | sourced |
| how the modifier mask is compared | step 6 | sourced |
| what a name that resolves to no symbol does | steps 7, 10 | sourced |
| this host's bind shape | live capture | observed |
| which keysym the host's `br` keymap gives a bound name | step 5, step 7 | not measured here |

## Limits

- The live capture is a shape, not the JSON: the digest binds the bytes, but no bind description, argument or dispatcher text is kept, so a bind cannot be re-identified from the receipt alone.
- The per-keyboard sym state was not exercised: the host sets `input:resolve_binds_by_sym` to 0, so step 5's other branch is sourced, never observed.
- No key was pressed and no bind was dispatched: the match is read from source, and the host's own keymap is not joined to it here.
- The wiki's `Binds` page and the `input:resolve_binds_by_sym` description were not opened this round; the option's value is observed, its documentation is [UNK].
- The submap and multi-key paths are read from source only; the host has no submap in the capture, so those branches are inferred from the code.

Lane: mado-shokunin. Round: 49.
