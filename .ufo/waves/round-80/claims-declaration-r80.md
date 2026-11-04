# mado round 80 — frozen claims declaration

Lane: mado-shokunin. Round: 80 (hyaku run 15). Base revision:
`e10f7e9f528b13195a1cdde28a68a702af3045c4` (lane `master` tip at round start, clean:
`jj-lane.sh state` → `local=remote=e10f7e9f, ahead=0 behind=0 tracked=0 untracked=0`).

This file is written **before any round data** and is the frozen contract for the round:
predicate, counter, kill rule and target below are not rewritten after a seat scores. The
instruments were validated pre-freeze on a throwaway sandbox clone under
`/fast/scratch/hyaku/mado-r80/sandbox` (commits `6c9872d0`…`fd08027f`, never in the lane);
their green there is a construction check, not the measurement below. Two claims, two
distinct axes (coverage, operability). One exploratory claim is not used. The round also
repairs the five defects the round-79 closure routed and runs the §2b frontier step.

## Round shape

ONE v1 wave, 8–16 seats (`ufo-wave-policy.json`, band 8–16, run-15 block), ≥25 % attack
seats, at most 2 connector seats. The L1 holds the canonical planner seat (the validator
rejects `planner`); the bounded planning data-walk rides the scout/connector items.

## C1 — coverage: a second exclusive layer surface composes under the running usable box

**Claim.** The bar-footprint join models **N declared layer surfaces**, not one: each is
arranged against the usable box the earlier surfaces already shrank
(`Renderer.cpp:2673-2700`), an empty arranged box is skipped (`:2655-2658`), each
exclusive surface's shrink is *attributed* to that surface by `applyExclusive`'s first
matching edge (`:2529-2586`), and the whole layer reserve is dropped when the surviving
box is empty or not contained in the static-reduced box (`ReservedArea.cpp:19-31`). The
join prints the per-surface attribution (`MADO_BARFOOT_ATTR:`) beside the compositor's
own `reserved` array, so ATTRIBUTED and GT are separate values that must agree. The
round-79 entry named this ground `NOT_MODELLED` (`corpus/knowledge/bar-footprint-reserve-r79.md`
§limits: "a band overflow on the cross axis" and no second consumer).

**Instrument.** `tools/mado-barfoot.py` generation `r80-v1`. **Counter.**
`quality/counters/c1-r80-multisurface.py`.

**Counting command — identical at the after and the before revision:**

```sh
python3 -I quality/counters/c1-r80-multisurface.py --repo . \
  --rev REV --base-rev e10f7e9f528b13195a1cdde28a68a702af3045c4 \
  --controls .ufo/waves/round-80/controls/c1-cases-r80.json \
  --carried .ufo/waves/round-79/controls/c1-cases-r79.json --scratch-root DIR
```

**Frozen set.** `.ufo/waves/round-80/controls/c1-cases-r80.json`: 33 cases — the
twenty-three round-79 cases carried unchanged (asserted parsed-equal field-for-field)
plus ten new: `overlay-compose-top` (level 3 arranged after level 2, 26 + 40 = 66),
`bottom-level-first` (level 1 first, so the *bar's own box* starts at y=40),
`same-level-order` (rule order 10 puts the panel before the bar; its anchored margin 6 is
part of the zone, 36 + 26 = 62), `exclusive-edge-matched` (anchor top|right + exclusive
edge top reserves 30), `anchor-unmatched` (the same mask with no exclusive edge matches no
rule and reserves nothing), `overlay-unexclusive-full` (exclusive -1 arranges against the
full monitor box), `ls-area-invalid` (a 2000 zone on a 800-high monitor voids the whole
layer reserve: GT 0 while ATTR 2026), `negative-margin-skip` (zone 12 + margin -12 fails
the `> 0` guard), `empty-box-skip` (an empty arranged box contributes nothing) and
`full-box-vs-usable` (exclusive -1 over a monitor whose bottom is also reserved: full-box
y=700, post-arrangement usable y=660). Every expectation is derived from the sources
above, not from a tool run.

**Mutants (22, each a single-anchor literal mutation killed iff it scores < 33).** The
twelve round-79 mutants (opposite-margin-dropped, horizontal-margin-leak,
level-bottom-swap, right-extent-flip, per-side-margin-dropped, negative-margin-accepted,
opposite-edge-wrong, static-dropped, static-order-swapped, static-first-wins,
static-box-unoffset, static-selector-ignored) plus ten on the composition: attr-edge-order,
running-bounds-ignored, exclusive-edge-ignored, edge-guard-dropped, invalid-area-kept,
full-box-uses-usable, empty-box-contributes, same-level-order-ignored,
zone-margin-not-added, attribution-not-summed.

**Predicate (one sentence, the same in this declaration, in the counter's code and in the
receipt label):** *the claim holds iff the successor counter prints `correct=33`,
`killed=22`, `base_correct=23/33`, `carried=23/23`, a green tool selftest, and
`verdict=TARGET_MET` at the measured revision, exit 0.*

**Kill rule.** Any of: `correct < 33`; `killed < 22`; `base_correct != 23`; `carried !=
23/23`; a red tool selftest → the claim fails and the round reports an honest stop.

**Do-nothing control (the cheapest skip):** the base revision's tool (the round-79 model,
`tool_sha256=9e274157…`) scored by the same counter on the same 33 cases. It has no
`--surfaces` input, so it cannot reach the ten new cases: 23/33 (dry run
`/fast/scratch/hyaku/mado-r80/sandbox` `fd08027f`; the committed receipt is
`receipts/control-c1-r80-at-base.txt`).

