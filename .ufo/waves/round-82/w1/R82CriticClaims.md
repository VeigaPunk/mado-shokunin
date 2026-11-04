# R82CriticClaims — round-82 claims under attack

Seat: critic (read-only). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Frozen declaration: `.ufo/waves/round-82/claims-declaration-r82.md` (freeze `780c30fc`,
base `6ea2386d`). Scratch: `/fast/scratch/hyaku/mado-r82/R82CriticClaims` (attacks only;
no lane file was written except this report).

Lane drift while reviewing (facts, not verdicts): HEAD moved `780c30fc` → `b6146ee6` →
`89acb06c` (E1 redaction/TMPDIR) → `57789ab6` → `df6c613d` (reviewer row-cell corrections) →
`12e6ad57` (E2 non-resolved-namespace refusal). At `780c` the frozen hashes verify exactly:
c1 counter `1e9f394d…`, c1 controls `e404bb3f…`, c2 counter `1e8eb499…`, c2 controls
`f64d7d5d…`, tool `38007528…`. At HEAD the c2 counter/controls are `a87bceab…`/`07599b24…`
and the tool is `58ef4f6a…`.

## Reproduced before attacking (both claims, both tip states)

- C1 at `780c` and at `12e6ad57` (with the E2 tool): `cases=47 correct=47 mutants=34 killed=34
  base_correct=39/47 carried=39/39 tool_selftest=133/133 verdict=TARGET_MET`; counter selftest
  `84/84`.
- C2 at `12e6ad57` with the E1 controls: `cases=29 executed=29 matched=29 shapes=24/24
  anchors=29/29 rows=29/29 control_new=0/3 mutants=25 killed=25 verdict=TARGET_MET tree=bound`;
  frozen counter selftest `90/90`, current counter selftest `90/90`. The frozen receipt at
  `780c` (controls `f64d7d5d`) records the same predicate.

So the declared predicates are true. The two attacks below are against what the predicates
*prove*, not against the green.

## C1 — verdict: REJECT as a counter-backed claim

**Sentence vs code (frozen tool).** Items 1–4 of the claim map to
`tools/mado-barfoot.py`: `parse_allocation` `:436-453`, `band_of` `:456-471`,
`declared_box` `:474-511`, the composition resolver `:802-803`. The measured code at both
`38007528` and `58ef4f6a` is the honest resolver: a positive declaration wins, else the map
value, else a model refusal; a negative is a setup refusal. The claim's *words* are
implemented.

