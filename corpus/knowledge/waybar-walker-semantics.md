# Waybar / Walker semantics — module-by-module (MADO-R3-1)

Lane: mado-shokunin. Assignment MADO-R3-1 (round 3, probation-completing).
Measured 2026-10-14 on host `plazir27`, session started 2026-10-13 11:02.
Substrates were READ-ONLY: no file under `~/.config/`, `~/.local/share/omarchy/`,
`~/Projects/` was written; no compositor or bar state was mutated; no external
site was contacted (the two network-using producers were read, never run).
Probe scratch: `/tmp/mado-r3-1-probe/` (man renders, codepoint map, signal test).

Tag legend — **OBS** measured (file bytes, command output, D-Bus property),
**MAN** value from the locally installed man page for the installed package,
**RUN** payload produced by executing a read-only producer script,
**INF** inference with its basis stated, **UNK** not measurable this pass.
Every non-MAN row carries a `path:line` or a command line.

---

## §1 Live snapshot (this pass)

| Component | Version (measured) | Runtime evidence |
|---|---|---|
| waybar | `waybar --version` → `Waybar v0.15.0`; pkg `0.15.0-3` | PID 1707, elapsed 89,039 s, cmdline `/usr/bin/waybar` (no `-c`/`-s`), parent = Hyprland PID 1671 (`ps -o pid,ppid,cmd`) |
| walker | `walker --version` → `2.17.0`; pkg `2.17.0-1` | PID 1808, `walker --gapplication-service`, parent `systemd --user` (1573) |
| elephant | pkg `2.21.0-1` | PID 1811, `elephant` |
| omarchy | `omarchy version` → `3.8.3` | git checkout `~/.local/share/omarchy` = tag **v3.8.4**, branch `master`, `status --porcelain` empty |

**OBS** — bar surface: `hyprctl layers -j` → DP-1, level 2 (top), `namespace: "waybar"`,
`pid: 1707`, `xywh: 0 0 3440 26`, `alpha: 1`. Level 0 holds `wallpaper` (pid 1710).
`hyprctl monitors -j` → DP-1 `reserved: [0, 26, 0, 0]`, scale 1, focused.
This is the live pair for `config.jsonc:3-6` (`layer top`, `position top`, `height 26`).

**OBS** — D-Bus ownership (`busctl --user list`, `busctl --user tree`):
`fr.arouillard.waybar` (waybar, :1.50/:1.51), `org.kde.StatusNotifierWatcher` and
`org.kde.StatusNotifierHost-1707-0` (waybar), `dev.benz.walker` (walker, :1.22),
`org.freedesktop.Notifications` (mako 1706), `org.erikreider.swayosd[-server]` (1815).

**OBS** — sockets (names only): `$XDG_RUNTIME_DIR/walker/walker.sock`,
`$XDG_RUNTIME_DIR/elephant/elephant.sock`, both `srwxr-xr-x`, created 2026-10-13 11:02.

**OBS** — systemd user units: `elephant.service` active/enabled (MainPID 1811);
`app-walker@autostart.service` active, `UnitFileState=generated`, MainPID 1808;
`ai-usage.timer` active (next fire ≈5 min cadence), `ai-usage.service` one-shot
`inactive/dead` ("Probe AI CLI usage limits into cache").

**OBS** — hardware plane the modules read: `/sys/class/power_supply/` is **empty**
(no battery, no AC adapter — desktop host); `ip -br link` → `enp7s0` UP,
`wlan0` DOWN `NO-CARRIER`; `iw dev` → one managed phy; BlueZ `hci0` present,
`Adapter1 Powered=true`, `Discoverable=false`, 0 device objects,
`rfkill` hci0 soft/hard unblocked; PipeWire 1.6.8 with waybar as client
`58. waybar [1.6.8, pid:1707]` (`wpctl status`).

**OBS** — tray state: `busctl --user get-property fr.arouillard.waybar
/StatusNotifierWatcher org.kde.StatusNotifierWatcher RegisteredStatusNotifierItems`
→ `as 0` (empty), `IsStatusNotifierHostRegistered` → `b true`, `ProtocolVersion` → `i 0`.

**OBS** — no GTK actions anywhere: `org.gtk.Actions.List` on both
`fr.arouillard.waybar` and `dev.benz.walker` → `as 0`. Neither app exposes a
control action surface; activation via `org.freedesktop.Application` exists but
is unused by this config.

**OBS** — walker is idle as a service: `hyprctl layers -j` shows no walker layer
surface (only `wallpaper` + `waybar`), i.e. the launcher is closed.

---

## §2 Bar-level semantics (the container)

### 2.1 What `config.jsonc` declares

| Key | Value | Anchor | Semantics (MAN `waybar(5)`) | Live check |
|---|---|---|---|---|
| `reload_style_on_change` | `true` | `config.jsonc:2` | reload CSS when the style sheet **or any imported css** changes; default false | style edits live; module edits do **not** (man: only style) |
| `layer` | `top` | `:3` | top = in front of windows (default bottom) | layers level 2 = top |
| `position` | `top` | `:4` | top/bottom/left/right (default top) | reserved top strip |
| `spacing` | `0` | `:5` | gaps between modules | — |
| `height` | `26` | `:6` | bar height if possible | layer `h: 26`, `reserved [0,26,0,0]` |
| `modules-left` | 2 modules | `:7-10` | rail order | — |
| `modules-center` | 8 modules | `:11-20` | rail order | — |
| `modules-right` | 7 entries | `:21-29` | rail order (first = group leader host) | — |

