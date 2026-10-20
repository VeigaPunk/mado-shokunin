source: S063 https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ (Configuration, General, Listeners, Examples); S064 https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/ (Warning, Command-line Arguments, Configuration, General, Authentication, System Configuration); S065 https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md (Features, Configuration); S066 https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp (setupDBUS, handleDbusSleep, dbus Lock/Unlock, onIdled, onResumed, onInhibit, onLocked, config load); S067 https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.hpp (SIdleListener); S068 https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/main.cpp (config lookup); S069 https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md (Features, Docs)
verified-at: 2026-10-20; wiki pages fetched as HTML (wiki version selector "Latest git"), tag-pinned raw files at hypridle v0.1.8 and hyprlock v0.9.6 read with curl; raw SHA-256 per source in corpus/SOURCES.md S063-S069 and lessons/round-17.md § Gate; host files read with cat/sha256sum only; nothing executed
recheck: re-fetch the two wiki URLs and the five tag-pinned raw URLs, compare raw SHA-256 with corpus/SOURCES.md S063-S069, re-anchor the cited lines; host: sha256sum of the seven files in § Host declaration plus hyprland.conf; no omarchy-*, hypridle, hyprlock, systemctl, hyprctl, loginctl, journalctl, pacman or pidof
surface: P6

# P6 idle and lock — documentary route (hypridle, hyprlock)

Documentary route only. The upstream contract and the host file bytes below
are read, not observed: no listener has fired, no lock has been taken, and no
behaviour on the running host is claimed. Unobserved behaviour is listed in
§ Unexercised behavior. Companion plane note: `corpus/knowledge/idle-lock-plane.md`
(§11 Unknowns is the open list this note narrows; §7 holds the earlier read-only
runtime snapshot and is not re-run here).

Anchor keys used below:

| key | source | version | anchor form |
|---|---|---|---|
| HW | https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ | wiki "Latest git", page modified 2026-08-26 | `[HW:n]` = line n of the tag-stripped `<article>` text, one line per block (table cells run together in the text) |
| LW | https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/ | wiki "Latest git", page modified 2026-08-26 | `[LW:n]` as HW |
| HR | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md | hypridle v0.1.8 (tag) | `[HR:n]` = file line |
| HC | …/hypridle/v0.1.8/src/core/Hypridle.cpp | hypridle v0.1.8 | `[HC:n]` = file line |
| HH | …/hypridle/v0.1.8/src/core/Hypridle.hpp | hypridle v0.1.8 | `[HH:n]` = file line |
| HM | …/hypridle/v0.1.8/src/main.cpp | hypridle v0.1.8 | `[HM:n]` = file line |
| LR | https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md | hyprlock v0.9.6 (tag) | `[LR:n]` = file line |

Tag selection: `releases/latest` redirects resolved to `v0.1.8` (hypridle) and
`v0.9.6` (hyprlock) on 2026-10-20. The GitHub REST API returned HTTP 403
rate-limit and was not used.

## Upstream contract

### General keys (hypridle)

- **lock_cmd** runs on a dbus `Lock` member: `if (MEMBER == "Lock") {` [HC:473], then `spawn(*LOCKCMD)` if non-empty [HC:477-478]. Documented as "command to run when receiving a dbus lock event (e.g. loginctl lock-session)" [HW:13]. README example: "dbus/sysd lock command (loginctl lock-session)" [HR:16].
- **unlock_cmd** — same pattern on `Unlock` [HC:480-485]; [HW:14].
- **on_lock_cmd / on_unlock_cmd** — fired from the Wayland session-lock notification, not dbus: `onLocked` reads `general:on_lock_cmd` [HC:402] and spawns it [HC:404]; `onUnlocked` reads `general:on_unlock_cmd` [HC:433]. The source warns when the compositor lacks the protocol: "Compositor is missing hyprland-lock-notify-v1!" with "general:inhibit_sleep=3, general:on_lock_cmd and general:on_unlock_cmd will not work." [HC:104-107]. Documented [HW:15-16].
- **before_sleep_cmd / after_sleep_cmd** — `handleDbusSleep` matches `PrepareForSleep` [HC:493]; `cmd = toSleep ? before : after` [HC:504]; spawned if non-empty [HC:509-510]. Documented [HW:17-18].
- **ignore_dbus_inhibit** — read in `setupDBUS` [HC:600]; when false (default) the block that registers `org.freedesktop.ScreenSaver` runs [HC:626]. README: "whether to ignore dbus-sent idle-inhibit requests (used by e.g. firefox or steam)" [HR:20]; documented [HW:19].
- **ignore_systemd_inhibit** — read in `setupDBUS` [HC:601], gated at [HC:617], documented [HW:20]. **ignore_wayland_inhibit** — read at [HC:58]; selects the inhibit-aware idle notification when true or when the listener sets `ignore_inhibit` [HC:74]; documented [HW:21].
- **inhibit_sleep** — modes 0 disable / 1 normal / 2 auto / 3 "wait until locked" [HW:22-26]. Source: case 2 "auto" [HC:120], case 3 waits only `if (m_sWaylandState.lockNotifier)` [HC:128-129]. Wiki: "3 makes your system wait until the session gets locked by a lock screen app." [HW:33].
- Default `inhibit_sleep` = 2 [HW:26].

