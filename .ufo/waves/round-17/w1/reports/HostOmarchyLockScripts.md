# Host omarchy lock/wake/screensaver scripts — file-byte inventory (round 17, W1)

Seat: `MadoR17.HostOmarchyLockScripts`. Scope: locate the three scripts named by
`~/.config/hypr/hypridle.conf`, record `sha256` + `cat -n`, and summarise **as declared
text only** what each would invoke (hyprlock, 1password, display off/DPMS). Report only.

Method — file bytes only, no execution: `ls -l`, `sha256sum`, `cat -n`, `diff -u`,
`grep -n`, `find`, `wc -c`. No `pacman`/`yay`/`paru` (not even queries), no `sudo`, no
`systemctl`, no `hyprctl`, no `hypridle`/`hyprlock`, no `pgrep`/`pidof`/`pkill`, no
screenshots. Nothing below was run; every behavioural statement is quoted from the script
body. Read `corpus/lessons/round-16-verifier-spotcheck.md` first (done). No tools
installed or updated.

Tags: `[OBS]` byte observed in file · `[INF]` inference from those bytes · `[UNK]` unknown.

## 1. Locations and digests `[OBS]`

| Path | Bytes | Mode/mtime | sha256 |
|---|---|---|---|
| `~/.config/hypr/hypridle.conf` | 765 | `-rw-r--r--`, Oct 3 17:44 | `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41` |
| `~/.local/share/omarchy/bin/omarchy-system-lock` | 699 | `-rwxr-xr-x`, Oct 3 17:42 | `c1dd3881e8aea9106cd844cc1f8ab4bcd4fcb07b81eefeab5e7a225e282b9ce1` |
| `~/.local/share/omarchy/bin/omarchy-system-wake` | 228 | `-rwxr-xr-x`, Oct 3 17:42 | `09ad52b0f184ced3756b3ba5cdcee743ff78174dd9f83334c68ba4ed110bd3d4` |
| `~/.local/share/omarchy/bin/omarchy-launch-screensaver` | 1641 | `-rwxr-xr-x`, Oct 3 17:42 | `ba783a3a55c134af4e7fe4111d9ef6fc7796d03a78bb7f114eeee6dd3758fa12` |

All three resolved in `~/.local/share/omarchy/bin/` (the guess in the ticket was correct).

Declared-helper presence (existence + digest only; bodies not read this pass):

| Helper named by the three scripts | Present | sha256 |
|---|---|---|
| `omarchy-brightness-display` | yes | `62e6d7655258c875a81a31c345614bffb854a7f5db6f2a10e848090c5de3dc93` |
| `omarchy-brightness-keyboard` | yes | `f1305c06b0ecaea29c415f74738c462b062155a11332d87df72c97cde2ecc917` |
| `omarchy-toggle-enabled` | yes | `5f5b2797e2f5912f0c5e19f02ede429fdc2952dbf3f3d0c31f1d6e2964006988` |
| `omarchy-hyprland-monitor-focused` | yes | `c3f4e85b13ca93d09af97ee8470a8b45f69293ef6d6d3acf07ff13a77e158d26` |
| `omarchy-screensaver` | yes | `11d7487aa3eebe3eedb453bee844225d3c213e58da25678b4ab7a07381a551f6` |

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

`[OBS]` Declared shape: `inhibit_sleep = 3`, one 150 s listener whose command is
`pidof hyprlock || omarchy-launch-screensaver`, one 152 s listener with
`on-timeout = omarchy-system-lock` / `on-resume = omarchy-system-wake`. Lines 3–4 and 14
carry the declared rationale (lock before suspend without display-off; +2 s margin
because the screensaver resets the idle timer).

## 3. `omarchy-system-lock` — `cat -n` (699 B, 33 lines)

```text
     1	#!/bin/bash
     2	
     3	# omarchy:summary=Lock the computer and turn off the display
     4	# omarchy:group=system
     5	# omarchy:name=lock
     6	# omarchy:examples=omarchy system lock
     7	
     8	if ! pidof hyprlock >/dev/null; then
     9	  (
    10	    hyprlock
    11	    omarchy-system-wake
    12	  ) &
    13	fi
    14	
    15	# Set keyboard layout to default (first layout)
    16	hyprctl switchxkblayout all 0 > /dev/null 2>&1
    17	
    18	# Ensure 1password is locked
    19	if pgrep -x "1password" >/dev/null; then
    20	  1password --lock &
    21	fi
    22	
    23	# Avoid running screensaver when locked
    24	pkill -f org.omarchy.screensaver
    25	
    26	if [[ ${OMARCHY_LOCK_ONLY:-false} != "true" ]]; then
    27	  (
    28	    sleep 3
    29	    pidof hyprlock >/dev/null || exit 0
    30	    omarchy-brightness-keyboard off
    31	    omarchy-brightness-display off
    32	  ) &
    33	fi
```

