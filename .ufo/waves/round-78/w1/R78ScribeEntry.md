# R78ScribeEntry — C1 knowledge entry (findings)

Seat: scribe. Assignment: draft the C1 knowledge entry `bar-footprint-margins-r78.md`; write prose
only, L1 integrates. Status: drafted, not integrated. No repo file edited, no git/jj mutation, no
live compositor probe, no counter rerun.

## Artifacts written

- `.ufo/waves/round-78/w1/R78ScribeEntry/bar-footprint-margins-r78.md` — the draft entry (97 lines,
  provenance trio + two-contributor composition + decision table + 18-case worked set + limits).
- `.ufo/waves/round-78/w1/R78ScribeEntry.md` — this file (copy also in the seat dir).

## Read (inputs, unmodified)

- `.ufo/waves/round-78/claims-declaration-r78.md` (frozen contract).
- `corpus/knowledge/bar-footprint-r77.md` (voice and shape).
- `.ufo/waves/round-78/receipts/measurement-c1-r78.txt`, `control-baseline-c1-r78.txt`.
- `.ufo/waves/round-78/controls/c1-cases-r78.json` (18 cases, `protocol: mado-c1-r78-v1`).
- `tools/mado-barfoot.py` (`VERSION = "r78-v1"`), `quality/counters/c1-r78-margins.py`.
- Pinned sources `.ufo/waves/round-78/fetch/S457.bin`, `S464.bin`, `S462.bin`, plus `sha256-r78.txt`.
- `corpus/SOURCES.md` rows S457–S464.

## Commands run and observed output (read-only)

1. `sha256sum tools/mado-barfoot.py quality/counters/c1-r78-margins.py .ufo/waves/round-78/controls/c1-cases-r78.json`
   → `aac5d41b923711e174c6d62bb24da5a2b53abf7c938bfc5b68816929a12009c0`, `1c39a53c9320b3f4c849ceb973e7fb0d42fb115e2f8f7a64bc3338fc4ab85000`, `99f1d82fd3476b151be2951549645ce71fd47b6d8a9e96f90a5f891bda5a56ae`.
   All three equal the declaration's frozen hashes and the `MADO_R78_CONTROL` line.
2. `cd .ufo/waves/round-78/fetch && sha256sum -c sha256-r78.txt`
   → `S457.bin: OK`, `S458.bin: OK`, `S459.bin: OK`, `S460.bin: OK`, `S462.bin: OK`, `S464.bin: OK`.
   (The manifest carries six rows; `S461.txt` — the `zcat` render — has no row, so the entry says
   "six fetched sources" and lists S461 as `waybar(5)`, not as a re-pinned byte receipt.)
3. `git rev-parse HEAD` → `fa6f3fda8d03e1f8faf066d2f8cbcc55d5a98950`;
   `git rev-parse 44a36b64` → `44a36b64117812af7cc23a1815430d8320642455`;
   `git show 44a36b64:tools/mado-barfoot.py | sha256sum` → `aac5d41b…` (equals the working file);
   `git show f597eccb…:tools/mado-barfoot.py | sha256sum` → `e54787b7…` (equals the receipt's
   `base_sha256`). HEAD being past the measured revision is post-wave commit activity, not a
   conflict: the measured tool bytes are identical at `44a36b64` and in the working tree.
