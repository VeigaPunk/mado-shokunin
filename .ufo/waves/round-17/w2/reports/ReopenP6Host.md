# ReopenP6Host — independent re-hash and anchor re-check of `idle-lock-route-r17.md` § Host declaration

Date: 2026-10-20. Seat: `MadoR17.ReopenP6Host`, wave 2 (FALSIFY). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD
`988b858bd6049bc709807534fd725c05264f7e60` (pushed). This file is the only
write; no commit, no git mutation, no jj, no delegation.

Method: host config trees read as file bytes only — `sha256sum`, `wc -c -l`,
`cat -n`, `grep -nE`, `cmp`, `ls -l`, `readlink -f`, `sed -n`, `tail -c | od`.
Nothing from any config or script was executed: **no** `pacman`/`yay`/`paru`
(not even `-Q`/`-Si`/`-Sp`/`-Fl`), no `sudo`, no `systemctl`/`loginctl`/
`journalctl`, no `hyprctl`/`libinput`/`evtest`/`wayland-info`/`hypridle`/
`hyprlock`/`alacritty`/`xdg-terminal-exec`/`waybar`/`walker`/`omarchy-*`/
`notify-send`, no `pgrep`/`pidof`/`pkill`, no screenshots or probes.
`/var/log/pacman.log` was read with `grep`/`sed` only.

**install: none.** No tool was installed, updated or queried.

Note under attack is byte-identical at HEAD and in the worktree (no stale-copy
falsification available):

```text
$ git show 988b858:corpus/knowledge/idle-lock-route-r17.md | sha256sum
abb4b45ddd8d652cabfbe0e072d9640266c2bc0b78c6de178cb6a6cb7e475afc  -
$ sha256sum corpus/knowledge/idle-lock-route-r17.md
abb4b45ddd8d652cabfbe0e072d9640266c2bc0b78c6de178cb6a6cb7e475afc  corpus/knowledge/idle-lock-route-r17.md
$ git diff --stat 988b858 -- corpus/knowledge/idle-lock-route-r17.md
(empty)
```

Tags: `[OBS]` bytes observed this run · `[INF]` inference from those bytes ·
`[UNK]` not observable under the host pause.

## 1. Hash and size re-check — 9/9 match `[OBS]`

§ Host declaration's table has 7 rows; `hyprland.conf` is hashed in the
following prose paragraph, and `~/.config/hypr/autostart.conf` is hashed in the
same paragraph. All 9 were re-hashed:

| file (under `/home/vgpnk`) | note sha256 | observed sha256 | note B / L | observed B / L | verdict |
|---|---|---|---|---|---|
| `.config/hypr/hypridle.conf` | `e7d3b8dd…07de41` | `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41` | 765 / 19 | 765 / 19 | match |
| `.config/hypr/hyprlock.conf` | `b8d173dc…68fc1` | `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1` | 742 / 43 | 742 / 43 | match |
| `.config/omarchy/current/theme/hyprlock.conf` | `3ef010e7…7ad0b` | `3ef010e72b5f69113e1500bb083fb053f9f121212ad5ed4fe74ad8d12507ad0b` | 176 / 5 | 176 / 5 | match |
| `.local/share/omarchy/bin/omarchy-system-lock` | `c1dd3881…b9ce1` | `c1dd3881e8aea9106cd844cc1f8ab4bcd4fcb07b81eefeab5e7a225e282b9ce1` | — / 33 | 699 / 33 | match |
| `.local/share/omarchy/bin/omarchy-system-wake` | `09ad52b0…3d3d4` | `09ad52b0f184ced3756b3ba5cdcee743ff78174dd9f83334c68ba4ed110bd3d4` | — / 9 | 228 / 9 | match |
| `.local/share/omarchy/bin/omarchy-launch-screensaver` | `ba783a3a…8fa12` | `ba783a3a55c134af4e7fe4111d9ef6fc7796d03a78bb7f114eeee6dd3758fa12` | — / 59 | 1641 / 59 | match |
| `.local/share/omarchy/default/hypr/autostart.conf` | `acb6a668…a0441` | `acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441` | — / 16 | 742 / 16 | match |
| `.config/hypr/autostart.conf` (prose) | `5ace1701…5fc46` | `5ace17016fe2998aa6e7ad2221c1889b430aa4b94faf5ef1f907d6301dd5fc46` | — | 210 / 5 | match |
| `.config/hypr/hyprland.conf` (prose) | `ce7483f3…0f8365` | `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365` | — | 1329 / 32 | match |

Structural observations that could have falsified a row but did not: all nine
files are regular files ending in a single LF; the two idle configs contain no
CR (`grep -c $'\r'` → 0 each), so `cat -n` anchors cannot drift on line
splitting. `~/.config/omarchy/current/theme/hyprlock.conf` resolves by
`readlink -f` to exactly the path the note names. The same mtimes wave 1
recorded (Oct 3 17:44 for both idle configs, Oct 3 17:49 for the theme file)
are still the observed mtimes, so no host drift occurred between wave 1 and
this re-run.

