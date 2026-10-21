# AuditEmptyClean — C2 fixture proposal report

Seat: MadoR22.AuditEmptyClean (reviewer). Wave: mado-r22-w1, round-22 attempt 1 authorized recovery. Scope: author one independent C2 calibration fixture — nonempty `files` list, zero findings, zero errors, `clean:true` claim, expected verdict 0 — in `preimplementation_proposal_shape`. Artifact consistency only; not semantic truth.

## Deliverable

Written: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/audit-proposals/AuditEmptyClean.json`

Shape follows `audit-contract.json` `preimplementation_proposal_shape` exactly — keys `id`, `snapshot` (raw JSON receipt object), `claim`, `expected` (`code`, `finding_ids`), `rationale`. No additional or omitted keys.

## Fixture semantics (independent reasoning, contract-derived)

- `snapshot.files`: two objects (`pkg/alpha.py`, `pkg/sub/beta.py`), each with `eval_unparsed: 0` and `unparsed_spawns: 0` — nonnegative exact ints, no booleans-as-counts, no negatives, no nonfinite values. Nonempty population rule satisfied.
- `snapshot.findings`: `[]` — explicitly permitted to be empty by the rules.
- Error sum over all file counters: 0.
- `claim`: `total 0, observed 0, lead 0, errors 0, clean true` — every claim field equals the actual corresponding count, and the `clean:true` gate (findings empty AND errors zero) holds on both conjuncts.
- `expected`: `code "0"`, `finding_ids ["evidence_audit_clean"]` — verdict 0 "clean (artifact assertions consistent)"; the success marker is the only finding id consistent with a fully consistent artifact. No contradiction id (mismatches, `uncertain_scan_claimed_clean`, `findings_claimed_clean`, `snapshot_tampered`) may appear; no input-invalid condition exists so code 2 / `evidence_audit_input_invalid` is excluded.

## Boundary coverage rationale

This fixture anchors the permissive pole of the `clean` gate: it distinguishes a true clean verdict from `AuditUnknownClean` (errors>0 + clean:true → 1 `uncertain_scan_claimed_clean`), `AuditFindingsClean` (findings present + clean:true → 1 `findings_claimed_clean`), and `AuditNoFiles`-style invalid input (empty files → 2). If an implementation returns nonzero here, the defect is in the happy path itself.

## Compliance

- No production edits, no detector/classifier reading, no measurements, no payload execution, no fixture execution. Contract file and w1 spec read as data only.
- No package queries/transactions, no installs (none needed — authoring only), no service/compositor/host probes, no network, no background jobs.
- Git untouched (read-only not even required); only my unique proposal and report paths written.
- Digest note: proposal shape embeds the raw snapshot object rather than a path+sha256 pair; digest checking applies at harness bundle materialization. No digest value was fabricated.

## Unknowns disclosed

- Whether the eventual harness tolerates incidental members (`path` strings) inside `files` objects: contract names only the two counter fields and states other counters/types are valid unless named invalid; judged safe, flagged for the reviewer.
- Whether a code-0 verdict emits `evidence_audit_clean` as its sole finding id is inferred from the contract's finding-id inventory and verdict table (only plausible success marker); not confirmed against any implementation, per the no-measurement freeze.

## Findings

None blocking. Proposal delivered as specified; no defects found in scope. Verification of the frozen expectation belongs to the wave-2 harness attack, not this seat.
