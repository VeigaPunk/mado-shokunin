# ReceiptMutation — R14-V1 red/green check design

**Axes:** coverage (preserve the measured mutation findings); evidence integrity (do not promote provisional receipts to standalone committed-full-gate evidence). **Status:** design only; no checker, mutation, gate, or test was run and no source or receipt bytes were edited.

## Evidence pinned

`corpus/lessons/round-14-verifier-spotcheck.md:169` says the three receipts retain `input_binding: provisional worktree snapshot`, old full-gate hashes and no `measured_commit`; their run/restore records bind to the derived target, and they are not standalone final-full-gate receipts. `SCORECARD.md:613-617` calls this an unscored append-only correction and explicitly disallows a wrapper or new gate behavior.

The committed binding inventory at `.ufo/waves/round-14/evidence/committed-bindings.json:2-13` pins measured commit `32118fc1014837b3a385c7a66abbdc59b1560835`, committed full-gate SHA-256 `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`, and derived-target SHA-256 `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`.

Current original-receipt byte pins (for asserting append-only preservation):

| Original receipt | Current SHA-256 | Provisional `gate_sha256` | Exact expected finding IDs |
|---|---|---|---|
| `.ufo/waves/round-14/evidence/regression-recut.txt` | `d54626345fa0a37efc4ad1f58cc51520a4e8bd5922d717128f4d5cd19199b75b` | `ef50e262f311d74e05afd558883415d2f47fa2a0247a0c834e37f49cb60c742b` | `D1`–`D9`, `R1` (10 total) |
| `.ufo/waves/round-14/evidence/regular-target-mutants.txt` | `267de2b54b41a7575716d56fcf4433f44d92b6d2f53b8c05e46d701c4762745f` | `d6d5eb27d5e6811367c9d447f224485460db13f1b832e131296036dc1fd39b36` | `RT1`–`RT4` (4 total) |
| `.ufo/waves/round-14/evidence/retained-census-mutants.txt` | `57c462c29984d0e878c4c986ca205bee73dd6e3119b802915be31e5f4b549d81` | `d6d5eb27d5e6811367c9d447f224485460db13f1b832e131296036dc1fd39b36` | `P1`–`P8` (8 total) |

Each receipt has `input_binding: provisional worktree snapshot`; all three record `MUTATE_TARGET` SHA-256 `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`. Their recorded results are GREEN controls, respectively 10/10, 4/4, and 8/8 KILLED, zero survived/inconclusive, `MUTATE_RESTORE: OK`, and exit 0 (`:10-77`, `:10-46`, `:10-61`). These are existing recorded outputs, not a run by this seat.

## Minimal red/green check (specification, not executed)

Use a static one-off assertion over the three original receipt byte files, `.ufo/waves/round-14/evidence/committed-bindings.json`, and the append-only correction record intended at `.ufo/waves/round-15/receipt-correction.json`. Do not invoke a wrapper, harness, mutation, or gate.

- **Red / standalone classification:** For each original receipt, require `REJECT` as standalone committed-full-gate evidence when `input_binding` is provisional, `measured_commit` is absent, or its header `gate_sha256` differs from the committed full-gate SHA. Expected finding: exactly the provisional binding and absence of a measured commit; do not infer a full-gate binding from `MUTATE_TARGET`, `CONTROL`, or restore lines. Pin the three original SHA-256 values above and require them unchanged.
- **Green / corrected composite classification:** With the appended mapping, require exactly one mapping row per original path. Each row must preserve that receipt’s exact provisional `input_binding` and old `gate_sha256`, identify measured commit `32118fc1014837b3a385c7a66abbdc59b1560835`, and distinguish committed full gate `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` from derived target `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`. Require the exact per-receipt finding-ID sets above, their recorded KILLED status, and an explicit scope label that the historical outcomes concern the derived target—not standalone committed-full-gate runs. Expected result: `ACCEPT` only as accurately mapped derived-target mutation evidence; the original receipts remain `REJECT` as standalone full-gate evidence. Any changed receipt hash, missing/extra ID, omitted receipt, old header presented as committed, or derived-target digest presented as full-gate digest must reject.

**Expected detector output (design):** pristine originals → three standalone `REJECT`s; originals plus accurate append-only mapping → three mapped-derived-target `ACCEPT`s and the same three standalone `REJECT`s. No output from this check was produced here. No tools installed or updated.