4. `python3 -I tools/mado-barfoot.py --selftest` → `MADO_BARFOOT_SELFTEST: 22/22` (rc 0).
5. Anchor checks in the pinned bytes:
   - `S457.bin:2575` — edge guard `(exclusiveEdge == … || anchor == … || anchor == …) && exclusive + edges[i].margin > 0`.
   - `S457.bin:2577` — `*edges[i].positive_axis += exclusive + edges[i].margin;`.
   - `S457.bin:2579-2581` — the negative-axis subtraction.
   - `S457.bin:2547/2555/2563/2571` — `.margin = marginTop/marginBottom/marginLeft/marginRight`.
   - `S457.bin:2660` — `box.round();`; `:2664` — the `applyExclusive` call; `:2682` — `logicalBoxMinusReserved()`;
     `:2696` — `m_reservedArea.addType(… CReservedArea{ORIGINAL_USABLE_AREA, usableArea})`.
   - `S464.bin:264` — `layer_surface_update_auto_exclusive_zone (LayerSurface *self)`;
     `:276` — `new_exclusive_zone = self->current_allocation.height;`; `:278/:280` — top/bottom adds;
     `:282-286` — the vertical transposition.
   - `S462.bin:357-358` — `if (mode.exclusive) { gtk_layer_auto_exclusive_zone_enable(gtk_window); }`,
     `:360` — `gtk_layer_set_exclusive_zone(gtk_window, 0);` on the else branch; `:422-424` — both
     horizontal anchors cleared when `configured_width > 1`; `:240` — `window.set_size_request(width_, height_);`.
   - `tools/mado-barfoot.py:69` — `OPPOSITE_EDGE`; `:307-315` — `edge_extent`; `:410-411` —
     `band = mon["reserved"][RESERVED_INDEX[edge]]` then `expected = extent + bar["margins"][OPPOSITE_EDGE[edge]]`;
     `:253-254` — negative-margin refusal; `:271-274` — dynamic-cross refusal; `:370-374` — scale/transform refusal.
6. `quality/counters/c1-r78-margins.py` read, not run: case scoring at `expected_ok`/`run_cases`,
   mutation anchors at `:35-57`, `apply_mutation` at `:145-149`, `MUTATIONS` names match the seven
   `MADO_R78_MUTANT` lines in the receipt.

## Findings carried into the entry

- The composition is `expected = extent + margin[opposite edge]`; the anchored margin enters through
  the box position (`mado-barfoot.py:280`, `:287-294`) and the opposite margin is added explicitly
  (`:411`). For a top bar that is `(m.top + h) + m.bottom`; vertical bars transpose to
  `w + m.left + m.right`.
- The seven mutation scores (9/18, 9/18, 17/18, 16/18, 17/18, 17/18, 17/18) and the base control
  8/18 are quoted from `measurement-c1-r78.txt`; the entry labels them as receipt lines, not as a
  fresh run by this seat.
- `exclusive-false` publishes `expected=26` with `reserved=NOT_APPLIED`; the entry states that the
  number is arithmetic, not proof that no band exists.
- `second-consumer` shows `band=60 expected=34 reserved=GT verdict=CLEAN`; the entry states `GT` is
  admissible and not an attribution of the band to a surface.

## Limits / not verified by this seat

- No live `hyprctl layers -j` / `hyprctl monitors -j` capture exists in this round's receipts; all 18
  cases are committed fixtures (`c1-cases-r78.json`). The draft says so explicitly and does not
  present `host-top` as an observation.
- The counter was not re-executed (assignment: cite the receipt, never rerun to decorate). The only
  execution performed is the tool selftest (`22/22`), recorded above.
- The draft's §2 table omits `layer: overlay`/`background` row distinctions beyond the refusal line;
  `background` is refused (`mado-barfoot.py:246`) while `overlay` is a reachable level. The L1 may
  decide whether that deserves its own row.
- No conflicts between declaration, receipt and source were found. Nothing was observed that
  contradicts the frozen instruments.
- Observed repo change during this seat (not made by me): `git diff` on
  `.ufo/waves/round-78/receipts/measurement-c1-r78.txt` shows one changed token, the rev field
  `b8508bd9…` → `44a36b64…`; every case, mutant, base and verdict line is byte-identical, and the
  entry quotes the current `44a36b64` line.

## Tooling

No tool installed or upgraded. `pacman` untouched.

Report: .ufo/waves/round-78/w1/R78ScribeEntry.md
