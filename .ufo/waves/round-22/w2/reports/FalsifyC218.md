# FalsifyC218 — C2 AuditRawOversizedBundle

## Findings by severity

**No actionable defect found in this assigned case.** The single capped invocation exited **2**, with exactly `['evidence_audit_input_invalid']`, `result: could-not-evaluate`, `error: Invalid`, and empty stderr. This matches both the fixed sealed expectation and the independently derived input-validity verdict. It is **not** clean 0, contradicted-assertion 1, source-semantic precision, or admission.

Axes: (1) fail-closed raw-input size boundary; (2) artifact arithmetic and finding-row evidence grain; (3) truthful authority and immutable reproducibility.

## Independent derivation and affected control flow

- Independently measured raw bundle size: **2,097,153 bytes**; candidate bound: **2 × 1,024 × 1,024 = 2,097,152 bytes**. The input exceeds the bound by exactly one byte. The original fixed proposal explicitly specifies bundle-space padding to this size and code 2: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/audit-proposals/AuditRawOversizedBundle.json:4-9`. Its SHA-256 matches the case provenance; `expected` equals `original_expected`, with no normalizations. No old classifier output was used to derive the result.
- The independently read snapshot has **zero finding rows**, one file, and integer-zero `eval_unparsed` and `unparsed_spawns`: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawOversizedBundle/root/snapshot.json:1-9`. Thus derived row counts are total/observed/lead/errors = **0/0/0/0**, not incident-line counts. The bundle declares those same exact integer zeros and Boolean `clean: true`: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawOversizedBundle/bundle.json:1-11`. The declared snapshot digest matches the independently hashed 104-byte snapshot. These otherwise consistent artifact assertions cannot override an invalid raw input.
- Canonical command path: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:267-286` selects `--check`, calls `evaluate`, prints the JSON result, and exits with its code. `check` calls `parse(bounded(bundle))` first at line 122. `bounded` verifies ordinary paths, reads at most `MAX_BYTES + 1`, and raises `Invalid` on excess at lines 56-64. `Invalid` subclasses `ValueError` at lines 25-26, so `evaluate` maps this error to code 2 and the single input-invalid ID at lines 165-169. This ordering rejects the oversized bundle **before decoding it or consulting its snapshot**.
- The source's separate snapshot path hashes raw snapshot bytes and compares the declared digest before `parse(raw)` at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:123-131`. That is static evidence only here: the oversized bundle prevents reaching it. Likewise, exact-type/negative/nonfinite/duplicate-key checks are not exercised by this early rejection. The fixed counts contain none of those adversarial forms.
- Both artifact paths are regular files; the root is an ordinary directory. `namei -l` showed no symlink in either path's ancestry. The snapshot name is the literal `snapshot.json`, with no escape or separator ambiguity. No alternate path, symlink, source-shaped probe, or fixture mutation was introduced.
- Reviewed actual final-commit diff for `71228fd582d6d9338d7916cc64e69bd4c2e928b5`: the tool change adds `allow_backslash=False` to `relative` and enables it only for fixture inventory filenames. The assigned `--check` route does not invoke selftest/inventory and does not enable that exception. This case used only the canonical audit runtime, without rerouting or replacement tools.

## Observed execution and immutable identity

Exactly one scanner child was run, using:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawOversizedBundle/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawOversizedBundle/root
```

Both soft and hard `RLIMIT_AS` were set in the child to **402,653,184 bytes (384 MiB)**; `subprocess.run(timeout=15)` enforced the 15-second wall cap. Elapsed time was **0.03295004100073129 s**, with no timeout. Full stdout was 240 bytes, including its final newline; stderr was zero bytes:

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

| Artifact | Independently measured SHA-256, unchanged before/after |
| --- | --- |
| Audit tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Sealed audit expectations | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Assigned bundle | `1ce89ad26a0ee50883c0c022ce6c3c11363698fec5460b726a3109cbd391f2d5` |
| Assigned snapshot | `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` |
| Original fixed proposal | `ede984bb738ecbb2e1131f0598d5cca5653e11f21e68e74cb24f1ab99ce70b45` |

Tool and expected hashes equal the assigned fixed identities; bundle/snapshot/proposal hashes equal the selected case's provenance. No drift was observed. Stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`; empty stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Full exact streams (UTF-8 and Base64), digests, cap configuration, command, counts, expectations, and semantic verdict are recorded in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC218/result.json`.

## Residual risk and verification gaps

- The compact sealed contract says snapshot bytes are bounded; the original fixed raw proposal explicitly requires the **bundle** bound as well. The case-specific preexisting requirement supports this rejection; the compact wording alone is not proof of the broader rule. No expectation was changed or contradiction normalized away. Proposal chronology/authorship was not authenticated by this artifact check.
- The generic `Invalid` output omits the underlying size-error message. Its size cause follows from measured raw length, ordinary paths, and the reviewed first-call control flow; no trace instrumentation was added. The reader did not fully render the oversized final padding line, so exact padding content is supported by matched fixed provenance/digest rather than a complete displayed line. The size verdict does not depend on padding content.
- This case proves rejection at **limit + 1**, not acceptance at the exact limit, arbitrary padding forms, symlink race resistance, other malformed schemas, positive/negative row mismatches, saturation, or whole-suite coverage. Snapshot digest-before-decode and counter checks are downstream and were not reached. No mutant was executed or credited as killed.
- LSP was unavailable: `read xd://lsp` returned **No such tool**. References and definitions cited above are manual/literal control-flow evidence, not semantic LSP proof; no diagnostics claim is made.
- No full selftest, measurement driver, old tool, build, lint, formatter, generic smoke, sibling fixture, or historical-r19 receipt was run. No production/fixture/expected/source file was changed. No packages were installed, updated, or queried; no delegation or background job was used.

## Authority boundary

This is **author-lane advisory, one-case input-boundary evidence**, not non-author admission or detector semantic-precision credit. The returned authority disclaimer is accurate. Actual markerless r19 remains **2/could-not-evaluate**. Five-observed/one-lead incident-line projections and ten-observed/one-lead markerful finding-row populations require explicit derivation; all-observed inflation claims are new counterfactuals, not actual r19. This case grants no historical repair, saturation, authentication, or promotion credit and changes no prior red receipt or streak.