## 2. Line-anchor re-check — every quoted anchor reproduces `[OBS]`

Each row gives the note's anchor and the bytes actually at that coordinate
(`cat -n`).

| # | note claim / anchor | observed bytes | verdict |
|---|---|---|---|
| 1 | `lock_cmd = omarchy-system-lock` — hypridle.conf:2 | `    lock_cmd = omarchy-system-lock                         # lock screen and 1password` | match |
| 2 | `before_sleep_cmd = OMARCHY_LOCK_ONLY=true omarchy-system-lock` — :3 | identical substring at :3 | match |
| 3 | `after_sleep_cmd = sleep 1 && omarchy-system-wake` — :4 | identical substring at :4 | match |
| 4 | `inhibit_sleep = 3` — :5 | `    inhibit_sleep = 3                                      # wait until screen is locked` | match |
| 5 | six keys (`ignore_dbus_inhibit`, `ignore_systemd_inhibit`, `ignore_wayland_inhibit`, `on_lock_cmd`, `on_unlock_cmd`) "not set" | `grep -nE` over hypridle.conf → no match for any | match |
| 6 | listener 1: `timeout = 150`, `on-timeout = pidof hyprlock \|\| omarchy-launch-screensaver`, no on-resume — :9-12 | block at 9-12; :10 timeout, :11 guarded command, :12 `}` | match |
| 7 | listener 2: `timeout = 152`, `on-timeout = omarchy-system-lock`, `on-resume = omarchy-system-wake` — :15-19 | :16, :17, :18 exactly; :19 `}` | match |
| 8 | host comment — :14 | `# Lock system after 5 minutes (screensaver resets idle timer, so have to just do half + 2s margin)` | match |
| 9 | hyprlock `source = ~/.config/omarchy/current/theme/hyprlock.conf` — hyprlock.conf:1 | exact at :1 | match |
| 10 | `general { ignore_empty_input = true }` — :3-5 | :3 `general {`, :4 `ignore_empty_input = true`, :5 `}` | match |
| 11 | `background { path = …/background; blur_passes = 3 }` — :7-12 | :7 `background {`, :10 `path = ~/.config/omarchy/current/background`, :11 `blur_passes = 3`, :12 `}` | match |
| 12 | `animations { enabled = false }` — :14-16 | :14 `animations {`, :15 `enabled = false`, :16 `}` | match |
| 13 | `input-field` 650×100, `fade_on_empty = false`, `fail_text` `$FAIL ($ATTEMPTS)` — :18-39 | :18 open, :20 `size = 650, 100`, :34 `fail_text = <i>$FAIL ($ATTEMPTS)</i>`, :38 `fade_on_empty = false`, :39 `}` | match |
| 14 | `auth { fingerprint:enabled = false }` — :41-43 | :41 `auth {`, :42 value, :43 `}` | match |
| 15 | `hide_cursor`, `fail_timeout`, `pam:module`, `grace` "not set" | `grep -nE 'hide_cursor\|fail_timeout\|pam\|grace'` → no match | match |
| 16 | theme file: five vars only, no timing keys — :1-5 | exactly `$color`, `$inner_color`, `$outer_color`, `$font_color`, `$check_color`; 5 lines/176 B | match |
| 17 | omarchy-system-lock: `if pidof hyprlock` empty → `( hyprlock; omarchy-system-wake ) &` — :8-13 | :8 `if ! pidof hyprlock >/dev/null; then`, :9 `(` … :12 `) &`, :13 `fi` | match |
| 18 | `hyprctl switchxkblayout all 0` — :16 | exact at :16 | match |
| 19 | 1password locked if running — :19-21 | :19 `if pgrep -x "1password" >/dev/null; then`, :20 `1password --lock &`, :21 `fi` | match |
| 20 | `pkill -f org.omarchy.screensaver` — :24 | exact at :24 | match |
| 21 | `OMARCHY_LOCK_ONLY` guard, then `sleep 3`, then display/keyboard off — :26-32 | :26 `if [[ ${OMARCHY_LOCK_ONLY:-false} != "true" ]]; then`, :28 `sleep 3`, :29 `pidof hyprlock >/dev/null \|\| exit 0`, :30 keyboard off, :31 display off, :32 `) &` | match |
| 22 | omarchy-system-wake — :8, :9 | :8 `omarchy-brightness-display on`; :9 `omarchy-brightness-keyboard restore` | match |
| 23 | launch-screensaver exits 1 without `tte` — :5-7 | :5 `if ! command -v tte &>/dev/null; then`, :6 `exit 1`, :7 `fi` | match |
| 24 | exits 1 when `screensaver-off`, unless `force` — :13-15 | :13 `if omarchy-toggle-enabled screensaver-off && [[ $1 != "force" ]]; then`, :14 `exit 1`, :15 `fi` | match |
| 25 | `walker -q` — :18 | exact at :18 | match |
| 26 | terminal branches Alacritty/ghostty/foot/kitty — :26-56; fallback `notify-send` — :53-54 | :26 `case $terminal in`; arms :27-32, :33-39, :40-45, :46-51; `*)` :53, `notify-send -u low …` :54; `esac` :56 | match |
| 27 | default autostart: `exec-once = uwsm-app -- hypridle` — :1 | exact at :1; file 742 B / 16 L | match |
| 28 | `~/.config/hypr/autostart.conf` does not start hypridle | 5 lines: two comments, a blank, a Grok Bot `exec-once`; `grep hypridle` → no match | match |
| 29 | `hyprland.conf:4` = `source = ~/.local/share/omarchy/default/hypr/autostart.conf` | exact at :4 | match |
| 30 | pacman.log version anchors — `pacman.log:1792` / `:1798` | `:1792 … upgraded hypridle (0.1.7-10 -> 0.1.8-2)`; `:1798 … upgraded hyprlock (0.9.6-1 -> 0.9.6-3)`, both `2026-10-11T16:14:32-0300`; no later `hypridle`/`hyprlock` line in the 3160-line log | match |

