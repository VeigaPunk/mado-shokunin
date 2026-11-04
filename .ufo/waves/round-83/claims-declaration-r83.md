# mado round 83 — declared claims (frozen before measurement)

Lane: **mado**. Round: **83** (attempt 1). Lane base: `67dd2b667b72f7f72309340d488b355d543841a5`
(`master`, clean; `jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0`).
Round axes: **coverage** (C1) and **operability** (C2) — two claims, one axis each, causally
separable (each counter runs on its own committed bytes and neither reads the other's).

## C1 — coverage: every declared layer surface's band resolves from the allocation map

**Before.** At the base, `tools/mado-barfoot.py` generation `r82-v1` resolves *only the bar's*
band. An `--allocation` entry naming any other declared surface is a setup refusal
(`only the bar's band is resolved`), and a non-bar surface with a dynamic band
(`height = 0` horizontal, `width = 0` vertical) is arranged over the usable box by the legacy
zero-size branch (explicit exclusive) or refused (auto zone).

**After.** Every declared surface's band axis resolves from the map: an allocation entry for
a declared namespace is that surface's own band (both the arranged box and gtk-layer-shell's
auto zone, `S464:276`/`:282`), a zero entry is refused (`was allocated a 0 … band`), an entry
naming a namespace no declared surface carries stays a setup refusal, and a dynamic band with
no entry keeps the two classes the lane already froze — the auto-zone arm that needs the band
is refused (`S464:276`, carried `auto-dynamic-band-refused`), and an explicit zone keeps the
compositor's assign branch, the box spanning the usable axis (`S470:2610-2637`, carried
`auto-left-dock`). The freeze drives the new resolution through the composition path, so the
surface's band also shrinks the usable box for later surfaces. The first freeze attempt
(`4e48d8e7`) refused the unallocated explicit-zone class and regressed the carried
`auto-left-dock` case (`correct=54/55`); that is why the freeze now keeps that branch — the
carried set is the evidence, and the instrument was corrected before any measurement was
cited. Two further corrections followed the same discipline, each before a measurement was
accepted: the survivors `alloc-composition-ignored` and `box-verdict-blind` (measurement at
`4208c24a`: `correct=55/55 mutants=38 killed=36`) showed that one resolution site was
duplicated and that the single-bar reader was unexercised, so the duplicate up-front
`band_of` call was deleted (dead code, the M82-1 class) and the case set grew the single-bar
and composition readers plus the two bar-refusal cases. The instrument's own mutations are
the reason three of these holes were found before the wave ran.

