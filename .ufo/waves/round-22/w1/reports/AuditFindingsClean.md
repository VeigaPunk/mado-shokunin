# AuditFindingsClean — C2 fixture report

Seat: MadoR22.AuditFindingsClean (reviewer, leaf). Scope: authored one independent C2
preimplementation proposal; no production edits, no detector measurements, no payload
execution, no package/compositor/service probes. Contract consulted:
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-contract.json` (normative).

## Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/audit-proposals/AuditFindingsClean.json`
in `preimplementation_proposal_shape` (keys: `id`, `snapshot`, `claim`, `expected`,
`rationale`). JSON parses; validated with `python3 -c 'json.load(...)'`.

## Fixture semantics (artifact arithmetic only)

- Snapshot: `files` has one member with `eval_unparsed: 0`, `unparsed_spawns: 0`
  (nonempty population satisfied; zero errors). `findings` has one row with
  `evidence: "observed"` and nonempty `class`/`command` strings — all evidence markers
  explicit, so no invalid-input path.
- Claim: `total: 1`, `observed: 1`, `lead: 0`, `errors: 0` — every counter equals the
  actual count, so no `*_count_mismatch` applies. `clean: true` contradicts the rule
  "clean:true only if findings empty and errors zero" because findings is nonempty.
- Expected: `code: "1"`, `finding_ids: ["findings_claimed_clean"]`.
- Deliberately NOT expected: `uncertain_scan_claimed_clean` (errors are zero and every
  marker is explicit — that ID covers error-bearing/uncertain scans claimed clean),
  `evidence_audit_input_invalid` (input is valid), `snapshot_tampered` (digest assumed
  to match the fixture's own bytes; tampering is out of scope here), and no
  `evidence_audit_clean` (verdict is failure, not clean).

## Rationale method

Derived solely from contract rules and verdict/finding-ID tables; candidate code was
not read and no run was performed. This is artifact-consistency truth, not semantic
truth — per the contract's authority clause and the registration's freeze-before-
implementation rule.

## Unknowns / residual notes

- The proposal shape carries `snapshot` inline rather than a bundle `sha256` field;
  digest checking is the harness's concern at selftest time and is assumed consistent.
- `code` written as string `"1"` to match the contract's quoted `"0|1|2"` literal.
- Findings: none actionable in scope; fixture is valid, verdict-frozen, and isolated to
  its own file.

## Tooling

No installs or updates performed (none needed; pacman transactions paused host-wide).
