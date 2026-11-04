# mado round 81 — frozen claims declaration

Lane: mado-shokunin. Round: 81 (hyaku run 15, attempt 1). Base revision:
`c702094ace5dd9b2b5e152951b4b2f4dd578f8b6` (lane `master` tip at round start; clean:
`jj-lane.sh state` → `local=remote=c702094a ahead=0 behind=0`) — the round-80 tool bytes are the same
blob at `dd4f844c` and at this base (`git rev-parse c702094a:tools/mado-barfoot.py
dd4f844c:tools/mado-barfoot.py` → both `7b15eda6…`).

This file is written **before any round data** and is the frozen contract for the round: predicate,
counter, kill rule and target below are not rewritten after a seat scores. Both instruments were
validated pre-freeze on a throwaway sandbox clone under `/fast/scratch/hyaku/mado-r81/sandbox`
(commits `9dd96085`, `457a9b9a`, `1dd44e95`; never in the lane): C1 `TARGET_MET` with
`base_correct=33/39`, C2 `TARGET_MET` with `control_new=0/2` and `23/23` mutants. That green is a
construction check, not the measurement below. Two claims, two distinct axes (coverage, operability).
No exploratory claim. The round also repairs the seven defects the round-80 closure routed and runs
the §2b frontier step.

## Round shape

ONE v1 wave, 8–16 seats (`ufo-wave-policy.json`, band 8–16, run-15 block), ≥25 % attack seats by the
policy list (reviewer, critic, mutation-tester, labrat; the sentinel is a security seat and is named
separately), at most 2 connector seats. The L1 holds the canonical planner seat (the validator
rejects `planner`); the bounded planning data-walk rides a scout/connector item.

## C1 — coverage: the composition's overflow rounding and its auto-zone gate

**Claim.** The bar-footprint join models the four reachable classes round 80 recorded as
`NOT_MODELLED` (`corpus/knowledge/bar-footprint-composition-r80.md` §11), each on the source that
states it:

1. **`CBox::round`'s coupled rounding.** Hyprland centres in doubles (`Renderer.cpp:2613`) and then
   rounds the box once (`:2660`); hyprutils rounds the origin first and the far edge's distance from
   that origin second (`src/math/Box.cpp:51-63`), so a box one pixel wider than its bounds at the
   layout origin lands at `x=-1, w=1002`, not the round-80 model's `x=0, w=1001` (integer floor
   division on the offset).
2. **The auto zone on a dynamic band.** gtk-layer-shell's auto zone is the *allocation's* band size
   (`layer-surface.c:276-286`); the join has no input for the client's allocation, so a declared
   `height = 0` (or `width = 0` on the vertical gate) with `exclusive = auto` is a **named model
   refusal**, never a zero band.
3. **The auto gate.** gtk sends a zone only when exactly one of `horiz = (LEFT == RIGHT)` and
   `vert = (TOP == BOTTOM)` holds (`:269-288`), so a corner, a parallel pair and an all-four anchor
   set send **no** zone even where an explicit `exclusiveEdge` would match a compositor rule.
4. **The vertical gate and its band.** A left/right-anchored surface's auto zone is the allocation
   *width* plus its unanchored horizontal margins (`:279-286`), so a left dock's band reaches
   `applyExclusive`'s left rule and the attribution vector's left cell, not the bar's top.

The round-80 entry named this ground `NOT_MODELLED`; the frozen thirty-three cases never cross it.

**Instrument.** `tools/mado-barfoot.py` generation `r81-v1` (selftest `121/121`). **Counter.**
`quality/counters/c1-r81-overflow-auto.py` (selftest `72/72`, sha256 `22405133…`).

**Counting command — identical at the after and the before revision:**

```sh
python3 -I quality/counters/c1-r81-overflow-auto.py --repo . \
  --rev REV --base-rev c702094ace5dd9b2b5e152951b4b2f4dd578f8b6 \
  --controls .ufo/waves/round-81/controls/c1-cases-r81.json \
  --carried .ufo/waves/round-80/controls/c1-cases-r80.json --scratch-root DIR
```

