# RevC1C2Controls — scoped findings

## Deliverables
- `w2/RevC1C2Controls/control-audit.md` — control/spec comparison and base-receipt audit.
- `w2/RevC1C2Controls.md` — this scoped review report.

## Findings

### Low — C2 overlap evidence disagrees for the isolated copy controls
The frozen predicate's clause (c) threshold is 30%. `w1/ExecControlsC2/controls-c2/expected.json` reports ctl-a2 and ctl-b2 `max_overlap` 0.993 and 0.992 (lines 19–48), echoed by the spec table (spec.md lines 76–84); the recorded summary instead reports 0.9747 and 0.9719 (receipts/summary.txt lines 7, 9). Both readings remain well above 30%, so the MISS verdict is robust, but the exact measurements in the control documentation are not consistent. Correct the evidence in a future amendment; do not alter the frozen predicate.

## Frozen-predicate verdicts
- **C1: PASS (receipt-backed).** Green plus each specified negative mutation is reported with expected output/exit; lane base receipt reports `TARGET_MISSED`, exit 1. Pointers: `w1/ExecControlsC1/controls-c1/expected.txt:34-58`, `w1/ExecControlsC1/controls-c1/spec.md:92-110`, `w1/ExecLedgerCounter/receipts/base-and-setup.txt:1-5`.
- **C2: PASS for the recorded controls and base red check.** Seven controls report MISS/exit 1; the isolating controls specifically fail (c), (d) control fails, and (b) no-pin control fails. Base is absent and MISS/exit 1. Pointers: `w1/ExecControlsC2/controls-c2/expected.json`, `w1/ExecControlsC2/controls-c2/receipts/summary.txt:6-14`, `w1/ExecCounterC2/receipt-base.txt:1-11`.

## Residual risk and verification gaps
Receipts are historical committed evidence; this reviewer did not replay runs. C1 synthetic fixture trees are documented as deleted, and C2 fixtures are scratch-only, so their old fixture revision IDs cannot be independently resolved from surviving objects here. C2 ctl-a/ctl-b are explicitly multi-clause fails rather than isolated (c) controls; ctl-a2/ctl-b2 supply the isolated variants. The audit records this distinction. No frozen predicate, lane data, or code was changed.
