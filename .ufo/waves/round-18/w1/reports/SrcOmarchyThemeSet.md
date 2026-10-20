# SrcOmarchyThemeSet — omarchy v3.8.4 `omarchy-theme-set` write/signal map

Seat: MadoR18.SrcOmarchyThemeSet (leaf scout). Round 18, W1.
Question assigned: fetch omarchy v3.8.4 raw `bin/omarchy-theme-set` and the helpers it
calls; record exactly which files/symlinks it writes (`current/theme`, `theme.name`,
`background`) and which apps it signals/restarts, quoted with line anchors. Data only.

Scope discipline: no omarchy binary was executed; no `git`/`jj` command was run in the
host checkout (`~/.local/share/omarchy`); no pacman/systemctl/hyprctl/process probes.
Host facts below are **file bytes read only** (`cat`, `ls -la`, `readlink`, `xxd`,
`sha256sum`). Labels: **OBSERVED** = file/receipt bytes; **INFERENCE** = derived from
source semantics, not executed.

## 1. Identity and receipts (R17-V3)

Tag resolution (`git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'`,
one line only — lightweight tag, no peeled entry):

```
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
```

**OBSERVED**: 22 raw bodies fetched from `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/<name>`,
each HTTP 200, all ≤1 MiB, saved under
`.ufo/waves/round-18/fetch/SrcOmarchyThemeSet/` with one receipt line per fetch in
`receipts.jsonl` (`mado-fetch-receipt-v1`, curl 8.23.0, `fetched_at` 2026-10-20T15:40Z).
`receipts.jsonl` sha256 `0a2b1ae6d1b81f6a2863975856735e24909afc0d86ccc82575ac89d5c8f20646`.

| body | sha256 |
|---|---|
| `omarchy-theme-set` | `79069c8018a7d6d20f52e357b0b473bd99fad0c5f2914523171687103eeb9516` |
| `omarchy-theme-set-templates` | `01264122666b3d49d4e976837db70d9f9962aa6afd1b2531010c8d7c7d0ea9c0` |
| `omarchy-theme-bg-next` | `ee4828127755566d48b46a3775d431601a4d56a9114277ddc78b49c273196c6a` |
| `omarchy-theme-bg-set` | `638f265f3a8e62e4d477499627a8f270049df838f038db4f95837acf29acdc05` |
| `omarchy-theme-refresh` | `597dd7f2f082e41e54d67ad9be4096b05f8acf72d9c311097e5da1ba2e85216b` |
| `omarchy-theme-current` | `2e5c370425b8151fe58ad9147ce4b5cb9c674e0740e3c51bbd432b686298dc93` |
| `omarchy-theme-colors-from-alacritty` | `89afbabbf03ed40003ae58f39ee2774a71280f587d3e5981cba45d0f52bed0de` |
| `omarchy-theme-set-browser` | `e8603251aca49dc2a6d8ecad4ff69f4bd2fd349d08a3506ad81282739a261001` |
| `omarchy-theme-set-foot` | `1b041f97b841a37c66c52f53ac21147ac74f749bd15529125f4107305d4b5314` |
| `omarchy-theme-set-gnome` | `e5c05b6de0287f608ec44fa2380546374a8217d8dd0ebb86c556dc42a5eb8342` |
| `omarchy-theme-set-vscode` | `d0a5032297006e432b407fb44897cd2eef766b373a7a92dd2ce7d179a6fcc366` |
| `omarchy-theme-set-obsidian` | `4af64acf20f20bd0db4e8a744e0a817508c4a28b7f9f5caaa175f79958699fda` |
| `omarchy-theme-set-keyboard` | `e8b2196f8b8e81fe9a97364ab7327e66ce30442ca4914d3430fe799cefef6b41` |
| `omarchy-hook` | `c64ea844feb1849375e7cd43dde98933293b0e0f0f522e1ba2c6572d86386c7b` |
| `omarchy-restart-waybar` | `078684d140c6049bd60e770062cd9887c2d32ac9b1cff8a1f046525806ec487a` |
| `omarchy-restart-terminal` | `3fbf0a2a898bec57662bb544e11d3c2c9194347e1dc9edc24376b94c29690efb` |
| `omarchy-restart-hyprctl` | `fc0484cd85aa4d3a8c84685022f4b33ccfd86cfdf9fa27e0013fc8ca99994d64` |
| `omarchy-restart-btop` | `8acc7c77bcd2ac4e269eef01ac88260871d0c4418ef5a381bb7100f53008fd81` |
| `omarchy-restart-opencode` | `5dd92885ee2a5170397b6bcc67f4ecbdda772cb80236ac1ca80eaf9c74085d41` |
| `omarchy-restart-mako` | `cd64bbb0d659b1cb9223e81898d75e29a82a5c101bdc79f9368fdacc262b5ef9` |
| `omarchy-restart-helix` | `3834a1bb91d6443514e0981b773d4517c519d925873ebebcb9f6adc6a07794cd` |
| `omarchy-restart-swayosd` | `da17ec6f78987ad01ab1766f49eead39452dc3ce1a7369b30a2ca696486d5fc3` |

