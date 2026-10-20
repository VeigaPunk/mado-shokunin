# HostBackgroundChain — where the wallpaper is started, and with what path

Seat: MadoR18.HostBackgroundChain (scout, leaf). Round 18 / w1.
Question: file-bytes only — find where `swaybg` (or `hyprpaper`) is started at session start on
this host, and which path it is given. Never run them, never query services.
Method: `grep -rn`, `cat`, `sed`, `ls`, `stat`, `readlink`, `sha256sum`, `cmp`, `od`, `strings`
on binaries. No pacman/systemctl/journalctl/pgrep. No web source opened, so no fetch receipts.

All paths below are absolute on the host. `sha256:` values are of the file bytes named.

---

## 1. Observed facts (file bytes, no execution)

### 1.1 The only session-start launch site

```
sha256: acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441
/home/vgpnk/.local/share/omarchy/default/hypr/autostart.conf:5
```

Verbatim line 5 (78 bytes, `swaybg` begins at column 25, single trailing `\n`, confirmed by `od -c`):

```
exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill
```

- `hyprpaper` appears **nowhere** under `~/.config` or `~/.local/share/omarchy` (grep, 0 hits).
- No systemd user unit mentions `swaybg`: `grep -rln swaybg /usr/lib/systemd/user ~/.config/systemd/user` → 0 hits.
- `~/.config/systemd/user/` has no wallpaper unit; `graphical-session.target.wants` contains only
  `elephant.service` and `swayosd-server.service` (symlinks).
- `~/.config/omarchy/hooks/post-boot.d/weather.sample` and `theme-set.d/show-theme-notification.sample`
  are the only hook files (`.sample`, inert) and contain no background logic.
- Full-checkout grep for `swaybg` returns exactly 5 sites: the autostart line above, plus four
  lines in two maintenance scripts (§1.4) and one package-list line
  (`~/.local/share/omarchy/install/omarchy-base.packages:120:swaybg`).

### 1.2 Sourcing chain that reaches that line

```
sha256: ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365
/home/vgpnk/.config/hypr/hyprland.conf:4
source = ~/.local/share/omarchy/default/hypr/autostart.conf
```

Sourcing order (line numbers in `~/.config/hypr/hyprland.conf`): defaults at :4–:13
(autostart, media/clipboard/tiling-v2/utilities bindings, envs, looknfeel, input, windows,
`~/.config/omarchy/current/theme/hyprland.conf`), personal overlays at :16–:20, toggles at :23,
then ai-usage (:29) and gkeep (:32). The autostart default is sourced **once**, at :4.

### 1.3 The user override exists but does not touch the background

```
sha256: 5ace17016fe2998aa6e7ad2221c1889b430aa4b94faf5ef1f907d6301dd5fc46
/home/vgpnk/.config/hypr/autostart.conf
```

Its only active line is `exec-once = /home/vgpnk/.local/share/grok-bot/appimage --ozone-platform=x11`
(the other two lines are comments). It adds an autostart, it does not replace or re-launch `swaybg`.
A backup `autostart.conf.bak.1791942509` (`sha256: 8b472371e78b7f8b9656b53bfe2290ff1f96b14e90bb063ebe1e3316437057ed`)
contains only the two comment lines.

Net at session start: **exactly one** `swaybg` exec-once, inherited from the omarchy default.

### 1.4 The path handed to `swaybg`, resolved

Argument as written: `-i ~/.config/omarchy/current/background` (mode `-m fill`, no `--color`).

```
/home/vgpnk/.config/omarchy/current/background
  lrwxrwxrwx  inode=27341  size=71  mtime=2026-10-03T17:49:02-03:00
  -> /home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg

/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg
  -rw-r--r--  size=1681677  mtime=2026-10-03T17:49:02.541927358-03:00
  sha256: 55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac
  JPEG/JFIF, Exif (Adobe Photoshop 24.6, 2023-08-04), baseline, 3840x2160, 3 components
```

`sha256sum` on the symlink resolves to the same digest (`55fa691a…`), i.e. the link's content
identity is the JPEG, and the link is **absolute**, so it is immune to the caller's cwd.

