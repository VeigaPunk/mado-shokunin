# ReviewThemeHost — `## Host declaration` of `corpus/knowledge/theme-route-r18.md`

Reviewer: MadoR18.ReviewThemeHost (wave 2, falsify). Artifact under review:
integrated revision `4c103b55b1ea5c3c555884afe3eb69b5189701b7`. The worktree copy is
byte-identical to the committed blob: note sha256 `b080bc479be42644cd3d2cf2cc5f4bdd44651cf137b1ee085353f23334a19f23`
(worktree and `git show <rev>:corpus/knowledge/theme-route-r18.md` agree), S095 line 107
sha256 `20860a465acd7e918759853465b98a85521efcea5831dadc4491402016b18141`; `git diff`
against the integration commit for both files is empty.

Method: host trees read as bytes only — `sha256sum`, `stat -c`, `readlink`, `find -printf`,
`sed -n`, `grep -n`, `od -c`, `realpath -m`, `cat -A`. No theme set, no `omarchy*`, no
swaybg/hyprctl/pgrep/pacman/systemctl. No writes to any config tree. No fetch this pass:
host-to-tag equality is checked against the committed `mado-fetch-receipt-v1` lines in
`.ufo/waves/round-18/fetch/NoteTheme/receipts.jsonl`, not against a fresh download.

## Verdict

Every hash, size, mtime, link target, line anchor, count and absence asserted in
§ Host declaration re-measured **exact** — no contradiction found in any asserted value.
Two live, declared consumer edges that name `current/theme` are **omitted** from the
section (F1), and row S095's declared scope/source list inherits the same omission (F2).
One exclusion sentence is narrower than the sibling set it describes (F3).

## What reproduced (all measured this pass)

### `current/` state

| claim | measured | result |
|---|---|---|
| `theme.name` 12 B, sha `48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b`, mtime 17:49:02.617 | sha identical; 12 B; `2026-10-03 17:49:02.617593239 -0300`; bytes `matte-black\n` | pass |
| `background` symlink 71 B → `/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg`, target sha `55fa691a…`, 1,681,677 B, mtime .620 | `readlink` gives exactly that absolute path; link size 71; target sha256 `55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac`; 1,681,677 B; `…02.620233763` | pass |
| `theme/` directory, 24 files, mtime .613 | directory (mode 755), `find -maxdepth 1 -type f` = 24, `…02.613233762`; only subdir `backgrounds/` | pass |
| `backgrounds/` 4 images | `0-ship-at-sea.jpg` 1,681,677 B; `1-dark-waters.jpg` 1,033,920 B; `2-dot-hands.jpg` 482,067 B; `omarchy.png` 4,491 B | pass |

### Nine key pins (full digests measured)

```
a1807a176659d7d6beaaf2a5c96cb7a03d131ee2740b8961d4c9aee393839c18  waybar.css
f88118e98b44cfa32ebc2d8f2394bd0448b2d1e0c01f01dd48677fe66ec7522b  swayosd.css
f44cb45063494d2f4a8f489c47d8901b3bc98b27fbd1ca1c5a8801b40606bbc0  walker.css
3ef010e72b5f69113e1500bb083fb053f9f121212ad5ed4fe74ad8d12507ad0b  hyprlock.conf
79126bec8c28da306712148734a3ee58335a8bd48bf863e4e2e2db6d6d8344b6  hyprland.conf
8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139  alacritty.toml
95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec  mako.ini
e9ee6fb643852b378429fc382badef31180aac4cfdccf7201c6749d1999acda9  btop.theme
dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786  colors.toml
```
All nine match the note's prefixes exactly. `colors.toml` also equals the tag receipt
digest in `fetch/NoteTheme/receipts.jsonl` (200, 461 B).

### Absences

- `current/next-theme`: `find current -maxdepth 1 -name 'next-theme*'` → no entry of any
  type (no dangling link). pass.
- `~/.config/omarchy/backgrounds`: no entry of any type. pass.
- `~/.config/omarchy/themes/`: `find … -mindepth 1 | wc -l` → 0. pass.
- `~/.config/omarchy/hooks/theme-set.d/`: only `show-theme-notification.sample`; the skip
  claim is confirmed on bytes — `~/.local/share/omarchy/bin/omarchy-hook:25` is
  `[[ $hook == *.sample ]] && continue`. pass.

### Payload vs rendered

- Eight payload names present among the 24 (btop.theme, colors.toml, icons.theme,
  neovim.lua, preview.png, preview-unlock.png, unlock.png, vscode.json).
