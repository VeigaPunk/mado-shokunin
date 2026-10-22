# HostGhostty — C2 host inventory for the ghostty config tree (wave 1, read-only)

Verdict: **the ghostty tree exists but is not consumed by anything on this host now.** No `ghostty`
binary, package, flatpak, desktop entry, or process exists; the only launch route
(`Super+Return → xdg-terminal-exec`) resolves to `Alacritty.desktop`; the tree is an unmodified
omarchy 3.8.3 default plus one changed `font-size` value. It is a *declaration*, not a live
consumer. Every probe was read-only; nothing on the host changed. C2 host-side evidence for the
ghostty route row is recorded in §2, §5 and §7.

## 1. Tree inventory (`~/.config/ghostty/`)

```
$ ls -la ~/.config/ghostty/
drwxr-xr-x 1 vgpnk vgpnk   64 Oct  3 19:02 .
drwxr-xr-x 1 vgpnk vgpnk 1692 Oct 22 04:55 ..
-rw-r--r-- 1 vgpnk vgpnk 1325 Oct  3 19:02 config
-rw-r--r-- 1 vgpnk vgpnk 1322 Oct  3 19:02 config.bak.20261003-190229
```

Two regular files, no subdirectories, no symlinks, 2647 bytes total (`du -sb`). Both are
`ASCII text`, mode `-rw-r--r--`, owner `vgpnk`.

| size (B) | sha256 | path |
|---|---|---|
| 1325 | `cb828c044b07d4fd924fe1d6b55c956035feb16f8d5c67899c8a598994596667` | `~/.config/ghostty/config` |
| 1322 | `e47630125605cb19c6b2c9bc33d767a0f3f1b5bf04cd4f36a2bb910897e24f78` | `~/.config/ghostty/config.bak.20261003-190229` |

Timestamps (stat): both files carry **identical** `mtime` and `ctime` `2026-10-03 19:02:29.840995595
-0300`; the directory `mtime` is `2026-10-03 19:02`. Mount is btrfs `@home` with `noatime`, so atime
is only meaningful when explicitly set (see §6). Inodes differ (`config` 21214, bak 38433), and both
sit under directory inode 21213 — a copy made in one operation, not two independently written files.

Content shape (no values printed; contract bounds):
- 41 lines each, 11 comment lines, 23 effective directives.
- First non-comment line shape (both files, and the omarchy default): `key=<config-file>
  has_value=yes value_len=47 value_quoted=no`. Resolved target `~/.config/omarchy/current/theme/ghostty.conf`
  **exists** (454 B, `2026-10-03 17:49`). The literal value is quoted-from omarchy's tracked default
  `~/.local/share/omarchy/config/ghostty/config:2`, not from a host edit.
- Directive key inventory (names only, live file): `config-file`, `font-family`, `font-style`,
  `font-size`, `window-theme`, `window-padding-x`, `window-padding-y`, `confirm-close-surface`,
  `gtk-toolbar-style`, `mouse-scroll-multiplier`, `resize-overlay`, `shell-integration-features`,
  `cursor-style`, `cursor-style-blink`, `async-backend`, and `keybind` ×8.
- `#` comments are sparse (11 lines); the live and default files have the same comment lines, so the
  comments themselves carry no host-local annotation.
- No `themes/` directory, no `~/.cache/ghostty`, no `~/.local/state/ghostty`, no
  `~/.local/share/ghostty` — i.e. no trace that ghostty ever ran and wrote state on this host.

## 2. Binary / package / supply state — all negative

| probe | command | result |
|---|---|---|
| PATH lookup | `command -v ghostty` | rc=1, no output |
| shell builtin | `type -a ghostty` | `type: ghostty not found`, rc=1 |
| PATH walk | every `$PATH` entry tested for `$d/ghostty` | none found |
| pacman query | `pacman -Q ghostty` | `error: package 'ghostty' was not found`, rc=1 |
| pacman search (installed) | `pacman -Qs ghostty` | empty |
| pacman file owner | `pacman -Qo /usr/share/terminfo/g/ghostty` | `/usr/share/terminfo/g/ghostty is owned by ncurses 6.6-2` — the only ghostty-named file anywhere, shipped by ncurses, **not** a ghostty install |
| binary dirs | `/usr/bin /usr/local/bin /opt ~/.local/bin ~/.local/opt /var/lib/flatpak/exports/bin ~/.local/share/flatpak/exports/bin /snap/bin` grepped for `ghostty` | no entries |
| filesystem sweep | `find /usr /opt /snap /var/lib -maxdepth 5 -name 'ghostty*'` | only `/usr/share/terminfo/g/ghostty` |
| package cache | `ls /var/cache/pacman/pkg | grep -i ghostty` | none — no evidence it was ever installed then removed |
| flatpak | `flatpak list` | flatpak **not installed**; `/var/lib/flatpak` absent; `~/.local/share/flatpak/` holds only `db/` (no `app/`, no `runtime/`) |
| desktop entry | `ls ~/.local/share/applications/*ghostty* /usr/share/applications/*ghostty*` | none; `grep -rl -i ghostty` over both application dirs → no match |

