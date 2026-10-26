# Matrix — staged rows (shokuknow merge/mado) vs lane registry (mado-shokunin corpus/SOURCES.md)

Seat ConnStagedVsRegistry, round 44 w1. All locators below were produced by `grep -n`
in this session (commands recorded inline); none are typed. Freeze: registration.md
commit e2289516a9a857f55cda7be635933e89b931c3da, base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f.

Inputs:
- Staged append: `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` (147 rows, ids S203–S349)
- Lane registry: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` (234 rows, tops S297)
- Residue: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/gkeep-*.md`, `glyph-and-geometry-r31.md` (10 files + the round-43-admitted `gkeep-size-to-real-size-r11.md`)
- Renumber map: `.ufo/waves/round-44/assimilation/renumber-map.tsv` (2 rows)
- Collision/quarantine: `.ufo/waves/round-44/assimilation/collisions` (42 ids), `quarantine-slice` (13 rows)

## A. Per-row verdicts — every staged id cited by the residue files

Command that extracted the citations:
`cd /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge && grep -nE '^source:|^Cites:' gkeep-*.md glyph-and-geometry-r31.md`
(26 distinct staged ids cited across 10 residue files; r11-admitted file included for completeness.)

Legend: SAME-DOC = staged row and the lane row it maps to are the same document
(tag/commit alias or excerpt/full extent); NONE = no lane row holds that document;
COLLISION = the staged id number equals a lane row number but the documents differ.

| residue file | staged id | staged document (source column) | lane verdict |
|---|---|---|---|
| gkeep-client-size-request-r12.md | S311 | Window.cpp § sendWindowSize, raw URL `/v0.56.2/` tag form | SAME-DOC → held S164 (`corpus/SOURCES.md:176`), commit form; hash-verified (see B1). Renumber row 2. |
| gkeep-client-size-request-r12.md | S312 | gkeep ui.py full file, raw URL @133b867 | SAME-DOC → new row S301 provisional (lane holds only excerpt S297); hash-verified (B2). Renumber row 3. |
| gkeep-rendered-geometry-chain-r9.md | S284 | Window.cpp § fetchClass, tag form | SAME-DOC as S164 by commit; COLLISION — lane S284 is FocusGrab.cpp (`:233`, B3) |
| gkeep-rendered-geometry-chain-r9.md | S285 | gkeep ui.py full file | SAME-DOC as S297-excerpt/S301; COLLISION — lane S285 is quickshell grab.cpp |
| gkeep-rendered-geometry-chain-r9.md | S286 | GTK4 docs set_default_size | NONE — 0 lane rows for docs.gtk.org |
| gkeep-rendered-geometry-chain-r9.md | S287 | wiki.hypr.land 0.56.0 Window-Rules | NONE — lane holds S017 (current), S023 (0.54.0), S030 (rejected dup), S045 (correction); no 0.56.0 page row |
| gkeep-rendered-geometry-chain-r9.md | S292 | lanes/mado/round9/fetch/gkeep-geometry-chain.txt (private) | NONE; COLLISION — lane S292 is Target.cpp |
| gkeep-rendered-geometry-chain-r9.md | S293 | lanes/mado/round9/fetch/host-compositor-log-scan.txt (private) | NONE; COLLISION — lane S293 is WindowTarget.cpp |
| gkeep-rendered-geometry-record-r13.md | S318 | Window.cpp § onAck, tag form | SAME-DOC as S164 by commit; no number collision (S318 > S297) |
| gkeep-rendered-geometry-record-r13.md | S319 | Window.cpp § map-request log, tag form | SAME-DOC as S164 by commit; no collision |
| gkeep-rendered-geometry-record-r13.md | S320 | lanes/mado/round13/fetch/host-journal-map-log-sweep.txt (private) | NONE |
| gkeep-rendered-geometry-record-r14.md | S326 | lanes/mado/round14/fetch/host-journal-map-log-alltime-sweep.txt (private) | NONE |
| gkeep-geometry-never-recorded-r15.md | S339 | lanes/mado/round15/fetch/corpus-round24-artifacts-sweep.txt (private) | NONE |
| gkeep-element-rules-r30.md | S251 | host file ~/.config/hypr/gkeep.conf | NONE as a content row (lane S014 pins presence only, per registration); no number collision |
| glyph-and-geometry-r31.md | S255 | gkeep ui.py full file | SAME-DOC as S297-excerpt/S301; no collision (lane has no S255) |
| glyph-and-geometry-r31.md | S256 | nerd-fonts v3.5.1 glyphnames.json | NONE; no collision (lane has no S256) |
| gkeep-geometry-unobservable-r8.md | S275 | lanes/mado/round8/fetch/host-focus-grab-and-timeout.txt (private) | NONE; no collision (lane has no S275) |
| gkeep-size-rule-application-r10.md | S297 | WindowRuleApplicator.cpp, tag form | SAME-DOC as lane S155 (`:167`) by commit; COLLISION — lane S297 is the ui.py excerpt (`:246`) |
| gkeep-size-rule-application-r10.md | S298 | Window.cpp § initial-commit read, tag form | SAME-DOC as S164 by commit; no collision |
| gkeep-size-rule-application-r10.md | S299 | lanes/mado/round10/fetch/host-r4-observation-sweep.txt (private) | NONE |
| gkeep-observation-route-r11.md | S310 | lanes/mado/round11/fetch/host-gkeep-rule-and-path.txt (private) | NONE |
| gkeep-size-to-real-size-r11.md (admitted r43) | S302 | DefaultFloatingAlgorithm.cpp, tag form | SAME-DOC as lane S291 (`:240`); admitted already |
| gkeep-size-to-real-size-r11.md | S303 | Target.cpp, tag form | SAME-DOC as lane S292 (`:241`) |
| gkeep-size-to-real-size-r11.md | S304 | WindowTarget.cpp, tag form | SAME-DOC as lane S293 (`:242`) |
| gkeep-size-to-real-size-r11.md | S305 | GeometricMovableAnimated.cpp, tag form | SAME-DOC as lane S294 (`:243`) |
| gkeep-size-to-real-size-r11.md | S310 | (same private row as above) | NONE |