## 2. Host checkout ↔ tag (OBSERVED, .git read as bytes; no git command)

- `.git/packed-refs:2` → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/heads/master`
- `.git/packed-refs:508` → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/tags/v3.8.4`
- `.git/packed-refs:321` → same commit for `refs/remotes/origin/master`
- `.git/logs/HEAD:1` → `clone: from https://github.com/basecamp/omarchy.git`
- `.git/FETCH_HEAD` (63 bytes) names the same commit for branch `master`.
- `.git/refs/heads/` is empty (refs are packed).

So the checkout commit **equals** the v3.8.4 tag commit. All **22** fetched `bin/` bodies are
**byte-identical to the checkout's files** (`sha256sum` of `~/.local/share/omarchy/bin/<name>`
matches the table above for every file). This is file-read evidence that the host checkout
matches the tag; it is still not proof that a given host *run* used these files.

## 3. Call graph (v3.8.4, `omarchy-theme-set`)

`omarchy-theme-set <name>` calls, in order:
`:34` `omarchy-theme-colors-from-alacritty` (conditional, :33) → `:38`
`omarchy-theme-set-templates` → `:49` `omarchy-theme-bg-next` (conditional, :48) →
`:54` `omarchy-restart-waybar` (conditional, :53) → `:56` `omarchy-restart-swayosd` →
`:57` `omarchy-restart-terminal` → `:58` `omarchy-restart-hyprctl` →
`:59` `omarchy-restart-btop` → `:60` `omarchy-restart-opencode` →
`:61` `omarchy-restart-mako` → `:62` `omarchy-restart-helix` → `:65` `omarchy-theme-set-foot`
→ `:66` `omarchy-theme-set-gnome` → `:67` `omarchy-theme-set-browser` →
`:68` `omarchy-theme-set-vscode` → `:69` `omarchy-theme-set-obsidian` →
`:70` `omarchy-theme-set-keyboard` → `:73` `omarchy-hook theme-set "$THEME_NAME"`.

Theme-name derivation `:17`: strip HTML-ish tags, lowercase, spaces → `-`
(`sed -E 's/<[^>]+>//g' | tr '[:upper:]' '[:lower:]' | tr ' ' '-'`). Existence gate `:19`:
directory must exist in `$OMARCHY_PATH/themes/<name>` or `$HOME/.config/omarchy/themes/<name>`.

## 4. Exact write set (HOME paths)

### 4.1 Staging directory (before the swap)

`omarchy-theme-set:12-15` declares the four roots:
`$HOME/.config/omarchy/current/theme`, `.../current/next-theme`, `.../themes`,
`$OMARCHY_PATH/themes`.

- `:25-26` `rm -rf "$NEXT_THEME_PATH"` then `mkdir -p "$NEXT_THEME_PATH"` — staging dir recreated.
- `:29-30` `cp -r` official theme tree first, then the user theme tree **over it**
  (`2>/dev/null` on both: a missing source is silently ignored, and copy failures do not abort).
