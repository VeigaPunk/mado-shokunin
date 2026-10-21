# AuditUnknownClean — C2 audit fixture proposal (zero findings, errors=1, clean:true → 1 `uncertain_scan_claimed_clean`)

Scope: independently authored pre-implementation fixture proposal for the round-22 C2 finding-evidence audit. Authority: `.ufo/waves/round-22/audit-contract.json` (normative) and `registration.md`. Artifact consistency only — no semantic truth, no candidate code read, no measurements, no fixture execution. No production edits.

## Deliverable

`.ufo/waves/round-22/w1/audit-proposals/AuditUnknownClean.json` in `preimplementation_proposal_shape`:

- `snapshot`: `findings: []`; `files` has one member `{"path": "pkg/handler.py", "eval_unparsed": 1, "unparsed_spawns": 0}` — nonempty population, both counters nonnegative exact ints.
- `claim`: `{total: 0, observed: 0, lead: 0, errors: 1, clean: true}`.
- `expected`: `{code: "1", finding_ids: ["uncertain_scan_claimed_clean"]}`.

## Reasoning (contract-only)

1. Input validity: `files` is a nonempty list (rule: at least one member required); `findings` empty is legitimate. All counters nonnegative exact ints; no duplicate keys, no booleans-as-counts, no negatives, no nonfinite numbers. → Not code 2.
2. Actual counts: total/observed/lead = 0/0/0 from empty findings; errors = 1+0 = 1 summed across `eval_unparsed` + `unparsed_spawns`.
3. Claim matches every actual count exactly → no `*_count_mismatch` IDs; `findings_claimed_clean` inapplicable (findings genuinely empty).
4. Sole contradiction: `clean: true` while errors ≠ 0 violates "clean:true only if findings empty and errors zero". The error is disclosed honestly (`errors: 1`), isolating the clean-flag rule — an auditor gating clean only on findings emptiness would wrongly return `0`/`evidence_audit_clean`.
5. Verdict `1` (assertion contradicted), single finding ID `uncertain_scan_claimed_clean`: the scan carried a residual unknown (one unparsed eval) yet claimed clean — exactly the "refuses an error-bearing scan as clean" behavior C2 requires.

## Distinction from siblings

Unlike `AuditFindingsClean` (nonempty findings + clean:true → `findings_claimed_clean`), the uncertainty here lives in the error counters, not finding rows. Unlike `AuditErrorsOmitted`-class fixtures (mismatched declared error total), `errors: 1` is honest, so `error_count_mismatch` must not fire — the fixture discriminates clean-flag evaluation from count comparison.

## Independence and limits

- Authored solely from `audit-contract.json` before any implementation; sibling proposals consulted only for JSON surface format (key order, `code` as string), not for semantics.
- Unknowns: none beyond the contract's own residual (whether the harness normalizes `code` as string vs number — contract quotes `"0|1|2"`, so string `"1"` used).
- Tools installed: none. No builds, tests, linters, or fixture runs performed.
