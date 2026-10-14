# Bar / launcher / notification plane — waybar, walker, mako, swayosd, hypridle, hyprlock

Lane: mado-shokunin (probation). Assignment: MADO-2.
Measured 2026-10-14 on host `vgpnk`, session PID namespaces as of that day.
Method: files read in place with line numbers; every dynamic fact is a command
output or a process/D-Bus observation. Substrates outside
`/home/vgpnk/Projects/shokunin/mado-shokunin` were READ-ONLY; no file in
`~/.config/`, `~/.local/share/omarchy/` or `~/Projects/` was written.

Convention: **OBS** = observation, **INF** = inference, **UNK** = unknown.
Anchors are `path:line` into the substrate as it existed at measurement time.

---

## 1. Inventory (bytes / lines / sha256-first-16)

| File | Lines | Bytes | sha256[:16] |
|---|---|---|---|
| `~/.config/waybar/config.jsonc` | 249 | 6068 | `07f7d663106b72e4` |
| `~/.config/waybar/style.css` | 136 | 1887 | `8316c08ceaa7e3f0` |
| `~/.config/walker/config.toml` | 49 | 1336 | `fecf71fa4253803e` |
| `~/.config/hypr/hypridle.conf` | 19 | 765 | `e7d3b8dd983523e4` |
| `~/.config/hypr/hyprlock.conf` | 43 | 742 | `b8d173dcff558287` |
| `~/.config/mako/config` | 5 | 50 | `95bf0c86c955cc81` |
| `~/.config/swayosd/config.toml` | 4 | 87 | `a8a09212a32f38df` |
| `~/.config/swayosd/style.css` | 28 | 372 | (not hashed) |
| `~/.config/omarchy/current/theme/waybar.css` | 2 | — | `a1807a176659d7d6` |
| `~/.config/omarchy/current/theme/walker.css` | 6 | — | `f44cb45063494d2f` |

**OBS** — every component in this plane is running, all started in the same
boot second: `ps -o pid,lstart,etimes,cmd -p 1707,1706,1808,1815` →
waybar PID 1707, mako PID 1706, walker PID 1808 (`--gapplication-service`),
swayosd-server PID 1815; all `STARTED Tue Oct 13 11:02:07 2026`.
**OBS** — `hypridle` and `hyprlock` had no matching PID at measure time
(`pgrep -x` empty); idle/lock processes are demand-started by config, see §5.

**OBS** — versions: `waybar --version` → `Waybar v0.15.0`; `walker --version` →
`2.17.0`; `hypridle --version` → `hypridle v0.1.8` (stdout, exit 0);
`hyprlock --version` → `Hyprlock version v0.9.6`; `swayosd-server --version` →
`swayosd 0.3.2`. `mako --version` → `mako: unrecognized option '--version'`
(no version flag). Omarchy itself: `omarchy version` → `3.8.3`.

---

## 2. Waybar — bar

### 2.1 Layout

**OBS** — `config.jsonc:2-6` bar globals: `reload_style_on_change: true`,
`layer: "top"`, `position: "top"`, `spacing: 0`, `height: 26`.

**OBS** — three module rails:
- left `config.jsonc:7-10`: `custom/omarchy`, `hyprland/workspaces`
- center `config.jsonc:11-20`: `clock`, `clock#secondary`, `custom/weather`,
  `custom/update`, `custom/voxtype`, `custom/screenrecording-indicator`,
  `custom/idle-indicator`, `custom/notification-silencing-indicator`
- right `config.jsonc:21-29`: `group/tray-expander`, `custom/ai-usage`,
  `bluetooth`, `network`, `pulseaudio`, `cpu`, `battery`

**OBS** — workspaces module: `on-click: activate`, `persistent-workspaces`
pinned to 1-5 (`config.jsonc:30-53`), active icon `󱓻` (`config.jsonc:45`).

### 2.2 Bar-to-system coupling (each module's exec/click is a system entry point)