- Seven host-to-host comparisons against `~/.local/share/omarchy/themes/matte-black/x`
  are **identical for all seven**: `btop.theme e9ee6fb6…`, `icons.theme
  1c2342215182a8e2880028e03e679fad194dbdfa5155b55daf8386390526cfbc`, `neovim.lua
  ec7df5fb1d3b7fc644fa0f69cd959ebc43fad8ebdb4aedfd01a5b1e387cd9778`, `preview.png
  02bf70793f2617710885cc8e389d3d00186b46e1a5a3fe5ffebe776b4ae5ae18`,
  `preview-unlock.png 00ae994f78564d06c08b17eff733073217400b2bfa2f18405ae10e4b34afe212`,
  `unlock.png ac806f14a214140f33e6c222879633ea24b194f59a86c59847e67bb379680c2d`,
  `vscode.json 18171ea89a57d4639b935d80a6b271c19a23e4ebe682cc0703144bb77474b83c`.
- Count arithmetic: `~/.local/share/omarchy/default/themed` holds exactly **17** `*.tpl`;
  the 16 declared rendered names equal those 17 minus `btop.theme` (name-set `diff` empty).
  8 + 17 − 1 = 24. pass.
- Whole-tree sweep (all 24 top-level files hashed, not only the pinned nine): the seven
  remaining names match the round-7 census prefixes and sizes exactly — `chromium.theme`
  9 B `e02da2b72d23d24c…`, `foot.ini` 378 B `d9c2e20e079a9314…`, `ghostty.conf` 454 B
  `418636f99922f1ea…`, `helix.toml` 4,582 B `c7f85d447f480b00…`, `keyboard.rgb` 8 B
  `8f32a6ecf0de6c50…`, `kitty.conf` 444 B `e8795b49ff5b6135…`, `obsidian.css` 2,523 B
  `d195eeaf760f9d87…`; plus `gum.env.conf` 5,413 B `ecab9ec4…` and
  `hyprland-preview-share-picker.css` 1,844 B `24474e34…` (F1 targets).

### Consumer table (11 rows)

| row | measured |
|---|---|
| Hyprland core | `hypr/hyprland.conf` sha `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365`; `:4` = `source = ~/.local/share/omarchy/default/hypr/autostart.conf`; `:13` = `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| default autostart | host sha `acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441` = receipt digest; `:5` exactly `exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill` |
| user autostart | sha `5ace17016fe2998aa6e7ad2221c1889b430aa4b94faf5ef1f907d6301dd5fc46`; 5 lines; `:5` grok-bot exec; no `swaybg` anywhere; the file is loaded at `hyprland.conf:19` (the note does not cite `:19`) |
| hyprlock | sha `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1`; `:1` theme source; lines 7–12 are the `background { … }` block, `path = ~/.config/omarchy/current/background` at `:10` |
| waybar | sha `8f335ca01da53d32eb968c2f7752f3149f073e8e56411980913f4dd25d385fdf`; `:1` import |
| swayosd | sha `6e3ba08fd929ba345c405c151858a581e2c0ced724ef07e0e23f155731f76d8c`; `:1` import |
| alacritty | sha `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8`; `:1` import |
| walker | config sha `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787`, `:3-4` lines exact; style sha `481267af0e89a475c851de82692176b4b496045e41081fa94eec0fbaf32500b0`; `:1` has 7 `../`, and `realpath -m` resolves it to `/home/vgpnk/.config/omarchy/current/theme/walker.css` |
| mako | symlink 50 B → `/home/vgpnk/.config/omarchy/current/theme/mako.ini`; target `95bf0c86…` |
| btop | symlink 52 B → `/home/vgpnk/.config/omarchy/current/theme/btop.theme`; `btop.conf:5` `color_theme = "current"`; target `e9ee6fb6…` |
| neovim | symlink 52 B, text `../../../../.config/omarchy/current/theme/neovim.lua` |

All three symlinks are mode 777 and present, as S095 states.

### Host binary/tree versions

- `/var/log/pacman.log:1158` = `[2026-10-03T17:44:27-0300] [ALPM] installed swaybg (1.2.2-1)`;
  `grep -n swaybg` returns exactly two lines, 484 and 1158; line 484 is the install
  command line and contains `swaybg` in its package list; no upgrade line. pass.
- Host copies equal the receipt digests: `bin/omarchy-theme-set 79069c80…`,
  `bin/omarchy-theme-bg-next ee482812…`, `bin/omarchy-theme-bg-set 638f265f…`,
  `bin/omarchy-theme-set-templates 01264122…`, `default/hypr/autostart.conf acb6a668…`.
  The four named in the note are therefore byte-identical to the tag files on the
  receipt record.
- Round-7 census agreement: `theme.name 48749715…`, background target, 24-file count,
  eight ★ prefixes and the mako/btop/neovim symlinks all reproduce the census.

## Findings

### F1 — medium — two live consumer edges naming `current/theme` are absent from the table

The section is titled “Consumers of `current/theme` and `current/background`”, yet these
two declared edges, both present on the host this pass, are in neither the table nor the
§ Declared-only paragraph nor the § Unexercised behavior consumer list:

1. `~/.config/hyprland-preview-share-picker/config.yaml:4`
   `stylesheets: ["../omarchy/current/theme/hyprland-preview-share-picker.css"]`
   — config 2,412 B, sha256 `cf88364e497e4af2adaff9a0b7ca12227d29f831bc7e18846dd8f03bf4c618a8`;
   target `current/theme/hyprland-preview-share-picker.css` 1,844 B, sha256
   `24474e34a4ed902250858eec8562838de33ce4a2782c5026ab764eb4cf6566c9`.
2. `~/.local/share/omarchy/default/hypr/envs.conf:3`
   `source = ~/.config/omarchy/current/theme/gum.env.conf` (guarded by
   `# hyprlang noerror true/false`); envs.conf is 785 B, sha256
   `80067da7b52fe1b45812f3d98cf44c025a693235e7380f4f405915ee4bf680fe`, and is itself
   sourced at `~/.config/hypr/hyprland.conf:9`; target `current/theme/gum.env.conf`
   5,413 B, sha256 `ecab9ec497c555155536913c09e03e612f1e91296953ead8e9052da310f3435f`.

