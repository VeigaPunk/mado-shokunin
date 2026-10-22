# HostKitty — read-only host inventory of the kitty config tree (C2 evidence)

Seat: MadoR23.HostKitty (scout, leaf). Date 2026-10-22. Host unchanged: read-only probes only, no
`pacman` transaction, no write outside this file. No installs or upgrades were made or needed.

LSP note: this assignment is host inventory, not repository source semantics, so no language server
applies. Every fact below is a direct filesystem/process observation produced by the command shown;
the only text greps are inventory greps over config/scripts, not semantic proof of code behaviour.
Where a behaviour claim is made about an omarchy script it rests on the script body read in full at
`~/.local/share/omarchy/bin/`, cited per item.

## 1. The tree: `ls -la ~/.config/kitty/`

```
total 8
drwxr-xr-x 1 vgpnk vgpnk   80 Oct  3 19:02 .
drwxr-xr-x 1 vgpnk vgpnk 1692 Oct 22 04:55 ..
-rw-r--r-- 1 vgpnk vgpnk  954 Oct  3 19:02 kitty.conf
-rw-r--r-- 1 vgpnk vgpnk  953 Oct  3 19:02 kitty.conf.bak.20261003-190229
```

Two regular files, no subdirectories, no `*.diff`, no `themes/`, no `kitty.conf.d`.

`stat -c '%n size=%s mode=%A mtime=%y ctime=%z inode=%i'` — all three tree entries share mtime and
ctime `2026-10-03 19:02:29.839995618 -0300` (one write pass, same instant):

| path | bytes | mode | inode |
|---|---|---|---|
| `~/.config/kitty` | 80 (dir) | `drwxr-xr-x` | 21232 |
| `~/.config/kitty/kitty.conf` | 954 | `-rw-r--r--` | 21233 |
| `~/.config/kitty/kitty.conf.bak.20261003-190229` | 953 | `-rw-r--r--` | 38432 |
| `~/.local/share/omarchy/config/kitty/kitty.conf` (reference) | 953 | `-rw-r--r--` | 712 |

## 2. Sizes and SHA256 (exact command + output)

Command: `cd ~/.config/kitty && sha256sum kitty.conf kitty.conf.bak.20261003-190229; sha256sum ~/.local/share/omarchy/config/kitty/kitty.conf`

```
f875291ecfe64ebc4ddc588282bcdb20fb883769e9938148411efa378d7f1e70  kitty.conf
95eed20aaedb09627e00e3ff504919b585a54799aa41cb45bba5e17b91c8dd44  kitty.conf.bak.20261003-190229
95eed20aaedb09627e00e3ff504919b585a54799aa41cb45bba5e17b91c8dd44  /home/vgpnk/.local/share/omarchy/config/kitty/kitty.conf
```

Content shape only (no bodies printed; nothing secret-shaped exists in these files):

- First non-comment, non-empty line of all three files is identical:
  `1: include ~/.config/omarchy/current/theme/kitty.conf`
- Line count 34 in each; non-comment (directive) line count 20 in each.
- Directive names present, in file order (`grep -nE '^[[:space:]]*[^#[:space:]]' | sed -E 's/^([0-9]+:)([a-z_]+).*/\1\2/'`):
  `include` (1), `font_family` (4), `bold_italic_font` (5), `font_size` (6), `window_padding_width`
  (9), `hide_window_decorations` (10), `confirm_os_window_close` (11), `map` (14,15,17,19),
  `allow_remote_control` (22), `cursor_shape` (25), `cursor_blink_interval` (26),
  `shell_integration` (27), `enable_audio_bell` (28), `tab_bar_edge` (31), `tab_bar_style` (32),
  `tab_powerline_style` (33), `tab_title_template` (34).
- The include target exists: `~/.config/omarchy/current/theme/kitty.conf`, 27 lines, first non-comment
  line `foreground #bebebe` (theme `matte-black`, per `~/.config/omarchy/current/theme.name`). The
  `current` symlink resolves inside `~/.config/omarchy/current/`, i.e. per-theme colours are live
  data the tree depends on, not vendored content.

## 3. Does the tree match an omarchy default?

Command: `diff -u ~/.local/share/omarchy/config/kitty/kitty.conf <user file>`

- `kitty.conf.bak.20261003-190229` vs the omarchy-shipped default: **byte-identical**, `diff` rc=0,
  matching SHA256 `95eed20a…`. The backup *is* the unmodified omarchy default.
