# ScoutBindSurface — host Hyprland bind surface

Read-only walk of the operator session's config, the way Hyprland v0.56.2 follows `source`. No tool was built. No lane file was edited except this report. Nothing was installed.

Live compositor queried (read verbs only): instance `efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120`, `WAYLAND_DISPLAY=wayland-1` (the long-running session, pid 1614 from `hyprctl instances`). Not a nested oracle. `hyprctl version` is Hyprland 0.56.2 `efb50993780079460b0cbed1363e2166a2de1d9f`. `hyprctl configerrors` exited 0 and printed only two newline bytes.

**Derived bind count 192. `hyprctl binds -j | jq length` = 192. Equal.**

The 192 is the count of comment-stripped lines whose keyword is the `bind` handler (`bind` plus flag letters) in the source walk below. `unbind` = 0, `submap` = 0, no line was dropped. The live table matches that count and these shapes: mouse 2, keycode nonzero 42, `has_description` 190, locked 26, release 1, repeat 14, longPress 0, nonempty submap 0, catch_all 0, modmask 0 = 23, and the modmask histogram in the modifier section. Three (modmask, key, keycode) pairs are stored twice; Hyprland appends, it does not replace.

## How the walk was done

Root file: `/home/vgpnk/.config/hypr/hyprland.conf` (not a symlink; 1329 bytes, 32 physical lines).

Observed rules, not the counter's helper:

- Hyprland registers one handler, `bind`, with `allowFlags` (`ConfigManager.cpp:607`). `bindd`, `bindl`, `bindeld`, and the rest are that keyword plus flag letters (`handleBind`, flags at `:1516-1541`). `unbind` and `source` and `submap` are exact handlers (`:608`, `:614`, `:615`).
- `source` calls `absolutePath(rawpath, currentFile)` then `glob(..., GLOB_TILDE)` (`ConfigManager.cpp:1816`). `absolutePath` (`src/helpers/MiscFunctions.cpp:61-83` at the same commit) replaces a leading `~` with `getenv("HOME")` and joins any other non-absolute path to the current file's directory. Glob is glibc without `GLOB_NOSORT`, so matches come back `strcoll`-sorted. Only regular files are parsed. This walk called libc `glob` the same way.
- A `source` is followed immediately (depth-first) before the rest of the parent file. `m_configCurrentPath` is the file being parsed.
- hyprlang 0.6.8 `parseLine`: trim, a line whose first non-space is `#` is a comment (and may be a `# hyprlang` directive), a later `#` starts a trailing comment unless it is `##` (escaped to one `#`). Backslash-newline joins physical lines. This tree had no joined line and no `# hyprlang if`.
- Every `source` path in this tree is a literal `~/...`. None is relative. None contains `$`. The leading-`~` branch is the only path branch this tree hits.

One glob: `~/.local/state/omarchy/toggles/hypr/*.conf` resolves to `flags.conf`, then `window-no-gaps.conf`. No file is read twice. No cycle. 40 files.

## Ordered files read

Counts are comment-stripped logical lines. "other" is a `bind` keyword that is not exactly one of the single-flag names in the brief (`bindeld`, `bindld`, `bindmd`, `binddr`). Named variants not listed on a row are 0. Files with no row in the detail table contribute zeros for every count.

