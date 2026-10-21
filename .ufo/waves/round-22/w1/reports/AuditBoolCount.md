# AuditBoolCount — C2 audit fixture proposal (w1)

## Deliverable

Authored `.ufo/waves/round-22/w1/audit-proposals/AuditBoolCount.json` in the
contract's `preimplementation_proposal_shape`: `id`, `snapshot` (raw JSON
receipt object), `claim`, `expected`, `rationale`. No candidate code read, no
classifier read, no measurements taken; artifact authored purely from
`.ufo/waves/round-22/audit-contract.json` (normative) plus the existing
`tools/mado-tripwire.py` emit shape for receipt field-name realism (read as
data for shape only).

## Assigned scenario

"Otherwise valid claim contains total:true -> 2 evidence_audit_input_invalid."

- Snapshot: `mado-tripwire-verdict-v1`-shaped receipt; two nonempty `files`
  rows with `eval_unparsed`/`unparsed_spawns` all zero; two `findings` rows —
  one `evidence:"observed"` (`tool_install`), one `evidence:"lead"`
  (`package_query`), each with nonempty `class`/`command` strings.
- Claim: `{"total": true, "observed": 1, "lead": 1, "errors": 0, "clean": false}`.
  Every field except `total` is the correct derived value; `total` is the
  boolean literal `true` where the schema demands a nonnegative exact int and
  the rules declare booleans-as-counts invalid.
- Expected: code `"2"` (could-not-evaluate), finding_ids
  `["evidence_audit_input_invalid"]` — exactly one ID; validation precedes
  count comparison so no `*_count_mismatch` or `*_claimed_clean` IDs arise.

## Rationale (independent, contract-only)

Contract rules: "booleans-as-counts ... are invalid"; verdict 2 covers
"invalid or unavailable input". The defect is isolated to `claim.total`; all
other claim counters and `clean` are consistent with the snapshot, so the
fixture tests exactly the bool-as-count invalidation path, not an incidental
mismatch.

## Unknowns / boundaries

- `bundle.snapshot`/`sha256` digest fields are harness-provided at run time;
  proposal carries the snapshot object only, per proposal shape. Hex digests
  in `files[].sha256` are shaped (64-hex) placeholders — contract requires
  only the bundle-level digest be real.
- Verdict comparison occurs only after the digest check; expected code
  assumes harness computes the true snapshot sha256, which it will.
- No install, no execution, no network, no git writes. Skipped all builds/
  tests per wave contract.
