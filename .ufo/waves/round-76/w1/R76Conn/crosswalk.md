# Round 76 provenance crosswalk — connector draft

Axes: **calibration** (C1: score the published outcome), **operability** (C2: classify deletion carriers without widening the population). Navigation is a supporting benefit, not an additional scored axis.

## Evidence mode

This seat **evidence-verified** existing local source and committed stdout; it did not execute either counting command. “Re-executed” below describes the originating measurement, not a new connector run. User-supplied rc 0 is not independently recorded in the initial measurement text this seat read. No new runtime, mutation, integration, admission or score is asserted.

## Generation | receipt | evidence mode | remaining limit

All paths below are relative to `mado-shokunin`; base is `c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf`.

| Claim / generation | Receipt and actual measured revision | Evidence mode | Remaining limit |
|---|---|---|---|
| C1: `c1-r76-outcome-field.py` scores both `mz=` and `verdict=` from `c1-r76-landing-controls.py`. The wrapper loads sha-pinned r72 generation `b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d`; r75 witness semantics carry forward with G1 widened grammar and G2 letter-bearing challenges. r76 C1 last-change revision: `cb713254ee9926e036e594312fdc61b57825526b`. | `.ufo/waves/round-76/measurement-c1-r76.txt`: measured `cb713254ee9926e036e594312fdc61b57825526b`, cases=16 correct=16 mutants=4 killed=4 base_killed=0. Labels v3 sha256 `320f7e6b54e71776f2d5b179b9a8b09ee9185886e2aeb045af0ecc9171cc77ea`; `receipts/label-derivation-r76.txt` contains sixteen agreeing independent-label rows. | Origin: re-executed fixture harness measurement; connector: evidence-verified stdout and label table. Label table says re-derived but does not itself retain raw SELFTEST/M-Z/M-R transcripts, command or rc. | The four mutations affect only observable outcome conjuncts. Dropping the echo term remains observationally equivalent because M-Z already demands the echo. Challenge freshness is not assertion truth. Sixteen fixture modes are separators, not general fault coverage or a production-health observation. |
| C2: `c2-r76-shapes.py` carries the r75 classifier under `BASE_COUNTER_SHA256=0544c0ef9d35e5cd76a0a8090d9f3a89fa0e3bb6acccee6da43bb9a3e864419b`, adding D3 callee deletion and D4 single-binding dynamic key. Instrument last changed at `755b339f1f6ec18f45b494d40515aecdbe9ceb73`. | Initial `.ufo/waves/round-76/measurement-c2-r76.txt` ends rev=`755b339f1f6ec18f45b494d40515aecdbe9ceb73`: population=20 readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59. C2 controls sha256 `df9e89841ed560613d7a05ad50f345b2d6bbf0d8e40a98f51e8b8134492b3948`; first 47 cases carried from r75. | Origin: re-executed classifier/population measurement; connector: evidence-verified stdout. L1 says it will additionally measure C2 at cb713254; that future rerun is not observed by this seat. | No general execution-order or value interpretation. D3 matches a simple first-positional-argument call, not function aliases, call chains or all carrier flows; its key is literal/module constant, not D4 dynamic flow composed into a callee. No new real reader changes class. |

Reproduction commands are the frozen declaration's C1/C2 commands, each with explicit `--repo`, `--rev`, `--base-rev`, frozen `--controls`, and a validated seat-owned `--scratch-root`. These were read, not run by this seat.

## Exact predecessor links and source cells

The two predecessor entries are `corpus/knowledge/harness-witness-credit-r75.md` (§4: mz-only outcome blind spot and probabilistic uppercase separator) and `corpus/knowledge/guard-carrier-copy-del-r75.md` (§3: same-scope/literal-only cancellation). Their index rows are `corpus/README.md:169-170` in the inspected snapshot. The r76 entries should cite these as predecessor/limit links, not replace or silently rewrite their historical predicates.

Source scope in the requested S450–S454 block:

| Row | New citation decision | Required used-by action, exact old → new |
|---|---|---|
| S450: `secrets.token_hex` | C1 `outcome-field-r76.md` should cite it for token shape only; not for outcome-rule correctness, letter rejection or assertion truth. r75 predecessor already cites it. | `corpus/knowledge/replay-witness-credit-r74.md` → `corpus/knowledge/replay-witness-credit-r74.md; corpus/knowledge/harness-witness-credit-r75.md; corpus/knowledge/outcome-field-r76.md`. The r75 missing back-link is inherited, separately distinguish it from r76 adoption in the lesson. |
| S451: assignment to attribute target | Neither new claim needs a direct citation unless explicitly explaining inherited attribute carriers; D3 does not cover that flow. | Unchanged: `corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md`. |
| S452: `os.environ` modification | Neither new claim needs direct reuse to claim D3/D4 support; inherited environ transport is not the new interprocedural cancellation rule. Use corrected S452, not superseded-digest S448, if mentioning that transport. | Unchanged: `corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md`. |
| S453: subscription deletion | C2 `interprocedural-del-r76.md` should cite it for deletion mutating the primary mapping; combine with argument-binding ground for crossing the call boundary. | `corpus/knowledge/guard-carrier-copy-del-r75.md` → `corpus/knowledge/guard-carrier-copy-del-r75.md; corpus/knowledge/interprocedural-del-r76.md`. |
| S454: `dict(mapping, **kwargs)` constructor | C2 should cite it for carried keyed copies and the `m = dict(m)` rebound-copy negative; not as evidence of callee dispatch or dynamic-key resolution. | `corpus/knowledge/guard-carrier-copy-del-r75.md` → `corpus/knowledge/guard-carrier-copy-del-r75.md; corpus/knowledge/interprocedural-del-r76.md`. |

These are proposed reconciliation targets from the observed cells, not edits by this seat. CORPUS rule 2 (`CORPUS.md:116-118`) requires each in-place `used-by` change be logged old → new in the round lesson. S450–S452 are round-74 registrations reused in round 75, not newly registered round-75 rows; S453/S454 are the round-75 additions.

The live snapshot also has S455 (argument placement into parameter slot) and S456 (deleting an unbound name), both mined with `used-by=corpus/knowledge/interprocedural-del-r76.md`. S455 belongs to C2/D3, not C1; L1 confirms dropping C1's accidental S455 citation. S456's quote concerns **deleting an unbound name**, whereas `del env[k]` **evaluates** `k`: do not treat the quote alone as proof of unbound-key-expression evaluation. The source scope/wording needs source-owner review; this seat makes no source admission or replacement.

## Contradictions retained explicitly

- C2's initial knowledge draft called cb713254 measured content, but the inspected measurement receipt names 755b339f. These are different revisions; unchanged instrument bytes do not establish a later population measurement. L1 confirms a later rerun will carry its own measured revision.
- “20 readers / 13 guarded / 0 unguarded” conflicts with the receipt: **20 population files / 13 readers / 13 guarded / 0 unguarded**. Seven files are nonreaders.
- Initial pre-freeze `control-baseline-r76.txt` has C1 **15** cases and different named mutations (`outcome-term-dropped`, `prefix-match`, `first-witness-wins`, `case-insensitive`). It is not a pre-freeze run of the final sixteen-case/four-outcome-mutation set. The final measurement's `base_score=16/16` and `base_killed=no` rows supply the matched final held-rule control. Preserve both provenance records; do not quote one as the other.
- The frozen declaration retains “fifteen-case expectation” / kill below fifteen while the frozen v3 target and final scores use sixteen. Record the mismatch explicitly rather than silently repairing frozen text. The named final mutant scores (15/16,15/16,15/16,14/16) demonstrate why the threshold wording matters.

## One bounded proposed move

Carry this **typed provenance crosswalk** into both successor entries and the report, with per-surface measured revision, instrument-last-change revision, source purpose and evidence mode. This implements the predecessor connector's request in `.ufo/waves/round-75/w1/R75Conn/crosslinks.md:60-74` without changing the frozen counter, harness, population, denominator or runtime.

Second-order effects: runtime/substrate remain untouched; contract interpretation becomes explicit about observable outcome versus echo authenticity; verification cannot accidentally equate a historical fixture run, unchanged instrument bytes and a fresh population measurement. Calibration benefits without weakening operability. This is a documentation proposal, not a measured axis-score gain.

Risk: copying the table without its evidence-mode sentence would launder a relayed result into a connector rerun; broadening source citations would imply unproved D3/D4 composition. L1 verification: compare the final receipt command/revision/rc with the two last-change revisions, confirm matched held-rule controls, resolve all cited paths, and reconcile the stated old → new cells with final SOURCES/lesson bytes. Run only the already-declared counters/no-harm checks under L1 ownership; none were run here.