| # | File (under `/home/vgpnk`) | Why read |
|---|---|---|
| 1 | `.config/hypr/hyprland.conf` | root |
| 2 | `.local/share/omarchy/default/hypr/autostart.conf` | root:4 |
| 3 | `.local/share/omarchy/default/hypr/bindings/media.conf` | root:5 |
| 4 | `.local/share/omarchy/default/hypr/bindings/clipboard.conf` | root:6 |
| 5 | `.local/share/omarchy/default/hypr/bindings/tiling-v2.conf` | root:7 |
| 6 | `.local/share/omarchy/default/hypr/bindings/utilities.conf` | root:8 |
| 7 | `.local/share/omarchy/default/hypr/envs.conf` | root:9 |
| 8 | `.config/omarchy/current/theme/gum.env.conf` | envs.conf:3, between `# hyprlang noerror true` and `# hyprlang noerror false` |
| 9 | `.local/share/omarchy/default/hypr/looknfeel.conf` | root:10 |
| 10 | `.local/share/omarchy/default/hypr/input.conf` | root:11 |
| 11 | `.local/share/omarchy/default/hypr/windows.conf` | root:12 |
| 12 | `.local/share/omarchy/default/hypr/apps.conf` | windows.conf:12 |
| 13-30 | `apps/{1password,bitwarden,browser,hyprshot,jetbrains,localsend,pip,qemu,retroarch,steam,geforce,moonlight,system,telegram,typora,terminals,walker,webcam-overlay}.conf` | apps.conf:2-19, that order |
| 31 | `.config/omarchy/current/theme/hyprland.conf` | root:13 |
| 32 | `.config/hypr/monitors.conf` | root:16 |
| 33 | `.config/hypr/input.conf` | root:17 |
| 34 | `.config/hypr/bindings.conf` | root:18 |
| 35 | `.config/hypr/looknfeel.conf` | root:19 |
| 36 | `.config/hypr/autostart.conf` | root:20 |
| 37 | `.local/state/omarchy/toggles/hypr/flags.conf` | root:23 glob |
| 38 | `.local/state/omarchy/toggles/hypr/window-no-gaps.conf` | root:23 glob |
| 39 | `.config/hypr/ai-usage.conf` | root:29 |
| 40 | `.config/hypr/gkeep.conf` | root:32 |

`apps/davinci-resolve.conf` sits beside the sourced app files and is not in `apps.conf`. It is not read.

## Per-file counts

Zero on every axis, and omitted below: files 1-2, 7, 11-30, 32, 35-40. File 7 is not empty of structure: it has the two `# hyprlang noerror` lines and the `source` of file 8, but no bind, unbind, submap, `$var`, trailing comment, or `##`.

| File | bind | bindd | bindl | binde | bindm | bindr | bindo | bindn | bindt | bindi | bindc | bindg | bindu | bindk | bindx | other (exact) | unbind | submap | $var | trailing `#` | lines with `##` | keycode keys | mouse keys |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 3 media.conf | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 23 (`bindeld` 14, `bindld` 9) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4 clipboard.conf | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 tiling-v2.conf | 0 | 88 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 (`bindmd` 2) | 0 | 0 | 0 | 3 | 0 | 41 | 2 |
| 6 utilities.conf | 0 | 46 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 (`bindld` 1, `binddr` 1) | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| 8 gum.env.conf | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 116 | 0 | 0 |
| 9 default looknfeel.conf | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| 10 default input.conf | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| 31 theme hyprland.conf | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 33 user input.conf | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 34 user bindings.conf | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| **Total** | **0** | **163** | **2** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **27** | **0** | **0** | **3** | **7** | **117** | **42** | **2** |

Exact keyword histogram (the thing to parse): `bindd` 163, `bindeld` 14, `bindld` 10, `bindl` 2, `bindmd` 2, `binddr` 1. Sum 192.

Flag letters actually present: `d` 190, `l` 26, `e` 14, `m` 2, `r` 1. Absent from this tree: `a c g i k n o p s t u x`. So the single-name buckets `binde`, `bindm`, `bindr`, `bindo`, `bindn`, `bindt`, `bindi`, `bindc`, `bindg`, `bindu`, `bindk`, `bindx`, and plain `bind`, are all zero. Combinations are the real surface, and they land in "other" if the buckets are exact-match only.

`unbind`: none, including no `unbind = all`. `submap`: none.

## Modifier spellings

Space-separated tokens, as written. Empty means the mod field is empty (`bindeld = ,XF86...`), which is legal: mask 0. No `+`, no `_`, no lowercase, no `WIN`/`LOGO`/`META`/`MOD1`-`MOD5`/`CTRL` spelled `CONTROL`. Both `SUPER SHIFT ALT` and `SUPER ALT SHIFT` occur; `stringToModMask` is a substring test after `toupper`, so order does not matter. Counts below are bind lines plus the zero unbind lines.

| Spelling | Lines | Mask | Spelling | Lines | Mask |
|---|---:|---:|---|---:|---:|
| *(empty)* | 23 | 0 | `SUPER` | 42 | 64 |
| `SHIFT` | 2 | 1 | `SUPER SHIFT` | 37 | 65 |
| `ALT` | 7 | 8 | `SUPER CTRL` | 26 | 68 |
| `ALT SHIFT` | 2 | 9 | `SUPER SHIFT CTRL` | 3 | 69 |
| `CTRL ALT` | 2 | 12 | `SUPER ALT` | 19 | 72 |
| `CTRL ALT SHIFT` | 1 | 13 | `SUPER SHIFT ALT` | 20 | 73 |
| | | | `SUPER ALT SHIFT` | 2 | 73 |
| | | | `SUPER CTRL ALT` | 6 | 76 |

