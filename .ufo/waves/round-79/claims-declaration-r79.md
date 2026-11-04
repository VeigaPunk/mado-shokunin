# mado round 79 — frozen claims declaration

Lane: mado-shokunin. Round: 79 (hyaku run 15). Base revision:
`e4b153dfa4a67ca56f7ec65cb6639082451626a7` (lane `master` tip at round start, clean:
`jj-lane.sh state` → `local=remote=e4b153df, ahead=0 behind=0 tracked=0 untracked=0`).

This file is written **before any data** and is the frozen contract for the round: predicate,
counter, kill rule and target below are not rewritten after a seat scores. Two claims, two
distinct axes (coverage, operability). One exploratory claim is not used. The round also
repairs three defects the round-78 closure routed (revision self-description, before-command
reproducibility, the frontier row count) and runs the §2b frontier step (SOURCES curation,
one mined mistake, one sourced claim).

## Round shape

ONE v1 wave, 8–16 seats (`ufo-wave-policy.json`, band 8–16, run-15 block), ≥25 % attack
seats, at most 2 connector seats. The L1 holds the canonical planner seat (the validator
rejects `planner`); the bounded planning data-walk rides the scout/connector items.

## C1 — coverage: the static `addreserved` reserve composes with the bar's own band

**Claim.** The bar-footprint join models a second exclusive consumer on the same edge as a
*composition* instead of an unexplained `GT`: the static reserved area a
`monitor = NAME, addreserved, TOP, BOTTOM, LEFT, RIGHT` rule declares is read from the same
config tree (`--rules`), the bar is arranged inside the static-reduced usable box, and the
expected band is `static[edge] + extent + opposite margin`. The round-78 entry named this
ground `NOT_MODELLED` (`corpus/knowledge/bar-footprint-margins-r78.md` §limits).

**Instrument.** `tools/mado-barfoot.py` generation `r79-v1`. **Counter.**
`quality/counters/c1-r79-reserve.py`.

**Counting command — identical at the after and the before revision** (the counter reports an
absent mutant anchor as `not killed`, never a setup error, so the base revision yields a
verdict rather than an rc 2 — closing the round-78 closure's D2):

```sh
python3 -I quality/counters/c1-r79-reserve.py --repo . \
  --rev REV --base-rev e4b153dfa4a67ca56f7ec65cb6639082451626a7 \
  --controls .ufo/waves/round-79/controls/c1-cases-r79.json \
  --carried .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root DIR
```

**Frozen set.** `.ufo/waves/round-79/controls/c1-cases-r79.json`: 23 cases — the eighteen
round-78 cases carried unchanged (the counter asserts the parsed prefix equals the round-78 set field-for-field) plus five new:
`static-composed` (static 26 + margined bar 34 = 60, EQ), `static-other-edge` (static left 40
moves the box, not the top band), `static-exclusive-false` (would-be band printed as
`static + bar`, `NOT_APPLIED`), `static-last-wins` (two `addreserved` for M1, one for M2; the
newest M1 rule and only M1's selector apply), `static-source-refused` (a `source =` line
refuses the join, `stage=model`). Every expectation is derived from the sources, not from a
tool run.

**Mutants (12, each a single-anchor literal mutation killed iff it scores < 23).** The seven
round-78 mutants (opposite-margin-dropped, horizontal-margin-leak, level-bottom-swap,
right-extent-flip, per-side-margin-dropped, negative-margin-accepted, opposite-edge-wrong)
plus five on the new term: static-dropped, static-order-swapped, static-first-wins,
static-box-unoffset, static-selector-ignored.

**Predicate (one sentence, the same in this declaration, in the counter's code and in the
receipt label):** *the claim holds iff the successor counter prints `correct=23`,
`killed=12`, `base_correct=18/23`, `carried=18/18`, a green tool selftest, and
`verdict=TARGET_MET` at the measured revision, exit 0.*

**Kill rule.** Any of: `correct < 23` (an expectation the tool misses), `killed < 12` (a
single-anchor misreading survives), `base_correct != 18` (the do-nothing tool reaches the
target), `carried != 18/18` (a frozen round-78 case moved), a red tool selftest → the claim
fails and the round reports an honest stop.

**Do-nothing control (the cheapest skip):** the base revision's tool (the round-78 model,
`tool_sha256=1bceb514…`) scored by the same counter on the same 23 cases. Receipt:
`.ufo/waves/round-79/receipts/control-c1-r79-at-base.txt` —
`cases=23 correct=18 mutants=12 killed=4 base_correct=18/23 tool_selftest=28/28
verdict=TARGET_MISSED` rc 1. The control misses the five new cases (it has no `--rules`) and
eight of the twelve mutants; it cannot reach 23/23. The 28/28 selftest is also the measured
disproof of the round-78 docstring's stale `22/22` example (routed defect 1).

## C2 — operability: the runbook executes per-row bindings, refusals and the keybindings shape

**Claim.** The read-only runbook becomes executable per row: each of the 22 cases owns a
distinct SKILL.md row whose command cell equals the case's command, the four documented model
refusals of `tools/mado-barfoot.py` (a `mode` preset, a scaled monitor, the `background`
layer, a spaced output pattern) are executed against committed fixtures and scored on their
own exit status and refusal stage, and the `omarchy menu keybindings --print` row is bound by
shape (≥100 lines, every line an arrow line) so a changed bind set passes while a truncated or
arrow-less reply fails. The round-78 entry bound three cases to one row and executed none of
these five.

