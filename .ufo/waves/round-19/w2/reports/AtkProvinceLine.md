# MadoR19.AtkProvinceLine — partial

Attack on the round-19 `PROVINCE.md` refinement at tip `01b80946d92b26370d3012a7da655d00dd135154`
(`git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d 01b80946… -- PROVINCE.md`
→ `2 insertions(+)`, one blank line at `:17` and one 929-byte physical line at `:18`).

Verdict scope: the two questions I was assigned **hold** — no sibling `PROVINCE.md`
claims any IN item, and the line does not absorb `hooks/`, `branding/` or
secret-shaped material. The line is **partial** because one IN item is misdescribed
against host bytes (`themes/`), and because landing it left two present-tense
`SKILL.md` claims stale that wave-1 itself listed as owed re-points.

## Observed facts

### 1. Sibling ownership of IN items — none

Read `/home/vgpnk/Projects/shokunin/MANIFEST.json` and all 21
`/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md`. Keyword sweep for
`omarchy|hypr|waybar|walker|wallpaper|backgrounds?/|theme\.name|chromium\.theme|vscode\.json|keyboard\.rgb`
over the 21 sibling files (mado excluded) returned **0 matches**. A second sweep
(`for f in */PROVINCE.md; do grep -c -i omarchy "$f"; done`) returns
`mado-shokunin/PROVINCE.md 2` and nothing else. The nearest neighbours are on the
OUT side of the line, not the IN side:

- `tsukuroi-shokunin/SKILL.md:47,50,108` etc. — the `[omarchy]` pacman repo,
  `omarchy-walker` package, update-safety; matches the line's OUT
  "every omarchy program update".
- `kagi-shokunin/PROVINCE.md` — secret custody; matches the line's
  "any secret-shaped value (→ kagi)".
- `tabi-shokunin/PROVINCE.md:8-13` — browser/CDP surfaces; `current/theme/chromium.theme`
  is a theme payload file, not a tabi surface.

[OBS] No sibling owns `themes/`, `current/` or `backgrounds`.
[UNK] `MANIFEST.json`'s `roster[]` lists 13 lanes and does not list mado at all,
so it is not a usable ownership index; the PROVINCE sweep is the operative check.

### 2. Absorption of hooks / branding / secret-shaped material — none

`find /home/vgpnk/.config/omarchy -maxdepth 3 -printf '%y %p\n'`:

```
d .../branding      d .../current   d .../extensions   d .../hooks
d .../themed        d .../themes    d .../current/theme d .../current/theme/backgrounds
l .../current/background -> /home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg
```

- `hooks/**`, `branding/`, `extensions/`, `themed/` all exist and all appear only
  in the line's OUT clause. The gate touches `hooks` as a directory count only
  (`tools/mado-verify.sh:3858-3862` at tip: `find "$hooks" -mindepth 1 -maxdepth 1 -type d -name '*.d'`),
  matching "OUT … `hooks/**` bodies".
- IN set `current/theme/**` = 28 files (24 at depth 1 + 4 backgrounds). No
  secret-shaped filename; `grep -cE 'secret|token|password|api[_-]?key'` over
  `current/theme/*` → 0 for every file. Values were never printed.
- `current/theme/backgrounds/omarchy.png` is a 3840x2160 PNG whose sha256
  `63d002b2…` equals `~/.local/share/omarchy/themes/matte-black/backgrounds/omarchy.png`
  — theme payload, not the two `branding/*.txt` files.
- The sole symlink in the plane, `current/background`, resolves **inside** the IN
  set (`…/current/theme/backgrounds/0-ship-at-sea.jpg`), so the link absorbs nothing
  outside the declared plane.

### 3. Every IN/OUT path exists; one is empty

`for p in current/theme.name current/background current/theme themes hooks branding extensions themed; do [ -e "$p" ] …`
→ all 8 `EXISTS`. `find themes -mindepth 1 -maxdepth 1 | wc -l` → **0**;
`find /home/vgpnk/.local/share/omarchy/themes -mindepth 1 -maxdepth 1 -type d | wc -l` → **19**.

### 4. The overclaim: `themes/` is called "the declared selectable store"

The line (`PROVINCE.md:18`) reads "…plus `themes/` as the declared selectable store".
Host bytes:

- `~/.config/omarchy/themes/` — **0 entries**. Lane's own note already says so:
  `corpus/knowledge/theme-wallpaper-plane.md:238` "`~/.config/omarchy/themes/` — **0 entries**
  (no user themes), re-measured", and wave-1 measured it too:
  `.ufo/waves/round-19/w1/reports/ProvinceScope.md:45` "`themes/` has zero children".
- The populated selectable inventory is the checkout store the same line puts OUT:
  `/home/vgpnk/.local/share/omarchy/themes/` = 19 theme dirs. `bin/omarchy-theme-set:14-15,19-22`
  (`USER_THEMES_PATH` / `OMARCHY_THEMES_PATH`; refuses a name absent from either) and
  `bin/omarchy-theme-list:7-8` (lists **both** stores; line 8 is the populated one).
