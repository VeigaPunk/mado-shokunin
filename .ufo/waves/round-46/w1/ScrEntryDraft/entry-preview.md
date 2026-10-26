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
recheck: on-release - when `hyprctl version` leaves efb50993 or hyprlang leaves 0.6.8 (or 90d at the latest) re-pull the ten pins and re-run the counter; upstream main has moved to a Lua config, so a release past 0.56.x may drop the `device { }` block form this entry and tools/mado-devices.py describe
ground: input-device plane, runtime state agreement for keyboard XKB names and pointer scroll factors; per-device resolution was absent at base (claim grep exit 1); held neighbours: point readings of `input:kb_layout` in hyprctl-verification-layer.md and config-health-report-r3.md
Lane: mado-shokunin. Round: 46.

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| which value of `kb_layout`, `kb_variant`, `kb_options`, `kb_model`, `kb_rules`, `kb_file` a keyboard gets | the chain below, steps 1-4 | sourced at the host's revision |
| what `hyprctl devices -j` prints for a keyboard and a mouse | step 5 | sourced |
| why a keyboard can print `us` although the config says otherwise | step 4 | sourced; the compile failure itself is not observed here |
| whether this host's keyboards and mice agree with their config | the live run | observed 2026-10-26 |
| which keymap a virtual keyboard really uses | not answerable from the dump | UNK by design (step 6) |

## The chain, step by step

1. Parsing. The config language reads a file line by line; a line ending in a backslash is joined with the next one (continuation, hyprlang-config.cpp:44-66). A `#` starts a comment unless it is doubled: `##` is one literal `#` comment character (hyprlang-config.cpp:674-700). Inside a category, a key's full name is the category stack joined with `:`.
2. The `device` block is a keyed special category: Hyprland registers it with `name` as its key and 47 values (hyprlang special category, Hyprland-ConfigManager.cpp:518-540 registers the device block). Three spellings reach the same per-device store: `device { name = X ... }`, `device[X] { ... }` and `device[X]:key = value` (the bracket name is cut out of the key, hyprlang-config.cpp:291-320). A `device { }` block whose first assignment is not `name` is an error: the first value must be the key (hyprlang-config.cpp:420-440 reports "first value must be the key"). The current device is forgotten when the last category closes (reset at the close, hyprlang-config.cpp:885-899), so a flat `device:kb_layout = x` outside a block has no device to land on.
3. Per-keyboard lookup. For every keyboard, applyConfigToKeyboard reads six keymap names per device (Hyprland-InputManager.cpp:1213-1238, applyConfigToKeyboard): for example the kb_layout lookup asks the device first and the global option second (Hyprland-InputManager.cpp:1226-1231, kb_layout and its siblings). The device value counts only when the user set it; otherwise the global fallback applies (Hyprland-ConfigManager.cpp:1115-1123, set-by-user test then global fallback). The block exists when one carries the keyboard's exact name (Hyprland-ConfigManager.cpp:1196-1201, deviceConfigExists), and a stored `[[EMPTY]]` reads as the empty string (Hyprland-ConfigManager.cpp:1156-1168, STRVAL_EMPTY marker). The global defaults are `us` for the layout and empty for the rest (Hyprland-ConfigValues.cpp:271-276, default XKB names). When nothing changed since the last apply, the keyboard is skipped (Hyprland-InputManager.cpp:1270-1280, did not change).
4. Compiling. The five names go to setKeymap as the keyboard's current rules (Hyprland-InputManager.cpp:1282-1295, setKeymap with the names). A non-empty kb_file is tried first (Hyprland-IKeyboard.cpp:87-96, kb_file read before the names). If no keymap compiles, the stored rules are reset and the keyboard falls back to layout `us` with every other name empty (Hyprland-IKeyboard.cpp:101-116, fallback to us after an error overlay), which is why a typo in `kb_layout` shows up in the dump as `us`, not as the typo.
5. What the dump shows. `hyprctl devices -j` prints the stored rules of each keyboard - rules, model, layout, variant, options - and for each pointer a `scrollFactor` with two decimals (Hyprland-HyprCtl.cpp:765-772, scrollFactor field; Hyprland-HyprCtl.cpp:785-802, layout and the other stored names). A pointer's factor is the device block's `scroll_factor` clamped to 0..100 only when that block explicitly sets it (Hyprland-InputManager.cpp:1376-1383, scroll_factor explicitly set), and is otherwise unset, printed as -1 (Hyprland-InputManager.cpp:1379-1383, nullopt branch). The global `input:scroll_factor` therefore never reaches the printed field (Hyprland-ConfigValues.cpp:290-300, input:scroll_factor is a separate global option), and neither does `input:touchpad:scroll_factor`.
6. Virtual keyboards. A virtual keyboard (an input method such as fcitx5) is named `hl-virtual-keyboard` plus its process name (Hyprland-protocols-VirtualKeyboard.cpp:11-30, hl-virtual-keyboard naming). When its client sends a keymap the keyboard marks the keymap overridden (Hyprland-VirtualKeyboard.cpp:36-44, virtual keyboard override flag), and setKeymap then returns early (Hyprland-IKeyboard.cpp:60-64, keymap overridden early return), so the rules the dump prints for it are the config's names at creation, not a witness of the keymap in use.
7. Names. A device's name is lower-cased with space, newline and comma replaced by `-` (Hyprland-MiscFunctions.cpp:777-789, lower-case name normalizer), and a duplicate gets a `-1`, `-2` suffix (Hyprland-InputManager.cpp:2119-2131, duplicate suffix). A block written with the product name as the kernel reports it (`Razer DeathAdder V2`) never matches: the lookup compares the stored key exactly. The wiki tells the user to copy the name from `hyprctl devices` (wiki-Keywords.md:79, hyprctl devices names) and documents that per-device options overwrite the `input` ones (wiki-Keywords.md:64-70, wiki override rule).

