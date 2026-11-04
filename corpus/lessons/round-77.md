# mado round 77 — the bar's footprint and an executable runbook (2026-11-04, hyaku run 15)

Claims: **C1 coverage** — the bar-footprint chain (declared waybar config → live layer box →
monitor `reserved` band) becomes a measured join with a durable read-only tool and a frozen
15-case set; **C2 operability** — the SKILL.md read-only probe table executes end-to-end as 12
frozen cases, each bound to its committed table row. Freeze `a83e9bee`; base `aeeef067`.
Declaration: `.ufo/waves/round-77/claims-declaration-r77.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M77-1 | registry row shape: two new-row batches were appended with a separate quote column (12 fields), so the first census read `E01 fields=12` for every appended row | `/fast/scratch/hyaku/mado-r77/census2.txt` (E01 S458–S463) versus the same census after the rewrite (exit 0, only W04/W01 warnings) | the frozen `sources-census.sh validate` gate, not a reading of the row by eye | rows rewritten to the 11-column schema with the quote in `teaches`; the red/green pair is the census receipt (E01 before, exit 0 after). Reverting the quote column reproduces E01. |
| M77-2 | the C1 counter resolved `--repo .` relative to its own scratch child cwd, so the git extraction failed with “not a git repository” at the first measurement attempt | `.ufo/waves/round-77/receipts/control-baseline-r77.txt` first section (ERROR stage=setup) versus its final section (TARGET_MET) | the counter's own setup path, on the first run against the frozen bytes | `repo = os.path.abspath(args.repo)` before the scratch-cwd git calls (freeze v2 `a83e9bee`). Red-before: the retained first section prints the git error; green-after: `MADO_R77_BARFOOT … TARGET_MET`. |
| M77-3 | carried class (stale revision citation): round 76's SCORECARD row cites `5dade9b3` as its instrument's last change, while the file last changed at `3588a527` | round-76 verifier spot-check D2; `git log -1 --format=%H -- quality/counters/c2-r76-shapes.py` | the non-author closure (outside this lane) | append-only correction plus an executable cited-revision check (`R77ExecRepairs`) that fails on the r76 text and passes after the correction — the check is the first fix for this class that can fail on the defect itself. |
| M77-4 | line-anchor drift in my own draft entry: `2610-2620` / `2576-2581` were written before the exact grep, the measured anchors are `2609-2620` / `2575-2581` (add line `:2577`) | entry §1; `grep -n 'both_horiz\|positive_axis +=' src/render/Renderer.cpp` (no match at 2610/2576, matches at 2609/2577) | the pre-commit anchor sweep, not the claim counter | anchors corrected before commit; the re-derivation is the grep above, which prints nothing for the old numbers. |
| M77-5 | frozen fixture defect: the `left-vertical` case paired a 40x1440 live layer with a 1080-high monitor, so the correct tool reported `DIFFER` and the case scored `correct=no` | the first counter run at the fixture repo (15 cases, `left-vertical correct=no`); after the fix `15/15` | the counter itself — a wrong expectation cannot become a green measurement | fixture corrected to 40x1080 (`controls/make-cases-r77.py`), case set re-frozen before the wave. The old fixture reproduces the `no`; the new one the `yes`. |

Sweep for a sixth: `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py quality/counters/c1-r77-barfoot.py quality/counters/c2-r77-runbook.py` → no output (no deferred note in the round's instruments).

## Gate (sources opened this round)

All sources were opened 2026-11-04 before their rows were written; bytes under
`.ufo/waves/round-77/fetch/` with `sha256-r77.txt`. Census before: exit 0, 393 rows
(S001–S456, documented W04 duplicate-URL warnings). Census after: see the round report.

| row | source and locator | status | quote (≤25 words) | what it licenses / does not |
|---|---|---|---|---|
| S457 | Hyprland v0.56.2 `src/render/Renderer.cpp` @ efb5099, `arrangeLayerArray :2587-2670`, `applyExclusive :2529-2585`, `arrangeLayersForMonitor :2673-2700` | mined | `box.width = bounds.width - (PSTATE->margin.left + PSTATE->margin.right);` | the box/anchors/margin rule and the `exclusive + margin` add; it does not license a statement about a margined auto-zone composition |
| S458 | Hyprland v0.56.2 `src/debug/HyprCtl.cpp` @ efb5099, `layersRequest :647-700`, `reserved` template `:253`, print `:281-282`, command `:2010` | mined | `sc<int>(m->m_reservedArea.left()), sc<int>(m->m_reservedArea.top())` | the reply shape and the reserved order; it does not say which surface set the zone |
| S459 | Hyprland v0.56.2 `src/desktop/reserved/ReservedArea.cpp` @ efb5099, `:19-35`, `:53-60` | mined | `m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size());` | the parent/child band; it does not license a per-consumer attribution |
| S460 | `wlr-layer-shell-unstable-v1.xml` @ efb5099, enum `:86-90`, `set_exclusive_zone :152-190` | mined | `The exclusive zone includes the margin.` | levels and the exclusive-zone contract; it is a contract, not host behaviour |
| S461 | installed `waybar(5)` 0.15.0, `BAR CONFIGURATION` (page lines 70/91/97/128/189) | mined | `Bar position, can be \fBtop\fR, \fBbottom\fR, \fBleft\fR, \fBright\fR.\&` | the declared placement keys and defaults; not what the compositor does with them |
| S462 | Waybar v0.15.0 `src/bar.cpp` @ 90b209ad, `:178-222`, `:232-233`, `:240`, `:355-361` | mined | `gtk_layer_auto_exclusive_zone_enable(gtk_window);` | margin precedence, namespace, size request, exclusive call; not gtk-layer-shell's internal zone arithmetic |
| S464 | gtk-layer-shell v0.10.1 `src/layer-surface.c` @ v0.10.1, auto-zone :264-292 | mined | `new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];` | the client-side auto zone adds the opposite-edge margin; it does not prove Hyprland's side of the addition (S457) |
| S463 | `https://wayland.app/protocols/wlr-layer-shell-unstable-v1` as served 2026-11-04 (147036 B) | rejected | `wlr layer shell protocol` (the page's own title text) | REJECTED: renders the protocol but pins no protocol/compositor revision, so it cannot ground a versioned 0.56.2 claim. Flip: a commit/tag pin for the rendered protocol. The pinned XML (S460) is the authoritative copy. |