The round-7 census the note says it re-measures and agrees with lists both
(`theme-wallpaper-plane.md` §4 rows for `gum.env.conf` — “live env agrees” — and
`hyprland-preview-share-picker.css`). The note mentions both target files only as
*rendered names* (line 92), so a reader of § Host declaration cannot see that either has
a live consumer. This is an omission of fact, not a wrong pin; it narrows the section’s
“Consumers” claim and makes its census-agreement statement (line 121) look broader than
the table supports (the line itself is scoped to pins and is true).

### F2 — low-medium — row S095 declares a scope its source list does not cover

S095’s `scope` says “this host’s P5 theme tree, wallpaper symlink and **the import lines
that name `current/theme` or `current/background`**”, but its `source` cell (10 paths)
omits the two files in F1, whose lines literally name `current/theme/…`; the row therefore
under-covers its own scope statement. Related, weaker point: the anchor carries only three
sha256 values (`theme.name`, the background target, the walker style) while the note’s
§ Host declaration pins ~19 files by hash; a re-checker of S095 alone cannot compare the
note’s nine in-theme pins and eight consumer hashes without recomputing them. The draft
row (`.ufo/waves/round-18/drafts/NoteTheme-rows.md:19`) has the same source list and
anchor, so this is not an L1 trim. The integrated row’s `recheck` is `90d` whereas the
draft said `on-change; re-hash the files and readlink the links`; the note’s own head
`recheck` still says to re-hash the host files, so the row now prescribes a calendar
cadence for state that changes on every theme set. Not a byte contradiction; a
traceability/registration drift between the row and the note it backs.

### F3 — low — exclusion sentence covers `.bak*` only, but a non-`.bak` sibling carries the import

Line 76: “The `.bak*` siblings of the consumer files carry the same import lines; they are
not loaded and are excluded.” Measured: the `.bak` siblings behave as stated for the files
that have import lines (`hypr/hyprland.conf.bak.1792267376` carries the `:4` and `:13`
sources; the four `waybar/style.css.bak*` and `alacritty.toml.bak.*` carry the line-1
import), and `hypr/autostart.conf.bak.1791942509` carries none (vacuous). But
`~/.config/waybar/style.css.pre-ai-readability` (2,118 B) is a **non-`.bak` sibling that
also carries `@import "../omarchy/current/theme/waybar.css";`** at line 1 and is not
covered by the exclusion rationale. It is inert: `waybar/config.jsonc` has no `style` key
(only `reload_style_on_change`), so waybar’s default `style.css` remains the loaded file
and no hash in the table is affected. Precision issue only.

## Residual risk / verification gaps

- No upstream fetch this pass. “Byte-identical to the tag” was checked as host-copy
  sha256 == the committed `NoteTheme` receipt sha256; it was not re-derived from a fresh
  download. A non-author can re-fetch the four raw URLs and compare.
