# R54Seat25 — C1 mutation probe (item 25)

## Axes
Coverage: whether the frozen C1 source-truth predicate rejects malformed proposition-table structure, in addition to the six named controls. Operability: whether its detector can be exercised reproducibly from the committed revision.

## Mutant selected: duplicate proposition ID replacing a required proposition

Distinct malformed-input probe: retain four table rows but change P22's ID to P21 (or duplicate an earlier row in its place). A count-only implementation could report four propositions while never checking that the required ID set is exactly P19–P22. Expected detector result under PRED-C1-r54: reject (`propositions<4/4` or `TARGET_MISSED`), because the frozen contract requires each of four corrected propositions P19–P22; registration also says the extracted P19–P22 rows are checked against the frozen table (registration.md:15–20, 25–34). This is independent of the specified drop-P22 control, which tests only a three-row table (registration.md:40–47).

## Run status / verdict

**Inconclusive — no detector available at the inspected lane state.** The pristine `quality/counters/c1-r54-errata-truth.py` was absent; therefore there was no bounded behavioral detector to invoke on pristine, mutant, and restored bytes. No source/input mutation or simulated detector result is claimed. The counter's absence is also the frozen base condition (`claims-frozen.md`, C1 Before; `receipts/before.txt`), not evidence that the proposed counter would kill this mutant.

Observed tool results:
- `glob` on `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters` (twice) listed existing counters and no `c1-r54-errata-truth.py`.
- `read` of `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r54-errata-truth.py` returned `Path ... not found`.
- `read` of `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/registration.md:30-58` confirms frozen controls and the exact-count/anchor requirements; `read` of the errata entry confirms the four distinct P19–P22 rows.

No baseline/mutant/restored detector output or byte hashes exist: no detector/input was mutated, so restoration was not needed. Hashes are **not applicable**, not omitted measurements. To make this a runnable test once the counter exists: use an isolated git fixture as prescribed by registration, mutate only the P22 ID to a duplicate while preserving four rows, invoke the same `python3 -I quality/counters/c1-r54-errata-truth.py --repo <fixture> --rev <rev>` detector on baseline/mutant/restored revisions, and require a nonzero `TARGET_MISSED` for the mutant. Do not count an absent-counter baseline as killed.

## Report trailer

Lane-relative report: `.ufo/waves/round-54/w1/R54Seat25.md`. Exact inspected paths are listed above. No fixture, git/jj mutation, producer execution, host/config/service/compositor mutation, package query, tool install/update, or source-repository write. Scratch directory `/fast/scratch/hyaku/mado-r54/R54Seat25` was prepared but no artifacts were written.