# HostFoot — read-only host inventory of the foot config tree (C2 evidence)

Seat: MadoR23.HostFoot (scout, leaf). Date 2026-10-22. Host unchanged: read-only probes only, no
`pacman` transaction (pacman guard respected), no write outside this file. No installs or upgrades
were made or needed. Lane untouched (read-only `ls`/`grep` of corpus files only).

LSP note: this assignment is host inventory, not repository source semantics, so no language server
applies. Every fact below is a direct filesystem/process observation produced by the command shown.
The text greps are inventory greps over config/scripts, not semantic proof of code behaviour; where a
behaviour claim is made about an omarchy script it rests on the script body read at
`~/.local/share/omarchy/bin/`, cited per item.

## 1. The tree: `ls -la ~/.config/foot/`

```
total 8
drwxr-xr-x 1 vgpnk vgpnk   72 Oct  3 19:02 .
drwxr-xr-x 1 vgpnk vgpnk 1692 Oct 22 04:55 ..
-rw-r--r-- 1 vgpnk vgpnk  516 Oct  3 19:02 foot.ini
-rw-r--r-- 1 vgpnk vgpnk  513 Oct  3 19:02 foot.ini.bak.20261003-190229
```

Two regular files, no subdirectories, no `*.diff`, no `themes/`. `find ~/.config/foot -maxdepth 3
-printf '%y %s %p\n'`:

```
d 72 /home/vgpnk/.config/foot
f 516 /home/vgpnk/.config/foot/foot.ini
f 513 /home/vgpnk/.config/foot/foot.ini.bak.20261003-190229
```

`~/.config/foot` is a real directory, not a symlink (`readlink -f` resolves to itself;
`stat -c '%F'` → `directory`).

`stat -c '%n size=%s mode=%A mtime=%y ctime=%z inode=%i'`:

| path | bytes | mode | mtime / ctime | inode |
|---|---|---|---|---|
| `~/.config/foot` | 72 (dir) | `drwxr-xr-x` | `2026-10-03 19:02:29.839995618 -0300` (both) | 21211 |
| `~/.config/foot/foot.ini` | 516 | `-rw-r--r--` | `2026-10-03 19:02:29.839995618 -0300` (both) | 21212 |
| `~/.config/foot/foot.ini.bak.20261003-190229` | 513 | `-rw-r--r--` | `2026-10-03 19:02:29.839995618 -0300` (both) | 38431 |
| `~/.local/share/omarchy/config/foot/foot.ini` (reference default) | 513 | `-rw-r--r--` | mtime `2026-10-03 17:42:32.292614772`, ctime `17:42:36.944650266` | 691 |
| `~/.local/share/omarchy/default/foot/foot.desktop` (reference) | 437 | `-rw-r--r--` | `2026-10-03 17:42:32.299121170` | 794 |
| `~/.local/share/omarchy/default/foot/screensaver.ini` (reference) | 103 | `-rw-r--r--` | `2026-10-03 17:42:32.299289869` | 795 |

Both user files share mtime and ctime to the nanosecond — one write pass at 19:02:29.839995618.

## 2. Sizes and SHA256 (exact command + output)

Command: `sha256sum ~/.config/foot/foot.ini ~/.config/foot/foot.ini.bak.20261003-190229 ~/.local/share/omarchy/config/foot/foot.ini`

```
3e88354476f2682e7a1a0bc840d04e221e5c6a7312b3ee9dcf76ec16d0842e60  /home/vgpnk/.config/foot/foot.ini
8afc9646c61e58e67f244e50a9ce5d4a45546920511a06b47f7443a3998da602  /home/vgpnk/.config/foot/foot.ini.bak.20261003-190229
8afc9646c61e58e67f244e50a9ce5d4a45546920511a06b47f7443a3998da602  /home/vgpnk/.local/share/omarchy/config/foot/foot.ini
```

