# Host idle/lock config bytes — `hypridle.conf`, `hyprlock.conf`, sourced theme file (round 17, W1)

Seat: `MadoR17.HostIdleFiles`. Scope: `sha256sum` + `cat -n` of
`~/.config/hypr/hypridle.conf`, `~/.config/hypr/hyprlock.conf`, and every file they
source, with line-anchored settings (timeouts, commands invoked). Report only; no draft,
no lane edit, no commit.

Method — file bytes only, host pause honoured: `cat -n`, `sha256sum`, `wc`, `stat`, `cmp`,
`grep -n`, `ls`, `find`, `readlink`, `od`. **Nothing was executed from any config or
script**: no `pacman`/`yay`/`paru` (not even `-Q`/`-Si`/`-Sp`/`-Fl`), no `sudo`, no
`systemctl`, no `hyprctl`, no `hypridle`/`hyprlock`/`alacritty`/`waybar`/`walker`/
`omarchy-*`, no `pgrep`/`pidof`/`pkill`, no `notify-send`, no screenshots, no input or
service probes. Config trees were read as bytes; nothing outside the lane was written.
`corpus/lessons/round-16-verifier-spotcheck.md` read first (done). No tools installed or
updated, so no tooling record is owed.

Tags: `[OBS]` byte observed · `[INF]` inference from observed bytes · `[UNK]` unknown
because the only non-mutating route is absent.

Host binary/package versions are `[UNK]` throughout: no package query was permitted.
Prior lane entries quote `hypridle 0.1.8-2`, `hyprlock 0.9.6` from 2026-10-14 `pacman -Q`
/ `--version` runs; those are **prior measurements I did not re-verify** and are not used
as current facts here.

## 1. Inventory `[OBS]`

| Path | Bytes | Lines | mtime (host) | sha256 |
|---|---|---|---|---|
| `~/.config/hypr/hypridle.conf` | 765 | 19 | 2026-10-03 17:44:32 | `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41` |
| `~/.config/hypr/hyprlock.conf` | 742 | 43 | 2026-10-03 17:44:32 | `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1` |
| `~/.config/omarchy/current/theme/hyprlock.conf` (sourced by `hyprlock.conf:1`) | 176 | 5 | 2026-10-03 17:49:02 | `3ef010e72b5f69113e1500bb083fb053f9f121212ad5ed4fe74ad8d12507ad0b` |

Sourced-file question answered: `hyprlock.conf` has **exactly one** `source` line
(`:1`) and it names the theme file above. `hypridle.conf` has **no** `source` directive
at all. No other `hypridle.conf`/`hyprlock.conf` exists under `~/.config/hypr/`, and
`/etc/hypr/hypridle.conf` and `/etc/hypr/hyprlock.conf` are absent.

Line integrity `[OBS]`: all three end with a single LF, contain no CR and no tab
characters. `hypridle.conf` is 15 code lines (2 comments, 2 blank) of 19; `hyprlock.conf`
is 34 code lines (0 comments, 9 blank) of 43.

Provenance by identity `[OBS]`: both local configs are **byte-identical** to Omarchy's
packaged copies —

| Comparison | Result |
|---|---|
| `cmp ~/.config/hypr/hypridle.conf ~/.local/share/omarchy/config/hypr/hypridle.conf` | identical (`765 B`, same sha256) |
| `cmp ~/.config/hypr/hyprlock.conf ~/.local/share/omarchy/config/hypr/hyprlock.conf` | identical (`742 B`, same sha256) |

and neither local file has a `hypridle.conf.bak.*` / `hyprlock.conf.bak.*` sibling
(the only `*.bak.*` in `~/.config/hypr/` is `autostart.conf.bak.1791942509`). The user
configs are unmodified shipped payload, not operator edits.

## 2. `~/.config/hypr/hypridle.conf` — `cat -n` (765 B, 19 lines)

