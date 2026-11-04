# mado round 82 — frozen claims declaration

Lane: mado-shokunin. Round: 82 (hyaku run 15, attempt 1). Base revision:
`6ea2386d49318a5f223097c78b5fe79c31b064f8` (lane `master` tip at round start; clean:
`jj-lane.sh state` → `local=remote=6ea2386d ahead=0 behind=0`). No earlier attempt of this
round exists (`.ufo/watchdog.log` carries `launch mado round=82` and no
`lane-dead-no-report mado round=82`), so `.ufo/waves/round-82/` starts empty and nothing is
inherited.

This file is written **before any round data** and is the frozen contract for the round:
predicate, counter, kill rule and target below are not rewritten after a seat scores. Both
instruments were validated pre-freeze on a throwaway sandbox clone under
`/fast/scratch/hyaku/mado-r82/sandbox` (lane commits `2dad6c01`, `1bb580ad`; never in the
lane): C1 `cases=47 correct=47 mutants=34 killed=34 base_correct=39/47 tool_selftest=133/133
TARGET_MET`; C2 `cases=29 executed=29 matched=29 shapes=24/24 anchors=29/29 rows=29/29
control_new=0/3 mutants=25 killed=25 TARGET_MET`. That green is a construction check, not the
measurement below. Two claims, two distinct axes (coverage, operability). No exploratory
claim. The round also repairs the six defects the round-81 closure routed and runs the §2b
frontier step.

## Round shape

ONE v1 wave, 8–16 seats (`ufo-wave-policy.json`, band 8–16, run-15 block), ≥25 % attack seats
by the policy list (reviewer, critic, mutation-tester, labrat; the sentinel is a security
seat and is named separately), at most 2 connector seats. The L1 holds the canonical planner
seat (the validator rejects `planner`); the bounded planning data-walk rides a scout or
connector item.

## C1 — coverage: the client's own band

**Claim.** The bar-footprint join models the class round 81 refused — a declared dynamic
band (`height = 0` on a horizontal surface, `width = 0` on a vertical one) — by accepting the
client's own allocation as a declared input (`--allocation {namespace: band}`), on the source
that states it:

1. **A zero size is the client's own** (`wlr-layer-shell-unstable-v1.xml` `set_size`
   `:116-123`, S481 opened this round): the compositor's desired size is not the band, the
   client's allocation is.
2. **The auto zone is that allocation** (gtk-layer-shell `layer-surface.c:276`/`:282`, S464
   held and re-opened): `self->current_allocation.height` / `.width` plus the unanchored
   margins of the band axis, so a dynamic bar's zone is the band it was allocated.
3. **The arranged box is the allocation too**, and the declaration wins when it is positive:
   the model resolves the band axis through one resolver (`band_of`), refuses an absent or
   zero allocation (never a guessed band), refuses a negative one as an invalid declaration
   (stage=setup), and refuses an allocation naming a namespace the composition does not
   carry.
4. **The composition path uses the same resolver** for the bar's band, so the bar's pass
   reserves the allocated band and the later surfaces arrange under it.

The round-81 entry named this ground `NOT_MODELLED`/refused; the frozen thirty-nine cases
never cross it.

**Instrument.** `tools/mado-barfoot.py` generation `r82-v1` (selftest `133/133`).
**Counter.** `quality/counters/c1-r82-allocation-band.py` (selftest `84/84`), frozen
controls `.ufo/waves/round-82/controls/c1-cases-r82.json` (39 carried + 8 new, sha256
`e404bb3f…`) built by `controls/make-c1-cases-r82.py` from cited arithmetic, not from a tool
run.

**Counting command — identical at the after and the before revision:**

```sh
python3 -I quality/counters/c1-r82-allocation-band.py --repo . \
  --rev REV --base-rev 6ea2386d49318a5f223097c78b5fe79c31b064f8 \
  --controls .ufo/waves/round-82/controls/c1-cases-r82.json \
  --carried .ufo/waves/round-81/controls/c1-cases-r81.json --scratch-root DIR
```