Not declared (so MAN defaults apply): `name`, `output`, `mode`, `start_hidden`,
`expand-left/center/right`, `passthrough`, `include`, `margin`.

### 2.2 Which file the live bar read

**OBS** — cmdline has no `-c`; `waybar --help` lists `-c <config>` / `-s <style>`.
**MAN** — `waybar(5)` resolves, in order, `$XDG_CONFIG_HOME/waybar/`,
`~/.config/waybar/`, `~/waybar/`, `/etc/xdg/waybar/`. ⇒ the live bar reads
`~/.config/waybar/config.jsonc` + `style.css` (the only user-path config).
Packaged fallback exists at `/etc/xdg/waybar/{config.jsonc,style.css}`
(`pacman -Ql waybar`); omarchy's own stock copy is
`~/.local/share/omarchy/config/waybar/` (refresh source, round-1 §6).

### 2.3 Introspection capability ledger — what can and cannot be measured

| Question | Surface | Verdict |
|---|---|---|
| Is the bar mapped, where, how big? | `hyprctl layers -j`, `hyprctl monitors -j` | **OBS** |
| Which process/args? | `ps`, `busctl` | **OBS** |
| Does it own the tray? | StatusNotifierWatcher props | **OBS** (0 items) |
| Any app-level actions? | `org.gtk.Actions.List` | **OBS** (none) |
| What text does module X show right now? | none — waybar has **no IPC/query verb** in 0.15.0 (`waybar --help` = config/style/log/bar only) | **UNK**; reconstruct from the producer's own output (**RUN**) where the producer is pure-read |
| Env of the waybar process (`$OMARCHY_PATH` for two `exec` lines) | `/proc/<pid>/environ` is barred (session material) | **UNK** |
| Waybar's stderr/log | not captured this pass | **UNK** |

---

## §3 Module-by-module semantics

Column key: **Displays** = config bytes; **Source** = what feeds it;
**Actions** = clicks/scroll; **Fails** = failure modes; **Live** = this pass.
Glyphs are given as codepoints so the bytes are unambiguous (map:
`/tmp/mado-r3-1-probe/codepoints.txt`).

### 3.1 Left rail

| Module (anchor) | Displays | Source | Actions | Fails | Live |
|---|---|---|---|---|---|
| `custom/omarchy` (`:55-60`) | static `<span font='omarchy'>` + **U+E900** (`:56`; stock writes the escape `\ue900`, `~/.local/share/omarchy/config/waybar/config.jsonc:43`) | none — no `exec` | L → `omarchy-menu`; R → `xdg-terminal-exec` | glyph font absent ⇒ tofu (`fc-list` has exactly 1 `omarchy` face: `~/.local/share/fonts/omarchy.ttf`); `omarchy-menu` needs walker+elephant | not opened (no mutation) → menu state **UNK** |
| `hyprland/workspaces` (`:30-53`) | `{icon}`; icons `default`=U+EA71 (`:34`), `1`…`9` digits, `10`→`0`, `active`=U+F14FB (`:45`); `persistent-workspaces` 1–5 (`:47-53`) | Hyprland IPC | L → `activate` (`:31`) = focus/create workspace | no session env ⇒ module errors (**INF**); >5 workspaces fall back to `default` icon; 1–5 render as placeholders even when the compositor has none | `hyprctl workspaces -j` = **only ws 1** (3 windows, `ispersistent:false`); `activeworkspace` = 1 |

**Semantics worth stating.** `persistent-workspaces` does not make Hyprland
workspaces persistent — it only pins *bar buttons*: MAN `waybar-hyprland-workspaces(5)`
example `"*": 5, // 5 workspaces by default on every monitor`. Class hooks are
`.active/.empty/.visible/.persistent/.special/.urgent` (MAN §Style); this
stylesheet uses only `.empty` (`style.css:29-31`) and the generic button rule
(`:22-27`).

### 3.2 Center rail