### Listeners (hypridle)

- **timeout / on-timeout** — `onIdled` returns without firing while any inhibit is held and the listener does not set `ignore_inhibit`: `if (g_pHypridle->m_iInhibitLocks > 0 && !pListener->ignoreInhibit) {` [HC:301]. Otherwise the command runs via `spawn(pListener->onTimeout);` [HC:327]. Wiki: "Every listener has a timeout (in seconds). After idling for timeout seconds," [HW:36-37].
- **on-resume** — `onResumed` skips the command when on-timeout was not fired: "Skipping onResumed: onTimeout was inhibited for rule" [HC:348] (guard at [HC:346-348], flag cleared at [HC:352]). Wiki: "When action is resumed after idle, on-resume will fire." [HW:38].
- **ignore_inhibit** (per listener) — `bool ignoreInhibit = false;` [HH:23]; copied from the rule at [HC:70]. Wiki table row [HW:51].
- **condition_cmd / condition_retry** — `l.conditionCmd = r.conditionCmd;` [HC:71], `conditionRetry` [HH:26]. Wiki [HW:52-53], [HW:55-60]. README [HR:28-29]. Not exercised here.
- **Config required** — `hypridle.conf` lookup: missing file logs "No hypridle.conf file found in:" [HM:61]; wiki: "A config file is required; hypridle won’t run without one." [HW:7]. Config path per [HW:6]: `~/.config/hypr/hypridle.conf`.
- **Start** — wiki: add `hypridle` to autostart, or `systemctl --user enable --now hypridle.service` under uwsm [HW:8-9]. README: `exec-once = hypridle` [HR:62].
- Wiki example timeouts and dpms/suspend examples are documentary only [HW:78-107].

### hyprlock (documentary, from wiki and README)

- Warning: "If no config file is found in any of the searched paths, hyprlock exits with an error and your session will not be locked." [LW:7].
- `--grace SECONDS`: "Set grace period in seconds before requiring authentication" [LW:16]. The grace implementation was not read (hyprlock source not opened this round) — see § Unexercised.
- `general:hide_cursor` default false [LW:37]; `general:ignore_empty_input` default false [LW:38]; `general:fail_timeout` default 2000 ms: "Milliseconds until the ui resets after a failed auth attempt" [LW:49].
- `auth:pam:enabled` default true [LW:53]; `pam:module` default `hyprlock`, falls back to `su` [LW:54]; `fingerprint:enabled` default false [LW:55].
- Arch: "On Arch Linux, by default, hyprlock integrates with pambase through pam_faillock.so, which forces a 10 minute timeout after 3 failed unlocks." [LW:84]. Remedy per [LW:85] (documentary).
- Protocol: "Uses the ext-session-lock protocol" [LR:5]. hypridle README: "based on the `ext-idle-notify-v1` wayland protocol" [HR:5].
- Drift: hyprlock README links the wiki at `wiki.hyprland.org` [LR:19]; the fetched wiki URL is `wiki.hypr.land` (page header [LW:1-3] carries no domain). Documentary only.

## Host declaration

Host bytes read with `cat -n` and `sha256sum` only. Paths are under `/home/vgpnk`. Anchors are file lines.