- live `foot.ini`: **516 B**, sha256 `3e88354476f2682e7a1a0bc840d04e221e5c6a7312b3ee9dcf76ec16d0842e60`
- `foot.ini.bak.20261003-190229`: **513 B**, sha256 `8afc9646c61e58e67f244e50a9ce5d4a45546920511a06b47f7443a3998da602`
- omarchy-shipped default `~/.local/share/omarchy/config/foot/foot.ini`: **513 B**, same
  `8afc9646…` hash — the backup is byte-identical to the shipped default.

## 3. Content shape only (no bodies printed; nothing secret-shaped)

Command: `awk 'NF && $1 !~ /^#/ {print NR": "$0; exit}' <file>` and `grep -n '^\[' <file>`

- First non-comment, non-empty line of all three files is identical: `1: [main]`.
- All three: 25 lines (`wc -l`), 19 non-comment lines
  (`grep -cE '^[[:space:]]*[^#[:space:]]'`).
- Section headers, identical in all three: `[main]` (1), `[scrollback]` (9), `[cursor]` (12),
  `[key-bindings]` (16), `[text-bindings]` (21).
- Secret-shaped key scan over both user files
  (`grep -oiE '^[[:space:]]*[a-z0-9_-]*(pass|token|secret|key|api|auth)[a-z0-9_-]*[[:space:]]*='`):
  **none**.
- The live file's `[main]` block carries an `include=` directive pointing at a theme fragment under
  `~/.config/omarchy/current/theme/` (line value not printed; that target directory holds
  `foot.ini`, 378 B, mtime 2026-10-03 17:49, and `theme.name` = `matte-black`).
- The two `[text-bindings]` entries the round-22-era omarchy migration expects are present:
  `grep -c '13;2u=Shift+Return'` → 1, `grep -c '13;4u=Mod1+Shift+Return'` → 1 (one each).

## 4. Does the tree match an omarchy default?

Command: `diff -u ~/.local/share/omarchy/config/foot/foot.ini ~/.config/foot/foot.ini`
(plus `cmp -s` on the pairs)

- `foot.ini.bak.20261003-190229` vs the omarchy-shipped default: **byte-identical**, `cmp` rc=0,
  matching SHA256 `8afc9646…`. The backup *is* the unmodified omarchy default (the file as installed
  at 17:42:32; note the live default at `~/.local/share/omarchy/config/foot/foot.ini` was not
  modified afterwards — same hash now).
- `foot.ini` vs the omarchy-shipped default: exactly **one changed line** (`diff | grep -c '^[<>]'`
  → 2, i.e. one `<`/`>` pair), inside hunk `@@ -1,7 +1,7 @@`, in the `[main]` block, the `font=`
  preference (values not printed; 516 vs 513 B = one value 3 bytes longer). This is the same
  single-line font delta the corpus already recorded for this tree
  (`corpus/knowledge/terminals-and-omarchy.md` §6 / R2-E2: one `NcN` hunk per terminal file).
- Net: the live tree is the omarchy default plus **one local font preference**, plus a stale
  timestamped backup of the pristine default. No other local divergence.

## 5. Does the foot binary exist? (all install channels checked)

| probe | command | output |
|---|---|---|
| PATH | `command -v foot` | (empty), rc=1 |
| PATH sweep | `for d in $(printf '%s' "$PATH" \| tr ':' ' '); do [ -e "$d/foot" ] && ls -la "$d/foot"; done` | no hits across all 17 PATH dirs (one of them `~/.local/share/omarchy/bin`) |
| pacman | `pacman -Q foot` | `error: package 'foot' was not found` |
| pacman (any foot package) | `pacman -Qq \| grep -i foot` | empty; `pacman -Qm \| grep -i foot` (foreign) also empty |
| flatpak | `command -v flatpak` | `error: command not found: flatpak` |
| snap / nix / appimage-run | `command -v snap nix appimage-run` | none found, rc=1 |
| fixed dirs | `ls -la /usr/bin/foot /usr/local/bin/foot ~/.local/bin/foot /usr/bin/footclient` | all `No such file or directory` |
| desktop entries | `ls /usr/share/applications/*foot* ~/.local/share/applications/*foot*` | no `foot.desktop` anywhere; only `~/.local/share/applications/foot-server.desktop` and `footclient.desktop` |
| stub content | `cat` of both stubs | 28 B each, exactly `[Desktop Entry]` + `Hidden=true` — hidden stubs, not launchers |
| stub provenance | `ls -la ~/.local/share/omarchy/applications/hidden/ \| grep -i foot` | `foot-server.desktop` + `footclient.desktop`, 28 B, 2026-10-03 17:42 — omarchy plants these via `omarchy-refresh-applications` (`cp ~/.local/share/omarchy/applications/hidden/*.desktop ~/.local/share/applications/`) |
| stub ownership | `pacman -Qo` on both stubs | `error: No package owns …` (leftovers, not package-owned) |