| Module (anchor) | Displays | Source | Actions | Fails | Live |
|---|---|---|---|---|---|
| `clock` (`:75-80`) | `{:L%A %H:%M}` (locale weekday + time), alt `{:L%d %B W%V %Y}` (`:77`), `tooltip:false` (`:78`) | wall clock; `interval` default 60 s (MAN `waybar-clock(5)`) | R → `omarchy-launch-floating-terminal-with-presentation omarchy-tz-select` (`:79`) | timezone picker needs `gum` + `sudo timedatectl`; the script then runs `omarchy-restart-waybar` | rendered text not screen-read → **UNK** (format is certain) |
| `clock#secondary` (`:81-86`) | `BJ {:L%H:%M}`, alt `BJ {:L%d %B W%V %Y}` | same clock engine, `timezone: "Asia/Shanghai"` (`:82`) | inherits clock defaults (no clicks declared) | obsolete tz database name ⇒ empty/error (**INF**) | same |
| `custom/weather` (`:87-93`) | `{text}` = weather icon from `weather.sh`; `class:"unavailable"` when absent | `exec: $OMARCHY_PATH/default/waybar/weather.sh` (`:88`), json, interval 60 (`:90`) → `omarchy-weather-icon` → `curl -fsS --max-time 3 https://wttr.in?format=j1` (`omarchy-weather-icon:5`) | L → `notify-send -u low "$(omarchy-weather-status)"` (`:92`; that status script curls `wttr.in?format=%l|%t|%w`) | offline/DNS/slow ⇒ `{"text":"","class":"unavailable"}` (`weather.sh:9`), styled to collapse to nothing (`style.css:75-79`); depends on `$OMARCHY_PATH` in the bar's env (**UNK**, §2.3) | **not run** (network); value UNK |
| `custom/update` (`:61-68`) | glyph U+F021 (`:62`) + text from script, `tooltip-format` static "Omarchy update available" (`:65`) | `exec: omarchy-update-available` (`:63`), `signal 7` (`:66`), `interval 21600` (6 h, `:67`) | L → floating terminal `omarchy-update` | script needs network (`git ls-remote origin`, `omarchy-update-available:5`) and a git checkout; offline it prints `Error: Could not retrieve latest tag.` + exit 1 (`:6-9`); how a non-zero exit renders (text vs. kept value) is MAN-undocumented → **UNK** | local baseline measured **v3.8.4** (`git describe --tags`), while `omarchy version` says 3.8.3; remote side **not fetched** ⇒ UNK |
| `custom/voxtype` (`:218-230`) | `{icon}` keyed `idle` (none), `recording` U+F036C (`:224`), `transcribing` U+F051F (`:225`) | `exec: omarchy-voxtype-status` (`:219`), json, **no interval, no signal** ⇒ script must self-loop (MAN `waybar-custom(5)`: "If no interval or signal is defined, it is assumed that the out script loops itself") | L → `omarchy-voxtype-model` (`:229`); R → `omarchy-voxtype-config` (`:228`) | `voxtype` is **not installed** on this host (`command -v voxtype` → missing) ⇒ script's else branch; the script's `trap 'kill 0' EXIT` (`omarchy-voxtype-status:5`) SIGTERMs **its own process group** — measured: running it directly killed the invoking shell (wrapper exit 143) | **RUN** payload `{"alt": "", "tooltip": ""}` ⇒ no icon, module invisible; waybar surviving 24.7 h with this module configured implies its exec children get their own process group (**INF**) |
| `custom/screenrecording-indicator` (`:200-205`) | `{text}` glyph U+F0EC2 when active | `exec: …/indicators/screen-recording.sh` (`:202`), json, `signal 8` (`:203`) → `pgrep -f "^gpu-screen-recorder"` (`screen-recording.sh:3`) | L → `omarchy-capture-screenrecording` (`:201`) — start/stop recording; also rings the bar: `omarchy-capture-screenrecording:253` `pkill -RTMIN+8 waybar` | needs `gpu-screen-recorder` (present) and an existing `~/Videos` (`omarchy-capture-screenrecording:22-27`) | **RUN** `{"text": ""}` → inactive (no recorder running, `pgrep` empty) |
| `custom/idle-indicator` (`:206-211`) | U+F1AD6 + tooltip "Idle lock disabled", `class:active`, when hypridle is **absent** | `exec: …/indicators/idle.sh` (`:208`), `signal 9` (`:209`) → `pgrep -x hypridle` (`idle.sh:3`) | L → `omarchy-toggle-idle` (`:207`) — kill hypridle, else `uwsm-app -- hypridle`; then `pkill -RTMIN+9 waybar` (`omarchy-toggle-idle:13`) | module semantics inverted vs. intuition: glyph shown = lock disabled, not "idle now" | **RUN** `{"text": "󱫖", "tooltip": "Idle lock disabled", "class": "active"}`; `pgrep -x hypridle` empty |
| `custom/notification-silencing-indicator` (`:212-217`) | U+F009B + "Notifications silenced", `class:active`, while DND is on | `exec: …/indicators/notification-silencing.sh` (`:214`), `signal 10` (`:215`) → `makoctl mode \| grep -q do-not-disturb` (`:3`) | L → `omarchy-toggle-notification-silencing` (`:213`) → `makoctl mode -t do-not-disturb` + notify-send + `pkill -RTMIN+10 waybar` (`:5-13`) | any mako restart moves the glyph; mako is the source of truth | **RUN** `{"text": ""}` → DND off; `makoctl mode` → `default` |

### 3.3 Right rail