- `:33-35` only if `next-theme/colors.toml` is missing **and** `next-theme/alacritty.toml` exists:
  `omarchy-theme-colors-from-alacritty "$NEXT_THEME_PATH"`, which writes
  `$THEME_SOURCE/colors.toml` (`colors-from-alacritty:10,185,187`; it also exits 0 early if the
  file already exists, `:19-21`).
- `omarchy-theme-set-templates` writes into `$HOME/.config/omarchy/current/next-theme/<basename>`
  for each `*.tpl` (`:38-45`), user templates first then `$OMARCHY_PATH/default/themed/*.tpl`,
  and **never overwrites** a file the theme already provided (`:43` `if [[ ! -f $output_path ]]`).
  Its inputs: `$NEXT_THEME_DIR/colors.toml` (`:9`), `$HOME/.config/omarchy/themed` (`:7`),
  `$OMARCHY_PATH/default/themed` (`:6`). Substitutions are `{{ key }}`, `{{ key_strip }}`,
  `{{ key_rgb }}` (`:27-31`), applied with `sed -f` (`:44`).

**OBSERVED on this host**: `~/.local/share/omarchy/default/themed/` holds 17 templates →
`alacritty.toml, btop.theme, chromium.theme, foot.ini, ghostty.conf, gum.env.conf, helix.toml,
hyprland-preview-share-picker.css, hyprland.conf, hyprlock.conf, keyboard.rgb, kitty.conf,
mako.ini, obsidian.css, swayosd.css, walker.css, waybar.css`. `~/.config/omarchy/themed/`
contains only `alacritty.toml.tpl.sample` (no `*.tpl` match). `~/.config/omarchy/themes/` is
empty. `~/.config/omarchy/current/theme/` contains exactly those 17 generated names plus
`colors.toml`, `icons.theme`, `neovim.lua`, `vscode.json`, `unlock.png`, `preview.png`,
`preview-unlock.png`, `backgrounds/`.

### 4.2 The swap — `current/theme` is a **directory**, not a symlink

- `:41-42` `rm -rf "$CURRENT_THEME_PATH"` then `mv "$NEXT_THEME_PATH" "$CURRENT_THEME_PATH"`.
  **OBSERVED**: `~/.config/omarchy/current/theme` is `drwxr-xr-x`, not a symlink. There is no
  symlink write for the theme itself; the rename replaces the tree. A reader holding a path
  into the old tree sees it disappear at `:41`.
- `:45` `echo "$THEME_NAME" >"$HOME/.config/omarchy/current/theme.name"` — plain file, LF
  terminated. **OBSERVED** now: `xxd` → `6d61 7474 652d 626c 6163 6b0a`, i.e. `matte-black\n`
  (12 bytes).

### 4.3 Background — symlink write

`:48-50` unless `OMARCHY_THEME_SKIP_BACKGROUND == 1`, run `omarchy-theme-bg-next`:

- `bg-next:6-9` reads `current/theme.name`; candidates are
  `$HOME/.config/omarchy/backgrounds/<theme>/` and `$HOME/.config/omarchy/current/theme/backgrounds/`
  (`:7-8`), enumerated `find -L … -maxdepth 1 -type f -print0 | sort -z` (`:11`).
- `:46` `ln -nsf "$NEW_BACKGROUND" "$CURRENT_BACKGROUND_LINK"` where the link is
  `$HOME/.config/omarchy/current/background` (`:9`). It **cycles**: the next file after the
  current link target, wrapping (`:41-42`), and falls back to the first (`:37-39`).
- `:49-50` `pkill -x swaybg` then `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill`.
- Empty candidate set (`:14-17`): `notify-send "No background was found for theme"`, kill
  swaybg, relaunch it with `--color '#000000'` — no symlink write.

`omarchy-theme-bg-set <path>` is the explicit variant: `ln -nsf` the `realpath`ed file onto the
same `current/background` link (`:12-21`), then the same swaybg kill/relaunch (`:24-25`).
`omarchy-theme-refresh` re-runs theme-set with `OMARCHY_THEME_SKIP_BACKGROUND=1`
(`refresh:8`), i.e. refresh **never** repoints the background link.
**INFERENCE**: after a refresh across a theme swap, `current/background` can point into a
path in the replaced tree until the next bg-set/bg-next; the script does not revalidate it.

