# RevC2CounterReplay — C2 counter replay

## Deliverables
- `.ufo/waves/round-51/w2/RevC2CounterReplay/c2-counter-replay.md` — replay receipts and independent checks.
- `.ufo/waves/round-51/w2/RevC2CounterReplay.md` — scoped findings.

## Findings
No actionable counter replay defect found. Under frozen PRED-C2-r51, base revision `6ca8c559a4a3d6d361101592116eea2bc7452437` PASSes its required MISS (exit 1, 0/4 clauses); data revision `a0e34387b30538372a1bb219eb3ccdc74013d458` PASSes its required MET (exit 0, 4/4).

The data replay reported index row present; 6 source rows / minimum 2 and 6 pins; 66 knowledge files plus 3 candidate files; body shingles 2900; maximum overlap 0.1% (top three pairs recorded in the receipt); held citations 7 / minimum 3, 8 lines, 1 untargeted, 14 tokens. Probe JSON preserves cited locations and top-pair hit counts. Independent `git show -s` matched exact data revision identity. Full commands, output summaries and receipt pointer are in the deliverable above.

## Residual risk and verification gaps
Replay exercises the frozen lexical predicate, not semantic coverage; this known limitation is recorded in the round registration. No additional verification beyond the two counter invocations and commit identity check is claimed.

Report: `.ufo/waves/round-51/w2/RevC2CounterReplay/c2-counter-replay.md`