Tally: 26 cited ids → SAME-DOC 15 (all Hyprland code rows resolve to lane commit-form
rows S155/S164/S291–S294, and the ui.py rows to S297-excerpt/S301), NONE 11 (2 public
docs/dataset URLs + 9 private/host receipts), COLLISION 7 (S284, S285, S286, S287,
S292, S293, S297 — same number in both registries, different document).

## B. Evidence — grep outputs (locators computed this session)

### B1. S311 → S164 is by document, hash-verified
Command: `grep -nE '^\| S164 ' corpus/SOURCES.md | cut -c1-450`
```
176:| S164 | Hyprland v0.56.2 CWindow implementation — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp | code | A | ... | src/desktop/view/Window.cpp:103-108,... @ commit efb50993780079460b0cbed1363e2166a2de1d9f, sha256:d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded, 124226 B | ... | corpus/knowledge/rule-attribution-r24.md |
```
Command: `cat .ufo/waves/round-44/receipts/fetch-sha256.txt` (line 2 + urls block)
```
d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded 124226 fetch/Hyprland-Window.cpp
fetch/Hyprland-Window.cpp https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp
```
Staged S311 (SOURCES.append.md) cites the tag form `…/v0.56.2/src/desktop/view/Window.cpp` and states
"commit efb5099". Registration freeze: host v0.56.2-4 == commit efb50993780079460b0cbed1363e2166a2de1d9f.
Same bytes: d735d454 == d735d454. Verdict: same document; anchor form differs (tag vs commit hash).

### B2. S312 → S301 is by document, hash-verified
Lane S297 (`grep -nE '^\| S297 ' corpus/SOURCES.md`, line 246):
```
| S297 | gkeep client window request - the app's own size (read-only excerpt, gkeep 133b867) - .ufo/waves/round-43/fetch/gkeep-ui-excerpt.py | own-work | A | ... | excerpt of ~/Projects/gkeep/gkeep/ui.py:446-488 (end of file) at gkeep HEAD 133b86717a02548aeaff3f1411bf301d936c5308, 1625 B sha256:3695b788...; full-file sha256:07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a | ...
```
Fetch receipt line 5: `07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a 14639 fetch/gkeep-ui.py`, url =
`https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py`.
Lane holds only the 446–488 excerpt (S297); S312 is the full file at the same commit → new row, not a held-row
extension. Verdict: same document, different extent; hash-verified.

### B3. The 7 number collisions cited by the residue (same id, different document)
Commands: `for id in S284 S285 S286 S287 S292 S293 S297; do grep -E "^\| $id " corpus/SOURCES.md; done` vs the
same loop on SOURCES.append.md. Lane side (line numbers from `grep -nE '^\| S(155|284|285|286|287|292|293|297) ' corpus/SOURCES.md`):
```
S284 (lane :233) → FocusGrab.cpp            @ efb5099  (staged S284 → Window.cpp       @ v0.56.2 tag)
S285 (lane :234) → quickshell grab.cpp      @ 9b0f339b  (staged S285 → gkeep ui.py     @ 133b867)
S286 (lane :235) → xdg-desktop-portal-hyprland PortalManager.cpp @ v1.4.1 (staged S286 → docs.gtk.org set_default_size)
S287 (lane :236) → github.com/hyprwm/Hyprland/issues/565          (staged S287 → wiki.hypr.land/0.56.0 Window-Rules)
S292 (lane :241) → layout/target/Target.cpp @ efb5099  (staged S292 → lanes/mado/round9/fetch/gkeep-geometry-chain.txt)
S293 (lane :242) → layout/target/WindowTarget.cpp @ efb5099 (staged S293 → lanes/mado/round9/fetch/host-compositor-log-scan.txt)
S297 (lane :246) → gkeep ui.py excerpt (own-work)      (staged S297 → WindowRuleApplicator.cpp @ v0.56.2 tag)
```
Collision universe: `.ufo/waves/round-44/assimilation/collisions` (42 ids: S203–S221, S253, S258, S277–S297);
`id-guard.md` records reg-ids 234, staged-ids 147, collisions 42.