```text
     1	general {
     2	    lock_cmd = omarchy-system-lock                         # lock screen and 1password
     3	    before_sleep_cmd = OMARCHY_LOCK_ONLY=true omarchy-system-lock    # lock before suspend without scheduling display off.
     4	    after_sleep_cmd = sleep 1 && omarchy-system-wake                 # delay for PAM readiness, then turn on display.
     5	    inhibit_sleep = 3                                      # wait until screen is locked
     6	}
     7	
     8	# Start screensaver after 2.5 minutes
     9	listener {
    10	    timeout = 150
    11	    on-timeout = pidof hyprlock || omarchy-launch-screensaver
    12	}
    13	
    14	# Lock system after 5 minutes (screensaver resets idle timer, so have to just do half + 2s margin)
    15	listener {
    16	    timeout = 152
    17	    on-timeout = omarchy-system-lock
    18	    on-resume = omarchy-system-wake
    19	}
```

### 2.1 Line-anchored settings `[OBS]`

| Anchor | Key | Literal value |
|---|---|---|
| `:2` | `general.lock_cmd` | `omarchy-system-lock` |
| `:3` | `general.before_sleep_cmd` | `OMARCHY_LOCK_ONLY=true omarchy-system-lock` |
| `:4` | `general.after_sleep_cmd` | `sleep 1 && omarchy-system-wake` |
| `:5` | `general.inhibit_sleep` | `3` (integer; comment "wait until screen is locked") |
| `:10` | listener 1 `timeout` | `150` (seconds; comment `:8` "Start screensaver after 2.5 minutes") |
| `:11` | listener 1 `on-timeout` | `pidof hyprlock \|\| omarchy-launch-screensaver` |
| `:16` | listener 2 `timeout` | `152` (seconds) |
| `:17` | listener 2 `on-timeout` | `omarchy-system-lock` |
| `:18` | listener 2 `on-resume` | `omarchy-system-wake` |

No `on-resume` on listener 1, no `on-timeout` persistence/ignore directives, no
`general` keys beyond the three commands plus `inhibit_sleep`.

### 2.2 Commands invoked (declared text only) `[OBS]`

Directly from this file: `omarchy-system-lock` (`:2,:3,:17`), `omarchy-system-wake`
(`:4,:18`), `sleep 1` (`:4`), `pidof hyprlock` (`:11`),
`omarchy-launch-screensaver` (`:11`), plus the `OMARCHY_LOCK_ONLY=true` environment
assignment prefix (`:3`).

One level deeper, from the invoked scripts' bytes (scripts read, never run):

| Script (all under `~/.local/share/omarchy/bin/`) | Bytes / L / sha256 | Declared argv, anchored |
|---|---|---|
| `omarchy-system-lock` | 699 / 33 / `c1dd3881e8aea9106cd844cc1f8ab4bcd4fcb07b81eefeab5e7a225e282b9ce1` | `pidof hyprlock` `:8`,`:29`; `hyprlock` `:10`; `omarchy-system-wake` `:11`; `hyprctl switchxkblayout all 0` `:16`; `pgrep -x 1password` `:19`; `1password --lock` `:20`; `pkill -f org.omarchy.screensaver` `:24`; guard `OMARCHY_LOCK_ONLY != true` `:26`; `sleep 3` `:28`; `omarchy-brightness-keyboard off` `:30`; `omarchy-brightness-display off` `:31` |
| `omarchy-system-wake` | 228 / 9 / `09ad52b0f184ced3756b3ba5cdcee743ff78174dd9f83334c68ba4ed110bd3d4` | `omarchy-brightness-display on` `:8`; `omarchy-brightness-keyboard restore` `:9` |
| `omarchy-launch-screensaver` | 1641 / 59 / `ba783a3a55c134af4e7fe4111d9ef6fc7796d03a78bb7f114eeee6dd3758fa12` | `command -v tte` `:5`; `pgrep -f org.omarchy.screensaver` `:10`; `omarchy-toggle-enabled screensaver-off` `:13`; `walker -q` `:18`; `omarchy-hyprland-monitor-focused` `:20`; `xdg-terminal-exec --print-id` `:21`; `hyprctl monitors -j \| jq …` `:23`; `hyprctl dispatch focusmonitor` `:24`,`:59`; `hyprctl dispatch exec -- alacritty --class=org.omarchy.screensaver --config-file ~/.local/share/omarchy/default/alacritty/screensaver.toml -e omarchy-screensaver` `:28-31` (with `*ghostty*` `:33-39`, `*foot*` `:41-44`, `*kitty*` `:46-51` branches); `notify-send -u low …` `:54` |

