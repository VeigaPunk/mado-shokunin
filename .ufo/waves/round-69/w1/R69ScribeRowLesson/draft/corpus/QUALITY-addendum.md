## Criterion from the round-69 equivalent-mutant and value-position defects (round 69)

**111. A frozen recipe must change a printed observable that a scripted case already spells, and a
guard key counts only where it is a key that reaches the read.**
(a) Before a mutation set is frozen, each recipe is shown to change the value a decision prints in
one named scripted case, and that case and its printed line are recorded in the pre-freeze receipt:
a recipe whose edit cannot change any printed line — a disjunct over a value whose type is already
fixed at that site, a clause in a branch the case never enters — is an equivalent mutant, excluded
from the frozen set and from the denominator, and never counted as a survivor, a kill or a forged
credit. (b) A guard mention is not a guard: the key counts only where it is a key of an environment
mapping that reaches a git launch (a dict-literal key, a subscript store, an `update`/`setdefault`
keyword, a `dict(KEY=…)` keyword, then one of the declared flows to the call), and the same string
in value position, in an uncalled helper, or in a branch that cannot run is not a guard. The four
cases `value-position-only`, `dead-branch-only`, `uncalled-helper` and `overwritten-env` are the
rule's red set, and the frozen control set must be complete and digest-pinned before scoring.

Shown able to fail: (a) recipe L (`mz_killed = mz_rc != 0` → `mz_killed = mz_rc != 0 or mz_rc is
None`) applied to the round-69 prototype's harness keeps its selftest green at 59/59 with
`MUTANT L rc=0 killed=no`, and the same edit kept the round-68 harness green at 52/52
(`.ufo/waves/round-69/control-baseline-r69.txt` § L probe; `.ufo/waves/round-68/w1/R68RevC1.md:54`)
— the frozen text sits inside `try:` after `mz_rc = r.returncode`
(`quality/counters/c1-r68-landing-controls.py:435,439`), so no printed line moves and the edit is a
non-mutant read as a survivor. (b) The round-68 classifier accepts all four red-set cases and reads
`MADO_R69_C2_BASE: controls=7/11` on the frozen 11-case set (same receipt § C2), while the landed
round-69 counter reads `controls=11/11 base_controls=7/11 verdict=TARGET_MET` at `5fc29ae7`
(`measurement-c2-r69.txt`). The landed C1 set shows (a)'s other half: R1/R2/R3 die at 57/59, 58/59
and 57/59 on the round-69 harness, while the round-68 harness survives all three at 52/52
(`measurement-c1-r69.txt`, `killed=3/3 applied=3/3 base=0/3`).

Recheck: `python3 quality/counters/c1-r69-paired-recipes.py --repo . --rev REV --base-rev
04093b83f73a841117d3b31dbb2a6063f4f2a454 --scratch-root DIR` must print
`selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET`; `python3
quality/counters/c2-r69-guard-dominance.py --repo . --rev REV --base-rev
04093b83f73a841117d3b31dbb2a6063f4f2a454 --controls .ufo/waves/round-69/controls/c2-controls-r69.json
--scratch-root DIR` must print `controls=11/11` beside `unguarded=0`.

Ground: `corpus/lessons/round-69.md` M69-1 and M69-2; `.ufo/waves/round-69/claims-declaration-r69.md`
§ C1 (the L exclusion) and § C2 (key position and dominance).

Limits: (a) bounds the denominator by what the scripted cases print; it does not prove those cases
cover the decision's real inputs, and a recipe killed by an unrelated printed difference still counts
as killed — criterion 108's marker-and-exit-status discipline carries that distinction, and the
scripted cases are stubs, so the rule proves the decision path is exercised, not that real children
behave as scripted. (b) is a bounded syntactic approximation of Python: one module, one hop, no
alias/attribute/container flow, no cross-module producer, no path-sensitivity beyond a literal-false
branch. Neither clause interprets the guard's value (`GIT_NO_REPLACE_OBJECTS=0` also disables), proves
a git child read unreplaced objects, protects a repository already rewritten, or establishes state
truth of any `PROVINCE.md` cell.
