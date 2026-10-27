# Hyprland 0.56.2: how the key field of a `bind` line becomes a match for a key press on this host

source: S352 - Hyprland 0.56.2 keybind manager @ commit efb509937800 - the press path, the +8 keycode, the translated-or-sym state choice, the exact modifier compare, the name-to-keysym double lookup
source: S353 - libxkbcommon 1.13.2 `src/keysym.c` @ xkbcommon-1.13.2 - `xkb_keysym_from_name`, the one flag it accepts, and the names it refuses
source: S354 - mado host, read-only `hyprctl binds -j` and `hyprctl getoption input:resolve_binds_by_sym -j` receipt (own-work) - 192 live binds, the form census, the live option value
verified-at: 2026-10-27
recheck: on-release - when Hyprland leaves 0.56.2 or commit efb509937800, or libxkbcommon leaves 1.13.2, re-pull `src/managers/KeybindManager.cpp` and `src/keysym.c` and re-run the capture behind `.ufo/waves/round-49/receipts/live-binds-r49.txt`; also when this host stops reporting the same bind total

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| which keycode a press carries | step 1 | sourced (S352) |
| which keysym of the press is compared | step 2 | sourced (S352, S317); the live option value observed (S354) |
| whether modifiers must match exactly | step 3 | sourced (S352) |
| how a key name becomes a keysym, and what case does | step 4 | sourced (S352, S353) |
| what a key field becomes at parse time | step 5 | held S303, not re-claimed |
| whether a keycode bind and a name bind on one key collide | step 6 | sourced (S352); the census observed (S354) |

## The match, step by step

1. **The press path converts libinput's code to XKB's.** The key event carries a code that is incremented by eight before any keymap call, because libinput and xkbcommon number the same keys differently; every later lookup and every stored keycode bind use that XKB number: `KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:368.
2. **One of two state objects supplies the compared keysym.** The call site picks the per-device sym state when `input:resolve_binds_by_sym` is on and the translated state otherwise, so by default the compared sym is the one the keyboard's stored keymap produces; the option is per-device and its default is zero, held in S317: `xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE);` at Hyprland-KeybindManager.cpp:369.
3. **Modifiers are compared by exact equality.** The mask of the press must equal the mask of the bind and there is exactly one relaxation, the ignore-mods flag; on release the mask captured at press time is used, so a key that is itself a modifier does not lose its own press: `modmask != k->modmask && !k->ignoreMods` at Hyprland-KeybindManager.cpp:652.
4. **A key name is resolved twice, exact first.** The plain lookup allows no flags and the second allows case-insensitivity; a name that resolves under neither is skipped rather than compared against zero, and the library rejects any flag other than the case-insensitive bit: `xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS)` at Hyprland-KeybindManager.cpp:710.
5. **A press that carries a key name compares the name and nothing else.** The name branch is taken before the keycode branch, so the mouse and switch forms cannot fall through to a keycode bind; the parse-time key forms themselves are held in S303: `key.keyName != k->key` at Hyprland-KeybindManager.cpp:694.
6. **Keycode binds and the catch-all come after the name branch, in that order.** A press with a keycode compares the keycode, and the catch-all is the last resort inside the submap that was active at press time, so a submap switch between press and release cannot retarget it: `key.submapAtPress.name != Config::Actions::state()->m_currentSubmap` at Hyprland-KeybindManager.cpp:700.

## Observations

**OBS** S352: `const auto         KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:367 - every later keymap call uses the +8 keycode.
**OBS** S352: `xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : m_xkbTranslationState, KEYCODE);` at Hyprland-KeybindManager.cpp:369 - the compared sym is chosen by the per-device switch at the call site.
**OBS** S352: `const auto KBKEY      = xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS);` at Hyprland-KeybindManager.cpp:710 - the first lookup of a press is exact.
**OBS** S352: `if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)` at Hyprland-KeybindManager.cpp:724 - a press must equal the exact or the case-insensitive resolution.
**OBS** S352: `if (!IGNORECONDITIONS && ((modmask != k->modmask && !k->ignoreMods)` at Hyprland-KeybindManager.cpp:652 - the modifier compare is inequality of the whole mask.
**OBS** S353: `bool icase = (flags & XKB_KEYSYM_CASE_INSENSITIVE);` at libxkbcommon-src-keysym.c:242 - case-insensitivity is one bit and nothing else is honoured.

**OBS** S354: binds=192, 142 named, 42 code, 6 mouse, 2 switch; the named binds cover 64 distinct key strings and the keycodes run 10 to 201.

## Live host capture (read-only)

`hyprctl version` reports Hyprland 0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f, and `hyprctl binds -j` returns binds=192 whose raw JSON sha256 is `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`; `hyprctl getoption input:resolve_binds_by_sym -j` answers `int: 0, set: false`. The capture is `.ufo/waves/round-49/receipts/live-binds-r49.txt`.

The census by form is 142 named, 42 code, 6 mouse and 2 switch; the named strings include both `DELETE` and `Delete`, and no bind carries both a key and a keycode.
Because the option is 0, the compared sym is the translated one on this host, so a bind written as a name fires on the sym the stored keymap produces.

## Limits

- The comparison order inside a press is read from the source, not instrumented: no key event was injected and no dispatcher was fired, so what a matched bind then does is outside this entry.
- The catch-all form has no live sample on this host, so its submap precondition is sourced only.
- The multi-key flag and the long-press matcher have no live sample and are not claimed.
- The pointer and switch paths are taken from the stored strings the census prints; the path that produces them is sourced, not observed.
- The compositor half of the keymap (which keymap the keyboard stored) stays held in S318 and S319 and is not re-claimed here; `input:kb_layout` reaching a keymap is the round-48 entry's ground.
- Session state, an active inhibitor or a submap can suppress a matched bind; this entry says nothing about dispatch conditions.
