# AuditTotalMismatch — C2 fixture proposal report

## Assignment
Independently author a C2 audit fixture: snapshot with two finding rows, claimed
`total:1` otherwise accurate -> verdict 1 `finding_count_mismatch`. Contract
`.ufo/waves/round-22/audit-contract.json` is normative.

## Deliverable
`.ufo/waves/round-22/w1/audit-proposals/AuditTotalMismatch.json` in
`preimplementation_proposal_shape` (id / snapshot / claim / expected / rationale).

## Fixture design (independent, contract-derived — no candidate code, no classifier
reading, no measurements)

- **Snapshot**: `mado-tripwire-verdict-v1`-shaped raw receipt (same field layout as
  committed r17 tripwire receipts, used as row-shape reference only).
  - `files`: two rows, each `eval_unparsed:0`, `unparsed_spawns:0` -> actual
    errors = 0. Nonempty list satisfies "at least one files member".
  - `findings`: two rows — one `evidence:"observed"` (`package_query`,
    `pacman -Qi linux`), one `evidence:"lead"` (`live_probe`, `wayland-info`);
    each with nonempty `class`/`command`. Commands are inert data strings.
- **Claim**: `{total:1, observed:1, lead:1, errors:0, clean:false}` — every field
  accurate **except** `total` (claimed 1 vs actual 2 rows).
- **Expected**: `code:"1"`, `finding_ids:["finding_count_mismatch"]`.

## Finding-ID isolation reasoning
- `observed_count_mismatch` — NOT triggered: claim 1 = actual 1.
- `lead_count_mismatch` — NOT triggered: claim 1 = actual 1.
- `error_count_mismatch` — NOT triggered: claim 0 = actual 0.
- `uncertain_scan_claimed_clean` / `findings_claimed_clean` — NOT triggered:
  claim `clean:false` is the required value (findings nonempty).
- `snapshot_tampered` — NOT triggered: proposal ships consistent bytes; digest
  check is pre-verdict and presumed honest per fixture construction.
- `evidence_audit_input_invalid` — NOT triggered: all rows satisfy snapshot
  validity requirements (explicit evidence, nonempty class/command, nonnegative
  exact-int counters).
- `evidence_audit_clean` — NOT triggered: an assertion was contradicted.

The mixed observed+lead split is deliberate: it additionally pins that total
counts *rows* (observed 1 + lead 1 = 2), so an implementation summing only
`observed` rows would wrongly accept `total:1`.

## Exact unknowns / scope notes
- The contract does not state whether `expected.code` is string or int; the
  contract's own `"0|1|2"` shape literal suggests a string — `"1"` used. Sibling
  proposal conventions may differ; harness should accept what it specifies.
- `unpermitted`/`counts`/`permitted` snapshot fields are descriptive receipt
  fields not governed by the contract; set consistent with the two rows
  (`package_query:1`, `live_probe:1`, `unpermitted:2`). They are not inputs to
  the audited arithmetic.
- Whether `snapshot_tampered` is checked before claim comparison is stated by the
  contract ("digest checked before verdict comparison"); since this fixture's
  bytes are internally consistent the question is moot here.
- No verification run was performed — wave 1 is proposal-authoring only; no
  candidate audit tool exists to execute against, and measurements are forbidden
  pre-seal.

## Compliance
No production edits, no detector/classifier reads, no payload execution, no
installs, no delegation, no git mutation. Only my two named artifact paths were
created.