No binary exists, so the assignment's `pacman -Qo` on a found ghostty binary is **not applicable**;
it was substituted with `pacman -Qo` on the one ghostty-named file on disk (terminfo, above).

## 3. Process state — nothing is running ghostty

```
$ pgrep -a ghostty     # rc=1, no output
$ pgrep -x ghostty     # rc=1, no output
$ pgrep -af ghostty    # no output
$ ps aux | grep -i ghostty | grep -v grep   # no output
$ lsof +D ~/.config/ghostty ; fuser -v ~/.config/ghostty/config   # rc=1 / rc=1, no holders
```

Live compositor cross-check (Hyprland 0.56.2 is running):

```
$ hyprctl -j clients
client_count=2
classes= {'Alacritty': 2}
ghostty_windows= 0
```

Both existing windows are Alacritty. Nothing holds the ghostty config open.

## 4. Omarchy-default comparison — the tree *is* the omarchy default, plus one font-size edit

```
sha256  1325  cb828c044b07d4fd924fe1d6b55c956035feb16f8d5c67899c8a598994596667  ~/.config/ghostty/config
sha256  1322  e47630125605cb19c6b2c9bc33d767a0f3f1b5bf04cd4f36a2bb910897e24f78  ~/.config/ghostty/config.bak.20261003-190229
sha256  1322  e47630125605cb19c6b2c9bc33d767a0f3f1b5bf04cd4f36a2bb910897e24f78  ~/.local/share/omarchy/config/ghostty/config
```

- The **backup is byte-identical** to the omarchy-shipped default (`cmp -s` → identical,
  `BAK_BYTE_IDENTICAL_TO_OMARCHY_DEFAULT`).
- `diff` of the live config against the omarchy default **with values masked** is empty → same lines,
  same order, same comments. A structural comparison of the 23 key/value pairs shows **exactly one
  differing value**: `font-size` (live value length 4, default length 1; the +3 bytes explain
  1325 − 1322). No other value, key, keybind or comment differs.
- omarchy checkout: version file `3.8.3`, git HEAD `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`
  (`2026-07-20`, merge `master` into `rc`); `git -C ~/.local/share/omarchy status --porcelain -- config/ghostty`
  is clean and `config/ghostty/config` is tracked — the default in the checkout is unmodified.
- `~/.local/share/omarchy/config/ghostty/` is a *directory of files*, not a symlink farm; the host
  copy at `~/.config/ghostty/` is a real copy (distinct inode), matching how omarchy migration
  `1758051607.sh` seeds it: `cp -Rpf $OMARCHY_PATH/config/ghostty/config ~/.config/ghostty/config`
  with the guard `[[ ! -f ~/.config/ghostty/config ]]`.
- So the tree is provenance-clean omarchy default material except one `font-size` value. `[INFERENCE]`
  the `.bak.20261003-190229` name, the nanosecond-identical `mtime`/`ctime` on both files, and the
  single-value delta say one scripted operation on 2026-10-03 19:02:29 saved the pristine default and
  wrote the edited config. No shell history records it (`~/.bash_history` has 0 matches for
  `config.bak.20261003-190229` and 0 lines mentioning ghostty; no `~/.zsh_history`, no fish history).

## 5. Omarchy references to ghostty — documentation and option wiring, not consumption

`grep -rn ghostty` over `~/.local/share/omarchy/{bin,install,default,config,applications,themes}` +
`boot.sh` + `install.sh` (and separately `migrations/`):

