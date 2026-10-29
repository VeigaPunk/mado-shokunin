# Keybind & window-rule semantics — declared plane decision tables (MADO-4; assignment MADO-R2-2)

Probe window: 2026-10-14 13:40–13:56 UTC (host offset −03:00, user `vgpnk`).
Substrates read-only: `~/.config/hypr/`, `~/.local/share/omarchy/default/hypr/`,
`~/.config/omarchy/current/theme/hyprland.conf`. Scratch only under `/tmp/mado-r2-2-probe/`
(`binds.json` snapshot, `reconcile2.py`). Nothing outside this repo and `/tmp` was written;
no compositor state was mutated.
Version pin: Hyprland 0.56.2 (`hyprctl version`, commit `efb50993780079460b0cbed1363e2166a2de1d9f`).

**Tag legend** — `[OBS]` measured directly (file bytes, command output) · `[INF-docs]`
inference from Hyprland documentation, fetched 2026-10-14 — **not runtime-verified by this
lane** · `[INF]` composite inference from measured parts, with docs cited where semantics
are invoked · `[UNK]` unknown.

**Claim boundary.** The lane ran no keystroke injection, no `hyprctl dispatch`, and mutated
nothing. "Verified against the docs" means exactly `[INF-docs]`; the only runtime checks are
read-only `hyprctl` queries (`binds`, `clients`, `getoption`), which verify how the host's
**parser** interpreted declared binds (fields, modmask, flags) and the live tag state — not
what a dispatcher does when fired.

Docs fetched (all 2026-10-14):
- Binds — <https://wiki.hypr.land/Configuring/Binds/>
- Window Rules — <https://wiki.hypr.land/Configuring/Window-Rules/>
- Dispatchers — <https://wiki.hypr.land/Configuring/Dispatchers/>
- Dwindle Layout — <https://wiki.hypr.land/Configuring/Layouts/Dwindle-Layout/>
- Variables (current) — <https://wiki.hypr.land/Configuring/Basics/Variables/>
- 0.54 archive (closest era): Binds / Window-Rules / Variables —
  <https://wiki.hypr.land/0.54.0/Configuring/Binds/>, `.../Window-Rules/`, `.../Variables/`

**Docs-drift caveat `[OBS]`.** The current Variables page carries the banner "Since Hyprland
0.55, hyprlang is deprecated in favor of lua" and lua-era examples; the host still parses
hyprlang configs cleanly (`hyprctl configerrors` empty, all binds parse — §1). The current
Binds/Window-Rules/Dispatchers pages still document the hyprlang forms used here, and the
0.54 archive matches them on every point used below; the classic **mod list survives only in
the 0.54 archive**. Residual drift risk carried in §6.2.

---

## 1. Declared keybind surface `[OBS]`

Five sourced files carry all 192 effective binds; the arithmetic closes exactly against
`hyprctl binds -j` (= 192), including per-dispatcher and per-flag counts.

| Source | binds | flag letters present | sha256 (16) | lines |
|---|---|---|---|---|
| `~/.config/hypr/bindings.conf` (local, L2–28) | 25 | d×25 | `e574a1ed08535e31` | 40 |
| `default/hypr/bindings/media.conf` | 23 | e×14, l×23, d×23 | `8d21d57e9d982b01` | 30 |
| `default/hypr/bindings/clipboard.conf` | 4 | d×4 | `19ca281aae91a7db` | 5 |
| `default/hypr/bindings/tiling-v2.conf` | 90 | d×90, m×2 | `0cca56696969a0f3` | 133 |
| `default/hypr/bindings/utilities.conf` | 50 | d×48, l×3, r×1 | `57ddb3045f81d693` | 76 |
| **sum** | **192** | | | |

