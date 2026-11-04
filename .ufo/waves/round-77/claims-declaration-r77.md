# mado round 77 — frozen claims declaration

Lane: mado-shokunin · round 77 · attempt 1 · 2026-11-04 · hyaku run 15.
Base: `aeeef067bd63672dfc681d6dacc3797f53ffd1f9` (round-76 verifier spot-check tip).
This file is written and committed before any measurement and before the wave is dispatched.
The predicates below are the sentences the counters implement and the receipts print; a
predicate changed after a seat has scored is not this round's predicate.

## Round shape

ONE v1 wave of 12 seats under `scripts/hyaku/ufo-wave-policy.json` (band 8–16): 4 executors,
2 scribes, 1 scout, 1 connector, 1 reviewer, 1 critic, 1 mutation-tester, 1 revenger; attack
seats = reviewer + critic + mutation-tester + revenger = 4/12 (33 %, policy floor 25 %). The L1
holds the planner seat (the validator rejects `planner` as a swarm role); no planner is dispatched.
Residual: none planned.

## Claims

### C1 — coverage: the bar-footprint chain becomes a measured join

**Surface moved.** The compositor layer plane as a *joined* surface: the declared waybar
configuration → the bar's live layer box in `hyprctl layers -j` → the monitor's `reserved`
band in `hyprctl monitors -j` → the usable area the bar takes. The lane held the bar's module
semantics (MADO-R3-1) and point-sample layer reads; it held no instrument that derives the
footprint from the declaration and separates agreement from drift, and no tool reads the
reserved-band join at all. This is one new surface with a durable read-only tool
(`tools/mado-barfoot.py`, `VERSION r77-v1`) and a frozen case set.

**Predicate (the one sentence).** On the fifteen frozen case artifacts, the extracted tool's
published `box=`, `reserved=` and `verdict=` fields and its exit status equal the frozen
expectation on 15/15 cases, five named single-anchor mutations of the join rule are each killed
by at least one case, the naive live-echo control scores below the target, and the tool's own
selftest passes 18/18.

**Counting command.**

    cd /home/vgpnk/Projects/shokunin/mado-shokunin
    python3 -I quality/counters/c1-r77-barfoot.py --repo . --rev REV \
      --controls .ufo/waves/round-77/controls/c1-cases-r77.json \
      --scratch-root /fast/scratch/hyaku/mado-r77/c1

**After-state sentence (receipt label).**

    MADO_R77_BARFOOT: cases=15 correct=15 mutants=5 killed=5 base_correct=8/15 \
      tool_selftest=18/18 verdict=TARGET_MET rev=<hash>

**Target.** `correct == 15`, `killed == 5`, `base_correct < 15`, `tool_selftest == 18/18`, rc 0.

**Do-nothing control (built and scored before the freeze).** The cheapest control that skips the
claimed work is a live-echo rule, implemented inside the counter: read the declared layer level,
report `MATCH` whenever a `waybar` entry exists there, report `EQ` whenever the monitor's band on
the declared edge is positive, and never model the configuration, margins, centring or drift.
It scores `base_correct=8/15` (misses `css-margins`, `drift-box`, `drift-reserved`,
`output-excluded`, `wrong-edge-band`, `malformed-layers`, `per-side-margin`): it cannot reach the
target, so the counter measures the join, not the dump. The receipt is the `MADO_R77_BASE` line in
`.ufo/waves/round-77/receipts/control-baseline-r77.txt`.

**Named limits (declaration, not afterthoughts).** List-valued waybar configs, dynamic (`0`)
height/width on the non-anchored axis where Hyprland's auto branch applies, list/`*` output
patterns, transforms, multiple bars per config, layer-rule effects, and the gtk-layer-shell auto
exclusive-zone composition when the bar's edge margin is non-zero (`NOT_MODELLED`) are outside
the model; the tool refuses or names them, never guesses. The reserved band is read as
`[left, top, right, bottom]` (HyprCtl.cpp monitors reply).