**Frozen control set.** `.ufo/waves/round-83/controls/c1-cases-r83.json`, sha256
`e4409dabcf74f32307f14b31afb85091bca7d584771076bdb9a3b336bc9512c4` — the 47 round-82 cases
carried parsed-equal plus 11 new: six on the new class (`extra-dyn-band-top`, `-dock`,
`-bottom`, `-explicit`, `-zero-alloc`, `alloc-two-namespaces`) and five closing round-82
routed gaps — `alloc-live-band-differs` (V7's single-bar discriminator),
`alloc-live-box-differs-composed` (V7's composition reader), `alloc-bool-refused` (G1),
`bar-dyn-band-no-alloc` (the bar's own dynamic-band refusal) and
`bar-dyn-band-exclusive-false` (the same refusal where the auto zone cannot mask it). Generator: `.ufo/waves/round-83/controls/make-c1-cases-r83.py` (no tool run; every
expectation derived from S481/S464/S457/S470's arithmetic).

**Counter.** `quality/counters/c1-r83-surface-band.py`.

**Counting command** (run from the lane root; replay verbatim):

```sh
python3 -I quality/counters/c1-r83-surface-band.py --repo . --rev REV \
  --base-rev 67dd2b667b72f7f72309340d488b355d543841a5 \
  --controls .ufo/waves/round-83/controls/c1-cases-r83.json \
  --carried .ufo/waves/round-82/controls/c1-cases-r82.json --scratch-root DIR
```

**Predicate (one sentence, the same in this declaration, the counter's target clause and the
receipt's label).** Every one of the 58 frozen cases scores correct, every one of the 38 named
mutants is killed, the held r82 tool at the base scores exactly 52 of 58, the 47 round-82 cases
are carried parsed-equal, and the tool selftest is green; only then does the counter print
`verdict=TARGET_MET` with rc 0.

**Target line.** `MADO_R83_BARFOOT: cases=58 correct=58 mutants=38 killed=38 base_correct=52/58
carried=47/47 tool_selftest=136/136 verdict=TARGET_MET rev=<freeze> tool_sha256=<sha>`.

**Kill rule.** Any clause false → `verdict=TARGET_MISSED`, rc 1, reported as an honest stop;
no clause is edited after the freeze.

**Do-nothing control (pre-freeze receipt).** The held r82 tool extracted at the base scores
`base_correct=52/58` (`receipts/control-c1-r83-at-base.txt`): the five gap-closure cases pass
there by design (the r82 model already fixes the bar's band from the allocation, refuses a
boolean, refuses the bar's dynamic band, and reports a composed DIFFER), and all six new-class
cases fail. A tree that does nothing cannot reach 58.

**Causality (V7, the round-82 critic's routed gap).** `alloc-live-band-differs` supplies
allocation 34 and a live box of height 40: the model must report `box=DIFFER band=34
expected=34 reserved=EQ verdict=DIFFER` rc 1; its composition twin
`alloc-live-box-differs-composed` does the same with a `--surfaces` declaration so the
composition's own `boxes.append` reader runs. The mutants `box-verdict-blind-single` and
`box-verdict-blind` (each reader made to say `"MATCH"`) die on exactly those two cases. The band is the
declared allocation, never an echo of the observed box. `extra-alloc-ignored` (the map entry
unused for a non-bar surface) dies on `extra-dyn-band-top`, and `alloc-resolved-set-bar-only`
(the declared set narrowed back to the bar) dies on `alloc-two-namespaces`.

## C2 — operability: the tray state pair in the read-only runbook

**Before.** The runbook section `### Executable runbook rows (round 82)` carries 29 command
rows; the tray plane binds the watcher's bus-name owner, its interface census and its method
table only. No row reads the watcher's *state*.

**After.** Section `### Executable runbook rows (round 83)` carries 31 rows. The two new rows
bind the tray state pair, live on this host at 2 items and `b true` (probes 2026-11-04):

| Row | Shape |
|---|---|
| `busctl --user get-property … RegisteredStatusNotifierItems \| awk '{print NF-2}'` | bare integer 0..10000 — the array's entry count (`int_range`) |
| `busctl --user get-property … IsStatusNotifierHostRegistered` | `b true` / `b false` — a boolean literal (new `bool_property` class) |

The property names and D-Bus types are `S482:13-21` (`as`, `b`); the terse `as N …` and
`b true` output shapes are `S484` (`man busctl`, "Terse and Verbose Output"). The count row
projects to the entry count so no item's session-bus address enters the output.

**Frozen control set.** `.ufo/waves/round-83/controls/c2-runbook-cases-r83.json`, sha256
`a0fba389676a87f2ceaf4933535057587b4ba7f1b2e0b63c00de256df3ae3f86` — the 29 round-82 cases
carried with one declared supersession (`waybar-pgrep`'s churn and negative samples' live
PID, the round-82 F1 remainder) plus the two new cases. Generator:
`.ufo/waves/round-83/controls/make-c2-cases-r83.py`.

**Counter.** `quality/counters/c2-r83-runbook.py`.

**Counting command** (run from the lane root; replay verbatim):

```sh
python3 -I quality/counters/c2-r83-runbook.py --repo . --rev REV \
  --controls .ufo/waves/round-83/controls/c2-runbook-cases-r83.json \
  --carried .ufo/waves/round-82/controls/c2-runbook-cases-r82.json --scratch-root DIR
```

**Predicate (one sentence, the same in this declaration, the counter's target clause and the
receipt's label).** All 31 frozen cases execute and match, all 26 shape-bound rows are good,
all 31 section rows are bound by exactly one case, all 27 named matcher mutants die, and the
working tree is the measured revision's bytes; only then does the counter print
`verdict=TARGET_MET` with rc 0.

**Target line.** `MADO_R83_RUNBOOK: cases=31 executed=31 matched=31 shapes=26/26 anchors=31/31
rows=31/31 superseded=waybar-pgrep mutants=27 killed=27 verdict=TARGET_MET rev=<freeze>
tree=bound`.

**Kill rule.** Any clause false → `verdict=TARGET_MISSED`, rc 1; a setup error prints rc 2 and
no contract line.

**Do-nothing control.** The held r82 instrument run against the freeze tree stops at its own
section check — `the runbook section carries 0 command rows, frozen target expects 29` (rc 2,
`receipts/control-c2-r82-at-r83.txt`). A tree that adds no rows cannot reach 31. The round-82
V8 tautology is gone: the summary has no `control_new` clause; the named control is the held
instrument's setup refusal, and `superseded=waybar-pgrep` is printed rather than silent.

## Round-82 routed defects carried into this round

| Id | Disposition this round |
|---|---|
| V1 (no vertical-band mutant) | `alloc-width-lost` added; dies on `alloc-dyn-width-dock` |
| V7 (no causal proof of the allocation as band source) | `alloc-live-band-differs` + `box-verdict-blind` |
| V8 (tautological `control_new` clause) | removed; held-instrument refusal named as the control |
| V9 (`--no-mutants` parsed but ineffective) | fixed in the successor C1 counter: the loop is guarded and the run prints `verdict=MUTANTS_SKIPPED`, never a kill claim |
| G1 (bool allocation unexercised) | `alloc-bool-refused` case added |
| G2 (object accepted as an array reply) | counter selftest regression: an object never satisfies `array_fields` |
| G3 (`stage=` prefix accepted) | counter selftest regression: the stage token is exact, `stage=setupx` is refused |
| F1 remainder (live PID in a carried sample) | declared supersession `waybar-pgrep` (fixture PID 4242) |
| D1–D10 (round-82 spot-check) | dispositioned in the round report; D1/D5 corrected append-only in the corpus, D2/D3/D6–D10 restated with the corrected values in the report |

## Freeze

`jj-lane.sh commit` of the instruments (tool, both counters, both control sets, both
generators, the SKILL.md section, the ledger rows) and this declaration. The measured revision
is the helper's `landed <hash>`; the two receipts record it plus the tool/counter sha256s.
