# Idle & lock plane — measured inventory (MADO-R4-2)

Depth extension for the idle/lock surface named in PROVINCE ("screen/idle
behavior (hypridle/hyprlock where present)"), same table discipline as
`hyprland-config-plane.md` / `waybar-walker-plane.md`.

Probe window: 2026-10-14 16:00–16:08 UTC (host offset −03:00, local
13:00–13:08). Host user `vgpnk`. Substrate read-only; the only writes this
pass were this file and namespace scratch `/tmp/mado-r4-2-probe/`.

Method: `wc`, `stat`, `sha256sum`, `diff`, `cat`, `grep -n` on files;
read-only queries only — `hyprctl` 0.56.2 `getoption`/`monitors`/`layers`/
`devices`/`clients`/`systeminfo`/`version`, `pgrep`/`pidof`,
`systemctl --user status`, `loginctl show-session`, `pacman -Q`.
No `hyprctl dispatch`/`keyword`/`notify` was issued; hypridle/hyprlock were
never started or stopped; no input was synthesized; no idle interval was
waited out. Live idle-state transitions are therefore UNKNOWN by design
(§7) — see the operator-presence constraint in §0.

Tags: `[OBS]` measured directly · `[INF]` inference from measured parts ·
`[UNK]` unknown.

## 0. Scope margin — what this pass may and may not touch

`[OBS]` The session is a live operator session (sddm → uwsm envelope:
`/usr/lib/sddm/sddm-helper … --start uwsm start -g -1 -e -D Hyprland
hyprland.desktop`, PID 1567; Hyprland PID 1671, `ps -eo pid,args`). The
operator may be away while the machine is live; anything that would change
compositor state (lock now, wake, toggle idle, DPMS, screensaver, session
signals) is out of bounds for this pass. All state claims below are point
samples at the probe window or file bytes.

## 1. Summary

`[OBS]` The idle/lock plane is three config files — `hypridle.conf`
(765 B, 19 L), `hyprlock.conf` (742 B, 43 L), theme color file
`~/.config/omarchy/current/theme/hyprlock.conf` (176 B, 5 L) — plus a set of
Omarchy actuator scripts (`~/.local/share/omarchy/bin/omarchy-system-lock`,
`…-system-wake`, `…-launch-screensaver`, `…-screensaver`, `…-toggle-idle`,
`…-toggle-screensaver`, `…-restart-hypridle`, `…-refresh-hypridle/-hyprlock`,
`…-brightness-display`, `…-brightness-keyboard`, §2b).

`[OBS]` Both config files are byte-identical to the shipped Omarchy defaults
(`~/.local/share/omarchy/config/hypr/`), i.e. unmodified shipped config
(§2, §3, §4). The declared chain is two hypridle listeners: at 150 s idle →
screensaver (TTE terminal animation, not a lock); at 152 s → lock via
`omarchy-system-lock`, which launches hyprlock and (unless
`OMARCHY_LOCK_ONLY=true`) turns the panel off by DPMS ~3 s later; wake
restores DPMS/brightness (§5).

`[OBS]` At probe time **hypridle is not running** (no process; the systemd
user unit is inactive/disabled) and no lock or screensaver process exists,
so `[INF]` the two timers cannot fire in this session as it stands — nothing
else implements them (no swayidle; Hyprland has no built-in idle). The
live idle-transition behavior of the plane — with or without the daemon —
remains UNKNOWN (§7, §11).

## 2. File table — configs `[OBS]`

| File | Bytes | Lines | mtime (host) | sha256 (first 12) |
|---|---|---|---|---|
| `~/.config/hypr/hypridle.conf` | 765 | 19 | 2026-10-03 17:44:32 | `e7d3b8dd9835` |
| `~/.config/hypr/hyprlock.conf` | 742 | 43 | 2026-10-03 17:44:32 | `b8d173dcff55` |
| `~/.config/omarchy/current/theme/hyprlock.conf` | 176 | 5 | 2026-10-03 17:49:02 | `3ef010e72b5f` |

`[OBS]` Provenance measured by hash identity, not by naming: the local
configs are byte-identical to the Omarchy default payload —
`sha256sum ~/.config/hypr/hypridle.conf ~/.local/share/omarchy/config/hypr/hypridle.conf`
→ both `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41`;
same for hyprlock (`b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1`),
`diff` exits 0 for both. `[OBS]` No `hypridle.conf.bak.*` or
`hyprlock.conf.bak.*` exists in `~/.config/hypr/` (only
`autostart.conf.bak.1791942509`), consistent with "never refreshed with a
differing predecessor".

`[OBS]` The default payload copy path is
`omarchy-refresh-config hypr/hypridle.conf`
(`~/.local/share/omarchy/bin/omarchy-refresh-config` L20-44: L23 timestamped
`.bak` name, L29 backup copy, L32 replacement copy, L35-40 `cmp` + `diff`
report and backup retention), wired as `omarchy-refresh-hypridle` (L5-6:
refresh + restart) and `omarchy-refresh-hyprlock` (L5: refresh only).
`[OBS]` Theme selection is
`~/.config/omarchy/current/theme.name` → `matte-black`; `current/theme` is a
real directory, `current/background` is a symlink →
`…/current/theme/backgrounds/0-ship-at-sea.jpg` (shape only).

## 2b. File table — actuator scripts (same payload, all mtime 2026-10-03 17:42:32) `[OBS]`

| Script (`~/.local/share/omarchy/bin/…`) | Bytes | Lines | sha256 (first 12) |
|---|---|---|---|
| `omarchy-system-lock` | 699 | 33 | `c1dd3881e8ae` |
| `omarchy-system-wake` | 228 | 9 | `09ad52b0f184` |
| `omarchy-launch-screensaver` | 1,641 | 59 | `ba783a3a55c1` |
| `omarchy-screensaver` | 1,015 | 35 | `11d7487aa3ee` |
| `omarchy-toggle-idle` | 316 | 13 | `11979b4d4198` |
| `omarchy-toggle-screensaver` | 213 | 8 | `87f2cb4073ba` |
| `omarchy-restart-hypridle` | 131 | 5 | `40655252840c` |
| `omarchy-refresh-hypridle` | 188 | 6 | `a5c4e33acfc5` |
| `omarchy-refresh-hyprlock` | 139 | 5 | `fd6ac952bb93` |
| `omarchy-brightness-display` | 1,794 | 60 | `62e6d7655258` |
| `omarchy-brightness-keyboard` | 1,692 | 55 | `f1305c06b0ec` |

Plus (outside `bin/`, same payload): `default/waybar/indicators/idle.sh`
(159 B, 7 L, `6d8d2c11d3c3`) and `default/hypr/autostart.conf`
(742 B, 16 L, `acb6a6686203`).

## 3. `hypridle.conf` — line anchors `[OBS]`

No `source` of this file exists in any hyprland config; hypridle reads it
from the default path. `[OBS]` Startup is `default/hypr/autostart.conf:1`
`exec-once = uwsm-app -- hypridle` (no `-c` argument); `[OBS]` the systemd
alternative `/usr/lib/systemd/user/hypridle.service` exists
(`PartOf`/`After=graphical-session.target`, `ExecStart=/usr/bin/hypridle`)
but is `disabled`. Binary `hypridle 0.1.8-2` (`pacman -Q`).

```
L1-6   general {
L2       lock_cmd = omarchy-system-lock                    # comment: "lock screen and 1password"
L3       before_sleep_cmd = OMARCHY_LOCK_ONLY=true omarchy-system-lock
                                                           # comment: "lock before suspend without scheduling display off."
L4       after_sleep_cmd = sleep 1 && omarchy-system-wake # comment: "delay for PAM readiness, then turn on display."
L5       inhibit_sleep = 3                                 # comment: "wait until screen is locked"
L8     # comment: "Start screensaver after 2.5 minutes"
L9-12  listener { timeout = 150; on-timeout = pidof hyprlock || omarchy-launch-screensaver }
L14    # comment: "Lock system after 5 minutes (screensaver resets idle timer, so have to just do half + 2s margin)"
L15-19 listener { timeout = 152; on-timeout = omarchy-system-lock; on-resume = omarchy-system-wake }
```

`[OBS]` Numeric note: the L14 comment says "5 minutes" while the declared
`timeout` is 152 s. `[INF]` The comment's own rationale resolves this: the
screensaver is expected to reset the idle timer, so the 150 s listener
itself restarts the count, and lock lands at ≈ 150 + 152 = 302 s ≈ 5 min.
Two listeners, 2 s apart, arranged so the screensaver (150 s) always
precedes the lock (152 s). `[UNK]` Whether the reset actually happens in
0.56.2/ext-idle-notify terms is unverified — reproducing it needs ≥ 302 s of
true inactivity or a simulation, both out of bounds (§0).

`[OBS]` `lock_cmd` (L2) is the config's lock entry point for lock requests
handled by hypridle (e.g. the `before_sleep_cmd` path and any DBus lock
request); the 152 s listener does not go through `lock_cmd` — it calls
`omarchy-system-lock` directly. `[INF]` Both routes land on the same
script, so lock behavior is script-defined (§5), not hypridle-defined.
`[OBS]` `inhibit_sleep = 3` is declared with the L5 comment "wait until
screen is locked"; `[UNK]` the numeric semantics beyond the comment were not
verified against the binary (no read-only config check exists; loading the
config would mutate the session).

## 4. `hyprlock.conf` + theme file — line anchors `[OBS]`

```
L1   source = ~/.config/omarchy/current/theme/hyprlock.conf
L3-5   general { ignore_empty_input = true }
L7-12  background { monitor = (empty → all); color = $color;
                     path = ~/.config/omarchy/current/background; blur_passes = 3 }
L14-16 animations { enabled = false }
L18-39 input-field { monitor = (all); size 650,100; position 0,0; halign/valign center;
                     inner/outer/font/check colors from theme vars; outline_thickness = 4;
                     font_family = JetBrainsMono Nerd Font; placeholder "Enter Password";
                     fail_text = "<i>$FAIL ($ATTEMPTS)</i>"; rounding 0; shadow_passes 0;
                     fade_on_empty = false }
L41-43 auth { fingerprint:enabled = false }
```

`[OBS]` Theme file (5 lines) defines only `$color`, `$inner_color`,
`$outer_color`, `$font_color`, `$check_color` (matte-black: background
rgba(18,18,18,1.0); inner 0.8 alpha; accents rgba(190,190,190,·) and
rgba(230,142,13,1.0)). `[OBS]` `~/.config/omarchy/current/background`
resolves to a real JPEG in the same theme tree (§2), so the blur
background has a concrete file at probe time. `[OBS]` L14-16 disables
animations in the locker itself, while the compositor's animations are on
(`hyprctl getoption animations:enabled` → `int: 1`) — the two are
independent. `[OBS]` Fingerprint auth is explicitly off (L41-43), matching
the AGENTS-documented migration pattern (omarchy AGENTS.md "Migrations"
example, L124-131). `[UNK]` PAM service/data used by hyprlock was not read
(credentials surface; out of province).

## 5. Declared idle → screensaver → lock → wake chain `[OBS]` + `[INF]`

Actuator bytes (line anchors from §2b files):

| Step (declared order) | Source anchor | Measured content |
|---|---|---|
| t = idle 150 s | `hypridle.conf:9-12` | `pidof hyprlock \|\| omarchy-launch-screensaver` |
| screensaver launch | `omarchy-launch-screensaver:5-6,10,13-18,23-57` | needs `tte`; exits if `org.omarchy.screensaver` already running or if toggle flag `screensaver-off` is set (unless arg `force`); quits walker; loops monitors, `hyprctl dispatch focusmonitor`, execs terminal with class `org.omarchy.screensaver` running `omarchy-screensaver`; restores focus |
| screensaver body | `omarchy-screensaver:17-34` | traps INT/TERM/HUP/QUIT → reset `cursor:invisible false`, `pkill -x tte`, kill class; sets `cursor:invisible true` (L21); TTE animation loop; exits on any key (L30-34) |
| t = 152 s | `hypridle.conf:15-19` | `omarchy-system-lock` (lock), `on-resume = omarchy-system-wake` |
| lock | `omarchy-system-lock:8-13` | if no hyprlock: `( hyprlock; omarchy-system-wake ) &` |
| lock side-effects | `…:16-24` | `hyprctl switchxkblayout all 0`; `1password --lock` if running; `pkill -f org.omarchy.screensaver` |
| display off | `…:26-32` | unless `OMARCHY_LOCK_ONLY=true`: after `sleep 3`, if hyprlock still up → `omarchy-brightness-keyboard off`, `omarchy-brightness-display off` |
| panel off primitive | `omarchy-brightness-display:18-23` | `off` → `hyprctl dispatch dpms off`; `on` → `… dpms on` (before any backlight device logic) |
| wake | `omarchy-system-wake:8-9` | `omarchy-brightness-display on`; `omarchy-brightness-keyboard restore` |
| suspend path | `hypridle.conf:3-5` | before suspend: `OMARCHY_LOCK_ONLY=true omarchy-system-lock` (lock without the DPMS half); after wake: `sleep 1 && omarchy-system-wake`; `inhibit_sleep = 3` |

`[INF]` Composed timeline in this configuration: 0→150 s active; at 150 s the
animation starts (display still on — it is a terminal window, not DPMS);
at 152 s the lock runs; at ≈155 s the panel goes off (lock script's
`sleep 3`, skipped only in the lock-only/suspend variant); unlocking exits
hyprlock, which triggers `omarchy-system-wake` from the lock script's
subshell, and the same wake is also declared as hypridle's `on-resume`
(L18) — redundant by design, not conflicting.

`[OBS]` Host-specific no-ops in this chain: keyboard backlight device search
`omarchy-brightness-keyboard:9-19` finds nothing on this host
(`/sys/class/leds/*kbd_backlight*` absent, §9) → the `off`/`restore` steps
exit 1; `hyprctl switchxkblayout all 0` targets index 0 and every keyboard
already reports `layout=br` with only `br` configured (`input.conf:10`;
default `us` at `default/hypr/input.conf:3` is overridden) — a no-op today,
not a guarantee. `[OBS]` `omarchy-system-lock:24` kills the screensaver
class on lock, so the declared order "screensaver then lock" ends with the
screensaver removed.

`[UNK]` All timing above is config-declared; no transition was observed
(§0). In particular the assumption "screensaver resets idle timer" (L14)
is inferred from the comment, not measured.

## 6. Screen/idle state semantics — Hyprland options (read-only) `[OBS]`

`hyprctl getoption` on a deliberately bogus path
(`misc:bogus_xyz_notreal`) returns `no such option`, so non-error responses
below are real options.

| Option | Value | `set` | Measured source |
|---|---|---|---|
| `misc:key_press_enables_dpms` | `int: 1` | true | `default/hypr/input.conf:19` (`= true` "key press will trigger wake") |
| `misc:mouse_move_enables_dpms` | `int: 1` | true | `default/hypr/input.conf:20` |
| `cursor:inactive_timeout` | `float: 0.000000` | false | Hyprland default — no time-based cursor hide |
| `cursor:hide_on_key_press` | `int: 1` | true | `default/hypr/looknfeel.conf:136` |
| `cursor:invisible` | `int: 0` | false | runtime keyword (screensaver L21 sets true while showing; L10 resets) |
| `misc:allow_session_lock_restore` | `int: 0` | false | Hyprland default |
| `misc:session_lock_xray` | `int: 0` | false | Hyprland default |

`[INF]` Division of labor: Hyprland itself only provides the wake half of
the screen-idle story (`key_press`/`mouse_move` re-light a DPMS-off panel)
and the session-lock protocol; it has no idle timer and no "turn panel off
after N" option. Turning the panel off is delegated entirely to the
omarchy script chain (§5, `dpms off` dispatch). `[OBS]` Cursor semantics at
probe: the cursor never hides by inactivity (`inactive_timeout = 0`) and is
hidden only on key press or by the screensaver's runtime keyword —
`cursor:invisible` reads `0` now (screensaver not running).

## 7. Runtime snapshot at probe (read-only) `[OBS]` — and the live-idle UNKNOWN

- Processes: `ps -eo pid,comm,args | grep -iE 'hypridle|hyprlock|hyprsunset|swayidle'` → no match. Hyprland itself: PID 1671 (`Hyprland --watchdog-fd 4`).
- `systemctl --user status hypridle.service` → `inactive (dead)`, loaded
  `disabled; preset: enabled`. `[INF]` With no hypridle process and no
  other idle implementation, neither listener (150/152 s) can fire now;
  the declared chain (§5) is inert in this session at probe time.
- Display: `hyprctl monitors` → DP-1 `dpmsStatus: 1`, `disabled: false`
  (panel on).
- Session: `loginctl show-session 1` → `Type=wayland Active=yes
  State=active IdleHint=no IdleSinceHint=0 LockedHint=no`. `[UNK]` which
  component sets `IdleHint`/`LockedHint` (logind input tracking vs
  compositor vs locker) — not traced.
- Lock state: `hyprctl layers` lists only `wallpaper` (pid 1710, background
  level) and `waybar` (pid 1707, top level) — no lock-layer surface.
  `hyprctl clients -j` → 3 windows, all Alacritty; none
  `org.omarchy.screensaver`. `[OBS]` Not locked, no screensaver, at the
  sample instant.
- **Live idle-state transitions: UNKNOWN.** The pass did not wait out 150 s
  of inactivity, dispatch DPMS, start/stop hypridle/hyprlock, or synthesize
  input (§0). The values above are one point sample; the idleness of the
  operator before/after it is not represented. Whether the operator's own
  presence kept `IdleHint=no` is also `[UNK]`.
- `[OBS]` Cause of the daemon's absence: still `[UNK]` (open since round 1,
  re-measured in rounds 2/3 and now). New evidence this round narrows it:
  `omarchy-toggle-idle:5-11` toggles by `pgrep`/`pkill -x hypridle` vs
  `uwsm-app -- hypridle` and leaves **no flag file**, so a manual toggle-off
  would be traceless; `omarchy-restart-app` (L6-7: `pkill -x $1; setsid
  uwsm-app -- "$@"`) could likewise leave no trace. What started or stopped
  it in this session is not recoverable from files alone.

