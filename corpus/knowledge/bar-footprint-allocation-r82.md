# The client's own band — a declared dynamic layer band, modelled (round 82)

source: S481 (new), S464, S470; held S460 (byte-identical to S481)
verified-at: 780c30fcae12d74ce8ab3b871a0888696c2415d9 (the round-82 freeze; the measured receipt
`.ufo/waves/round-82/receipts/measurement-c1-r82.txt` records `rev=780c30fc… tool_sha256=38007528…`)
recheck: `python3 -I quality/counters/c1-r82-allocation-band.py --repo . --rev REV --base-rev
6ea2386d49318a5f223097c78b5fe79c31b064f8 --controls .ufo/waves/round-82/controls/c1-cases-r82.json
--carried .ufo/waves/round-81/controls/c1-cases-r81.json --scratch-root DIR` — 47 frozen cases
(39 carried + 8), 34 named mutants, exit 0 only on `MADO_R82_BARFOOT: cases=47 correct=47 mutants=34 killed=34 base_correct=39/47 carried=39/39 tool_selftest=133/133 verdict=TARGET_MET`

Evidence classes as in the rest of the corpus: `[OBS]` seen in a pinned byte or a live read;
`[INF-src]` follows from pinned code; `[DOC]` a pinned document's sentence; `[UNK]` not
established. Quotes are ≤25 words with a line anchor. No layer surface is created and no
compositor verb is run: every number below is a model over committed bytes and the frozen
fixtures, not a host capture.

## 0. What this entry is

Round 81 modelled the bar-footprint join's auto zone and named the dynamic band — a declared
`height = 0` on a horizontal surface, `width = 0` on a vertical one — `NOT_MODELLED`: gtk-layer-shell
sends the client's *allocation* as the zone, and the join had no input for that number
(`bar-footprint-rounding-auto-r81.md` §4, §7 item 1). This entry states the two source facts that
class rests on, the declared input the round-82 join grew (`--allocation`), the resolver that
consumes it, and the classes that remain refused.

The instrument is `tools/mado-barfoot.py` generation `r82-v1`, sha256
`380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59`; the counter is
`quality/counters/c1-r82-allocation-band.py`, sha256
`1e9f394df80284e78f1fdf3f24cb5e14d1e4091f4880ccc60a2a45060b54612d`; the frozen controls are
`.ufo/waves/round-82/controls/c1-cases-r82.json`, sha256
`e404bb3fa93d5f12338129adc8733574084e6fab2ee12fbb471dd45df94a315f`. The receipt's totals
(`measurement-c1-r82.txt:84`):

```
MADO_R82_BARFOOT: cases=47 correct=47 mutants=34 killed=34 base_correct=39/47 carried=39/39 tool_selftest=133/133 verdict=TARGET_MET rev=780c30fcae12d74ce8ab3b871a0888696c2415d9 tool_sha256=380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59
```

The do-nothing control is the held round-81 tool at the base (`a129a435…`): 39/47, with all eight
new cases unreachable (`measurement-c1-r82.txt:82`; the base run's six r82-only mutants report
`killed=no reason=anchor-absent` in `.ufo/waves/round-82/receipts/control-c1-r82-at-base.txt`, so
28 of 34 kill at base and the six allocation mutants have no anchor to cut). The new cases'
`layers` replies are constructed to the derivation (fixed 3440×1440 fixtures, `pid: 4242`,
`controls/make-c1-cases-r82.py:33-53`), so a `box=MATCH` in the receipt is a model-versus-fixture
check, not a host capture.

## 1. A zero size is a request, and the band is the client's allocation

`set_size` is a request, and its zero case delegates the number:

> `If you pass 0 for either value, the compositor will assign it and inform you of the assignment in the configure event.` (S481:128-131)

`[DOC]` The request is double-buffered (`S481:133`) and both values default to 0 (`S481:131`). The
assigned size comes back in `configure`, whose payload is explicitly a hint (`S481:327-349`):

> `The size is a hint, in the sense that the client is free to ignore it` (S481:341-342)

and, for a zero payload:

> `If the width or height arguments are zero, it means the client should decide its own window dimension.` (S481:347-348)

`[DOC]` So the number is not in the declaration at all: on a zero request the compositor assigns,
and on a zero (or smaller-than-offered) configure the client decides. gtk-layer-shell takes the
second branch. In `layer_surface_on_size_allocate` (S464:298-315) it copies GTK's allocation into
`self->current_allocation` (`S464:307-310`), sends that size back with
`layer_surface_send_set_size` (`S464:312`), and immediately recomputes the auto zone from it
(`S464:313`). The sender zeroes only the axes that are stretched between opposite anchors
(`S464:33-45`): for a `top|left|right` bar the width request is 0 and the height request is the
allocation's height.

