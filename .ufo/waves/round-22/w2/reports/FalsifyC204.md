# FalsifyC204: C2 AuditLeadInflated

Seat: MadoR22.FalsifyC204 (leaf, no subagents). Delivered revision 71228fd582d6d9338d7916cc64e69bd4c2e928b5.
Authority: artifact arithmetic and evidence labels only. Author-lane advisory attack, not non-author admission. No semantic-precision credit.

## Result

- Observed match: yes. Exit 1; stdout `code` 1, `result` "failed", `finding_ids` `[lead_count_mismatch, observed_count_mismatch]`; stderr empty.
- Independent verdict, derived from raw bytes and the check logic before the run: code 1 (failed), same two IDs. Agreement. No expectation changed.
- Nothing contradicted and nothing normalized away. The normalizations recorded in expected.json (string "1" to 1; IDs sorted) are kept as recorded.

## Scope and execution

- Read: round-22 registration.md, supported-forms.md and guard-clarifications.md (context); expected.json AuditLeadInflated entry and its provenance lines; case bundle.json and root/snapshot.json bytes; w1 proposal AuditLeadInflated.json; inputs/audit-contract.json; tools/mado-evidence-audit.py lines 1-286.
- Executed exactly one capped child, absolute paths, 384 MiB address space, 15 s wall clock:
  `timeout 15 prlimit --as=402653184 -- python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditLeadInflated/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditLeadInflated/root`
- Not run: 46-case selftest, measurement driver, C1 tool or its source, variant or mutant probes. No installs (pacman transactions paused; none needed). No production file touched.
- Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC204/result.json` (exit, full stdout and stderr, digests), with `stdout.txt` and `stderr.txt` beside it.

## Digests and tool drift

| Artifact | sha256 | Binding |
|---|---|---|
| tools/mado-evidence-audit.py, before run | 277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca | matches fixed C2 identity |
| same, after run | 277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca | no drift |
| audit expected.json | b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09 | matches fixed audit-expected identity |
| case bundle.json (218 B) | 32fabd725ba4fa42c8a5d34dc9713c82dd5e1a9753626b7519524f37948608f7 | equals expected bundle_sha256 |
| case root/snapshot.json (1112 B) | 86594a7200ba514d5f45270a04524eeade7ca50a997223f5366942ca66fa62b8 | equals bundle claim sha256 and expected snapshot_sha256 |
| inputs/audit-contract.json | e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f | equals expected contract sha256 |
| w1 proposal AuditLeadInflated.json | 3fdae2e29b3714f6a4a6ba7e6ba69d12993085ccadb143aa78173df3ec31df93 | equals expected proposal_sha256 |
| receipt stdout.txt (390 B) | aff5bc67f8eed8a1d41be46ad50216e4fabd409811f824fa79f3052958d0775b | captured run output |
| receipt stderr.txt (0 B) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | captured run output |

`namei -l` shows every ancestor of the root and bundle paths, and both leaves, as real directories or regular files. No symlink.

## Independent derivation (before the run)

Raw bytes: the claim is total 6, observed 6, lead 0, errors 0, clean false (plain JSON ints and a bool). The snapshot has six finding objects with explicit markers: rows 1-5 `observed`, row 6 `lead` (`threading.Thread(target=handler, args=(blob,))`). Two file rows, each with eval_unparsed 0 and unparsed_spawns 0.

Check logic applied by hand:
- total 6 = 6, so no finding_count_mismatch.
- observed 6 != 5, so observed_count_mismatch.
- lead 0 != 1, so lead_count_mismatch.
- errors 0 = 0, so no error_count_mismatch.
- clean false, so neither findings_claimed_clean nor uncertain_scan_claimed_clean applies.
- Inputs valid (exact non-negative ints, valid markers, nonempty files, no duplicate keys, no NaN or Infinity), so no code 2.
- Snapshot digest equals the claim, so no snapshot_tampered.

Derived: code 1, failed, IDs sorted `[lead_count_mismatch, observed_count_mismatch]`.

## Observed versus expected

| Field | Expected (normalized) | Observed | Match |
|---|---|---|---|
| exit / code | 1 | 1 / 1 | yes |
| finding_ids | lead_count_mismatch, observed_count_mismatch | same | yes |
| actual counts | total 6, observed 5, lead 1, errors 0 (per rationale) | same | yes |
| snapshot digest | 86594a72... | 86594a72... | yes |
| stderr | empty | empty | yes |

## Attack notes (only where relevant to this case)

1. Row grain, holds. Rows are JSON finding objects and the case is row-grain by construction. The explicit markers give 5 observed and 1 lead directly, so no line or row projection is derived. The r19 "5/1 lines" and "10/1 rows" projections do not apply here and were not derived. The six command strings are distinct, so deduplication cannot change the counts. The claimed observed 6 folds the lead row into observed; the tool refuses it through observed_count_mismatch together with lead_count_mismatch.
2. Digest-before-decode, holds (static read plus observed). check() reads the snapshot bytes once, hashes them, compares the digest with the claim, and only then parses the same bytes. The observed actual_snapshot_sha256 equals the independent sha256sum. The tamper path (code 2) is not exercised.
3. Signed, bool and nonfinite counts, not exercised. All counts are plain non-negative ints and clean is a bool. count() rejects bool-as-int by type identity and rejects negatives; parse_constant and finite() reject NaN and Infinity. None of these appear in these bytes.
4. Path, symlink and size, not exercised as an attack. Boundaries checked with namei and stat. Static read: rooted() refuses symlink components and resolution outside the root; bounded() refuses symlinks, non-regular files and inputs over 2 MiB. Sizes are 218 B and 1112 B.
5. Truthful authority, holds. The stdout authority text is identical to the contract authority text. "failed" means the artifact assertion is contradicted; it is not a scanner-semantic verdict. No precision credit is claimed.

## Uncertainty and contradiction retained

- U1 [INFERENCE]. The "lead folded into observed" cause in the expected rationale is plausible: 5 observed + 1 lead = 6 claimed observed. The artifacts establish only the arithmetic, not the cause.
- U2. AuditLeadInflated is a synthetic all-observed counterfactual (claim_kind null, source_pointer null). It is new, not an actual r19 claim, and must not be cited as r19 evidence. Static inference, not executed on r19 data: a markerless actual r19 row raises Invalid at require(row, 'evidence'), which evaluate() maps to code 2. That is consistent with the expected code 2 for markerless r19.
- U3, informational, static. Exit status 1 is also what an uncaught Python exception produces, for example MemoryError raised outside evaluate()'s caught tuple. That path prints a traceback and no JSON. This run printed valid JSON with code 1 and empty stderr, so the verdict is genuine here. Exit-code-only consumers could misread a crash as failed 1. The selftest guards this (parsed JSON required, stderr must be empty); the bare CLI does not.
- U4, informational, static. check() reads only known keys and ignores unknown ones. This case has no unknown keys, so there is no effect on the verdict.
- No contradiction between the normalized expected entry and the independent derivation or the observed run. The original proposal expectation (code "1", IDs in observed-then-lead order) is recorded in expected.json and is not changed here.

## Verification gaps

Tamper, symlink, size, bool/sign/nonfinite and duplicate-key variants are reasoned statically only. Exercising them would need probes that are not authorized in this lane. No checks are requested from the main agent on account of this lane; the selftest and integration checks remain with L1.