- The live selection came from the OUT half, not the IN half: `theme.name` matches
  `matte-black` (`grep -qxF` over the 19 checkout names → `MATCH matte-black`);
  `current/theme/colors.toml` sha `dbdd13a6…` equals
  `~/.local/share/omarchy/themes/matte-black/colors.toml`; all four
  `current/theme/backgrounds/*` digests equal the checkout payload (sorted-sha `diff`
  shows live-only template files, no differing or checkout-only file).
- The cited gate has no row for this IN item: `git show 01b80946…:tools/mado-verify.sh | grep -nE 'omarchy/themes|/themes'`
  → only `.local/share/omarchy/default/walker/themes` (walker's own theme dir, lines 276/350/373/1124).
  `theme_plane()` (`:3979-4024` at tip) reads `theme.name`, four `theme_chain_row`s,
  the mako symlink, `walker`/`swayosd` css rows, the wallpaper link and a
  `parts.declared_only` NOTE — never `~/.config/omarchy/themes/`.

So the clause is not fabricated (the dir *is* a user-theme location omarchy scans),
but "the declared selectable store" overstates an empty directory and omits that the
only selectable themes — and the live one — live in the checkout path the line marks
OUT. Wave-1's report never checked the 19-theme checkout store; it recorded the empty
IN dir and still wrote the definite-article claim. [INFERENCE] A reader of the line
would look for selectable themes in the wrong place.

### 5. Landing collateral: two present-tense `SKILL.md` claims are now false

`PROVINCE.md` went 18 L / `7aad7b86…` → **20 L / `539a9f6a…`**. At the same tip:

- `SKILL.md:666`: "Pack: `PROVINCE.md` (18 L, sha `7aad7b86…`)" — false at HEAD.
- `SKILL.md:747`: "unchanged (18 L, `7aad7b86…`)" — false at HEAD.
- `SKILL.md:391` cites `PROVINCE.md:18` for the closing "out of province → report,
  never absorb"; after the insert, `:18` is the refinement and the slogan moved to `:20`.

Wave-1 explicitly listed the fix as owed: `ProvinceScope.md:114` "Present-tense pins to
re-point: `SKILL.md:660` … and `SKILL.md:741`". The integration commit
`df84807` added 15 SKILL.md lines and did not re-point either pin or the `:18` citation
(`git grep '7aad7b86' 01b80946… -- SKILL.md` still returns 666/747; `grep -n '539a9f6a\|20 L'`
over SKILL.md at tip → no hits). This is a stale-claim defect created by the landing,
on ground the wave-1 report already measured.

Minor receipt mismatch: `ProvinceScope.md:6` calls the line "924 B"; the physical line
is 925 chars / 929 bytes incl. newline (`wc -mc`), sha `8817dc0f…` for both draft line 16
and committed line 18 — draft and landed are byte-identical, so only the count is off.

### 6. What holds (honest agreement after trying to break it)

- Consumer chain "owned" claim verified at file bytes: `~/.config/hypr/hyprland.conf:13`
  → `current/theme/hyprland.conf`; `hyprlock.conf:1` and `:10`; `waybar/style.css:1`
  (`../omarchy/current/theme/waybar.css`); `alacritty.toml:1`; `foot.ini:2`; `kitty.conf:1`;
  `ghostty/config:2`; `swayosd/style.css:1`; mako config is a symlink into the theme;
  walker `config.toml:3-4` + `default/walker/themes/omarchy-default/style.css:1`
  `@import "…/.config/omarchy/current/theme/walker.css"`.
- "mako.ini / swayosd.css / btop.theme / neovim.lua … consumer configs not owned":
  none of those consumer paths is in the primary Owns list (`PROVINCE.md:6-9`).
- Checkout OUT claim: `~/.local/share/omarchy/version` = `3.8.3` = `OMARCHY_VERSION_PIN`
  (`tools/mado-verify.sh:3595`); `~/.agents/skills/omarchy` →
  `…/default/omarchy-skill` = `OMARCHY_SKILL_LINK_TARGET`; leaf sha `becd149e…` =
  `OMARCHY_SKILL_SHA_PIN` (`:3598-3599`).
- "no new write surface": true trivially — `PROVINCE.md:11-12` already declares every
  config tree read-only; the line adds reads only.
- Draft/landed identity: sha `8817dc0f423d384f9d2a2e9e29ee09cc8b73ba692ecaa1ab166e48ff1e0caf48`.

## Remaining unknowns

- `[UNK]` whether the operator will populate `~/.config/omarchy/themes/`; today it is
  unreachable as a store (0 themes), so the IN clause carries no measurable surface.
- `[UNK]` `~/.config/omarchy/backgrounds/<theme>/` (read by `bin/omarchy-theme-bg-next:8`)
  is **absent** on this host and is named in neither the IN nor the OUT list. No current
  contradiction — a background plane the line does not enumerate, should it appear.
- `[UNK]` rendered wallpaper/consumer behaviour (not observed; host pause).

## Limits

No gate or copy of the gate executed; no `omarchy-*` binary, compositor, package,
service or screenshot operation. Host files read as bytes (`find`, `readlink`, `stat`,
`sha256sum`, `grep -c`, `file`); under `~/.config/omarchy` no hook/extension bodies were
printed, `theme.name` was matched with `grep -qxF` rather than printed, and theme-part
content was only counted against secret-shaped patterns (all zero matches).

## Installs

none
