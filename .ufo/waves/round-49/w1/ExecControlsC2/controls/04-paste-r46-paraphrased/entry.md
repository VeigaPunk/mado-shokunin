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

## The chain, step by step

1. Parsing. The configuration language parses a document row by row; a row ending in a backslash is joined with the next one, and a last row that still ends in one is dropped. A row whose first character is `#` is a comment; elsewhere a `#` ends the row unless it is doubled, and a doubled `##` leaves one literal `#` in the field. Inside a category, a key's full label is the category stack joined with `:`. (`KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:367)
2. The `device` block is a keyed special category: Hyprland registers it with `label` as its key and 47 fields in all. Three spellings reach the same per-device store: `device { label = X ... }`, `device[X] { ... }` and `device[X]:key = field`; the wiki documents only the first. A second block with the same label merges into the first: it overwrites only the keys it sets. A `device { }` block whose first assignment is not `label` is a configuration error: the first field must be the key. The current device is forgotten when the last category closes, so a flat `device:kb_layout = x` outside a block runs into the same first-field-must-be-the-key error instead of setting anything. (`KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:367)
3. Per-input device lookup. For every input device, applyConfigToKeyboard parses six keymap labels per device: for example the kb_layout lookup asks the device first and the global option second. The device field counts only when the user set it; otherwise the global fallback applies. The block exists when one carries the input device's exact normalised label, and the STRVAL_EMPTY sentinel parses as the empty string. The global built-in fallbacks are `us` for the layout and empty for the rest. When nothing changed since the last apply, the input device is skipped. Every `input:kb_*` option re-applies input devices when changed, which is how a runtime `hyprctl keyword` reaches a input device. (`KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:367)
4. Compiling. The five labels go to setKeymap as the input device's current rules, which keeps them before any build. A non-empty kb_file (relative to the configuration document) is tried first and the labels only when no keymap came from the document; so with a readable kb_file the printed labels say nothing about the keymap in use, and even labels that would not build are printed as written. If no keymap results, the kept rules are reset to layout `us` with every other label empty and an error overlay labels the rejected labels, which is why a typo in `kb_layout` shows up in the snapshot as `us`, not as the typo; a comma list of layouts collapses to that single `us`. (`KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:367)
5. What the snapshot shows. `hyprctl devices -j` reports the kept rules of each input device - rules, model, layout, variant, options - and for each pointer a `scrollFactor` with two decimals. The input device object also carries `active_keymap` and `active_layout_index` (the compiled keymap's active layout, named in XKB's words such as `Portuguese (Brazil)`, not the configuration's `br`), `capsLock` and `numLock` (locked-modifier state, not the `numlock_by_default` option) and `main`, which marks the input device `switchxkblayout main` acts on, not the primary hardware input device: on this host only the input-method virtual input device has it. The `mice` list holds every pointer, touchpads included, and its `defaultSpeed` is libinput's built-in fallback, not the configured sensitivity. A pointer's factor is the device block's `scroll_factor` clamped to 0..100 only when that block explicitly sets it, and is otherwise unset, printed as -1.00. The global `input:scroll_factor` (range 0..2, unlike the block's 0..100 clamp) never reaches the printed field, and neither does `input:touchpad:scroll_factor`. (`KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:367)
6. Virtual input devices. A virtual input device (an input method such as fcitx5) is named `hl-virtual-input device`, followed, while `misc:name_vk_after_proc` is on (the built-in fallback), by `-` and the normalised label of its client's binary or `-unknown`. The configuration's labels are applied to it once at creation; when its client sends a keymap the input device marks the keymap overridden, and setKeymap then returns early, so the rules the snapshot reports for it are the creation-time labels, not a witness of the keymap in use; its `active_keymap` does label the active layout of the client's keymap. (`KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:367)
7. Names. A device's label is lower-cased with space, newline and comma replaced by `-`, an empty result becomes `unknown-device`, and a label already taken by any input device gets a `-1`, `-2` suffix. A block written with the product label as the kernel reports it (`Razer DeathAdder V2`) never matches: the lookup compares the kept key exactly. The wiki tells the user to copy the label from `hyprctl devices` and documents that per-device options overwrite the `input` ones. (`KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:367)

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
