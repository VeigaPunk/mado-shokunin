# ConnProvinceScope — P5 province scope: resolve, don't transfer (round 18, wave 2)

Seat: `MadoR18.ConnProvinceScope` (connector, leaf; no dispatch, no delegation).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Pins by hash, never HEAD:
baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`; integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`; receipts
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`.

Wrote only this report. No tool installed, no fetch, no host probe, no gate run,
no compositor/package/service command, no git/jj write, no write under
`~/.config` or `~/.local/share/omarchy`. No host config tree was read this
item; lane and sibling repository files were read as bytes only.
No line of `PROVINCE.md`, `SKILL.md`, `corpus/` or `tools/` was edited.

## Answer

**The P5 route is inside mado's province in substance; `PROVINCE.md` does need a
refinement line — a resolving one, not a transfer.**

- Not out of province: no sibling `PROVINCE.md` among the 21 lane declarations
  claims the theme plane or the omarchy checkout (E6). The lane already reads
  the theme tree as its own declared surface: the round-4/5 self-audit resolves
  the clause to `~/.config/omarchy/current/**` (E2), the live gate has a `theme`
  plane that reads that tree and its consumer imports (E3), the SCORECARD's own
  C2 text lists it as a `PROVINCE.md` owned surface (E4), and the corpus index
  carries it as a surface route (E5).
- Refinement needed: `PROVINCE.md:8-9` names "themes/wallpapers as declared
  files" with **no path root**, and the P5 note legitimately reads four path
  classes the Owns sentence does not name (E9). Under `PROTOCOL.md:430`
  ("Declared surfaces must resolve") that is a correction the integrator makes
  to the real path — not an absorption of another lane's ground.
- Report-not-absorb applies to the *edges*: package/update state stays
  tsukuroi's (their ADJ-03 retains "package and driver health", E6), and omarchy
  program development/updates and every theme write stay out
  (`SKILL.md:391`, `PROVINCE.md:18`).

Net: the note's P5 credit is valid, but not yet derivable from the boundary
document alone. One appended refinement paragraph makes it derivable and changes
no measured number.

## 1. Evidence (all read at `4c103b5` unless stated)

| id | claim | anchor / output |
|---|---|---|
| E1 | `PROVINCE.md` declares themes/wallpapers with no path root; 18 lines; byte-identical at baseline, integration and working tree | `:6-12` owns list, clause at `:8-9` "themes/wallpapers as declared files"; `:18` "Out of province → report, never absorb"; `sha256sum` = `7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a` at `d9a5a18`, `4c103b5` and the worktree; `git log --oneline -- PROVINCE.md` = one commit (`74d3b7b`, round 0) |
| E2 | The lane's own province audit resolves the same clause to the omarchy theme tree | `corpus/knowledge/province-accuracy-selfaudit.md:52` (C6): "Owns themes/wallpapers as declared files (:8-9)" checked against `current/theme.name`, `current/theme/`, `current/background` → `HOLDS`; `:67-70` lists the theme include among `hyprland.conf`'s 17 sources as `~/.config/omarchy/current/theme/hyprland.conf` |
| E3 | The live gate already has a `theme` plane over that tree and its consumers | `tools/mado-verify.sh` theme-plane comment `:3556-3566`, function `theme_plane()` `:3667`, invoked live at `:3012`; row calls `:3685-3699` check `hyprland.conf:13`, `hyprlock.conf:1`, `waybar/style.css:1`, `alacritty.toml:1`, the mako symlink, walker css, swayosd css and the `current/background` link inside `current/theme/backgrounds/`; `omarchy_plane()` at `:3343` is invoked at `:3007` and reads the checkout (`:65-66` "link into the checkout … worktree == HEAD blob") |
| E4 | The coverage instrument's own declaration maps P5 to the PROVINCE surface | `SCORECARD.md:843-845` (round-17 C2): "PROVINCE.md owned surfaces P1 Hyprland config tree, P2 Waybar, P3 Walker, P4 terminal-emulator configs, P5 themes/wallpapers, P6 screen/idle" |
| E5 | The corpus index already routes the surface | `corpus/README.md:65` row "Themes / wallpapers"; `:67` row "Omarchy documentation, read-only" with limit "do not run mutating probes or edit the upstream skill/checkout" |
| E6 | No sibling claims this ground; sibling headings route desktop work here | `grep -l -i omarchy */PROVINCE.md` → `mado-shokunin/PROVINCE.md` only (21 files searched); `tsukuroi-shokunin/PROVINCE.md:48` ADJ-03 routes "Desktop rendering, bindings, menu or idle behavior" → mado, citing `../mado-shokunin/PROVINCE.md:3-16`, and retains "package and driver health"; `kotoba-shokunin/PROVINCE.md` Adjacent lists "mado (desktop config)"; `kagi-shokunin/PROVINCE.md` has no desktop/theme claim |
| E7 | The protocol makes this a resolving correction, not a negotiation | `PROTOCOL.md:430`: "Declared surfaces must resolve; when a lane finds a surface moved or absent it corrects `PROVINCE.md` to the real path and logs the correction"; `:457-459`: contested scope → integrator refines `PROVINCE.md` and records the ruling; "silence is not a ruling" |
| E8 | Reading the checkout is lane practice, editing it is not | `SKILL.md:212` "reading `~/.local/share/omarchy/**` … reading is safe and encouraged (omarchy skill:41, :58-62)"; `SKILL.md:391` omarchy source development "out of province → report, never absorb (PROVINCE.md:18)" |
| E9 | The P5 note reads four classes the Owns sentence does not name | `corpus/knowledge/theme-route-r18.md` (blob `49d2231f…` at `4c103b5`): `~/.config/omarchy/**` incl. `backgrounds/`, `themes/`, `hooks/theme-set.d/` (`:87`); `~/.local/share/omarchy/{default,themes,bin}` and `.git/{ORIG_HEAD,packed-refs}` (`:32-33`, `:91`); consumer lines in `~/.config/{mako,swayosd,btop,nvim}`; `/var/log/pacman.log:1158` (`:119`). The note keeps behaviour `[UNK]`: "Whether each consumer loads these bytes on this host is `[UNK]`" |
| E10 | Instrument state: P5 credited, P5 is rubric vocabulary, not a PROVINCE token | `python3 .ufo/waves/round-17/measure.py 4c103b5` → `c1` 18/26 = 6.9231, `c2` 6/6 = 10.0, `P5` entry `corpus/knowledge/theme-route-r18.md` sources `S092-S095`; `grep -nE 'P[1-6]' PROVINCE.md` → 0 hits (rc 1), consistent with `ExistingThemeNotes.md` S10 |

## 2. What the P5 note reads, classified

| path class | in `PROVINCE.md` Owns? | already a gate surface? | reading class in the note |
|---|---|---|---|
| `~/.config/omarchy/current/{theme.name,background,theme/}` | yes by clause `:8-9`, no path named (E2) | `theme` plane, `:3685-3699` | declared state |
| `~/.config/omarchy/{themes,backgrounds,hooks/}` | no | no (hooks read by `omarchy` plane only for `*.d` count) | presence/emptiness only |
| `~/.local/share/omarchy/{default,themes,bin}`, `.git/{ORIG_HEAD,packed-refs}` | no | `omarchy` plane reads the checkout (`:65-66`) | read-only source/protocol evidence |
| `~/.config/{hypr,waybar,walker,alacritty}` | yes (`:6-8`) | yes | consumer import lines |
| `~/.config/{mako,swayosd}`, walker theme css | no | yes, `theme` plane rows | evidence-only chain reads |
| `~/.config/{btop,nvim}` | no | no | evidence-only chain reads |
| `/var/log/pacman.log` | no (tsukuroi core, E6) | no | version receipt, not package analysis |

The strict charge available to a non-author is **"undeclared surface"**
(documentation), not "absorbed ground". The note itself matches that charge: it
declares the theme plane, reads consumer declarations, and explicitly refuses to
claim consumer behaviour.

## 3. Proposed move — one bounded refinement paragraph

L1 appends this to `PROVINCE.md` after the `Refuses:` paragraph and before the
final slogan line, changing no existing line:

```
Round-18 refinement (P5 theme/wallpaper route; resolves `:8-9`; no new write
surface, no sibling ground). The declared theme/wallpaper state is the omarchy
theme plane: `~/.config/omarchy/` — state in `current/` (`theme.name`,
`background`, `theme/`), and `themes/`, `backgrounds/`, `hooks/` read for
presence only — plus `~/.local/share/omarchy/` (`{default,themes,bin}` and
checkout identity from `.git/ORIG_HEAD` and `.git/packed-refs`, read as bytes)
as READ-ONLY source/protocol evidence; the gate's landed `theme` and `omarchy`
planes already read the same files. Consumer import or symlink lines outside
the Owns list (`~/.config/{mako,swayosd,btop,nvim}`) are evidence-only chain
reads under this clause, never owned configuration planes and never a
behaviour claim. A `/var/log/pacman.log` line is a version receipt, not
package-state analysis (package/update state stays tsukuroi). Omarchy program
development, updates and every theme write stay out of province — report,
never absorb.
```

This is the sibling-refinement pattern (`tsukuroi` round-12/13/14 paragraphs,
`kagi` round-21 Core/Frontier/Adjacent, `kotoba` round-46 Adjacent) reduced to
what mado's actual contacts require. It deliberately does **not** copy
tsukuroi's seven-row adjacency table: there is no competing owner to arbitrate
(E6), and a table would invent contested scope and a larger pinned surface.

Landing recipe (so the refinement does not become a stale-pin defect):

1. Append the paragraph; record new `wc -l` and `sha256sum PROVINCE.md`.
2. `SKILL.md:660` and `:741` currently assert "PROVINCE.md (18 L,
   `7aad7b86…`)" — re-point the current value and keep the historical pack line
   as history (the M1/R17-V2 class applies to this lane's own prose).
3. `corpus/knowledge/province-accuracy-selfaudit.md:13`, `:213`, `:295` assert
   the same 18 L/`7aad…`; add an append-only errata naming the new digest, never
   rewrite the audit body.
4. One `LOG.md` entry with motivating evidence (`AGENTS.md:3`).
5. Gate: no change. `PROVINCE.md` is not a gate input — `grep -n PROVINCE
   tools/mado-verify.sh` returns only the comment at `:21`, so no selftest or
   harm-watch re-cut follows from the content change.
6. Record the ruling in the round notes (`PROTOCOL.md:457-459`).

## 4. Report-not-absorb edges the refinement must preserve

1. **Package/update state → tsukuroi.** A pacman-log line is a receipt; `-Qu`,
   holds, sync-db provenance and any transaction are not mado's.
2. **Omarchy program development and updates → out.** Source authorship,
   `omarchy update`, packaging and any checkout edit are out (`SKILL.md:391`).
3. **App behaviour → out.** An import line proves a declared edge, never that
   waybar/mako/btop/nvim loaded it; the note's `[UNK]` stands.
4. **The omarchy skill text stays a read-only documentation surface**
   (`PROVINCE.md:10-11`); the checkout is not reclassified as a doc surface, and
   its `.git` metadata is read as bytes, never with a git command.

## 5. Affected axes

| axis | state at `4c103b5` | effect of the move |
|---|---|---|
| C1 calibration | 18/26 = 6.9231 | **unchanged** — the move adds no QUALITY criterion and no lesson row; doing so would be C1 score-seeking, not wave-2 falsification |
| C2 coverage (rubric V) | 6/6 = 10.0, P5 credited via `theme-route-r18.md` S092-S095 | **number unchanged; claim made self-supporting.** P5 credit currently rests on a clause without a path root; after the refinement it is derivable from `PROVINCE.md` alone. Without it, a scope ruling against P5 would drop the axis to 5/6 = 8.3333 (−1.6667) and require a C2 erratum |
| C3 operability | frozen replay `frozen_match` exit 0 (round receipt; not re-run here) | **unchanged** — no gate row reads `PROVINCE.md` |
| harm watch | PASS at `4c103b5` | no config tree, no service, no tool; one documentation-pin re-cut, not a gate re-cut |

Stated plainly: **this move raises no measured score.** It protects C2 against a
falsification-driven loss and closes a boundary-documentation defect. Reporting
it as an axis gain would smooth a contradiction into a scalar.

## 6. Risks and falsifiers

- **R1 pin drift (the defect this round exists to close).** Appending changes the
  sha and line count that three documents pin. Landing the refinement without
  the re-point in §3.2-3.3 recreates the M1/R17-V2 class exactly.
- **R2 absorption creep.** If the paragraph names `mako/swayosd/btop/nvim`
  without "evidence-only, never owned", the lane silently acquires four app
  config planes with no corpus, no gate rows and no operator grant.
- **R3 over-claim.** The resolution rests on the lane's own `[~]` self-audit
  (E2) plus landed gate rows (E3). The refinement must read as "the existing
  clause resolves here", not as a new surface or an observed behaviour.
- **R4 alternative ruling.** If L1 rules P5 out of province, the honest cost is
  C2 5/6 = 8.3333 plus a C2 erratum and a reclassification of the note as
  cross-plane evidence. The evidence above does not support that ruling; if L1
  still wants arbitration, `PROTOCOL.md:457-459` requires the integrator to
  record it — silence must not default the scope.
- **Falsifiers.** A sibling `PROVINCE.md` claiming the theme plane or the
  checkout (none: E6); a gate or corpus rule excluding generated theme state
  (none: E3); or a reading of "declared files" that excludes
  `~/.config/omarchy/current/**` — contradicted by the lane's own C6 audit and
  the landed `theme` rows.

## 7. Commands run (read-only) and output

```
sha256sum PROVINCE.md
  7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a  PROVINCE.md
git show 4c103b55b1ea5c3c555884afe3eb69b5189701b7:PROVINCE.md | sha256sum
  same digest
git show d9a5a18:PROVINCE.md | sha256sum
  same digest
git log --oneline -- PROVINCE.md
  74d3b7b round 0: minted as shonen …
wc -l PROVINCE.md
  18
grep -nE 'P[1-6]' PROVINCE.md
  (no output; rc=1)
grep -l -i omarchy */PROVINCE.md          # run from /home/vgpnk/Projects/shokunin
  mado-shokunin/PROVINCE.md
