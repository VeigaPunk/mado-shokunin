# R56W3MutKillC3 — C3 survivor kill fixtures

## Attacked and scope

Attacked item: **C3 harness/counter kill power**. Scored source revision: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, never the working tree. Axes: discrimination, fixture fidelity, exact restoration.

Read the v2 claim/registration and w2 C3 harness report; v2 takes precedence. No frozen predicate, tracked lane source, counter, target or kill rule was changed. All mutant programs and mutation commits were scratch copies. These are **proposal fixtures**, not integrated controls. Findings requiring a new predicate/control route to round 57.

Deliverable root: `.ufo/waves/round-56/w3/R56W3MutKillC3/`.

## Results

### Harness: rebuild of the named w2 survivors

All 54 original mutant fragments occur exactly once in the tip harness. Its only source change since the w2 tested revision is the per-control scratch removal line.

The original A/B/C oracle was rerun (real counter, always-green counter, every-leg counter):

```
mutants=54 killed=29 survived=25 invalid=0
```

The survivor set is unchanged:

```
M10 M12 M13 M15 M23 M24 M25 M26 M27 M29 M30 M31 M32
M33 M35 M36 M37 M38 M41 M43 M44 M47 M49 M50 M52
```

The fourteen w2 proposed additions were materialized and exercised against pristine, mutant and byte-restored sources:

```
M13 M15 M24 M25 M26 M27 M29 M30 M32 M36 M37 M38 M44 M52
pristine PASS / mutant FAIL / restored PASS: 14/14
```

**Kill-level distinction matters.** M36/M37/M38 use an added no-op control on a harness COPY: pristine refuses it as ineffective (exit 2); the mutant proceeds and prints `control 10 noop-control: FAIL`, despite a green nine-control summary. M44 is diagnostic-only. M13/M15/M52 are parser/token unit assertions. M24/M25/M26/M27/M29/M30/M32 are control-construction/shape assertions over registry/entry/used-by data. These checks discriminate the mutants, but the latter eleven are **not new end-to-end frozen-control FAIL receipts**. Do not count them as such.

The remaining eleven survivors have byte-identical real-counter stdout AND stderr to pristine at tip (11/11): M10, M12, M23, M31, M33, M35, M41, M43, M47, M49, M50. This corroborates the prior equivalence arguments on this tree, not universal equivalence. M50 (180s→5s timeout) is particularly run-conditioned; the small scratch tree is not a loaded-host timing guarantee. No new killer was established for these eleven.

### Counter: additional bounded mutation probe

No other w2 mutation directory examined named mutants of `quality/counters/c3-r56-used-by.py`; the w2 counter seat had no report. This seat therefore constructed a clearly separate, exploratory 30-mutant table, not a purported reconstruction of nonexistent w2 counter evidence. R56W2MutC1CounterA DEF-2's C3-related token-width observation motivated CM08.

Oracle: unchanged C3 harness, with each counter COPY supplied via `--counter`.

```
mutants=30 killed=18 survived=12 invalid=0
survivors: CM01 CM03 CM04 CM06 CM07 CM08 CM11 CM12 CM19 CM25 CM27 CM28
```

Eleven fixtures discriminate eleven survivors, each with pristine PASS / mutant FAIL / restored PASS:

| Survivor | Fixture input | Actual decisive output |
|---|---|---|
| CM01 conflict dropped | Append allowlisted S005 entry to its used-by cell | pristine `missed=conflict`; mutant `missed=none` |
| CM03 exempt check dropped | Remove one allowlist row | pristine `missed=missing,allow_sha,exempt`; mutant lacks `exempt` |
| CM04 tables checksum leg dropped | Add a harmless JSON key to tables COPY | pristine `missed=tables_sha`; mutant `missed=none` |
| CM06 window 16 | Insert `source: S999` at line 16 | pristine `dangling=0`; mutant `dangling=1` |
| CM07 window 30 | Insert `source: S999` at line 26 | pristine `dangling=0`; mutant `dangling=1` |
| CM08 token width | Insert `source: S38` | pristine `dangling=0`; mutant `dangling=1` |
| CM11 entries +1 | Add one entry | pristine `entries=72`; mutant `entries=73` |
| CM12 rows +1 | Add one registry row | pristine `rows=333`; mutant `rows=334` |
| CM19 base hash guard removed | Change tables COPY's base_rev to scratch tip commit | pristine exit 2/no stdout; mutant exit 1/verdict line |
| CM25 missing truncated | Remove two distinct back-reference pairs | pristine `missing=2`; mutant `missing=1` |
| CM28 allowlist filtered by ids | Delete registry row S005 | pristine `exempt=24` and `missed=dangling,stale,lost`; mutant `exempt=23`, lacks stale |

Only CM01/CM03/CM04/CM28 establish **missed-leg** differences. CM06/CM07/CM08 are false-positive dangling differences; CM11/CM12/CM25 are number/count differences; CM19 is fail-closed. These are not all literal missing-leg kills under the assignment's strict detector wording; they are separately labelled exploratory discrimination evidence, not widened frozen controls.