- `kitty.conf` vs the omarchy-shipped default: exactly one line differs.

```
@@ -3,7 +3,7 @@
 font_family JetBrainsMono Nerd Font
 bold_italic_font auto
-font_size        9.0
+font_size        12.5
```

- Net: the live tree is the omarchy default plus **one local preference** (`font_size 12.5` instead of
  `9.0`), plus a stale timestamped backup of the pristine default. No other local divergence.
- `allow_remote_control yes` is present and identical in both the user file and the shipped default
  (`sed -n '22p'` on each, and `git show HEAD:config/kitty/kitty.conf` in the omarchy checkout). This
  is a preference value, not a secret; recording it because it is a shell-integration/security-
  relevant default that any cited route row for this tree will inherit.
- The `.bak` suffix form (`YYYYMMDD-HHMMSS`) is **not** produced by `omarchy-refresh-config`, whose
  body uses `backup_config_file="$user_config_file.bak.$(date +%s)"` (epoch seconds). So the backup
  was made by something else (an editor save-with-backup or a hand script). Provenance is not
  established; see unresolved gaps.

## 4. Is the kitty binary installed? (three channels checked)

| probe | command | output |
|---|---|---|
| PATH | `command -v kitty` | (empty), rc=1 |
| PATH sweep | `for d in $(printf '%s' "$PATH" \| tr ':' ' '); do [ -e "$d/kitty" ] && ls -la "$d/kitty"; done` | no hits across all 19 PATH dirs (incl. `~/.local/share/omarchy/bin`) |
| pacman | `pacman -Q kitty` | `error: package 'kitty' was not found` |
| pacman (related) | `pacman -Qs kitty` | empty |
| flatpak | `command -v flatpak` | `error: command not found: flatpak` |
| snap / nix / appimage-run | `command -v …` | all absent |
| desktop entries | `ls /usr/share/applications ~/.local/share/applications \| grep -i kitty` | no `kitty.desktop`; only `Alacritty.desktop`, `foot-server.desktop`, `footclient.desktop` |
| fixed dirs | `ls /usr/local/bin /opt ~/.local/bin ~/.cargo/bin` | no `kitty`, no `kitten` |

`pacman -Qo` on a found binary: not applicable — no kitty binary exists on this host to query
ownership for. (For contrast, the terminal that *is* installed: `alacritty 0.17.0-1` from pacman,
`/usr/bin/alacritty`.)

## 5. Is any running process using it?

```
pgrep -a kitty                 -> no output, rc=1
pgrep -a -f kitty (filtered)   -> no output
ps -eo pid,comm,args | grep -Ei 'alacritty|foot|ghostty|kitty'
  2487 alacritty  alacritty --working-directory=/home/vgpnk
for n in kitty alacritty foot ghostty; do pgrep -x "$n"; done
  kitty     rc=1 pids=
  alacritty rc=0 pids=2487 291084
  foot      rc=1 pids=
  ghostty   rc=1 pids=
```

4190 processes are visible to this session's `ps`, so the negative is over a complete process table,
not a truncated one. `ps -eo pid,comm,args | grep -i kitty` returns nothing.

(Two probes run and discarded as unusable: a `/proc/*/environ` scan for `TERM=xterm-kitty` returned
`Permission denied` on every pid despite `/proc` being mounted `rw,nosuid,nodev,noexec,relatime`
without `hidepid`, so environment-level TERM evidence is unavailable here; the cmdline and comm
evidence above already covers process identity.)

## 6. Routing: would anything start kitty right now?

- `~/.config/xdg-terminals.list` (the list `xdg-terminal-exec` reads first) contains exactly
  `Alacritty.desktop`; it is byte-identical to the omarchy-shipped
  `~/.local/share/omarchy/config/xdg-terminals.list`. kitty is **not** in the preference order.
- No system fallback list exists: `/etc/xdg-terminals.list` and `/usr/share/xdg-terminals.list` are
  both absent (`ls` → `No such file or directory`), so `xdg-terminal-exec`'s
  `${XDG_CONFIG_DIRS:-/etc/xdg}` search adds nothing.
- `~/.local/share/omarchy/bin/omarchy-default-terminal` (read in full) derives the answer from that
  same list and prints `alacritty` when run now.
