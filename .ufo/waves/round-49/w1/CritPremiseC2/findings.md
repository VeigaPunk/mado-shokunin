# CritPremiseC2 findings — ground/open-premise attack

## Verdict

**Premise is mostly sound for press-time matching, but the framing is materially incomplete.** At base, the broad matching path is open: the held material records bind declarations/parser table and one option boundary, but not how a key press is translated and compared. However, a new entry MUST explicitly build on `bind-table-r25.md` and not re-present its parser grammar as new ground. In the province, mado owns the Hyprland configuration/keybind surface; sibling-lane PROVINCE/README checks found only references back to mado, not another owner or matching entry. The claimed 0.56.2 commit contains the relevant code paths. No entry/fetch/pins S352+ existed yet at time of this check, so provenance requirements remain unverified.

## Counterexample / held coverage

- `corpus/knowledge/bind-table-r25.md` at base (read from base tree; body lines 25–56) already covers bind grammar/flags/modifiers and `parseKey`: line 46 says decimal/code:N/catchall handling and preserves other key strings; lines 38–44 cover field parsing/modifier conversion; lines 50–56 cover rejection and registration/table identity. `tools/mado-binds.py` additionally implements the parser projection (`parse_key` lines 111–116; bind representation around 704–722). Therefore C2’s proposed list “key name to keysym (case handling, code:, mouse:N, mouse_up/down, switch:, catchall)” partly overlaps held parser/key forms. New work should distinguish parser recognition already held from press-time matching not held, and cite S162/entry r25 for the former.
- `corpus/knowledge/keybind-rule-semantics.md:103-111` documents key field forms, but explicitly labels named keysym interpretation `[INF-docs]` at line 106 (“use the segment after `XKB_KEY_`”); it does not state the runtime’s xkb lookup flags or press-time matching. This supports “not sourced matching semantics,” not “no key-field knowledge.”
- `corpus/knowledge/hyprland-input-devices-r46.md:71` says per-device layouts do not change the keymap binds resolve against unless `resolve_binds_by_sym=1`, and that its join does not check binds. This is an explicit held boundary; it does not explain which sym is selected or the comparison algorithm.
- `corpus/knowledge/xkb-keymap-compile-r48.md` describes compilation and fallback, not bind resolution. Its `ground` points to r46:69 as open compile behavior; do not conflate that with bind-resolution coverage.
- At base `corpus/SOURCES.md` has S162 for Hyprland ConfigManager.cpp and S319 for IKeyboard.cpp. S162 is already used by r25 and its source URL is the exact commit `efb509…`; S319 is keyboard keymap/fallback, not the key event matching path. C2’s requirement to cite held S319 without re-registering is appropriate. Avoid registering S162 again; cite/reuse it for parse overlap and register genuinely new source files for matching.

## Province / sibling check

- `mado-shokunin/PROVINCE.md:10-12` (read at lane current state; ownership language) and `SKILL.md:69-74` assign Hyprland/app keybinds to mado. `PROVINCE.md` round-46 refinement (line 114 in current file) explicitly excludes `resolve_binds_by_sym` from the input-device join; this makes it a boundary, not an ownership gap.
- `../kotoba-shokunin/PROVINCE.md:69` states mado owns the Hyprland/waybar/walker/terminal config plane, with no split; `../tsukuroi-shokunin/PROVINCE.md:124` likewise lists mado’s Hyprland/keybind surface. Sibling READMEs/PROVINCE grep found no separate owner or key-press matching treatment. `README.md`’s corpus index points to r25 for bind-table parsing, not press resolution.
- `corpus/knowledge/remaining-planes-census.md:36` calls the Hyprland config/keybind/rules plane a source-order re-measure; it does not claim key-press matching coverage.

## Source verification at claimed commit

Fetched into scratch only from `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/`; SHA256s observed:

- `src/config/legacy/ConfigManager.cpp`: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` (same held S162).
- `src/managers/KeybindManager.cpp`: `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40`.
- `src/managers/KeybindManager.hpp`: `cee22c13d413ab389803e0eb87a6fcefadedea885cee4457b56ae351228dd1e0`.
- `src/devices/IKeyboard.cpp`: `8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d` (same held S319).
- `src/managers/input/InputManager.cpp`: `feedf32e2e3d23aeaed7a02ef4ab94be2d66f4b22873b3166026da1e9ece4765`.
- `src/keysym.c` libxkbcommon 1.13.2: `123e3390d443b85c9cc9d1833c168ecda955d1c642fda03881052bb99c3369c5` (scratch only; no cite until registered/pinned into lane fetch).

Source findings, line numbers computed with `grep -n`/context reads:

- `ConfigManager.cpp:1481-1489` has `parseKey`: decimal >9 and `code:N` become keycode; `catchall` is special; remaining strings are preserved. `:1569-1572` uses `xkb_keysym_from_name(..., XKB_KEYSYM_CASE_INSENSITIVE)` for multi-key entries; ordinary bind key strings are not converted there. `:1617-1624` registers `SKeybind`.
- `KeybindManager.cpp:367-369`: libinput code is adjusted by +8; matching keysym comes from `xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE)`. This is a decisive source check against the proposed prose: option false uses shared `m_xkbTranslationState`; true uses per-keyboard `m_xkbSymState`.
- `InputManager.cpp:1224-1241`: per-device `resolve_binds_by_sym` is read with global `input:resolve_binds_by_sym` fallback and assigned to keyboard. `ConfigManager.cpp:533` registers default 0.
- `IKeyboard.cpp:379-381`: regular state gets depressed/latched/locked + effective group; symbol state gets zero modifier masks and only the group. `KeybindManager.cpp:289-332` builds the shared translation state from global configured `input:kb_*`/`kb_file`; source shows it is constructed/rebuilt there, not updated for active layout in the key event path.
- `KeybindManager.cpp:652` compares `modmask != k->modmask` unless `ignoreMods`; the remaining submap/shadow conditions are separate. `:697-717` matches explicit keycode by keycode; otherwise resolves stored key name both `NO_FLAGS` and `CASE_INSENSITIVE`, rejects unresolved names, then compares against event keysym. This is NOT keycode-first precedence: the loop can collect multiple matching binds; dispatch loop at `:760+` iterates `bindsHit`. Keycode and keysym bind can both match the same event.
- `InputManager.cpp:1701,1711` writes only merged `MODS.depressed` to `m_lastMods`; `getModsFromAllKBs` returns it (`:1887-1888`). Thus the modmask comparison is exact equality on depressed modifiers (unless `i`/ignoreMods), not all XKB depressed+latched+locked state.
- `KeybindManager.cpp:446-464` uses event keyName for wheel names; `:488+` uses `mouse:N`; `:536-545` synthesizes `switch:...` names. In `handleKeybinds` (`:692-700`) nonempty `keyName` is compared directly to `k->key`; separate from keysym path.
- libxkbcommon `keysym.c:237+` confirms case-insensitive lookup searches case-folded duplicates and returns the “best” lower-case keysym name (`:270-305`); Hyprland itself also tries exact name first then case-insensitive (`KeybindManager.cpp:710-711`).

Live read-only check (command output, no receipt written here): `hyprctl version` returned Hyprland 0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f`; `hyprctl getoption input:resolve_binds_by_sym -j` returned `{"option":"input:resolve_binds_by_sym","int":0,"set":false}`; `hyprctl binds -j` length 192. This supports the declared host context only, not behavior under a key press.

## Smallest safe correction

1. Tighten the C2 premise to “press-time key translation/matching and modifier comparison are not yet grounded,” rather than implying all key-field handling is open.
2. Explicitly cite `bind-table-r25.md`/S162 as held parser ground; do not re-state parseKey, field grammar, keycode/catchall parsing as newly established.
3. Verify and pin the actual new source path `src/config/legacy/ConfigManager.cpp` if needed; do not assume `src/config/ConfigManager.cpp`. Reuse held S162/S319 rather than creating duplicate source authorities. Add new KeybindManager / InputManager source rows and libxkbcommon/wiki sources only for new claims.
4. State the active-versus-shared keymap choice, zeroed-modifier symbol state, exact depressed-modifier equality, `ignoreMods`, and simultaneous keycode+keysym matches precisely; avoid unsupported “translated vs untranslated” shorthand. The 0.56.2 code demonstrates a source route, not real press outcomes.
5. Ensure the eventual committed entry's source locators/quotes, source registry rows, and live receipt are copied/pinned into the lane; those had not appeared at time of this review.
