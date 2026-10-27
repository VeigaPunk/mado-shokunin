# MutC1ToolRename — C1 inventory-boundary mutation

Axes attacked: **coverage** (path inclusion/exclusion) + **operability** (counter measurement/output).

## Frozen-sentence result

**PASS on the path-boundary probe; full predicate inconclusive.** Against frozen base `6ca8c559a4a3d6d361101592116eea2bc7452437`, the actual counter reported population 79 on pristine base. Adding five requested paths raised population to 82: `tools/edge.sh`, nested `tools/sub/extra.py`, and top-level `quality/edge.py` counted; nested `quality/sub/nested.py` and `quality/counters/edge.json` did not. These are the exact path boundaries in C1's frozen sentence. The checker's full TARGET_MET gate was not established in this fixture, and a baseline ledger-absent MISS is not a mutant kill.

## Commands and pointers

Executed actual counter (`python3 -I .../c1-r51-ledger.py --repo <isolated fixture> --rev HEAD --work <scratch>`). Exact actual output, candidate paths, revisions, and inconclusive ledger attempt are in `MutC1ToolRename/path-boundary-mutants.md`. Population implementation pointer: `quality/counters/c1-r51-ledger.py:133-148`; mutation used the frozen counter copy at `w1/ExecLedgerCounter/c1-r51-ledger.py`.

No lane source was changed. The isolated scratch tree was removed after the probe. No installs performed.

## Deliverables

- `.ufo/waves/round-51/w2/MutC1ToolRename/path-boundary-mutants.md`
- `.ufo/waves/round-51/w2/MutC1ToolRename.md`

Report: `.ufo/waves/round-51/w2/MutC1ToolRename.md`