## 8. Toggle & indicator surface `[OBS]`

- `omarchy-toggle-idle` (13 L): if `pgrep -x hypridle` → kill + notify
  "Stop locking computer when idle", else `uwsm-app -- hypridle` + notify
  "Now locking computer when idle"; then `pkill -RTMIN+9 waybar` (L5-13).
  Process-state toggle; no file state.
- `omarchy-toggle-screensaver` (8 L): `omarchy-toggle … screensaver-off` —
  flag file `~/.local/state/omarchy/toggles/screensaver-off` (`omarchy-toggle`
  L20-25: flag exists → `rm` + "Screensaver disabled"; absent → `touch` +
  "Screensaver enabled"). `[OBS]` Flag absent at probe (`toggles/` contains
  only `hypr/`) → screensaver availability **enabled**; read back by
  `omarchy-launch-screensaver:13`.
- Waybar module `custom/idle-indicator` in `~/.config/waybar/config.jsonc:206-208`
  (`exec` = `default/waybar/indicators/idle.sh`, `on-click = omarchy-toggle-idle`);
  `idle.sh:3-6` prints the "idle lock disabled" glyph + `"class": "active"`
  exactly when hypridle is absent. `[UNK]` Whether the currently *rendered*
  waybar module reflects that state (no RTMIN+9 refresh sent, no screenshot
  taken per the probe constraints); file-level behavior only.