`[OBS]` Live cross-check (`hyprctl binds -j`): flag counts `has_description` 190, `repeat` 14,
`locked` 26, `mouse` 2, `release` 1 — identical to the file-letter sums (d 190, e 14, l 26,
m 2, r 1). `submap` is `""` on all 192 (no submaps in the plane). `catch_all` 0.
`[OBS]` Full reconciliation: for each declared bind line, a predicted modmask (from the mod
string, §2.2) was matched against a live JSON entry on key/keycode + dispatcher + arg —
**192/192 matched, 0 unmatched, 0 unused live entries** (scratch `reconcile2.py`; method in §5).
`[OBS]` No active `unbind` in the plane — the only occurrence is commented
(`bindings.conf:34`); the stock deprecated `default/hypr/bindings.conf` is not sourced
(MADO-1 §4). `[INF-docs]` `unbind` key matching is case-sensitive.

## 2. Modifier grammar — decision table

### 2.1 Docs grammar `[INF-docs]`
- Form: `bind = MODS, key, dispatcher, params`; description flag moves the description in
  front of the dispatcher: `bindd = MODS, key, description, dispatcher, params`; mouse binds
  take one less arg. Empty MODS is legal (`bind = , PRINT, …`, `utilities.conf:38`).
- MOD is a "string modmask"; **any separators are allowed except `,`** — so `SUPER SHIFT`,
  `SUPER_SHIFT`, `SUPER+SHIFT` are the same thing; mod order is not significant.
  Mod list (0.54 archive; absent from the current page): `SHIFT CAPS CTRL/CONTROL ALT MOD2
  MOD3 SUPER/WIN/LOGO/MOD4 MOD5`.
- Comma rule: the fixed fields are comma-separated, but a dispatcher's `params` may itself
  contain commas (`sendshortcut` — measured live arg `CTRL, Insert, activewindow`). A trailing
  comma means an intentionally empty `params` (used widely here, e.g. `tiling-v2.conf:2`).

### 2.2 Measured modmask decode `[OBS]`
Derived by matching all 192 predicted masks to live `modmask` values (0 mismatches); bit
names from the docs mod list `[INF-docs]`.

| modmask | declared string(s) | bit meaning | live count |
|---|---|---|---|
| 0 | *(empty)* | none | 23 |
| 1 | `SHIFT` | SHIFT | 2 |
| 8 | `ALT` | ALT | 7 |
| 9 | `ALT SHIFT` | ALT+SHIFT | 2 |
| 12 | `CTRL ALT` | CTRL+ALT | 2 |
| 13 | `CTRL ALT SHIFT` | CTRL+ALT+SHIFT | 1 |
| 64 | `SUPER` | SUPER (mod4) | 42 |
| 65 | `SUPER SHIFT` | SUPER+SHIFT | 37 |
| 68 | `SUPER CTRL` | SUPER+CTRL | 26 |
| 69 | `SUPER SHIFT CTRL` | SUPER+CTRL+SHIFT | 3 |
| 72 | `SUPER ALT` | SUPER+ALT | 19 |
| 73 | `SUPER ALT SHIFT`, `SUPER SHIFT ALT` | SUPER+ALT+SHIFT | 22 |
| 76 | `SUPER CTRL ALT` | SUPER+CTRL+ALT | 6 |

`[OBS]` Both modifier orderings (`tiling-v2.conf:46` `SUPER SHIFT ALT` and
`tiling-v2.conf:114` `SUPER ALT SHIFT`) parse to the same mask 73 — order-insensitivity
measured, not just recited. No live bind uses CAPS / MOD2 / MOD3 / MOD5. Bit values
1=SHIFT, 4=CTRL, 8=ALT, 64=SUPER are measured; CAPS/MOD2/MOD3/MOD5 bit positions remain
`[UNK]` (no live sample).