`[OBS]` S481 is byte-identical to the held S460 pin: both are 407 lines and
`sha256sum` reports `87e0b9c837aecd6977f76f3c47d73088b7159871f5d979dc1840f6cadb5e2ed8` for
each. The new id re-opens the same protocol text; it is a new registry row, not a new revision.

**Why the compositor's arranged box is not the band.** Hyprland's arrange pass starts from the
last requested size, not from the client's allocation (`S470:2607`):

```c
CBox           box = {{}, PSTATE->desiredSize};
```

Fed a zero desired size — what a zero declaration stands for — the arrange takes the *assign*
branches: a zero width sets `box.x = bounds.x` (`S470:2610-2611`) and then fills the axis
`box.width = bounds.width - (PSTATE->margin.left + PSTATE->margin.right)` (`S470:2635-2637`); a
zero height does the same vertically (`S470:2623-2624`, `:2645-2647`). The result is the
available box, rounded (`S470:2660`), not the number the client will occupy. The client's
allocation enters the compositor as a requested size only after `layer_surface_send_set_size`
(`S464:312`), and as the zone through `set_exclusive_zone` (`S464:292`); at that point the
desired size on the band axis *is* the allocation — exactly the number a join reading only the
declaration does not have.

The two numbers coincide when the client accepts the whole span; the protocol permits that but
does not require it (`S481:341-345`). A model that equated them would be right by accident on a
full-span client and wrong on a bar, which is the class this round freezes.

## 2. The auto zone is that allocation, plus the unanchored margin

The gate and both arms are in `layer_surface_update_auto_exclusive_zone` (S464:264-295). The
equality tests are `horiz = (LEFT == RIGHT)` and `vert = (TOP == BOTTOM)` (`S464:269-272`); the
arms are transposed by axis (`S464:275`, `:281`):

```c
if (horiz && !vert) {
    new_exclusive_zone = self->current_allocation.height;   /* :276 */
    if (!self->anchors[GTK_LAYER_SHELL_EDGE_TOP])
        new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_TOP];   /* :278 */
    if (!self->anchors[GTK_LAYER_SHELL_EDGE_BOTTOM])
        new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];
} else if (vert && !horiz) {
    new_exclusive_zone = self->current_allocation.width;    /* :282 */
    if (!self->anchors[GTK_LAYER_SHELL_EDGE_LEFT])
        new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_LEFT];   /* :284 */
    if (!self->anchors[GTK_LAYER_SHELL_EDGE_RIGHT])
        new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_RIGHT];
}
```

Four facts follow.

1. **The gate is anchor equality, not "spans".** `horiz` is true when both horizontal anchors are
   present or both absent (`S464:269-270`); `vert` likewise (`S464:271-272`). A corner pair makes
   both false; a parallel pair and all four make both true. In those classes `new_exclusive_zone`
   stays `-1` (`S464:273`) and the `>= 0` guard (`S464:289`) skips the request entirely — no
   `set_exclusive_zone` is sent. The join returns 0 for the same classes
   (`tools/mado-barfoot.py:633-634`).
2. **The base is the allocation** (`S464:276`, `:282`), assigned from GTK's rectangle in
   `layer_surface_on_size_allocate` (`S464:304-310`), not the requested or declared size.
3. **The unanchored margin is added client-side** (`S464:277-280`, `:283-286`): a top bar adds the
   *bottom* margin, a left dock the *right* one. The anchored edge's margin is not added here.
4. **The value is sent only when it changes** (`S464:289-292`). It is a stored integer the
   compositor receives as the surface's exclusive zone; Hyprland then adds the anchored margin in
   `applyExclusive` (guard `S470:2531-2533`, match and add `S470:2575-2581`). A top bar with a
   4 px margin on all four sides therefore reserves `allocation.height + 4 (bottom, client) + 4
   (top, compositor)`.

## 3. What the round-82 join does with that

**Input.** `--allocation PATH|-` reads a JSON object whose values are non-negative integers
(`parse_allocation`, `tools/mado-barfoot.py:436-453`). A non-object, an empty namespace, a
non-integer, or a negative value is a `Setup` failure — exit 2, stage `setup` — before any surface
is arranged (`:441-451`). Zero is a *model* refusal later, not a parse failure.

**Resolver.** `band_of(spec, allocation)` is the single entry point for the band axis
(`:456-471`), in this order:

1. the declared value, when positive (`:461-462`);
2. else the allocation for `spec["namespace"]` (`:463`);
3. an absent entry is `Unmodelled` — stage `model`, exit 3 (`:464-467`);
4. a zero or negative entry is `Unmodelled` — stage `model`, exit 3 (`:468-470`).

