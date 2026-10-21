# AuditHarness — round 22 C2 implementation handoff

**Lane:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/worktrees/r22-audit` (`r22-audit`, recorded observed base `a963ce67e303db94201507a93018416e4e44fd23`). This report and the implementation files are in the isolated clone; no report or implementation file was written to the shared lane checkout.

## Files authored

- `.ufo/waves/round-22/audit/assemble.py`
- `.ufo/waves/round-22/audit/measure.py`
- `.ufo/waves/round-22/w1/reports/AuditHarness.md` (this report)

The prior incomplete shared-checkout draft was preserved by Main at `.ufo/waves/round-22/evidence/audit-assemble-shared-draft.py`; I did not edit or remove it. Its shared-checkout authorship remains conformance debt. Current work resumed in the isolated clone as directed.

## Implemented behavior (not exercised)

`assemble.py` is a static materializer; it does not invoke a detector. It refuses to overwrite an existing fixture tree, verifies the sealed raw truth file list against all 106 current source files, requires the sealed 35 audit-proposal paths to match the proposal directory, and pins the raw truth seal, audit contract, all proposal bytes, fixture bytes, and symlink targets. It emits the agreed `mado-r22-audit-fixtures-v1` manifest and `expected.sha256`. Every case carries its own `bundle` and `root`; expected codes normalize only exact integer/string `0|1|2`, finding IDs are sorted/deduplicated, and the originals and normalization records are retained. The `AuditRawSnapshotAtLimit` record keeps its original `contingent:` text and Main’s inclusive 2 MiB ruling in `eligibility_log`.

The historical C3 path is conditional on the truth-sealed artifact and source hashes. It retains the markerless r19 scan and counter receipt as unchanged copied provenance, validates the later r20 5-observed/1-lead source, and creates only explicitly derived audit cases. The six-row green case is labeled as derived; counterfactual all-observed cases remain labeled counterfactual and are not attributed as r19 claims. The original r19 claim remains the reported detected 6/6 without an evidence split.

`measure.py --tool PATH --fixtures ROOT` checks `expected.json` against its sidecar, validates the complete file/directory/symlink inventory and per-case bundle/snapshot digests, then invokes each `--check BUNDLE --root ROOT` serially and invokes `--selftest FIXTURE_ROOT`. Child processes are limited to 384 MiB address space, 15 seconds, and 1 MiB per output stream; the runner captures stdout/stderr bytes, SHA-256 digests, exit status, finding IDs, and bounded text/base64. It kills the child process group on timeout and rechecks fixtures, the selected tool, and the runner for changes after each child.

## Exact retained source evidence

- Raw truth seal: `.ufo/waves/round-22/truth-seal.json`, SHA-256 `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4`; schema `mado-r22-independent-truth-seal-v1`, base `741122d177ae8ff68a73768777f20484d5bdcbe4`, 106 listed files, including 35 C2 proposals and historical C3.
- Audit contract: `.ufo/waves/round-22/audit-contract.json`, SHA-256 `e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f`.
- C2 clarifications: `.ufo/waves/round-22/audit-clarifications.md`, SHA-256 `db5e5c30b21ccacfb48930648a12893cb0b94d7fc3c76b98572076e057526176`.
- Historical translation: `.ufo/waves/round-22/w1/historical-c3.json`, SHA-256 `9ee6144d73342062fc1120afd2e4d4db4a52ec014f8a18744f116ab0dbebed7a`.
- Historical original scan receipt: `.ufo/waves/round-19/evidence/final/tripwire-frozen-scan-classes.txt`, SHA-256 `64648ccad1f2c872d62026f530ee535624b03268e454ffd1ab8437ab2d0cf857`.
- Historical original C3 counter receipt: `.ufo/waves/round-19/evidence/final/tw-recall-after.txt`, SHA-256 `8ff13d23d3ffeab946a301a3457360edc3abf52ea833611ac2a0d6bda48ec1c1`.
- Later split authority: `.ufo/waves/round-20/evidence/recall-split-final.txt`, SHA-256 `5165b72878feec8c67e20a0ab079db0aaaea358258b8a62fbb965dd91a6df0a2`.

These are retained source records; no candidate audit implementation was opened. No derived fixture tree or measurement output has been generated.

## Risks and remaining gate

- L1 reported the landed auditor’s `--check` stdout contract: one JSON object with top-level integer `code`, `result`, sorted-unique `finding_ids`, and `authority` (optional count/digest fields); process exit equals `code`. The runner requires exit/code and exact `finding_ids` to match, and the authority string to match `audit-contract.json`; it records the result label and optional fields in captured output. It captures `--selftest` output/digests and requires exit `0`; no candidate source was opened and neither mode was run by this seat.
- No assembly, `--check`, `--selftest`, detector measurement, build, test, lint, or formatter was run. Candidate source was not read; its output contract is based only on Main’s handoff and was not exercised. Main owns post-integration verification and sealing.
- LSP was not available among mounted tools; no LSP results are claimed.
- No tools were installed or updated.
