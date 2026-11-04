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
| S458 | Hyprland v0.56.2 `src/debug/HyprCtl.cpp` @ efb5099, `layersRequest :647-700`, `reserved` template `:253`, print `:281-282`, command `:2010` | mined | `sc<int>(m->m_reservedArea.left()), sc<int>(m->m_reservedArea.top()), sc<int>(m->m_reservedArea.right()), sc<int>(m->m_reservedArea.bottom())` | the reply shape and the reserved order; it does not say which surface set the zone |
| S459 | Hyprland v0.56.2 `src/desktop/reserved/ReservedArea.cpp` @ efb5099, `:19-35`, `:53-60` | mined | `m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size());` | the parent/child band; it does not license a per-consumer attribution |
| S460 | `wlr-layer-shell-unstable-v1.xml` @ efb5099, enum `:86-90`, `set_exclusive_zone :152-190` | mined | `A positive zone is the distance from the edge in surface-local coordinates to consider exclusive.` | levels and the exclusive-zone contract; it is a contract, not host behaviour |
| S461 | installed `waybar(5)` 0.15.0, `BAR CONFIGURATION` (page lines 70/91/97/128/189) | mined | `Bar position, can be top, bottom, left, right.` | the declared placement keys and defaults; not what the compositor does with them |
| S462 | Waybar v0.15.0 `src/bar.cpp` @ 90b209ad, `:178-222`, `:232-233`, `:240`, `:355-361` | mined | `if (mode.exclusive) { gtk_layer_auto_exclusive_zone_enable(gtk_window); }` | margin precedence, namespace, size request, exclusive call; not gtk-layer-shell's internal zone arithmetic |
| S463 | `https://wayland.app/protocols/wlr-layer-shell-unstable-v1` as served 2026-11-04 (147036 B) | rejected | `wlr-layer-shell-unstable-v1 protocol` (page title) | REJECTED: renders the protocol but pins no protocol/compositor revision, so it cannot ground a versioned 0.56.2 claim. Flip: a commit/tag pin for the rendered protocol. The pinned XML (S460) is the authoritative copy. |

## Notes

- The host join (§2 of the entry) is a read-only capture: `hyprctl layers -j` and
  `hyprctl monitors -j` into `fetch/`, no socket, no write.
- The tool's 15-case score, its five killed mutations and the live-echo control (8/15) are in
  `receipts/control-baseline-r77.txt`; the C2 twelve probes are in the same file.
- Addenda after the wave (`## Wave findings` and corrections) are appended, never rewritten.