| file | sha256 | bytes / lines |
|---|---|---|
| `~/.config/hypr/hypridle.conf` | `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41` | 765 / 19 |
| `~/.config/hypr/hyprlock.conf` | `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1` | 742 / 43 |
| `~/.config/omarchy/current/theme/hyprlock.conf` (sourced by hyprlock.conf:1) | `3ef010e72b5f69113e1500bb083fb053f9f121212ad5ed4fe74ad8d12507ad0b` | 176 / 5 |
| `~/.local/share/omarchy/bin/omarchy-system-lock` (called by hypridle.conf:2-3, 17) | `c1dd3881e8aea9106cd844cc1f8ab4bcd4fcb07b81eefeab5e7a225e282b9ce1` | — / 33 |
| `~/.local/share/omarchy/bin/omarchy-system-wake` (hypridle.conf:4, 18) | `09ad52b0f184ced3756b3ba5cdcee743ff78174dd9f83334c68ba4ed110bd3d4` | — / 9 |
| `~/.local/share/omarchy/bin/omarchy-launch-screensaver` (hypridle.conf:11) | `ba783a3a55c134af4e7fe4111d9ef6fc7796d03a78bb7f114eeee6dd3758fa12` | — / 59 |
| `~/.local/share/omarchy/default/hypr/autostart.conf` | `acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441` | — / 16 |

`~/.config/hypr/autostart.conf` (sha `5ace17016fe2998aa6e7ad2221c1889b430aa4b94faf5ef1f907d6301dd5fc46`) does not start hypridle. The omarchy default autostart does: line 1 `exec-once = uwsm-app -- hypridle` (autostart.conf:1). It is loaded by `~/.config/hypr/hyprland.conf:4` `source = ~/.local/share/omarchy/default/hypr/autostart.conf` (hyprland.conf sha256 `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365`, read as bytes in round 17; same edge as `hyprland-config-plane.md` §3). Declared start route only; whether hypridle is running is `[UNK]`.

### hypridle.conf (`general`, `listener`)

- `lock_cmd = omarchy-system-lock` (hypridle.conf:2).
- `before_sleep_cmd = OMARCHY_LOCK_ONLY=true omarchy-system-lock` (:3) — the env var suppresses the display-off branch in the script (omarchy-system-lock:26).
- `after_sleep_cmd = sleep 1 && omarchy-system-wake` (:4).
- `inhibit_sleep = 3` (:5) — the wait-until-locked mode whose lock-notify precondition is `[HC:104-107]`.
- Not set, so defaults apply: `ignore_dbus_inhibit`, `ignore_systemd_inhibit`, `ignore_wayland_inhibit` = false [HW:19-21]; `on_lock_cmd`/`on_unlock_cmd` empty.
- Listener 1: `timeout = 150`, `on-timeout = pidof hyprlock || omarchy-launch-screensaver`, no on-resume (:9-12).
- Listener 2: `timeout = 152`, `on-timeout = omarchy-system-lock`, `on-resume = omarchy-system-wake` (:15-19). Host comment (:14): "screensaver resets idle timer, so have to just do half + 2s margin" — a claim about runtime, `[UNK]` here.

### hyprlock.conf

- `source = ~/.config/omarchy/current/theme/hyprlock.conf` (:1).
- `general { ignore_empty_input = true }` (:3-5) — documented default false [LW:38].
- `background { path = ~/.config/omarchy/current/background; blur_passes = 3 }` (:7-12).
- `animations { enabled = false }` (:14-16).
- `input-field` size 650×100, `fade_on_empty = false`, `fail_text` with `$FAIL ($ATTEMPTS)` (:18-39).
- `auth { fingerprint:enabled = false }` (:41-43). Documented default is already false [LW:55]; the line is explicit.
- `hide_cursor`, `fail_timeout`, `pam:module`, `grace` not set: defaults apply [LW:37, 49, 54].

### omarchy theme and scripts (bytes, not executed)