**Single-surface path.** `declared_box` resolves the band axis through `band_of` before the
anchor arithmetic (`:481-482`), so for a horizontal surface the box's `height` is the declared
height when positive and the allocation when it is 0; the other axis is untouched. The
anchored-edge extent is then measured from that resolved box (`edge_extent`, `:515-524`), and the
reserved contribution adds the opposite (unanchored) margin (`:1041`). The join does not call
`surface_zone` in this path: the box is the only source of the band, and it is already resolved.

**Composition path.** `evaluate_composition` resolves the bar's band into `bar_spec` before the
arrangement order is built (`:802-803`), so the same resolver supplies the box *and* the auto
zone: `surface_zone` reads `spec["height"]` / `spec["width"]` (`:614-622`) and the loop calls it
at `:837`. Each surface is then arranged against the running usable box (`:820-828`), a positive
zone shrinks that box on its matched edge (`:855-866`, helper `apply_exclusive`
`:718-738`), and the total is one attribution vector (`:868-878`). The same run recomputes the
bar's pass from the allocated band, so a later surface sees `y = allocation` and arranges under
it.

**Unknown namespaces.** The single path accepts only the bar's namespace in the map (`:962-965`);
the composition accepts the bar's or any declared `--surfaces` namespace (`:769-773`). Anything
else is a `Setup` failure, exit 2.

## 4. Decision table

The eight new cases are `alloc-*` in `c1-cases-r82.json`; the carried `auto-dynamic-band-refused`
is the no-allocation control. "Modelled result" is the `RESULT`/`DECL` the join prints for the
frozen fixture, not a host reply.

| # | Case | Surface and declaration | `--allocation` | Modelled result |
|---|---|---|---|---|
| 0 | `auto-dynamic-band-refused` (carried) | top bar, `height: 0`, `exclusive: auto` | — | refused, stage `model`, rc 3 (`band_of` `:464-467`) |
| 1 | `alloc-dyn-height-top` | top bar, `height: 0` | `{"waybar": 34}` | box `0,0,3440,34`; band 34; `CLEAN` |
| 2 | `alloc-dyn-height-margin` | top bar, `height: 0`, `margin: 4` | `{"waybar": 30}` | box `4,4,3432,30`; client zone `30+4=34`; reserved `34+4=38` |
| 3 | `alloc-dyn-width-dock` | left dock, `width: 0`, `height: 0` | `{"waybar": 60}` | box `0,0,60,1440`; left band 60; `CLEAN` |
| 4 | `alloc-zero-refused` | top bar, `height: 0` | `{"waybar": 0}` | refused, stage `model`, rc 3 (`:468-470`) |
| 5 | `alloc-negative-refused` | top bar, `height: 0` | `{"waybar": -4}` | refused, stage `setup`, rc 2 (`:450-451`) |
| 6 | `alloc-unknown-namespace` | top bar, `height: 26` | `{"panel": 40}` | refused, stage `setup`, rc 2 (`:962-965`) |
| 7 | `alloc-explicit-ignored` | top bar, `height: 26` | `{"waybar": 40}` | declaration wins; band 26; `CLEAN` |
| 8 | `alloc-composition-dyn-bar` | top bar, `height: 0` + level-3 panel, `height: 100`, `exclusive: 12` | `{"waybar": 34}` | bar box `0,0,3440,34`, zone 34; panel box `0,34,3440,100`; `attr=0,46,0,0`; `CLEAN` |