| Module | Anchor | Coupling |
|---|---|---|
| `custom/omarchy` | `config.jsonc:55-60` | on-click `omarchy-menu`; right-click `xdg-terminal-exec`; glyph rendered from font `omarchy` |
| `custom/update` | `config.jsonc:61-68` | exec `omarchy-update-available`, interval 21600 s (6 h), `signal: 7` |
| `cpu` | `config.jsonc:69-74` | left `omarchy-launch-or-focus-tui btop`, right `alacritty` |
| `clock` | `config.jsonc:75-80` | right-click `omarchy-launch-floating-terminal-with-presentation omarchy-tz-select` |
| `clock#secondary` | `config.jsonc:81-86` | timezone `Asia/Shanghai`, format `BJ {:L%H:%M}` |
| `custom/weather` | `config.jsonc:87-93` | exec `$OMARCHY_PATH/default/waybar/weather.sh`, return-type json, interval 60 |
| `network` | `config.jsonc:94-112` | left-click `omarchy-launch-wifi` |
| `battery` | `config.jsonc:113-154` | left `omarchy-menu power`, right `notify-send "$(omarchy-battery-status)"`, states 20/10 |
| `bluetooth` | `config.jsonc:155-163` | left-click `omarchy-launch-bluetooth` |
| `pulseaudio` | `config.jsonc:164-180` | left `omarchy-launch-audio`, right `pamixer -t` (mute toggle), scroll-step 5 |
| `group/tray-expander` | `config.jsonc:181-199` | drawer transition 600 ms, wraps `tray` |
| `tray` | `config.jsonc:231-234` | `icon-size: 12`, `spacing: 17` |

**OBS** — `custom/ai-usage` (`config.jsonc:235-248`) is a local extension:
exec `~/.local/bin/ai-usage waybar`, json, interval 60, `signal: 11`,
`escape: false`, `exec-on-event: false`; scroll/click cycle providers,
right-click cycles identity. `~/.local/bin/ai-usage` is a 52-byte symlink
(777) → `~/Projects/omarchy-usage-tray/bin/ai-usage`; its deployment artifact
`~/Projects/omarchy-usage-tray/deploy/waybar-ai-usage.jsonc:7` also declares
`"signal": 11`. That project is outside this lane's write surface.

### 2.3 Bar signal bus (RTMIN+n → module refresh)

**OBS** — declared consumers in `config.jsonc`: 7→`custom/update` (`:66`),
8→`custom/screenrecording-indicator` (`:203`), 9→`custom/idle-indicator`
(`:209`), 10→`custom/notification-silencing-indicator` (`:215`),
11→`custom/ai-usage` (`:239`).

**OBS** — producers found by `grep -rn RTMIN ~/.local/share/omarchy/bin/`:
- `omarchy-capture-screenrecording:253` → `pkill -RTMIN+8 waybar`
- `omarchy-toggle-idle:13` → `pkill -RTMIN+9 waybar`
- `omarchy-toggle-notification-silencing:13` → `pkill -RTMIN+10 waybar`
- `omarchy-update-available-reset:5` → `pkill -RTMIN+7 waybar`
- signal 11 producer lives outside omarchy: `~/Projects/omarchy-usage-tray/deploy/waybar-on-click.sh:6` → `pkill -x -RTMIN+11 waybar`

**INF** — the private RT signals are the only push channel into the bar; a
module whose producer never fires stays at its `interval`/last value.

### 2.4 Indicator scripts (what "active" means)

**OBS** — all three are stock `$OMARCHY_PATH/default/waybar/indicators/*.sh`:
- `idle.sh:3` — `pgrep -x hypridle` decides; absent hypridle ⇒ text `󱫖`,
  tooltip "Idle lock disabled", class `active`.
- `notification-silencing.sh:3` — `makoctl mode | grep -q do-not-disturb`
  decides; Mako is the source of truth for the silencing glyph.
- `screen-recording.sh:3` — `pgrep -f "^gpu-screen-recorder"` decides.

**INF** — bar state for idle/notifications/recording is a *process or Mako-mode
probe*, not a bar-owned flag: killing hypridle or switching mako mode moves the
bar without waybar being told.

### 2.5 Style