`pacman -Qo` on a found binary: **not applicable** — no foot binary exists on this host to query
ownership for. Contrast, the terminal that *is* installed: `alacritty 0.17.0-1` (`/usr/bin/alacritty`)
and `xdg-terminal-exec 0.14.3-2` (owns `/usr/bin/xdg-terminal-exec`).

## 6. Is any running process using it?

```
pgrep -a foot            -> no output, rc=1
pgrep -x foot            -> no output, rc=1
pgrep -x footclient      -> no output, rc=1
pgrep -f foot            -> no output, rc=1
ps -eo pid,comm,args | grep -Ei 'foot'   -> no match (grep rc=1)
ps -e --no-headers | wc -l               -> 3177 processes visible
pgrep -x alacritty       -> 2487  (alacritty --working-directory=/home/vgpnk)
```

The negative is over a 3177-process table, not a truncated one. Open-handle probes agree:
`lsof +D ~/.config/foot` → rc=1 (no open files); `fuser -v` on both files → rc=1 (no users).
No runtime or cache artefacts: `ls /run/user/1000/foot*` → absent; `ls ~/.cache/foot` → absent
(foot would keep a client/server socket there when running). No autostart/systemd reference:
`grep -rIl -i foot ~/.config/autostart ~/.config/systemd/user` → none.

## 7. Routing: would anything start foot right now?

- `~/.config/xdg-terminals.list` contains exactly the two comment lines plus `Alacritty.desktop`
  (127 B, sha256 `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b`) and is
  byte-identical (`cmp` rc=0) to the omarchy-shipped
  `~/.local/share/omarchy/config/xdg-terminals.list`. foot is **not** in the preference order.
- No system fallback list exists: `/etc/xdg/xdg-terminals.list` and `/usr/share/xdg-terminals.list`
  both absent (`ls` → `No such file or directory`), so `xdg-terminal-exec`'s
  `${XDG_CONFIG_DIRS:-/etc/xdg}` search adds nothing.
- `~/.local/share/omarchy/bin/omarchy-default-terminal` (read in full) derives the current answer
  from that same list: `Alacritty.desktop → alacritty`, `foot.desktop → foot`; the list names
  Alacritty, so the resolver answers `alacritty`. `foot.desktop` does not exist in any applications
  dir anyway (only the two `Hidden=true` stubs).
- The launch path is terminal-agnostic: `~/.config/hypr/bindings.conf:2` binds
  `SUPER, RETURN → uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`; the running
  terminal is `alacritty` (pid 2487).
- Screensaver route: `omarchy-launch-screensaver` computes `terminal=$(xdg-terminal-exec --print-id)`
  and its `*foot*` branch (`foot --app-id=org.omarchy.screensaver --config="$OMARCHY_PATH/default/foot/screensaver.ini"`)
  is only taken when that id is foot; with the current list it takes `*Alacritty*`. The foot
  screensaver config (`default/foot/screensaver.ini`, 103 B) is present but unreachable today.