`[OBS]` Declares, in order: (a) if no `hyprlock` process, background a subshell running
`hyprlock` then `omarchy-system-wake` (L10–11); (b) `hyprctl switchxkblayout all 0`
keyboard-layout reset, output discarded (L16); (c) **1password**: if `pgrep -x 1password`
matches, background `1password --lock` (L19–20); (d) `pkill -f org.omarchy.screensaver`
(L24); (e) unless `OMARCHY_LOCK_ONLY=true`, a backgrounded 3 s-later block that exits
unless `hyprlock` is by then running, then `omarchy-brightness-keyboard off` and
`omarchy-brightness-display off` (L26–33). Frontmatter summary L3: "Lock the computer and
turn off the display".

`[INF]` The `OMARCHY_LOCK_ONLY=true` form used as `before_sleep_cmd` deliberately skips
step (e): the display is left for the suspend path, matching the config comment on line 3.
No `set -e`; ordering means the 1password lock and screensaver kill happen regardless of
whether `hyprlock` was already running.

## 4. `omarchy-system-wake` — `cat -n` (228 B, 9 lines)

```text
     1	#!/bin/bash
     2	
     3	# omarchy:summary=Wake displays and restore brightness after idle
     4	# omarchy:group=system
     5	# omarchy:name=wake
     6	# omarchy:examples=omarchy system wake
     7	
     8	omarchy-brightness-display on
     9	omarchy-brightness-keyboard restore
```

`[OBS]` Entire body is two calls: display on, keyboard brightness restore. No branch, no
argument handling, no lock interaction.

## 5. `omarchy-launch-screensaver` — `cat -n` (1641 B, 59 lines)

```text
     1	#!/bin/bash
     2	
     3	# omarchy:summary=Launch the Omarchy screensaver in the default terminal on the system with the correct font configuration.
     4	
     5	if ! command -v tte &>/dev/null; then
     6	  exit 1
     7	fi
     8	
     9	# Exit early if screensave is already running
    10	pgrep -f org.omarchy.screensaver && exit 0
    11	
    12	# Allow screensaver to be turned off but also force started
    13	if omarchy-toggle-enabled screensaver-off && [[ $1 != "force" ]]; then
    14	  exit 1
    15	fi
    16	
    17	# Silently quit Walker on overlay
    18	walker -q
    19	
    20	focused=$(omarchy-hyprland-monitor-focused)
    21	terminal=$(xdg-terminal-exec --print-id)
    22	
    23	for m in $(hyprctl monitors -j | jq -r '.[] | .name'); do
    24	  hyprctl dispatch focusmonitor $m
    25	
    26	  case $terminal in
    27	  *Alacritty*)
    28	    hyprctl dispatch exec -- \
    29	      alacritty --class=org.omarchy.screensaver \
    30	      --config-file ~/.local/share/omarchy/default/alacritty/screensaver.toml \
    31	      -e omarchy-screensaver
    32	    ;;
    33	  *ghostty*)
    34	    hyprctl dispatch exec -- \
    35	      ghostty --class=org.omarchy.screensaver \
    36	      --config-file=~/.local/share/omarchy/default/ghostty/screensaver \
    37	      --font-size=18 \
    38	      -e omarchy-screensaver
    39	    ;;
    40	  *foot*)
    41	    hyprctl dispatch exec -- \
    42	      foot --app-id=org.omarchy.screensaver \
    43	      --config="$OMARCHY_PATH/default/foot/screensaver.ini" \
    44	      -e omarchy-screensaver
    45	    ;;
    46	  *kitty*)
    47	    hyprctl dispatch exec -- \
    48	      kitty --class=org.omarchy.screensaver \
    49	      --override font_size=18 \
    50	      --override window_padding_width=0 \
    51	      -e omarchy-screensaver
    52	    ;;
    53	  *)
    54	    notify-send -u low "✋  Screensaver only runs in Alacritty, Foot, Ghostty, or Kitty"
    55	    ;;
    56	  esac
    57	done
    58	
    59	hyprctl dispatch focusmonitor $focused
```

`[OBS]` Declares: `tte` must exist else exit 1 (L5–7); exit 0 if
`pgrep -f org.omarchy.screensaver` already matches (L10); exit 1 when
`omarchy-toggle-enabled screensaver-off` succeeds and `$1 != force` (L13–15); `walker -q`
(L18); terminal identity from **`xdg-terminal-exec --print-id`** (L21); one pass per
`hyprctl monitors -j` name (L23) focusing each monitor (L24) and dispatching the
per-terminal launcher with class/app-id `org.omarchy.screensaver`, `-e omarchy-screensaver`,
and a per-terminal config file (L26–52); `notify-send` low-urgency refusal message for any
other terminal (L54); restore focus to the previously focused monitor (L59).

`[INF]` Line 21 is the documentary junction to the P4 terminal surface: this script's
behaviour is selected by whatever `xdg-terminal-exec --print-id` returns, and the
`*Alacritty*` case (L27) is the branch the host's `~/.config/xdg-terminals.list` name would
take. This is a declared text path only — the branch taken at runtime is `[UNK]`.

## 6. What each would invoke, as declared text

