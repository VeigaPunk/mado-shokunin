# MutC2HeldLines — C2 held-citation mutants

## Axes

- **Coverage:** evaluated held-citation coverage predicate against four concrete mutations.
- **Operability:** ran unchanged frozen counter on pristine data, mutants, and restored revision in an isolated scratch clone.

## Result

**PASS** for all requested mutations: duplicate same citation three times, absent file, out-of-range line, and one absent token each caused clause (d) to MISS while clauses a–c remained met. Repeating an identical citation does not count as distinct; accepted citations are keyed by `(file,line)` and duplicates are skipped.

The initial W1 satisfiability fixture builder failed its assertion because S364 already exists at the registered data revision; this was a setup failure, not a counter result. A pristine run on the data revision itself succeeded, providing a valid baseline.

## Deliverables

- `.ufo/waves/round-51/w2/MutC2HeldLines/held-line-mutants.md` — exact commands, per-mutant outputs, revisions, verdict, and restoration evidence.

Report: `.ufo/waves/round-51/w2/MutC2HeldLines.md`
