# MadoR19.ProvinceScope — `~/.config/omarchy/**` resolves as the P5 theme plane; refinement landed byte-identical, no lane file edited by this seat

Seat: `MadoR19.ProvinceScope` (scout, leaf; no dispatch). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, baseline `9c54c56`, pre-registration
`17661e0`. Deliverable: `.ufo/waves/round-19/drafts/ProvinceScope-line.md`
(11,303 B; the refinement is one physical line, 924 B, at draft line 19). The
line landed mid-wave at `PROVINCE.md:18` in commit `df84807` — 20 L, sha256
`539a9f6a9f452a82f8ca0fa7700d6824d842957d463e1673ae93a2012f79e8bc`, `cmp`-identical
to the canonical bytes quoted below.

## Verdict

`PROVINCE.md:8-9` ("themes/wallpapers as declared files") has no path root; the
route it already carries resolves to `~/.config/omarchy/**`. The host tree yields
a clean split — theme/background state and its declared consumer parts are mado's
(read-only), while hook bodies, branding, the menu extension, template machinery,
secrets and every omarchy write/update stay out. No sibling lane claims the
ground (roster sweep: all 21 fleet `PROVINCE.md` plus out-of-root `kimi-shokunin`;
zero claims on the omarchy tree, update flows or secrets there). The line changes
no measured number and creates no new write surface.

## The drafted line (draft:19, one physical line, verbatim)

