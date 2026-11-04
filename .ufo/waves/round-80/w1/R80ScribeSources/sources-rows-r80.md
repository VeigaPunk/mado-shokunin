# SOURCES.md rows — round 80 (seat R80ScribeSources)

Prose draft for the L1 append. Freeze `6c302a53eb8f577e83fbcadc01e05a286778df8e`, base
`e10f7e9f528b13195a1cdde28a68a702af3045c4`. Six rows, exact 11-column schema, no literal
`|` inside a cell. Bytes verified against `.ufo/waves/round-80/fetch/sha256-r80.txt`
(`sha256sum -c` 5/5 OK) and against each file's own line numbers.

Note for the L1: the registry already carries S470–S475 at `corpus/SOURCES.md:421-426`
(written 08:39, before this seat settled). §3 is the cell-by-cell delta, not a silent second
copy; §1 is the row prose this seat stands behind.

## 1. The six rows

S470

| S470 | Hyprland v0.56.2 — src/render/Renderer.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/render/Renderer.cpp | code | A | mado layer plane: more than one exclusive layer surface composes — the arrangement order, the running usable box each surface is placed against, and the edge each zone is attributed to (round-80 C1); repeats S457's URL at this separate scope | `applyExclusive` :2529-2586, `arrangeLayerArray` :2587-2671, `arrangeLayersForMonitor` :2673-2700 @ efb5099 (fetched 2026-11-04, sha256 `9af8a74e7dc42ba3c5532303b9bb4ee7c350d4cef2f2c8984e41f2a01b3bdd22`, 143211 B; byte-identical to S457's round-78 pin, the two rows differ in scope only) | every level is arranged in order against one running usable box; an empty arranged box is skipped (:2655-2658); `applyExclusive` walks top, bottom, left, right and applies the first rule where the exclusive edge is the singular anchor, or the anchor is the singular anchor, or the anchor is the three-edge triplet, guarded by `exclusive + margin(edge) > 0` (:2575); one `CReservedArea{ORIGINAL_USABLE_AREA, usableArea}` becomes the whole layer reserve (:2696), a total with no per-surface attribution | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-composition-r80.md |

S471

| S471 | Hyprland v0.56.2 — src/protocols/LayerShell.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/LayerShell.cpp | code | A | mado layer plane: the protocol requests that carry a surface's exclusive zone and exclusive edge, and the alignment error that forbids an edge outside the anchor (round-80 C1) | `setSetExclusiveZone` :100-103, `setSetExclusiveEdge` :156-169, the alignment refusal :162-165 @ efb5099 (fetched 2026-11-04, sha256 `ad9314dafda63278aaaa4241e969544560f01fb00983d7754e35fae2567a8961`, 9935 B) | the requested zone is stored exactly as the client sent it, with no clamp, so a non-positive or oversized zone reaches the renderer's `exclusive <= 0` and area guards; an exclusive edge that is not inside the pending anchor mask is refused with `INVALID_EXCLUSIVE_EDGE` — the refusal the composition cases `exclusive-edge-matched` and `anchor-unmatched` rest on | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-composition-r80.md |

S472

| S472 | Hyprland v0.56.2 — tests/desktop/Reserved.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/tests/desktop/Reserved.cpp | code | A | mado layer plane: the upstream unit test that pins `CReservedArea`'s parent/child arithmetic, its empty-box zeros and its not-contained verdict (round-80 C1) | whole file, 1532 B; the parent/child case :32-37, the empty-parent and empty-child cases :39-51, the not-contained case :53-54 @ efb5099 (fetched 2026-11-04, sha256 `37988cca6d024a1481cc419c3bb06cf8c5929e91297514cda11475931a330402`) | the area is `child.pos - parent.pos` on the near side and `(parent.pos + parent.size) - (child.pos + child.size)` on the far side; an empty parent or an empty child gives all four sides zero; a child not contained in the parent gives `ok() == false` — the test asserts that verdict alone, the zeroed area in that branch belongs to the constructor (S459, S466) | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-composition-r80.md |