`~/.config/omarchy/current` and `~/.config/omarchy/current/theme` are **real directories**, not
symlinks (`stat -c %F` → `directory`; inode 27311 for `theme`). `current/theme.name` is
`matte-black` (12 bytes incl. newline). `~/.config/omarchy/themed/` holds only
`alacritty.toml.tpl.sample`; `~/.config/omarchy/themes/` is empty.

The JPEG is a byte-identical copy of the checkout theme file:

```
sha256: 55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac
/home/vgpnk/.local/share/omarchy/themes/matte-black/backgrounds/0-ship-at-sea.jpg
cmp -> IDENTICAL
```

This matches `omarchy-theme-set` (`sha256: 79069c80…`, lines 24–42): it copies the official theme
into `current/next-theme`, then `rm -rf current/theme && mv next-theme current/theme`, writes
`theme.name` (:45), then calls `omarchy-theme-bg-next` (:48–:50) unless `OMARCHY_THEME_SKIP_BACKGROUND=1`.
So `current/theme/` is a **copy**, and a theme switch replaces the directory the background symlink
points into; the link's absolute target survives only because `bg-next` re-points it in the same run.

### 1.5 Other writers of the same symlink (not session start)

- `~/.local/share/omarchy/bin/omarchy-theme-bg-set` (`sha256: 638f265f…`) — `:13` defines
  `CURRENT_BACKGROUND_LINK="$HOME/.config/omarchy/current/background"`, `:21` re-points it
  (`ln -nsf`), `:24–:25` `pkill -x swaybg` then `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill`.
- `~/.local/share/omarchy/bin/omarchy-theme-bg-next` (`sha256: ee482812…`) — same link at `:9`;
  backgrounds enumerated with `find -L` over `~/.config/omarchy/backgrounds/<theme>/` and
  `current/theme/backgrounds/`, `sort -z` (:11); re-launch at `:49–:50`. Empty-set fallback is
  `swaybg --color '#000000'` (:16–:17), i.e. no image at all.
- `~/.config/hypr/hyprlock.conf:10` and `~/.local/share/omarchy/config/hypr/hyprlock.conf:10`
  (identical files, both `sha256: b8d173dc…`) — `background { path = ~/.config/omarchy/current/background }`.
  The lock screen consumes the same symlink; it does not launch `swaybg`.

### 1.6 Versions, by file read only

`/var/log/pacman.log` (grep, line numbers as printed):

```
:1158  [2026-10-03T17:44:27-0300] [ALPM] installed swaybg (1.2.2-1)
:848   [2026-10-03T17:44:22-0300] [ALPM] installed hyprland (0.56.0-2)
:1797  [2026-10-11T16:14:32-0300] [ALPM] upgraded hyprland (0.56.0-2 -> 0.56.2-2)
:2733  [2026-10-20T09:16:38-0300] [ALPM] upgraded hyprland (0.56.2-2 -> 0.56.2-4)
```

`swaybg` has exactly one pacman.log row (the install); no upgrade, no removal. Binary identity:
`/usr/bin/swaybg` `-rwxr-xr-x 31536` `sha256: e36544a1faf6cb4f91493062684f0c4c5d95bce5454e1739a5ccde925ceffe27`.
`uwsm-app` wrapper: `/usr/bin/uwsm-app` `sha256: 8be631abfe3671f618ba4d4866ba85c4d79bd58c15a5afd9065e4cc5a42bbc4c`
(448-byte unit `/usr/lib/systemd/user/wayland-wm-app-daemon.service` present).