### 2.3 Key field forms in the plane `[OBS]` (+ `[INF-docs]` semantics)
| Form | Declared examples (anchors) | Note |
|---|---|---|
| Named keysym | `RETURN`, `F`, `SLASH`, `PERIOD`, `COMMA`, `BACKSPACE`, `TAB`, `ESCAPE`, `DELETE`, `PRINT`, `F9`, `LEFT/RIGHT/UP/DOWN`, `SPACE` | `[INF-docs]` use the segment after `XKB_KEY_` |
| XF86 media/switch keys | `media.conf:2-29` (`XF86Audio*`, `XF86MonBrightness*`), `utilities.conf:10,12` (`XF86PowerOff`, `XF86Calculator`) | press-locked/repeat flags in §2.4 |
| Keycode | `code:10`–`code:19` (digits), `code:20,21` (minus/equal), `code:61` (slash), `code:201` (`utilities.conf:8`) | `[OBS]` live JSON: `key:""`, `keycode: N` |
| Wheel | `mouse_up`, `mouse_down` (`tiling-v2.conf:95,96,121,122`) | `[INF-docs]` reset time `binds:scroll_event_delay` = 300 live |
| Switch | `switch:on:Lid Switch`, `switch:off:Lid Switch` (`utilities.conf:34-35`) | `[INF-docs]` triggers when switch turns on/off |
| Mouse button | `mouse:272`, `mouse:273` with `m` flag (`tiling-v2.conf:99-100`) | `[OBS]` live: dispatcher reported as `mouse`, arg `movewindow`/`resizewindow` |

### 2.4 Flags used in the plane `[INF-docs]` semantics, `[OBS]` counts
| Flag | Meaning (docs) | Where declared | Live count |
|---|---|---|---|
| `d` | has description; description precedes dispatcher, must not contain commas | all files | 190 |
| `l` | locked — fires even while an input inhibitor (lockscreen) is active | all 23 media binds; `utilities.conf:10,34,35` | 26 |
| `e` | repeat — re-fires while held | media `bindeld` lines (14) | 14 |
| `r` | release — fires on key release | `utilities.conf:69` (F9 push-to-talk stop) | 1 |
| `m` | mouse | `tiling-v2.conf:99-100` | 2 |
| `c,g,o,n,t,i,s,p,u,k` | click/drag/long-press/non-consuming/transparent/ignore-mods/separate/bypass/submap-universal/per-device | not used | 0 each |

### 2.5 Multiple actions on one key `[OBS]` + `[INF-docs]`
- `tiling-v2.conf:79-82`: `ALT, TAB` = `cyclenext` + `bringactivetotop`; `ALT SHIFT, TAB` =
  `cyclenext prev` + `bringactivetotop`. Live JSON holds both entries per key; docs: binds
  "will be executed top to bottom, in the order they were written in".
- `utilities.conf:68-69`: F9 pair — press (`bindd`) starts dictation, release (`binddr`)
  stops it; distinguished by the `r` flag, not by duplicate firing.
- No keysym-combo (`s`), submap, catch-all, or per-device binds anywhere in the plane
  (`[OBS]` JSON: `submap:""` ×192, `catch_all:0`; no `s` flag in any of the five files —
  `&` occurs only in an exec arg (`utilities.conf:34` `&&`) and a description
  (`tiling-v2.conf:12` "(float & pin)"), never in a key field).

## 3. Dispatcher inventory — per-dispatcher semantics (24 live) `[OBS]` counts, `[INF-docs]` semantics

Counts are live `hyprctl binds -j` values; each equals the declared-file count exactly
(per-dispatcher reconciliation in §1). Semantics are quoted/paraphrased from the Dispatchers
page unless another page is named; **none were fired by this lane.**

