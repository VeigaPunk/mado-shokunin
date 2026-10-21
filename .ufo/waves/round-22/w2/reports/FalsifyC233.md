# FalsifyC233 — C2 `HistoricalC3.D1.counterfactual-row-observed11-inflation`

Author-lane advisory attack only. This is not non-author admission. It gives no semantic-precision credit and no C3 retroactive credit.

## Verdict

- **Observed match: YES.** The tool's output equals the frozen expectation exactly: `code: 1`, `finding_ids: ["lead_count_mismatch", "observed_count_mismatch"]`, `result: failed`.
- **Independent semantic verdict: code 1 with the same two IDs.** I derived this from the raw bytes, the declared counts and the strict schema in `audit-contract.json` and `audit-clarifications.md`. I did not use any old classifier output.
- **Defects found in the C2 tool for this case: none.**
- **One population-count finding (calibration axis):** this case duplicates another case byte for byte (see below).

## Identities

| Item | sha256 |
|---|---|
| `tools/mado-evidence-audit.py` before the run | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` (matches the fixed identity) |
| `tools/mado-evidence-audit.py` after the run | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` (no drift) |
| audit `expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` (matches the fixed identity) |
| `bundle.json` (220 B) | `2aee92e7d76af77c8524653bcb0e26b1332a5c655e1bbb551f646842dc30951f` (equals `bundle_sha256` in expected) |
| `root/snapshot.json` (3140 B) | `f9cf3c643213c085a5031c15ea314458b18aca0d7312df01a86d5f87ce46c608` (equals the bundle's `sha256` and `snapshot_sha256` in expected) |
| `w1/historical-c3.json` (proposal) | `9ee6144d73342062fc1120afd2e4d4db4a52ec014f8a18744f116ab0dbebed7a` (equals the recorded `proposal_sha256`) |

## Independent derivation

- Strict decode with a duplicate-key hook and a non-finite rejector: no duplicate keys and no NaN or Infinity in either file. The snapshot has exactly the keys `findings` and `files`. The bundle has exactly `claim`, `sha256` and `snapshot`.
- `findings` contains **11 rows**. Each has an explicit string `evidence` and nonempty `class` and `command`. The split is **10 observed and 1 lead**; the lead is `inputs/r13-root.jsonl:4 pacman -Q …`, matching the later authoritative lead in `guard-clarifications.md`. The rows fall on **6 distinct (file, line)** pairs.
- `files` has 5 members. Every `eval_unparsed` and `unparsed_spawns` value is the exact int 0, so errors = 0. Every finding's file is listed in `files[]`.
- The claim is `{total: 11, observed: 11, lead: 0, errors: 0, clean: false}`, and every count is an exact int, not a bool.
- Comparing the claim with the actual row-grain counts:
  - total 11 = 11, so there is no `finding_count_mismatch`.
  - observed 11 ≠ 10, so `observed_count_mismatch`.
  - lead 0 ≠ 1, so `lead_count_mismatch`.
  - errors 0 = 0.
  - `clean: false` is a conservative non-clearance claim, so neither clean-related ID applies.
- **Derived result: code 1, `["lead_count_mismatch", "observed_count_mismatch"]`.**
- Provenance check: the snapshot equals `historical-c3.json#/derived_audit_inputs/D1_row_level_with_later_markers/snapshot` exactly (`derived: true`). Its derivation text says the markers come from a later interpretation and `files[]` comes from the original r19 receipt. The provenance labels this an all-observed claim that is a **NEW counterfactual**, not an r19 claim (r19 recorded `unpermitted=11` with no split). The actual markerless r19 receipt is still code 2 (could-not-evaluate), never failed (1) or clean (0). The 10/1 row split is an explicitly DERIVED input.

## Attacks scoped to this case

- **Row vs line grain:** the tool counts `len(findings)`, i.e. rows. The claim also counts rows (11), so the row and line grains do not mix here. Limitation, not a defect: a row-grain audit cannot see that the 11 rows cover only 6 incident lines. Line-grain claims are tested in sibling cases (`D1.line-claim-on-row-snapshot` expects `finding_count_mismatch` plus `observed_count_mismatch`).
- **Digest before decode:** the tool reads the bounded bytes, hashes them, and returns `snapshot_tampered` with code 2 before any `parse(raw)`. The bundle itself has to be decoded first to learn the digest, which is unavoidable. The SHA is checked against a regex before the comparison. This case's digest matches, so the verdict path runs on verified bytes.
- **Signed, bool and non-finite counts:** `require(..., int)` uses `type(x) is int`, which rejects bool. `count` rejects negative values. `parse_constant` plus a recursive `finite` walk rejects non-finite numbers. `clean` must be an exact bool. All claim values in this case are valid, so the verdict comes from arithmetic, not from input-invalid handling.
- **Path, symlink and size:** the snapshot name `snapshot.json` is relative and is resolved against `--root`, not the bundle's parent. `find -type l` returns no symlinks in the case tree. The tool rejects symlinks in root ancestors and in each path component, and checks `resolve().is_relative_to(root)`. Both inputs are far below the 2 MiB bound (220 B and 3140 B). None of these guards fire on this case. There is a check-then-open race (TOCTOU) between `is_symlink` and `open`, but it does not apply to a static fixture and is not attacked here.
- **Truthful authority:** the output carries the authority string "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion". A code 1 here only proves that a counterfactual claim contradicts the derived labels. It says nothing about detector precision.

## Finding: duplicate population member (calibration/count axis)

- **Counterexample:** this case and `HistoricalC3.derived-row-level-counterfactual-observed11-inflation-red` have byte-identical `bundle.json` and `root/snapshot.json` (`cmp` passes for both). They have the same claim, the same expected `{1, [lead_count_mismatch, observed_count_mismatch]}` and the same `source_pointer`.
- **Evidence:** across all 46 cases, grouping by (`bundle_sha256`, `snapshot_sha256`) gives **41 groups**. Four HistoricalC3 pairs are byte-identical duplicates:
  - D1 observed11 inflation and derived-row-level observed11 inflation red
  - D1 row-claim-matches-derived and r19-c3-derived-row-level-green
  - D2 counterfactual-line-observed6-inflation and derived-six-row-counterfactual-observed6-inflation-red
  - D2 line-claim-5-observed-1-lead and r19-c3-derived-six-row-5obs-1lead

  A fifth group, `AuditRawSymlinkEscape` and `AuditRawSymlinkFile`, shares both hashes, but its roots may differ through symlink targets. I did not check that, so it is **[INFERENCE]**, not a confirmed duplicate.
- **Impact:** a "46/46 passing" selftest overstates the independent fixture population. At most 42 inputs are distinct (41 if the symlink pair also matches). This case adds no evidence beyond its twin. Per the registration's "no criterion-count credit", the case total must not be presented as independent coverage.
- **Smallest safe correction:** do not delete or edit any expectation. In the C2 report, disclose the distinct-input count next to the case count, keyed by (bundle_sha256, snapshot_sha256, root inventory). Treat each duplicate pair as one population member that has two registered names.

## Receipts

`.ufo/waves/round-22/w2/receipts/FalsifyC233/` contains:

- `result.json`: command, caps, exit code, full stdout and stderr, their sha256 digests, tool hash before and after, and the independent derivation.
- `stdout.txt` sha256 `570504a2d36d0d6e14679ab8ce568ad56f6db66261b326b90992a6d0f80e5b9c`
- `stderr.txt`: empty, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `exit.txt`: contains `1`
- `tool-sha-before.txt` and `tool-sha-after.txt`

The single run was `prlimit --as=402653184 -- timeout 15 python3 -I tools/mado-evidence-audit.py --check <case>/bundle.json --root <case>/root`, on Python 3.14.8 with util-linux prlimit 2.42.4. I did not run the selftest, the measurement driver or any fixture code. I installed nothing.
