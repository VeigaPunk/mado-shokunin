# Host option table — mado round 40, wave w1, seat ExecHostCompose

What this is: the operator-facing option table of the running host compositor, one row per key
the static resolver declares **and** the compositor answers, composed from the round-40 census
(reference tool, live mode) joined with the declarer derivation (which file:line last declared
the key, and which earlier declaration it shadows). Facts only; no recommendations.

## Provenance

- Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`; claims frozen at `.ufo/waves/round-40/registration.md`
  (freeze commit `5e7e88525cc539563de7746361b2650802e81809`, base `9fc511ddce708327377161202f358ce37dc266ba`).
- Data tool: throwaway reference `c1/ctl-ref-tool.py.txt` copied to `/tmp/hostcompose.2qy6nV/ref.py`
  (sha256 `f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa`). A control, never delivered.
- Census command (exit 0, no stderr):

  ```
  python3 -I /tmp/hostcompose.2qy6nV/ref.py --home "$HOME" --live > live.json
  ```

- Native replies: one `hyprctl getoption -j KEY` per declared key (the only compositor verb run).
  Raw tool output retained at `live.json` (sha256 `cde4b2dfb586e5d9765af1df6f73188da3537b53f13a9525d21b693684905462`).
- `hyprctl version` (retained at `hyprctl-version.txt`, sha256 `e0fb982b88d0017e13a5ee2697765a10c4c088eefc589bdc02656b9be7f2844f`):
  `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`,
  `Hyprlang: built against 0.6.8, system has 0.6.8`.
- Form cross-check: the 70 native values and `set` flags in this run are identical (0 diffs) to the frozen
  capture `c1/native-capture.jsonl`; that capture supplies the native form name per key, since the
  reference tool's row carries only the value string.
- Declarer derivation: owner file:line and raw line text read from the host trees at the paths named in
  each row; the shadowed declarers in the last column were located by exact-key grep over the same
  resolved `source =` graph.

## Counts

| measure | value |
|---|---|
| declared keys (static table) | 70 |
| keys with a native reply | 70 (`config-only` 0, `live-default` 0) |
| label `agreement` | 62 |
| label `agreement*` | 8 |
| label `mismatch` | 0 |
| native forms | int 44, float 5, custom 13, str 8 |

## Legend

- **declared (as written)** — the value text the owner file writes after `=` (trimmed of surrounding
  whitespace only), comments and variable indirection included. Where the RHS is a `$variable`, the
  resolved expansion the resolver used follows the arrow.
- **live (native form)** — the form the compositor answered with (`int` | `float` | `str` | `custom`)
  and the value as it prints. Floats print with 6 decimals on the wire (`0.600000`).
- **label** — `agreement` (live equals the resolved declaration, `set=true`, one declarer);
  `agreement*` (same, but an earlier declarer of the key is shadowed).
- **owner** — the last declarer, relative to `$HOME`, as `file:line`.
- **†1 / †2** — the two angle-inheritance rows, dissected in the section after the tables.
- Paths: `looknfeel.conf` = `~/.local/share/omarchy/default/hypr/looknfeel.conf`,
  `default/hypr/input.conf` = `~/.local/share/omarchy/default/hypr/input.conf`,
  theme = `~/.config/omarchy/current/theme/hyprland.conf`,
  toggle = `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf`.

## Colours (11)

| key | declared (as written) | live (native form) | label | owner file:line | earlier declarer (shadowed) |
|---|---|---|---|---|---|
| `general:col.active_border` | `$activeBorderColor` → `rgb(e68e0d)` (theme `hyprland.conf:1`) | `custom` `ffe68e0d 45deg` | `agreement*` | `~/.config/omarchy/current/theme/hyprland.conf:4` †1 | `looknfeel.conf:15` `col.active_border = $activeBorderColor` = `rgba(33ccffee) rgba(00ff99ee) 45deg` (`looknfeel.conf:4`) |
| `general:col.inactive_border` | `$inactiveBorderColor` → `rgba(595959aa)` (`looknfeel.conf:5`) | `custom` `aa595959 0deg` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:16` | — |
| `group:col.border_active` | `$activeBorderColor` → `rgb(e68e0d)` (theme `hyprland.conf:1`) | `custom` `ffe68e0d 45deg` | `agreement*` | `~/.config/omarchy/current/theme/hyprland.conf:8` †2 | `looknfeel.conf:51` `col.border_active = $activeBorderColor` = `rgba(33ccffee) rgba(00ff99ee) 45deg` (`looknfeel.conf:4`) |
| `group:col.border_inactive` | `$inactiveBorderColor` → `rgba(595959aa)` (`looknfeel.conf:5`) | `custom` `aa595959 0deg` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:52` | — |
| `group:col.border_locked_active` | `$activeBorderColor` → `rgba(33ccffee) rgba(00ff99ee) 45deg` (`looknfeel.conf:4`, defaults value: this line is parsed before the theme redefines it) | `custom` `ee33ccff ee00ff99 45deg` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:53` | — |
| `group:col.border_locked_inactive` | `$inactiveBorderColor` → `rgba(595959aa)` (`looknfeel.conf:5`) | `custom` `aa595959 0deg` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:54` | — |
| `group:groupbar:col.active` | `rgba(00000040)` | `custom` `40000000 0deg` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:70` | — |
| `group:groupbar:col.inactive` | `rgba(00000020)` | `custom` `20000000 0deg` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:71` | — |
| `group:groupbar:text_color` | `rgb(ffffff)` | `int` `4294967295` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:68` | — |
| `group:groupbar:text_color_inactive` | `rgba(ffffff90)` | `int` `2432696319` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:69` | — |
| `decoration:shadow:color` | `rgba(1a1a1aee)` | `custom` `ee1a1a1a 0deg` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:35` | — |