**Instrument.** `quality/counters/c2-r79-runbook.py`.

**Counting command** (identical at both ends; the base revision refuses with rc 2 because the
working tree is not its bytes — the declared before state):

```sh
python3 -I quality/counters/c2-r79-runbook.py --repo . \
  --rev REV --controls .ufo/waves/round-79/controls/c2-runbook-cases-r79.json \
  --carried .ufo/waves/round-78/controls/c2-runbook-cases-r78.json --scratch-root DIR
```

**Frozen set.** `.ufo/waves/round-79/controls/c2-runbook-cases-r79.json`: 22 cases — the
seventeen round-78 cases with their command, expectation (`kind`/`value`), churn samples,
negative samples and `frozen` value unchanged (the counter asserts every field but
`skill_anchor`), twenty-two distinct anchors, plus four `refusal` cases over the committed
fixtures and one `lines_shape` case. **Mutants (9):** the five round-78 matcher mutants plus
refusal-stage-blind, refusal-rc-blind, lines-any-line, lines-min-lines-dropped.

**Predicate:** *the claim holds iff the counter prints `executed=22`, `matched=22`,
`shapes=17/17`, `anchors=22/22`, `rows=22/22`, `control_new=0/5`, `killed=9`,
`tree=bound`, and `verdict=TARGET_MET` at the measured revision, exit 0.*

**Kill rule.** Any of: `matched < 22`; `shapes < 17`; a row bound twice or by no case; any
round-78 carried field changed; `control_new != 0`; `killed < 9`; the working tree's SKILL.md
or tool bytes differ from the measured revision's → the claim fails.

**Do-nothing controls.** (a) The held round-78 instrument on the successor set exits 2
(`control set carries 22 cases, frozen target expects 17`) — receipt
`.ufo/waves/round-79/receipts/control-c2-heled-instrument-at-base.txt`. (b) The held r78 rule
(rc 0 and output equal to one frozen value) has no frozen value for the five new cases, so it
matches `control_new=0/5` by construction; `control_all` is printed as an observation over all
22 cases and is never a predicate (host-state dependent by nature).

## Frontier step (§2b) — frozen here

One new entry `corpus/knowledge/bar-footprint-reserve-r79.md` citing two rows opened this
round: **S465** (`src/output/Monitor.cpp` — `m_reservedArea.setStatic(m_activeMonitorRule.
m_reservedArea)` and `logicalBoxMinusReserved`) and **S466** (`src/desktop/reserved/
ReservedArea.cpp` — `calculate()` sums the static initial box with every dynamic type). Both
fetched byte-identically at `efb5099…` (`fetch/sha256-r79.txt`). S457/S458/S459/S460/S461/
S462/S464 re-opened and re-fetched byte-identically (S462's raw URL 404'd at that commit; its
r78 byte-identical pin is reused and the fact is not load-bearing this round). Mined mistake:
the round-78 C1 `--no-mutants` before-command (recorded in the lesson). One sourced claim:
C1, above.

## Unfreeze prohibition

No seat may rewrite `tools/mado-barfoot.py`, the two counters, the two control sets, the
fixtures or this declaration. Seats return findings and draft files; the L1 integrates.

## Repair R1 (append-only; after the `5eb8f20f` measurement, wave seat R79ScribeEntry F1)

The frozen run at `5eb8f20f` scored 23/23, but its model credited an `addreserved` area that the
handler drops when no same-selector rule exists: `handleMonitor` writes the area only into an
existing rule (`ConfigManager.cpp:1331`) and, with none, falls through to `add(parser.rule())`
(`:1341`) where the parser holds only the selector (`Parser.cpp:92-101`). The tool was repaired
(an `addreserved` with no prior rule now leaves a zero reserve; selftest 43 → 44 assertions) and
the four static fixtures gained the prior positional rule their expectation presupposes; no
expectation, label, mutant or target moved, and the twenty-three cases score 23/23 on the
repaired bytes with twelve mutants killed (`receipts/measurement-c1-r79-repair.txt`). The
pre-repair fixture set scores 20/23 against the repaired tool, so the fixture change is
load-bearing (`receipts/repair-r79-c1-oldfixtures.txt`). Named limit: the fall-through rule is
asserted in the tool selftest only — no frozen case covers it, so a mutant that credits it would
survive. The frozen 23/23 at `5eb8f20f` stands as the measurement of the bytes at that revision;
the repaired measurement is the one the round reports as the capability.

## Correction (append-only; wording only, after the `5eb8f20f` measurement)

The C1 section said the eighteen round-78 cases are "carried byte-identically". The counter's check
is parsed equality: `cases[:18]` equals the round-78 set field-for-field (the generator re-serializes
the parsed cases, so the JSON text differs in key order and indentation while every value, including
every expectation, churn sample and negative sample, is identical). The predicate, counter, kill rule
and target are unchanged — `carried=18/18` means eighteen cases equal field-for-field — and the
landed prose in the lesson, SCORECARD, SKILL registry row and report says "carried unchanged (parsed
equality)". Reported here because the frozen text said "byte-identically" and a closure that reads it
as a byte compare would find the successor file's bytes differ. Source: the L1's own re-read of the counter's
`cases[:CARRIED] == carried` check while preparing the report; no measurement moved.