**Sourced ground.** C1 cites `S457`–`S462`, opened 2026-11-04 in the round's Gate: Hyprland
v0.56.2 `arrangeLayerArray`/`arrangeLayersForMonitor` and the `layers`/`monitors` reply builders;
the wlr-layer-shell level/anchor semantics; the installed waybar 0.15.0 manual (`position`,
`layer`, `height`, `width`, `margin`, `exclusive`) and `bar.cpp`'s anchor/margin/exclusive code.
The counter runs committed bytes only and never touches the host.

### C2 — operability: the read-only probe table executes end-to-end

**Surface moved.** The SKILL.md *Read-only probes* table (line 204 ff.) was a dated record
("all executed 2026-10-14 unless cited"), not an executable checklist: no frozen expectation set,
no command that runs the table as a batch, and no separation of "the row exists" from "the probe
ran and produced the stated outcome". This claim makes the table executable end-to-end on the
returned host: twelve rows, one frozen expectation each, all bound to their committed table row.

**Predicate (the one sentence).** The counter runs all twelve frozen probe commands, and for
every case the observed outcome equals the expectation the bound SKILL.md row states (12/12), with
12 executed, 0 unexecuted, and 12/12 anchors present in the committed SKILL.md at the measured
revision.

**Counting command.**

    cd /home/vgpnk/Projects/shokunin/mado-shokunin
    python3 -I quality/counters/c2-r77-runbook.py --repo . --rev REV \
      --controls .ufo/waves/round-77/controls/c2-runbook-cases-r77.json

**After-state sentence (receipt label).**

    MADO_R77_RUNBOOK: cases=12 executed=12 matched=12 unexecuted=0 anchors=12/12 \
      verdict=TARGET_MET rev=<hash>

**Target.** `executed == 12`, `matched == 12`, `anchors == 12`, rc 0.

**Do-nothing control (built and scored before the freeze).** The cheapest control that skips the
claimed work is "read the table": count a row as satisfied when its text occurs in SKILL.md. It
prints `MADO_R77_BASE: executed=0 matched_by_read=12/12 rule=read-the-table` — it never reaches
`executed=12`, so the counter measures execution, not mention. Receipt:
`.ufo/waves/round-77/receipts/control-baseline-r77.txt`.

**Named limits.** The probe set is the twelve rows whose stated outcome is a stable value on this
host; volatile values (process ids, the active workspace) are shape-checked or excluded, and the
exclusion is recorded here. The counter executes the frozen command list in the caller's session
environment (the table is a session-shell runbook; `hyprctl` needs the instance signature and
`omarchy` needs its own path variable) and prints only each probe's stdout. It is a point-in-time
run: a probe that changes state after the run is outside it. `grim` (screenshot) and journal
reads are excluded by scope, not failed.

## Distinct axes and the lowest-axis obligation

C1 = coverage, C2 = operability: two claims, two axes. At round start the published finite
sub-axes are all at their measured maximum (`MADO_AXIS_ROW navigation 95/95, calibration 86/86,
operability 12/12`, `MADO_AXIS: checked=3 mismatched=0` at the base revision), so no axis is
distinctly lowest; the dormant freshness value (9.6552, recorded host-absent since round 57) is
operator-owned and excluded from the tie. The lowest-axis obligation therefore does not select a
different claim this round; both claims are stated against their axis by the surface they change,
not by a number they produce.

## Routed defects carried from round 76 (dispositions; not claims)

D1 provenance trios in `corpus/knowledge/outcome-field-r76.md` and `interprocedural-del-r76.md`
→ append-only `## Correction (round 77)` block naming the missing fields and the rows.
D2 `SCORECARD.md:4339` stale C2 revision (`5dade9b3` → `3588a527`) → dated correction append with
the re-derivation command.
D3 `claims-declaration-r76.md:26` "fifteen-case" text and the stale mutant list/deprecated example
in `quality/counters/c1-r76-outcome-field.py` → appended errata plus a text-only docstring fix,
with a parity receipt showing the r76 counts unchanged.
D4 mistake-count defect (report says six, lesson holds five M76-1…M76-5) → corrected count named in
the lesson's `## Corrections (round 77)` block and the LOG entry, derived from the lesson rows.
D5 Stale-lane line → this round's report states the driver state explicitly.
D6 three untracked round-76 handoff files (`w1.ready`, `w1.ready.dispatched`, `w1-run.err`, 0 B)
→ committed with the round-77 wave evidence, disposition stated.
D7 report pointer arithmetic (`2308e12a` adds only the harm-watch receipt, census landed at
`e160d18e`) → named in the r76 lesson correction block with the `git diff --name-status` command.
D8 declaration pointer (tallies live at `w1/R76ExecC1/…`, not `receipts/`) → named in the same
correction block.

