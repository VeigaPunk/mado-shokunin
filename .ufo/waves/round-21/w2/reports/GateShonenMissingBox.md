# GateShonenMissingBox — advisory review

## Axes and verdict

Axes assessed: verdict correctness, nearby-variant robustness, C1 independence, and evidence/authority honesty.

**Advisory verdict: no actionable finding in scope.** The frozen `shonen_missing_box` case correctly returns `could-not-evaluate`: it has assessment rows for boxes 1–3 but no row for box 4, so the four-box artifact is incomplete. A count-only false-positive variant (append a duplicate box-1 row to reach four rows while box 4 remains absent) is also rejected. This is a case-level recommendation, not promotion or round admission.

## Evidence

- Observed lane `HEAD`: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`. Tested `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py` actual-byte SHA-256: `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`.
- Frozen `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/shonen_missing_box.json` actual-byte SHA-256: `c7253b2c50ac88c20918c392631c0d56e7b96baad7d1fdfcbe8921a81b54af07`, matching `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/seal.json:53-55`. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json` actual SHA-256 `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/snapshots/population-baseline.txt` actual SHA-256 `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json:104-107` expects code `2` and result `could-not-evaluate`. In a private temporary root containing only copies of the expectation artifact, baseline population snapshot, frozen case, and one altered case, I invoked `python -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py --root ROOT --check CASE` under a 384 MiB address-space cap and 15-second timeout. No C1 source or result was present in that root.
  - Frozen case: exit `2`; JSON `code: 2`, `result: "could-not-evaluate"`, `finding_ids: ["assessment_input_invalid"]`; stderr empty. Error observed: `canonical four-box assessment incomplete`.
  - Repeated the same frozen input: identical exit/code/result/finding ID (stable tuple).
  - Altered variant: appended a copy of the existing box-1 row, leaving box 4 absent. Actual variant SHA-256 `1a0800f849132fa1fa3797c603b78122ae97647f66d9da1458fc129ef79424f5`. Exit `2`; JSON `code: 2`, `result: "could-not-evaluate"`, `finding_ids: ["assessment_input_invalid"]`; stderr empty. Error observed: `duplicate or invalid assessment box`.
- The expected fixture pins code/result; the test harness maps an unmapped nonzero case to `assessment_input_invalid` and checks exit code, JSON code, result, and finding ID (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:193-197`). The observed case output agrees with that mapping. No full selftest was run.
- Mechanically, `check()` rejects a non-four-row assessment at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:128-129`, and then rejects invalid or duplicate box identities at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:130-135`. With four rows, all four distinct valid box IDs are required because the only accepted IDs are exactly 1–4 (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:20-25,130-135`). The altered duplicate-filler case exercises the latter guard.

## C1 dependency review

`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:8-15` imports only Python standard-library modules. The `--check` path in `main()` calls `evaluate()`/`check()` (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:206-221`); that path reads the supplied JSON and rooted files and computes their digests (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:41-73,91-127`). It does not call the classifier or consume classifier results. The `subprocess` use is in the separate `--selftest` path (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:166-203`), which was not invoked. The isolated `--check` run also succeeded with no C1 code/results supplied. This verifies code-path independence for this check; it does not authenticate the provenance of the artifact assertions.

## Residual risk and verification gaps

- The gate validates assertions in JSON; timestamp strings and named-verifier text are not independent proof of chronology, identity, or authorship. The tool itself limits its authority to artifact assertions (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:142-155`). No such claims are upgraded here.
- The LSP device/status route was unavailable: `read xd://lsp` returned “No such tool” and the mounted-tool inventory contained no LSP device. Therefore no LSP references/definition/diagnostics were available; literal search output was not treated as semantic proof. The review instead relies on the inspected implementation and bounded direct runs.
- No full selftest/corpus was run; no tools were installed.

Report: `.ufo/waves/round-21/w2/reports/GateShonenMissingBox.md`
