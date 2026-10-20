# S095 re-open — non-author check (host P5 theme state and consumer declarations)

Target: `corpus/SOURCES.md:107` (row S095) at `4c103b55b1ea5c3c555884afe3eb69b5189701b7`.
Citing note: `corpus/knowledge/theme-route-r18.md` (head `source:` names S092-S095;
`surface: P5`). Working-tree bytes equal the committed bytes at 4c103b55:

```
git rev-parse 4c103b55b1ea5c3c555884afe3eb69b5189701b7^{commit}
4c103b55b1ea5c3c555884afe3eb69b5189701b7
git show 4c103b55…:corpus/knowledge/theme-route-r18.md | sha256sum -> b080bc479be42644cd3d2cf2cc5f4bdd44651cf137b1ee085353f23334a19f23
sha256sum corpus/knowledge/theme-route-r18.md                     -> b080bc479be42644cd3d2cf2cc5f4bdd44651cf137b1ee085353f23334a19f23
git show 4c103b55…:corpus/SOURCES.md | sha256sum -> 9552071c0b286075ffabb3a7ea1373e8dbaef5e6c37f906d2620ae83454f26de
sha256sum corpus/SOURCES.md                     -> 9552071c0b286075ffabb3a7ea1373e8dbaef5e6c37f906d2620ae83454f26de
```

Method: host files read as bytes only (`sha256sum`, `od`, `sed -n`, `readlink`,
`stat`, `find` without `-exec`, `grep -c`); read-only `git show/rev-parse`; no
package, service, compositor, process or input operation; `/var/log/pacman.log`
read only at the cited lines. No file outside this report was written.

## Commands run and their output