Declared transitively named helpers, existence + digest only (bodies not read this pass):
`omarchy-brightness-display` `62e6d7655258c875a81a31c345614bffb854a7f5db6f2a10e848090c5de3dc93`
(60 L), `omarchy-brightness-keyboard`
`f1305c06b0ecaea29c415f74738c462b062155a11332d87df72c97cde2ecc917` (55 L),
`omarchy-toggle-enabled` `5f5b2797e2f5912f0c5e19f02ede429fdc2952dbf3f3d0c31f1d6e2964006988`
(6 L), `omarchy-hyprland-monitor-focused`
`c3f4e85b13ca93d09af97ee8470a8b45f69293ef6d6d3acf07ff13a77e158d26` (5 L),
`omarchy-screensaver` `11d7487aa3eebe3eedb453bee844225d3c213e58da25678b4ab7a07381a551f6`
(35 L), `omarchy-toggle-idle`
`11979b4d4198526445ee124a66ce1d2b5607b9f62ad01a516f22bba66256b284` (13 L).

Cross-surface link to P4 `[OBS]`+`[INF]`: `~/.config/xdg-terminals.list` (3 L,
`d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b`) lists
`Alacritty.desktop` at `:3`, and the screensaver script's `case` selects the
`*Alacritty*` branch (`:26-32`). The declared screensaver terminal is therefore
Alacritty; `--print-id` resolution itself was not measured (`[INF]`).

## 3. `~/.config/hypr/hyprlock.conf` — `cat -n` (742 B, 43 lines)

```text
     1	source = ~/.config/omarchy/current/theme/hyprlock.conf
     2	
     3	general {
     4	    ignore_empty_input = true
     5	}
     6	
     7	background {
     8	    monitor =
     9	    color = $color
    10	    path = ~/.config/omarchy/current/background
    11	    blur_passes = 3
    12	}
    13	
    14	animations {
    15	    enabled = false
    16	}
    17	
    18	input-field {
    19	    monitor =
    20	    size = 650, 100
    21	    position = 0, 0
    22	    halign = center
    23	    valign = center
    24	
    25	    inner_color = $inner_color
    26	    outer_color = $outer_color
    27	    outline_thickness = 4
    28	
    29	    font_family = JetBrainsMono Nerd Font
    30	    font_color = $font_color
    31	
    32	    placeholder_text = Enter Password
    33	    check_color = $check_color
    34	    fail_text = <i>$FAIL ($ATTEMPTS)</i>
    35	
    36	    rounding = 0
    37	    shadow_passes = 0
    38	    fade_on_empty = false
    39	}
    40	
    41	auth {
    42	    fingerprint:enabled = false
    43	}
```

### 3.1 Line-anchored settings `[OBS]`

| Anchor | Object / key | Literal value |
|---|---|---|
| `:1` | top-level `source` | `~/.config/omarchy/current/theme/hyprlock.conf` (the only include) |
| `:3-5` | `general` | `ignore_empty_input = true` |
| `:8` | `background.monitor` | empty value (no monitor name on the line) — monitor-selection semantics `[UNK]` here |
| `:9` | `background.color` | `$color` |
| `:10` | `background.path` | `~/.config/omarchy/current/background` (symlink, see §4.3) |
| `:11` | `background.blur_passes` | `3` |
| `:14-16` | `animations` | `enabled = false` |
| `:19` | `input-field.monitor` | empty value |
| `:20` | `input-field.size` | `650, 100` |
| `:21` | `input-field.position` | `0, 0` |
| `:22-23` | `input-field.halign/valign` | `center` / `center` |
| `:25-26` | `input-field.inner_color/outer_color` | `$inner_color` / `$outer_color` |
| `:27` | `input-field.outline_thickness` | `4` |
| `:29` | `input-field.font_family` | `JetBrainsMono Nerd Font` |
| `:30` | `input-field.font_color` | `$font_color` |
| `:32` | `input-field.placeholder_text` | `Enter Password` |
| `:33` | `input-field.check_color` | `$check_color` |
| `:34` | `input-field.fail_text` | `<i>$FAIL ($ATTEMPTS)</i>` (markup + two runtime-looking variables; expansion `[UNK]` from bytes) |
| `:36-38` | `input-field.rounding/shadow_passes/fade_on_empty` | `0` / `0` / `false` |
| `:41-43` | `auth` | `fingerprint:enabled = false` |