| Dispatcher | n | Declared forms (anchors) | Semantics `[INF-docs]` |
|---|---|---|---|
| `exec` | 104 | 5 files; e.g. `bindings.conf:2` terminal, `utilities.conf:72-73` zoom (`hyprctl keyword cursor:zoom_factor …`) | executes a shell command; supports `[rules…] command` prefix (not used in plane) |
| `workspace` | 15 | `tiling-v2.conf:22-31` `1..10`; `:62` `e+1`, `:63` `e-1`, `:64` `previous`; `:95-96` wheel `e+1/e-1` | changes the workspace; args: id 1–2147483647, relative `+n/-n`, `e±n` open-relative, `previous` |
| `changegroupactive` | 11 | `tiling-v2.conf:113` `f`, `:114` `b`, `:117-118` `b/f`, `:121-122` scroll, `:125-129` `1..5` | switch window in a group: `b` back, `f` forward, or index (1-based) |
| `movetoworkspacesilent` | 11 | `tiling-v2.conf:46-55` `1..10`, `:59` `special:scratchpad` | like `movetoworkspace` but does not follow; `special` form supported here |
| `movetoworkspace` | 10 | `tiling-v2.conf:34-43` `1..10` | moves the focused window to a workspace |
| `movecurrentworkspacetomonitor` | 4 | `tiling-v2.conf:67-70` `l/r/u/d` | moves the active workspace to a monitor (monitor = direction/id/name/current/relative) |
| `movefocus` | 4 | `tiling-v2.conf:16-19` `l/r/u/d` | moves focus in a direction |
| `moveintogroup` | 4 | `tiling-v2.conf:107-110` `l/r/u/d` | moves active window into a group in direction; no-op if none |
| `resizeactive` | 4 | `tiling-v2.conf:89-92` `-100 0` etc. | resizes the active window; resizeparams = pixel delta / `%` / `exact` |
| `swapwindow` | 4 | `tiling-v2.conf:73-76` `l/r/u/d` | swaps the active window with the window in direction |
| `sendshortcut` | 3 | `clipboard.conf:2-4` args `CTRL, Insert, activewindow` / `SHIFT, Insert, activewindow` / `CTRL, X, activewindow` | sends mods+key to an optionally specified window (`window` = class regex / `activewindow` / …); docs warn XWayland pass-through is "wonky" |
| `bringactivetotop` | 2 | `tiling-v2.conf:81-82` | **deprecated** in favor of `alterzorder`; brings current window to top of stack |
| `cyclenext` | 2 | `tiling-v2.conf:79` (empty), `:80` `prev` | focuses the next window (args: empty=next, `prev`, plus `tiled/floating/visible/hist` modifiers) |
| `focusmonitor` | 2 | `tiling-v2.conf:85` `+1`, `:86` `-1` | focuses a monitor (relative values allowed) |
| `fullscreen` | 2 | `tiling-v2.conf:9` `0`, `:11` `1` | sets fullscreen mode: `0` fullscreen (whole screen), `1` maximize (keeps gaps/bar); action defaults to `toggle` |
| `mouse` | 2 | `tiling-v2.conf:99-100` (`bindmd`) | `[OBS]` hyprctl's representation of mouse binds; underlying functions are `movewindow` / `resizewindow` (moves/resizes the active window on drag) |
| `fullscreenstate` | 1 | `tiling-v2.conf:10` `0 2` | sets internal and client fullscreen state: internal `0` none, client `2` fullscreen; docs example "keeps the window non-fullscreen, but the client goes into fullscreen mode within the window" |
| `killactive` | 1 | `tiling-v2.conf:2` | closes (not kills) the active window |
| `layoutmsg` | 1 | `tiling-v2.conf:6` `togglesplit` | layout-specific dispatcher (main page defers to layout pages); Dwindle: `togglesplit` toggles the current window's split — **requires `preserve_split`**, measured on (`hyprctl getoption dwindle:preserve_split` → `int: 1`, `set: true`; `default/hypr/looknfeel.conf:110-111`) |
| `moveoutofgroup` | 1 | `tiling-v2.conf:104` | moves the active window out of a group; no-op if not in one |
| `pseudo` | 1 | `tiling-v2.conf:7` | Dwindle: toggles the window's pseudo mode |
| `togglefloating` | 1 | `tiling-v2.conf:8` | toggles the current window's floating state |
| `togglegroup` | 1 | `tiling-v2.conf:103` | toggles the current active window into a group |
| `togglespecialworkspace` | 1 | `tiling-v2.conf:58` `scratchpad` | toggles a special workspace; name must be a special workspace's name |

`[INF-docs]` Related machinery *not* declared (kept for completeness): `pass`/`global`
(global keybinds), `execr`, `submap`, `alterzorder`, `setprop` — none appear in the plane.

## 4. Window-rule semantics