**Frozen set.** `.ufo/waves/round-81/controls/c1-cases-r81.json` (sha256 `ab8154a1…`, 39 cases): the
thirty-three round-80 cases carried **parsed-equal, field for field, first** (asserted by the
counter), plus six new cases, every expectation derived from the sources above, not from a tool run:
`overflow-tie-negative` (the 1001-wide panel: `x=-1, w=1002`, band 26), `auto-dynamic-band-refused`
(model refusal, rc 3), `auto-corner-edge` (corner pair + `exclusiveEdge: top`: no zone, band 26),
`auto-all-four-edge` (all four + edge: no zone, box `400,363,200,100`), `auto-parallel-edge`
(`top|bottom` + edge: no zone), `auto-left-dock` (a level-1 left dock, width 40 auto: `left:40` in
the attribution vector, the bar's box shifted to `40,0,960,26`).

**Mutants (28, each a single-anchor literal mutation killed iff it scores < 39).** The twenty-two
round-80 mutants carried in semantics, two of them re-pointed at the renamed bounds-selection line
(`if spec["exclusive"] == -1:` replaced `if zone == -1:` when the zone moved after the box), plus
six on the new ground: `tie-round-trunc`, `round-width-spec`, `auto-gate-open`, `auto-gate-and`,
`auto-axis-swapped`, `auto-dynamic-kept`.

**Predicate (one sentence, the same in this declaration, in the counter's code and in the receipt
label):** *the claim holds iff the successor counter prints `correct=39`, `killed=28`,
`base_correct=33/39`, `carried=33/33`, a green tool selftest, and `verdict=TARGET_MET` at the
measured revision, exit 0.*

**Kill rule.** Any of: `correct < 39`; `killed < 28`; `base_correct != 33`; `carried != 33/33`; a
red tool selftest → the claim fails and the round reports an honest stop.

**Do-nothing controls.** (a) The held round-80 tool at the base revision (`5b9e2930…`) scored by the
same counter on the same 39 cases: **33/39** — it passes its own thirty-three and fails all six new
cases (`receipts/control-c1-r81-at-base.txt`). (b) The cheapest skip of *this* claim — leaving the
tool unchanged — is the same run; it cannot reach 39. (c) The round-80 counter's own set (33 cases)
is the frozen prior generation and is not re-scored here.

## C2 — operability: the action column and the bar's pgrep state in the runbook

**Claim.** The read-only runbook gains two matcher classes, not just two rows. The keybindings row is
now bound on the **action column** that `omarchy-menu-keybindings --print` prints with
`printf "%-35s → %s\n"` (installed payload `:164`): `cut -c36-` yields ` → ` at a fixed column
because the chord is padded to 35, a non-empty trimmed action, and no second `→` inside the action —
so a missing separator, an empty action, a trailing space, an action containing the arrow, a short
reply and a failed run each fail while a changed bind set passes. The host payload does **not** escape
every ampersand (one live action carries a bare `&`), so the grammar binds the separator and the
action's shape, never the entity text: that falsification is committed as a positive sample. The
`pgrep -x waybar` row is bound on its **PID list and exit status together** (one or more decimal PIDs
in 1..4194304 with rc 0 while the bar runs; empty stdout with rc 1 while it does not; any other pair
fails), so the bar's own state is read from the pair instead of being frozen to a value that churns.
The round-79/80 entries bound the keybindings rows by the chord column and by an arrow shape only,
and the r80 table's `pgrep -x waybar | head -n 1` row is a fixed `int_range` that reads DIFFER the
moment the bar stops.

**Instrument.** `quality/counters/c2-r81-runbook.py` (selftest `88/88`, sha256 `1bc9ca40…`).

**Counting command** (identical at both ends; the base revision refuses with rc 2 because its SKILL.md
is not the measured rev's bytes — the declared before state):

```sh
python3 -I quality/counters/c2-r81-runbook.py --repo . \
  --rev REV --controls .ufo/waves/round-81/controls/c2-runbook-cases-r81.json \
  --carried .ufo/waves/round-80/controls/c2-runbook-cases-r80.json --scratch-root DIR
```

**Frozen set.** `.ufo/waves/round-81/controls/c2-runbook-cases-r81.json` (sha256 `ae7ee90e…`, 26
cases): the twenty-four round-80 cases with every field but `skill_anchor` carried unchanged (the
counter asserts each field; `skill_anchor` is the documented row text and is re-bound at the successor
heading), 26 distinct anchors; plus `keybindings-actions` (`action_column`, three samples and six
negatives) and `waybar-pgrep` (`pid_state`, three samples and six negatives).

**Mutants (23):** the sixteen round-80 matcher mutants carried (two re-pointed at the successor kinds
they now precede: `chord-min-chords-dropped` → `if kind == "action_column"`, `state-rc-blind` →
`if kind == "pid_state"`), plus seven: `action-prefix-blind`, `action-empty-accepted`,
`action-arrow-inside-accepted`, `pid-rc-blind`, `pid-numeric-blind`, `pid-zero-accepted`,
`pid-single-only`.

**Predicate:** *the claim holds iff the counter prints `executed=26`, `matched=26`, `shapes=21/21`,
`anchors=26/26`, `rows=26/26`, `control_new=0/2`, `killed=23`, `tree=bound`, and `verdict=TARGET_MET`
at the measured revision, exit 0.*

**Kill rule.** Any of: `matched < 26`; `shapes < 21`; a row bound twice or by no case; any carried
case field changed; `control_new != 0`; `killed < 23`; the working tree's SKILL.md or tool bytes
differ from the measured revision's → the claim fails.

**Do-nothing controls.** (a) The held round-80 instrument on the successor set exits 2 (`control set
carries 26 cases, frozen target expects 24`) — `receipts/control-c2-held-instrument-r81.txt`. (b) The
held r78 fixed-value rule has no frozen value for the two new rows (`control_new=0/2`); `control_all`
is an observation over all 26 cases and never a predicate. (c) The round-80 counter at the base
revision cannot read the successor SKILL.md's command rows (row count 26 ≠ 24).

## Repairs of the round-80 closure's routed defects (append-only record, not claims)

1. **D1** — report corrections this round are appended errata naming the superseded text, never
   rewrites of filed bytes.
2. **D2** — `SHONEN.md` box 1's pointer is re-filed from `SKILL.md:786-789` to the r80–r81 registry
   rows' actual lines at the landing tip.
3. **D3** — every pointer this round is measured at the landing tip with `grep -n` and pasted with its
   line number.
4. **D4** — the blank line before M80-6 in `corpus/lessons/round-80.md` is removed so the six-row
   table renders as one table.
5. **D5** — the report names every seat and states the artifact count explicitly.
6. **D6** — the attack share is stated by the policy list; the sentinel is named separately.
7. **D7** — the wave-done line has a committed receipt (`receipts/wave-done-r81.txt`).

## Frontier step (§2b)

`corpus/SOURCES.md` census at round start: 412 rows, `sources-census.sh validate --root …
mado` exit 0 (standing W04 duplicate-URL warnings). Two rows opened and pinned this round
(`fetch/S478.bin`, `fetch/S479.bin`, manifest `fetch/sha256-r81.txt`): **S478** = hyprutils v0.14.0
`src/math/Box.cpp` (the `CBox::round` and `CBox::empty`/`containsPoint` arithmetic), **S479** =
Hyprland `CMakeLists.txt` at `efb50993…` (`set(HYPRUTILS_MINIMUM_VERSION 0.14.0)`, the pin that
licenses the tag). C1 cites S478; the round's mistake and its Gate block live in
`corpus/lessons/round-81.md`.
