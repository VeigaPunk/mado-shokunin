# log-and-scorecard.md — seat R77ScribeSources (round 77)

Drafts of the LOG entry and the SCORECARD round-77 block, produced independently from the
committed receipts and this seat's own counter runs, then checked against the landed bytes
(`3e35d0a9`, HEAD `0fa69f41` at this writing). Both landed versions are correct in substance
and are reproduced here with the seat's corroboration; the one staleness the seat found in
the landed SCORECARD block is flagged at the end (also carried in
`lesson-round-77.md` ## Corrections).

## LOG entry (draft — mirrors the landed `## Round 77` entry)

- **Claims.** C1 coverage: the bar-footprint chain becomes a measured join —
  `tools/mado-barfoot.py` derives the declared waybar box (position/layer/height/width/margin/
  exclusive) and joins it to the live layer entry in `hyprctl layers -j` and the monitor's
  `reserved` band from `hyprctl monitors -j`; a frozen fifteen-case set scores
  `cases=15 correct=15 mutants=5 killed=5 base_correct=8/15 tool_selftest=18/18 TARGET_MET`
  at freeze `a83e9bee` (base `aeeef067`), with the live-echo control at 8/15
  (`receipts/control-baseline-r77.txt`). C2 operability: the SKILL.md read-only probe table
  executes end-to-end — twelve frozen expectations, each bound to its committed table row,
  `cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12 TARGET_MET` at the same freeze;
  the read-the-table control reports `executed=0`.
- **Host ground (read-only).** DP-1 3440x1440@99.997, waybar at layer level 2, box
  0,0,3440,26, reserved `[0,26,0,0]`, usable area y=26..1440; the bar declares `layer top`,
  `position top`, `height 26`, no margins, exclusive default. Captures
  `fetch/live-{layers,monitors}-r77.json` (sha256 `46eb2481…` / `e732af34…`); live join
  `MADO_BARFOOT … verdict=CLEAN`. No config tree, compositor state or service was written.
- **Sources.** SOURCES 393 → 400 rows: S457–S462 new (Hyprland `Renderer.cpp`, `HyprCtl.cpp`,
  `ReservedArea.cpp`, the layer-shell XML at efb5099; `waybar(5)` and Waybar 0.15.0
  `bar.cpp`), S463 opened and rejected (wayland.app, no revision pin). Census exit 0 with
  the documented W04 duplicate-URL warning for S458 (the HyprCtl.cpp URL is held at separate
  scopes by S158/S307/S320/S366/S389/S394); this seat re-ran the census at the tip
  (`receipts/census-scribe-r77.txt`).
- **Mistakes.** Five mined in `corpus/lessons/round-77.md` (M77-1…M77-5) plus the
  scribe-seat's three in its lesson draft (MS-1 = r76 D7 verified by this seat; MS-2/MS-3
  this seat's own).
- **Routed defects D1–D8 (round-76 spot-check).** Dispositioned append-only (D1 provenance
  trios; D2 SCORECARD revision correction; D3 declaration errata + r76 counter docstring
  parity; D4 mistake count; D5 stale-lane line; D6 handoff files; D7/D8 pointer corrections).
- **Registry and gate bookkeeping.** `quality/tool-ledger.md` 136 → 140 rows; SKILL.md Gate
  registry gains `mado-r77-barfoot`, `mado-r77-barfoot-counter`, `mado-r77-runbook`; index
  95 → 96 rows.
- **No-harm.** Gate `bash tools/mado-verify.sh --selftest` 460/460 at unchanged bytes; frozen
  r72–r76 instruments keep their base blob ids; axis table re-derived at the landing tip
  (navigation 96/96, calibration 86/86, operability 12/12, ledger 140/140); census exit 0.
- **Wave.** One v1 wave, 12 seats (attack share 4/12); seat outcomes per seat report.

## SCORECARD round-77 block (draft — mirrors the landed block)

Frozen declaration: `.ufo/waves/round-77/claims-declaration-r77.md`; freeze `e4717a1c`, freeze
v2 `a83e9bee` (C1 counter absolute-repo fix), pre-wave receipts `94b5afb1`; base
`aeeef067bd63672dfc681d6dacc3797f53ffd1f9`. Frozen control sets:
`.ufo/waves/round-77/controls/c1-cases-r77.json` (15 cases, sha256 `7d6e2b1a…`) and
`c2-runbook-cases-r77.json` (12 cases, sha256 `597b2302…`). Pre-freeze do-nothing controls:
the C1 live-echo rule scores `base_correct=8/15`; the C2 read-the-table rule reports
`executed=0` (`.ufo/waves/round-77/receipts/control-baseline-r77.txt`). Axis posture at round
start: navigation 95/95, calibration resolved-active 86/86, operability selftest 12/12 (no
axis distinctly lowest); the dormant freshness value (9.6552, host-absent) stays
operator-owned and is excluded from the tie. The stagnation nudge does not apply (last
capability r76, window N=3).

| Claim / axis | Counting command | Before → after | Verdict |
|---|---|---|---|
| C1 **coverage** — the bar-footprint chain (declared waybar config → live layer box → monitor `reserved`) becomes a measured join | `python3 -I quality/counters/c1-r77-barfoot.py --repo . --rev REV --controls .ufo/waves/round-77/controls/c1-cases-r77.json --scratch-root DIR` | at the base rev the join does not exist (0 layer-plane rows; the live-echo control scores 8/15); at `a83e9bee`: `cases=15 correct=15 mutants=5 killed=5 base_correct=8/15 tool_selftest=18/18 verdict=TARGET_MET` rc 0 — re-derived by this seat at the same rev (`receipts/measure-c1-scribe-r77.txt`, identical contract line); bounded `10 × 15/15` → 10.0000 on this finite set | improved on the frozen fifteen-case set |
| C2 **operability** — the SKILL.md read-only probe table executes end-to-end | `python3 -I quality/counters/c2-r77-runbook.py --repo . --rev REV --controls .ufo/waves/round-77/controls/c2-runbook-cases-r77.json` | at the base rev the table is a dated record (0 frozen expectations, 0 batch execution; the read-the-table control reports `executed=0`); at `a83e9bee`: `cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12 verdict=TARGET_MET` rc 0 — re-derived by this seat (`receipts/measure-c2-scribe-r77.txt`, identical contract line); bounded `10 × 12/12` → 10.0000 | improved |
| — | coverage / admitted-note reachability (`quality/check-index.py --repo . --rev REV`) | 95/95 at base → 96/96 at the landing tip (one new entry indexed) | improved (index) |
| — | operability / hermetic gate (`bash tools/mado-verify.sh --selftest`) | 460/460 both ends; the gate is byte-identical this round | unchanged (harm watch) |
| — | operability / instrument ledger (`quality/check-tool-ledger.py --repo . --rev REV`) | 136 rows at base → 140 rows at the tip, uncovered 0 (four new instruments) | improved (ledger) |
| — | calibration / held instruments (`git rev-parse <rev>:<path>`) | identical blob ids at base and tip for `tools/mado-verify.sh`, `quality/landing-counters.sh`, `check-tool-ledger.py`, `check-axis-scores.py`, `c1-r72/r73/r74/r75/r76-*`, `c2-r73/r74/r75/r76-shapes.py` (the r76 counter receives a docstring-text-only correction under D3, with a parity receipt) | unchanged (frozen) |

**Capability demonstrated**

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Bar-footprint join over the compositor layer plane | Predict a waybar bar's layer box from the declaration (position/layer/height/width/margin/exclusive), find the live entry in `hyprctl layers -j`, and separate MATCH from drift against the monitor's `reserved` band on a captured `hyprctl monitors -j`; name what it cannot model (margined auto exclusive zones; scaled/transformed and dynamic-cross monitors refused) | `.ufo/waves/round-77/measurement-final-r77.txt`; `tools/mado-barfoot.py`, `quality/counters/c1-r77-barfoot.py` | round 77 |
| Executable read-only probe runbook | Run the SKILL.md read-only probe table as one batch: 12 frozen expectations, each bound to its committed table row, with executed/matched/unexecuted reported separately so a table that is only read is not a probe | `.ufo/waves/round-77/measurement-final-r77.txt`; `quality/counters/c2-r77-runbook.py` | round 77 |

**Axis table re-derived at the landing tip:** navigation 96/96; calibration resolved-active
86/86; operability selftest 12/12, ledger 140/140.

## Seat flag on the landed block (for the L1)

The landed block's C1 row says "at `a83e9bee` (its instrument's last change)". After the
wave-found hardening commit `0fa69f41` (which modified `tools/mado-barfoot.py` and the entry,
receipt `repair-r77-tool-refusals.txt`), the instrument's last change is `0fa69f41`, not
`a83e9bee` — the D2/M77-3 stale-revision class recurring in-round. This seat re-measured C1
at `0fa69f41` (`receipts/measure-c1-scribe-at-0fa69f41.txt`); the L1 should append the
correction and final measurement at the closing tip.