- Hyprland rules that name foot are inert string matches, not routes:
  `~/.config/hypr/input.conf:45` and `~/.local/share/omarchy/config/hypr/input.conf:44`
  (`windowrule = match:class (Alacritty|kitty|foot), scroll_touchpad 1.5`),
  `~/.local/share/omarchy/default/hypr/apps/terminals.conf:2` (tag `terminal` for the same class
  list). No foot window class can exist without the binary.
- A broad config-plane sweep (`grep -rIl -i foot ~/.config`, excluding the tree itself) found no
  reader of `~/.config/foot/` — only substring noise (Typora/Chromium dictionaries, CSS
  `footer`/`tfoot`) and the hypr class-string rules above.

## 8. Latent (conditional) consumers — present in code, not active on this host

Each requires the binary or an explicit user action, so none consumes the tree today:

| consumer | file:line | gate |
|---|---|---|
| font setter rewrites the `font=` line of `~/.config/foot/foot.ini` (to `:size=9`) | `~/.local/share/omarchy/bin/omarchy-font-set:25-26` | only if `~/.config/foot/foot.ini` exists — it does, so `omarchy font set <name>` **would** rewrite this file (and then notify only if `pgrep -x foot`, line 44-45) |
| text-binding migration appends `[text-bindings]` entries | `~/.local/share/omarchy/migrations/1783833508.sh:39-52` | greps `^\[text-bindings\]$` and both literal bindings — both already present (1/1 each), so it would no-op |
| theme applier pushes colours to running foot via OSC escapes | `~/.local/share/omarchy/bin/omarchy-theme-set-foot` (called by `omarchy-theme-set:65`) | exits 0 unless the theme file exists **and** `pgrep -x foot` — false today |
| default-terminal switcher writes `foot.desktop` into the list | `~/.local/share/omarchy/bin/omarchy-default-terminal:21,29-34` | explicit `omarchy default terminal foot` |
| installer | `~/.local/share/omarchy/bin/omarchy-install-terminal:17,34-36` (`omarchy-pkg-add foot`, copies `default/foot/foot.desktop`) | explicit; needs sudo and pacman transactions are paused host-wide |
| menu entries | `~/.local/share/omarchy/bin/omarchy-menu:404,411,418,555-557` | switch entry gated by `omarchy-cmd-present foot` → false today; the *install* entry is always listed |
| screensaver | `~/.local/share/omarchy/bin/omarchy-launch-screensaver:40-45` | only when `xdg-terminal-exec --print-id` is foot (it is Alacritty) |
| omarchy skill docs name the tree | `~/.local/share/omarchy/default/omarchy-skill/SKILL.md:6,81,167` | documentation, not a consumer |

## 9. Provenance of the tree (observed)

- The tree is omarchy-planted, not user-installed: the shipped default landed at 17:42:32 with the
  omarchy checkout (`~/.local/share/omarchy` is a git checkout, HEAD
  `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` 2026-07-20 on `master`, `git describe` `v3.8.4`,
  `version` file `3.8.3` — the same version discrepancy the kitty seat recorded).
- The 19:02:29.839995618 pass touched this tree in the same instant as the other three terminal
  trees' backups: `ls -la --time-style=full-iso` shows
  `alacritty.toml.bak.20261003-190229` (873 B, `.838995642`),
  `kitty.conf.bak.20261003-190229` (953 B, `.839995618`),
  `foot.ini.bak.20261003-190229` (513 B, `.839995618`),
  `ghostty/config.bak.20261003-190229` (1322 B, `.840995595`) — **all four trees kept a `.bak`** in
  one batch pass, not only kitty. (Cross-report note: `HostKitty.md` originally stated "Only kitty
  kept a `.bak`; foot and ghostty did not"; that wording now survives only inside the seat's own
  retraction note (its lines 181-182), and its corrected §8 carries the four-backup table — closed
  2026-10-22.) [INFERENCE] This is one batch font-enlargement pass across the
  four planted terminal trees; the diff evidence (one font line each) is consistent, but the pass
  itself was not observed.
