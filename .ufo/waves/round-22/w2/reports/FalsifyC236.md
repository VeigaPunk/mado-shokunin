# FalsifyC236: C2 HistoricalC3.D1.row-counts-claimed-clean

Seat MadoR22.FalsifyC236, critic, author-lane advisory only. This is not non-author admission. Revision 71228fd582d6d9338d7916cc64e69bd4c2e928b5.

## Verdict

The observed result matches the expectation, and it also matches an independent semantic derivation. The tool exits 1 with `findings_claimed_clean` only, and stderr is empty. No counterexample to the verdict was found. One provenance contradiction (the expected.json rationale text for this case) is retained below. It does not affect the expectation.

## Independent derivation (from raw bytes, before the run)

- Fixed identities match. The snapshot raw sha256 is `f9cf3c64…6c608` (3140 bytes, regular file, no symlinks anywhere in the root ancestry or case paths), and the bundle `sha256` field equals it. The canonical sha256 is `9507e816…fae94b`, which equals `historical-c3.json#/derived_audit_inputs/D1_row_level_with_later_markers.canonical_sha256`. The bundle sha256 `695ec010…a6601` equals the expected entry. The expected.json sha256 `b5df74b5…2fd09` equals the fixed value.
- Strict schema: no duplicate keys, and no nonfinite numbers. All 11 rows carry an explicit `evidence` marker of `observed` or `lead`, and every `class`/`command` is nonempty after strip. `files` holds 5 members whose counters are all exact int 0, so errors = 0.
- Row grain: total 11, observed 10, lead 1. The lead is r13-root.jsonl:4.
- Line grain, informational only and not a count the contract uses: 6 distinct (file, line) pairs, 5 observed lines and 1 lead line.
- Claim `{total 11, observed 10, lead 1, errors 0, clean true}`, with exact int and bool types.
  - All four count assertions equal the actual counts, so no `*_count_mismatch` applies.
  - The contract rule "clean:true only if findings empty and errors zero" is violated by the findings side only. That gives `findings_claimed_clean`. `uncertain_scan_claimed_clean` does not apply because errors = 0.
- Derived result: **code 1, `["findings_claimed_clean"]`**.

## Observed result (the single authorized run)

The run was `prlimit --as=402653184 -- timeout 15 python3 -I tools/mado-evidence-audit.py --check …/bundle.json --root …/root`.

- Exit 1. Stdout is 368 bytes, sha256 `8a548fda…a3f26`: `code 1`, `result failed`, `finding_ids ["findings_claimed_clean"]`, `actual_counts {errors 0, lead 1, observed 10, total 11}`, `actual_snapshot_sha256 f9cf3c64…`, and the authority string verbatim from the contract.
- Stderr is empty.
- The tool sha256 was `277eced2…9fca` both before and after, so there was no drift.
- The receipts are in `.ufo/waves/round-22/w2/receipts/FalsifyC236/`: `result.json`, `stdout.bin`, `stderr.bin`, `exit.txt`, and the tool hashes.

## Attacks, limited to this case

- **Row vs line grain.** The tool counts `len(findings)`, which is row grain. This claim is row-grain (11/10/1), so it is consistent. A 6/5/1 line claim on this snapshot would be a count mismatch; the sibling case covers that. Nothing here is silently projected to line grain.
- **Digest before decode.** `check()` hashes the bounded raw snapshot bytes and compares them before `parse(raw)`. The bundle must be decoded first because it carries the digest. That ordering is correct, and the digest check does not fire for this case.
- **Signed, bool and nonfinite counts.** `count()` requires `type is int` and value ≥ 0, `clean` requires an exact bool, and NaN/Infinity/overflow-to-inf are rejected. None of these triggers here; all claim types are exact.
- **Path, symlink and size boundary.** The snapshot path is the single relative component `snapshot.json`, resolved against `--root` (not the bundle parent). No symlinks exist in the ancestry, and the file is 3140 bytes, far below the 2 MiB cap. Nothing further applies to this case.
- **Truthful authority.**
  - The output authority string limits itself to artifact arithmetic.
  - The expected entry labels itself "Derived historical C3 comparison; not an r19 claim". Its provenance marks the snapshot as DERIVED: r19 rows with later r20 markers, not the original r19 output.
  - This case does **not** demonstrate the literal registered target. The actual markerless r19 receipt remains code 2 (could not evaluate), as `guard-clarifications.md` states. This case is not a "red on a faithful actual r19 receipt".

## Retained contradiction (provenance text, not the verdict)

- **Counterexample.** The expected.json `rationale` for this case says "Six rows … total 6 = 6 rows, observed 5, lead 1 … clean:false … -> code 0 evidence_audit_clean". That text is the top-level D2 six-row proposal rationale from `historical-c3.json` lines 21–23. The D1 `cases[]` entry at `historical-c3.json:193` has no rationale of its own. The inherited text contradicts this case's claim (11 rows, `clean:true`) and its expected result (code 1, `findings_claimed_clean`). The sibling entries `row-claim-matches-derived` and `line-claim-on-row-snapshot` show the same inherited text.
- **Impacted axis.** Truthful provenance and authority of the fixture record. Expectations, codes and finding IDs are correct and unaffected.
- **Smallest safe correction (for L1; not applied, because this seat is read-only).** Record per-case rationale for the D1 cases, or label the inherited rationale as belonging to the D2 parent proposal, through the materialization record. Do not change `expected`.

## Coverage limits (uncertainty, not failure)

This case's discriminating power is narrow. Because actual total = declared total = 11, observed = 10 and lead = 1, all nonzero, the following mutants of line 159 (`if clean and actual['total']`) would **survive** this case:

- replacing `actual['total']` with `declared['total']`;
- replacing it with `actual['observed']`;
- replacing it with `actual['lead']`.

Deleting or negating the `findings_claimed_clean` branch, or inverting `clean`, would be killed (they yield code 0 `evidence_audit_clean`). These are proposed fault recipes only; L1 runs actual mutants. Coverage of declared-versus-actual and lead-only clean claims must come from other fixtures. Per scope, this seat did not inspect them.

## Not credited

Semantic precision, r19 C3 admission or the streak, the literal registered r19 target, and non-author admission.

## Installs

None.