**OBS** — `style.css:1` imports `../omarchy/current/theme/waybar.css`; that
theme file defines exactly two colors — `foreground #bebebe`,
`background #121212` (`~/.config/omarchy/current/theme/waybar.css:1-2`).
**OBS** — global font `JetBrainsMono Nerd Font 13px`, `border: none`,
`border-radius: 0` (`style.css:3-12`).
**OBS** — hardcoded warning red `#a55555` at `style.css:96` (screenrecording),
`:101` (idle + notification-silencing), `:110` (voxtype recording), `:135`
(ai-usage warn/critical).
**INF** — because the theme supplies only two colors and the warning color is
literal, that red and the ai-usage chip do **not** track theme changes; a
theme switch changes background/foreground only.
**OBS** — spacing is hand-tuned per module: e.g. `#clock` margin-left 8.75px
(`style.css:66-68`), `#bluetooth` margin-right 17px (`:46-48`), `#network`
margin-right 13px (`:50-52`), `#custom-expand-icon` margin-right 18px
(`:54-56`), `#tray` margin-right 16px (`:42-44`).
**OBS** — ai-usage chip rules `style.css:113-136`: 12px font, `min-width: 0`,
padding 2px/7px, `border-radius: 4px`, opacity 0.7 (`unauth`/`unknown`) and
0.55 (`stale`).

---

## 3. Walker — launcher

**OBS** — `~/.config/walker/config.toml` (49 lines) overrides the packaged
defaults: `force_keyboard_focus = true` (`:1`), `selection_wrap = true` (`:2`),
`theme = "omarchy-default"` (`:3`), `additional_theme_location =
"~/.local/share/omarchy/default/walker/themes/"` (`:4`),
`hide_action_hints = true` (`:5`).
**OBS** — placeholders `:7-8`; `[keybinds] quick_activate = []` (`:10-11`) —
i.e. no quick-activate binding is configured here.
**OBS** — `max_results = 256` (`:17`); default providers
`desktopapplications`, `websearch` (`:18-21`).
**OBS** — prefix routing `:23-45`: `/` providerlist, `.` files, `:` symbols,
`=` calc, `@` websearch, `$` clipboard.
**OBS** — single emergency row `:47-49`: text `Restart Walker`, command
`omarchy-restart-walker`.
**OBS** — theme dir contains exactly one theme,
`~/.local/share/omarchy/default/walker/themes/omarchy-default/`
(`style.css` 121 lines, `layout.xml`). The theme CSS `style.css:1` reaches back
by a relative path into `.config/omarchy/current/theme/walker.css`; that file
defines 6 colors (`:1-6`: selected-text `#e68e0d`, text/base/border/foreground/
background).
**OBS** — window geometry is in `layout.xml`: `GtkWindow#Window` with
`BoxWrapper` `width-request 644` (`layout.xml:4-15`).
**OBS** — theme CSS kills subtext (`style.css:94-99`: `font-size: 0px`) and
italics the selected row (`:109-111`); keybind hints block sits at `:113`.

### 3.1 Launch and lifecycle (the non-obvious part)

**OBS** — Walker is launched as the *systemd user service*
`app-walker@autostart.service`, `Loaded: ... (/home/vgpnk/.config/autostart/
walker.desktop; generated)`, `Active: active (running) since Tue 2026-10-13
11:02:08 -03; 22h ago`, `Main PID: 1808 (walker)`. The desktop file is
byte-identical to the stock one
(`~/.local/share/omarchy/default/walker/walker.desktop:1-7` →
`Exec=walker --gapplication-service`).
**OBS** — `~/.config/hypr/autostart.conf` does **not** launch walker (it holds
only the commented template at `:1-2` and the Grok Bot exec-once at `:5`).
**OBS** — the actual app-launch path is `omarchy-launch-walker:5-14`: it starts
`elephant` if absent (`:5-7`), ensures the walker service (`:10-12`), then
execs `walker --width 644 --maxheight 300 --minheight 300 "$@"` (`:14`).
**OBS** — `systemctl --user is-enabled elephant.service` → `enabled`.
**OBS** — restart path `omarchy-restart-walker:5-15` restarts
`elephant.service` when enabled, then `app-walker@autostart.service`; if the
latter is not enabled the script prints `Unable to restart Walker -- RESTART
MANUALLY`.
**OBS** — `~/.config/hypr/bindings.conf` has **no active launcher bind**: the
only walker reference is commented (`:40`, `# bind = SUPER, PERIOD, exec,
omarchy-launch-walker -m symbols`); `:35` (`omarchy menu` on SUPER+SPACE) and
`:38` (screenshot on SUPER+SHIFT+S) are also commented out.
**INF** — on this host Walker is reached through the Omarchy menu (bar
left-click, `config.jsonc:57`) rather than a standing keybind; whether a
stock binding under `~/.local/share/omarchy/default/hypr/bindings/` opens it is
**UNK** (not read in this pass).
**OBS** — `omarchy-launch-screensaver:18` runs `walker -q` before drawing the
screensaver: the idle screensaver deliberately dismisses the launcher.
**OBS** — `walker --help` exposes `--provider`, `--set`, `--inputonly`,
`--password`, `--selectsingle`, `--height` etc.; `walker --version` → `2.17.0`.

