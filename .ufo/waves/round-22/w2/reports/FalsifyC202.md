# FalsifyC202 — C2 AuditErrorsOmitted

## Findings, by severity

**No actionable defect found in this fixed case.** The single authorized invocation returned exit **1**, JSON code **1**, result `failed`, and exactly `['error_count_mismatch']`. This matches both the sealed case expectation and an independent derivation from the frozen bundle/snapshot bytes and strict audit contract. It is a correct contradiction verdict, not a clean scan, semantic-precision result, or admission recommendation.

## Scope and axes

Reviewed delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, fixed C2 identity, and only `AuditErrorsOmitted`:

1. Row-grain arithmetic: finding rows and summed error counters must not be confused with file/incident/line counts.
2. Strict input and byte identity: evaluability, exact nonnegative integers, digest-before-snapshot-decode, regular bounded input paths.
3. Runtime identity and bounds: one isolated C2 CLI child, one at a time, 384 MiB address-space and 15-second wall limits.
4. Honest authority: artifact arithmetic only, with historical uncertainty and admission boundaries unchanged.

All production, fixture, expected, proposal, and source files remained read-only. Only this report and the assigned receipt were written. No delegation, installations/updates, code execution from fixture payloads, C1 run, original-old-tool rerun, selftest, measurement driver, build, lint, formatter, generic smoke, or additional probe was performed.

## Independent derivation, before the candidate invocation

The strict independent contract is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/audit-contract.json:5-8`: findings may be empty; files must be nonempty; each count is a nonnegative exact integer, not a Boolean; errors are summed from every file's `eval_unparsed` and `unparsed_spawns`; a contradictory valid claim is code 1, while invalid/unavailable input is code 2.

Raw evidence:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditErrorsOmitted/root/snapshot.json:2-9` contains **one file row**, `eval_unparsed: 0`, `unparsed_spawns: 2`, and **zero finding rows**.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditErrorsOmitted/bundle.json:2-10` declares `total=0`, `observed=0`, `lead=0`, `errors=0`, `clean=false`, and binds `snapshot.json` to its exact SHA-256.

| Quantity | Raw-byte-derived actual | Declared | Consequence |
| --- | ---: | ---: | --- |
| Finding rows | 0 | 0 | No `finding_count_mismatch` |
| Observed rows | 0 | 0 | No `observed_count_mismatch` |
| Lead rows | 0 | 0 | No `lead_count_mismatch` |
| Error counters | **0 + 2 = 2** | **0** | **`error_count_mismatch`** |

There is no finding row requiring an evidence marker, class, or command; those per-row requirements are vacuously satisfied, not silently repaired. The nonempty file population makes the empty findings list evaluable. `clean=false` does not assert that the error-bearing scan is clean, so neither `uncertain_scan_claimed_clean` nor `findings_claimed_clean` is owed. Thus the independently derived verdict is **code 1 with exactly `['error_count_mismatch']`**, not code 0 or code 2. This counts two recorded errors, not one affected file, two finding rows, or source lines. `pkg/mod.py` is an inert row label; it was not opened or executed.

The parent measurement independently rejected duplicate keys/nonfinite JSON values, checked exact integer types, hashed the raw snapshot before decoding it, and established that this snapshot digest equals the bundle digest. Bundle/snapshot sizes are **218/132 bytes**, respectively, below the 2 MiB limit. Both are regular files; the root is a directory; neither file nor any checked ancestor is a symlink. The ordinary `snapshot.json` relative name contains no escape, backslash, or separator ambiguity. These are observations about this case, not adversarial boundary-test results. No signed, Boolean, nonfinite, malformed-path, size-boundary, or symlink fixture was introduced.

## Expectation and provenance

Read only this case's expectation/provenance from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json` (case ID `AuditErrorsOmitted`) and the relevant shared contract/seal metadata. The original case proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/proposals/AuditErrorsOmitted.json:3-24` contains the same raw counter values, claim, and original expected code string `"1"`. The manifest records only `expected.code` string-to-integer normalization (`"1"` to `1`), not a semantic change. Its proposal digest and input sizes match the measured bytes. No expected value was modified or derived from candidate output.

The assignment's chronology remains intact: raw truth landed at `9185f1f9` before implementation, and normalized expected materialized later. This case measurement does not independently authenticate chronology or turn a manifest's chronology statement into external authority.

## Actual diff, canonical caller, and error-path review

LSP was unavailable: attempting the `xd://lsp` device returned **`No such tool`**. No LSP status, references, definition, or diagnostics could be obtained. Text search was used only as a literal fallback to locate local call sites; it is not semantic reference proof.