| location | what it does | consumes the tree now? |
|---|---|---|
| `bin/omarchy-default-terminal` | accepts `alacritty\|foot\|ghostty\|kitty`, writes `~/.config/xdg-terminals.list` (`com.mitchellh.ghostty.desktop`) | no — see §5.1; host list names Alacritty only |
| `bin/omarchy-install-terminal` | `omarchy-pkg-add ghostty`, then seeds `~/.config/ghostty` only `if [[ ! -e ~/.config/$package ]]` | no — install path only, requires sudo, never run for ghostty |
| `bin/omarchy-restart-terminal` | `if pgrep -x ghostty; then killall -SIGUSR2 ghostty; fi` | no — guard never true |
| `bin/omarchy-font-set` | `if [[ -f ~/.config/ghostty/config ]]; then sed -i 's/font-family = .../' ; pkill -SIGUSR2 ghostty` | **the only writer that would touch the tree on a font change** — but it edits `font-family`, and the one host delta is `font-size`; it also signals the process, which does not exist |
| `bin/omarchy-launch-screensaver` | `*ghostty*) hyprctl dispatch exec ghostty --class=org.omarchy.screensaver --config-file=…/default/ghostty/screensaver …` | no — branch only fires when the active terminal is ghostty |
| `bin/omarchy-menu` | `omarchy-cmd-present ghostty && …` builds the terminal menu entry from `command -v` | no — `omarchy-cmd-present` is `command -v`, which fails |
| `default/hypr/apps/terminals.conf` | `windowrule = tag +terminal, match:class (Alacritty\|kitty\|com.mitchellh.ghostty\|foot)` | passive rule, needs a window |
| `default/hypr/input.conf:45` | `windowrule = match:class com.mitchellh.ghostty, scroll_touchpad 0.2` | passive rule — also present live at `~/.config/hypr/input.conf:46` |
| `default/themed/ghostty.conf.tpl` (601 B) | theme template consumed by the theme pipeline | renders `~/.config/omarchy/current/theme/ghostty.conf`; the terminal never reads it |
| `migrations/*.sh` (12 files) | seed the config, add keybinds, `async-backend`, `mouse-scroll-multiplier`; two also patch `hypr/input.conf` windowrules | already applied historically; omarchy migrations are not a live consumer |
| `install/omarchy-base.packages`, `install/omarchy-other.packages` | `grep -i ghostty` → no match | ghostty is not in either package list |
| `default/omarchy-skill/SKILL.md` | lists `~/.config/ghostty/` as an editable terminal config | documentation |

### 5.1 The one live launch route resolves away from ghostty

- `~/.config/hypr/bindings.conf:2` → `bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`
- `~/.config/xdg-terminals.list` (127 B, `2026-10-03 17:44`) contains exactly one non-comment entry:
  `Alacritty.desktop`.
- Therefore `Super+Return` → `xdg-terminal-exec` → Alacritty. Ghostty is absent from the preference
  order, has no `com.mitchellh.ghostty.desktop` to resolve to, and no binary for that entry to point at.
- `~/.config/hypr/input.conf:46` carries the ghostty `scroll_touchpad 0.2` windowrule left by migration
  `1762770442.sh`/`1767138576.sh`; it is inert without a ghostty window.

Whole-config sweep: `grep -rIl -i ghostty ~/.config --exclude-dir=ghostty` returns only
`~/.config/hypr/input.conf` (the windowrule) and one unrelated Chromium extension ruleset
(`.../ruleset_208.json`, a filter substring). No shell rc, systemd user unit, autostart entry,
nautilus extension (`~/.local/share/nautilus-python/extensions/` holds only `localsend.py`,
`transcode.py`), or `systemctl --user list-units` row mentions ghostty.

## 6. One anomaly worth recording, not a consumer

