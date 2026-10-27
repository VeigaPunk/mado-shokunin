# Report evidence readiness — RevReportEvidence

Axes: **operability (C1)** and **coverage (C2)**. This is an evidence-pointer audit, not a new predicate verdict. Scope is the frozen claims and published measurements at the named revisions; W2 aggregate results/final receipt remain pending.

## C1 — PRED-C1-r51

- **Frozen work/definition:** `.ufo/waves/round-51/claims.md:19-37`; implementation `quality/counters/c1-r51-ledger.py` and `quality/check-tool-ledger.py` are present at the round data tip. Frozen semantics are restated in `.ufo/waves/round-51/registration.md:7-11`.
- **Measurement:** `.ufo/waves/round-51/receipts/c1-at-current.txt:1-4` records population/rows 82, zero uncovered/dangling/bad pointers/empty descriptions, selftest ok, TARGET_MET, exit 0 at rev `22ab80bc79ef99bbe3a0c37948a8dd6241075ca8`. This receipt is NOT the exact advertised freeze rev `56026fcb9800370ae04bc65952a6567181c398d0`; registration says the C1 measurement is at freeze, so the current receipt alone does not evidence that exact revision. W1 has `w1/ExecLedgerCounter/receipts/base-and-setup.txt` for base MISS; see registration line 11.
- **Gate/control support:** registration line 11 points to `w1/ExecLedgerGate/selftest.txt` and `w1/RevLedgerPred/attacks.md`, plus named mutation seats. Pre-data controls are mapped at registration lines 21-23 to `w1/ExecControlsC1/`; individual command outputs are committed there. Use these, not an invented W2 result.
- **LOG/SCORECARD:** `SCORECARD.md:2774-2781` contains the Round 51 summary, predicate commands, measurements and explicitly says final verdict awaits W2. LOG has no Round-51 matches (search for `Round 51|round-51|C1_R51|C2_R51` returned none); therefore no LOG link/entry yet.
- **Evidence status:** work and supporting W1 controls are locatable; exact-freeze measurement receipt linkage is unresolved/mismatched to current-rev receipt. W2 verdict and final integration receipt are pending.

## C2 — PRED-C2-r51

- **Frozen work/definition:** `.ufo/waves/round-51/claims.md:47-69`; entry `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`, registry/index and counter `quality/counters/c2-r51-dispatch-entry.py` exist at data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`. Predicate and implementation caveats are in `.ufo/waves/round-51/registration.md:13-19`.
- **Measurement:** `.ufo/waves/round-51/receipts/c2-at-data.txt:1-8` records rev `a0e34387...`, clauses a-d all ok, 4/4, admitted 1/1, TARGET_MET, exit 0; it includes the probe work path. This is the named C2 data revision.
- **Gate/control support:** registration lines 17 and 21-23 link the base MISS, fixture-green, six declared mutant misses, and pre-data controls at `w1/ExecCounterC2/` and `w1/ExecControlsC2/`. Residual interpretations are enumerated there and in W1 reports; frozen limits remain disclosed, not silently changed.
- **LOG/SCORECARD:** `SCORECARD.md:2774-2781` has the C2 command, data measurement and residual caveats, with final verdict pending W2. LOG has no Round-51 entry/match yet.
- **Evidence status:** data artifact and measurement receipt are linked and revision-aligned. W2 falsification results, final receipt, and LOG closure link are pending; do not treat the current scorecard's provisional claim as final integration evidence.

## Pending / unresolved pointers

1. W2 aggregate results and final receipt do not yet exist in the inspected committed evidence; label pending until produced.
2. C1 published evidence currently names measurement at freeze, but `c1-at-current.txt` reports `22ab80bc...`; obtain/publish a freeze-revision receipt or correct the link in the eventual integration record (without altering frozen predicates).
3. `SCORECARD.md` is the available round summary; `LOG.md` has no Round-51 section yet, so its final reciprocal evidence link remains outstanding.

## Deliverables

- `report-evidence.md` — this scoped evidence audit.

Report: `.ufo/waves/round-51/w2/RevReportEvidence/report-evidence.md`