Sum of the `SUPER SHIFT ALT` and `SUPER ALT SHIFT` rows is 22, and live modmask 73 has 22 entries. Every other row matches the live modmask histogram one-for-one.

Per bind file:

- media.conf: empty 16, `SHIFT` 2, `ALT` 4, `SUPER` 1
- clipboard.conf: `SUPER` 3, `SUPER CTRL` 1
- tiling-v2.conf: `SUPER` 31, `CTRL ALT` 2, `SUPER CTRL` 4, `SUPER ALT` 16, `SUPER SHIFT` 17, `SUPER SHIFT ALT` 14, `ALT` 2, `ALT SHIFT` 2, `CTRL ALT SHIFT` 1, `SUPER ALT SHIFT` 1
- utilities.conf: `SUPER` 6, `SUPER CTRL` 21, `SUPER ALT` 2, `SUPER SHIFT` 4, empty 7, `SUPER SHIFT CTRL` 2, `SUPER SHIFT ALT` 1, `SUPER CTRL ALT` 6, `ALT` 1
- user bindings.conf: `SUPER` 1, `SUPER ALT` 1, `SUPER SHIFT` 16, `SUPER ALT SHIFT` 1, `SUPER SHIFT ALT` 5, `SUPER SHIFT CTRL` 1

## Keycode keys and mouse keys

No bare number key (the `parseKey` rule "all digits and value > 9"). Every keycode is `code:N`. Live table stores `key: ""` and `keycode: N`.

- tiling-v2.conf, 41 lines: `code:10`-`code:14` four times each, `code:15`-`code:19` three times each, `code:20` twice, `code:21` twice, `code:61` twice. Workspaces (`:22-31`, `:34-43`, `:46-55`), group windows (`:125-129`), resize (`:89-92`), monitor scale (`:132-133`).
- utilities.conf: one line, `:8`, `code:201` ("Omarchy menu").

Mouse, both `bindmd` in tiling-v2.conf:

- `:99` `SUPER, mouse:272` becomes live key `mouse:272`, dispatcher `mouse`, arg `movewindow`, description "Move window"
- `:100` `SUPER, mouse:273` becomes arg `resizewindow`, description "Resize window"

The config dispatcher (`movewindow` / `resizewindow`) is not the JSON dispatcher. Flag `m` rewrites the dispatcher to `mouse` and keeps the written dispatcher as the arg.

Other keys that are not keysyms and not keycodes: `switch:on:Lid Switch` and `switch:off:Lid Switch` (utilities.conf:34-35, `bindl`, empty mod, locked, no description). The key contains a space. Live `key` is the whole field `switch:on:Lid Switch`.

## Comments, hashes, variables

Trailing-comment lines (7). Three of them are binds; the comment is not part of the value:

- tiling-v2.conf:7 `bindd = SUPER, P, Pseudo window, pseudo, # dwindle` becomes live arg `""`, dispatcher `pseudo`
- tiling-v2.conf:89 `resizeactive, -100 0    # - key` becomes live arg `-100 0`, keycode 20
- tiling-v2.conf:90 same pattern, arg `100 0`, keycode 21
- default input.conf:11, :19, :20 and user input.conf:11 are input settings, not binds

Lines containing `##`: 117. 116 are in gum.env.conf, color values like `env = FOREGROUND,##bebebe` (hyprlang turns `##` into one `#`). The one in user bindings.conf is line 18, a full-line comment telling the reader to write `##` for a literal `#` in a URL. No sourced bind value uses `##`.

`$var` definitions in the walk (3), none of them on a bind:

- default looknfeel.conf:4 `$activeBorderColor = rgba(33ccffee) rgba(00ff99ee) 45deg`
- default looknfeel.conf:5 `$inactiveBorderColor = rgba(595959aa)`
- theme hyprland.conf:1 `$activeBorderColor = rgb(e68e0d)` (parsed later, so it overrides the first)