## Gaps and borders (5)

| key | declared (as written) | live (native form) | label | owner file:line | earlier declarer (shadowed) |
|---|---|---|---|---|---|
| `general:gaps_in` | `0` | `custom` `0 0 0 0` | `agreement*` | `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf:4` | `looknfeel.conf:9` `gaps_in = 5` |
| `general:gaps_out` | `0` | `custom` `0 0 0 0` | `agreement*` | `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf:3` | `looknfeel.conf:10` `gaps_out = 10` |
| `general:border_size` | `0` | `int` `0` | `agreement*` | `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf:5` | `looknfeel.conf:12` `border_size = 2` |
| `group:groupbar:gaps_in` | `5` | `int` `5` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:65` | — |
| `group:groupbar:gaps_out` | `0` | `int` `0` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:66` | — |

## Rounding (2)

| key | declared (as written) | live (native form) | label | owner file:line | earlier declarer (shadowed) |
|---|---|---|---|---|---|
| `decoration:rounding` | `0` | `int` `0` | `agreement*` | `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf:9` | `looknfeel.conf:29` `rounding = 0` |
| `group:groupbar:gradient_rounding` | `0` | `int` `0` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:74` | — |

## Blur (6)

| key | declared (as written) | live (native form) | label | owner file:line | earlier declarer (shadowed) |
|---|---|---|---|---|---|
| `decoration:blur:enabled` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:40` | — |
| `decoration:blur:size` | `2` | `int` `2` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:41` | — |
| `decoration:blur:passes` | `2` | `int` `2` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:42` | — |
| `decoration:blur:special` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:43` | — |
| `decoration:blur:brightness` | `0.60` | `float` `0.600000` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:44` | — |
| `decoration:blur:contrast` | `0.75` | `float` `0.750000` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:45` | — |

## Shadow (3)

| key | declared (as written) | live (native form) | label | owner file:line | earlier declarer (shadowed) |
|---|---|---|---|---|---|
| `decoration:shadow:enabled` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:32` | — |
| `decoration:shadow:range` | `2` | `int` `2` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:33` | — |
| `decoration:shadow:render_power` | `3` | `int` `3` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:34` | — |

## Animations (1)

