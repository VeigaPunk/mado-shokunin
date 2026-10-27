# MutC2Novelty — clause (c) mutation report

Attack of the frozen C2 clause (c) at data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`. Pristine execution passed; sentence reorder, repeated stopword insertion, em-dash substitution, fenced wrapping, and scratch-only unusual-extension candidate all retained `TARGET_MET`. Exact overlap percentages were not captured, so no threshold-distance estimate is claimed. The uncommitted candidate was invisible to the counter's `git ls-tree` lookup at `--rev HEAD`; this only establishes the pinned-revision boundary, not a committed-candidate or extension-filter defect.

Detailed variants, actual final lines/exit results, interpretation, commands and code pointers: `w2/MutC2Novelty/novelty-mutants.md`.

## Deliverables
- `w2/MutC2Novelty/novelty-mutants.md` — novelty-mutant probe record.

Report: `.ufo/waves/round-51/w2/MutC2Novelty.md`