## Notes

- The host join (§2 of the entry) is a read-only capture: `hyprctl layers -j` and
  `hyprctl monitors -j` into `fetch/`, no socket, no write.
- The tool's 15-case score, its five killed mutations and the live-echo control (8/15) are in
  `receipts/control-baseline-r77.txt`; the C2 twelve probes are in the same file.
- Addenda after the wave (`## Wave findings` and corrections) are appended, never rewritten.

## Wave findings (append-only; written as the seats settle)

- **R77ScoutSources (source reconnaissance).** The scout's anchor table licenses every modelled
  branch and names the gaps the declaration did not: F1 `monitors[].width/height` are pixel size
  while the layer box is logical (`HyprCtl.cpp:278` vs `Monitor.cpp:699-700`); F2 the auto branch
  is unreachable for a horizontal waybar bar because gtk-layer-shell zeroes only a double-anchored
  dimension; F5 a static `monitor … addreserved` band shifts the origin; F3 `mode` presets rewrite
  layer/exclusive at runtime; F4 centring rounding differs by 1 px on odd deltas; and its I2
  derivation shows the auto zone adds the *opposite*-edge margin, so `NOT_MODELLED` must trigger on
  any margin, not only the edge margin. The first two were behaviourally wrong for reachable
  configurations and are now **refused** by the tool (`UNMODELLED`, rc 3), with the red/green pair
  `receipts/repair-r77-tool-refusals.txt` (rc 1 before, rc 3 after for both fixtures); the rest
  are named in the entry §4. The scout also confirms `layer: bottom` + `exclusive: true` still
  reserves (source-licensed, case-unexercised) and that `name` is the namespace (code-only; the
  manual documents only the CSS class).