Row 2's arithmetic is the two margin owners: the allocation is 30, gtk adds the unanchored bottom
4 (`S464:279-280`), and Hyprland adds the anchored top 4 (`S470:2575-2581`). Row 8's panel is
arranged after the bar's pass: usable becomes `0,34,3440,1406`, the panel's zone 12 moves the usable
origin to `y=46`, and the attribution vector is `left=0, top=46, right=0, bottom=0`
(`RESULT.attr` is in the monitors reply's left, top, right, bottom order, `:897-898`).

## 5. Limits

1. **The allocation is declared, not observed.** The join prints the caller's number; it never
   reads the surface's allocation back. A caller that declares 34 for a client allocated 40 gets a
   modelled box and band the compositor never reserves. A captured `hyprctl layers -j` reply does
   catch it: `LIVE` is compared with the modelled box and a mismatch prints `box=DIFFER`
   (`tools/mado-barfoot.py:1025`). The frozen cases' `layers` replies are built to the derivation
   (§0), so their `box=MATCH` is a fixture echo, not that check.
2. **Per-axis dynamic extra surfaces stay refused.** `--allocation` is consumed only for the bar:
   the composition resolves `bar_spec`'s band axis (`:802-803`) and never rewrites an extra's
   spec, so an extra declaring `height: 0` still hits the `surface_zone` refusal (`:614-616`,
   `:624-626`) at its turn. An entry for an extra's namespace passes the unknown-name check
   (`:769-773`) but is inert — not an error and not a model. A caller can believe the extra was
   resolved; it was not.
3. **Fractional scale stays refused.** `scale` other than 1 or `transform` other than 0 is an
   `Unmodelled` refusal in both paths (`:978-981` single, `:763-766` composition); the allocation
   is in the monitor's logical pixels, matching the layer box the join compares.
4. **Unknown namespace and negative band are setup refusals** (`:962-965` / `:769-773` and
   `:450-451`), as are a non-object, empty-name or non-integer map. A zero band is a model refusal
   (`:468-470`): gtk would send 0 and Hyprland's `zone + margin > 0` guard would reserve nothing
   (`S470:2531-2533`, `:2575`), so there is no band to print.
5. **A caller can mis-declare in three ways the model does not refuse.** (a) A band larger than
   the usable box: no bound check exists; the single path prints the oversized box and the
   containment test drops its contribution (`:483-496`, `:1030-1042`), while the composition
   shrinks the usable box negative and reports `ls=INVALID` (`:868`) — neither is a refusal.
   (b) A band on a non-band axis is never read: a top/bottom surface resolves only `height`
   (`:481`), so a `width` value in the map is accepted and unused. (c) An allocation that
   duplicates a positive declaration is silently ignored (`:461-462`; case
   `alloc-explicit-ignored`), so a stale or contradictory entry cannot be detected from the
   output.
6. **The protocol clause is not a host observation.** S481 says what a zero request and a zero
   configure mean; it does not say what waybar sends on this host today. `--allocation` is
   caller knowledge, and the frozen fixtures are the only executions of it in this round.
7. **The carried case's name is historical.** `auto-dynamic-band-refused` now refuses through
   `band_of` (`:464-467`), not through `surface_zone`; the round-81 name and its rc 3 are
   unchanged, which is why the carried case still scores `correct=yes` (`carried=39/39`).

## 6. Where this sits

Round 77 measured the bar's footprint from the declaration; round 78 composed the margins; round
79 composed the static reserve; round 80 composed several exclusive surfaces; round 81 modelled
the coupled rounding and the auto gate and named the dynamic band `NOT_MODELLED`; this round
models the bar's dynamic band from a declared allocation and keeps every other refusal in force.
The next finite grounds are an extra surface whose band is dynamic (requires the resolver to
reach `--surfaces` specs, not only the bar's) and fractional scale (requires the monitor and
layer spaces to be reconciled), neither of which has a case yet.

## sources

source: S481 — wlr-layer-shell `wlr-layer-shell-unstable-v1.xml`, `.ufo/waves/round-82/fetch/S481.xml`, 407 lines, sha256 `87e0b9c837aecd6977f76f3c47d73088b7159871f5d979dc1840f6cadb5e2ed8`, opened 2026-11-04; byte-identical to held S460. Anchors used: `set_size` `:122-137` (zero clause `:128-131`), `configure` `:327-349` (hint `:341-345`, zero clause `:347-348`).
source: S464 — gtk-layer-shell v0.10.1 `src/layer-surface.c`, `.ufo/waves/round-79/fetch/S464.bin`, held. Anchors used: `:31-57` (the sender zeroes stretched axes, `:33-45`), `:264-295` (auto zone; `:269-272` gate, `:276`/`:282` allocation, `:277-280`/`:283-286` margins, `:289-292` send guard), `:298-315` (size-allocate assignment `:304-310`, send `:312`, zone update `:313`).
source: S470 — Hyprland 0.56.2 `src/render/Renderer.cpp`, `.ufo/waves/round-80/fetch/S470.bin`, held. Anchors used: `:2531-2533` (exclusive guard), `:2575-2581` (edge match and margin add), `:2607` (`desiredSize`), `:2610-2611`/`:2623-2624`/`:2635-2637`/`:2645-2647` (zero-size and span branches), `:2660` (round), `:2664` (applyExclusive call).

## Round-83 receipt erratum (round-82 spot-check D1)

The live path `measurement-c1-r82.txt` was overwritten after the freeze and no longer records
the revision in this note's header. Resolve that historical receipt at its cited commit, or use
`receipts/measurement-c1-r82-at-tip.txt` (rev 57789ab6, tool sha256 prefix 38007528).
The later live-path receipt records rev 12e6ad57 and tool sha256 prefix 58ef4f6a.
These are distinct generations, not interchangeable measurement pointers.
