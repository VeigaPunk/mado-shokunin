# AuditErrorsOmitted — scoped findings (round 22, w1, C2)

Seat: `MadoR22.AuditErrorsOmitted` (reviewer, leaf; no delegation).
Assigned fixture: `unparsed_spawns2 claim errors0 cleanfalse -> 1 error_count_mismatch`.

## Deliverable

Wrote `/.ufo/waves/round-22/w1/audit-proposals/AuditErrorsOmitted.json` in
`preimplementation_proposal_shape` per
`.ufo/waves/round-22/audit-contract.json`.

## Derivation (independent, artifact arithmetic only)

- Snapshot: `findings: []`; `files` has one member `eval_unparsed=0`,
  `unparsed_spawns=2`.
- Actual counts: total=0, observed=0, lead=0, errors=2 (sum of
  `eval_unparsed` + `unparsed_spawns` across all file rows).
- Claim: total=0, observed=0, lead=0 — each matches actual; errors=0 —
  contradicts actual 2; clean=false — a correct statement (errors nonzero
  means not clean, and the claim does not assert clean).
- Expected: `code: "1"` (failed — artifact assertion contradicted),
  `finding_ids: ["error_count_mismatch"]` and no others:
  - no `findings_claimed_clean` / `uncertain_scan_claimed_clean`: findings is
    empty and `clean` is not claimed true;
  - no `evidence_audit_input_invalid`: JSON well-formed, integer nonnegative
    finite counts, files member present, empty findings permitted by rule
    "findings may legitimately be empty";
  - no `snapshot_tampered` / count mismatches beyond errors.

## Scope discipline observed

- No candidate/audit-harness code read; no classifier source read; no
  measurements, fixture execution, or payload runs; no production edits.
- Authored the snapshot receipt independently from the contract grammar only;
  other counters/types treated as valid because none were named invalid.
- No tool installs performed (none needed); no package queries; all repo
  access read-only except the two owned artifact paths.

## Residual risk / unknowns

- Proposal `snapshot` shape (bare `findings`/`files` receipt) assumed; contract
  does not pin receipt-only fields beyond those two keys — reported as
  assumption, not measured.
- `files` member `path` field is illustrative; contract requires only the two
  counter fields.