- **R77ConnSiblings (cross-lane scan).** No sibling lane claims the layer plane, the bar
  footprint or the runbook: 0 hits for `hyprctl layers` across 20 sibling repos, and the nearest
  neighbours (game-dev-2d's `clients -j` window evidence; audio's waybar process names in
  receipts) do not overlap. It measured the stale-revision-citation class at **nine instances in
  rounds 68–77**, including the r75→r76 back-to-back repeat, and confirmed the round's fix is the
  first in-class fix that is executable machinery rather than a one-time re-cite. Its caveat (a)
  — the check must land with a red/green pair — is now met: `quality/check-cited-revisions.py`
  lands as a registered probe that reads the r76 row itself: `cited-r76-red-row.txt` → `red` (mismatched=1)
  and `cited-r76-green-row.txt` → `green` (`receipts/cited-revision-check-r77.txt`, selftest 6/6), and its caveat (b) — an un-wired check
  decays — is carried to round 78 as the standing-gate move. `considerthese/2026-10-28.md`
  proposal 4 (the live-tool table) is still unimplemented and is deferred to round 78: absorbing
  it would change the ledger grammar and `quality/` bytes after the freeze.

## Mistakes (wave-found, appended)

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M77-6 | the C2 counter inherited the caller's environment but a non-interactive runner lacks `HYPRLAND_INSTANCE_SIGNATURE` and `OMARCHY_PATH`, so every `hyprctl`/`omarchy` probe failed with "not set" and the runbook scored 3/12 | `.ufo/waves/round-77/receipts/measurement-final-r77.txt` first C2 section (matched=3, "HYPRLAND_INSTANCE_SIGNATURE not set!") versus `receipts/repair-r77-c2-env.txt` (12/12) | the final measurement, run from a non-session shell rather than the session shell the runbook assumes | the counter now discovers the instance from `$XDG_RUNTIME_DIR/hypr/*/.socket.sock` and `OMARCHY_PATH` from the `omarchy` binary's own location, adding them only when absent; the red run is retained and the green run was executed with neither variable set. |

- **R77Critic (design falsification).** The design stands: C1 is a coverage move (no `barfoot`/
  `footprint` token at base; no prior counter reads the monitors band), the live-echo control is
  the cheapest sufficient rule (best alternative 8/15; best constant 5/15), and C1/C2 are
  causally separable (disjoint inputs, zero cross-references). Three findings are dispositioned:
  **F1** C2's predicate overclaims for two rows — the anchor binds the row's presence, not its
  sample text (`monitors-reserved` states no band value; `waybar-process` is shape-checked);
  corrected by an append-only erratum to the declaration's C2 limits, no byte change to the
  instrument, target or case set. **F2** the `reserved-wrong-edge` mutant's replacement carried a
  trailing comma, so the kill was a `TypeError` crash rather than an oracle verdict
  (`receipts/repair-r77-mutant-oracle.txt`: before-tuple → TypeError, after-dict → `reserved=DIFFER`
  on `host-top`); the replacement is now a valid dict and the counter re-scores 5/5 killed with
  oracle-based verdicts. **F3** the declaration's source provenance was uncommitted at the
  critic's scan; it landed at `3e35d0a9` and the final tip is checked in §Landed. Watch items:
  W1 `binds-count`/`monitors-size` are operator-volatile (re-measure after any change); W2 the
  `row=` field prints the anchor, so `omarchy-version` shows the theme row (cosmetic, noted here).