| Script | Declared invoked commands (line) | Notable state it would touch |
|---|---|---|
| `omarchy-system-lock` | `hyprlock` (L10); `omarchy-system-wake` (L11); `hyprctl switchxkblayout all 0` (L16); `pgrep -x 1password` (L19); `1password --lock` (L20); `pkill -f org.omarchy.screensaver` (L24); `omarchy-brightness-keyboard off` (L30); `omarchy-brightness-display off` (L31) | a running hyprlock lock surface; keyboard layout XKB index 0; the 1password process; any `org.omarchy.screensaver` process; keyboard/display brightness |
| `omarchy-system-wake` | `omarchy-brightness-display on` (L8); `omarchy-brightness-keyboard restore` (L9) | display power/brightness; keyboard backlight |
| `omarchy-launch-screensaver` | `pgrep -f org.omarchy.screensaver` (L10); `omarchy-toggle-enabled screensaver-off` (L13); `walker -q` (L18); `omarchy-hyprland-monitor-focused` (L20); `xdg-terminal-exec --print-id` (L21); `hyprctl monitors -j` + `jq` (L23); `hyprctl dispatch focusmonitor` (L24, L59); `hyprctl dispatch exec` (L28, L34, L41, L47); `alacritty`/`ghostty`/`foot`/`kitty` with `-e omarchy-screensaver` (L29–31, 34–38, 41–44, 47–51); `notify-send` (L54) | Hyprland monitor focus; Walker; one screensaver terminal window per monitor |

Declared call graph from `hypridle.conf`:
`hypridle → {omarchy-system-lock, sleep 1 && omarchy-system-wake, pidof hyprlock ||
omarchy-launch-screensaver}`; downstream as in the table. `hyprlock` is reached only via
`omarchy-system-lock` (and gated on absence by `pidof hyprlock`); the screensaver is
reached only via `omarchy-launch-screensaver`.

### DPMS specifically

`[OBS]` The literal token `dpms` does **not** occur in any of the three scripts
(`grep -nE 'dpms|...'` over all three returned no `dpms` hit). Display power-off is
delegated to `omarchy-brightness-display off` (L31 of `omarchy-system-lock`) and
`omarchy-brightness-display on` (L8 of `omarchy-system-wake`); that helper exists
(digest in §1) but its body was **not** read this pass, so whether it uses DPMS,
`brightnessctl`, or a Hyprland dispatcher is `[UNK]`. `[INF]` The only direct
compositor-control calls in the lock path are `hyprctl switchxkblayout all 0` (layout, not
DPMS) and none in the wake path.

## 7. Provenance: user config is byte-identical to the Omarchy default `[OBS]`

- `sha256sum ~/.local/share/omarchy/config/hypr/hypridle.conf` =
  `e7d3b8dd…07de41`, identical to the user file; `diff -u` → `IDENTICAL`.
- `omarchy-refresh-hypridle` (127 B) declares: `omarchy-refresh-config hypr/hypridle.conf`
  then `omarchy-restart-hypridle`; `omarchy-restart-hypridle` (131 B) declares
  `omarchy-restart-app hypridle`.
- Also present: `~/.config/hypr/hyprlock.conf` 742 B, sha256
  `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1`, mtime Oct 3 17:44
  (same minute as `hypridle.conf`), and template
  `~/.local/share/omarchy/default/themed/hyprlock.conf.tpl`.

`[INF]` The 150/152 s idle thresholds and the three lock commands are **upstream Omarchy
defaults**, not host-specific customization, so a note describing them describes the
shipped design and cannot be read as a host-specific observation of tuning.

## 8. Overlap pointer (not an edit)

`[OBS]` `corpus/knowledge/idle-lock-plane.md` (382 lines) already covers this plane, but
`grep -nE '^(source|covers|surface):'` on it returns **nothing** — its first lines are prose
("Idle & lock plane — measured inventory (MADO-R4-2)"), so under the round-17 rubric
definition it would not satisfy a `source:`/`surface: P6` requirement as it stands. It also
records probe-environment commands (`hyprctl`, `systemctl --user status`, `pacman -Q`) that
this round's pause forbids; any reuse must stay documentary. Decision on upgrading that
file vs a new route note belongs to L1 and the rubric seat (see `MadoR17.ExistingIdleNotes`);
this seat made no edit outside this report.

## 9. Remaining unknowns

- `[UNK]` Whether `hyprlock`, `1password`, `walker`, `tte`, `alacritty`/`ghostty`/`foot`/
  `kitty`, `jq`, `hypridle` are installed and at what versions — no package or process
  queries were run (pause).
- `[UNK]` Runtime `xdg-terminal-exec --print-id` value and which `case` branch fires.
- `[UNK]` Mechanism behind `omarchy-brightness-display` (DPMS vs another path) — helper
  body not read.
- `[UNK]` `$OMARCHY_PATH` resolution used only by the `foot` branch (L43).
- No live idle transition, lock, wake, or screensaver was triggered or observed.

Report: .ufo/waves/round-17/w1/reports/HostOmarchyLockScripts.md