```
cd ~/.config/omarchy/current
sha256sum theme.name
48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b  theme.name
od -An -c theme.name
   m   a   t   t   e   -   b   l   a   c   k  \n
stat -c 'size=%s mtime=%y' theme.name
size=12 mtime=2026-10-03 17:49:02.617593239 -0300

readlink background
/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg
sha256sum "$(readlink -f background)"
55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac  …/theme/backgrounds/0-ship-at-sea.jpg
stat -c 'size=%s mtime=%y' "$(readlink -f background)"
size=1681677 mtime=2026-10-03 17:49:02.541927358 -0300
stat -c '%s %N' background
71 '…/current/background' -> '…/current/theme/backgrounds/0-ship-at-sea.jpg'

find theme -maxdepth 1 -type f | wc -l
24            # alacritty.toml btop.theme chromium.theme colors.toml foot.ini ghostty.conf
              # gum.env.conf helix.toml hyprland.conf hyprland-preview-share-picker.css
              # hyprlock.conf icons.theme keyboard.rgb kitty.conf mako.ini neovim.lua
              # obsidian.css preview.png preview-unlock.png swayosd.css unlock.png
              # vscode.json walker.css waybar.css
find theme -maxdepth 2 -printf '%y %P\n'   # d backgrounds; f backgrounds/{0-ship-at-sea.jpg,
                                           # 1-dark-waters.jpg, 2-dot-hands.jpg, omarchy.png}

sed -n '4p;13p' ~/.config/hypr/hyprland.conf
source = ~/.local/share/omarchy/default/hypr/autostart.conf
source = ~/.config/omarchy/current/theme/hyprland.conf
sha256sum ~/.config/hypr/hyprland.conf -> ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365

sed -n '1p;7,12p' ~/.config/hypr/hyprlock.conf
source = ~/.config/omarchy/current/theme/hyprlock.conf
background {
    monitor =
    color = $color
    path = ~/.config/omarchy/current/background
    blur_passes = 3
}
sha256sum ~/.config/hypr/hyprlock.conf -> b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1   # path at :10

sed -n '1p' ~/.config/waybar/style.css
@import "../omarchy/current/theme/waybar.css";
sha256sum -> 8f335ca01da53d32eb968c2f7752f3149f073e8e56411980913f4dd25d385fdf
sed -n '1p' ~/.config/swayosd/style.css
@import "../omarchy/current/theme/swayosd.css";
sha256sum -> 6e3ba08fd929ba345c405c151858a581e2c0ced724ef07e0e23f155731f76d8c
sed -n '1p' ~/.config/alacritty/alacritty.toml
general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]
sha256sum -> 695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8

sed -n '1p' ~/.local/share/omarchy/default/walker/themes/omarchy-default/style.css
@import "../../../../../../../.config/omarchy/current/theme/walker.css";
sha256sum -> 481267af0e89a475c851de82692176b4b496045e41081fa94eec0fbaf32500b0

readlink ~/.config/mako/config            -> /home/vgpnk/.config/omarchy/current/theme/mako.ini   (link 50 B)
readlink ~/.config/btop/themes/current.theme -> /home/vgpnk/.config/omarchy/current/theme/btop.theme (link 52 B)
readlink ~/.config/nvim/lua/plugins/theme.lua -> ../../../../.config/omarchy/current/theme/neovim.lua
readlink -f ~/.config/nvim/lua/plugins/theme.lua -> /home/vgpnk/.config/omarchy/current/theme/neovim.lua
sha256sum target mako.ini  -> 95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec
sha256sum target btop.theme -> e9ee6fb643852b378429fc382badef31180aac4cfdccf7201c6749d1999acda9

sha256sum theme/{waybar.css,swayosd.css,walker.css,hyprlock.conf,hyprland.conf,alacritty.toml,mako.ini,btop.theme,colors.toml}  (first 16 chars)
a1807a176659d7d6 f88118e98b44cfa3 f44cb45063494d2f 3ef010e72b5f6911 79126bec8c28da30
8c3d1457c09d32e8 95bf0c86c955cc81 e9ee6fb643852b37 dbdd13a629aac86d

test -e next-theme -> absent ; test -e ~/.config/omarchy/backgrounds -> absent
find ~/.config/omarchy/themes -mindepth 1 | wc -l -> 0
find ~/.config/omarchy/hooks -mindepth 1 -maxdepth 2 -> theme-set.d/show-theme-notification.sample only
find ~/.local/share/omarchy/default/themed -maxdepth 1 -name '*.tpl' | wc -l -> 17

sed -n '484p;1158p' /var/log/pacman.log ; grep -c swaybg /var/log/pacman.log -> 2
[2026-10-03T17:42:38-0300] [PACMAN] Running 'pacman -S --noconfirm --needed … swaybg …'
[2026-10-03T17:44:27-0300] [ALPM] installed swaybg (1.2.2-1)

# note lines beyond the row's file list, re-read as bytes
sed -n '5p' ~/.config/btop/btop.conf -> color_theme = "current"
sha256sum ~/.config/btop/btop.conf -> 4e17dd28c43948af48a408ed9b0901c008e57dfe3b8fcf09649ec10f28746137
sed -n '3p;4p' ~/.config/walker/config.toml
theme = "omarchy-default"
additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"
sha256sum ~/.config/walker/config.toml -> fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787
sed -n '5p' ~/.config/hypr/autostart.conf -> exec-once = /home/vgpnk/.local/share/grok-bot/appimage --ozone-platform=x11
grep -c swaybg ~/.config/hypr/autostart.conf -> 0
sha256sum ~/.config/hypr/autostart.conf -> 5ace17016fe2998aa6e7ad2221c1889b430aa4b94faf5ef1f907d6301dd5fc46
sed -n '5p' ~/.local/share/omarchy/default/hypr/autostart.conf
exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill
sha256sum …/default/hypr/autostart.conf -> acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441
# .bak siblings (carry the same import lines)
find ~/.config/{hypr,waybar,swayosd,alacritty} ~/.config/omarchy/current/theme -maxdepth 1 -name '*.bak*'
…/alacritty.toml.bak.20261003-190229  …/hyprland.conf.bak.1792267376  …/waybar/style.css.bak.* (4)
sed -n '13p' hyprland.conf.bak.1792267376 -> source = ~/.config/omarchy/current/theme/hyprland.conf
sed -n '1p'  waybar/style.css.bak.1792267376 -> @import "../omarchy/current/theme/waybar.css";

# payload host-to-host (8 files, both trees) — identical digests
current/theme: e9ee6fb643852b37 dbdd13a629aac86d 1c2342215182a8e2 ec7df5fb1d3b7fc6
               02bf70793f261771 00ae994f78564d06 ac806f14a214140f 18171ea89a57d463
~/.local/share/omarchy/themes/matte-black: same eight digests
```

