# Exit-code mutation probe — MutCounterExitCodes

## Axes
- Coverage: does the frozen receipt/gate bind observed exit status as well as the printed final verdict?
- Operability: can a setup failure or internal exception be misreported as an ordinary predicate MISS?

## Scope and method
Frozen predicates are verbatim in `../claims.md` (PRED-C1-r51, lines 23–32; PRED-C2-r51, lines 51–63); registration details the implemented counters at `../registration.md:7-19`. This probe inspected the real entrypoint paths only; no counter copies were mutated or detector re-run. Therefore the requested mutation matrix is **inconclusive/not executed**, not a kill or survival result. No source bytes were changed; restoration is exact by non-modification.

Commands / pointers:
- `read .../quality/counters/c1-r51-ledger.py:356-445`
- `read .../quality/counters/c2-r51-dispatch-entry.py:588-666`
- C1 returns 1 on absent ledger and on normal predicate miss (lines 382–386, 428–433); setup exceptions explicitly return 2 (431–433). An uncaught exception would have Python's nonzero traceback exit, not the expected final TARGET line.
- C2 `main` returns 2 for caught `Setup`, 1 for non-admission, and 0 for admission (659–662); exceptions outside caught `Setup` propagate as Python failure. `score` prints the final TARGET line and returns admission as integer (623–634).

## Requested cases
- Setup error: source paths explicitly distinguish setup exit 2 from predicate MISS exit 1 for both counters. No scratch execution receipt was produced.
- Predicate miss: C1 absent-ledger path returns 1; C2 non-admitted score returns 1. No execution receipt was produced.
- Clean target: source returns 0 when met/admitted. No execution receipt was produced.
- Internal exception: neither top-level main wraps arbitrary exceptions; such an exception should terminate nonzero with traceback, but the exact status/output was not exercised. For C2, clause-B `Setup` is locally converted to a failed clause while processing continues, so this specific caught setup does not become a top-level exit 2.

## Verdict
**INCONCLUSIVE — mutation assignment not completed.** Static implementation distinguishes return codes, but the assignment requires pristine/mutated/restored behavioral runs and receipts. It cannot establish whether current receipts bind exact status/exit or empirically rule out a crash masquerading as MISS. Need bounded probes in an isolated scratch copy, changing each counter's exit mapping and injecting each requested error, while preserving exact pre/post bytes and recording raw stdout, stderr, and process status.

## Deliverables
- `.ufo/waves/round-51/w2/MutCounterExitCodes/exit-code-mutants.md` — `Report: .ufo/waves/round-51/w2/MutCounterExitCodes/exit-code-mutants.md`
- `.ufo/waves/round-51/w2/MutCounterExitCodes.md` — `Report: .ufo/waves/round-51/w2/MutCounterExitCodes.md`