| Module (anchor) | Displays | Source | Actions | Fails | Live |
|---|---|---|---|---|---|
| `group/tray-expander` (`:181-191`) | a **drawer** group: leader `custom/expand-icon`, hidden child `tray` | `drawer.transition-duration:600` (`:184`), `children-class:"tray-group-item"` (`:185`); MAN `waybar(5)` Group Drawers: first module is the leader and never hidden, others get `children-class` while hidden | hover expands | — | drawer currently expands onto nothing (0 SNI items, §1) |
| `custom/expand-icon` (`:192-199`) | glyph U+F053 (`:193`), `tooltip:false` | static | `on-scroll-up/down/left/right` are set to **empty strings** (`:195-198`) — no scroll action; purpose of the empty overrides is **UNK** | — | — |
| `tray` (`:231-234`) | StatusNotifierItem icons, `icon-size:12`, `spacing:17` | waybar itself owns `org.kde.StatusNotifierWatcher` + `StatusNotifierHost-1707-0` (§1) | per-item menues are the client's own | no registered items ⇒ nothing rendered | **OBS** `RegisteredStatusNotifierItems` = `as 0` |
| `custom/ai-usage` (`:235-248`) | `format:"{}"` raw markup (`:243`), meter text from the script | `exec: ~/.local/bin/ai-usage waybar` (`:236`), json, `interval 60` (`:238`) + `signal 11` (`:239`), `escape:false` (`:241`), `exec-on-event:false` (`:242`) ⇒ clicks do not re-exec the script | scroll-↑ `cycle next`, scroll-↓ `cycle prev` (`:244-245`), L `cycle next` (`:246`), R `identity next` (`:247`) | chip is **cache-only** (`ai-usage:2`, argparse help `:2534` "print Waybar JSON from cache only"); cache `~/.cache/ai-usage/status.json` (0600, mtime 11:40 this pass) refreshed by `ai-usage.timer` every 5 min; meters come from `omp usage --json` (`:406-408`); `~/.config/ai-usage/env` exists 0600 — **shape only, never read** | **RUN** payload: `text` = `K` + two span-rendered meter bars, `class` = `ok`, `alt` = `kimi`, tooltip 9 lines |
| `bluetooth` (`:155-163`) | glyph U+F294 (`:156`); off/disabled U+F00B2 (`:157-158`), connected U+F00B1 (`:159`), no-controller = "" (`:160`); tooltip "Devices connected: {num_connections}" (`:161`) | BlueZ D-Bus (module-native; `bluetoothctl` is **not installed** and is not needed) | L → `omarchy-launch-bluetooth` (`:162`) → `rfkill unblock bluetooth; omarchy-launch-or-focus-tui bluetui` (`omarchy-launch-bluetooth:5-6`) | no adapter ⇒ empty text (silent disappearance); `bluetui` missing ⇒ click does nothing visible | adapter exists, `Powered=true`, 0 devices ⇒ branch selection **INF/UNK** (`format` vs `format-off`) |
| `network` (`:94-112`) | `format-icons` 5 wifi steps U+F092F…U+F0928 (`:96-100`), `format-wifi`=`{icon}` (`:103`), ethernet U+F0002 (`:104`), disconnected U+F092E (`:105`); tooltip wifi `{essid} ({frequency} GHz)` (`:106`) | libnl/sysfs, `interval 3` (`:109`) | L → `omarchy-launch-wifi` (`:111`) → `rfkill unblock wifi; omarchy-launch-or-focus-tui impala` (`omarchy-launch-wifi:5-6`) | none — the disconnected branch always has an icon; `essid` needs `iw` | `enp7s0` UP, `wlan0` down ⇒ ethernet branch expected (**INF**, interface auto-detection unchanged: no `interface` key) |
| `pulseaudio` (`:164-180`) | `{icon}` (`:165`); muted U+EEE8 (`:170`); icons headphone/headset U+F025 (`:172-173`), default 3-step U+F026/27/28 (`:175-177`) | libpulse against PipeWire (`wpctl` shows waybar as client 58) | L → `omarchy-launch-audio` (`:166`) → wiremix TUI; R → `pamixer -t` mute toggle (`:167`); **scroll** = volume, `scroll-step:5` (`:169`; MAN: replaces default on-scroll only if `on-scroll-*` set — none are) | no sink ⇒ ecosystem problem, not bar | live sink volume 0.40 (PipeWire), module value not screen-read → **UNK** |
| `cpu` (`:69-74`) | glyph **U+F035B only** — `format` has no placeholder (`:71`), so the text never carries a number | sysfs/proc; `interval 5` (`:70`); `tooltip` default true (MAN) | L → `omarchy-launch-or-focus-tui btop` (`:72`) = focus-or-spawn btop in a terminal; R → `alacritty` (`:73`, plain new window) | btop/terminal missing ⇒ click fails silently | reading invisible by design → **UNK** (tooltip-only value) |
| `battery` (`:113-154`) | `{capacity}% {icon}` (`:114`), discharging/charging `{icon}` (`:115-116`), plugged U+F1E6 (`:117`), icons charging 10 + default 10 (`:118-143`), full (`:144`); tooltips `{power:>1.0f}W↓/↑ {capacity}%` (`:145-146`); `states` 20/10 (`:150-153`) | UPower/sysfs; `interval 5` (`:147`) | L → `omarchy-menu power` (`:148`) — reaches `show_setup_power_menu` (`omarchy-menu:871`) = `omarchy-powerprofiles-list` + `powerprofilesctl set`; R → `notify-send "$(omarchy-battery-status)"` (`:149`) | **this host has no battery** (`/sys/class/power_supply/` empty; `upower -e \| grep BAT` empty) ⇒ no capacity source; right-click text degrades to blanks (`omarchy-battery-status:5-19` would read nothing) | module value **UNK**; MAN documents no no-device behavior |

**State classes.** `states: {warning:20, critical:10}` maps to CSS classes by the
rule in `waybar-states(5)`: for battery the class triggers when value ≤ threshold.
The only `states` declaration in the live config is the battery one; no other
module declares `states`.

**`alt` (undocumented).** `men 5 waybar-custom` documents JSON fields
`text/tooltip/class/percentage` only, and `format-icons` selection "based on the
set percentage" — yet both local producers emit `alt`
(`omarchy-voxtype-status:9` rewrites `class`→`alt`; `ai-usage:2383` sets
`alt: pid`) and the configs key icons by those values. The `alt`→icon keying is
therefore **INF** (basis: producer design + config keys); documented behavior is
**UNK**. `ai-usage`'s own `format` is `"{}"`, so its `alt` is informational here.

---

## §4 Signal bus (RTMIN+n → module refresh)

Consumers declared in `config.jsonc`: `7`→`custom/update` (`:66`),
`8`→`custom/screenrecording-indicator` (`:203`), `9`→`custom/idle-indicator`
(`:209`), `10`→`custom/notification-silencing-indicator` (`:215`),
`11`→`custom/ai-usage` (`:239`).