## Judgment

**Kind (`code`).** Correct. The row is a set of text config/consumer files read as
bytes; host rows S019, S041, S090, S091 use the same kind for the same reason.

**Tier (`A`).** Correct. For the stated scope — *this host's* theme tree, wallpaper
link and consumer import lines — the host file bytes are the primary source, and
every pinned digest reproduced exactly. This is not a web row; no
`mado-fetch-receipt-v1` is owed (round-18 lesson M6 binds credited *web* rows).

**Scope.** Names its surface twice: `P5` and `theme`/`wallpaper` in
`this host's P5 theme tree, wallpaper symlink and the import lines …` — passes the
rubric-V T4 keyword requirement for P5 (`theme, wallpaper, hyprpaper, swaybg`).
One wording gap: the clause says the import lines *name* `current/theme` or
`current/background`, but the file list/anchor also carries `hypr/hyprland.conf:4`
(`source = ~/.local/share/omarchy/default/hypr/autostart.conf`), which names
neither; only its sourced file does, one hop later (`[OA:5]`). The anchor labels
the line honestly ("default autostart"), so this is a scope-wording gap, not a
false byte.

**`teaches` grounded.** Yes, all three clauses reproduce: the import edges and
wallpaper link exist as declared; `theme/` holds exactly 24 regular files plus
`backgrounds/` (4 images); the three consumer symlinks (mako, btop, nvim) exist
and resolve into `current/theme/`; and the stated limits (no rendering, no swaybg
process) are correct — nothing in the read establishes either.

**Anchor vs read.** All pinned values agree byte-for-byte: `theme.name`
`48749715…` content `matte-black`; background target `55fa691a…` (1,681,677 B);
walker `omarchy-default/style.css:1` `481267af…`; hyprland `:4`/`:13`; hyprlock
`:1`/`:10`; waybar, swayosd, alacritty `:1`; mako 50 B, btop 52 B, nvim relative
symlink. The note's `24 = 8 payload + 17 tpl − 1` arithmetic reproduces (17 `.tpl`
files). One literal deviation: the anchor writes the background target as
`theme/backgrounds/0-ship-at-sea.jpg`; `readlink` prints the absolute
`/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg`. Same
file, same sha256 — notation only.

**Note truthfulness.** The note's § Host declaration is accurate against this
re-read, including its absence claims (`next-theme`, user `backgrounds/`, empty
`themes/`, hooks only the `.sample`), the theme-inner pins, the payload
host-to-host equality, and the user-autostart line (`grok-bot`, 0 `swaybg`). Two
bounded attribution gaps, both true bytes but outside S095's enumerated file list:
`~/.config/walker/config.toml:3-4` (belongs to tier-A S085/S091, which the note's
head does not cite) and `~/.config/btop/btop.conf:5` (no SOURCES row lists
`btop.conf`). The `.bak*` siblings and `~/.config/hypr/autostart.conf` are the
same class. None contradicts the row; a round-19 fix is to add those paths to
S095's source cell (or cite S085/S091) and to widen the scope clause to cover
`hyprland.conf:4`.

No falsifying contradiction found: 3/3 anchor digests, 6/6 import edges, 24/24
theme files, 3/3 consumer symlinks, and every note pin reproduce.

GATE | S095 | /home/vgpnk/.config/hypr/hyprlock.conf | 2026-10-20 | hyprlock.conf:10 "path = ~/.config/omarchy/current/background" (3 words) | b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1 | agree: anchor theme.name 48749715…/matte-black, background 55fa691a…, walker style 481267af… and all six import edges reproduce byte-for-byte; only nits are a relative-form link target and a scope clause that omits hyprland.conf:4