Five theme variables are consumed at `:9,:25,:26,:30,:33` — exactly the five defined by
the sourced file, no orphan variable and no undefined reference `[OBS]` (set comparison).

No command is invoked by this file; it is a render description. The only external
references are the sourced theme file and the background image path.

## 4. Sourced file: `~/.config/omarchy/current/theme/hyprlock.conf` — `cat -n` (176 B, 5 lines)

```text
     1	$color = rgba(18,18,18, 1.0)
     2	$inner_color = rgba(18,18,18, 0.8)
     3	$outer_color = rgba(190,190,190, 1.0)
     4	$font_color = rgba(190,190,190, 1.0)
     5	$check_color = rgba(230,142,13, 1.0)
```

`[OBS]` The five variables are the complete definition set; `hyprlock.conf` is the only
file under `~/.config/hypr/` that sources it.

### 4.1 How this file is produced (documentary chain) `[OBS]`

It is rendered from a template, not hand-written:

| Link | Anchor | Observed content |
|---|---|---|
| Template | `~/.local/share/omarchy/default/themed/hyprlock.conf.tpl` (224 B, 5 L, `9e95036ecbd011cd82bb27f89b52b466d472219cdfe3b097babd6bdba784e211`) | `$color = rgba({{ background_rgb }}, 1.0)`, `$inner_color = rgba({{ background_rgb }}, 0.8)`, `$outer_color = rgba({{ foreground_rgb }}, 1.0)`, `$font_color = rgba({{ foreground_rgb }}, 1.0)`, `$check_color = rgba({{ accent_rgb }}, 1.0)` — `:1-5` |
| Renderer | `~/.local/share/omarchy/bin/omarchy-theme-set-templates` | `:6` `TEMPLATES_DIR=$OMARCHY_PATH/default/themed`; `:7` user template dir; `:9` `COLORS_FILE=next-theme/colors.toml`; `:12-15` `hex_to_rgb()` (`0x` byte → decimal); `:21-33` builds `sed` rules `{{ key }}`, `{{ key_strip }}`, and `{{ key_rgb }}`; `:38` user templates then built-ins; `:40` output `next-theme/<basename>`; `:43` skip if output exists; `:44` render |
| Orchestrator | `~/.local/share/omarchy/bin/omarchy-theme-set` | `:29-30` copy theme files then user overlay into `next-theme`; `:38` call `omarchy-theme-set-templates`; `:42` `mv next-theme current/theme`; `:45` write `theme.name` |
| Colour source | `~/.config/omarchy/current/theme/colors.toml` (461 B, 23 L, `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`) | `:1` `accent = "#e68e0d"`, `:3` `foreground = "#bebebe"`, `:4` `background = "#121212"` |

`[OBS]` Value derivation is exact, not approximate: `#121212` → `0x12,0x12,0x12` →
`18,18,18` (`$color`, `$inner_color`); `#bebebe` → `190,190,190` (`$outer_color`,
`$font_color`); `#e68e0d` → `230,142,13` (`$check_color`). Alpha literals `1.0` / `0.8`
come from the template, and the accent enters only via `check_color`.

`[OBS]` Theme identity: `~/.config/omarchy/current/theme.name` = `matte-black`;
`current/theme` is a **real directory** (not a symlink) with
`colors.toml` byte-identical to `~/.local/share/omarchy/themes/matte-black/colors.toml`
(`cmp` identical, same sha256). `themes/matte-black/` contains **no** `hyprlock.conf`,
so the built-in template is the source of the rendered file (a theme-specific file would
have won per renderer `:43`). `~/.config/omarchy/themed/` holds only
`alacritty.toml.tpl.sample`, i.e. no user `hyprlock.conf.tpl` override.