The actual delivered commit diff for `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py` changes `relative(name)` to `relative(name, allow_backslash=False)` and opts only fixture `inventory()` into `allow_backslash=True`. In the inspected source, `rooted()` still calls `relative(name)` with its default rejection (`:80-105`); fixture `inventory()` opts in at `:185-187`. This case runs `--check`, not inventory/selftest, and uses an ordinary snapshot name. The inventory-only allowance does not change this case's arithmetic or snapshot path validation.

Canonical evaluated route in that same absolute source file:

- `main()` at `:267-286` parses `--check/--root`, calls `evaluate()` at `:275`, prints the returned JSON at `:281`, and returns its exact code at `:282`; `SystemExit(main())` is at `:286`.
- `evaluate()` at `:165-169` calls `check()` and maps the enumerated invalid-input exceptions to **code 2** / `evidence_audit_input_invalid`. No invalid-input result was reclassified as failed 1 or clean 0 here.
- `check()` at `:121-131` reads bounded raw bytes, compares snapshot SHA-256 **before snapshot JSON decoding**, and reserves code 2 / `snapshot_tampered` for a mismatch. The frozen digest matches.
- `require()`/`count()` at `:67-77` require exact integer types and reject negative counters. `check()` at `:132-146` permits the empty findings list, requires a nonempty files list, and sums both error counters. At `:147-162`, only the declared-versus-actual error total is unequal; the clean-only branches are inactive.

No alternative audit runtime, classifier import, same-identity reroute, or resume operation was exercised. Resume preflight/`resume_continuity_v1` is not on this assigned CLI path; no continuity or zero-mutation-preflight claim is inferred from this case.

## Bounded execution and byte identities

Executed exactly once, without a shell:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditErrorsOmitted/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditErrorsOmitted/root
```

The child had `RLIMIT_AS=402653184` bytes, a 15-second wall timeout, and an additional 15-second CPU limit. It exited in approximately **0.0327 seconds**, without timeout; stderr was empty. This is not a peak-memory or saturation measurement.

| Item | SHA-256, unchanged before/after |
| --- | --- |
| C2 tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit expected manifest | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Selected bundle | `9e3625bde77478b05516ea366f665a216958165ba69f1557d5ba4b6b8e2b3a19` |
| Selected raw snapshot | `fe95f49b608f494df801cce34172abb99a8f2b49d9bf7f0a73969d56ef019e69` |
| Independent audit contract | `e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f` |
| Original selected proposal | `6eeb88473a5532ef252a69d89ecddcd54da29e31845a8521547372181fc8e09b` |

Full stdout/stderr, their digests/base64, exact argv, process exit, raw selected input text, independent arithmetic, and all before/after digests are preserved in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC202/result.json`. Observed stdout SHA-256: `5c1635b7d29803a1d776ee67e2c4b920a1575a31c368668bf74d504ff4fd36f9`; empty stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. No measured input/tool drift occurred.

## Independent semantic verdict, residual risk, and verification gaps

**Observed match: yes. Independent semantic verdict: correct artifact-arithmetic failure for this case.** The receipt omits two recorded errors from its declared total, and the candidate reports exactly that contradiction. Its authority string explicitly excludes semantic correctness, authentication, admission, and promotion.

This single error-counter case does not establish general classifier precision, marker correctness for nonempty findings, line-versus-row historical projections, complete boundary rejection, resource scaling/saturation, authenticated provenance, or non-author admission. LSP diagnostics and semantic caller enumeration were unavailable. No full 46-case replay or any other candidate case was run.

The historical boundary in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:5-9` is unchanged: prior r19/r20/r21 rejected-harmed receipts and the streak remain. Actual markerless r19 is **code 2, could-not-evaluate**, not failed 1 or clean 0. Derived 5/1-line or 10/1-row populations require explicit derivation and are not substituted for actual r19. No all-observed inflation counterfactual was measured or represented as an actual-r19 claim. This report supplies bounded author-lane advisory evidence only; it grants no semantic-precision, clearance, admission, or streak-reset credit.