---

## 4. Notification / OSD plane

**OBS** — `~/.config/mako/config` is 5 lines: it includes
`~/.local/share/omarchy/default/mako/core.ini` (`:1`) and overrides exactly
three colors — `text-color=#bebebe`, `border-color=#e68e0d`,
`background-color=#121212` (`:3-5`).
**OBS** — D-Bus: `dbus-send ... GetNameOwner org.freedesktop.Notifications` →
`:1.44`; `busctl --user status org.freedesktop.Notifications` → `PID=1706`,
`PPID=1671`, `UID=1000` — and PID 1706 is `/usr/bin/mako`. **OBS** therefore:
Mako owns the notification name; swayosd-server (PID 1815) does not.
**OBS** — stock `core.ini` behavior: anchor top-right (`:1`), grouped by
app/summary/body (`:2`), 5000 ms default timeout (`:3`), width 420 (`:4`),
border 2 (`:7`), Spotify notifications invisible (`:11-12`), `do-not-disturb`
mode invisible (`:14-15`) **except** for `notify-send` (`:17-18`), critical
urgency sticky on overlay layer (`:20-22`).
**OBS** — `core.ini:24-37` wires click actions to the bar/launcher plane:
Wi-Fi (`omarchy-notification-dismiss` + `omarchy-launch-wifi`), Update System,
Learn Keybindings (`omarchy-menu-keybindings`), Voxtype install, and a
Screenshot toast with `max-icon-size=80`.
**OBS** — live mode value: `makoctl mode` → `default` (no do-not-disturb).
**OBS** — `~/.config/swayosd/config.toml` (4 lines): `show_percentage = true`,
`max_volume = 100`, `style = "~/.config/swayosd/style.css"` (`:2-4`).
`style.css:1` imports `../omarchy/current/theme/swayosd.css`, sets window
opacity 0.97, 2px `@border-color` border, 11pt `JetBrainsMono Nerd Font`.
**UNK** — no measurement in this pass ties swayosd-server to a specific key
(volume/brightness OSD), and `swayosd-client` was not observed running; the
"which keys raise the OSD" question is open.

---

## 5. Idle / lock plane