`[INF]` Therefore the lock-screen palette is a P5 (theme) product surfaced in P6: a
theme change rewrites this file, and `hyprlock.conf:1` re-reads it on the next lock.
Not measured: whether hyprlock re-reads the file per invocation (config semantics belong
to the upstream scouts).

### 4.2 Referenced (not sourced) path `[OBS]`

`hyprlock.conf:10` points `background.path` at `~/.config/omarchy/current/background`,
which is a symlink resolving to
`/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg`; the target
exists. Shape only — the image bytes were not opened.

### 4.3 Not sourced, but same payload `[OBS]`

`/usr/share/hypr/hyprlock.conf` (109 L, `22e74ea5e271fee900b8fd06b5900465adf779fc8ca50d70be14760622faa71e`)
and `/usr/share/hypr/hypridle.conf` (37 L,
`ef385d88e8c99820ed910eadd62cd14c16bc948317d4f78e93453e24c70d13d1`) are upstream
package examples, **not** the effective config: the effective files are the Omarchy
copies in §1, and the local `hypridle.conf` differs structurally from the upstream
example (2 listeners vs 5; `omarchy-*` commands vs `loginctl`/`brightnessctl`/
`hyprctl`/`systemctl suspend`; upstream `:24` timeout 300 and `:34-37` 1800 s suspend
have no local counterpart). Whether either binary falls back to the `/usr/share` file
when the user file is absent is `[UNK]` here (both user files are present).

## 5. Wiring: how these files are read and how their commands resolve `[OBS]`

| Link | Anchor | Content |
|---|---|---|
| Compositor start graph | `~/.config/hypr/hyprland.conf:4` | `source = ~/.local/share/omarchy/default/hypr/autostart.conf` |
| Idle daemon launch | `~/.local/share/omarchy/default/hypr/autostart.conf:1` | `exec-once = uwsm-app -- hypridle` |
| Config selection | `hypridle.conf` + `autostart.conf:1` | no `-c` flag anywhere; bare `hypridle` ⇒ default config path `[INF]` |
| Lock binary launch | `omarchy-system-lock:10` | bare `hyprlock`, no `-c`; no other config file is passed |
| PATH for bare helper names | `~/.config/uwsm/env:4-5` | `export OMARCHY_PATH=$HOME/.local/share/omarchy`; `export PATH=$OMARCHY_PATH/bin:$PATH:$HOME/.local/bin` |
| PATH mirror for shells | `~/.local/share/omarchy/default/bash/envs:10-11` | same two exports |
| No system-wide copy | `/usr/bin/omarchy-system-lock`, `/usr/local/bin/omarchy-system-lock` | both absent; resolution depends on the session `PATH` above `[INF]` |
| Keybindings | `~/.local/share/omarchy/default/hypr/bindings/utilities.conf:30,:76` (sourced at `hyprland.conf:8`) | `SUPER CTRL, I` → `omarchy-toggle-idle`; `SUPER CTRL, L` → `omarchy-system-lock` |
| Systemd alternative | `/usr/lib/systemd/user/hypridle.service` (14 L, `81939c3f6004a96599b385e2ffe64201c7e76f1fbf25e08c0efbc349381c0f34`) | `PartOf=`/`After=graphical-session.target`, `ConditionEnvironment=WAYLAND_DISPLAY`, `ExecStart=/usr/bin/hypridle`, `Restart=on-failure`, `WantedBy=graphical-session.target` |
| Refresh route | `omarchy-refresh-hypridle:5-6`, `omarchy-refresh-hyprlock:5`, `omarchy-refresh-config:13-20` | `omarchy-refresh-config hypr/{hypridle,hyprlock}.conf`; hypridle variant also `omarchy-restart-hypridle`; refresh backs up `<file>.bak.<epoch>` |
| Other editors/consumers | `omarchy-menu:464-465` (open in editor), `omarchy-font-set:29` (sed `font_family`), `omarchy-setup-security-fingerprint:47-48` / `omarchy-remove-security-fingerprint:25-26` (sed placeholder / fingerprint) | documents why `:29` and `:42` are machine-edited fields |