**Counterexample 1 — the band source is not forced.** Six added lines around
`local = declared_box(bar, usable["w"], usable["h"], allocation)` (and around the
composition's `bar_spec[band_axis] = band_of(...)`): if the bar's band axis is declared 0
*and* the allocation is positive, replace the map value with the layers reply's `h`/`w`
before the resolver. The declared allocation is then only a positivity gate; the band is the
arranged box. Result on the frozen tool and on the E2 tool: `correct=47/47`,
`mutants=34/34 killed`, `base=39/47`, tool selftest `133/133`. The counter cannot tell this
from the claim.

**Counterexample 2 — the join's comparison is unexercised.** No case in the frozen 47 has
`box=DIFFER`; every `LIVE` entry matches the modelled box. Mutating
`tools/mado-barfoot.py:1025` (`box_verdict = "MATCH" if live_box == box else "DIFFER"`) to
`box_verdict = "MATCH"` still scores **47/47 — the mutant survives**. The same is true of
the composition's `NOT_APPLIED` branch (`reserved-verdict-blind`). The claim's item 3 ("the
arranged box is the allocation too") is consequently untested: the `box=MATCH` in the
receipts is a fixture echo. The knowledge entry already says this (`corpus/knowledge/
bar-footprint-allocation-r82.md` §5.1: the eight cases' replies are built to the derivation,
so `box=MATCH` is "a fixture echo, not that check"), but the declaration offers the 47/47 as
the claim's proof, so the claim is not established by its instrument.

**Impacted axis:** coverage. The dynamic-band class is modelled correctly; what fails is the
evidence that the *declared* allocation is the band source rather than the observed box.

**Smallest safe fix (next freeze, data only — no tool change):** add one case
`alloc-live-band-differs` — config `{"position":"top","layer":"top","height":0}`; layers
`h=40` at `0,0,3440,40`; monitors `reserved [0,34,0,0]`; allocation `{"waybar":34}`; expect
`{"rc":1,"box":"DIFFER","reserved":"EQ","band":34,"expected":34,"verdict":"DIFFER"}` — and
add `box-verdict-blind` (anchor `:1025`) to `MUTATIONS`. Verified: the honest tool prints
`box=DIFFER reserved=EQ band=34 expected=34 verdict=DIFFER` rc 1; the live-box cheat prints
`box=MATCH reserved=DIFFER band=34 expected=40`; the blind mutant fails the same case. If a
case is not added, the claim must be re-scoped to "the allocation input is validated and the
band equals the arranged box on consistent fixtures" — weaker than the declaration.

**Secondary instrument defect:** `quality/counters/c1-r82-allocation-band.py:405` parses
`--no-mutants`, but the mutant loop at `:468` is unguarded; running with the flag still ran
all 34 mutants. Guard the loop (as the C2 counter does) or drop the flag.

**Disclosed, not new:** the declaration's S481 locator `set_size :116-123` points at the
request's opening, not the zero clause; the pinned bytes have `set_size` `:122-137` (zero
clause `:128-131`) and the configure zero sentence `:347-348`. `corpus/lessons/round-82.md:86`
and `:97` already disclose this; the claim's substance is unaffected.

## C2 — verdict: ADMIT (named corrections)

**Sentence vs code.** The three rows exist at `SKILL.md:274-276` at HEAD (273–275 at
`780c`), one per class: `busctl --user list` (owner), `busctl --user introspect …`
(census), `… | awk '$2=="method"'` (method table). All are read-only; each case's
`skill_anchor` equals its row and binds exactly one row; 29 anchors are distinct. The kill
rule is the declared one: live output + samples + negatives (`case_correct`), single
binding, tree bytes (`SKILL.md`, tool, listed fixtures), mutants. The held r81 instrument
exits 2 at this section (receipt).

**Corrections, none of which overturn the claim:**

1. **Redaction (real, already fixed by E1).** The frozen controls `f64d7d5d` carried the live
   account name, the unique bus name `:1.56`, and `user@1000.service` in the `tray-owner`
   samples/negatives — 6 hits in the controls and the maker at `780c`; the redacted file
   (`07599b24`) has 0. The frozen claim's controls hash is the unredacted file; the closure
   should quote the redacted hash or disclose the substitution.
2. **Frozen table cells (already fixed at `df6c613d`).** `tray-methods` third cell said
   `1 / 3` while the controls carry 2 samples / 3 negatives (now `2 / 3`); the `tray-owner`
   cell said "1..4194304" while the matcher is `(?m)^org\.kde\.StatusNotifierWatcher\s+
   [1-9][0-9]*\s` — ≥1, no upper bound, and no sample above the ceiling (now "non-zero
   decimal … the process-table ceiling is the live read's own bound"); chords `2 / 7` → `2 / 8`.
3. **Predicate tautology (open).** `control_new=0/3` is true by construction: `held_rule`
   returns False whenever the case has no `frozen` key (`:438-442`), and the three new cases
   never have one. The declaration says so ("by construction, printed as an observation"),
   but the term sits in the predicate. Drop it from the predicate, or replace it with the
   held instrument's setup refusal (already a real control in
   `receipts/control-c2-held-instrument-r82.txt`).
4. **Cosmetic.** `rows=29/29` and `anchors=29/29` print the same quantity (`len(bindings)`,
   `:750-752`); the section's row count is enforced by a setup check. `tray-interface` uses
   `re.search` (existence), so "one … interface line" is not count-enforced; say "an …
   interface line" or add a negative with two interface lines.

**Neutralized do-nothing attack.** A trivial row cannot reach 29/29: the case set freezes
each anchor and each shape, so the three commands must exist as rows and must run. The only
material cheap change (loosening the shapes) is blocked by the frozen `value` fields, which
are specific to the tray plane.

## Causation separability

- **C1 without C2:** the C1 counter reads only `tools/mado-barfoot.py` at `--rev` and its own
  controls; it never reads `SKILL.md`. C1 can land and be measured with C2 absent.
- **C2 without C1:** the four `refuse-*` rows execute the lane's join on round-79 fixtures and
  pass with the **r81 base tool** (rc 3, `stage=model` each, verified); the other 25 rows do
  not invoke the tool. The C2 tree binding requires the tool bytes at the measured rev, but
  not the r82 `--allocation` feature, so a tree carrying the r81 tool plus the r82
  `SKILL.md` section would score 29/29. C2 can land with C1 absent.
- **No axis harmed either way:** the r82 tool leaves the four refusal rows at rc 3; the C2
  landing touches only `SKILL.md`. The C1 `--allocation` input is additive.

## Axis names

- C1 "coverage" moves the dynamic-band **class** (a declared zero band resolved from the
  client's allocation) — a modelled class, not a number.
- C2 "operability" moves three runbook **row classes** (bus-name owner, interface census,
  method table), each a command plus a shape.
- The surfaces are disjoint (tool model vs runbook rows); neither landing mutates the other's
  surface. The only coupling is the join's four refusal rows, and their rc/stage is unchanged
  by C1 (verified base and r82).

## Open limits

- I did not run the frozen C2 counter's full battery from a clean `780c` checkout (a mutating
  checkout is out of this seat); I used the frozen receipt plus the current counter at
  `12e6ad57`. The frozen C2 counter at `780c` now correctly refuses from the current tree
  (`ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)`);
  that is the tree check working, not a claim failure.
- The held r81 instrument's setup refusal is taken from the round's receipt; my re-run with
  the r82 flags printed its usage message (different CLI), not the section refusal.
- The C1 attack is a candidate-input attack on the case set, not a claim that the measured
  tool is dishonest: `tools/mado-barfoot.py` at `38007528`/`58ef4f6a` does implement the
  declared resolver. The defect is the instrument's discriminating power.

STATUS: defect — `quality/counters/c1-r82-allocation-band.py` (`MUTATIONS`, no band-source
or box mutant), `tools/mado-barfoot.py:1025` (`box_verdict` never exercised; the
`box-verdict-blind` mutant survives 47/47), and the missing `box=DIFFER` case: the C1 target
is reachable with the arranged box, not the declared allocation, as the band source.