- Writer of the `.bak` files is **not attributed**: the suffix form `YYYYMMDD-HHMMSS` is produced by
  no omarchy script in the installed checkout (`grep -rIn -E '\+%Y%m%d|bak\.[0-9]{8}-' ~/.local/share/omarchy`
  finds only `/etc/fstab.$(date +%Y%m%d%H%M%S).back` in `omarchy-hibernation-{setup,remove}`,
  a different shape; `omarchy-refresh-config:23` uses epoch seconds), and
  `git -C ~/.local/share/omarchy log --all -S '%Y%m%d-%H%M%S'` is empty. Unresolved.
- Corroboration (HostKitty seat, un-truncated re-measure 2026-10-22, same host): the four `.bak`
  files' parent-dir mtimes stagger by ~1 ms in order alacritty (`.838995642`) → kitty/foot
  (`.839995618`) → ghostty (`.840995595`), i.e. one sequential loop over the four trees; and a
  fleet-wide sweep found the `YYYYMMDD-HHMMSS` suffix form only in model-routing scripts, none
  touching terminal configs. The writer of all four backups is host-side and unidentified; the form
  is shared across all four, so it treated the trees uniformly.

## 10. Verdict

**The `~/.config/foot/` tree is not consumed by anything on this host now.** It is a dormant,
omarchy-planted alternative-terminal config: no foot binary on any channel (PATH sweep over 17
dirs, `pacman -Q` not found, no foot package in the DB or foreign set, no flatpak/snap/nix at all,
no fixed-dir binary), no launcher entry (only two 28 B `Hidden=true` stubs; no `foot.desktop`), no
running process (3177-process table, `pgrep`/`ps`/`lsof`/`fuser` all negative), no runtime socket or
cache dir, no autostart/systemd reference, and foot absent from the `xdg-terminals.list` preference
order (which names only `Alacritty.desktop` and is itself byte-identical to the omarchy default),
with the live terminal being `alacritty` (pid 2487) and the screensaver resolver picking the
Alacritty branch. The only code paths that would touch the tree are explicit user commands
(`omarchy font set`, `omarchy default terminal foot`, `omarchy install terminal foot`) or a
foot-hosted session, none of which is active. Its entire distinguishing local content is one font
preference (516 B vs the 513 B default, one changed line); the pristine default is preserved
byte-exact as `foot.ini.bak.20261003-190229` (`8afc9646…`).

## 11. What this means for C2 (foot route rows)

- Host-side facts available for a route row: the tree exists as 2 files / 1 live config; the live
  file is the omarchy default plus one `font=` preference; the pristine default is preserved as the
  timestamped backup; the effective config includes the theme fragment
  `~/.config/omarchy/current/theme/foot.ini` (theme `matte-black`); and the tree is
  **carried-but-unconsumed** on this host (no binary, no route, no process).
- A route row claiming the host *uses* foot would be false. A row claiming the host *carries* the
  tree, which omarchy commands rewrite it (`omarchy-font-set:25-26` is the live writer; the
  text-binding migration is a satisfied no-op), and that `xdg-terminals.list` routes elsewhere is
  supported by the bodies and observations above.
- The counter of record (`python3 -I .ufo/waves/round-23/c2/count.py REV`) requires a
  `corpus/knowledge/terminal-trees-r23.md` row citing a `mined` SOURCES row opened 2026-10-22 that
  names foot. At the base tip that note is **absent** (`ls` → `No such file or directory`), and
  `corpus/README.md` frontier lines 123-126 still record the foot/kitty/ghostty trees as unsourced.
  This report is host inventory evidence for such a row, not a SOURCES row itself; the upstream
  foot source (codeberg.org/dnkl/foot) was **not** opened by this seat.

## Unresolved

1. What created the four `.bak.20261003-190229` files (writer unattributed; see §9). Content and
   timestamp are established; the writer is not.