**OBSERVED** now: `current/background -> /home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg`
(71-byte target, symlink owned by the user, mtime 2026-10-03 17:49). `theme/backgrounds/`
holds 4 files (`0-ship-at-sea.jpg`, `1-dark-waters.jpg`, `2-dot-hands.jpg`, `omarchy.png`), so
`sort -z` order is `0-…`, `1-…`, `2-…`, `omarchy.png`.

### 4.4 App-specific theme writes (all after the swap, all read `current/theme/*`)

| helper | write / effect | anchor |
|---|---|---|
| `omarchy-theme-set-foot` | no file; OSC escape sequences `\033]4;N;…\007`, `]10`, `]11`, `]12`, `]17`, `]19` written to each `foot` child's `/dev/pts/*` tty | `:26` `printf '%b' "$foot_osc" >"$tty"` |
| `omarchy-theme-set-gnome` | `gsettings` only: `color-scheme` `prefer-light`/`prefer-dark`, `gtk-theme` `Adwaita`/`Adwaita-dark` (chosen by `current/theme/light.mode` existence), `icon-theme` from `current/theme/icons.theme` else `Yaru-blue` | `:6-20` |
| `omarchy-theme-set-browser` | `/etc/chromium/policies/managed/color.json` and the same under `/etc/opt/chrome`, `/etc/opt/edge`, `/etc/brave` — each only if that dir exists (`:19`); JSON `{"BrowserThemeColor": "...", "BrowserColorScheme": "device"}` via `tee` (`:20`); then `--refresh-platform-policy --no-startup-window` if the browser binary and process are present (`:28-29`) | `:20,33-44` |
| `omarchy-theme-set-vscode` | `mkdir -p` + create `{}` if absent, then `sed -i --follow-symlinks` insert/update `"workbench.colorTheme"` in `~/.config/{Code,Code - Insiders,VSCodium,Cursor}/User/settings.json`; may run `--install-extension`; gated by `omarchy-toggle-enabled skip-*-theme-changes` | `:22-31,37-40` |
| `omarchy-theme-set-obsidian` | per vault in `~/.config/obsidian/obsidian.json`: `mkdir -p <vault>/.obsidian/themes/Omarchy`, create `manifest.json` with a heredoc, copy `theme.css` from `current/theme/obsidian.css` | `:13-27` |
| `omarchy-theme-set-keyboard` | delegates to `omarchy-theme-set-keyboard-asus-rog` and `omarchy-theme-set-keyboard-f16` (not fetched) | `:6-7` |

`omarchy-theme-set-browser` does **not** use `sudo`; on this host the only existing policy dir
is `/etc/chromium/policies/managed` and it is `drwxrwxrwx`, so the user-writable `tee` succeeds
there. **OBSERVED**: `color.json` exists, owned by `vgpnk`, 65 bytes,
`{"BrowserThemeColor": "#121212", "BrowserColorScheme": "device"}`; mtime 2026-10-03 17:49 is
the same second as the theme dir and the background link.

### 4.5 Hook

`:73` `omarchy-hook theme-set "$THEME_NAME" >/dev/null`. `omarchy-hook` runs
`$HOME/.config/omarchy/hooks/theme-set` if it is a file, then every non-`.sample` file in
`$HOME/.config/omarchy/hooks/theme-set.d` (`:14-27`), each via `bash` with the theme name as
`$1`. It sets `set -e` but each hook failure is tolerated (`|| echo "Hook failed: …"`, `:19,26`).
**OBSERVED**: `~/.config/omarchy/hooks/theme-set.d/` exists and contains only
`show-theme-notification.sample` (270 bytes), so no enabled theme-set hook file exists.

## 5. Signals and restarts (exact, in order)

All of these are unconditional calls from `omarchy-theme-set` unless the table says otherwise;
each helper's own guard is listed.