## C2 — operability: a chord grammar and a state/exit-status matcher in the runbook

**Claim.** The read-only runbook gains two matcher classes, not just two rows. The
keybindings row is bound on the **chord column** `omarchy-menu-keybindings` prints
(`printf "%-35s → %s"` over the twelve-mask table, with `code:201` → `COPILOT KEY` and the
mouse-button symbols): one to four distinct modifier words from SUPER/SHIFT/CTRL/ALT,
` + `, one key token, or a bare key — so a foreign modifier, a numeric mask, a repeated
modifier, a padded or doubled key, an arrow in the chord column, an empty line and a
truncated reply each fail while a changed bind set passes. The `systemctl --user is-active
hypridle` row is bound on its **state word and exit status together** (`active` ⇔ rc 0,
otherwise rc 3), so a state/status contradiction fails while the host flipping between
active and inactive does not. The round-79 entry bound the keybindings row by an arrow
shape only and executed no `is-active` row.

**Instrument.** `quality/counters/c2-r80-runbook.py`.

**Counting command** (identical at both ends; the base revision refuses with rc 2 because
the working tree is not its bytes — the declared before state):

```sh
python3 -I quality/counters/c2-r80-runbook.py --repo . \
  --rev REV --controls .ufo/waves/round-80/controls/c2-runbook-cases-r80.json \
  --carried .ufo/waves/round-79/controls/c2-runbook-cases-r79.json --scratch-root DIR
```

**Frozen set.** `.ufo/waves/round-80/controls/c2-runbook-cases-r80.json`: 24 cases — the
twenty-two round-79 cases with every field but `skill_anchor` unchanged (and every anchor
unchanged too), 24 distinct anchors, plus `keybindings-chords` (`chord_shape`, bound to the
new row `omarchy menu keybindings --print | cut -c1-35`, seven committed negatives) and
`hypridle-is-active` (`is_active`, bound to the new row `systemctl --user is-active
hypridle`, four committed negatives). **Mutants (16):** the nine round-79 matcher mutants
plus chord-mod-word-blind, chord-key-padded, chord-arrow-blind,
chord-mod-duplicate-accepted, chord-min-chords-dropped, state-rc-blind, state-enum-blind.

**Predicate:** *the claim holds iff the counter prints `executed=24`, `matched=24`,
`shapes=19/19`, `anchors=24/24`, `rows=24/24`, `control_new=0/2`, `killed=16`,
`tree=bound`, and `verdict=TARGET_MET` at the measured revision, exit 0.*

**Kill rule.** Any of: `matched < 24`; `shapes < 19`; a row bound twice or by no case; any
round-79 carried field changed; `control_new != 0`; `killed < 16`; the working tree's
SKILL.md or tool bytes differ from the measured revision's → the claim fails.

**Do-nothing controls.** (a) The held round-79 instrument on the successor set exits 2
(`control set carries 24 cases, frozen target expects 22`) — receipt
`receipts/control-c2-held-instrument-r80.txt`. (b) The held r78 fixed-value rule has no
frozen value for the two new rows (`control_new=0/2`); `control_all` is an observation over
all 24 cases and never a predicate.

## Repairs of the round-79 closure's routed defects (append-only record, not claims)

