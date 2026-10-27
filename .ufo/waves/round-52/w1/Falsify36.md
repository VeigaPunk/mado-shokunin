# Falsify36 — C1 counter isolation/scratch behavior

## Deliverables

- `.ufo/waves/round-52/w1/Falsify36.md`

## Finding: no concrete scratch-isolation bypass reproduced from permitted source-only evidence

**Target/predicate attacked:** C1 operability, registration §7: new counter runs at requested pinned revision and validates the production-ledger/control behaviors; in particular its scratch isolation claim. The counter is absent at frozen base per claims-frozen §7, so there are no round-52 bytes to execute or attack as an implementation. I examined the nearest existing predecessor `quality/counters/c1-r51-ledger.py` as source evidence only; did not execute it or any producer.

**Source evidence.** `SKILL.md:39-45` marks the round source-only, disallows producer execution, and says read already available tagged source. `quality/counters/c1-r51-ledger.py:42-46` documents its clone and checker homes under `--work`; implementation at `:106-124`, `:251-275`, `:331-346`, `:356-377`, `:434-441` shows clone destination under work, sandbox `HOME`/`TMPDIR`/`XDG_*` under sandbox, caller-provided `--work` accepted if writable, and cleanup of clone/sandbox plus only a work dir created internally. The caller-supplied work dir persists by design; this is not by itself a leak. The counter strips inherited `GIT_*` from git subprocess environment (`:85-96`).

**Reproducible setup/command and result:** source-only inspection of the cited bytes using repository file reader; execution command intentionally not run because SKILL.md forbids producer execution. Result: no executable reproduction; **reproduced: no**. The predecessor's code indicates no observed scratch-root escape in the normal `--work` path. Its selftest is executed with `--work <sandbox>/selftest` (`:278-285`), and the checker receives the same sandbox environment (`:302-304`). No evidence here establishes behavior of the absent round-52 counter.

**Potential named control / unresolved boundary:** the predecessor rejects `/tmp`, `/var/tmp`, and `/dev/shm` only as a hint after selftest failure (`:68`, `:404-407`); it does not reject those paths in `resolve_work` (`:331-346`). Thus that list is not a mandatory work-root security boundary. This matters only if the round-52 counter claims to enforce the path restriction; frozen C1 instead requires requested pinned revision and scratch behavior, and its predicate does not require this particular refusal policy. Also, `--work` is caller-selected and merely checked writable; safety depends on caller honoring the round scratch root. Do not treat this observation as falsification of frozen C1 without a counter contract requiring a stricter root policy.

**Limitations:** no scratch fixture, source checkout, clone, git/jj mutation, control execution, or package/tool action was performed. No URL/source candidate applies. No changes to claims, predicates, source files, or controls. No tooling installed.

## Report

Attacked item: C1. Concrete bypass reproduced: no. Source-only assessment: predecessor makes its child process home/temp/XDG paths beneath its sandbox, but permits caller-chosen `--work` roots and its refused-root list is advisory, not enforcement. Round-52 target counter implementation remains unavailable at frozen base; no verdict on its runtime behavior.