### B4. Anchor/tag-form census
Commands:
- `grep -cE 'raw\.githubusercontent\.com/hyprwm/Hyprland/v0\.56\.2' corpus/SOURCES.md` → `0`
- `grep -c 'efb50993780079460b0cbed1363e2166a2de1d9f' corpus/SOURCES.md` → `35`
- lane tag-form precedent: `grep -n 'HyprCtl' corpus/SOURCES.md` → line 30 (S018, `blob/v0.56.2/src/debug/HyprCtl.cpp`, "tag commit efb5099378007946…") and line 170 (S158, `raw/efb5099…/src/debug/HyprCtl.cpp`) — same document+commit, two URL forms, both active.

### B5. Duplicate-URL screen for the four provisional new rows (S298–S301 pins)
Commands and counts against `corpus/SOURCES.md`:
- `grep -cE 'XDGShell\.cpp'` → 0
- `grep -cE 'xdg-shell\.xml'` → 0 (nearest: S048 line 60, colour-management-v1.xml @1.49 staging — different path)
- `grep -cE 'gdktoplevel'` → 0; `grep -c '4\.24'` → 0
- `grep -cE 'raw\.githubusercontent\.com/VeigaPunk'` → 0 (all gkeep URL forms: `grep -cE 'VeigaPunk/gkeep'` → 0)
- `grep -cE 'desktop/view/Window\.cpp'` → 1 (S164 only; the pin reuses this URL exactly → correctly held, not re-opened)
- screen basis: `corpus/QUALITY.md:34` — "screen repeated canonical URLs across active rows even when scope wording differs";
  S030 precedent (`grep -n 'S030 duplicated' corpus/SOURCES.md` → line 324: S030 duplicated S017's URL, rejected in place).
  The screen is string-equality: the tag/commit alias pairs (B4) pass it.

### B6. Tier census of the 26 cited staged ids
Command: `for id in S251 S255 S256 S275 S284 S285 S286 S287 S292 S293 S297 S298 S299 S302 S303 S304 S305 S310 S311 S312 S318 S319 S320 S326 S339; do grep -E "^\| $id " SOURCES.append.md | awk -F'|' '{print $4}'; done`
→ code ×14, docs ×2 (S286, S287), dataset ×1 (S256), own-work ×9. Tier B/C/community: 0.
(Staged append does contain tier-C rows — S210, S211, S216, S217, S230, S244, S348 — none cited by gkeep residue.)

### B7. Private receipts
- Lane: S297 source is `.ufo/waves/round-43/fetch/gkeep-ui-excerpt.py` (lane-private; records excerpt sha256 +
  full-file sha256).
- Staged, cited by residue: S275, S292, S293, S299, S310, S320, S326, S339 — all `lanes/mado/roundN/fetch/*.txt`
  (package-private); S251 — host file `/home/vgpnk/.config/hypr/gkeep.conf`.
- Round-44 pins are lane-private `.ufo/waves/round-44/fetch/*` with the public URL recorded per pin in
  `receipts/fetch-sha256.txt`; the C2 entry should cite the pins, not the staged receipts.

### B8. renumber-map.tsv — mappings by document?
File (3 lines incl. header), both rows name the same document on both sides and give the document-identity
reason in `note`; no row maps by id. Coverage: exactly the C2 predecessor's two citations — sufficient for
C2 scope; the unmapped colliding ids (B3) are outside r12 and must not be resolved by number.

## C. Risks

- R1: string-equality URL dedup (QUALITY.md:34) misses tag/commit aliases; document-aware screening (commit
  resolution or sha256) is required, as applied in the renumber map.
- R2: 7 residue-cited staged ids collide with different lane rows (B3); number-based lookup of staged citations
  in the lane registry yields the wrong document for each.
- R3: staged S287 (wiki.hypr.land 0.56.0 Window-Rules) and S286 (GTK docs) are genuinely unheld; if the r9
  citations are ever assimilated, two new rows are needed (no duplicate-URL conflict today).

## D. What this supports

- C2 assimilation: the r12 predecessor's citations map cleanly (S311→S164, S312→S301, both by document,
  hash-verified); the four provisional new rows add zero duplicate URLs; the staged private receipts must not
  be cited in the entry.
- Round-43 closure D1/D2 context: the collision/quarantine files back the id-guard proof.
