# MutC2Index — C2 README index-row mutation

## Deliverables
- `index-mutants.md` — README-index mutants and detector outputs.
- `.ufo/waves/round-51/w2/MutC2Index.md` — this scoped report.

Report: `.ufo/waves/round-51/w2/MutC2Index.md`

## Target and method
Frozen predicate: PRED-C2-r51, clause (a): entry exists and is indexed in `corpus/README.md`; counter command as frozen, against data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`. Mutants are tested only in an isolated scratch repository copy; frozen predicate and lane files remain unchanged.
## Result

The pristine counter run exited 0 with `clauses_met=4`, `TARGET_MET`. Four README-only mutants were tested. All **SURVIVED**: removing the row's entry path, changing it to a longer substring path (`...r51.md.backup`), duplicating the row, and placing the row inside an HTML comment all left the counter at `a ok=1`, clauses_met=4, TARGET_MET (exit 0). Each should have produced TARGET_MISSED/exit 1 under the ordinary reading of clause (a). Exact per-mutant output and hashes are in `MutC2Index/index-mutants.md`.

Restoration: the fixture README was restored byte-for-byte; pristine and restored SHA-256 are `e71e8f73317950f70104314a3e423896feeb149bc565df27fe58d0cef28267d2`. A post-restoration detector run again returned TARGET_MET/exit 0. No lane files or frozen claim were changed.

Report: `.ufo/waves/round-51/w2/MutC2Index.md`
