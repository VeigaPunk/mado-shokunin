# AuditValidMixed — C2 audit proposal report

Seat: `MadoR22.AuditValidMixed` (reviewer, leaf — no delegation).
Artifact written: `.ufo/waves/round-22/w1/audit-proposals/AuditValidMixed.json`

## Assignment

Independently author a C2 `preimplementation_proposal_shape` fixture: snapshot with
**one observed finding and one lead**, all counters correct, `clean:false` → expected
verdict code `0`. Contract
`.ufo/waves/round-22/audit-contract.json` is normative. No candidate code, no
classifier reading, no measurements; artifact-consistency reasoning only.

## What was authored

- **snapshot** (raw receipt object, per proposal shape — harness computes/binds the
  actual SHA-256 at assembly time; digest check precedes verdict comparison per
  contract rule):
  - `findings`: 2 rows — `{evidence:"observed", class:"thread", command:…}` and
    `{evidence:"lead", class:"spawn", command:…}`, all `class`/`command` nonempty
    strings. Invented content; no receipt was copied (the faithful r19 C3 receipt
    belongs to the HistoricalC3 seat; fabricating it here is forbidden).
  - `files`: 2 entries, each `eval_unparsed:0`, `unparsed_spawns:0` — nonempty list
    as required; error sum = 0.
- **claim**: `total:2, observed:1, lead:1, errors:0, clean:false`.
- **expected**: `code:"0"`, `finding_ids:["evidence_audit_clean"]`.
- **rationale**: full per-rule arithmetic in the proposal file.

## Rule-by-rule check (contract rules as written)

| Rule | Fixture state | Effect |
|---|---|---|
| ≥1 `files` member; findings may be empty | 2 files, 2 findings | satisfied |
| errors = Σ `eval_unparsed` + Σ `unparsed_spawns` | 0 | claim `errors:0` matches |
| total/observed/lead/errors equal actual counts | 2/1/1/0 | all match |
| `clean:true` iff findings empty AND errors 0 | findings nonempty | `clean:false` is the *correct* disclosure — no contradiction |
| missing/invalid evidence → uncertainty, never observed | both rows explicit `observed`/`lead` | no uncertainty path |
| counts exact nonnegative ints, no bool/negative/nonfinite | all plain ints | valid |
| malformed/duplicate-key JSON | none | valid |

Distinctness exercised vs. sibling seats: the `lead` row contributes to
`total` and `lead` only — never `observed` — and `clean:false` with present
findings yields 0, distinguishing it from `AuditFindingsClean` (same shape but
claims `clean:true` → 1 `findings_claimed_clean`) and `AuditLeadInflated`
(claims lead folded into observed → 1). `AuditValidObserved` uses 2 observed/0 lead;
this fixture is the mixed-split complement.

## Contract ambiguities flagged (not resolved, not blocking)

1. **`finding_ids` on a clean verdict.** The contract lists
   `evidence_audit_clean` among stable IDs annotated "clean (artifact assertions
   consistent)". I pinned `["evidence_audit_clean"]` reading it as the
   emitted verdict label. If the implementation treats finding_ids as
   defect-only, the equivalent expectation is `[]`. Main/AuditHarness should
   decide once, identically for `AuditValidObserved`, `AuditEmptyClean` and
   this fixture.
2. **`snapshot` in the proposal shape** is the raw receipt (no sha pinning
   possible pre-assembly); bundle `sha256` must be bound by the assembler,
   else the digest-before-verdict rule is untestable from proposals alone.
3. Extra keys (`file`, `line`, `path`) are not required by the contract text;
   I included plausible receipt fields. A strict-whitespace/strict-schema
   validator could reject unknown keys — no rule forbids them, but flagging.

## Compliance

- No production edits, no detector/harness code read, no measurements, no
  payload execution, no network, no installs (none needed).
- Only my named files were written; no shared/lane/git state touched.
- Git read-only not needed (no queries performed).

## Residual risk

Single-axis positive control: one observed + one lead at zero errors. It cannot
detect a checker that (a) accepts clean:false unconditionally, or (b) miscounts
only at larger N — both are covered by sibling invalid fixtures by design.