## No-harm plan

Gate selftest (`bash tools/mado-verify.sh --selftest`) unchanged at 460/460 or better and its bytes
untouched; index rows = knowledge files; tool-ledger population grows by the new instruments and
covers them; `check-axis-scores.py` re-derived at the landing tip; SOURCES census exit 0. No config
tree, compositor state, service, sibling repo or package transaction is written; host probes are
the read verbs on the SKILL runbook table plus the two `hyprctl` dumps captured for C1.

## Freeze

- Instruments and controls are committed at the freeze commit; the hashes below are re-measured by
  the counters and printed in every receipt (`MADO_R77_CONTROL: sha256=…`, `tool_sha256=…`).
- Frozen control sets: `controls/c1-cases-r77.json` (15 cases) and
  `controls/c2-runbook-cases-r77.json` (12 cases); the C1 set is generated by
  `controls/make-cases-r77.py` and both are committed with this declaration.
- Live captures used by the C1 evidence entry are committed under
  `.ufo/waves/round-77/fetch/` with their sha256 in the measurement receipt.

## Errata (round 77, append-only; never a re-freeze)

C2's predicate sentence says "the observed outcome equals the expectation the bound SKILL.md row
states". The anchor check binds the row's *presence*, not its sample text, and for two cases the
expectation is the frozen case value rather than a sample the row prints: `monitors-reserved`
(the probes row documents the command, not the band value) and `waybar-process` (the row's pid is
volatile; the case shape-checks `^[0-9]+$`, as the named limits already say). Two more cases carry a
written-form transform of the row's value: `monitors-size` compares the jq-rendered rate
`99.99700` (the row writes `99.997`), and `layers-namespaces` compares a sorted join of the
namespaces (the row lists them by level). The transforms are part of the frozen command text. The instrument,
predicate, target and case set are unchanged. Source: the wave critic's F1.

C1's sourced ground names S457–S462; S464 (gtk-layer-shell v0.10.1 `layer-surface.c`, the
client-side auto exclusive zone) was opened in the same round to ground the `NOT_MODELLED`
margin claim the entry makes, so the round's registry delta is seven mined rows plus one
rejected (S463), not six. The predicate, target and case set are unchanged.

## Post-freeze repairs (append-only; the freeze pins the predicate, not the bytes)

The freeze fixed the predicate, labels, targets and control sets; it did not freeze the instrument
bytes. During the wave the instruments were repaired, each with a red/green receipt and no change
to a predicate, label, target or control: the tool at `0fa69f41` (scale/transform and dynamic
cross-size refusals), `bbca7469` (mode-preset refusal), `2df46e29` (literal quote fragments and
the contract's anchor attribution) and `9197405c` (background-layer refusal); the C1 counter at
`de627316` (the `reserved-wrong-edge` mutant replacement is now a valid dict, so the kill is an
oracle verdict); the C2 counter at `4a17b31f` (session-env discovery) and `bce906f3` (the matcher
requires exit 0 — the frozen matcher's rc-blindness is finding F2). The final measurement pins the
repaired bytes (`receipts/measurement-final-r77.txt`, C1 counter `de627316`, tool `9197405c`, C2
counter `bce906f3`), and the control sets are byte-identical to the freeze. Readers must pin a
revision; "frozen" here never means "HEAD".

C2's `anchors=12/12` clause is a pre-loop gate (the counter aborts before running if an anchor is
missing), so the printed value cannot fall; nine distinct SKILL.md rows carry the twelve cases, and
`omarchy-version` is bound to the shared `omarchy theme current` / `omarchy version` row. The
binding claim is that every case's row exists at the measured revision, which the gate checks; the
counter's printed count is not an independent measurement (reviewer F4).