Sourced bind lines that contain `$` all use shell `$(...)` inside an `exec` arg (`$(date ...)`, `$(omarchy-battery-status)`, `$(hyprctl ...)`, `$(omarchy-cmd-terminal-cwd)`). No sourced bind uses a hyprlang `$name`. Same-named config variables do not apply to those args.

default looknfeel.conf:141 is a category `binds {` / `hide_special_on_workspace_change = true`, not a bind keyword. A startswith-`bind` scan of raw lines will false-hit it.

## Duplicates the table keeps

`addKeybind` appends. Three identities appear twice in `hyprctl binds -j`:

- modmask 0, key `F9`: utilities.conf:68 `bindd` "voxtype record start" (release false) and `:69` `binddr` "voxtype record stop" (release true). `removeKeybind` matches mod+key+keycode+catchAll and ignores release, so one `unbind` of that key would drop both.
- modmask 8 (`ALT`), key `TAB`: `cyclenext` and `bringactivetotop`
- modmask 9 (`ALT SHIFT`), key `TAB`: same pair

## Comma-bearing args

clipboard.conf `sendshortcut` lines keep commas in the last field. Live args: `CTRL, Insert, activewindow`, `SHIFT, Insert, activewindow`, `CTRL, X, activewindow`. Splitting every comma loses the dispatcher argument.

## Files under the four roots that this walk does not read

A grep of every `bind` under the roots over-counts. These have real bind lines and are not sourced from `hyprland.conf`:

| Path | Bind-like lines | Note |
|---|---:|---|
| `.local/share/omarchy/default/hypr/bindings/tiling.conf` | 50 | old tiling table; root sources `tiling-v2.conf` instead |
| `.local/share/omarchy/default/hypr/bindings.conf` | 10 | uses `$terminal`, `$fileManager`, `$browser`, `$music`, `$messenger`; not sourced |
| `.local/share/omarchy/default/hypr/plain-bindings.conf` | 7 | not sourced |

Also present and not read: `.config/hypr/{envs,hypridle,hyprlock,hyprsunset,xdph}.conf`, both `hyprland.conf.bak.*` and `autostart.conf.bak.*`, `apps/davinci-resolve.conf`, `default/hypr/toggles/*.conf`, theme `hyprlock.conf` (its five `$color` lines are not in the Hyprland walk). User `.config/hypr/envs.conf` is not the file Hyprland reads; the sourced envs file is the default one.

## Comparison

| | Walk | `hyprctl binds -j` |
|---|---:|---:|
| entries | 192 bind-keyword lines | 192 |
| mouse | 2 | 2 |
| keycode nonzero | 42 | 42 |
| has description (`d`) | 190 | 190 |
| locked (`l`) | 26 | 26 |
| release (`r`, and `c`/`g` which also set it) | 1 | 1 |
| repeat (`e`) | 14 | 14 |
| modmask 0 | 23 | 23 |
| unbind / submap | 0 / 0 | nonempty submap 0 |

`hyprctl configerrors`: exit 0, no error text.

## Unknowns

- Relative `source` paths, `~user`, a missing glob, a directory match, and `# hyprlang if` are not in this tree. The walk implements them as the sources above describe, but this host did not exercise them.
- Plugin dispatchers beyond `KeybindManager.cpp:42-112` are not on this surface. Every live dispatcher is in that list (`exec` 104, `workspace` 15, and the rest down to one each).
- Env-variable expansion at Hyprland start was not replayed. No sourced bind or source path needs a config `$name`. A `$NAME` that is also an environment variable would expand before `handleBind`; this tree does not show that case.
- `hyprctl` field equality was checked on the counts and the modmask histogram, plus the mouse, F9, pseudo, resize, switch, and sendshortcut rows. It was not a full 192-row multiset diff.

## Commands

```text
hyprctl version
hyprctl instances
hyprctl binds -j | jq length          # 192
hyprctl configerrors                  # exit 0, two newline bytes
```

The file walk was a Python libc `glob(GLOB_TILDE)` plus the `absolutePath` and hyprlang comment rules above, run against `HOME=/home/vgpnk`. Source files read for those rules (not written into the lane): Hyprland `efb50993` `src/config/legacy/ConfigManager.cpp` (already at `.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin`), `src/helpers/MiscFunctions.cpp`, `src/managers/KeybindManager.cpp`, and the hyprlang v0.6.8 tag tarball `src/config.cpp`.