**OBS** — `~/.config/hypr/hypridle.conf` (19 lines) hooks the lock plane to
Omarchy helpers, not to raw `hyprlock`:
`lock_cmd = omarchy-system-lock` (`:2`);
`before_sleep_cmd = OMARCHY_LOCK_ONLY=true omarchy-system-lock` (`:3`);
`after_sleep_cmd = sleep 1 && omarchy-system-wake` (`:4`);
`inhibit_sleep = 3` (`:5`, file comment: "wait until screen is locked").
**OBS** — two listeners: `timeout = 150` → `pidof hyprlock ||
omarchy-launch-screensaver` (`:9-12`); `timeout = 152` →
`omarchy-system-lock` on timeout, `omarchy-system-wake` on resume (`:15-18`).
The file's own comment (`:14`) states the 2 s margin exists because the
screensaver resets the idle timer.
**OBS** — `omarchy-system-lock:8-13` spawns `hyprlock` only when
`pidof hyprlock` is empty, runs `omarchy-system-wake` after it exits (`:11`),
resets the keyboard layout to the first layout (`:16`), locks 1password when
running (`:19-21`), and kills any screensaver (`:24`).
**OBS** — `omarchy-launch-screensaver:5-7` exits 1 if `tte` is missing; `:10`
exits 0 if `org.omarchy.screensaver` already runs; `:13-15` honors a
`screensaver-off` toggle flag.
**OBS** — `~/.config/hypr/hyprlock.conf` (43 lines) sources the theme variables
first (`:1`), sets `ignore_empty_input = true` (`:3-5`), blurs the current
wallpaper 3 passes (`:7-12`), disables animations (`:14-16`), and defines a
650×100 centred input field (`:18-39`) with `placeholder_text = Enter Password`
(`:32`) and `fail_text = <i>$FAIL ($ATTEMPTS)</i>` (`:34`).
Fingerprint auth is explicitly off: `auth { fingerprint:enabled = false }`
(`:41-43`).
**OBS** — theme values come from
`~/.config/omarchy/current/theme/hyprlock.conf:1-5`: `$color`, `$inner_color`,
`$outer_color` `rgba(190,190,190,1.0)`, `$font_color`, `$check_color`
`rgba(230,142,13,1.0)`.
**INF** — `fingerprint:enabled = false` (`hyprlock.conf:42`) means the
fingerprint reader, if any, is unused at the lock screen; this was a deliberate
setting, not a default (its value is overridden here, whereas `hyprlock.conf:1`
imports the theme for colors only).

---

## 6. Local drift vs stock Omarchy (measured by diff)

**OBS** — the refresh source for the bar is
`~/.local/share/omarchy/config/waybar/{config.jsonc,style.css}` (182 and 111
lines) and the refresh tool is `omarchy-refresh-waybar:6-8`:
`omarchy-refresh-config waybar/config.jsonc`, `.../style.css`, then
`omarchy-restart-waybar`. `omarchy-refresh-config:23` names the backup
`<config>.bak.$(date +%s)` and `:35-39` deletes the backup when the refreshed
file is unchanged, otherwise prints the diff.

**OBS** — real local drift, all of it lost by a refresh:
1. `config.jsonc:81-86` — added `clock#secondary` (Asia/Shanghai) *and* its rail
   entry `config.jsonc:13`.
2. `config.jsonc:235-248` — added `custom/ai-usage` *and* its rail entry
   `config.jsonc:23`.
3. `config.jsonc:56` — the Omarchy glyph is a raw PUA character in the user
   file where stock writes `\ue900`.
4. `style.css:11,63,91` — font sizes raised 12→13px and 10→11px.
5. `style.css:110` and `style.css:113-136` — the `#a55555` recording color and
   the whole ai-usage chip block (25 lines).
6. Reformatting only (multi-line arrays) at `config.jsonc:7-20,95-101,
   119-142,174-178,187-190` — no behavior change.

**OBS** — backup archaeology in `~/.config/waybar/`:
| File | mtime | ctime | size |
|---|---|---|---|
| `config.jsonc` | 2026-10-11 10:36:11 | 2026-10-11 10:36:11 | 6068 |
| `config.jsonc.bak` | 2026-10-11 10:36:07 | 2026-10-11 10:36:07 | 5892 |
| `config.jsonc.bak.1791314470` | 2026-10-03 17:44:32 | 2026-10-03 17:44:32 | 5114 |
| `style.css` | 2026-10-06 16:21:10 | 2026-10-06 16:21:10 | 1887 |
| `style.css.bak.1791314470` | 2026-10-03 19:02:29 | 2026-10-06 16:21:10 | 1458 |
| `style.css.bak.20261003-190229` | 2026-10-03 19:02:29 | 2026-10-03 19:02:29 | 1458 |

