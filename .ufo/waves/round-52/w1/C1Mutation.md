# C1Mutation — mutation probe

## Deliverables

- `quality/counters/c1-r52-ledger.py` draft detector: unavailable in the round-52 tree at inspection; no new detector was present to exercise.
- `C1Mutation.md` (this report): frozen-predicate attack design and exact expected outcomes, not an executed mutation receipt.

## Probe status

Attacked item/predicate: frozen C1 meaningful tool-ledger accountability, specifically unique population, resolvable/non-self evidence pointer, and instrument-specific functional context; requested bypasses are repeated self-pointer/generic control and further plausible evasion.

I read the frozen claims and registration before other project content. Base checkout HEAD observed as `85d57a818c3707397e21c840b6498b105ba798aa`; source checkout is unchanged (round files are untracked). `quality/counters/c1-r51-ledger.py` exists, but is the explicitly insufficient prior counter, not the new detector. At inspection, `w1/` contained `OverlapScan.md` and `swarm-registry.json`, with no C1 r52 draft counter. Therefore no same bounded detector could be run on pristine, mutated, and restored bytes. Per mutation protocol, a baseline detector failure/absence is inconclusive, not a killed mutant; I did not invent a substitute detector or claim execution.

| Candidate mutation to production-shaped ledger | Frozen expected outcome under new detector | Status |
|---|---|---|
| Replace all evidence pointers with the ledger itself, preserving repeated generic descriptions | Fail; pointer must be resolvable and not self-referential, and context must be instrument-specific | Not run: detector unavailable |
| Keep self-pointers but add the instrument basename / generic “tool used” wording | Fail; basename/token presence is not instrument-specific functional context | Not run |
| Unique, resolvable, non-self pointer to unrelated evidence, while describing no instrument action | Fail; context check must reject unrelated/generic description | Not run |
| Repeat a population row with superficially different whitespace or field order | Fail uniqueness check if parsed row identity is equivalent; otherwise this probes parser normalization | Not run; exact normalization contract is not frozen |
| Use `./` or normalized path spelling to point to the ledger itself | Fail after path normalization / resolved identity comparison | Not run; exact pointer resolver behavior is not frozen |
| Point to an absent evidence path | Fail resolvability check | Not run |

The latter cases are adversarial expected outcomes derived from the frozen requirements, not measured outputs. The frozen predicate does not specify equivalence normalization for duplicate rows, symlink treatment, or a precise lexical/semantic rubric for instrument-specific context; detector behavior on those is consequently not established here. These are coverage findings only, not proposed claim or predicate changes.

## Evidence and limitations

- Frozen claim and registration: `.ufo/waves/round-52/claims-frozen.md`, `.ufo/waves/round-52/registration.md`.
- Prior detector inspected: `quality/counters/c1-r51-ledger.py`; it is not executed. Its existence does not satisfy the requested r52 mutation test.
- The source-only safety boundary was observed: no package query, live read, producer execution, or source write was performed. No scratch bytes were created, so no before/after hashes or restoration receipt exist.
- No tools installed.

## Report

`mado-shokunin/.ufo/waves/round-52/w1/C1Mutation.md`
