# From `input` and `device` config to `hyprctl devices -j`: how Hyprland 0.56.2 picks each keyboard's XKB names and each mouse's scroll factor

source: S316 - hyprwm/Hyprland src/managers/input/InputManager.cpp @ efb5099 (v0.56.2) - per-keyboard and per-pointer config application, device naming
source: S317 - hyprwm/Hyprland src/config/legacy/ConfigManager.cpp @ efb5099 - the `device` special category and the per-device fallback
source: S318 - hyprwm/Hyprland src/config/values/ConfigValues.cpp @ efb5099 - the `input:kb_*` and `input:scroll_factor` options and defaults
source: S319 - hyprwm/Hyprland src/devices/IKeyboard.cpp @ efb5099 - stored rules, the fallback keymap, kb_file, overridden keymaps
source: S320 - hyprwm/Hyprland src/debug/HyprCtl.cpp @ efb5099 - the `devices` request and its JSON fields
source: S321 - hyprwm/Hyprland src/helpers/MiscFunctions.cpp @ efb5099 - how a device name is normalized
source: S322 - hyprwm/Hyprland src/devices/VirtualKeyboard.cpp @ efb5099 - a virtual keyboard adopts the keymap its client sends
source: S323 - hyprwm/Hyprland src/protocols/VirtualKeyboard.cpp @ efb5099 - the names virtual keyboards get
source: S324 - hyprwm/hyprlang src/config.cpp @ v0.6.8 (the host's hyprlang 0.6.8-5) - comments, continuations, keyed special categories
source: S325 - hyprwm/hyprland-wiki content/Configuring/Keywords.md @ ecc06f3 (2026-04-20) - the documented per-device block
verified-at: 2026-10-26
recheck: on-release - when `hyprctl version` leaves efb50993 or hyprlang leaves 0.6.8 (or 90d at the latest) re-pull the ten pins and re-run the counter; observed 2026-10-26 (w1/ScoutRecheck, not a pin): Hyprland main has no src/config/legacy/ and configures devices through Lua, so a release past 0.56.x drops the `device { }` block form this entry and tools/mado-devices.py describe
ground: input-device plane, runtime state agreement for keyboard XKB names and pointer scroll factors; per-device resolution was absent at base (claim grep exit 1); held neighbours: point readings of `input:kb_layout` in hyprctl-verification-layer.md and config-health-report-r3.md
Lane: mado-shokunin. Round: 46.

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| which value of `kb_layout`, `kb_variant`, `kb_options`, `kb_model`, `kb_rules`, `kb_file` a keyboard gets | the chain below, steps 1-4 | sourced at the host's revision |
| what `hyprctl devices -j` prints for a keyboard and a mouse | step 5 | sourced |
| why a keyboard can print `us` although the config says otherwise | step 4 | sourced; the compile failure itself is not observed here |
| whether this host's keyboards and mice agree with their config | the live run | observed 2026-10-26 |
| which keymap a virtual keyboard really uses | the dump's `active_keymap` names its active layout (step 5); the rest of the keymap is UNK | partly observable |

## The chain, step by step

1. Parsing. The config language reads a file line by line; a line ending in a backslash is joined with the next one, and a last line that still ends in one is dropped (continuation, hyprlang-config.cpp:44-66). A line whose first character is `#` is a comment; elsewhere a `#` ends the line unless it is doubled, and a doubled `##` leaves one literal `#` in the value (comment rule, hyprlang-config.cpp:674-702). Inside a category, a key's full name is the category stack joined with `:`.
2. The `device` block is a keyed special category: Hyprland registers it with `name` as its key (hyprlang special category, Hyprland-ConfigManager.cpp:518-540 registers the device block and its first values) and 47 values in all (Hyprland-ConfigManager.cpp:541-565 ends the list at pressure_range_max). Three spellings reach the same per-device store: `device { name = X ... }`, `device[X] { ... }` and `device[X]:key = value` (the bracket name is cut out of the key, hyprlang-config.cpp:291-321; the category it names is created and keyed at hyprlang-config.cpp:322-350); the wiki documents only the first (wiki-Keywords.md:70-79). A second block with the same name merges into the first: it overwrites only the keys it sets. A `device { }` block whose first assignment is not `name` is a config error: the first value must be the key (hyprlang-config.cpp:420-440 reports "first value must be the key"). The current device is forgotten when the last category closes (reset at the close, hyprlang-config.cpp:885-899), so a flat `device:kb_layout = x` outside a block runs into the same first-value-must-be-the-key error instead of setting anything.
3. Per-keyboard lookup. For every keyboard, applyConfigToKeyboard reads six keymap names per device (Hyprland-InputManager.cpp:1213-1238, applyConfigToKeyboard): for example the kb_layout lookup asks the device first and the global option second (Hyprland-InputManager.cpp:1226-1231, kb_layout and its siblings). The device value counts only when the user set it; otherwise the global fallback applies (Hyprland-ConfigManager.cpp:1115-1123, set-by-user test then global fallback). The block exists when one carries the keyboard's exact normalised name (Hyprland-ConfigManager.cpp:1196-1201, deviceConfigExists; the name is the `name` the dump prints), and the STRVAL_EMPTY sentinel reads as the empty string (Hyprland-ConfigManager.cpp:1156-1168, STRVAL_EMPTY; its spelling `[[EMPTY]]` lives in a Hyprland header outside these pins). The global defaults are `us` for the layout and empty for the rest (Hyprland-ConfigValues.cpp:271-276, default XKB names). When nothing changed since the last apply, the keyboard is skipped (Hyprland-InputManager.cpp:1270-1280, did not change). Every `input:kb_*` option re-applies input devices when changed, which is how a runtime `hyprctl keyword` reaches a keyboard.
4. Compiling. The five names go to setKeymap as the keyboard's current rules (Hyprland-InputManager.cpp:1282-1295, setKeymap with the names), which stores them before any compile. A non-empty kb_file (relative to the config file) is tried first and the names only when no keymap came from the file (Hyprland-IKeyboard.cpp:87-99, kb_file read before the names); so with a readable kb_file the printed names say nothing about the keymap in use, and even names that would not compile are printed as written. If no keymap results, the stored rules are reset to layout `us` with every other name empty and an error overlay names the rejected names (Hyprland-IKeyboard.cpp:101-116, fallback to us after an error overlay), which is why a typo in `kb_layout` shows up in the dump as `us`, not as the typo; a comma list of layouts collapses to that single `us`.
5. What the dump shows. `hyprctl devices -j` prints the stored rules of each keyboard - rules, model, layout, variant, options - and for each pointer a `scrollFactor` with two decimals (Hyprland-HyprCtl.cpp:765-772, scrollFactor field; Hyprland-HyprCtl.cpp:785-802, layout and the other stored names). The keyboard object also carries `active_keymap` and `active_layout_index` (the compiled keymap's active layout, named in XKB's words such as `Portuguese (Brazil)`, not the config's `br`), `capsLock` and `numLock` (locked-modifier state, not the `numlock_by_default` option) and `main` (Hyprland-HyprCtl.cpp:793-801, main and the lock fields), which marks the keyboard `switchxkblayout main` acts on, not the primary hardware keyboard: on this host only the input-method virtual keyboard has it (Hyprland-InputManager.cpp:1934-1942, disableAllKeyboards clears main for physical keyboards). The `mice` list holds every pointer, touchpads included, and its `defaultSpeed` is libinput's default, not the configured sensitivity. A pointer's factor is the device block's `scroll_factor` clamped to 0..100 only when that block explicitly sets it (Hyprland-InputManager.cpp:1376-1383, scroll_factor explicitly set), and is otherwise unset, printed as -1.00 (Hyprland-InputManager.cpp:1379-1383, nullopt branch). The global `input:scroll_factor` (range 0..2, unlike the block's 0..100 clamp) never reaches the printed field (Hyprland-ConfigValues.cpp:290-300, input:scroll_factor is a separate global option), and neither does `input:touchpad:scroll_factor`.
6. Virtual keyboards. A virtual keyboard (an input method such as fcitx5) is named `hl-virtual-keyboard`, followed, while `misc:name_vk_after_proc` is on (the default), by `-` and the normalised name of its client's binary or `-unknown` (Hyprland-protocols-VirtualKeyboard.cpp:11-31, hl-virtual-keyboard naming). The config's names are applied to it once at creation; when its client sends a keymap the keyboard marks the keymap overridden (Hyprland-VirtualKeyboard.cpp:36-44, virtual keyboard override flag), and setKeymap then returns early (Hyprland-IKeyboard.cpp:60-64, keymap overridden early return), so the rules the dump prints for it are the creation-time names, not a witness of the keymap in use; its `active_keymap` does name the active layout of the client's keymap.
7. Names. A device's name is lower-cased with space, newline and comma replaced by `-` (Hyprland-MiscFunctions.cpp:777-789, lower-case name normalizer), an empty result becomes `unknown-device`, and a name already taken by any input device gets a `-1`, `-2` suffix (Hyprland-InputManager.cpp:2119-2131, duplicate suffix). A block written with the product name as the kernel reports it (`Razer DeathAdder V2`) never matches: the lookup compares the stored key exactly. The wiki tells the user to copy the name from `hyprctl devices` (wiki-Keywords.md:79, hyprctl devices names) and documents that per-device options overwrite the `input` ones (wiki-Keywords.md:64-70, wiki override rule).

## Observations

**OBS** S316 (pin opened 2026-10-26): `const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");` at Hyprland-InputManager.cpp:1229 - the device value first, the global option as fallback.
**OBS** S317 (pin opened 2026-10-26): `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` at Hyprland-ConfigManager.cpp:1119 - a block value the user did not set does not shadow the global one.
**OBS** S318 (pin opened 2026-10-26): `MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",` at Hyprland-ConfigValues.cpp:272 - the built-in layout.
**OBS** S319 (pin opened 2026-10-26): `m_currentRules.layout = "us";` at Hyprland-IKeyboard.cpp:113 - the stored layout after a keymap that does not compile.
**OBS** S320 (pin opened 2026-10-26): `"defaultSpeed": {:.5f}, "scrollFactor": {:.2f}` at Hyprland-HyprCtl.cpp:769 (the quote spans two lines of the pin) - the pointer fields of the dump.
**OBS** S321 (pin opened 2026-10-26): `case ',': return '-';` at Hyprland-MiscFunctions.cpp:782 - commas in a device name become dashes too.
**OBS** S322 (pin opened 2026-10-26): `m_keymapOverridden = true;` at Hyprland-VirtualKeyboard.cpp:41 - set when a virtual keyboard's client sends its keymap.
**OBS** S323 (pin opened 2026-10-26): `std::string name = "hl-virtual-keyboard";` at Hyprland-protocols-VirtualKeyboard.cpp:12 - the name every virtual keyboard starts with.
**OBS** S324 (pin opened 2026-10-26): `special category's first value must be the key.` at hyprlang-config.cpp:435 - the error a `device` block without a leading `name` gets.
**OBS** S325 (pin opened 2026-10-26): `It's worth noting that ONLY values explicitly changed will be overwritten.` at wiki-Keywords.md:67 (the quote spans two lines of the pin) - the documented rule the set-by-user test implements.

Census of the pinned bytes:

hyprland input-device default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100 json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard

## Live host run (read-only)

On this host (Hyprland 0.56.2 at efb50993, one `input` block in `~/.config/hypr/input.conf`, no `device` block) the join reports nine keyboards AGREE on layout `br` with options `compose:caps`, the fcitx5 input method as VIRTUAL, and four pointers AGREE at -1.00 (receipt .ufo/waves/round-46/receipts/live-devices-host-l1.txt). The touchpad's `scroll_factor = 0.4` inside `input { touchpad { } }` is a global option and, as step 5 says, is not what the dump's field shows.

## Reading a DIFFER or a FALLBACK

- A keyboard that prints `us` and empty names while its config names something else most likely failed to compile its keymap (step 4); Hyprland also queues an error overlay naming the rejected names.
- A keyboard that prints other names than the config may have been changed at runtime with `hyprctl keyword`, or the config lives in a file not passed to the join, or a `source =` line the join does not follow.
- A device block that matches nothing was most likely written with the kernel product name instead of the normalized name (step 7).
- `hyprctl switchxkblayout` changes the active layout index, not the stored names, so it never turns AGREE into DIFFER.
- With `kb_file` set, an AGREE only says the stored names match; the keymap in use is the file's (step 4).

## Limits

- The XKB compile itself is not reproduced: whether a given layout/variant pair exists in xkeyboard-config is not checked; only the stored names are compared.
- `repeat_rate`, `repeat_delay`, `numlock_by_default`, `enabled`, `keybinds`, `sensitivity`, `accel_profile` and the libinput settings are applied per device too but the dump prints none of them (it prints lock state and libinput's default speed, which are different things); they are UNK for this join.
- Per-device layouts do not change the keymap binds are resolved against unless `resolve_binds_by_sym = 1` (wiki-Keywords.md:124-130); the join does not check binds.
- Variables, `{{ }}` expressions and hyprlang directives are not modelled (the tool reports NOT_COMPARED).
- The Lua config of later Hyprland releases is out of scope.
