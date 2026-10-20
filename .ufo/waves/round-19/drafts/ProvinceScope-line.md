# ProvinceScope — one PROVINCE line: `~/.config/omarchy/**` with an in/out split

Draft only. This seat edited no lane file; `PROVINCE.md` belongs to L1.
Root of every path below: `/home/vgpnk/Projects/shokunin/mado-shokunin` unless
absolute. Host tree read 2026-10-20; `PROVINCE.md` at baseline `9c54c56`
(18 L, sha256 `7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a`,
byte-identical to the pre-registration `17661e0` and the worktree).

## The line (canonical: one physical line, verbatim)

Insert after `PROVINCE.md:16` (end of the `Refuses` paragraph), keeping one blank
line before the final slogan at `:18`; do not reflow it if the post-landing
digest is to be reproducible from this draft.

```
**Round-19 refinement (P5 theme/wallpaper route; resolves `:8-9`; no new write surface):** the theme/wallpaper state is the omarchy theme plane under `~/.config/omarchy/**`, read-only — IN: `current/theme.name`, the `current/background` link and `current/theme/**` as declared theme state (the hypr/waybar/walker/terminal consumers are the owned chain; `mako.ini`, `swayosd.css`, `btop.theme` and `neovim.lua` are chain evidence only, their consumer configs not owned), plus `themes/` as the declared selectable store; OUT (report, never absorb): `hooks/**` bodies, `branding/`, `extensions/`, `themed/` template machinery, any secret-shaped value (→ kagi), and every omarchy program update, theme write or consumer reload; `~/.local/share/omarchy/**` (checkout) is read-only source evidence for this chain (gate `theme_plane()`/`omarchy_plane()` in `tools/mado-verify.sh`; route note `corpus/knowledge/theme-route-r18.md`).
```

Why a refinement, not a transfer: `PROVINCE.md:8-9` already declares
"themes/wallpapers as declared files" with no path root, and the lane's own
audit resolves that clause to the omarchy theme tree
(`corpus/knowledge/province-accuracy-selfaudit.md:52`, C6 `HOLDS`); `PROTOCOL.md:430`
requires a found surface to be corrected to the real path. No sibling
`PROVINCE.md` claims this ground (E9).

## Evidence

| id | fact | pointer |
|---|---|---|
| E1 | The clause to resolve, and the boundary sentence the refinement sits behind | `PROVINCE.md:8-9` "themes/wallpapers as declared files"; `:10-12` config trees READ-ONLY; `:14-16` secrets → kagi; `:18` "Out of province → report, never absorb." File: 18 L, final byte `0x0a`, sha `7aad7b86…` |
| E2 | The path root exists with exactly one symlink; `current` and `current/theme` are real directories (materialized state), `themes/` is empty | `find /home/vgpnk/.config/omarchy -maxdepth 3 -printf '%y %p %l\n'` → dirs `branding current current/theme current/theme/backgrounds extensions hooks hooks/{battery-low,font-set,post-boot,post-update,theme-set}.d themed themes`; `l …/current/background -> …/current/theme/backgrounds/0-ship-at-sea.jpg`; `test -L current` / `current/theme` → REAL; `find themes -mindepth 1 | wc -l` → 0; `~/.config/omarchy/backgrounds` absent; `current/next-theme` absent |
| E3 | Theme state under `current/`: 24 regular parts + 4 backgrounds, `theme.name` one 12 B file | `find current/theme -maxdepth 1 -type f | wc -l` → 24; `…/backgrounds -maxdepth 1 -type f | wc -l` → 4; `stat -c %s current/theme.name` → 12; mtimes `2026-10-03 17:49:02` |
| E4 | Consumers demonstrably name `current/theme` parts (declared edges only) | `~/.config/hypr/hyprland.conf:13`, `hyprlock.conf:1` (and `:10` background path), `~/.config/waybar/style.css:1`, `~/.config/alacritty/alacritty.toml:1`, `~/.config/foot/foot.ini:2`, `~/.config/kitty/kitty.conf:1`, `~/.config/ghostty/config:2`, `~/.config/swayosd/style.css:1`; `~/.config/mako/config` is a symlink to `current/theme/mako.ini`; walker: `~/.config/walker/config.toml:3-4` (`theme = "omarchy-default"`, `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"`) and the checkout theme `omarchy-default/style.css:1` imports `current/theme/walker.css` (cited from `corpus/knowledge/theme-route-r18.md` § Host declaration; not re-read this pass) |
| E5 | The landed gate already reads exactly this tree, so the refinement adds no new measured surface | `tools/mado-verify.sh:3667` `theme_plane()`; rows `theme.chain.{hypr_include,hyprlock,waybar_css,alacritty}`, `theme.chain.mako_link`, `theme.chain.walker_css`, `theme.chain.swayosd_css`, `theme.wallpaper.link`, `theme.parts.declared_only` (function body read at `:3660-3712`); `omarchy_plane()` at `:3343`, hook dirs read presence-only at `:3546-3551`, invocations `:3007`/`:3012` |
| E6 | The out-of-domain entries, by name/type/mode only | `branding/about.txt` 2,734 B 0644; `branding/screensaver.txt` 1,525 B 0644; `extensions/menu.sh` 656 B 0644; `hooks/*` six files — five `*.sample` 0644 and `hooks/post-update.d/install-voxtype.hook` 174 B **0755** (the only executable in the tree, mtime 2026-10-03 17:48:34); `themed/alacritty.toml.tpl.sample` 2,729 B 0644 |
| E7 | No secret-shaped name in the tree; the one `*key*` match is a colour part, not a credential | name-only `find` for `*secret*|*token*|*credential*|*.env|*key*|*passw*` → only `current/theme/keyboard.rgb` (8 B), which the gate classifies in `theme.parts.declared_only` as the asusctl RGB part; no content was read. Secrets stay under `PROVINCE.md:14` |
| E8 | Lane documents this line must agree with | `corpus/knowledge/theme-route-r18.md` (`surface: P5`, host declaration, consumer table, § Unexercised behaviour `[UNK]`); `SCORECARD.md:843-845` maps P5 to "themes/wallpapers"; round-18 w2 `ConnProvinceScope.md` E6/E9 |
| E9 | No sibling lane claims the ground (re-check at HEAD) | `grep -l -i omarchy /home/vgpnk/Projects/shokunin/*/PROVINCE.md` → `mado-shokunin/PROVINCE.md` only. `[INFERENCE]` no contested claim; `MadoR19.ConnProvinceRoster` is producing the authoritative adjacency sweep in parallel |

## In/out split, entry by entry

| entry | class | reason / evidence |
|---|---|---|
| `current/theme.name` | IN — declared state | machine name of the selected theme; gate `theme.name.read` (E5) |
| `current/background` (symlink) | IN — declared state | wallpaper pointer the autostart/hyprlock name; gate `theme.wallpaper.link`; target `0-ship-at-sea.jpg` (E2) |
| `current/theme/**` (24 parts + `backgrounds/`) | IN — declared theme state | rendered/copied theme payload; consumers at E4; gate chain rows (E5) |
| `themes/` (empty) | IN — declared store, presence only | selectable user theme store; empty at E2; no content to own |
| `~/.local/share/omarchy/**` (checkout) | read-only SOURCE evidence | walker theme package import (E4); gate `omarchy_plane()` (E5); no write, no git command |
| `hooks/**` (5 `*.sample`, 1 executable `.hook`) | OUT — report, never absorb | omarchy lifecycle hook bodies; the executable post-update hook is update-triggered behaviour; gate reads only the `*.d` count (E5/E6) |
| `branding/` (`about.txt`, `screensaver.txt`) | OUT | omarchy branding text, not compositor/desktop config craft |
| `extensions/menu.sh` | OUT | omarchy program extension script/behaviour (non-executable data mode, but still a script) |
| `themed/` (`*.tpl.sample`) | OUT | theme template machinery (write-side asset), sample only |
| secret-shaped value anywhere under the root | OUT → kagi | existing `PROVINCE.md:14`; no such name found (E7) |
| theme writes, `omarchy update`, any consumer reload | OUT | `PROVINCE.md:10-12,18`; lane never mutates running state |

## Landing recipe (so the refinement does not become a stale-pin defect)

1. Insert the line and one blank line before the final slogan (`:18`); the file
   then reads 20 L with a trailing newline. Record the new `wc -l` and
   `sha256sum PROVINCE.md` in the landing receipt.
2. Re-point the **present-tense** pins of the old artifact:
   - `SKILL.md:660` — "Pack: `PROVINCE.md` (18 L, sha `7aad7b86…`)"
   - `SKILL.md:741` — "unchanged (18 L, `7aad7b86…`)"
3. The self-audit's measured rows are history, not current pins:
   `corpus/knowledge/province-accuracy-selfaudit.md:12-13`, `:213`, `:295`.
   Append an errata naming the round-19 digest and stating that the `18 L` /
   `7aad7b86…` values are the round-4/5 measured state; never rewrite the audit
   body (round-18 w2 §3.3).
4. `plans/round-5..10-*` record drafts also hold `18 L` / `7aad7b86…`; leave
   them as historical records and never cite them as current.
5. One `LOG.md` entry; a `SCORECARD.md` round-19 non-claim repair note. No
   QUALITY criterion (C1 counts lesson-cited criteria only) and no `S###` row
   (this is host-byte evidence, not a web source; `S096`-`S105` stay reserved).
6. Gate: no change. `grep -n PROVINCE tools/mado-verify.sh` returns only the
   comment at `:21`; `PROVINCE.md` is not a gate input, so no selftest or
   harm-watch re-cut follows.
7. Counters: C1 `18/26 = 6.9231` unchanged; C2 rubric V `6/6` unchanged (P5 is
   already credited and becomes derivable from `PROVINCE.md` alone); C3
   `3/6` unchanged; freshness `2/13` unchanged — `PROVINCE.md` contains zero
   `2.17.0` lines (`grep -c '2\.17\.0' PROVINCE.md` → 0), and the line adds none.

## Risks and unknowns

- **R1 pin drift.** Landing without §2-§3 recreates the M1/R17-V2 class on the
  lane's own boundary document.
- **R2 absorption creep.** Dropping the `mako.ini`/`swayosd.css`/`btop.theme`/
  `neovim.lua` carve-out would silently acquire four consumer planes that have
  no corpus note, no gate rows and no operator grant.
- **R3 over-claim.** The line says *declared* theme state. Whether any consumer
  loads the current bytes stays `[UNK]` (theme-route-r18 § Unexercised
  behaviour); walker's runtime resolution of `current/theme/walker.css` is
  likewise `[UNK]` — the gate checks a declared import only.
- **R4 adjacency.** If the roster sweep finds a sibling claim on this root, the
  OUT column may need lane attribution; secrets are already routed to kagi.
- **R5 executable hook.** `hooks/post-update.d/install-voxtype.hook` is mode
  0755 and update-triggered; the line keeps it out and the lane never runs or
  reads it.

## Limits

- No gate run (neither live nor hermetic) and no omarchy/walker/swaybg/hypr*
  command; no pacman query; no compositor, service or input probe.
- No file content of `~/.config/omarchy/**` was read or printed beyond the
  `theme.name` size; `keyboard.rgb` was classified by name and the gate's
  declared-only list.
- The checkout's `omarchy-default/style.css:1` import is cited, not re-read this
  pass. `PROVINCE.md` was not edited, so no post-landing digest exists yet.
- Sibling adjacency is the round-18 E6 read plus a HEAD re-grep; the
  authoritative sweep is `MadoR19.ConnProvinceRoster`.