### 4.1 Syntax and rule categories `[INF-docs]` + `[OBS]`
- Anonymous form used everywhere here: `windowrule = [effects…, props…]` with props being
  `match:*` fields; named blocks (`windowrule { name = …; match:class = …; effect = … }`)
  appear exactly 3 times in the plane (`jetbrains.conf:2`, `geforce.conf:1`,
  `moonlight.conf:1`). Props and effects may be in any order (`typora.conf:2` puts props
  first, then `float on, center on`); **all props must match**; exactly one of each `match:`
  type per rule; at least one prop required.
- Era pin `[OBS]`: `default/hypr/windows.conf:2` labels the stock rules "Hyprland 0.53+
  syntax"; the 0.54 archive and current wiki document the same anonymous/named syntax.
- Regex `[INF-docs]`: Google RE2; `negative:` prefix negates.

### 4.2 Effective evaluation order in this plane `[OBS]` order + `[INF-docs]` semantics
Written order (measured through the include graph, MADO-1 §3; docs: "Rules are evaluated top
to bottom, so the order they're written in does matter!"):

1. `windows.conf:3` `suppress_event maximize, match:class .*`
2. `windows.conf:6` `tag +default-opacity, match:class .*`
3. `windows.conf:9` `no_focus on` (6 props: empty class/title + xwayland/float/fullscreen/pin)
4. `windows.conf:12` sources `apps.conf:2-19` → 18 app files in listed order
   (69 rule statements; `apps/davinci-resolve.conf` exists but is **not sourced** — orphan
   excluded from the live plane)
5. `windows.conf:15` `opacity 0.97 0.9, match:tag default-opacity`
6. `input.conf:45-46` (sourced `hyprland.conf:17`, user layer): `scroll_touchpad 1.5` /
   `0.2`
7. `ai-usage.conf:2-5` (sourced last, `hyprland.conf:29`): tag/float/center/size for
   `^(org.omarchy.ai-usage)$`

Totals `[OBS]`: 79 sourced rule statements = 4 (windows.conf) + 69 (sourced app files) + 2
(local input.conf) + 4 (ai-usage.conf); 3 of them named. `input.conf` sha256 `3769c92ab7660f17`,
`ai-usage.conf` `21e76af98ce791fa`, `windows.conf` `45b1e4654edaec11`, `apps.conf` `1a5482bb81b325ef`.

### 4.3 Matching-order decision table `[INF-docs]`
| # | Rule | Consequence |
|---|---|---|
| 1 | Top-to-bottom evaluation; order matters | later rules see the state left by earlier ones (tags toggled, props changed) |
| 2 | **Named rules first, then all anonymous ones** | the 3 named blocks are evaluated before every anonymous rule regardless of position |
| 3 | Effects: last match takes precedence | conflicting effects resolved in favor of the later rule |
| 4 | **Static** effects evaluated once at window open; match against `initialClass`/`initialTitle` | cannot retro-apply on title change (e.g. `float`, `size`, `workspace`, `suppress_event`) |
| 5 | **Dynamic** effects re-evaluated on property change | e.g. `opacity`, `tag`, `no_focus`, `scroll_touchpad`, `no_screen_share` |
| 6 | Opacity is a **product** of all opacity rules unless `override` is appended | stacking opacity rules darkens (0.5×0.5=0.25); no rule in the plane uses `override` |
| 7 | Tag dynamics: rule `tag` manipulates **dynamic** tags (rendered with `*` suffix); `+`/`-`/toggle by prefix; `match:tag X` matches `X` and `X*`, `match:tag X*` matches the starred tag only | drives the default-opacity opt-out chain (§4.4) |
| 8 | Only **named** rules can be live-toggled (`hyprctl keyword 'windowrule[name]:enable false'`) | anonymous rules (most of the plane) are not runtime-reconfigurable this way |

### 4.4 Props and effects actually used in the plane `[OBS]` (+ `[INF-docs]` classification)
- Props: `match:class` (most rules; e.g. `windows.conf:3`, `input.conf:45`), `match:title`
  (`steam.conf:3,6,7`, `pip.conf:2`, `webcam-overlay.conf:2-6`),
  `match:tag` (`windows.conf:15`, `system.conf:2-4`, `pip.conf:3-10`, `terminals.conf:3-4`,
  `browser.conf:4,5,12,15,16`), booleans `match:xwayland 1`, `match:float 1/0`,
  `match:fullscreen 0`, `match:pin 0` (`windows.conf:9`), `match:float 1` (unsourced
  davinci orphan only). Layerrules use `match:namespace` (`hyprshot.conf:2`, `walker.conf:2`).
- Static effects declared: `float`, `tile` (`browser.conf:12`), `center`, `size`, `move`
  (`pip.conf:10`, `webcam-overlay.conf:6` — expressions `monitor_w|h`, `window_w|h`),
  `fullscreen` (`retroarch.conf:1`, `system.conf:11`), `workspace special silent`
  (`browser.conf:19`), `no_initial_focus` (`webcam-overlay.conf:4`), `pin`
  (`pip.conf:5`, `webcam-overlay.conf:3`), `suppress_event maximize` (`windows.conf:3`).
- Dynamic effects declared: `opacity` (`terminals.conf:4`, `windows.conf:15`, `system.conf:17`,
  `steam.conf:5`, `qemu.conf:2`, `retroarch.conf:3`, `pip.conf:9`, `browser.conf:15-16`),
  `tag` (throughout), `no_focus` (`windows.conf:9`), `no_screen_share` (`1password.conf:1`,
  `bitwarden.conf:1,5`), `idle_inhibit` (`retroarch.conf:4`, `steam.conf:8`,
  `geforce.conf`, `moonlight.conf`), `focus_on_activate off` (`telegram.conf:2`),
  `no_follow_mouse` (`jetbrains.conf`), `stay_focused` (davinci orphan only),
  `keep_aspect_ratio` (`pip.conf:7`), `border_size 0` (`pip.conf:8`), `rounding 8`
  (`system.conf:20`), `animation slide` (`system.conf:13`),
  `scroll_touchpad` (`input.conf:45-46`), layer `no_anim` (`hyprshot.conf:2`,
  `walker.conf:2`), `no_dim` (`webcam-overlay.conf:5`).

### 4.5 Worked chains `[INF]` (file order measured; doc semantics labeled)
- **Alacritty default-opacity chain** — `windows.conf:6` adds tag `default-opacity`;
  `terminals.conf:2` adds `terminal`; `terminals.conf:3` `tag -default-opacity, match:tag
  terminal` un-sets it; `terminals.conf:4` sets `opacity 0.97 0.9`; `windows.conf:15`
  (`opacity 0.97 0.9, match:tag default-opacity`) is intended **not** to match after the
  un-set. `input.conf:45` additionally overrides `input:touchpad:scroll_factor` (live
  `0.4`, `input.conf:34`) with `1.5` for Alacritty/kitty/foot. **Live state diverges — §4.6.**
- **ai-usage float chain** — when an `org.omarchy.ai-usage` window maps, `system.conf:2-4`
  (match:tag floating-window) does not match yet (tag added later at `ai-usage.conf:2`);
  the window is floated/centered/sized directly by `ai-usage.conf:3-5`. On re-evaluation the
  system.conf rules then match the same tag and re-apply the identical effects. Net result:
  floats at 875×600, centered — same as the `floating-window` TUI recipe. `[UNK]` no such
  window currently open, so unverified at runtime.

### 4.6 Live divergence observed `[OBS]` — Alacritty tag state
`hyprctl clients -j`, 3 clients (all class `Alacritty`, workspace 1, monitor 0):

| pid | tags |
|---|---|
| 3982970 | `default-opacity*`, `terminal*` |
| 275049 | `terminal*` |
| 1784450 | `default-opacity*`, `terminal*` |

The declared intent (`terminals.conf:2-3`) leaves `terminal*` and **no** `default-opacity` —
matched by only 1 of 3 windows. Two windows still carry `default-opacity*`.
`[OBS]` also confirms the docs' dynamic-tag `*` suffix first-hand.
`[INF-docs]` Consequence for the two windows: `windows.conf:15` matches → its `opacity 0.97
0.9` multiplies with `terminals.conf:4` (docs: opacity is a product by default) ≈ 0.9409
active / 0.81 inactive, darker than intended. `[UNK]` cause of the divergence (window age vs
config-reload history, or dynamic re-evaluation sequencing) — not investigated; no
mutations performed. Operator-side read-only follow-up: compare tags of a freshly opened
Alacritty against these three.

## 5. Read-only verification recipes `[OBS]`
- `hyprctl binds -j` — fields `modmask / key / keycode / dispatcher / arg / locked /
  release / repeat / mouse / has_description / submap / catch_all`. Count: 192. Flag counts
  in §1. Modmask mapping in §2.2.
- Reconciliation method (reproducible): parse each `^bind([flags]*)\s*=` line, take
  `[mods=field0, key=field1, (description=field2 if d-flag), dispatcher, params…]`; predict
  the modmask by summing `{SHIFT:1, CTRL:4, ALT:8, SUPER:64}` over mod tokens; match against
  a live entry on `key`/`keycode` + `dispatcher` + `arg` (whitespace-insensitive); mouse
  binds map to live `dispatcher:"mouse"` with `arg` = the declared function. Result 192/192.
- `hyprctl clients -j` — per-window `tags` (dynamic tags starred), `floating`, `xwayland`,
  `workspace`, `pid`; §4.6.
- `hyprctl getoption` — `input:touchpad:scroll_factor` → `float: 0.400000`;
  `dwindle:preserve_split` → `int: 1` (`set: true`); `input:follow_mouse` → `int: 1`;
  `decoration:rounding_power` → `float: 2.000000` (default, `set: false`).
- Named-rule toggle recipe (`hyprctl keyword 'windowrule[jetbrains-focus]:enable false'`) —
  **mutating; operator-only; not run by this lane.**

## 6. Unknowns
1. **No dispatcher was fired.** All per-dispatcher semantics are `[INF-docs]`; the lane
   verified parsing (modmask/flags/args), not behavior.
2. **Docs drift.** Current wiki is lua-era ("hyprlang deprecated since 0.55"); host 0.56.2
   still parses hyprlang. Syntax-critical points were cross-checked against the 0.54 archive;
   the underscore spelling (`SUPER_SHIFT`) shown in current-wiki examples was not tested
   against 0.56.2, and current-only props/effects (`scrolling_width`, `allows_input`,
   `match:xdg_tag`, …) were not compared to the host version.
3. Cause of the `default-opacity*` divergence (§4.6) — unverified.
4. Whether `layoutmsg togglesplit` actually toggles here (`preserve_split` is on; behavior
   unexercised).
5. Per-window effective values (applied opacity product, scroll factor) are not directly
   readable via hyprctl; §4.5/§4.6 consequences remain inference.
6. `match:tag` matching subtleties beyond the docs' example (`X` matches `X`/`X*`; `X*` only
   the starred tag) — not tested at runtime.

## 7. Errata (append-only — add blocks, never edit above)
- E1 (2026-10-14, MADO-R2-2 seed): no corrections yet.

## 8. Spot-checks (reproducible)
1. `hyprctl binds -j | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d))'`
   → `192`; flag counters (`locked` 26, `repeat` 14, `release` 1, `mouse` 2,
   `has_description` 190) and modmask histogram
   `{0:23, 1:2, 8:7, 9:2, 12:2, 13:1, 64:42, 65:37, 68:26, 69:3, 72:19, 73:22, 76:6}`.
2. `grep -c '^bind'` on the five sources = 25 + 23 + 4 + 90 + 50 = 192.
3. `hyprctl getoption input:touchpad:scroll_factor` → `float: 0.400000`;
   `hyprctl getoption dwindle:preserve_split` → `int: 1`.
4. `hyprctl clients -j` → the 3 Alacritty windows and their tags as in §4.6.
5. sha256 drift check: bind sources per §1 table; rule files per §4.2.