1. **D1** — the round-79 report's stale C1 after-cell (`tool_selftest=44/44` at `d6be05ef`)
   is corrected by an erratum in this round's report and by the lesson row M80-1; the r79
   claim itself is unaffected.
2. **D2** — `S467`'s rejection reason is narrowed by a **new row that supersedes it**
   (`supersedes S467 —`), since `SOURCES.md` is append-only.
3. **D3** — LOG.md's round-79 "Seven mined" count is corrected by an appended correction
   line (LOG is append-only).
4. **D4** — `.ufo/waves/round-79/fetch/S468.bin` and `S469.bin` are named in the lesson as
   fetched-but-unregistered files; new registry ids therefore start at **S470**, so no row
   retroactively blesses bytes no round opened.
5. **D5** — the round-79 partial seat (`R79ExecC1Tool` settled without a `.md`) stays an
   evidence gap; its `out.txt` (73 OK / 0 FAIL against the pre-R2 tool) is named in the
   lesson, never backfilled.

## Frontier step (§2b) — frozen here

One new entry `corpus/knowledge/bar-footprint-composition-r80.md` citing rows opened this
round: **S470** (`src/render/Renderer.cpp` — `applyExclusive` `:2529-2586`,
`arrangeLayerArray` `:2587-2671`, `arrangeLayersForMonitor` `:2673-2700`; byte-identical to
the round-78 pin `9af8a74e…`), **S471** (`src/protocols/LayerShell.cpp` — the request
handlers and the exclusive-edge/anchor error `:100-168`), **S472**
(`tests/desktop/Reserved.cpp` — the upstream unit test asserting the area arithmetic),
**S473** (the installed `omarchy-menu-keybindings`, own-work: the modmask table and
`printf "%-35s → %s"`), **S474** (the installed `systemctl` man page, systemd 262: the
`is-active` exit contract). Rows S457/S459/S466/S465 are re-opened and byte-compared.
Mined mistake: the round-79 orchestrator's own before-state class (an absent mutant anchor
reported as a setup error) and the round-79 closure's D1–D5, whichever the wave
substantiates. One sourced claim: C1 (S470/S471/S472) and C2 (S473/S474).

## Unfreeze prohibition

No seat may rewrite `tools/mado-barfoot.py`, the two counters, the two control sets, the
fixtures or this declaration. Seats return findings and draft files; the L1 integrates.

## Repair R1 (append-only; after the freeze measurement, wave seat R80ScribeEntry F1)

The composition path's `box=` field read `boxes[order.index(0)]`, but `boxes` is appended in
*arrangement-sequence* order (the exclusive pass, then the non-exclusive pass) while `order` is the
level/order-sorted list. The two positions coincide in every frozen case (all ten composition cases
use an exclusive bar and no non-exclusive surface sorts before it), so no case, expectation, mutant
or target moves; the field would misreport only for a non-exclusive bar with an exclusive surface
sorting after it (a reachable declaration the set does not carry). Repaired to
`boxes[sequence.index(0)]`; the r80 tool's `VERSION` stays `r80-v1` (the generation's contract is
unchanged) and the measured `tool_sha256` moves from `c3eb5fbe…` to the value the new receipts print.
A second, documentation-only repair in the same commit corrects the C1 counter's docstring contract
line (`cases=30 … base_correct=23/30` → `cases=33 … base_correct=23/33`); no executable constant or
branch changes.

## Repair R2 (append-only; after R1, L1 check of the C2 row on live bytes)

The `chord_shape` grammar rejected a line the formatter demonstrably produces: when
`parse_keycodes`' keymap cache has no symbol for a keycode, `parse_bindings` prints the chord as
`MODS + ` with no key. The L1 observed 41 such lines in one `omarchy menu keybindings --print`
invocation (the same 193-line reply, `SUPER +` in the chord column) and none in the next, so the
rendering is intermittent in the formatter's own keymap resolution — a churn class the row must
tolerate, not a regression. The grammar now treats a line ending ` +` as a chord with an empty key
(and still refuses a *padded* key, a doubled key, a foreign modifier, a numeric mask, a repeated
modifier and an arrow in the chord column). No case, sample, negative, expectation, mutant or target
moves; the counter's selftest gains one assertion (80 → 81) and the re-cut `chord-key-padded` mutant
drops the strip check only. The frozen `24/24` is re-measured at the repair tip.