| key | declared (as written) | live (native form) | label | owner file:line | earlier declarer (shadowed) |
|---|---|---|---|---|---|
| `animations:enabled` | `yes, please :)` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:82` | — |

## Input and cursor (15)

| key | declared (as written) | live (native form) | label | owner file:line | earlier declarer (shadowed) |
|---|---|---|---|---|---|
| `input:kb_layout` | `br` | `str` `br` | `agreement*` | `~/.config/hypr/input.conf:10` | `default/hypr/input.conf:3` `kb_layout = us` |
| `input:kb_variant` | *(empty)* | `str` *(empty)* | `agreement` | `~/.local/share/omarchy/default/hypr/input.conf:4` | — |
| `input:kb_model` | *(empty)* | `str` *(empty)* | `agreement` | `~/.local/share/omarchy/default/hypr/input.conf:5` | — |
| `input:kb_rules` | *(empty)* | `str` *(empty)* | `agreement` | `~/.local/share/omarchy/default/hypr/input.conf:7` | — |
| `input:kb_options` | `compose:caps # ,grp:alts_toggle` | `str` `compose:caps` | `agreement*` | `~/.config/hypr/input.conf:11` | `default/hypr/input.conf:6` `kb_options = compose:caps` |
| `input:repeat_rate` | `40` | `int` `40` | `agreement` | `~/.config/hypr/input.conf:14` | — |
| `input:repeat_delay` | `250` | `int` `250` | `agreement` | `~/.config/hypr/input.conf:15` | — |
| `input:numlock_by_default` | `true` | `int` `1` | `agreement` | `~/.config/hypr/input.conf:18` | — |
| `input:sensitivity` | `0 # -1.0 - 1.0, 0 means no modification.` | `float` `0.000000` | `agreement` | `~/.local/share/omarchy/default/hypr/input.conf:11` | — |
| `input:follow_mouse` | `1` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/input.conf:9` | — |
| `input:touchpad:natural_scroll` | `false` | `int` `0` | `agreement` | `~/.local/share/omarchy/default/hypr/input.conf:14` | — |
| `input:touchpad:clickfinger_behavior` | `true` | `int` `1` | `agreement` | `~/.config/hypr/input.conf:31` | — |
| `input:touchpad:scroll_factor` | `0.4` | `float` `0.400000` | `agreement` | `~/.config/hypr/input.conf:34` | — |
| `cursor:hide_on_key_press` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:136` | — |
| `cursor:warp_on_change_workspace` | `1` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:137` | — |

## Layout, windows and group bar (17)

| key | declared (as written) | live (native form) | label | owner file:line | earlier declarer (shadowed) |
|---|---|---|---|---|---|
| `general:layout` | `dwindle` | `str` `dwindle` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:24` | — |
| `general:resize_on_border` | `false` | `int` `0` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:19` | — |
| `general:allow_tearing` | `false` | `int` `0` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:22` | — |
| `dwindle:preserve_split` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:111` | — |
| `dwindle:force_split` | `2` | `int` `2` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:112` | — |
| `master:new_status` | `master` | `str` `master` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:121` | — |
| `scrolling:column_width` | `0.49` | `float` `0.490000` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:116` | — |
| `binds:hide_special_on_workspace_change` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:142` | — |
| `group:groupbar:height` | `22` | `int` `22` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:64` | — |
| `group:groupbar:font_size` | `12` | `int` `12` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:57` | — |
| `group:groupbar:font_family` | `monospace` | `str` `monospace` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:58` | — |
| `group:groupbar:font_weight_active` | `ultraheavy` | `custom` `1000` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:59` | — |
| `group:groupbar:font_weight_inactive` | `normal` | `custom` `400` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:60` | — |
| `group:groupbar:indicator_height` | `0` | `int` `0` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:62` | — |
| `group:groupbar:indicator_gap` | `5` | `int` `5` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:63` | — |
| `group:groupbar:gradients` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:73` | — |
| `group:groupbar:gradient_round_only_edges` | `false` | `int` `0` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:75` | — |

## Misc, ecosystem, XWayland (10)