**INF** — reading the table: `style.css` changed at 2026-10-06 16:21:10, the
same second as `~/.local/bin/ai-usage`,
`~/.config/hypr/ai-usage.conf` and `~/.config/hypr/hyprland.conf` — the
ai-usage deployment moment; the pre-change CSS was copied with times preserved
(ctime = name epoch 1791314470 = 2026-10-06 16:21:10, mtime = source mtime
2026-10-03 19:02:29). `config.jsonc` changed at 2026-10-11 10:36:11, four
seconds after its un-suffixed `.bak` — the `clock#secondary` edit.
**UNK** — the un-suffixed `config.jsonc.bak` names no tool and its timestamp
format differs from the `.bak.$(date +%s)` and `.bak.20261003-190229` formats
seen elsewhere; the tool that produced it was not identified. Also unresolved:
`config.jsonc.bak.1791314470` carries name-epoch 2026-10-06 16:21:10 but
mtime/ctime 2026-10-03 17:44:32 — the name and the metadata disagree.
**INF** — `custom/update`'s 6 h interval (`config.jsonc:67`) plus the
`signal: 7` reset path (`omarchy-update-available-reset:5`) implies the update
icon is push-driven, while the exec itself is polled.

---

## 7. Decision table (falsifiable operating rules)

| Situation | Action | Why (anchor) |
|---|---|---|
| Change bar layout/modules | edit `~/.config/waybar/config.jsonc`, then `omarchy restart waybar` | `omarchy-restart-waybar:6` `pkill -9 -x waybar` + respawn; `config.jsonc:2` reloads **style** only |
| Change bar colors | edit the **theme** `~/.config/omarchy/current/theme/waybar.css` for fg/bg; hardcoded `#a55555` (`style.css:96,101,110,135`) must be edited in `style.css` | theme file has exactly 2 colors (theme `waybar.css:1-2`) |
| Reset bar to stock | `omarchy refresh waybar` — **destroys** §6 items 1-5 | `omarchy-refresh-waybar:6-7` copies stock over the user file |
| Move the idle/lock timings | edit `~/.config/hypr/hypridle.conf` listeners (`:10, :16`) | measured timeouts 150 s screensaver / 152 s lock |
| Silence notifications | toggle DND (mako mode), not a bar setting; verify with `makoctl mode` | `notification-silencing.sh:3`; live value `default` |
| Restart the launcher | `omarchy restart walker` | `omarchy-restart-walker:5-15` (also restarts elephant when enabled) |
| Ring the bar from a script | `pkill -RTMIN+<n> waybar` with n from §2.3 | consumers at `config.jsonc:66,203,209,215,239` |
| Diagnose "bar shows stale value" | check the module's producer/probe, not waybar: hypridle exists? mako mode? gpu-screen-recorder running? | `idle.sh:3`, `notification-silencing.sh:3`, `screen-recording.sh:3` |

---

## 8. Unknowns (open, not filled by inference)

1. Which stock hypr binding (if any) launches Walker on this host — the user
   `bindings.conf` only has it commented (`bindings.conf:40`); the stock
   bindings tree under `~/.local/share/omarchy/default/hypr/bindings/` was not
   read.
2. Which key raises the swayosd OSD, and whether `swayosd-client` is invoked
   anywhere (only `swayosd-server` PID 1815 was observed).
3. Whether `custom/weather` currently returns an icon or the `unavailable`
   class — `weather.sh:5-9` has both branches; no live waybar IPC read was made.
4. What `$OMARCHY_PATH` resolves to in the waybar process environment.
5. Which tool wrote `~/.config/waybar/config.jsonc.bak` (un-suffixed).
6. `hyprlock`/`hypridle` were not running at measure time, so the lock screen
   was not observed end-to-end; §5 is config-only plus helper-script reading.
7. Whether any `~/.config/omarchy/hooks/theme-set` hook rewrites the waybar
   files on theme change (hooks dir exists, contents not read in this pass).

## 9. Rejections (kept)

- "SUPER+SPACE opens the Omarchy menu" — **rejected as an active binding on
  this host**: `bindings.conf:35` is commented out, and the same file's
  `# unbind` template (`:34`) plus the absence of a stock check make the
  claim unverified here. Kept because the commented line is exactly the trap
  the next reader will fall into.
- "Mako and swayosd compete for notifications" — **rejected**: the D-Bus name
  is held by Mako alone (§4, `busctl` PID=1706).

## 10. Errata (append-only)

_No errata yet. New entries append below this line; earlier text is never
edited — a correction is a new block citing the block it corrects._

## Errata (round 2) — appended 2026-10-14 (MADO-R2-3)