S473

| S473 | omarchy 3.8.3 — omarchy-menu-keybindings (installed payload) — ~/.local/share/omarchy/bin/omarchy-menu-keybindings | own-work | A | the keybindings chord column the C2 runbook row reads: how a numeric modifier mask and a key become the printed chord (round-80 C2) | `dynamic_bindings` :90-116, its modmask sed table :100-115 (sixteen `s/^N,/` rules: `^0,` strips the mask, then SHIFT, CTRL, SHIFT CTRL, ALT, SHIFT ALT, CTRL ALT, SHIFT CTRL ALT, SUPER, SUPER SHIFT, SUPER CTRL, SUPER SHIFT CTRL, SUPER ALT, SUPER SHIFT ALT, SUPER CTRL ALT, SUPER SHIFT CTRL ALT); `parse_keycodes`' `code:201` → `COPILOT KEY` :49-50 and the mouse-button symbols :58-63; `parse_bindings`' `printf "%-35s → %s\n"` :164 @ payload `version` 3.8.3, checkout HEAD `8fcc9d60` (tagged v3.8.4), no local modification; fetched 2026-11-04, sha256 `3487bbb89bb2d4bbbb345b54691e1db393875cd12526203e0e305e9b584b14fe`, 8064 B, 251 L, byte-identical to the installed file | a chord prints as the modifier words joined by spaces, ` + `, then one key, left-padded to 35 columns before ` → ` and the action; a keycode or a mouse button prints as a bare multi-word key; a bind whose action is empty is not printed — the grammar the runbook row binds, not a statement that any particular bind exists | mined | 2026-11-04 | on-change | corpus/knowledge/bar-footprint-composition-r80.md |

S474

| S474 | systemd 262 (262.1-1-arch) — systemctl(1) — man systemctl on this host (/usr/share/man/man1/systemctl.1.gz) | docs | A | the `systemctl --user is-active` row's contract: the state word and the exit status that must agree with it (round-80 C2) | the `is-active PATTERN...` paragraph, `.ufo/waves/round-80/fetch/S474.txt:3-7` (the MANWIDTH=80 render's lines 190-193) @ systemd 262.1-1, installed man page (fetched 2026-11-04, sha256 `d3c367601a22ceb9b950c6a9a4b6a4cbba8936d5ff28742eaf01a3b589e4f1cb`, 337 B) | `is-active` returns exit code 0 if at least one named unit is active and non-zero otherwise, and prints the current unit state unless `--quiet` — with one unit named, status 0 and the word `active` are one fact, which is why the row binds word and status together and never the word alone | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-composition-r80.md |

S475

| S475 | Hyprland wiki — Configuring › Monitors — https://wiki.hypr.land/Configuring/Monitors/ (as committed at .ufo/waves/round-45/fetch/wiki-Monitors.md) | docs | B | the `addreserved` line syntax and its stacking sentence, re-stated to narrow S467's rejection (round-80 correction) | `.ufo/waves/round-45/fetch/wiki-Monitors.md:179` (the line syntax) and `:183-184` (the stacking sentence); the live URL 404s on 2026-11-04 and no page revision is pinned anywhere in the committed fetch | supersedes S467 — REJECTED: dead live URL, no revision pin, tier-B prose only. The committed round-45 fetch does state the stacking at :183 ("This does stack on top of the calculated reserved area"), so S467's "syntax only, not the summation" ground is refuted rather than incomplete; what survives is the unresolving URL, the absent revision pin and the tier-B prose alone — none of which a row can supply for itself. flip: a resolving, revision-pinned page that states the static-plus-dynamic arithmetic | rejected | 2026-11-04 | 180d | — |

## 2. Gate-table quotes (≤25 words, located)