## Observations

**OBS** S316 (pin opened 2026-10-26): `const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");` at Hyprland-InputManager.cpp:1229 - the device value first, the global option as fallback.
**OBS** S317 (pin opened 2026-10-26): `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` at Hyprland-ConfigManager.cpp:1119 - a block value the user did not set does not shadow the global one.
**OBS** S318 (pin opened 2026-10-26): `MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",` at Hyprland-ConfigValues.cpp:272 - the built-in layout.
**OBS** S319 (pin opened 2026-10-26): `m_currentRules.layout = "us";` at Hyprland-IKeyboard.cpp:113 - the stored layout after a keymap that does not compile.
**OBS** S320 (pin opened 2026-10-26): `"defaultSpeed": {:.5f}, "scrollFactor": {:.2f}` at Hyprland-HyprCtl.cpp:769 - the pointer fields of the dump.
**OBS** S321 (pin opened 2026-10-26): `case ',': return '-';` at Hyprland-MiscFunctions.cpp:782 - commas in a device name become dashes too.
**OBS** S322 (pin opened 2026-10-26): `m_keymapOverridden = true;` at Hyprland-VirtualKeyboard.cpp:41 - set when a virtual keyboard's client sends its keymap.
**OBS** S323 (pin opened 2026-10-26): `std::string name = "hl-virtual-keyboard";` at Hyprland-protocols-VirtualKeyboard.cpp:12 - the name every virtual keyboard starts with.
**OBS** S324 (pin opened 2026-10-26): `special category's first value must be the key.` at hyprlang-config.cpp:435 - the error a `device` block without a leading `name` gets.
**OBS** S325 (pin opened 2026-10-26): `It's worth noting that ONLY values explicitly changed will be overwritten.` at wiki-Keywords.md:67 - the documented rule the set-by-user test implements.

Census of the pinned bytes:

hyprland input-device default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100 json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard

## Live host run (read-only)

On this host (Hyprland 0.56.2 at efb50993, one `input` block in `~/.config/hypr/input.conf`, no `device` block) the join reports nine keyboards AGREE on layout `br` with options `compose:caps`, the fcitx5 input method as VIRTUAL, and four pointers AGREE at -1.00 (receipt .ufo/waves/round-46/receipts/live-devices-host-l1.txt). The touchpad's `scroll_factor = 0.4` inside `input { touchpad { } }` is a global option and, as step 5 says, is not what the dump's field shows.

## Running the join on this host

Two read-only steps: `hyprctl devices -j` asks the running compositor for the JSON dump, and the join reads that dump and
the config files and nothing else - it starts no process and opens no socket of its own (mado-devices.py:22-26, the usage
lines and the I/O contract).

    hyprctl devices -j > /fast/scratch/mado-r46-devs.json
    python3 tools/mado-devices.py --devices /fast/scratch/mado-r46-devs.json \
        --config ~/.local/share/omarchy/default/hypr/input.conf --config ~/.config/hypr/input.conf

The same join on a pipe: `hyprctl devices -j | python3 tools/mado-devices.py --devices - --config <file> ...`. `--selftest`
alone runs the tool's own cases. The exit code is the verdict - 0 OK, 1 DIFFER, 3 NO_KEYBOARDS, 4 STALE_BLOCK,
5 NOT_COMPARED, tested in that order - and one line per keyboard, per pointer and per device block precedes the summary
line (mado-devices.py:87-89, the verdict table). Do not answer a DIFFER with `hyprctl keyword` or `hyprctl reload`: both
mutate the compositor, and the join needs neither.

