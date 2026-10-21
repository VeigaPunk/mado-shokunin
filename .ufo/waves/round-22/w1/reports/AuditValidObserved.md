# AuditValidObserved — C2 independent fixture proposal report

Seat: MadoR22.AuditValidObserved (leaf, reviewer lane; no subagents dispatched).
Wave: round-22 attempt 1, w1 freeze phase. No production edits, no detector
measurements, no payload execution performed or attempted.

## Deliverable

- Authored: `.ufo/waves/round-22/w1/audit-proposals/AuditValidObserved.json`
  in `preimplementation_proposal_shape` per `round-22/audit-contract.json`.
- This fixture is the **valid** pole: two observed finding rows, claim
  total2/observed2/lead0/errors0/clean-false → expected code "0",
  finding_ids `["evidence_audit_clean"]`.

## Fixture semantics (independently reasoned from the contract only)

- `snapshot.findings`: two rows, each `evidence:"observed"` with nonempty
  `class` and `command` strings → actual total=2, observed=2, lead=0.
- `snapshot.files`: two members, all `eval_unparsed`/`unparsed_spawns`
  exact int 0 → actual errors=0; nonempty files list satisfies the
  at-least-one-member rule.
- `claim`: total 2, observed 2, lead 0, errors 0 → each equals its actual
  count, so no *_count_mismatch finding applies.
- `claim.clean: false` → consistent: findings are nonempty so clean:true
  would trigger `findings_claimed_clean`; claiming false with nonempty
  findings triggers no finding.
- No invalid inputs: no booleans-as-counts, negatives, nonfinite numbers,
  duplicate keys, malformed JSON; markers explicit; size far under 2MiB.
- Expected verdict: code "0" (`clean — artifact assertions consistent`)
  with sole finding_id `evidence_audit_clean`. Interpretation note: verdict
  0 means assertion consistency, not "no scanner findings" — a nonzero
  observed count with clean:false is still a consistent artifact.

## Boundary decisions

- Claim object excludes `snapshot`/`sha256`: contract proposal shape carries
  the snapshot object inline and lists claim fields exactly; digest binding
  is the harness's job at freeze time.
- File rows carry only the two contract-named integer fields; finding rows
  carry only `evidence`, `class`, `command` — no speculative extra keys.
- `expected.code` authored as string "0" matching the contract's `"0|1|2"`
  literal.
- No candidate auditor source was opened; `tools/mado-evidence-audit.py`
  was never read or run. No sibling proposals existed to copy (directory was
  created by this write); nothing was measured.

## Unknowns / residual risk

- Whether the harness expects `finding_ids` to include `evidence_audit_clean`
  on a pass or an empty list is inferred, not observed: the ID exists only
  for the clean/consistency verdict and no sibling or prior-round artifact
  was available to confirm convention. Recorded as an explicit unknown, not
  a fabricated certainty.
- Snapshot byte digest is intentionally absent from the proposal; freezing
  computes it. No verification against an implementation was possible by
  design of this phase.

## Compliance

Git read-only; no installs (none needed); no package queries, probes,
services, or network; no builds/tests/linters run (artifact-authoring wave);
no files outside the two seat-owned paths touched.