| target | mechanism | guard in helper | anchor |
|---|---|---|---|
| Waybar | `pkill -9 -x waybar`; `setsid uwsm-app -- waybar` | caller checks `pgrep -x waybar` first (`theme-set:53`) | `restart-waybar:6-7` |
| swayosd-server | `systemctl --user daemon-reload`; `stop` ; `pkill -x swayosd-server`; `reset-failed`; `enable --now` | unconditional; `\|\| true` on stop/pkill/reset | `restart-swayosd:5-9` |
| Alacritty | `touch ~/.config/alacritty/alacritty.toml` (mtime write → live reload) | file must exist | `restart-terminal:5-7` |
| kitty | `killall -SIGUSR1 kitty` | `pgrep -x kitty` | `restart-terminal:9-11` |
| ghostty | `killall -SIGUSR2 ghostty` | `pgrep -x ghostty` | `restart-terminal:13-15` |
| Hyprland | `hyprctl reload` | unconditional (no process check) | `restart-hyprctl:5` |
| btop | `pkill -SIGUSR2 btop` | **none** — `pkill` return 1 ignored; no `setsid`/respawn | `restart-btop:5` |
| opencode | `killall -SIGUSR2 opencode` | `pgrep -x opencode` | `restart-opencode:5-7` |
| mako | `makoctl reload` | unconditional | `restart-mako:5` |
| Helix | `pkill -USR1 helix` | `pgrep -x helix` | `restart-helix:5-7` |
| swaybg | `pkill -x swaybg`; `setsid uwsm-app -- swaybg -i current/background -m fill` | via bg-next unless skip-background | `bg-next:49-50` |
| browsers | `--refresh-platform-policy --no-startup-window` | `omarchy-cmd-present` + `pgrep` | `set-browser:28-29,34-44` |

Notable semantics: Waybar is **SIGKILL + full respawn** (not reload) and only if it was running;
`omarchy-restart-terminal` restarts nothing except kitty/ghostty via signals and touches
Alacritty's config; `omarchy-restart-swayosd` is the only helper that drives user systemd
(`daemon-reload`, `stop`, `reset-failed`, `enable --now`); `hyprctl reload` and `makoctl reload`
have no existence guard, so on a host where mako is absent they emit an error but cannot abort
the rest (theme-set has no `set -e`).

## 6. Host declaration cross-check (OBSERVED, no execution)

- Chain is consistent for the current theme: `current/theme/colors.toml:1,4`
  (`accent = "#e68e0d"`, `background = "#121212"`) → `current/theme/waybar.css:1-2` and
  `current/theme/walker.css:1-6` (`@define-color base #121212`) → `current/theme/chromium.theme`
  `18,18,18\n` → `/etc/chromium/policies/managed/color.json` `"#121212"`.
- `theme.name` `matte-black` matches the official theme directory name convention
  (`$OMARCHY_PATH/themes/<lowercase-hyphenated>`); `$OMARCHY_PATH` is declared as
  `$HOME/.local/share/omarchy` in `~/.config/uwsm/env:4`.
- Theme picker route: `~/.local/share/omarchy/bin/omarchy-menu:297-298` reaches themes through
  `omarchy-launch-walker -m menus:omarchythemes` (P3 Walkers is the selector UI, not the
  writer; the writer is `omarchy-theme-set`).

## 7. What this does **not** establish (remaining unknowns)

- **[UNK] Host execution history.** `color.json`/theme-dir/background mtimes (2026-10-03 17:49)
  are consistent with one theme-set run, but no receipt records a run; timestamps alone do not
  prove which code path ran. `theme.name` could have been written by hand.
- **[UNK] Whether Waybar/swayosd/kitty/ghostty/btop/opencode/mako/helix were running** at that
  moment — no process state was captured, and process probing is out of bounds this round.
- **[UNK] `omarchy-theme-set-keyboard-asus-rog` / `-f16`** effects (not fetched; they are leaves
  of `omarchy-theme-set-keyboard`).