- Theme `hyprlock.conf` (5 lines): `$color`, `$inner_color`, `$outer_color`, `$font_color`, `$check_color` only (:1-5). No timing keys.
- `omarchy-system-lock`: if `pidof hyprlock` is empty, runs `( hyprlock; omarchy-system-wake ) &` (:8-13); `hyprctl switchxkblayout all 0` (:16); locks 1password if running (:19-21); `pkill -f org.omarchy.screensaver` (:24); unless `OMARCHY_LOCK_ONLY` is `true`, after `sleep 3` and if hyprlock is still running turns off keyboard and display brightness (:26-32).
- `omarchy-system-wake`: `omarchy-brightness-display on` (:8), `omarchy-brightness-keyboard restore` (:9).
- `omarchy-launch-screensaver`: exits 1 unless `tte` is present (:5-7); exits 1 when `screensaver-off` is enabled unless arg `force` (:13-15); runs `walker -q` (:18); opens the screensaver in Alacritty, ghostty, foot or kitty (:26-56), otherwise `notify-send` (:53-54).

### Host binary

- Version binding (file read of `/var/log/pacman.log`, no package query): the last logged transactions are `upgraded hypridle (0.1.7-10 -> 0.1.8-2)` (pacman.log:1792) and `upgraded hyprlock (0.9.6-1 -> 0.9.6-3)` (pacman.log:1798), both 2026-10-11; no later hypridle/hyprlock line through 2026-10-20. The tags read above (v0.1.8, v0.9.6) therefore match the last logged pkgver. Arch packaging patches, the running binary and whether a later non-logged change occurred stay `[UNK]`; a log line is not a running-binary fact.

## Safe observation

What an operator may read without mutating state:

- `cat -n` and `sha256sum` on the six host files and the omarchy default autostart listed above. Re-run to detect drift against the table.
- `grep -n` on the same files for the key names above (read-only, no parse by a daemon).
- Upstream: `curl` of the two wiki pages and the tag-pinned raw URLs; tag resolution via `curl -sI https://github.com/hyprwm/<repo>/releases/latest` (Location header). The GitHub REST API is rate-limited and was not needed.
- Upstream source directory listings at the tag: `https://github.com/hyprwm/hypridle/tree/v0.1.8` and `…/tree/v0.1.8/src` (root listing has no `example/` directory; `example/hypridle.conf` and `example/hyprlock.conf` return HTTP 404 at both tags).

Not safe under the current pause, and not used: `pidof`, `pgrep`, `hypridle -v`, `hyprlock`, `loginctl`, `systemctl status`, `journalctl` (live probes), any `omarchy-*` command including the scripts above, `hyprctl`, `pacman -Q`/`-Si`, and any idle/lock trigger.

## Unexercised behavior

- `[UNK]` Actual idle timing: whether the 150 s and 152 s listeners fire on this host, and whether the screensaver really resets the idle timer (hypridle.conf:14). Extends `idle-lock-plane.md` §11 item 2.
- `[UNK]` Listener firing and on-resume execution on this host (`idle-lock-plane.md` §11 items 2, 5).
- `[UNK]` Lock success: whether `hyprlock` starts and takes the session lock; behaviour when its grace period or `fail_timeout` applies; the PAM faillock lockout in [LW:84] is documentary.
- `[UNK]` Whether the compositor exposes `hyprland-lock-notify-v1` on this host. This decides whether `inhibit_sleep = 3` waits and whether `on_lock_cmd` works ([HC:104-107]; `idle-lock-plane.md` §11 item 6).
- `[UNK]` Whether the `pidof hyprlock ||` guard holds against the backgrounded `( hyprlock; omarchy-system-wake ) &` in `omarchy-system-lock` (race is not analysed).
- `[UNK]` Why hypridle is not running at probe time (`idle-lock-plane.md` §11 item 1). This note adds the declared start route above (hyprland.conf:4 → default autostart.conf:1); running state is not observed.
- `[UNK]` Whether the wiki ("Latest git", last updated 2026-08-26 [HW:120]) matches the v0.1.8 and v0.9.6 tag bytes; the wiki documents `condition_cmd`, which the v0.1.8 source also contains ([HC:71]), so the two agree on that key only.
- `[UNK]` hyprlock source behaviour (grace, fail_timeout, fingerprint, faillock): hyprlock v0.9.6 source not opened this round; wiki and README only.
- `[UNK]` The wiki's example-config link target (`[LW:8]` "which can be found here"): the upstream `example/` paths 404 at both tags.
- `[UNK]` Multi-monitor behaviour of the chain (`idle-lock-plane.md` §11 item 8).
- `[UNK]` Host binary version of hypridle and hyprlock against the tags above.