- Maintenance: `omarchy-restart-hypridle` (L5) → `omarchy-restart-app hypridle`
  (L6-7: `pkill -x`, `setsid uwsm-app`); `omarchy-refresh-hypridle` (L5-6) →
  `omarchy-refresh-config hypr/hypridle.conf` + restart;
  `omarchy-refresh-hyprlock` (L5) → refresh only. `omarchy-menu` also
  references hypridle (menu wiring; not enumerated here — menu plane).

## 9. Hardware dependencies on the lock/wake path `[OBS]`

- `/sys/class/backlight/` is **empty** (no display-backlight device) and
  `/sys/class/leds/*kbd_backlight*` does not exist. `[INF]` Therefore the
  keyboard-brightness steps of the chain (`off`/`restore` inside
  `omarchy-system-lock` / `omarchy-system-wake`) exit 1 with "No keyboard
  backlight device found" (`omarchy-brightness-keyboard:9-19`) on this host —
  they are inert here, while the DPMS half still works because
  `omarchy-brightness-display:19-22` handles `off`/`on` before any device
  lookup.
- `tte` present (`/usr/bin/tte`). `[INF]` The operative screensaver branch is
  the Alacritty one (`omarchy-launch-screensaver:27-32`): all three live
  windows are Alacritty (`hyprctl clients` classes) and
  `xdg-terminal-exec --print-id` (L21) resolves the default terminal —
  the resolver itself was not executed this pass. `[OBS]` The screensaver
  requires `tte` (`…-launch-screensaver:5-6` exits 1 without it) and a
  supported terminal (else a `notify-send` warning, L53-55).
