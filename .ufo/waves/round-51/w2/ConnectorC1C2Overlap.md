# ConnectorC1C2Overlap — round 51 w2

## Axes
Coverage + operability.

## Finding
PASS under both frozen controls: C1 at freeze revision `56026fcb9800370ae04bc65952a6567181c398d0` returns TARGET_MET while the C2 entry is absent; C2 at base `6ca8c559a4a3d6d361101592116eea2bc7452437` returns TARGET_MISSED while the ledger is absent. C2 also returns TARGET_MET at data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`. No direct claim coupling or shared content failure mode observed. Important limitation: C2's base miss co-occurs with an absent ledger but is not an isolated ledger-deletion counterfactual; the C2 clauses do not require the ledger.

Commands, outputs, evidence pointers, and detailed scope assessment are in `claim-separability.md`. No lane edits or installs.

## Deliverables
- `.ufo/waves/round-51/w2/ConnectorC1C2Overlap/claim-separability.md` — exact-revision probes and cross-claim analysis.
- `.ufo/waves/round-51/w2/ConnectorC1C2Overlap.md` — this scoped summary.

Report: `.ufo/waves/round-51/w2/ConnectorC1C2Overlap.md`