- The launch path itself is terminal-agnostic: `~/.config/hypr/bindings.conf:2` binds
  `SUPER, RETURN → uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`, and
  `TERMINAL=xdg-terminal-exec` in the live environment. So the binding resolves through the list
  above to Alacritty, confirmed by the running `alacritty` pid 2487.
- No autostart / systemd-user / uwsm unit references kitty:
  `grep -rn -i kitty ~/.config/autostart ~/.config/systemd ~/.config/uwsm` → empty.

## 7. Latent (conditional) consumers — present in code, not active on this host

Each requires the binary or an explicit user action, so none consumes the tree today:

| consumer | file:line | gate |
|---|---|---|
| font setter rewrites `~/.config/kitty/kitty.conf` and `pkill -USR1 kitty` | `~/.local/share/omarchy/bin/omarchy-font-set:15-17` | only if `~/.config/kitty/kitty.conf` exists — it does, so `omarchy font set <name>` **would** edit this file and pkill a non-existent process (harmless no-match). The tree is a live write target for that command. |
| terminal switcher writes `kitty.desktop` into `~/.config/xdg-terminals.list` | `~/.local/share/omarchy/bin/omarchy-default-terminal:23,30-34` | explicit `omarchy default terminal kitty` |
| installer | `~/.local/share/omarchy/bin/omarchy-install-terminal:19` (`omarchy-pkg-add kitty`) | explicit; needs sudo, and pacman transactions are paused host-wide |
| menu entries | `~/.local/share/omarchy/bin/omarchy-menu:406,413,420,555-559` | `omarchy-cmd-present kitty` gate for the switch entry → false today; the *install* entry is always listed |
| screensaver | `~/.local/share/omarchy/bin/omarchy-launch-screensaver:46-51` (`kitty --class=…`) | only when the active terminal is kitty |
| restart nudge | `~/.local/share/omarchy/bin/omarchy-restart-terminal:9-10` (`pgrep -x kitty`) | no match today |
| hyprland scroll rule | `~/.config/hypr/input.conf:45` `windowrule = match:class (Alacritty|kitty|foot), scroll_touchpad 1.5` | inert without a `kitty` window class (a string match, not a route) |
| tmux/bash integration | `~/.local/share/omarchy/default/tmux/tmux.conf:79` (`xterm-kitty:extkeys`), `default/bash/aliases:9-10` (`$TERM == xterm-kitty` → `kitty icat`) | only inside a kitty terminal; also active only under a `xterm-kitty` TERM |
| layouts/theme | `~/.local/share/omarchy/config/hypr/input.conf:44`, `migrations/{1758051607,1759895423,1760724934,1783833508}.sh` | historical: created the tree and appended its key maps |

## 8. Provenance of the tree (observed)

