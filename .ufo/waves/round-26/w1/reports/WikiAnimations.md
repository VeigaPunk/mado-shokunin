# Wiki Animations source opening

## Finding

At the requested wiki pin `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`, the raw tree locates the Animations page at `content/configuring/core/animations.md` (lowercase, under `core`). That page is Lua-era documentation: it says animations use `hl.animation()` and gives a Lua table syntax, not `animation = NAME, ONOFF, SPEED, CURVE[, STYLE]`. The pinned tree lists `animations.md` as 6066 bytes; the saved page has 162 lines.

The hyprlang page is absent at the pin. The page-history view shows the April 26, 2026 commit `e99eac80a63d68e050623af2f69629f9423befdb` changed the old directive to Lua; its parent, `ecc06f3b6605e453c0ad533d979fccbefff788ef` (April 20, 2026), is the newest wiki commit snapshot still containing the legacy grammar. The edit history lists `c4dfbc2808fb915246739632dd2d99b7bbe1976b` (November 1, 2025) as the preceding page-specific revision. The source opened for legacy syntax is the page at the April 20 parent commit. At the requested pin, the exact current path is Lua-era; the old page path no longer exists.

The pinned page also documents a hierarchical animation tree, inheritance of unset entries, and Lua style syntax. This is current wiki documentation, not evidence of Hyprland v0.56.2 runtime behavior. The historical page is documentation evidence for the old hyprlang grammar and style vocabulary only.

## Source files and provenance

- Pinned page: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/animations.md`; saved as `.ufo/waves/round-26/fetch/WikiAnimations.bin`. SHA-256 `b0d11943144532f7950b3236da3dd62938571b0d311664a53407279846285344`; 6066 bytes, 162 lines. Useful anchors: `content/configuring/core/animations.md:8-18,30-40,56-60,143-161` at the pin.
- Legacy page: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Animations.md`; saved as `.ufo/waves/round-26/fetch/WikiAnimations-legacy.bin`. SHA-256 `f30f6bf44052e87b803a640750d5cb8c3295616a8508303a2280560a5964120b`; 4023 bytes, 115 lines. Full commit: `ecc06f3b6605e453c0ad533d979fccbefff788ef`.
- The pinned source URL and the legacy source URL were searched in `corpus/SOURCES.md`; neither is already a row. A draft row is below; it was not added to the registry.

## Located quotations

The following four quotes are copied from the saved legacy bytes. A Python check confirmed each quote, after whitespace collapse, is a substring of the whitespace-collapsed decoded source and of the cited line span; each is at most 25 words.

1. `content/Configuring/Animations.md:11` — “animation = NAME, ONOFF, SPEED, CURVE [,STYLE]”
   This gives the ordered hyprlang directive fields and optional style field.
2. `content/Configuring/Animations.md:23-24` — “The animations are a tree. If an animation is unset, it will inherit its parent's values.”
   This states that unset animation values inherit from their parent.
3. `content/Configuring/Animations.md:38` — “↳ windows - styles: slide, popin, gnomed”
   This lists the style choices documented for the `windows` tree node.
4. `content/Configuring/Animations.md:114` — “animation = windows, 1, 8, default, slide left”
   This shows the optional style field using `slide left` for a windows animation.

## Draft SOURCES row

| S? | Hyprland Wiki Animations — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Animations.md | docs | A | Hyprlang-era animation directive grammar, inherited animation tree, and styles; historical documentation only | content/Configuring/Animations.md:8-12,23-24,34-39,94-115 @ ecc06f3b6605e453c0ad533d979fccbefff788ef, sha256:f30f6bf44052e87b803a640750d5cb8c3295616a8508303a2280560a5964120b, 4023 B | Documents the animation keyword fields, optional style, inheritance tree, node styles, and style modifiers | mined | 2026-10-23 | on-release | corpus/knowledge/animation-table-r26.md |

## Commands and outcomes

The source-save commands were:

```sh
timeout 30 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/animations.md -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/WikiAnimations.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/WikiAnimations.bin && wc -c -l /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/WikiAnimations.bin
```

Output: `b0d11943144532f7950b3236da3dd62938571b0d311664a53407279846285344` and `162 6066` (lines, bytes).

```sh
timeout 30 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Animations.md -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/WikiAnimations-legacy.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/WikiAnimations-legacy.bin && wc -c -l /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/WikiAnimations-legacy.bin
```

Output: `f30f6bf44052e87b803a640750d5cb8c3295616a8508303a2280560a5964120b` and `115 4023` (lines, bytes).

Quote check:

```sh
timeout 30 prlimit --as=4000000000 -- python3 -I -c 'import pathlib,re; p=pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/WikiAnimations-legacy.bin"); text=p.read_bytes().decode("utf-8"); norm=lambda s: re.sub(r"\s+", " ", s).strip(); quotes=[("animation = NAME, ONOFF, SPEED, CURVE [,STYLE]",11,11),("The animations are a tree. If an animation is unset, it will inherit its parent\x27s values.",23,24),("↳ windows - styles: slide, popin, gnomed",38,38),("animation = windows, 1, 8, default, slide left",114,114)]; assert all(len(q.split()) <= 25 and norm(q) in norm(text) and norm(q) in norm("\n".join(text.splitlines()[a-1:b])) for q,a,b in quotes); print("verified 4 whitespace-collapsed quotes at lines 11, 23-24, 38, 114; each <=25 words")'
```

Output: `verified 4 whitespace-collapsed quotes at lines 11, 23-24, 38, 114; each <=25 words`.

Raw URL probes through the read tool returned HTTP 404 for the following attempted locations; they were path-discovery probes, not saved source files:

- `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/Configuring/Animations.md`
- `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/animations.md`
- `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/263edbb1cc1e/content/Configuring/Animations.md` (an exploratory pre-restructure path probe; the selected legacy source is instead at the April 20 parent commit listed above).

The raw-tree lookup at the pin found `content/configuring/core/animations.md`. The historical commit tree lookup at `ecc06f3b6605` found `content/Configuring/Animations.md` (4023 bytes). The current `main` history page identified `c66e8de21f5ecdc4bc5e278e7d94800ea10957af` as its October 22, 2026 tip when checked.

## Surfaces and limits

Touched only this report and the two named fetch artifacts. No product code, counter, harness, or `corpus/SOURCES.md` was edited; no control/counter or Hyprland runtime was run; no tool was installed. The draft SOURCES row is not a committed registry change. The historical wiki text does not establish behavior for a particular installed Hyprland version.

Report: .ufo/waves/round-26/w1/reports/WikiAnimations.md