Append-only block; nothing above this line is edited. Sources: wave-1 record
items plus a number re-measure pass by MADO-R2-3 (read-only probes staged at
`/tmp/mado-r2-3-probe/`, ephemeral). Number-touching corrigenda re-measured;
judgment items recorded with their measured pairs.

- **R2-E1 (number-touching corrigendum, re-measured).** §1's table lists
  `~/.config/mako/config` as **50 B**; live `wc -lc` → `5 119` — **119 B**.
  The content is the measured one (full sha256
  `95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec`
  = the recorded `95bf0c86c955cc81…`), so the byte cell was a transcription
  error; §4's 5-line structure (:1 include, :3-5 three colours) holds.
- **R2-E2 (judgment-class — §8 U1 resolved; §9's stated reason superseded).**
  The stock bindings tree was read and the pair re-measured live:
  `~/.local/share/omarchy/default/hypr/bindings/utilities.conf:2` =
  `bindd = SUPER, SPACE, Launch apps, exec, omarchy-launch-walker`; `:7` =
  `bindd = SUPER ALT, SPACE, Omarchy menu, exec, omarchy-menu`;
  `hyprctl binds -j` shows modmask 64 SPACE → `omarchy-launch-walker` and
  modmask 72 SPACE → `omarchy-menu`; `omarchy menu keybindings --print` →
  `SUPER + SPACE → Launch apps`, `SUPER ALT + SPACE → Omarchy menu` (the
  menu also sits on COPILOT KEY). Therefore §8 U1 is answered — SUPER+SPACE,
  stock, launches Walker — and §9's rejection *direction* stands
  (SUPER+SPACE does not open the Omarchy menu) while its wording "rejected
  as an active binding" and "the absence of a stock check … unverified here"
  are superseded: the claim is verified false, not merely unverified, and
  the local `bindings.conf:34-35` pair is the commented *overwrite* template
  for that key.
- **R2-E3 (number-touching — round-1 note-length pin, re-measured).** The
  round-1 body (commit `65a2254`) is **364 lines by `wc -l`** (365 in editor
  view; no trailing newline — `tail -c 1` → `_`); this block extends it.
  Quotes must name the command (SKILL.md "Round 1 sources" quotes the editor
  count of the round-1 body).
- **R2-E4 (re-measure held, plus one addition to §6's drift list).** §1/§2/
  §4/§6/§7 numbers re-checked: `config.jsonc` 249 L / 6,068 B /
  `07f7d663106b72e4`; `style.css` 136 L / 1,887 B / `8316c08ceaa7e3f0`;
  walker 49 L / 1,336 B; swayosd 4 L / 87 B; theme `waybar.css` 2 L;
  `walker.css` 6 L; PIDs 1707/1706/1808/1815 all `STARTED Tue Oct 13
  11:02:07`; versions v0.15.0 / 2.17.0 / v0.1.8 / v0.9.6 / 0.3.2;
  `makoctl mode` → `default`; hypridle absent + `inactive`; signals
  `config.jsonc:66/203/209/215/239`; `#a55555` at `style.css:96/101/110/135`.
  Diffs vs stock reproduce §6 items 1-6, with one addition to item 6:
  `config.jsonc` also drops one stock blank line (stock `:56` → local `:68`)
  — no behaviour change.

## Errata (round 4) — appended 2026-10-14 (ERR-M; applies MADO-R3-1 §8)

Append-only block; nothing above this line is edited. Sources: the 7 divergence
candidates recorded in `waybar-walker-semantics.md` §8 (round 3), applied by the
round-4 errata sweep, plus one provenance corrigendum (R4-E8). Re-measured
read-only 2026-10-14 16:20–16:25 UTC; scratch `/tmp/w4-err-m-sweep/`. Live
values are point samples: the compositor session was replaced at ~16:11:06–07
UTC (new Hyprland PID 1203316, `hyprctl -j instances` `time` 1791994267 =
16:11:07 UTC; waybar now PID 1203352, mako 1203350) — round-1 PIDs (1707 etc.)
no longer resolve.

- **R4-E1 (addition — `custom/voxtype`; MADO-R3-1 §8.1).** The module is
  configured (`config.jsonc:16`, `:218-229`; `exec` = `omarchy-voxtype-status`)
  but `voxtype` is not installed — `command -v voxtype` → rc=1 — so the
  producer's else-branch payload `{"alt": "", "tooltip": ""}` renders the
  module invisible (**RUN**, measured by R3-1; not re-run here). Hazard kept:
  line 5 of `~/.local/share/omarchy/bin/omarchy-voxtype-status` is
  `trap 'kill 0' EXIT` — it SIGTERMs its own process group; R3-1 measured a
  direct invocation killing the caller (exit 143) and contained its re-run
  under `setsid`. Script bytes re-read; trap line present; producer
  deliberately not executed.
- **R4-E2 (addition — `battery`; §8.2).** No battery device on this host:
  `/sys/class/power_supply/` → 0 entries (re-measured), so the capacity source
  is absent and the right-click script would emit blanks; `waybar-battery(5)`
  documents no no-device rendering ⇒ live value stays **UNK**.
- **R4-E3 (correction — walker `[columns]` comment; §8.3).** Local
  `~/.config/walker/config.toml:14` says `symbols = 1 # providers to be
  queried by default`; that role belongs to `[providers] default` (local
  `:16-21`; packaged `/etc/xdg/walker/config.toml:53-58`, whose own comment
  reads "providers to be queried by default"). `[columns] symbols` is the
  provider grid column count — packaged `[columns] "symbols" = 3`
  (`/etc/xdg/walker/config.toml:31-32`). The user file's inline comment is
  wrong; semantics are R3-1 §6.3.
- **R4-E4 (version-pin caveat; §8.4).** Omarchy carries two pins that must be
  named: `omarchy version` → `3.8.3`, while the checkout's
  `git -C ~/.local/share/omarchy describe --tags` → `v3.8.4` (branch `master`;
  clean — `status --porcelain` empty). Both re-measured.
- **R4-E5 (contradiction — `pkill -RTMIN+N`; §8.5).** Re-measured, contained,
  against a scratch process: a copy of `/usr/bin/sleep` named `wsig` died to
  `pkill -x -RTMIN+11 wsig` → pkill rc=0, wait status 173 (= 128+45 =
  SIGRTMIN+11) under **procps-ng 4.0.7** (`pkill --version`). This
  contradicts the docstring claim in `~/.local/bin/ai-usage:150-156` that
  "`pkill -RTMIN+N` is not a signal procps-ng accepts"; R3-1's `caught=45`
  result reproduces, and the round-1 producer list stands as recorded.
- **R4-E6 (addition — tray live state; §8.6).** `busctl --user get-property
  fr.arouillard.waybar /StatusNotifierWatcher org.kde.StatusNotifierWatcher
  RegisteredStatusNotifierItems` → `as 0`; `ProtocolVersion` → `i 0`; the bus
  name is `fr.arouillard.waybar` (`busctl --user list`). The drawer is empty
  by data, not by bug. (The double-r spelling `fr.arrouillard…` carried in
  round-3 SKILL.md is a typo; the worktree's round-4 SKILL edit reads
  single-r.)
- **R4-E7 (addition — signal offset is self-read; §8.7).** `ai-usage` does not
  assume offset 11: `waybar_signal()` regex-reads the `signal` value out of
  `~/.config/waybar/config.jsonc` (`~/.local/bin/ai-usage:127-148`; range
  guard `11 <= sig < 31`, fallback 11). Re-read; script path is
  `~/.local/bin/ai-usage`. Consequence stands: changing the config number
  keeps clicks working; changing it with a stale cache does not.
- **R4-E8 (corrigendum-of-corrigendum — mako 50 B provenance).** R2-E1 above
  attributed the round-1 "50 B" cell to a "transcription error"; the measured
  provenance (MADO-R3-2 §3.1, re-measured here) is: `~/.config/mako/config`
  is a **symlink** → `~/.config/omarchy/current/theme/mako.ini`, and "50" was
  the symlink's own `ls` size string — the two historical numbers measure
  different objects. The corrected content cell (5 L / 119 B, sha
  `95bf0c86c955cc81…`) stands as written.