Pass the files, not the entry point. On this host `~/.config/hypr/hyprland.conf` holds no `input` and no `device` block;
it `source`s them, and the `input` block the keyboards actually use is split - the omarchy default, sourced at
`~/.config/hypr/hyprland.conf:11`, sets all five keyboard names, and the host's own file, sourced at
`~/.config/hypr/hyprland.conf:17`, overrides two of them. A join that passes only the second file still reaches the other
three, from the built-in default rather than from the file that set them; here both files leave them empty, so the live
verdict above is right by value, and it would be wrong the moment the default file set a variant.

A glob (`~/.config/hypr/hyprland.conf:23` sources `hypr/*.conf`) is not expanded by the join, and a `$` variable or
`{{ }}` expression on a relevant line raises the verdict to NOT_COMPARED instead of guessing (mado-devices.py:48-50, the
relevance test and the unsupported counter). Keep the dump in scratch: it carries device names and process addresses.

## Reading a DIFFER or a FALLBACK

Decide in this order.

**FALLBACK** means the names the config asked for did not compile. When no keymap is built the keyboard queues an error
overlay that repeats the five names, logs them, and replaces its stored rules with layout `us` and four empty names -
the exact quintuple the dump then prints (Hyprland-IKeyboard.cpp:101-116, the failed-compile reset;
Hyprland-IKeyboard.cpp:102-103, the overlay text). Two consequences. A config that really asks for `us` and nothing else
AGREEs, because agreement is tested before the fallback shape (mado-devices.py:71-73, the verdict order), so a FALLBACK
is never the config itself. And a runtime `hyprctl keyword device:<name>:kb_layout us` produces the same quintuple with no
failed compile at all, because a keyword is parsed as one config line (Hyprland-HyprCtl.cpp:1188-1192, the keyword to
parseKeyword hop).

**DIFFER** has four mechanisms; rule them out from cheapest to most expensive.

1. A stale runtime value. `hyprctl keyword` builds a config line out of its two arguments and parses it in place, so the
   value lives in the parsed store and never returns to the file (Hyprland-HyprCtl.cpp:1188-1192; hyprlang-config.cpp:1064-1068,
   parseDynamic). A command containing `device` or `input` re-applies every keyboard and pointer at once, which is why the
   dump follows the keyword while the file does not (Hyprland-HyprCtl.cpp:1203-1208, the post-keyword re-apply). A full
   parse resets the values to their defaults before it reads the files, so a `hyprctl reload` clears those dynamic values
   and re-applies after (hyprlang-config.cpp:915-926, parse and its clearState; Hyprland-ConfigManager.cpp:726-751, reload;
   Hyprland-ConfigManager.cpp:970-980, postConfigReload). A DIFFER that survives a reload is not a leftover keyword; the
   join itself reloads nothing.
2. A file the join never saw. `source` is a Hyprland handler rather than a hyprlang builtin: it expands the path with glob
   and parses every regular file it matched at the point the line appears (Hyprland-ConfigManager.cpp:614, the handler
   registration; Hyprland-ConfigManager.cpp:1816-1841, glob then parseFile). The join neither expands `source` nor counts
   it as unsupported - `source` is neither a `device` nor an `input:kb_*` key - so the sourced block is simply absent from
   the expectation, which then falls to the global option or the built-in default. Pass every sourced file, in source order
   (mado-devices.py:36, files read in argument order).
3. A block whose name the compositor never uses. The value lookup compares the block's stored name with the device's
   internal name character for character, and that name is the lower-cased kernel name with space, newline and comma turned
   into `-` (hyprlang-config.cpp:1083-1099, the exact key compare; Hyprland-MiscFunctions.cpp:777-789, the normalizer), a
   duplicate getting a `-1` or `-2` suffix (Hyprland-InputManager.cpp:2119-2131, the suffix). A block written as the
   product name reports NO_SUCH_DEVICE; note that the existence test maps spaces to dashes as well, so a name with spaces
   can be found by one lookup and missed by the other (Hyprland-ConfigManager.cpp:1196-1201, deviceConfigExists).
4. A name that only looks right. `kb_file` compiles a file before the five names are tried, so an AGREE there says the
   names match, not that the file exists or compiled; an unreadable file is logged and the names are tried after it
   (Hyprland-IKeyboard.cpp:87-99, kb_file first, names second).