| row | located quote | file:line | what it licenses / does not |
|---|---|---|---|
| S470 | `applyExclusive(*usableArea, PSTATE->anchor, PSTATE->exclusive, PSTATE->exclusiveEdge, PSTATE->margin.top, PSTATE->margin.right, PSTATE->margin.bottom, PSTATE->margin.left);` | `.ufo/waves/round-80/fetch/S470.bin:2664` | every exclusive surface, in arrangement order, mutates the one running box, so composition is cumulative and order-bearing; not which edge takes the zone (that is :2575) and not any per-surface band |
| S471 | `r->error(ZWLR_LAYER_SURFACE_V1_ERROR_INVALID_EXCLUSIVE_EDGE, "Exclusive edge doesn't align with anchor");` | `.ufo/waves/round-80/fetch/S471.bin:163` (the condition is `:162`) | an exclusive edge outside the pending anchor mask is a protocol error, so every accepted edge names an edge the anchor already holds; not what the renderer then does with the zone |
| S472 | `Desktop::CReservedArea e{CBox{20, 30, 900, 900}, CBox{0, 0, 100, 100}};` then `EXPECT_EQ(e.ok(), false);` | `.ufo/waves/round-80/fetch/S472.bin:53-54` | upstream asserts the not-contained verdict; it does not assert the zeroing of that branch, which is the constructor's (S459, S466) |
| S473 | `printf "%-35s → %s\n", key_combo, action;` | `.ufo/waves/round-80/fetch/S473.txt:164` | the printed line is the chord left-padded to 35 columns, then ` → `, then the action, so the chord column is `cut -c1-35`; not that any particular bind, or the 35-column pad in practice, holds on this host |
| S474 | `Returns  an  exit code 0 if at least one is active` | `.ufo/waves/round-80/fetch/S474.txt:5` | status 0 and the word `active` are the same fact for a one-unit `is-active`; the sentence continues `or non-zero other‐wise.` at :5-6 (the `‐` is the render's line-break hyphen); not why a unit would be inactive |
| S475 | `This does stack on top of the calculated reserved area (e.g. bars)` | `.ufo/waves/round-45/fetch/wiki-Monitors.md:183` | the committed pin does state the stacking, so S467's "syntax only" ground fails; it supplies no revision pin, no resolving URL and no arithmetic |

## 3. Deltas against the rows already at `corpus/SOURCES.md:421-426`

Written 08:39 (before this seat settled). Cell-by-cell, in the order I would change them.

1. **S473 (:424) — factual, the one that matters.** The committed anchor says "the modmask sed
   table :100-120 (the twelve masks …)". The table is `:100-115`, and it holds **sixteen**
   `s/^N,/` rules: `^0,` (strip the mask) plus fifteen modifier sets. `:116` is the closing
   `}`, `:119-121` is `static_bindings`. Neither 12 nor 120 is reproducible from the bytes;
   the count of 12 appears in the seat brief and in the claims declaration, so it is worth
   correcting in all three places or nowhere. Detail: `S473.txt:100-115`.
2. **S472 (:423) — span and one clause.** Committed cites the empty cases as `:40-52`; the two
   declarations are `:39` (`c`) and `:46` (`d`) and the last assertion is `:51`, so `:39-51`.
   Committed's teaches joins "`ok() == false` with a zeroed area"; the test at `:53-54` asserts
   the verdict only (no area read after it), so the zeroing is S459/S466's, not this row's.
3. **S471 (:422).** `setSetExclusiveZone :100-102` omits the handler's closing `});` at `:103`.
   The seat brief's `set_exclusive_edge :156-168` likewise omits the `});` at `:169`; the
   committed `:156-169` is the accurate span.
4. **S470 (:421).** Committed omits the note the seat asks for — the row repeats S457's URL at a
   different scope — and it compresses the first-match rule into `zone + margin(edge) > 0`; the
   guard is on the sum (`exclusive + margin`), not on the zone. The census's standing W04
   duplicate-URL warning is expected for this pair, as it was for S465/S306 and S466/S459.
5. **S473 (:424) — version label.** "omarchy 3.8.3" matches the payload's own `version` file
   (3.8.3, tracked and clean at HEAD), while that checkout's HEAD `8fcc9d60` is tagged
   **v3.8.4**. Naming the HEAD sha and the tag beside the payload version removes the
   ambiguity; my row does.
6. **S474 (:425).** Committed's anchor names the paragraph but no line. The paragraph is
   `S474.txt:3-7`, i.e. render lines 190-193 at `MANWIDTH=80`. The version string matches both
   the fetch's line 1 and `pacman -Q systemd` → `systemd 262.1-1`.
7. **S475 (:426).** Committed says S467's reason "was too narrow"; it was **refuted** — the
   pin answers the very question the old reason said it did not. Committed also sets
   `used-by = corpus/lessons/round-80.md` where my row files `—`; either is defensible
   (S463, a rejected row, does list citing entries; S467 and S045 file `—`), and the committed
   value truthfully records the Gate row's home. Committed's `recheck = on-change` cannot fire
   on a URL that 404s; I file `180d` as a re-probe duty. Both are L1 calls, named not forced.

Precision note, not a delta: the three S470 ranges are the declaration's and S457's
(`:2529-2586`, `:2587-2671`, `:2673-2700`). Line 2586 and 2671 are the blank lines after each
closing brace (`applyExclusive` closes at 2585, `arrangeLayerArray` at 2670), and
`arrangeLayersForMonitor` continues past 2700 (`damageMonitor`) to `invalidateMonitorGeometries`
at 2701 and the brace at 2702. I keep the declaration's ranges so the row, the report and the
counter agree.

## 4. Verification actually run (read-only)

- `sha256sum -c sha256-r80.txt` in `.ufo/waves/round-80/fetch/` → five `OK`, rc 0. The manifest
  has no self-entry (the M79-5 defect does not recur).
- `stat -c '%s'` → 143211 / 9935 / 1532 / 8064 / 337 B, matching every size cited above.
- `cmp ~/.local/share/omarchy/bin/omarchy-menu-keybindings fetch/S473.txt` → identical;
  `sha256sum` of the installed file equals the fetch's.
- `git -C ~/.local/share/omarchy` reads only: `rev-parse HEAD` → `8fcc9d60…`, `show HEAD:version`
  → `3.8.3`, `status --porcelain -- version` → empty, `tag --points-at HEAD` → `v3.8.4`.
- `MANWIDTH=80 man systemctl` render: `is-active PATTERN...` at 189, the paragraph at 190-193,
  byte-equal to `S474.txt:3-7`; `pacman -Q systemd` → `262.1-1`.
- Line spans re-read from the fetch files themselves (S470:2664, S471:100-103 and 156-169 with
  the refusal at 162-165, S472:32-37/39-51/53-54, S473:100-115 and 164, S474:3-7,
  round-45 wiki:179/183).

## 5. Limits

- `S474.txt` is a 337 B assembled excerpt (the man page's `systemd 262 (262.1-1-arch)` banner plus
  the `is-active` paragraph), not one contiguous render; the quoted lines are verbatim-present in
  the installed page at `MANWIDTH=80`, verified line for line, but the file's sha256 pins the
  assembled excerpt's bytes, not the page.
- The "twelve masks" figure is not reproducible from `S473.txt`; I report sixteen rules and do not
  adopt the count. If the frozen instrument or a receipt already prints "twelve", that string and
  this row disagree and the instrument's line should be named before the lesson repeats it.
- `corpus/SOURCES.md` was already carrying S470–S475 when this seat read it; this draft is a
  re-derivation and a delta, never a claim that I appended anything.
- No source here establishes host behaviour; every row is a document or a captured payload read
  without executing it.

STATUS: ok