```
**Round-19 refinement (P5 theme/wallpaper route; resolves `:8-9`; no new write surface):** the theme/wallpaper state is the omarchy theme plane under `~/.config/omarchy/**`, read-only — IN: `current/theme.name`, the `current/background` link and `current/theme/**` as declared theme state (the hypr/waybar/walker/terminal consumers are the owned chain; `mako.ini`, `swayosd.css`, `btop.theme` and `neovim.lua` are chain evidence only, their consumer configs not owned), plus `themes/` as the declared selectable store; OUT (report, never absorb): `hooks/**` bodies, `branding/`, `extensions/`, `themed/` template machinery, any secret-shaped value (→ kagi), and every omarchy program update, theme write or consumer reload; `~/.local/share/omarchy/**` (checkout) is read-only source evidence for this chain (gate `theme_plane()`/`omarchy_plane()` in `tools/mado-verify.sh`; route note `corpus/knowledge/theme-route-r18.md`).
```

Insertion point (as landed): after the `Refuses` paragraph, one blank line before
the final slogan — the slogan moved from `:18` to `:20`. The line deliberately
cites function names, not gate line numbers, so the new prose does not create its
own line-pin drift.

## Findings

### 1. The root exists and is materialized state, not a symlink farm

`find /home/vgpnk/.config/omarchy -maxdepth 3 -printf '%y %p %l\n'` (names/types
only) gives seven top-level entries: `branding/`, `current/`, `extensions/`,
`hooks/`, `themed/`, `themes/`, and `current/theme/backgrounds/`. Exactly one
symlink exists in the whole tree:

```
l /home/vgpnk/.config/omarchy/current/background ->
  /home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg
```

`current` and `current/theme` test as REAL directories (not links), consistent
with the theme-set writer's copy-then-swap; `current/theme` holds 24 regular
files, `backgrounds/` four images, `theme.name` is a 12 B file, and
`current/next-theme` is absent (swap completed). `themes/` has zero children;
`~/.config/omarchy/backgrounds` is absent. This matches
`corpus/knowledge/theme-route-r18.md` § Host declaration (24 parts, 4
backgrounds, same target); mtimes are all `2026-10-03 17:49`.

### 2. Declared consumer edges make the theme parts mado's surface

`grep -rn -E 'omarchy/(current|…)'` over the owned config trees (excluding
`*.bak*`) returns:

| consumer | line |
|---|---|
| Hyprland core | `~/.config/hypr/hyprland.conf:13` → `current/theme/hyprland.conf` |
| hyprlock | `hyprlock.conf:1` → `current/theme/hyprlock.conf`; `:10` → `current/background` |
| waybar | `~/.config/waybar/style.css:1` → `../omarchy/current/theme/waybar.css` |
| alacritty / foot / kitty / ghostty | `alacritty.toml:1`, `foot.ini:2`, `kitty.conf:1`, `ghostty/config:2` |
| swayosd | `~/.config/swayosd/style.css:1` → `current/theme/swayosd.css` |
| mako | `~/.config/mako/config` is a symlink → `current/theme/mako.ini` |
| walker | `~/.config/walker/config.toml:3-4` names `omarchy-default` +
`~/.local/share/omarchy/default/walker/themes/`; that package's `style.css:1`
imports `current/theme/walker.css` (cited from `theme-route-r18.md`; not re-read) |

btop and nvim reach the same tree only through symlinks recorded in the route
note; their consumer configs are outside the Owns list, which is why the line
keeps them as evidence-only chain parts rather than owned planes.

### 3. The landed gate already reads this exact tree

`tools/mado-verify.sh:3667` `theme_plane()` reads `current/theme.name`, runs
`theme_chain_row` for hypr/hyprlock/waybar/alacritty, `theme_symlink_row` for the
mako config and `current/background`, `theme_walker_css_row` (resolves walker's
`theme` + `additional_theme_location`, checks the package imports
`current/theme/walker.css`), `theme_swayosd_css_row`, and a
`theme.parts.declared_only` NOTE list (foot, kitty, ghostty, helix,
vscode.json, keyboard.rgb). `omarchy_plane()` at `:3343` reads the checkout
(`version`, skill link/sha) and at `:3546-3551` counts `hooks/*.d` directories —
presence only, never hook bodies. Invocations: `:3007`, `:3012`. So the
refinement documents an already-measured surface; it does not enlarge it.

### 4. Other domains, classified by name/type/mode only (no contents read)

| entry | observed | class |
|---|---|---|
| `branding/about.txt`, `branding/screensaver.txt` | 2,734 B / 1,525 B, 0644 | OUT — omarchy branding text |
| `extensions/menu.sh` | 656 B, 0644 (not executable) | OUT — omarchy program extension script |
| `hooks/*` | five `*.sample` 0644; `hooks/post-update.d/install-voxtype.hook` 174 B **0755**, mtime 17:48:34 | OUT — lifecycle hook bodies; the executable one is update-triggered behaviour |
| `themed/alacritty.toml.tpl.sample` | 2,729 B, 0644 | OUT — template machinery, sample only |
| `current/theme/keyboard.rgb` | 8 B | colour part, name-only match; gate classifies it as the asusctl declared-only part |
| secrets | no credential-shaped name anywhere (`*secret*|*token*|*credential*|*.env|*key*|*passw*`); content never read | OUT → kagi (existing `PROVINCE.md:14`) |

### 5. Boundary and adjacency

- Pre-landing: `PROVINCE.md` hashed
  `7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a` (18 L) at
  `9c54c56`, `17661e0` and the worktree. Post-landing (commit `df84807`):
  20 L, sha256 `539a9f6a9f452a82f8ca0fa7700d6824d842957d463e1673ae93a2012f79e8bc`,
  final byte `0x0a`; `git status --porcelain -- PROVINCE.md` is empty at
  `01b8094`, i.e. the landed bytes are committed.
- `grep -l -i omarchy /home/vgpnk/Projects/shokunin/*/PROVINCE.md` →
  `mado-shokunin/PROVINCE.md` only. Now grounded, not inferred:
  `MadoR19.ConnProvinceRoster` swept all 21 fleet `PROVINCE.md` plus out-of-root
  `kimi-shokunin` (no `PROVINCE.md`) and reports zero sibling claims on
  `~/.config/omarchy` (themes/hooks/branding/scripts), omarchy update flows or
  secrets there; `.config/omarchy` appears only in mado's own files and kotoba
  substrate captures quoting the skill description (report:
  `.ufo/waves/round-19/w1/reports/ConnProvinceRoster.md`).
- `PROTOCOL.md:430` makes this a resolving correction; round-18 w2
  `ConnProvinceScope.md` E6/E9 is the prior read of the same ground. The lane's
  own C6 audit (`corpus/knowledge/province-accuracy-selfaudit.md:52`) already
  resolves the clause to `current/theme.name`, `current/theme/`,
  `current/background`.

### 6. Landing state, pins and counters

- Landed as drafted: 20 L, sha256
  `539a9f6a9f452a82f8ca0fa7700d6824d842957d463e1673ae93a2012f79e8bc`
  (commit `df84807`); the refinement occupies `:18`, the slogan moved to `:20`,
  and the line is byte-identical to the draft (`cmp` clean, 924 B).
- Stale pin text still in the worktree (sibling edits in flight; this seat did
  not touch it): `SKILL.md:666` carries "Pack: `PROVINCE.md` (18 L, sha
  `7aad7b86…`)" in the round-4 pack row, and `SKILL.md:747` carries "unchanged
  (18 L, `7aad7b86…`)" in the round-5 refreshed-pointers block. Both now name a
  superseded artifact; L1 decides re-point vs append-only erratum (the R1 class).
- Historical, not current: `corpus/knowledge/province-accuracy-selfaudit.md:12-13`,
  `:213`, `:295` (add an append-only errata, never rewrite the audit body), and
  `plans/round-5..10-*` (ten `7aad7b86…` hits; leave as records).
- Gate: no change — `grep -n PROVINCE tools/mado-verify.sh` returns only the
  comment at `:21`.
- Counters: C1 `18/26 = 6.9231`, C2 rubric V `6/6`, C3 `3/6`, freshness `2/13`
  all unchanged. `PROVINCE.md` has zero `2.17.0` lines
  (`grep -c '2\.17\.0' PROVINCE.md` → 0), so the line adds none and does not
  enter the freshness denominator.

## Limits

- No gate run (live or hermetic), no omarchy/walker/swaybg/hyprctl/pacman
  command, no compositor, service or input probe; host files read as bytes only.
- No content of `~/.config/omarchy/**` was read or printed beyond `theme.name`
  size and the mode/size census above; `keyboard.rgb` was classified by name and
  the gate's declared-only list.
- The checkout's `omarchy-default/style.css:1` import is cited from
  `theme-route-r18.md`, not re-read this pass; walker's runtime resolution of
  `current/theme/walker.css` and every consumer's loading of current bytes stay
  `[UNK]`.
- No web source opened, so no fetch receipts are owed. This seat did not edit
  `PROVINCE.md`; the landing (commit `df84807`) was L1's, verified here by
  `wc -l`/`sha256sum`/`cmp` only.
- Adjacency is now the roster's grounded sweep
  (`.ufo/waves/round-19/w1/reports/ConnProvinceRoster.md`), not only the
  round-18 E6 read; this seat did not re-run that sweep.

## Installs

none