| n | Producer (re-measured this pass) | Line |
|---|---|---|
| 7 | `omarchy-update-available-reset` | `:5` `pkill -RTMIN+7 waybar` |
| 8 | `omarchy-capture-screenrecording` | `:253` `pkill -RTMIN+8 waybar` |
| 9 | `omarchy-toggle-idle` | `:13` `pkill -RTMIN+9 waybar` |
| 10 | `omarchy-toggle-notification-silencing` | `:13` `pkill -RTMIN+10 waybar` |
| 11 | `deploy/waybar-on-click.sh:6` `pkill -x -RTMIN+11 waybar`; plus the CLI path `ai-usage` `poke_waybar()` (`:150-178`) which resolves the offset **by reading `signal` back out of `~/.config/waybar/config.jsonc`** (valid range 11 ≤ n < 31) and `os.kill`s waybar's PIDs | — |

**RUN (this pass)** — delivery mechanism is real on this host:
`pkill -x -RTMIN+11` against a scratch process running a handler for
`SIGRTMIN+11` produced `caught=45 SIGRTMIN=34` (procps-ng **4.0.7**), i.e. the
offset form works. This **contradicts** the in-script claim in `ai-usage:150-153`
("`pkill -RTMIN+N` is not a signal procps-ng accepts") — on this procps version it
parses and delivers. The producers in the table therefore ring the bar as designed.
MAN `waybar-custom(5)` for `signal`: "the number is valid between 1 and N, where
SIGRTMIN+N = SIGRTMAX"; with no `interval` a signal is the *only* refresh path —
which is why the three indicators (no `interval`) move only when their producer fires.

---

## §5 Style map (module → CSS)

`style.css:1` imports `../omarchy/current/theme/waybar.css`, which defines exactly
two colors — `foreground #bebebe`, `background #121212`. Everything else is literal.

| Selector (anchor) | Applies to | Effect |
|---|---|---|
| `*` (`:3-12`) | all | font `JetBrainsMono Nerd Font 13px`, no border/radius |
| `.modules-left` / `.modules-right` (`:14-20`) | rails | 8px outer margins |
| `#workspaces button` (`:22-27`) | workspaces | 6px padding, 1.5px gaps, min-width 9px |
| `#workspaces button.empty` (`:29-31`) | placeholder workspaces 2–5 | opacity 0.5 |
| `#cpu,#battery,#pulseaudio,#custom-omarchy,#custom-update` (`:33-40`) | 5 modules | min-width 12px, margin 0 7.5px |
| `#tray` `:42-44`, `#bluetooth` `:46-48`, `#network` `:50-52`, `#custom-expand-icon` `:54-56` | spacing tuning | 16/17/13/18px right margins |
| `#custom-update` (`:62-64`) | update | 11px |
| `#clock` (`:66-68`), `#custom-weather` (`:70-73`) | center | margins 8.75 / 7.5px |
| `#custom-weather.unavailable` (`:75-79`) | offline weather | collapses to zero size |
| `.hidden` (`:81-83`) | group drawer child | opacity 0 — pairs with MAN `children-class` default `"hidden"` |
| `#custom-screenrecording-indicator,#custom-idle-indicator,#custom-notification-silencing-indicator` (`:85-93`) | indicators | 12px min-width, 11px font |
| `…-indicator.active` (`:95-102`) | indicator on | color `#a55555` (literal) |
| `#custom-voxtype` (`:104-107`), `.recording` (`:109-111`) | voxtype | glyph box; recording = `#a55555` |
| `#custom-ai-usage` (`:113-136`) | chip | 12px, `min-width:0`, pad 2/7, radius 4px; `.unauth/.unknown` 0.7, `.stale` 0.55, `.warn/.critical` `#a55555` |