- Panel target: single monitor DP-1; `dpms off` in
  `omarchy-brightness-display:19` carries no monitor argument → applies to
  all monitors (one here). `[INF]` For multi-monitor setups the same
  dispatch would blank the whole set.

## 10. Errata (append-only — add blocks, never edit above)

- E1 (2026-10-14, MADO-R4-2 seed): new plane doc; no corrections recorded
  yet. First cross-plane check applied: `hyprland-config-plane.md` §10
  ("hypridle is not running … cause [UNK]") re-measured here and **held**
  (still absent, still `[UNK]`); no contradiction to correct. The file
  counts in that doc (`hypridle.conf` 765 B/19 L, `hyprlock.conf` 742 B/43 L)
  and their first-12 hashes match this pass exactly (§2).

## 11. Unknowns `[UNK]`

1. Why hypridle is not running (no flag file, no trace in files; §7).
2. Live idle transitions of any kind — screensaver appearance at 150 s,
   lock at 152 s, "screensaver resets idle timer", effective ≈302 s lock:
   declared in config, unobserved (§0, §5).
3. Which component writes logind `IdleHint`/`LockedHint`, and whether
   hyprlock participates (§7).
4. Whether `hyprlock.conf`/`hypridle.conf` parse cleanly (`hyprctl
   configerrors` covers the compositor config only; hypridle/hyprlock have
   no read-only check; loading them would mutate the session).