- **[UNK] Hook semantics beyond dispatch**: no enabled `theme-set` hook exists on this host, so
  the `omarchy-hook` path is declared but unexercised.
- **[UNK] Actual swaybg/compositor behaviour** after `pkill`/relaunch; the scripts declare
  intent, not result.
- Tag source ≠ host binary in general; here byte equality for the 22 fetched `bin/` files is
  file-read evidence for this checkout only.

## 8. Runnable read-only checks (no host mutation)

```sh
# tag → commit
git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'
# checkout identity and file equality (read .git bytes; do not run git in the checkout)
sed -n '2p;508p' ~/.local/share/omarchy/.git/packed-refs
sha256sum ~/.local/share/omarchy/bin/omarchy-theme-set        # expect 79069c80…
sha256sum ~/.config/omarchy/current/theme.name                # content: matte-black\n
readlink ~/.config/omarchy/current/background
ls ~/.local/share/omarchy/default/themed | wc -l              # 17 -> 17 template outputs
ls ~/.config/omarchy/current/theme | wc -l                    # 25 entries = 17 outputs + colors.toml,
                                                              #   icons.theme, neovim.lua, vscode.json,
                                                              #   unlock.png, preview.png, preview-unlock.png,
                                                              #   backgrounds/
# re-verify every receipt body against its recorded digest
python3 - <<'PY'
import json,hashlib,pathlib
d=pathlib.Path(".ufo/waves/round-18/fetch/SrcOmarchyThemeSet")
for l in (d/"receipts.jsonl").read_text().splitlines():
    r=json.loads(l); b=(d/r["body"]).read_bytes()
    assert hashlib.sha256(b).hexdigest()==r["sha256"] and len(b)==r["bytes"], r["body"]
print("receipts ok")
PY
```

## 9. Tooling

No install or upgrade was performed by this seat; `curl 8.23.0` and coreutils were already
present. No web source beyond `raw.githubusercontent.com` and the `ls-remote` tag lookup was
opened.

**Confidence**: write/signal map — high (22/22 bodies byte-match the checkout; every claim
anchored to a line). Host execution history — low, explicitly `[UNK]`.

## 10. Draft registry row and cross-note handoff

Draft row for `corpus/SOURCES.md` (id and `used-by` assigned by L1; the P5 note is
`corpus/knowledge/theme-route-r18.md` per the round-18 brief):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx-pending | omarchy v3.8.4 theme-set implementation — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-theme-set plus helpers `omarchy-theme-set-templates`, `omarchy-theme-bg-next`, `omarchy-theme-bg-set`, `omarchy-hook`, `omarchy-restart-*`, `omarchy-theme-set-{browser,foot,gnome,vscode,obsidian,keyboard}` | code | A | documented theme and wallpaper write chain, restart fan-out and app-theme side effects for the host's declared omarchy release (P5), with no runtime claim | tag v3.8.4 = `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`; `omarchy-theme-set:12-15,25-30,33-38,41-45,48-50,53-62,65-73`; `omarchy-theme-bg-next:11,14-17,37-50`; bodies sha256 `79069c80…` (set), `01264122…` (templates), `ee482812…` (bg-next), `638f265f…` (bg-set); receipts `.ufo/waves/round-18/fetch/SrcOmarchyThemeSet/receipts.jsonl` | `current/theme` is replaced as a directory (rm -rf then mv, never a symlink); `theme.name` is a plain LF file; `current/background` is a symlink that bg-next advances (cycles) rather than resets; theme-set fans out to seven restart helpers plus background, and to six app-theme helpers before one hook | mined | 2026-10-20 | on-release | corpus/knowledge/theme-route-r18.md |

Cross-note handoff: `walker.css` and `waybar.css` in `~/.config/omarchy/current/theme/` are
**template outputs generated at theme-set time** from `colors.toml`
(`omarchy-theme-set-templates:38-45`; both `.tpl` files are in
`~/.local/share/omarchy/default/themed/`). That makes P3/P2 styling downstream of P5 theme
state — a P3 route note should cite this as the *documented* link, without claiming the host
ever ran theme-set.
