# C2 entry-draft sections (seat ScrEntryDraft, round 46)

Drop-in replacements for `.ufo/waves/round-46/l1-draft/entry.md`. Nothing here adds an `S###` id; no line names a cited
id; no fenced block is proposed for the entry (the command example is indented, so the entry's fence rule never sees it).

Merge map for the L1:

| block | replaces / inserts at | entry.md at freeze 8c5434c |
|---|---|---|
| R1 | `## Reading a DIFFER or a FALLBACK` and its four bullets | lines 59-65 |
| R2 | new section, inserted between the live-run paragraph and `## Reading a DIFFER` | after line 57 |
| R3 | `## Limits` and its four bullets | lines 66-71 |

R0 (optional, one line): line 57 says "one `input` block in `~/.config/hypr/input.conf`". The effective `input` block of
this host is split across two files (omarchy default at `~/.config/hypr/hyprland.conf:11`, host file at `:17`), so
"one `input` block" understates it. Suggested clause: "(the effective `input` block is split across two files, both
`source`d from `~/.config/hypr/hyprland.conf`; see *Running the join on this host*)".

R4 (optional, one locator in the live-run paragraph): the sentence "The touchpad's `scroll_factor = 0.4` inside
`input { touchpad { } }` is a global option..." has no locator of its own. Suggested wording, same claim: "is the global
`input:touchpad:scroll_factor` (Hyprland-ConfigValues.cpp:324)". Verifying that locator is part of `verify-locators.py`,
so the added token is checked like every other one; the line's existing verdict tokens stay inside the live receipt.

Locator discipline: every locator below is `<= 30` lines wide, every one is verified against the pinned bytes by
`verify-locators.py` in this directory (receipt `verify-locators.txt`: each locator's anchor is found by grep at a line
inside the cited range, ranges are checked for width and against the file length, and every locator that appears in this
file is required to appear in the table). Nothing outside these blocks needs to move: step 2's `hyprlang-config.cpp:885-899`
(special-key reset at the close), step 3's `Hyprland-InputManager.cpp:1270-1280` (did not change) and step 5's
`Hyprland-HyprCtl.cpp:785-802` (layout field) stay where they are — the new blocks add locators and delete none.

---

## R1

```markdown
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
```

## R2

```markdown
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
```

## R3

```markdown
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
```

---

## Why these three blocks (axis notes for the L1)

- Operability: R1 turns four hunches into an ordered decision list, each branch with the code path that produces it, so a
  reader can tell a config bug from a runtime leftover from a name mismatch without guessing. R2 gives the exact commands
  and the file set, and names the trap this host actually has (a split `input` block) rather than a generic one.
- Coverage: every new compositor claim carries a computed locator inside 30 lines. These blocks carry 39 distinct
  locators, 31 of them not yet in the entry at the freeze (the entry has 38 distinct; 8 are in common), all on surfaces
  the counter already scores (fallback, setKeymap, enabled gate, active_keymap, source handler, name compare), and none of
  them replaces an existing one.
- What R1 deliberately does not claim: that the join can see the compile, that a FALLBACK names its cause in the dump, or
  that `active_keymap` proves the keymap in use. Each of those is stated as a limit in R3 instead.
