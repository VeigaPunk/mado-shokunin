# RevC1Population — C1 population audit

Axis: operability / coverage of the exact C1 population.

## Verdict

**PASS** for the population component of PRED-C1-r51 at freeze revision `56026fcb9800370ae04bc65952a6567181c398d0`: independent `git ls-tree -r` enumeration yields 82 files under the exact frozen path rules, agreeing with the counter's `population=82`. No set/count mismatch found. This does not independently establish the ledger-row or pointer clauses.

Evidence and full scoped set derivation: `w2/RevC1Population/population-audit.md`. Query: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r --name-only 56026fcb9800370ae04bc65952a6567181c398d0`. Selected all tools paths, direct `quality/*.py`, and direct `quality/counters/*.py`; counts 17 + 18 + 47 = 82. Nested tools and non-Python quality files were considered against the frozen words; none changes the selected set. W1's 79 count is at the distinct round base and is not contradictory.

## Deliverables

- `.ufo/waves/round-51/w2/RevC1Population/population-audit.md` — set count/diff.
- `.ufo/waves/round-51/w2/RevC1Population.md` — scoped verdict.

Report: `.ufo/waves/round-51/w2/RevC1Population.md`