Not verified here: the omarchy checkout tag (`.git` tag read was another seat's item); the
`/usr/bin/Hyprland` binary (`strings` shows both `v0.56.2` and `Hyprland 0.57`, which is
contradictory — no version claim is made from the binary; only the pacman.log rows above).

---

## 2. Inference `[INFERENCE]`

1. **`~` expansion happens in the shell that Hyprland spawns.** The exec line relies on `~`; a
   literal-`~` `execvp` would fail. `strings /usr/bin/Hyprland` contains `/bin/sh` (string 45887)
   and no `bash` string, consistent with exec commands going through `/bin/sh -c`. Therefore
   `~` expands to `/home/vgpnk` and the effective argument is
   `/home/vgpnk/.config/omarchy/current/background`. This is consistent with the fact that the same
   convention (`~` inside `source =`) is used on every adjacent line of `hyprland.conf`, and those
   sources demonstrably resolve (the theme file's directives are in effect in the sourced chain).
2. **`uwsm-app --` does not change the path.** The wrapper is a pipe client for
   `wayland-wm-app-daemon.service` (`/usr/bin/uwsm-app:23-27`: `PIPE_IN`/`PIPE_OUT` under
   `$XDG_RUNTIME_DIR`, `DAEMON_UNIT=wayland-wm-app-daemon.service`); it forwards argv into a
   transient app unit. So `swaybg -i … -m fill` is started as its own unit, not as a child of Hyprland.
   If the daemon is absent, the launch fails silently at session start and the compositor background
   stays unset — the symlink and image would still be correct.
3. **Ordering.** `exec-once` line 5 runs after lines 1–4 in the same file, but Hyprland does not
   serialize exec-once against compositor readiness; `swaybg` is expected to bind a Wayland output
   once one exists (`-m fill` letterboxes/crops to the output). Whether it retries on late outputs
   is not evidenced here.
4. **`-m fill`** is the swaybg scaling mode passed verbatim (78-byte line, `fill` final token);
   the image is 3840x2160 while `~/.config/hypr/monitors.conf` was not read for the current mode set,
   so per-output crop behavior is unstated.

---

## 3. Unexercised behavior and remaining unknowns `[UNK]`

- `[UNK]` Whether a `swaybg` process is running *right now*: not probed (host pause forbids
  process/service queries; `pgrep` deliberately not run).
- `[UNK]` Whether `wayland-wm-app-daemon.service` is active in this session — unit file presence is
  observed (§1.6), liveness is not.
- `[UNK]` Whether `swaybg` re-resolves the `-i` symlink after a theme change; `bg-set`/`bg-next`
  both `pkill -x swaybg` and relaunch, which suggests the path is resolved at startup, but the
  binary's behavior was not observed.
- `[UNK]` Monitor hotplug / lid-close behavior; `omarchy-recover-internal-monitor.service` is
  wanted by `graphical-session-pre.target`, but no background logic was found in it (not read in depth).
- `[UNK]` What happens when `~/.config/omarchy/current/background` is deleted (rather than
  re-pointed): the default line has no fallback; only `bg-next` has the `--color '#000000'` branch.
- `[UNK]` Hyprland's exact exec path/expansion (see §2.1) — inferred from one binary string, not
  from upstream source or docs in this seat.

---

## 4. Reproduction (file bytes only, safe under host pause)

```sh
grep -rn 'swaybg\|hyprpaper' ~/.config/hypr ~/.config/uwsm \
  ~/.local/share/omarchy/default ~/.config/systemd
grep -n '^source' ~/.config/hypr/hyprland.conf
sed -n '5p' ~/.local/share/omarchy/default/hypr/autostart.conf | od -c
readlink ~/.config/omarchy/current/background
sha256sum ~/.config/omarchy/current/background
grep -n 'swaybg' /var/log/pacman.log
```

No command here launches `swaybg`, queries a service, or touches the compositor.

## 5. Handoff note for the P5 route note

For `corpus/knowledge/theme-route-r18.md`, the session-start wallpaper contract is a single
`exec-once` at `~/.local/share/omarchy/default/hypr/autostart.conf:5`
(`sha256: acb6a668…`), sourced from `~/.config/hypr/hyprland.conf:4` (`sha256: ce7483f3…`),
handing the **symlink** `~/.config/omarchy/current/background` (absolute target
`current/theme/backgrounds/0-ship-at-sea.jpg`, `sha256: 55fa691a…`) to `swaybg -i … -m fill`.
The lock screen reads the same symlink (`~/.config/hypr/hyprlock.conf:10`). Host binary versions
are file-read only: swaybg 1.2.2-1, hyprland 0.56.2-4. No observed runtime behavior is claimed.

Tooling: none installed or updated. No web fetch performed (no receipts). No `pacman`/`systemctl`/
`hyprctl`/`pgrep` invocation; no writes outside this report.