Migration provenance for the exact current bytes `[OBS]` (scripts under
`~/.local/share/omarchy/migrations/`): `1767414310.sh:3` `timeout = 300` → `151`;
`1771618300.sh:2` copies `config/hypr/hypridle.conf` over the user file wholesale
(explains the byte identity and the current `152`); `1777467659.sh:3-4` renames
`omarchy-lock-screen` → `omarchy-system-lock`. For hyprlock:
`1762684663.sh:6,9` font family, `1762685081.sh:3-11` placeholder text,
`1764378788.sh:3-4` inserts `general { ignore_empty_input = true }` after the `source`
line, `1770372978.sh:4` forces `fingerprint:enabled = false`. The current files are
consistent with this history (`:1-5` general block right after `source`, `152` timeout,
`omarchy-system-lock` spelling, `JetBrainsMono Nerd Font`, fingerprint off).

## 6. Drift observations relevant to the round (not scored here) `[OBS]`

- `hypridle.conf`, `hyprlock.conf`, and the theme file are unchanged since
  2026-10-03 17:44:32 / 17:49:02: same bytes as the round-4 measurement
  (`idle-lock-plane.md` §2 pins `e7d3b8dd9835`, `b8d173dcff55`, `3ef010e72b5f`).
- `~/.config/hypr/hyprland.conf` is now **32 lines / 1,329 B**, sha256
  `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365`, with
  `source = ~/.config/hypr/gkeep.conf` at `:32` and `ai-usage.conf` at `:29`. The
  MADO-1 measurement (`hyprland-config-plane.md:13-14`: "29 lines, 1,273 B") survives
  byte-exactly as `hyprland.conf.bak.1792267376` (29 L / 1,273 B,
  `4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462`), which is the
  digest `hyprctl-verification-layer.md:205` records. So current ≠ measured: P1-side
  freshness text must be re-derived from the 32-line file, not copied.
- `hyprland.conf:23` still sources the toggle glob
  `~/.local/state/omarchy/toggles/hypr/*.conf`; a `screensaver-off`/`waybar-off` toggle
  could therefore change declared behaviour without touching these files. The toggle
  directory was **not** enumerated (state tree, not config bytes).

## 7. P6 coverage status under the round-17 rubric V `[OBS]` (measurement inputs only)

The claim defines coverage as: an admitted `corpus/knowledge/` entry whose **first 15
lines** carry `source:` citing a `mined` tier-A `SOURCES.md` row whose `used-by` names
that entry, **plus** `surface: P<n>` (new entries) or the fixed legacy map
`covers: U1|U2 → P1`, `covers: U7 → P2`.

Measured state at this reading:

| Check | Command | Result |
|---|---|---|
| SOURCES rows naming idle/lock | `grep -nE 'hypridle\|hyprlock' corpus/SOURCES.md` | **0 rows** — no tier-A (or any) source row exists for P6 |
| Entries declaring a province surface | `grep -rn '^surface:' corpus/knowledge/` | **none** — `surface:` is a new field, absent everywhere |
| Legacy map entries | `grep -rn '^covers:' corpus/knowledge/` | `U1` `window-rule-effects-getprop.md:6`; `U2` `hyprland-config-era-r12.md:6`; `U3` `xdg-portal-routing-r12.md:6`; `U4` `wayland-protocol-boundaries-r13.md:4`; `U5` `output-colour-boundaries-r14.md:4`; `U6` `input-debugging-boundaries-r15.md:4`; `U7` `waybar-observation-boundaries-r16.md:4` |
| Implied legacy coverage | U1,U2 → P1; U7 → P2 | exactly **2 surfaces** (P1, P2); P3–P6 uncovered — corroborates the declared baseline 2/6 |
| P6 knowledge entry with `source:` | `corpus/knowledge/idle-lock-plane.md` (381 L) | exists and documents the plane in depth, but its first 15 lines carry **no `source:` and no `surface:`**; it cannot count as covered under rubric V as written |