The `stat` atime on `~/.config/ghostty/config` is `2026-10-19 17:35:18.345658692`. The mount is
`noatime`, so ordinary reads cannot set it. A sweep shows the same second is shared by large batches
elsewhere: `~/.config/chromium/**` (atimes `17:35:18.157`–`.295`) and **the entire**
`~/.local/share/omarchy/config` and `default` trees at one identical stamp `17:35:18.679659189`
(including omarchy's own `ghostty`, `kitty`, `foot`, `alacritty` defaults). `~/.config/foot/foot.ini`
and `~/.config/kitty/kitty.conf` share ghostty's exact `.345658692` stamp. `[INFERENCE]` a bulk
copy/restore at 2026-10-19 17:35:18 stamped a wide slice of `~/.config` and the omarchy checkout;
it is not ghostty-specific and it did not modify content (all content hashes/`git status` above are
consistent with 2026-10-03 material). `[UNK]` which tool ran it — no ghostty consumer is implied.

## 7. What this means for C2 (routed to the planner, not a decision)

- The counter `python3 -I .ufo/waves/round-23/c2/count.py REV` requires, per terminal, a row in
  `corpus/knowledge/terminal-trees-r23.md` whose first cell is the terminal name and which cites an
  `S###` token that is `mined`, `opened == 2026-10-22`, and whose **source cell names that terminal**.
- At `a28e4815`: `corpus/knowledge/terminal-trees-r23.md` **does not exist**; `corpus/SOURCES.md` has
  122 `S###` rows and **none** names ghostty, kitty or foot (`grep -niE 'ghostty|kitty|foot'` → no match).
  So the ghostty route row needs a *new* mined SOURCES row opened today whose source cell says
  "ghostty" — host bytes alone cannot satisfy the counter.
- Host-side facts available for that row, all with receipts above: tree exists with 2 files and the
  hashes in §1; the tree is omarchy 3.8.3 default + one `font-size` value; **zero** consumer routes
  (§2, §3, §5.1); colours live outside the tree in the theme plane
  (`~/.config/omarchy/current/theme/ghostty.conf`, 454 B) reached through the `config-file` directive —
  the same cross-terminal invariant already recorded for the theme plane in
  `corpus/knowledge/terminals-and-omarchy.md` §4 and `corpus/README.md:14`.
- Prior corpus statement this confirms rather than contradicts: `corpus/README.md:14` records "only
  Alacritty installed of alacritty/foot/kitty/ghostty (`command -v` sweep §1)" and
  `corpus/README.md:65` calls the other configs "declarations, not tested consumers". The ghostty
  half of that claim holds again today, on newer evidence.

## 8. Observed / inference / unknown

**Observed:** every path, hash, size, mode, timestamp, rc code and command output quoted above;
`ghostty` absent from PATH, pacman, flatpak, desktop entries and all processes; `hyprctl -j clients`
shows 2 Alacritty windows and 0 ghostty; backup byte-identical to the omarchy default; exactly one
differing value (`font-size`) versus that default; `xdg-terminals.list` names only `Alacritty.desktop`;
`terminal-trees-r23.md` absent; 0/122 SOURCES rows name ghostty/kitty/foot.

**Inference (`[INFERENCE]`):** the single scripted 2026-10-03 19:02:29 operation that saved the
pristine default as `.bak.20261003-190229` and changed one `font-size` value; the 2026-10-19
17:35:18 atime batch being a bulk copy/restore rather than terminal activity; that omarchy's
`omarchy-font-set` is the writer that would touch this tree next if a font were changed while ghostty
is installed (it edits `font-family`, which the host has not changed).

**Unknown (`[UNK]`):** which tool produced the 2026-10-19 atime batch (bash history is empty of
relevant commands, no zsh/fish history exists); whether the `font-size` edit was made by hand or by a
tool (no record survives); whether ghostty was ever installed on this host before the current
filesystem state — no package-cache tarball, no state/cache dir, and no pacman log evidence was found
for it in this pass.

## 9. Commands run (all read-only)

`ls -la ~/.config/ghostty/`; `find ~/.config/ghostty -mindepth 1`; `stat -c …`, `sha256sum`, `wc -l/-c`,
`cmp -s`, `file`, `du -sb`, `getfattr -d`; a value-masked `diff` and a 23-pair key/value comparison via
`python3 -` over the two files and `~/.local/share/omarchy/config/ghostty/config`; `command -v ghostty`;
`type -a ghostty`; a `$PATH` walk; `pacman -Q ghostty`; `pacman -Qs ghostty`; `pacman -Qo
/usr/share/terminfo/g/ghostty`; `ls /var/cache/pacman/pkg | grep -i ghostty`; `flatpak list`;
`find /usr /opt /snap /var/lib -maxdepth 5 -name 'ghostty*'`; `grep -rl -i ghostty` over
`~/.local/share/applications` and `/usr/share/applications`; `pgrep -a/-x/-af ghostty`;
`ps aux | grep -i ghostty`; `lsof +D`, `fuser -v`; `hyprctl -j clients`, `hyprctl version`;
`grep -rn`/`grep -rIl -i ghostty` over `~/.config`, `~/.local/share/omarchy/{bin,install,config,default,
applications,themes,migrations}`, shell rc files; `git -C ~/.local/share/omarchy status/ls-files/log`
(read-only); `cat ~/.local/share/omarchy/version`; masked `grep` of `~/.bash_history`; `find -newerat`
plus a `stat` sweep for the atime batch; `findmnt -no OPTIONS -T ~/.config/ghostty`;
`sed -n` reads of `omarchy-cmd-present`, `omarchy-cmd-terminal-cwd`, `omarchy-install-terminal`,
`omarchy-restart-terminal`, `omarchy-theme-set`; `ls corpus/knowledge/`, `sed -n '1,12p' corpus/SOURCES.md`,
`grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` in the lane.

**Host safety:** no writes outside this report, no package transactions (only `pacman -Q`, `-Qs`,
`-Qo` reads), no installs (nothing was needed), no compositor/systemd/service changes, no jj at the
fleet root, no git write commands anywhere, no agent dispatch. Content beyond the first non-comment
line shape was not printed; the one edited value is reported only by key name and length, and the
literal value is withheld.

**Confidence:** high on every §1–§5 fact (direct tool output, quoted); medium on the §6 `[INFERENCE]`
about the atime batch and the 2026-10-03 operation; the §2/§3/§5 negatives are exhaustive within the
probes listed and would only be overturned by an install after 2026-10-22 08:00 -0300.