| key | declared (as written) | live (native form) | label | owner file:line | earlier declarer (shadowed) |
|---|---|---|---|---|---|
| `misc:anr_missed_pings` | `3` | `int` `3` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:130` | — |
| `misc:disable_hyprland_logo` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:126` | — |
| `misc:disable_splash_rendering` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:127` | — |
| `misc:disable_scale_notification` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:128` | — |
| `misc:focus_on_activate` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:129` | — |
| `misc:key_press_enables_dpms` | `true  # key press will trigger wake` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/input.conf:19` | — |
| `misc:mouse_move_enables_dpms` | `true # mouse move will trigger wake` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/input.conf:20` | — |
| `misc:on_focus_under_fullscreen` | `1` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/looknfeel.conf:131` | — |
| `ecosystem:no_update_news` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/envs.conf:32` | — |
| `xwayland:force_zero_scaling` | `true` | `int` `1` | `agreement` | `~/.local/share/omarchy/default/hypr/envs.conf:24` | — |

## The two angle-inheritance rows

Both rows declare a single colour with no `deg` token, and both read back with the earlier
declarer's `45deg` angle.

### †1 `general:col.active_border` — live `custom ffe68e0d 45deg`

| step | file:line | as written | resolved |
|---|---|---|---|
| earlier declarer (shadowed) | `~/.local/share/omarchy/default/hypr/looknfeel.conf:15` | `col.active_border = $activeBorderColor` | `$activeBorderColor` at `looknfeel.conf:4` = `rgba(33ccffee) rgba(00ff99ee) 45deg` |
| last declarer (owner) | `~/.config/omarchy/current/theme/hyprland.conf:4` | `col.active_border = $activeBorderColor` | `$activeBorderColor` at theme `hyprland.conf:1` = `rgb(e68e0d)` — one colour, no angle token |
| native reply | — | — | `{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }` |

The colour that survives is the theme's (`e68e0d`, alpha `ff` prefixed); the `45deg` angle is the
one only the shadowed defaults declaration carried.

### †2 `group:col.border_active` — live `custom ffe68e0d 45deg`

| step | file:line | as written | resolved |
|---|---|---|---|
| earlier declarer (shadowed) | `~/.local/share/omarchy/default/hypr/looknfeel.conf:51` | `col.border_active = $activeBorderColor` | `$activeBorderColor` at `looknfeel.conf:4` = `rgba(33ccffee) rgba(00ff99ee) 45deg` |
| last declarer (owner) | `~/.config/omarchy/current/theme/hyprland.conf:8` | `col.border_active = $activeBorderColor` | `$activeBorderColor` at theme `hyprland.conf:1` = `rgb(e68e0d)` — one colour, no angle token |
| native reply | — | — | `{"option": "group:col.border_active", "custom": "ffe68e0d 45deg", "set": true }` |

### Why the angle is inherited rather than a fixed default

Six rows in the table have exactly the same declared shape — one colour, no `deg` token — and all
six read back `0deg`:

| key | declared | owner | live |
|---|---|---|---|
| `decoration:shadow:color` | `rgba(1a1a1aee)` | `looknfeel.conf:35` | `custom ee1a1a1a 0deg` |
| `general:col.inactive_border` | `$inactiveBorderColor` = `rgba(595959aa)` | `looknfeel.conf:16` | `custom aa595959 0deg` |
| `group:col.border_inactive` | `$inactiveBorderColor` = `rgba(595959aa)` | `looknfeel.conf:52` | `custom aa595959 0deg` |
| `group:col.border_locked_inactive` | `$inactiveBorderColor` = `rgba(595959aa)` | `looknfeel.conf:54` | `custom aa595959 0deg` |
| `group:groupbar:col.active` | `rgba(00000040)` | `looknfeel.conf:70` | `custom 40000000 0deg` |
| `group:groupbar:col.inactive` | `rgba(00000020)` | `looknfeel.conf:71` | `custom 20000000 0deg` |

The two † rows differ from these six in one respect only: a preceding declaration of the same key
carried `45deg`. That is the whole difference the data shows.

The complementary row is `group:col.border_locked_active` (`looknfeel.conf:53`): it declares
`$activeBorderColor` and its own declaration resolves to the defaults value
`rgba(33ccffee) rgba(00ff99ee) 45deg`, so it carries two colours and an explicit angle, and reads
`custom ee33ccff ee00ff99 45deg` — no inheritance needed.

## Other facts the rows show

1. `animations:enabled = yes, please :)` (`looknfeel.conf:82`) — the RHS is prose, not a bare
   boolean; it resolves to `1` (label `agreement`) and the reply is `int 1`.
2. A gap declared as one integer answers as a four-token tuple: `gaps_in = 0` and `gaps_out = 0`
   (toggle) both answer `custom 0 0 0 0`; the shadowed defaults were `gaps_in = 5`,
   `gaps_out = 10`.
3. Font-weight names answer as numbers: `font_weight_active = ultraheavy` → `custom 1000`,
   `font_weight_inactive = normal` → `custom 400`.
4. Colour values held by `int`-form options answer as decimal ARGB:
   `text_color = rgb(ffffff)` → `int 4294967295` (`0xFFFFFFFF`),
   `text_color_inactive = rgba(ffffff90)` → `int 2432696319` (`0x90FFFFFF`).
5. Colour values held by `custom`-form options answer as lowercase unpadded ARGB with the alpha
   moved to the front: `rgb(e68e0d)` → `ffe68e0d`, `rgba(1a1a1aee)` → `ee1a1a1a`,
   `rgba(00000040)` → `40000000`, `rgba(00000020)` → `20000000`.
6. `input:sensitivity = 0` is a float option and answers `float 0.000000`.
7. `misc:disable_splash_rendering  = true` (`looknfeel.conf:127`) writes two spaces before `=`;
   the key resolves normally and the reply is `int 1`.
8. `input:kb_options = compose:caps # ,grp:alts_toggle` (`~/.config/hypr/input.conf:11`) drops the
   trailing comment and answers `str compose:caps`.