2. omarchy installed revision: `version` file `3.8.3` vs `git describe` `v3.8.4` (same as the kitty
   seat's open item; not resolved here).
3. `xdg-terminal-exec --version` did not return within its probe window and was cancelled; the
   version `0.14.3-2` comes from `pacman -Qo`/`pacman -Q`, not from the tool's own output.
4. (Closed 2026-10-22) `HostKitty.md`'s "only kitty kept a `.bak`" statement contradicted the
   observed four-backup set; the seat retracted it in its own file after being messaged (retraction
   note at its lines 181-182, corrected §8 table with all four hashes). Our reports now agree.

## Commands run (exhaustive, all read-only)

`ls -la ~/.config/foot/`; `stat -c '%F %N'` and `readlink -f` on the tree; `find ~/.config/foot
-maxdepth 3 -printf '%y %s %p\n'`; `stat -c '%n size=%s mode=%A mtime=%y ctime=%z inode=%i'` on the
tree, the omarchy default `config/foot/foot.ini`, `default/foot/foot.desktop`,
`default/foot/screensaver.ini`; `sha256sum` on the three foot.ini variants; `cmp -s` on
live↔default, backup↔default, live↔backup; `diff -u` default↔live (values masked in the report);
`awk`/`grep -n '^\['`/`wc -l`/`grep -cE` for shape and counts; secret-shaped key scan; `grep -c` for
the two migration bindings; `command -v foot`; PATH-directory sweep for `foot` (17 dirs);
`pacman -Q foot`; `pacman -Qq | grep -i foot`; `pacman -Qm | grep -i foot`; `pacman -Q alacritty
xdg-terminal-exec`; `command -v flatpak snap nix appimage-run`; `ls -la /usr/bin/foot
/usr/local/bin/foot ~/.local/bin/foot /usr/bin/footclient`; `ls /usr/share/applications/*foot*
~/.local/share/applications/*foot*`; `cat` of the two 28 B stubs; `ls -la
~/.local/share/omarchy/applications/hidden/`; `pacman -Qo` on the two stubs and on
`/usr/bin/xdg-terminal-exec`; `pgrep -a foot`; `pgrep -x foot|footclient`; `pgrep -f foot`;
`ps -e --no-headers | wc -l`; `ps -eo pid,comm,args | grep -Ei foot`; `lsof +D ~/.config/foot`;
`fuser -v` on both files; `ls` of `/run/user/1000/foot*` and `~/.cache/foot`; `grep -rIl -i foot
~/.config/autostart ~/.config/systemd/user`; `cat ~/.config/xdg-terminals.list`; `sha256sum`/`cmp`
on `~/.config/xdg-terminals.list` vs `~/.local/share/omarchy/config/xdg-terminals.list`; `ls` of
`/etc/xdg/xdg-terminals.list`, `/usr/share/xdg-terminals.list`; `cat` of
`omarchy-default-terminal`, `omarchy-refresh-applications`, `omarchy-theme-set-foot`,
`omarchy-refresh-config` (lines 15-30); `sed -n` of `omarchy-font-set` (20-50),
`omarchy-launch-screensaver` (1-60), `migrations/1783833508.sh` (35-55); `grep -rIn` of
`~/.local/share/omarchy` for foot and for backup timestamp formats; `git -C ~/.local/share/omarchy
log/describe` (read-only) for HEAD/version and `log -S` searches; `cat
~/.config/omarchy/current/theme.name`; `ls -la ~/.config/omarchy/current/theme/foot.ini`;
`grep -rIl`/`grep -rIn -i foot ~/.config` (broad sweep); `ls -la --time-style=full-iso` of the four
terminal `.bak` files; `grep -n` of `corpus/README.md` and `corpus/knowledge/terminals-and-omarchy.md`
for foot lines; `ls` of `corpus/knowledge/terminal-trees-r23.md` and `corpus/SOURCES.md`; read of
`.ufo/waves/round-23/c2/count.py` and `.ufo/waves/round-23/registration.md`; read of
`.ufo/waves/round-23/w1/reports/HostKitty.md` for format. No file outside this report was written.