## 3. Falsification probes that came back negative `[OBS]`

The aim was to break the note, not to re-print it. Each probe below was chosen
because a hit would have contradicted a host-declaration claim.

1. **Stale note.** Note blob at HEAD vs worktree: identical sha
   (`abb4b45d…`), empty diff → the anchors being checked are the landed ones.
2. **Alternate declared start route for hypridle.** `~/.config/systemd/user/`
   has no `hypridle.service`; `default.target.wants/` symlinks are
   shim/ai-usage/elephant/swayosd/ssh-agent only — no hypridle;
   `.config/systemd/user/graphical-session*.target.wants/` likewise.
   `/usr/lib/systemd/user/hypridle.service` exists as packaged payload but has
   no enabling symlink under `~/.config`. `/etc/hypr/` absent. So the note's
   single declared route (hyprland.conf:4 → default autostart.conf:1) is the
   only declared route, and "does not start hypridle" for the user autostart
   holds.
3. **Second idle declaration in a sourced file.** Recursive `grep` for
   `hypridle|hyprlock` over `~/.config/hypr/`, `~/.local/share/omarchy/default/hypr/`,
   `~/.local/state/omarchy/toggles/hypr/` (glob sourced at hyprland.conf:23),
   and `~/.config/omarchy/current/` returns exactly three lines:
   hypridle.conf:11, hyprlock.conf:1, default autostart.conf:1. The theme's
   `hyprland.conf` (sourced at :13) contains neither token. No omitted route.
4. **Deployed-copy identity.** `cmp` of `~/.config/hypr/hypridle.conf` and
   `hyprlock.conf` against `~/.local/share/omarchy/config/hypr/…` → rc 0 both;
   the hashed files are the shipped payload, and the only `.bak` siblings in
   `~/.config/hypr/` are `autostart.conf.bak.1791942509` and
   `hyprland.conf.bak.1792267376` — no idle-file backup that could shadow them.
5. **Independent wave-1 agreement.** Wave-1 receipts record the same digests
   and sizes: `HostIdleFiles.md:29-31` (765/19, 742/43, 176/5 with matching
   shas), `:106-108` (699/33, 228/9, 1641/59 with matching shas),
   `HostOmarchyLockScripts.md:20-23`, `FrontierDraft.md:20-21`. No drift
   between wave 1 and this wave-2 re-read.

## 4. Verdict

**The attack failed.** 9/9 file digests, 9/9 byte/line counts (where the note
states them), all 30 anchor groups, both quoted absence sets, and the
pacman.log version anchors reproduce exactly from current host bytes, and the
note's blob is unchanged at HEAD. No counterexample was found in the host
declaration: not a hash, not a line number, not a quoted fragment, not a
negative claim. What the note does *not* claim remains unclaimed — every
runtime fact stays `[UNK]` (§ Unexercised behavior, unchanged): listener
firing, lock success, `hyprland-lock-notify-v1` presence, the
`pidof hyprlock` race in the backgrounded lock subshell, and why hypridle was
absent at the earlier probe time. This report adds no runtime observation.

Residual gap in coverage, stated plainly: the note's upstream anchors
(`[HW:*]`, `[LW:*]`, `[HC:*]`, `[HH:*]`, `[HM:*]`, `[HR:*]`, `[LR:*]`) are out
of this seat's scope and were not re-fetched; only host bytes were attacked.
Host package state beyond the log line (running binary, Arch patches) stays
`[UNK]`, as the note itself says.