- **R77RevBytes (byte fidelity).** All seven fetch receipts and the live join re-derive
  byte-identically; C1 15/15 and C2 12/12 reproduce at the tip. Four defects found and fixed:
  (1) the `mado-r77-barfoot` gate row put `reserved=NOT_MODELLED` under exit 0 while the tool
  returns `UNMODELLED` rc 3 — the row now maps NOT_MODELLED to exit 3; (2) the tool docstring
  claimed `mode` presets and static `addreserved` bands are "refused" while no code path refused
  them — a `mode: hide` config scored CLEAN (receipt `receipts/repair-r77-mode-refusal.txt`:
  before rc 0 CLEAN, after rc 3 `UNMODELLED`), the docstring now separates refused from
  not-modelled and a `mode` key is refused; (3) the entry attributed waybar's anchor clearing to
  Hyprland's branch — it now names `bar.cpp:422-424` for the clearing and `Renderer.cpp:2609-2620`
  for the centring; (4) the lesson's S463 quote was not literal on the page — the title text is
  `wlr layer shell protocol`; and the S458/S460/S462/S461 quotes are now single-line literal fragments of the stored
  bytes (`S461.txt:91` for the troff line), not whitespace-normalized readings. The static-`addreserved` limit stays named, not refused: the reply cannot
  separate static from dynamic reserve, and the docstring says so.

## Registry used-by updates (round 77, in-place, logged old → new)

The `used-by` cell is the only registry cell changed in place this round (CORPUS.md rule 2).
Each change adds an entry that already cites the row; the used-by counter
(`quality/counters/c3-r56-used-by.py --detail`) listed the missing pairs, and the landings receipt
re-runs it.

| row | old | new |
|---|---|---|
| S435 | corpus/lessons/round-66.md,corpus/knowledge/landing-kill-credit-real-children-r70.md,corpus/knowledge/kill-credit-exit-disagreement-r71.md | corpus/lessons/round-66.md,corpus/knowledge/landing-kill-credit-real-children-r70.md,corpus/knowledge/kill-credit-exit-disagreement-r71.md,corpus/knowledge/outcome-verdict-gate-summary-r72.md,corpus/knowledge/summary-credit-own-detail-r72.md |
| S441 | corpus/knowledge/landing-kill-credit-real-children-r70.md,corpus/lessons/round-70.md,corpus/knowledge/kill-credit-exit-disagreement-r71.md | corpus/knowledge/landing-kill-credit-real-children-r70.md,corpus/lessons/round-70.md,corpus/knowledge/kill-credit-exit-disagreement-r71.md,corpus/knowledge/control-set-mutant-kill-r73.md,corpus/knowledge/outcome-verdict-gate-summary-r72.md,corpus/knowledge/replay-witness-credit-r74.md,corpus/knowledge/summary-credit-own-detail-r72.md |
| S442 | corpus/knowledge/kill-credit-exit-disagreement-r71.md,corpus/lessons/round-71.md,corpus/knowledge/summary-credit-own-detail-r72.md | corpus/knowledge/kill-credit-exit-disagreement-r71.md,corpus/lessons/round-71.md,corpus/knowledge/summary-credit-own-detail-r72.md,corpus/knowledge/outcome-verdict-gate-summary-r72.md |
| S444 | corpus/knowledge/outcome-verdict-gate-summary-r72.md | corpus/knowledge/outcome-verdict-gate-summary-r72.md,corpus/knowledge/control-set-mutant-kill-r73.md,corpus/knowledge/replay-witness-credit-r74.md |
| S448 | corpus/knowledge/guard-carrier-global-environ-r73.md | corpus/knowledge/guard-carrier-global-environ-r73.md,corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md |
| S455 | corpus/knowledge/interprocedural-del-r76.md | corpus/knowledge/interprocedural-del-r76.md,corpus/knowledge/outcome-field-r76.md |
| S463 | — | corpus/knowledge/bar-footprint-r77.md |