**Predicate.** `cases=47 correct=47 mutants=34 killed=34 base_correct=39/47 carried=39/39
verdict=TARGET_MET` (rc 0). **Kill rule.** One case wrong, one mutant surviving (an absent
anchor counts as not killed), a carried set that is not parsed-equal, or a base score other
than 39/47 → `TARGET_MISSED`. **Target.** 47/47 on the frozen set.

**Do-nothing control (frozen before data).** The held round-81 tool (`a129a435…`, the blob at
the base) scores `correct=39/47` on this set: the eight new cases are unreachable without the
allocation input, so the target is not one a do-nothing control can reach.

## C2 — operability: the tray plane in the runbook

**Claim.** The read-only runbook gains the tray plane as three executable row classes, each
bound to its own command and to a shape rather than a frozen value:

1. the `StatusNotifierWatcher`'s bus-name owner (`busctl --user list`: an
   `org.kde.StatusNotifierWatcher` line whose PID column is a decimal in 1..4194304 — a
   zero, a dash or a failed command is not an owner);
2. its interface census (`busctl --user introspect … /StatusNotifierWatcher`: one
   `org.kde.StatusNotifierWatcher interface` line — a property or method line is not the
   interface);
3. the method table that census prints (`… | awk '$2=="method"'`: every line `.Name method`,
   at least two lines — one row or a mixed line is not the table).

S482 (opened this round) grounds the bus name and the register calls; the shapes were
measured against the live bus on 2026-11-04 (`org.kde.StatusNotifierWatcher  1720  waybar`).

**Instrument.** `quality/counters/c2-r82-runbook.py` (selftest `90/90`); frozen controls
`.ufo/waves/round-82/controls/c2-runbook-cases-r82.json` (26 carried + 3 new, sha256
`f64d7d5d…`). **Counting command:**

```sh
python3 -I quality/counters/c2-r82-runbook.py --repo . --rev REV \
  --controls .ufo/waves/round-82/controls/c2-runbook-cases-r82.json \
  --carried .ufo/waves/round-81/controls/c2-runbook-cases-r81.json --scratch-root DIR
```

**Predicate.** `cases=29 executed=29 matched=29 shapes=24/24 anchors=29/29 rows=29/29
control_new=0/3 mutants=25 killed=25 verdict=TARGET_MET tree=bound` (rc 0). **Kill rule.** A
command whose live output does not meet its row, a churn sample that stops matching, a
negative that matches, an unbound or doubly bound row, a tree that is not the measured
revision's bytes, or a surviving mutant → `TARGET_MISSED`. **Target.** 29/29.

**Do-nothing control (frozen before data).** The held round-81 instrument cannot score this
table: its `SECTION` is `### Executable runbook rows (round 81)`, so at the round-82 tree it
exits 2 (setup refusal), and the held fixed-value rule has no frozen value for any of the
three new rows (`control_new=0/3` by construction, printed as an observation).

## Frontier step (§2b)

- `corpus/SOURCES.md` census at round start: `sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin mado` → exit 0, 415 rows (`receipts/census-start-r82.txt`).
- One sourced claim: C1 rests on S481 (layer-shell protocol `set_size`), opened this round;
  C2 rests on S482 (StatusNotifierWatcher), opened this round.
- One mistake mined into `corpus/lessons/round-82.md` `## Mistakes`, with a sweep if none.
- Assimilation: the shokuknow package is checked read-only; `Assimilation: none` is reported
  if nothing is admitted (the round-81 state: 94 id collisions, no staged entry on this
  round's ground).

## Repairs carried from the round-81 closure

R1 (five empty attack seats → this wave's attack items must write an artifact or the round
reports the gap), R2 (round-81 disclosure written into the round-80 section → round-82
corrections go in the round-82 section), R3 (C2 counter docstring drift → the r82 counter
carries the r82 contract line), R4 (selftest tallies lack receipts → `--selftest`
transcripts land under `receipts/`), R5 (round-80 D1–D3 erratum), R6 (wave counts carry a
counting command in the report).
