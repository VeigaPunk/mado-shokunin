# MutC1Whitespace — C1 whitespace/description-cell falsification

## Finding

**MISS** under the exact frozen C1 sentence: the counter reports `TARGET_MET` after every description cell is changed to whitespace-only and again when each cell contains punctuation only. The duplicate-row and removed-row mutations also report `TARGET_MET`. Thus the prescribed empty-description control does not catch these cases in the actual counter run; duplicate and missing-row attacks likewise expose a failure of “each such file appears exactly once.”

The exact sentence requires a “non-empty description”; these mutations show that the checker accepts cells with no alphanumeric content. The row mutations also show that the counter does not enforce uniqueness/completeness for repeated/missing paths despite the predicate’s exactly-once requirement. These are advisory findings against the frozen predicate, not predicate amendments.

## Controls and evidence

See `MutC1Whitespace/whitespace-mutations.md` for full commands, outputs, exit codes and hashes. All four mutants exited 0 with `verdict=TARGET_MET`, including whitespace-only and punctuation-only descriptions (both `empty_desc=0`), one duplicated row, and one removed population row. Consequently:

- prescribed control (c), “empty description” → **MISS** for whitespace-only and punctuation-only descriptions;
- prescribed control (a), “ledger omitting one population file” → **MISS** for the removed row;
- the predicate’s exact-once condition → **MISS** for duplicate row.

All actual outputs were `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET` at revision `56026fcb9800370ae04bc65952a6567181c398d0`. Each mutant's pristine ledger SHA256 was `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b`; the restored scratch-clone bytes matched exactly. Scratch clones were removed after each probe.

## Deliverables

- `.ufo/waves/round-51/w2/MutC1Whitespace/whitespace-mutations.md` — mutation-by-mutation outputs and restoration hashes.
- `.ufo/waves/round-51/w2/MutC1Whitespace.md` — this scoped finding.

Report: .ufo/waves/round-51/w2/MutC1Whitespace.md
