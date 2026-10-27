# RevReportEvidence — report evidence readiness

Axes: **operability (C1)** and **coverage (C2)**.

This is an evidence-pointer audit, not a new predicate verdict. Frozen claims are at `.ufo/waves/round-51/claims.md:12-69`; registration records the implementations, W1 controls and known residuals at `.ufo/waves/round-51/registration.md:7-25`.

## Findings

### C1 — PRED-C1-r51 (operability)

- **Work/definition:** frozen claim `.ufo/waves/round-51/claims.md:19-37`; implementation files `quality/counters/c1-r51-ledger.py`, `quality/check-tool-ledger.py`, and `quality/tool-ledger.md` are present at the round data tip. Registration `.ufo/waves/round-51/registration.md:7-11` points to the executable and caveats.
- **Measurement receipt:** `.ufo/waves/round-51/receipts/c1-at-current.txt:1-4` reports 82/82, zero listed failures, selftest ok, TARGET_MET and exit 0 at `22ab80bc79ef99bbe3a0c37948a8dd6241075ca8`. **Unresolved pointer:** SCORECARD says C1 measured at freeze revision `56026fcb9800370ae04bc65952a6567181c398d0`, while this receipt is at `22ab80bc...`; it cannot by itself prove the freeze-revision result. Registration line 11 points to W1 base receipt `w1/ExecLedgerCounter/receipts/base-and-setup.txt` and checker receipt `w1/ExecLedgerGate/selftest.txt`.
- **Controls/gate evidence:** registration lines 11 and 21-23 point to W1 residual analysis and `w1/ExecControlsC1/` control specifications/receipts. These support the frozen kill-rule decisions; no new W2 output is asserted here.
- **LOG/SCORECARD:** `SCORECARD.md:2774-2781` records command, claimed before/after and residuals, explicitly leaving final verdict pending W2. `LOG.md` has no Round-51 matches for `Round 51|round-51|C1_R51|C2_R51` in this inspection; final LOG linkage is outstanding.
- **Status:** PASS receipt exists for a nearby later revision; exact freeze measurement link unresolved. Final W2 verdict pending.

### C2 — PRED-C2-r51 (coverage)

- **Work/definition:** `.ufo/waves/round-51/claims.md:47-69`; data artifact `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`, index and `quality/counters/c2-r51-dispatch-entry.py` are included at `a0e34387b30538372a1bb219eb3ccdc74013d458`. Registration `.ufo/waves/round-51/registration.md:13-19` documents measured result and W1 residuals.
- **Measurement receipt:** `.ufo/waves/round-51/receipts/c2-at-data.txt:1-8` records clauses a-d, clauses_met=4, admitted=1/1, TARGET_MET, exit 0 at the named data revision. This receipt is revision-aligned.
- **Controls/gate evidence:** registration lines 17 and 21-23 point to `w1/ExecCounterC2/` base/fixture/mutant receipts and `w1/ExecControlsC2/` pre-data control receipts; W1 residuals remain explicitly disclosed.
- **LOG/SCORECARD:** `SCORECARD.md:2774-2781` links the command, data result and residual caveats, and says final verdict awaits W2. `LOG.md` has no Round-51 entry yet.
- **Status:** data measurement evidence PASS and well-linked; W2 falsification, final receipt and LOG closure link pending.

## Deliverable

- Detailed per-claim evidence pointers and pending gaps: `w2/RevReportEvidence/report-evidence.md`.

Report: `.ufo/waves/round-51/w2/RevReportEvidence.md`