5. If hyprlock is killed while the screensaver has set
   `cursor:invisible true`, whether the cursor is restored — the reset
   lives only in `omarchy-screensaver`'s trap (L9-14) and in the
   screensaver process being alive to run it.
6. Whether `inhibit_sleep = 3` behaves as the L5 comment says (§3).
7. Whether the waybar idle indicator's current rendering matches
   `idle.sh`'s file-level behavior (§8).
8. Multi-monitor behavior of the chain (single monitor here; §9).

## 12. Spot-checks (reproducible)

1. Provenance by identity:
   `sha256sum ~/.config/hypr/hypridle.conf ~/.local/share/omarchy/config/hypr/hypridle.conf`
   → both `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41` (§2/§3).
2. Daemon state: `pgrep -x hypridle; systemctl --user is-active hypridle`
   → no output; `inactive` (§7).
3. Screen/session sample: `hyprctl monitors | grep dpmsStatus` →
   `dpmsStatus: 1`; `loginctl show-session 1 -p IdleHint -p LockedHint` →
   `IdleHint=no`, `LockedHint=no`; `hyprctl layers` → no lock layer (§7).

## Errata (round 4) — appended 2026-10-14 (ERR-M)

Append-only block; E1 above stands unedited. Written by the round-4 errata
sweep; read-only probes 2026-10-14 16:20–16:25 UTC (scratch
`/tmp/w4-err-m-sweep/`).