**OBS** — the four `#a55555` sites (`:96, :101, :110, :135`) and the theme file's
two colors mean a theme switch repaints foreground/background only; every alert
color stays literal. The chip's meter bars carry their own inline colors
(measured payload uses `bgcolor='#3a3a3a'` / `'#f2f2f2'`) and therefore also do
not track the theme (**OBS** payload + **OBS** `style.css:113-136` don't override).

---

## §6 Walker — launcher semantics

### 6.1 Layers

| Layer | Path | Size | Role |
|---|---|---|---|
| packaged default | `/etc/xdg/walker/config.toml` | 298 lines | full default table (inline comments = the closest local documentation) |
| user override | `~/.config/walker/config.toml` | 49 lines | keys that differ; XDG precedence puts `$XDG_CONFIG_HOME` ahead of `/etc/xdg` (**INF**, standard XDG; walker's binary carries `XDG_CONFIG_DIRS`) |
| omarchy theme | `~/.local/share/omarchy/default/walker/themes/omarchy-default/{layout.xml,style.css}` | 156 + 121 lines | named by `theme = "omarchy-default"` + `additional_theme_location` |

### 6.2 User config, key by key (with the packaged counterpart)

| Key (user anchor) | User value | Packaged default (`/etc/xdg/walker/config.toml`) | Semantics |
|---|---|---|---|
| `force_keyboard_focus` (`:1`) | `true` | `false` (`:1`) | keep keyboard focus in walker; walker's own binary warns: "windows might potentially not be focused if force_keyboard_focus is true" (**OBS** `strings /usr/bin/walker`) |
| `selection_wrap` (`:2`) | `true` | `false` (`:6`) | wrap list at ends |
| `theme` (`:3`) | `omarchy-default` | `default` (`:9`) | theme name |
| `additional_theme_location` (`:4`) | `~/.local/share/omarchy/default/walker/themes/` | — | where walker looks in addition to built-ins |
| `hide_action_hints` (`:5`) | `true` | `false` (`:14`) | suppress per-item action hints |
| `[placeholders] default` (`:7-8`) | input `" Search..."`, list `"No Results"` | input `"Search"`, list `"No Results"` (`:35`) | input/empty-list text |
| `[keybinds] quick_activate` (`:10-11`) | `[]` | `["F1","F2","F3","F4"]` (`:47`) | clearing the array disables quick-activation; the packaged block also sets `close/next/previous/…` (`:38-50`) which the user file does not override |
| `[columns] symbols` (`:13-14`) | `1` | `"symbols" = 3` (`:31-32`) | **grid columns for the `symbols` provider** — see §6.3 |
| `[providers] max_results` (`:17`) | `256` | `50` (`:61`) | global result cap |
| `[providers] default` (`:18-21`) | `desktopapplications`, `websearch` | `desktopapplications`, `calc`, `websearch` (`:53-58`) | providers queried without a prefix (user drops `calc`) |
| prefixes (`:23-45`) | `/` providerlist, `.` files, `:` symbols, `=` calc, `@` websearch, `$` clipboard | `;` providerlist, `>` runner, `/` files, `.` symbols, `!` todo, `%` bookmarks, `=` calc, `@` websearch, `:` clipboard, `$` windows (`:69-107`) | prefix→provider routing; the user remaps nearly every prefix |
| (absent) `[providers.actions]` | — | full table `:112-298` with the note "This will be **MERGED/OVERWRITTEN** with what the user specifies" (`:112`) | user drops it ⇒ packaged action bindings (Return/ctrl-*) still apply |
| (absent) `[shell]` | — | `exclusive_zone=-1`, `layer="overlay"`, all four anchors true (`:23-29`) | user drops it ⇒ packaged shell anchors apply ⇒ walker is a full-screen overlay anchored on all sides |
| `[[emergencies]]` (`:47-49`) | text `Restart Walker`, command `omarchy-restart-walker` | — | see §6.4 |

### 6.3 `[columns]` is grid columns, not "providers to be queried" (correction)

The user file's inline comment (`config.toml:14`, "providers to be queried by
default") is **wrong**. Evidence: (a) the packaged default keys the same table by
a *provider name* (`"symbols" = 3`, `/etc/xdg/walker/config.toml:31-32`) while the
"providers to be queried" table is `[providers] default` (`:53-58`); (b) walker's
binary contains GTK `GridView` column properties and a `list_max_columns` field in
its `Providers` struct (**OBS** `strings /usr/bin/walker`); (c) the packaged theme
ships a dedicated `item_symbols_grid.xml` alongside `item_symbols.xml`. ⇒
**INF (high)**: `[columns] <provider> = n` sets the result-grid column count for
that provider; locally `symbols` is forced to a single column.

### 6.4 Emergencies

**OBS** — walker's binary defines `struct EmergencyEntry with 2 elements`, and
carries the strings `failed to run emergency command`, `menus-emergency`,
`Emergency`. **OBS** — the user file declares one entry
(`text = "Restart Walker"`, `command = "omarchy-restart-walker"`). **INF** — it is
a fail-safe row offered by the launcher, distinct from normal results.
**UNK** — the exact condition that surfaces it (no local doc; not triggered
without mutating the running launcher).

### 6.5 Providers and the data engine (elephant)

**OBS** — provider plugins installed: `/usr/lib/elephant/{bluetooth,calc,clipboard,
desktopapplications,files,menus,providerlist,runner,symbols,todo,unicode,websearch}.so`.
All six providers reachable through the live prefix table are present
(providerlist, files, symbols, calc, websearch, clipboard).
**OBS** — elephant config (`~/.config/elephant/`): `calc.toml` `async=false`;
`desktopapplications.toml` `show_actions=false`, `only_search_title=true`,
`history=false`; `symbols.toml` `command = 'wl-copy && hyprctl dispatch
sendshortcut "SHIFT,Insert,activewindow"'` (**`:`** prefix copies the glyph and
synthesises Shift+Insert into the active window); `menus/` holds three Lua
symlinks to `~/.local/share/omarchy/default/elephant/*.lua`
(theme/background/unlock pickers), and the menus may set
`HideFromProviderlist = true` (e.g. `omarchy_background_selector.lua:4`).

### 6.6 Window/layout/theme semantics

**OBS** — `layout.xml`: `GtkWindow#Window` → `BoxWrapper` `width-request 644`
(`:15`) → `Box` (vertical, spacing 10) → `SearchContainer`/`Input` (`:30-48`) →
`ContentContainer` with `GtkGridView` `List` `max_columns 1` (`:96-101`) and a
`Preview` box (`:107`); placeholder labels `"Waiting for elephant..."` (`:67`)
and `"No Results"` (`:75`); `Keybinds` region with global/item keybind boxes
(`:116-136`).
**OBS** — `style.css`: `18px monospace` (`:8-9`); `.box-wrapper` =
`alpha(@base,0.95)` + 2px `@border` (`:25-29`); selected row background
`alpha(@text,0.07)` and `@selected-text` (`:77-83`); `.item-subtext {font-size: 0}`
(`:94-102`) hides provider subtext; `.current {font-style: italic}` (`:109-111`);
`.keybind-hints` panel (`:113-117`). Colors come from
`~/.config/omarchy/current/theme/walker.css` (6 colors; selected `#e68e0d`).
**OBS** — the omarchy theme ships **only** `layout.xml` + `style.css`; the packaged
theme ships 11 `item_*.xml` layouts (incl. `item_symbols_grid.xml`).
**UNK** — which item layout the omarchy theme resolves for each provider (a
fallback to the packaged default theme is **INF**, not measured).
**UNK** — `theme = "omarchy-default"` + `additional_theme_location` resolution
order versus built-in themes (walker ships no man page; `man walker` → "No manual
entry").

### 6.7 Runtime, launch path, standing binds

**OBS** — `walker --gapplication-service` (PID 1808) is a systemd-generated user
service `app-walker@autostart.service`; `~/.local/share/omarchy/default/walker/restart.conf`
is its drop-in (`[Service] Restart=always`, `RestartSec=2`).
**OBS** — launch entry: `omarchy-launch-walker` starts `elephant` if absent (`:5-7`),
starts the walker service if absent (`:10-12`), then execs
`walker --width 644 --maxheight 300 --minheight 300 "$@"` (`:14`) — the geometry
flags match `layout.xml:15` (width 644) and `.scroll max-content-height 300`
(`layout.xml:89`).
**OBS** — restart entry: `omarchy-restart-walker:5-15` restarts
`elephant.service` when enabled and `app-walker@autostart.service` (else prints
`Unable to restart Walker -- RESTART MANUALLY`).
**OBS** — standing binds that open the launcher (`hyprctl binds -j`):
modmask `0x40` + SPACE → `omarchy-launch-walker`; `0x44` + E →
`omarchy-launch-walker -m symbols`; `0x44` + V →
`omarchy-launch-walker -m clipboard`. (`-m` = exclusive provider, `walker --help`.)
**OBS** — the Omarchy Menu is a walker dependency, not a separate UI:
`omarchy-menu:43` pipes its options into
`omarchy-launch-walker --dmenu --width 295 --minheight 1 --maxheight 630 -p "…"`,
and `:20-24` closes an open dmenu with `walker --close`. The bar's left-most
button (`custom/omarchy`) therefore reaches walker through `omarchy-menu`.
`omarchy-menu:47` also shows that `xdg-terminal-exec --app-id=org.omarchy.terminal`
is the menu's terminal path.
**OBS** — default terminal: `~/.config/xdg-terminals.list` first entry
`Alacritty.desktop`; `omarchy-default-terminal` maps desktop ids to names
(`:8-14`).

### 6.8 Walker introspection ledger

| Question | Surface | Verdict |
|---|---|---|
| Running? which argv? sockets? | `ps`, systemd, `$XDG_RUNTIME_DIR` listing | **OBS** |
| App-level actions? | `org.gtk.Actions.List` on `dev.benz.walker` | **OBS** (`as 0`) |
| Open window geometry? | `hyprctl layers` (walker maps as layer surface when open) | **OBS** (not open now ⇒ absent) |
| Query its state / drive it read-only? | `walker.sock` / `elephant.sock` exist but their protocols are undocumented locally; probing them would exercise a daemon | **UNK** (left untouched) |

---

## §7 Cross-plane failure-mode summary

| Symptom | Check first | Because |
|---|---|---|
| indicator glyph stuck | the producer probe, not waybar: `pgrep -x hypridle`, `makoctl mode`, `pgrep -f '^gpu-screen-recorder'` | the three indicator scripts are pure probes with **no interval** — only signals move them (§4) |
| weather icon vanished | network path `curl -fsS --max-time 3 wttr.in` | `.unavailable` collapses the module by design (`style.css:75-79`) |
| update glyph stale | `git -C "$OMARCHY_PATH" describe --tags` locally vs the 6 h poll | exec is `git ls-remote` (network) and the value is poll+signal driven (`:66-67`) |
| chip frozen | `ai-usage.timer` and cache age vs `STALE_AFTER_SEC = 20*60` (`ai-usage:31`) | chip is cache-only; staleness is rendered as a class, not an error |
| tray empty | `RegisteredStatusNotifierItems` | waybar is the SNI host; no items registered = correct empty state |
| bar edit "did nothing" | was it style or modules? | style/imports reload live (`reload_style_on_change`), module changes need `omarchy restart waybar` (`pkill -9 -x waybar` + `setsid uwsm-app -- waybar`, `omarchy-restart-waybar:6-7`) |
| module text blank that can't run | `$OMARCHY_PATH` in the bar's env | two `exec` lines depend on it; env is unreadable (barred) ⇒ **UNK** |

---

## §8 Divergences vs the round-1 note (candidates for append-only errata)

Recorded here as findings; the errata block proper lives in
`corpus/knowledge/waybar-walker-plane.md` (append-only, owned by that note).

1. **`custom/voxtype` semantics + hazard (new).** `voxtype` is not installed, so
   the module's live payload is `{"alt": "", "tooltip": ""}` (**RUN**) and the
   module is invisible; the producer `omarchy-voxtype-status:5` `trap 'kill 0' EXIT`
   SIGTERMs its own process group — invoking it directly killed the caller
   (exit 143, contained re-run under `setsid`). Waybar's 24.7 h uptime with this
   module configured implies isolated child process groups (**INF**).
2. **`battery` has no device on this host (new).** `/sys/class/power_supply/`
   empty; `upower -e | grep BAT` empty ⇒ capacity source absent; the right-click
   action's script would emit blanks. `waybar-battery(5)` documents no
   no-device rendering ⇒ live value **UNK**.
3. **`[columns] symbols = 1` comment is wrong (correction).** See §6.3 —
   it is the provider's grid column count; the "queried by default" role belongs
   to `[providers] default` (`/etc/xdg/walker/config.toml:53-58`).
4. **Version pin caveat.** `omarchy version` → `3.8.3` while
   `git -C ~/.local/share/omarchy describe --tags` → `v3.8.4` (branch `master`,
   clean). Any claim keyed to "Omarchy 3.8.3" should name which of the two it means.
5. **`pkill -RTMIN+n` works here (contradiction).** `pkill -x -RTMIN+11` delivered
   SIGRTMIN+11 (=45) under procps-ng **4.0.7** (§4), contradicting the
   `ai-usage:150-153` docstring claim; the round-1 producer list (§2.3 of the
   round-1 note) stands as recorded.
6. **Tray live state (new).** `RegisteredStatusNotifierItems` = 0 items,
   `ProtocolVersion = 0`, host registered — the drawer is empty by data, not by bug.
7. **Signal-11 resolution is self-reading.** `ai-usage` does not assume 11: it
   regex-reads `signal` out of `~/.config/waybar/config.jsonc` (range guard
   11 ≤ n < 31) before signalling (`ai-usage:127-178`). Changing the config's
   number silently keeps clicks working; changing it *and* keeping a stale cache
   does not.

---

## §9 Unknowns

1. `$OMARCHY_PATH` inside the waybar process (barred `/proc` read) — the two
   `exec` lines that expand it (`:88`, `:63`) depend on it. My shell reports
   `/home/vgpnk/.local/share/omarchy`.
2. Live values of `custom/weather` and `custom/update` (both need network; not run).
3. Rendered result of `battery` with no battery device; and of `bluetooth`
   with `Powered=true` but 0 connected devices (which format branch wins).
4. Rendered `network` icon/interface choice (auto-detection; ethernet is the
   expected branch, **INF**).
5. `alt`-keyed `format-icons` for custom modules — undocumented in
   `waybar-custom(5)`; behaviour **INF** from producers/configs.
6. Walker's `[[emergencies]]` trigger condition (§6.4).
7. Walker/elephant unix-socket protocols and any query API (§6.8).
8. Item-layout resolution for the omarchy theme (packaged `item_*.xml` fallback
   path) — **INF** only.
9. The three indicators' rendered pixels (payloads measured; the bar's actual
   glyphs were not screen-read — cf. round-1's `grim -t ppm -` technique).
10. Purpose of the empty `on-scroll-*` strings on `custom/expand-icon` (`:195-198`).
11. Waybar's child process-group handling (inferred, §8.1).

---

## §10 Method and boundary proof

- Read-only probes used: `wc`, `stat`, `sha256sum`, `cat`, `grep`, `fc-list`,
  `ps`, `pgrep`, `pkill` (delivery test only, against a scratch process),
  `systemctl --user show/list-*`, `busctl --user list/tree/introspect/get-property/
  call org.gtk.Actions.List`, `hyprctl layers/monitors/workspaces/activeworkspace/binds`,
  `ip -br link`, `iw dev`, `rfkill list`, `wpctl status`, `git rev-parse/describe/
  rev-list/status` (no fetch), `man 5 waybar*`, `pacman -Ql/-Qi`.
- Executed scripts were pure-read producers only: the three indicator scripts,
  `omarchy-voxtype-status` (contained re-run), `ai-usage waybar` (cache-only by
  its own argparse help). No network command was executed
  (`omarchy-weather-*`, `omarchy-update-available`, `git ls-remote` all skipped).
- **Boundary proof** — substrate hashes identical before and after the pass:

| File | sha256 (this pass = round-1 pin) |
|---|---|
| `~/.config/waybar/config.jsonc` | `07f7d663106b72e4c2a7da90883ef2ade044d7e6cb791e81ead777f7d8a08e71` (249 L / 6,068 B) |
| `~/.config/waybar/style.css` | `8316c08ceaa7e3f0624e1b82b1e03523096820fbf775362a930d7f831b0c4e8f` (136 L / 1,887 B) |
| `~/.config/walker/config.toml` | `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` (49 L / 1,336 B) |
| `~/.config/mako/config` | `95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec` |

- mtimes unchanged (`config.jsonc` 2026-10-11 10:36:11; `config.toml`
  2026-10-03 17:44:32) — nothing was written into any substrate tree.
- Scratch: `/tmp/mado-r3-1-probe/` (man renders, `codepoints.txt`, `voxtype.out`,
  `sigtest.py` + `sig.out` signal-delivery proof). Ephemeral.

## Errata (append-only)

_None yet. New entries append below this line; earlier text is never edited —
a correction is a new block citing the block it corrects._

- **E1 (pointer — §8 candidates applied; ERR-M, 2026-10-14).** All 7
  divergence candidates recorded in §8 were applied to the round-1 note's
  append-only errata as `waybar-walker-plane.md` "Errata (round 4)" items
  R4-E1–R4-E7 by the round-4 errata sweep (each re-measured read-only
  16:20–16:25 UTC; scratch `/tmp/w4-err-m-sweep/`). Nothing in this note is
  corrected by the application; §8 remains the finding record.