CM27 remains **SURVIVED / no reachable tree killer established**. It widens the resolved-object-name guard from 40–64 to 39–64 hex characters. Real git emits full 40- or 64-character names. Attempt: a forged-git probe with a 39-hex result made pristine reject the name and mutant fail later at ls-tree; both exited 2 with no stdout. No end-to-end kill was observed, and this is not a registry/entry/used-by input. It is not absorbed as killed.

## Defects and severity

1. **Weakens claim — harness discrimination coverage.** Fourteen non-equivalent harness mutants still pass the original A/B/C oracle. Inputs/checkers and actual counterexamples are in `suite/harness_killers.py`, its fixture inputs, and `receipts/restoration.json`. The proposed checks kill them, but were not added to the lane or frozen denominator.
2. **Weakens claim — untested counter legs.** CM01/CM03/CM04 retain `good=ok controls=9/9` after disabling conflict/exempt/tables_sha reporting. The three concrete fixture diffs produce the required pristine missed legs and show their absence from mutants. CM01 and CM04 can print TARGET_MET on their violating fixture trees.
3. **Weakens measurement, not a green-verdict bypass — population/count coverage.** CM11/CM12/CM25 survive with incorrect reported numbers. Fixture inputs and exact pristine/mutant counts are above. CM25 still reports the `missing` leg; its kill is count-only.
4. **Routed definition observation.** CM28's deletion fixture makes pristine `stale` depend on `(S,entry)` disappearing from counter pairlines when the row id is removed. The v2 prose defines stale in terms of entry existence, CITE and LINESHA; this fixture leaves the entry/citing bytes intact. Treat that as a wording/implementation question for round 57, not permission to change v2. Independently, CM28 changes the frozen allowlist population from 24 to 23, which is the final fixture's primary population discriminator.

No finding here establishes that the actual tip's frozen C3 TARGET_MET receipt is false. This is a test-power probe, not claim adjudication or non-author closure.

## Evidence, commands and restoration

Exact commands, per-phase outputs, return codes and SHA256 values: **`receipts/kill-c3.txt`**, backed by **`receipts/restoration.json`**. Commands use absolute scratch paths and `python3 -I`; all detector work used explicit scratch work directories.

Final restoration detector output:

```
TOTAL 25 KILLED 25 exact_restorations 25
```

That total is fourteen harness assertion/effectiveness/diagnostic discriminators plus eleven exploratory counter discriminators; it is **not** twenty-five strict end-to-end control/missed-leg kills. Every probe reran the same detector on pristine bytes, mutant bytes, and exact restored bytes. Original tip-source hashes and original scratch-source hashes match in `kill-c3.txt`.

The reduced scratch repo's registry, tables, allowlist and counter blobs were identical to tip; all 71 entries came from the tip export. Base revision objects were borrowed read-only via git alternates. Reference run:

```
MADO_USED_BY: ... entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK
```

Corrections disclosed: an early counter sweep reversed status labels (corrected results are supplied); CM25 initially removed no comma-suffixed path (fixed); an initial same-path restoration import reused cached bytecode for M27 (final pass deletes that cache before each import and kills M27). The forged-git attempt's optimistic printed footer was not evidence and is not delivered as a killer. Counter fixture commits and all scratch copies were removed after receipts were copied.

Process deviation: setup repeated archive extraction while diagnosing a hidden-directory listing; it was not the requested single-archive discipline. All extraction and git writes stayed in this seat's scratch; no lane/fleet git mutation occurred. A temporary forged-git executable was created under scratch for the CM27 attempt, never in a host PATH directory; that probe did not establish a claim-level kill.

## Deliverables and limits

- `survivor-to-fixture-to-kill.md` — every named harness survivor and exploratory counter survivor, with kill level.
- `suite/fixtures/harness/` — literal parser/token/synthetic-entry/no-op-control inputs.
- `suite/fixtures/counter/CM*.diff` — eleven materialized tree-mutation diffs.
- `suite/harness_killers.py`, `suite/counter_killers.py`, and runners — executable fixture recipes.
- `mutants_w2.py`, `suite/counter_mutants.py` — exact old/new fragments.
- `src/` — the three tested tip source copies (not modified lane files).
- `receipts/` — sweeps, fixture results, equivalent-output observations, restoration hashes/output.
- `reproduce.py --scratch /fast/scratch/hyaku/mado-r56/R56W3MutKillC3` — explicit scratch bootstrap/cleanup entrypoint. The bootstrap itself was not run; the component commands listed in the receipt were.

No C1/C2 tests, live compositor checks, production integration, or new frozen predicate verification was performed. No tools installed/upgraded; existing Python 3.14.8 and git 2.56.0 used. No subagent/background dispatch. The original eleven harness-equivalence survivors and CM27 remain explicitly un-killed within the tested fixture domain.