- No consumer liveness or render was observed (host pause): no swaybg argv/layer surface,
  no waybar/mako/btop/alacritty reload check, no hyprlock draw. The note’s `[UNK]` list
  remains the honest state; I did not exercise it.
- The 1.68 MB active background exceeds the fetch cap; its bytes were hashed host-side
  only, matching the note.
- `~/.local/share/omarchy/.git/{ORIG_HEAD,packed-refs}` tag claims were not read (the
  host-copy digests were compared to receipts instead); no git command was run inside the
  omarchy checkout.
- F1/F2 depend on treating a `stylesheets:` list and a guarded hyprlang `source =` as
  “import lines”. That is the note’s own usage for `source =` rows elsewhere in the table,
  so the omission is inconsistent with its own convention.

## Commands run (representative, with results)

```
sha256sum theme.name theme/backgrounds/0-ship-at-sea.jpg theme/{waybar.css,swayosd.css,walker.css,hyprlock.conf,hyprland.conf,alacritty.toml,mako.ini,btop.theme,colors.toml}
  → the 11 digests listed above
stat -c '%n|%s|%y|%F' theme.name background theme/backgrounds/0-ship-at-sea.jpg theme
  → 12|…02.617593239|regular; 71|…02.620233763|symlink; 1681677|…02.541927358|regular; 610|…02.613233762|directory
readlink background → /home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg
find theme -maxdepth 1 -type f | wc -l → 24 ; find theme/backgrounds -maxdepth 1 -type f → 4 names+sizes
sha256sum .config/{hypr/hyprland.conf,hypr/hyprlock.conf,hypr/autostart.conf,waybar/style.css,
  swayosd/style.css,alacritty/alacritty.toml,walker/config.toml} \
  .local/share/omarchy/default/walker/themes/omarchy-default/style.css \
  .local/share/omarchy/default/hypr/autostart.conf
  → all nine digests listed above; link targets via readlink (mako 50 B, btop 52 B, nvim 52 B)
sed -n '1p;4p;13p' .config/hypr/hyprland.conf → :4 default autostart, :13 theme source
sed -n '1p;7,12p' .config/hypr/hyprlock.conf → :10 path = ~/.config/omarchy/current/background
realpath -m …/omarchy-default/../../../../../../../.config/omarchy/current/theme/walker.css
  → /home/vgpnk/.config/omarchy/current/theme/walker.css
sha256sum bin/{omarchy-theme-set,omarchy-theme-bg-next,omarchy-theme-bg-set,omarchy-theme-set-templates} \
  default/hypr/autostart.conf themes/matte-black/{btop.theme,icons.theme,neovim.lua,preview.png,
  preview-unlock.png,unlock.png,vscode.json,colors.toml}
  → host copies equal receipt digests; seven payload files equal the host tree copies
grep -n swaybg /var/log/pacman.log → 484, 1158 only
test -e …/current/next-theme → absent; find … -name 'next-theme*' → none of any type
find ~/.config/omarchy/backgrounds -maxdepth 1 → none; find ~/.config/omarchy/themes -mindepth 1 | wc -l → 0
find ~/.config/omarchy/hooks/theme-set.d -mindepth 1 → show-theme-notification.sample only
grep -n sample /home/vgpnk/.local/share/omarchy/bin/omarchy-hook → :25 [[ $hook == *.sample ]] && continue
find ~/.local/share/omarchy/default/themed -maxdepth 1 -name '*.tpl' | wc -l → 17
diff <declared 16 rendered names> <tpl names minus btop.theme> → empty
grep -rn --exclude='*.bak*' -E 'current/(theme|background)' .config/{hypr,waybar,swayosd,alacritty,walker,btop,nvim,mako,hyprland-preview-share-picker} \
  .local/share/omarchy/default/{hypr,walker}
  → the 11 table rows plus config.yaml:4 (share-picker) and envs.conf:3 (gum.env.conf); plus
    .config/waybar/style.css.pre-ai-readability:1 (non-.bak sibling)
sha256sum .config/hyprland-preview-share-picker/config.yaml .local/share/omarchy/default/hypr/envs.conf
  .config/omarchy/current/theme/{gum.env.conf,hyprland-preview-share-picker.css}
  → cf88364e…, 80067da7…, ecab9ec4…, 24474e34… (sizes 2,412 / 785 / 5,413 / 1,844 B)
```

All outputs above are byte reads; no host state was modified.