- **E2 (post-probe environment turnover; UNK-1 narrowed).** The compositor
  session this note probed (Hyprland PID 1671) was replaced at ~16:11:06–07
  UTC. The current instance is Hyprland PID **1203316** (`hyprctl -j
  instances`: one entry, `time` 1791994267 = 16:11:07 UTC), and in it
  hypridle ran as an autostart child of Hyprland — **PID 1203349**, started
  16:11:07 UTC, ppid = 1203316 — measured present 16:21:49 UTC, **absent
  again by 16:23:19 UTC** (repeated `pgrep -a hypridle` → no match;
  `systemctl --user is-active` `inactive` / `disabled` throughout — the
  daemon is a session child, never the unit, so a `systemctl`-only re-check
  cannot see it; only the `pgrep` half discriminates). §1/§7's "not running"
  remains true as a point sample of the probe window, not of the session
  after the turnover. §11 UNK-1 is narrowed for the new instance: the
  declared autostart route (`default/hypr/autostart.conf:1`, re-read)
  demonstrably launches hypridle in a fresh session; the old instance's
  absence/stop cause and the new session's present→absent toggle stay
  `[UNK]` (no flag file; §7's stopper routes stand). AUD-M1's audit verdict
  independently records the same turnover and PIDs; both local config files
  re-hashed here equal §2's pins (`e7d3b8dd…` / `b8d173dc…`, unchanged since
  2026-10-03 17:44:32).