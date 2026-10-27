# C1 generic-description falsification

## Axes
- **Operability:** checker/counter accept the fabricated ledger fixture.
- **Coverage:** the acceptance does not establish that descriptions meaningfully describe tools.

## Counterexample and evidence
At data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`, I made an isolated scratch fixture containing every population path, gave every row the identical generic non-empty description `A useful instrument for the lane.`, and supplied a valid existing pointer file (`quality/notes.md`) containing every basename. Ran:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r51-ledger.py --repo /fast/scratch/hyaku/mado-r51/CritC1GenericDesc/fixture --rev 4801609fee45eb28d95844ebab36a89ea4e40317 --work /fast/scratch/hyaku/mado-r51/CritC1GenericDesc/work
```

Exact output and fixture derivation are in `.ufo/waves/round-51/w2/CritC1GenericDesc/generic-descriptions.md`. It exits 0 with `TARGET_MET`, 82/82 rows, no uncovered/dangling/bad-pointer/empty-description cases, and selftest ok.

**PRED-C1-r51: PASS** under its exact frozen sentence: every path is listed once, descriptions are non-empty, pointer exists and contains basename, and target summary is met. It does **not** promise meaningful or instrument-specific descriptions. This is consequently a limitation/tradeoff of the frozen claim, not a counterexample to its literal predicate. Registration line 11 already records repeated generic descriptions as a residual limitation.

## Smallest safe correction
For a future amendment only: specify a measurable meaningfulness condition (for example, description must distinguish tool behavior against a defined rubric or fixture set) and add generic-identical-description negative controls. Do not change the frozen predicate retroactively.

## Deliverables
- `.ufo/waves/round-51/w2/CritC1GenericDesc/generic-descriptions.md` — exact counter output and probe revision.

Report: `.ufo/waves/round-51/w2/CritC1GenericDesc.md`