**AGREE with something odd-looking.** `enabled = 0` in a device block is read per device and stored on the keyboard, yet it
can never produce a DIFFER: the dump prints no `enabled` field, only the stored names, so a disabled keyboard reports its
names as usual and instead stops delivering keys and modifiers (Hyprland-InputManager.cpp:1233-1240, the enabled read;
Hyprland-HyprCtl.cpp:785-798, the printed fields; Hyprland-InputManager.cpp:1619-1621 and Hyprland-InputManager.cpp:1685-1688,
the gates that drop its events). `hyprctl switchxkblayout` likewise moves only the active layout index, which changes
`active_layout_index` and `active_keymap` - two fields the join does not read - and leaves the five names alone
(Hyprland-HyprCtl.cpp:1368-1396, the layout index switch).

## Limits

- The compile is not reproduced. Nothing here checks that a layout/variant pair exists in xkeyboard-config, and no keymap
  is built: the join compares the names handed to setKeymap with the names the dump prints, and only FALLBACK licenses the
  inference that they did not compile (Hyprland-IKeyboard.cpp:98-116, the compile and its reset). A name that xkb accepts
  but mangles is invisible.
- The five names are the request, not a readback. setKeymap stores them before it compiles, behind the overridden-keymap
  return and ahead of the `kb_file` branch, so a keyboard whose keymap came from a file or from a virtual keyboard's client
  prints names that describe what was asked for (Hyprland-IKeyboard.cpp:60-66, the override return and the assignment;
  Hyprland-IKeyboard.cpp:87-96, the file branch). The one field read out of the compiled keymap is `active_keymap`, and the
  join does not compare it (Hyprland-HyprCtl.cpp:781-794, active_layout_index and active_keymap;
  Hyprland-IKeyboard.cpp:306-321, the layout name taken from the keymap).
- Everything a device block can set that the dump does not print stays UNK for this join: `enabled`, `keybinds`, `tags`,
  `repeat_rate`, `repeat_delay`, `numlock_by_default`, `sensitivity`, `accel_profile`, `rotation`, the libinput switches and
  the touchpad sub-block (Hyprland-InputManager.cpp:1233-1238, those read in applyConfigToKeyboard;
  Hyprland-HyprCtl.cpp:785-798, those actually printed). An option can change how the device behaves and change nothing in
  the comparison.
- A pointer's scroll factor is compared only where its block sets it. The global `input:scroll_factor` and
  `input:touchpad:scroll_factor` are separate options that never reach the printed field, so their effect lies outside this
  comparison (Hyprland-InputManager.cpp:1379-1382, the explicitly-set test and the unset branch;
  Hyprland-ConfigValues.cpp:296, the global option).
- The config language is modelled only as far as the steps above describe. A `$` variable or a `{{ }}` expression on a
  relevant line, and any line starting with `#` that matches `#[ \t]*hyprlang`, each add to the unsupported count, which
  turns the verdict into NOT_COMPARED instead of a guess (mado-devices.py:39-42, the comment and directive rules;
  mado-devices.py:48-50, relevance). That is a recognised-form counter, not a parser: a directive spelled outside that
  form is not reported, and the branch it guards is read as if it were active. A `source =` line is ignored silently, so a
  file left out is a gap in the expectation, not a warning.
- A `scroll_factor` is compared as a number only when it spells a decimal. The C library's number grammar is not
  reproduced: inf, nan, a hex float, an infinite result or a denormal magnitude counts as unsupported, so a block that
  spells the value that way raises NOT_COMPARED rather than a verdict (mado-devices.py:62-66, the value rule), while
  Hyprland hands the string to `std::stof` and clamps the result (hyprlang-config.cpp:465-471, the float parse;
  Hyprland-InputManager.cpp:1379-1382, the explicitly-set test and the clamp). Whether a given spelling survives `std::stof`
  is not checked here; the join cannot overstate agreement on it, only decline to compare.
- A missing file leaves no trace in the result: an expectation that fell to the global option or the built-in default can
  agree with a dump that a device block would have contradicted.
- The rejected names behind a FALLBACK live in the compositor's log and its error overlay; this join reads neither and
  starts no process (Hyprland-IKeyboard.cpp:102-106, the queueError and the log line).
- The Lua config and the non-legacy parser are out of scope: `hyprctl keyword` refuses on a non-legacy parser, so the
  reproduction path in *Reading a DIFFER or a FALLBACK* stops at the 0.56.x line (Hyprland-HyprCtl.cpp:1160-1163, the parser
  guard).
- The join's own output is shape-only - names, numbers, verdicts - but the dump it reads carries device names and process
  addresses; keep both in scratch and cite only what a receipt already holds.