grep -n "ADJ-03" ../tsukuroi-shokunin/PROVINCE.md
  48
grep -n "Declared surfaces must resolve\|Contested scope" ../PROTOCOL.md
  430 / 457
grep -n "Themes / wallpapers\|Omarchy documentation" corpus/README.md
  65 / 67
grep -n "theme   — declared file chain" tools/mado-verify.sh
  68
grep -n "omarchy_plane$\|theme_plane$" tools/mado-verify.sh
  3007 / 3012 (invocations)
grep -n "plane_omarchy()\|omarchy_plane()\|plane_theme()\|theme_plane()" tools/mado-verify.sh
  3343 (omarchy_plane) / 3667 (theme_plane)
sed -n '3685,3699p' tools/mado-verify.sh
  theme.chain.hypr_include / hyprlock / waybar_css / alacritty / mako_link /
  walker css / swayosd css / theme.wallpaper.link row calls
grep -n "PROVINCE" tools/mado-verify.sh
  21 only (comment; no PROVINCE pin/row)
grep -n "reading is safe and encouraged\|out of province → report, never absorb" SKILL.md
  212 / 391
grep -n "7aad7b86" SKILL.md corpus/knowledge/province-accuracy-selfaudit.md
  SKILL.md:660, :741; self-audit:13, :213, :295
