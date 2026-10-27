# MutC1TreeReads — C1 revision isolation

## Findings
The worktree-only ledger/checker mutation did not influence the frozen counter at `--rev 56026fcb9800370ae04bc65952a6567181c398d0`; pristine and mutated runs both printed `TARGET_MET` with matching metrics. Code path evidence: `quality/counters/c1-r51-ledger.py` lines 106–125 clone/checkout the resolved revision; lines 128–130 list tree paths; lines 151–153 use `git show <rev>:<path>`; lines 397–402 use checker in the clone. This means the suggested worktree mutant is ineffective against the frozen revision-scoped predicate, not a counter bypass. A valid ledger/checker committed at a distinct revision also yielded `TARGET_MET` and reported that exact revision, as the predicate allows.

**Verdict: PASS / no applicable mutant killed (inconclusive kill-test).** The frozen sentence requires `<rev>`-object reads for population and ledger/pointer evidence; it does not require the selected rev to equal the freeze revision. Full commands, outputs, hash evidence, and controls are in the probe receipt.

## Deliverables
- `w2/MutC1TreeReads/revision-isolation.md` — commands, outputs, verdict, and hash/restoration evidence.

Report: `.ufo/waves/round-51/w2/MutC1TreeReads.md
