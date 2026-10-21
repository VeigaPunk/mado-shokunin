# AuditLeadInflated — C2 preimplementation proposal report

## Deliverable

Wrote `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/audit-proposals/AuditLeadInflated.json`
in `preimplementation_proposal_shape` per `audit-contract.json`.

## Fixture semantics (assignment)

- Snapshot: **six** finding rows — **five** `evidence: "observed"`, **one** `evidence: "lead"`;
  every row has nonempty `class` and `command` strings.
- Files: two members, each `eval_unparsed: 0`, `unparsed_spawns: 0` → actual errors `0`.
- Claim: `total 6, observed 6, lead 0, errors 0, clean false` — the lead row is folded
  into the observed bucket (lead-as-observed inflation).

## Expected verdict

- `code: "1"` (failed — artifact assertion contradicted).
- `finding_ids`: `["observed_count_mismatch", "lead_count_mismatch"]` (contract order).

## Per-counter arithmetic check

| Claim | Actual | Result |
|---|---|---|
| total 6 | 6 rows | match — no `finding_count_mismatch` |
| observed 6 | 5 | `observed_count_mismatch` |
| lead 0 | 1 | `lead_count_mismatch` |
| errors 0 | 0 + 0 + 0 + 0 = 0 | match — no `error_count_mismatch` |
| clean false | findings nonempty | honest — no `findings_claimed_clean`, no `uncertain_scan_claimed_clean` |

Input validity: all evidence markers explicit and in `{observed, lead}`; files list nonempty;
all counts nonnegative exact ints; no duplicate keys, booleans-as-counts, negatives, or
nonfinite numbers → valid input, so `evidence_audit_input_invalid` does not apply and the
verdict is `1`, not `2`.

## Scope honesty

- Independently authored from contract arithmetic/evidence-label rules only; **no candidate
  code read, no classifier reading, no measurements, no payload execution**.
- Artifact consistency claim only — not semantic truth, authentication, or admission.
- Unknowns: none within scope; the only unspecified detail is how the harness pins the
  snapshot digest (`bundle.sha256` is filled at assembly time by `AuditHarness`, not by
  this proposal, per the contract's shape).

## Tooling

No installs performed or needed (contract: pacman transactions paused; none required).