grep -n "^| C6" corpus/knowledge/province-accuracy-selfaudit.md
  52
grep -n "ORIG_HEAD\|packed-refs" corpus/knowledge/theme-route-r18.md
  32-33
git ls-tree -r 4c103b55b1ea5c3c555884afe3eb69b5189701b7 -- corpus/knowledge/theme-route-r18.md
  100644 blob 49d2231fe66d5aaf62c5d16aeebfeb9d7a72d7c9
python3 .ufo/waves/round-17/measure.py 4c103b55b1ea5c3c555884afe3eb69b5189701b7
  c1: criteria 26, lesson_cited 18, score 6.9231
  c2: count 6, score 10.0; P5 = [theme-route-r18.md, sources S092-S095]
sed -n '836,845p' SCORECARD.md
  round-17 C2 text mapping PROVINCE surfaces P1..P6 incl. "P5 themes/wallpapers"
```

`sed`/`grep`/`head` reads only; no mutation of any file outside this report.

## 8. Not done / limits

- No source fetch, no fetch receipts (this item needs none).
- No gate invocation (`--selftest`/`--regression` not required for a
  documentation-scope question).
- No sibling lane was messaged; no claim is made that tsukuroi or kotoba has
  accepted the routing — their declarations were read as bytes only.
- The "inside province" judgement is documentary (`[OBS]` on the anchors,
  `[INF]` on the intent of "declared files"), not an outside-lane ruling. The
  ruling itself belongs to L1 under `PROTOCOL.md:430,457-459`.
