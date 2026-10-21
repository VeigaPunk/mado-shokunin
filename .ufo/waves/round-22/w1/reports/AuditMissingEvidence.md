# AuditMissingEvidence — C2 fixture proposal (seat report)

## Deliverable
- Authored: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/audit-proposals/AuditMissingEvidence.json`
- Shape: `preimplementation_proposal_shape` per `audit-contract.json` — keys `id`, `snapshot`, `claim`, `expected`, `rationale`; no extra fields.
- Independence: derived from `audit-contract.json` alone. No candidate/audit implementation code read, no classifier reading, no detector measurements, no fixture or payload execution, no production edits.

## Fixture semantics
- **Named invalidity (sole defect):** second `findings` row has nonempty `class` and `command` strings but **no `evidence` key**. Per contract schema ("each explicit evidence observed|lead") and rule ("Missing/invalid evidence markers are uncertainty, never silently observed"), a markerless row is malformed input, not a countable lead and never an observed execution.
- **Everything else valid:** `files` nonempty (1 member); `eval_unparsed`/`unparsed_spawns` are nonnegative exact ints summing to 0 errors; claim fields are nonnegative exact ints plus exact bool `clean`.
- **Claim kept arithmetically consistent** under the lenient reading: `total=2` (both rows), `observed=1` (only the row with explicit `"observed"`), `lead=0`, `errors=0`, `clean=false` (findings nonempty). This forces the audit to fail on input validity, not on any count comparison.
- **Snapshot digest:** the harness computes the real SHA-256 over the snapshot bytes; the proposal shape carries no `sha256` field, so `snapshot_tampered` cannot be implicated.

## Expected verdict
- `code`: `"2"` (string literal, matching the contract's `"0|1|2"` verdict keys and the `AuditValidObserved`/`AuditFindingsClean` convention).
- `finding_ids`: `["evidence_audit_input_invalid"]` — the only applicable stable ID; input validity is decided before verdict comparison, so no `*_count_mismatch` or clean-flag ID can attach.

## Targeted bug class
An auditor that tallies observed/lead by skipping unmarked rows but continues to verdict comparison sees every claim field agree and wrongly returns `0`/`evidence_audit_clean`. Equally, an auditor that counts the markerless row as observed (observed=2) or lead (lead=1) and stops at a mismatch would emit code 1 — also wrong, since could-not-evaluate supersedes verdict comparison.

## Residual risk / unknowns
- Sibling `AuditNoFiles`/`AuditNegative` use integer `2` for `code`; this proposal uses the contract-literal string `"2"`. If the harness normalizes both, no conflict; if it demands one form, the contract's `"0|1|2"` string listing favors this choice. Flagged for reviewer, not silently harmonized (seats own only their own proposals).
- Whether a markerless row should additionally count toward `total` is unobservable until a canonical auditor exists; the lenient reading (total counts all rows) was chosen so no counting interpretation rescues a clean/failed verdict.
- No tool installs performed; none needed. No Git mutation, no delegation (leaf seat).