- `~/.local/share/omarchy/migrations/1758051607.sh:8-10` created `~/.config/kitty/kitty.conf` by
  copying the omarchy default ("Copy configs for ghostty + kitty so they're available as alternative
  terminal options") — the tree exists because omarchy plants all four terminal configs at install
  time, not because kitty was chosen.
- The 2026-10-03 19:02:29 pass touched **all four** planted terminal trees (alacritty, kitty, foot,
  ghostty) with the same single-line change — font size `9 → 12.5` — and in each tree it first wrote a
  timestamped backup that is byte-identical to the corresponding omarchy default:

  | tree | live file | .bak.20261003-190229 | .bak sha256 | vs default |
  |---|---|---|---|---|
  | alacritty | `alacritty.toml` 876 B, `size = 9 → 12.5` (line 13) | 873 B | `ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a` | identical |
  | kitty | `kitty.conf` 954 B, `font_size 9.0 → 12.5` (line 6) | 953 B | `95eed20aaedb09627e00e3ff504919b585a54799aa41cb45bba5e17b91c8dd44` | identical |
  | foot | `foot.ini` 516 B, `font=…:size=9 → size=12.5` (line 4) | 513 B | `8afc9646c61e58e67f244e50a9ce5d4a45546920511a06b47f7443a3998da602` | identical |
  | ghostty | `config` 1325 B, `font-size = 9 → 12.5` (line 7) | 1322 B | `e47630125605cb19c6b2c9bc33d767a0f3f1b5bf04cd4f36a2bb910897e24f78` | identical |

  The four directory mtimes stagger by ~1 ms in sequence — alacritty `19:02:29.838995642`, kitty and
  foot `.839995618`, ghostty `.840995595` — so this was one sequential loop over the four trees, not
  four independent edits. Every live file differs from its own backup by exactly one line. This is
  one batch "make text bigger" pass across all terminals, not per-terminal tuning — [INFERENCE on
  intent, FACT on the contents, hashes and mtime order].
- **Correction (peer-flagged, verified):** an earlier draft of this report said "only kitty kept a
  `.bak`; foot and ghostty did not". That was wrong and is retracted. The error came from a listing
  probe that piped `ls -la` through `sed -n '2,4p'`, which silently truncated each directory to
  `.`, `..` and the first file. A full `ls -la --time-style=full-iso` on all four directories, plus
  `sha256sum` of each backup against its omarchy default, shows four backups as tabulated above. The
  kitty inventory itself (§1, `ls -la` + `find`) is unaffected and remains exactly two files. Reported
  independently by the sibling seat `MadoR23.HostFoot` from `ls -la --time-style=full-iso`; the
  hash-level comparison above is my own verification.
- `~/.local/share/omarchy` is a git checkout: HEAD `8fcc9d604` (2026-07-20) on `master`,
  `version` file says `3.8.3`, `git describe --tags --always` says `v3.8.4` (both observed; the
  discrepancy is not resolved here). Its remote refs include `origin/fix/kitty-system-defaults` and
  `origin/security/disable-kitty-remote-control`, and a commit `eaed240be "Credit Erik Melton for the
  Kitty remote-control fix"` is reachable only from non-master refs — while `master`'s shipped
  `config/kitty/kitty.conf:22` still reads `allow_remote_control yes`. So the shipped default this
  tree copies is the pre-fix variant; the hardening branch is not merged at the installed revision
  [INFERENCE on "pre-fix", FACT on the file contents and ref containment].

## 9. Verdict

**The `~/.config/kitty/` tree is not consumed by anything on this host now.** It is a dormant,
omarchy-planted alternative-terminal config: no kitty binary on any install channel (PATH sweep,
pacman, no flatpak/snap/nix), no `kitty.desktop`, no running process, kitty absent from the
`xdg-terminals.list` preference order (which names only `Alacritty.desktop` and is itself the omarchy
default), the default-terminal resolver answering `alacritty`, and the live terminal being
`alacritty` (pid 2487). The only code paths that would touch it are explicit user commands
(`omarchy font set`, `omarchy default terminal kitty`, `omarchy install terminal kitty`) or a
kitty-hosted session, none of which is active. Its entire distinguishing local content is one font
size (`12.5`), set by the same four-tree batch pass that set the same size in the alacritty, foot and
ghostty trees (§8); its `.bak` is the pristine omarchy default.

## 10. What this means for C2 (kitty route rows)

- Sourceable now, host-side: the kitty tree exists, is 2 files / 1 live config, is the omarchy
  default plus `font_size 12.5`, includes a theme fragment at
  `~/.config/omarchy/current/theme/kitty.conf`, and is present-but-unconsumed on this host. Any route
  row that claims the host *uses* kitty would be false; a row that claims the host *carries* the tree
  and which omarchy command rewrites it is supported by the bodies cited in §7.
- The tree's own reference points outward rather than being self-contained: the single `include`
  line makes the effective config `~/.config/omarchy/current/theme/kitty.conf` (27 lines,
  theme `matte-black`). A route row for kitty that ignores the theme include would document a
  different config than kitty would actually read.
- This report is host inventory, **not** a `mined` SOURCES row: C2's counter requires a
  `terminal-trees-r23.md` route row citing a SOURCES row naming kitty that was mined 2026-10-22. My
  evidence can back such a row, but does not itself satisfy the counter. The kitty upstream source
  (sw.kovidgoyal.net / the kitty repo) was **not** opened by me; the `MadoR23.SrcKitty` seat is on
  that leg.

## Unresolved

1. What created `kitty.conf.bak.20261003-190229` — the suffix form matches no omarchy script
   (`omarchy-refresh-config` uses epoch). A fleet-wide sweep for that pattern
   (`grep -rln -E 'bak\.%Y%m%d|bak\.\$\(date \+%Y%m%d|%Y%m%d-%H%M%S' /home/vgpnk/Projects/shokunin
   /home/vgpnk/.local/bin /home/vgpnk/.agents`; the `/home/vgpnk/Projects/shokunin` leg exhausted its
   300 s cap before finishing the tree, so this is near-exhaustive rather than exhaustive) returned
   six paths, all unrelated: a `CR8.md` doc in kaidoku-shokunin (plus two clone/worktree copies of
   it), `research/round-18-kimi-model-routing/routing/APPLY.md`, and two model-routing scripts —
   `routing/splice_secondary.py:165` `strftime("%Y%m%d-%H%M%S")` and
   `cascade-legorder/scripts/apply_legorder.py:216` `time.strftime("%Y%m%d-%H%M%S")`, both stamping
   their own routing outputs and neither mentioning `kitty` or `~/.config/kitty` (checked with
   `grep -n -E 'kitty|\.config/kitty'` on both: no hits). So the `YYYYMMDD-HHMMSS` form is a fleet
   convention for backups, but no fleet tool applying it touches terminal configs. The backup's
   *content* is established (byte-identical to the shipped default); only the writer is unknown —
   most likely an editor save-with-backup or a hand command [INFERENCE].
2. Why the batch pass wrote a backup only in some trees — **retracted, premise false**: all four trees
   got one (§8). What remains genuinely unknown is why the backup *name* embeds wall-clock local time
   rather than epoch seconds; no script in the fleet applies that name to a terminal config.
3. omarchy installed revision: `version` file `3.8.3` vs `git describe` `v3.8.4`.
4. `/proc/*/environ` is unreadable in this session (permission denied on every pid), so no
   environment-level `TERM` corroboration was possible; process/cmdline evidence stands.

## Commands run (exhaustive, all read-only)

`ls -la ~/.config/kitty/`; `find ~/.config/kitty -maxdepth 3 -printf '%y %s %p\n'`;
`stat -c …` on the 4 paths; `sha256sum` on the 3 configs; `diff -u` default↔user, default↔backup,
default↔foot, default↔ghostty; `awk`/`grep -nE`/`wc -l` for line shape and directive names;
`sed -n '22p'` on both kitty configs; `command -v kitty`; PATH-directory sweep for `kitty`/`kitten`;
`pacman -Q kitty`; `pacman -Qs kitty`; `pacman -Q alacritty`; `command -v` for
`flatpak snap nix appimage-run alacritty foot ghostty xdg-terminal-exec`; `ls` of
`/usr/share/applications`, `~/.local/share/applications`, `/usr/local/bin`, `/opt`, `~/.local/bin`,
`~/.cargo/bin`; `ls` of `/etc/xdg-terminals.list`, `/usr/share/xdg-terminals.list`;
`cat ~/.config/xdg-terminals.list` and the omarchy default copy; `cat -n` of
`omarchy-default-terminal`; `sed -n` of `omarchy-install-terminal`, `omarchy-launch-screensaver`,
`omarchy-font-set`, `~/.config/hypr/bindings.conf`, `~/.config/hypr/input.conf` (grep); `grep -rn` of
`~/.local/share/omarchy` for `kitty`; `grep -rn` of `~/.config/autostart ~/.config/systemd
~/.config/uwsm`; `pgrep -a kitty`; `pgrep -x kitty|alacritty|foot|ghostty`; `ps -eo pid,comm,args`
(filtered) and `ps -e --no-headers | wc -l`; `~/.local/share/omarchy/bin/omarchy-default-terminal`;
`git -C ~/.local/share/omarchy log/branch/for-each-ref/rev-parse/describe/show` (read-only);
`cat ~/.config/omarchy/current/theme.name`. No file outside this report was written.

Correction round (after the peer flag): `ls -la --time-style=full-iso` on
`~/.config/{kitty,foot,ghostty,alacritty}/`; `sha256sum` of each of the four backups against its
omarchy default; `diff -q`/`diff -u` of each backup vs default and of each live file vs its own
backup; `grep -n -E 'kitty|\.config/kitty'` and `grep -n -E 'bak\.|%Y%m%d-%H%M%S'` on the two
research scripts found by the fleet sweep. Also recorded as a process failure: the earlier truncating
probe `ls -la ~/.config/<t> | sed -n '2,4p'` in a `for t in foot ghostty kitty` loop hid each
directory's `.bak` entry and produced the wrong comparative claim; all comparative listing claims in
this report now come from un-truncated `ls`.