9. All 8 `agreement*` rows shadow an earlier declaration of the same key; in 6 the surviving value
   differs from the shadowed one and in 2 it does not. The theme overwrites the two angle rows;
   `window-no-gaps.conf` overwrites four (`gaps_in` 5→0, `gaps_out` 10→0, `border_size` 2→0,
   `rounding` 0→0) and `~/.config/hypr/input.conf` overwrites two (`kb_layout` `us`→`br`,
   `kb_options` `compose:caps`→`compose:caps`). `decoration:rounding` and `input:kb_options` are
   labelled `agreement*` although the two declarations agree in value: the label is driven by the
   declarer count, not by a value difference.
10. Three `str` options are declared empty and answered empty with `set: true`:
    `input:kb_variant`, `input:kb_model`, `input:kb_rules`.
11. Every one of the 70 replies carries `set: true`; no declared key is unset on this host.
12. The graph the table walks: `~/.config/hypr/hyprland.conf:4-12` sources nine defaults files,
    `:13` the theme, `:16-20` five user files, `:23` the toggles glob, `:29,:32` `ai-usage.conf`
    and `gkeep.conf`. `~/.config/hypr/hyprlock.conf` is not sourced by it, so its `rounding = 0`
    at `hyprlock.conf:36` does not enter the table.
13. Row accounting: 11 colours + 5 gaps/borders + 2 rounding + 6 blur + 3 shadow + 1 animations +
    15 input/cursor + 17 layout/groupbar + 10 misc = 70.

## What this table does not establish

- It does not test the delivered `tools/mado-options.py`; every value here comes from the
  throwaway reference tool (`c1/ctl-ref-tool.py.txt`), which is a control and is never delivered.
- It does not establish that the compositor's conversion matches the reference model in general —
  only that on these 70 keys the model's predicted label is `agreement`/`agreement*` with 0
  `mismatch` (the declared C1 residual: this is an out-of-distribution check, reported not scored).
- `agreement*` is a declarer-count fact; it says nothing about whether the shadowed value would
  have been preferable.