Consequence for the P6 note: it needs (a) a `source:` line inside lines 1–15 citing at
least one **mined tier-A** row, (b) a `surface: P6` line, and (c) that row's `used-by`
naming the new entry path. Two viable shapes, both consistent with the measured bytes:
a **new** note that cites upstream documentation (source ids are being opened by sibling
scouts — `SrcHypridleWiki`, `SrcHypridleTag`, `SrcHypridleSrc`, `SrcHyprlockWiki`,
`SrcHyprlockTag`, `SrcHyprlockLockProto`, `SrcIdleNotifyProto`, `SrcLogindLock`; ids
`S0xx-pending`, L1 assigns — I fetched no web source and mint no id), or a **retrofit**
of `idle-lock-plane.md` inserting `source:`/`surface:` in its first 15 lines. The retrofit
is riskier: it edits an admitted, measurement-dated entry and still needs a mined row
whose `used-by` names it. Documentary routes only — §2–§5 establish declared text; no
behaviour was observed.

Also note for the note's honesty: `idle-lock-plane.md` already contains the plane's
prior measured facts (including 2026-10-14 `pacman -Q`/`--version` values and the
live-idle UNKNOWN). A new note should cite that entry as prior lane work rather than
restate its process observations as fresh measurements, and must not present the
`hypridle 0.1.8-2` / `hyprlock 0.9.6` strings as host facts for today.

## 8. Label check — a comment is not a measurement `[OBS]`/`[INF]`

`hypridle.conf:14` labels the second listener "Lock system after 5 minutes", while `:16`
sets `timeout = 152` seconds. The same line's parenthetical ("screensaver resets idle
timer, so have to just do half + 2s margin") is the only place the 300 s figure and the
150 + 2 derivation appear. Reading the comment as evidence would report a 300 s lock;
the bytes say 152 s, and the ~302 s end-to-end figure is `[INF]` from that comment, not
an observation. This is the same defect class as R16-V1 (citing text for a verdict it
does not carry): the note should quote `timeout = 150` / `timeout = 152` as settings and
mark every effective-timing statement `[INF]`/`[UNK]`.

## 9. Observed / inference / unknown

**Observed** — all digests, byte and line counts, mtimes, `cat -n` bodies above; `cmp`
identity of the two configs against the packaged payload; theme file's five variables and
their exact hex→decimal derivation; template placeholders; renderer/orchestrator line
anchors; `theme.name`; theme directory type and background symlink target; reference scan
results; keybind, autostart, uwsm-PATH and systemd-unit contents; migration scripts;
`SOURCES.md`/`covers:`/`surface:` inventory; `xdg-terminals.list` naming Alacritty.

**Inference** — bare `hypridle`/`hyprlock` read `~/.config/hypr/{hypridle,hyprlock}.conf`
because no `-c` is passed anywhere (config-path semantics unverified without upstream
docs); `omarchy-*` bare names resolve because the compositor session inherits
`~/.config/uwsm/env`'s `PATH`; the `*Alacritty*` screensaver branch is the one selected on
this host; ~302 s effective lock; the theme change rewrites the lock palette.

**Unknown** — whether hypridle/hyprlock are running now and whether any timer can fire
(no process/service probes permitted); every live transition; whether `inhibit_sleep = 3`
behaves as its comment says; whether the 150 s screensaver actually resets the idle
timer; `$FAIL`/`$ATTEMPTS` and empty `monitor =` semantics; whether either config parses
cleanly (no non-mutating checker); installed versions; whether the binaries would fall
back to `/usr/share/hypr/*.conf` in the absence of the user files; contents/effect of
`~/.local/state/omarchy/toggles/hypr/*.conf`.

## 10. Overlap (not an edit)

`.ufo/waves/round-17/w1/reports/HostOmarchyLockScripts.md` independently measures
`hypridle.conf` and the three helper bodies; my digests agree with its table
(`765 B e7d3b8dd…`; helpers `c1dd3881…` 699 B, `09ad52b0…` 228 B, `ba783a3a…` 1,641 B).
My non-overlapping ground: `hyprlock.conf` body, the sourced theme file and its
render chain, uwsm `PATH`/autostart/keybind/systemd wiring, reference and migration
scan, and the rubric-V/SOURCES inventory. `HostTerminalFiles.md` owns P4;
`xdg-terminals.list:3` is the shared link between the P6 screensaver branch and P4.

## 11. Tooling

No tool was installed, upgraded or removed by this seat; the tooling clause's install
channels were superseded by the binding host pause, and no package, service or compositor
command was issued.
