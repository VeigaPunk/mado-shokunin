# ReceiptChain — UFO-FSD Connector Synthesis: R14-V1, QUALITY 7/9/13, and Append-Only Correction Architecture

Seat: `MadoR15.ReceiptChain` (connector, leaf).  
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
Role: UFO-FSD connector (find one non-obvious move synthesizing round proposals improving declared axes without harming another; trace second-order effects across runtime, contract, substrate, and verification; stop after one bounded proposal).  
Output report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/ReceiptChain.md`.  
Constraints observed: No commits, no gates, no mutation runs, no test/lint/formatter/smoke runs, no live probes, no input event reading/injection/recording, no credential/agent.db access, no delegation. Read-only static inspection and hashing only.

---

## 1. Named Axes & Milestone Context

1. **Coverage (Round 15 Claim Axis C1):** Sourced U1–U5 (5/7) → U1–U6 (6/7) via a bounded input-debugging layer route without input event collection or kernel diagnosis.
2. **Quality / Discernment (Contract & Calibration Axis):** Unscored lesson-backed precision correction for outside request R14-V1 (`corpus/lessons/round-14-verifier-spotcheck.md:169`). Prevents Goodhart criteria inflation; keeps calibration criteria grounded in real incidents.
3. **Operability & Evidence Integrity (Harm-Watch Axis):** Gate bytes at `32118fc1` (`fba82a66…`, 177,849 B) and derived target PIN (`cd1d73d7…`, 117,602 B) must remain bit-for-bit intact; historical receipt files in `round-14/evidence/` must retain their exact byte hashes; no new generic execution wrapper or standing gate behavior introduced.

---

## 2. Grounded Evidence & Round Proposal Contradictions

### 2.1 Verified Evidence Anchor
- **The Outside Finding (R14-V1):** `corpus/lessons/round-14-verifier-spotcheck.md:169` observed that `.ufo/waves/round-14/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt:3-4` retain `input_binding: provisional worktree snapshot`, old whole-gate hashes (`ef50e262…` or `d6d5eb27…`), and no `measured_commit` header. However, their `MUTATE_TARGET`, `CONTROL: GREEN`, and `MUTATE_RESTORE` lines directly bind the exact derived target `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`.
- **Historical Bytes (Unchanged since commit `32118fc1`):**
  - `regression-recut.txt` (SHA-256 `d54626345fa0a37efc4ad1f58cc51520a4e8bd5922d717128f4d5cd19199b75b`): 10/10 KILLED (`D1`–`D9`, `R1`), provisional `gate_sha256: ef50e262…`.
  - `regular-target-mutants.txt` (SHA-256 `267de2b54b41a7575716d56fcf4433f44d92b6d2f53b8c05e46d701c4762745f`): 4/4 KILLED (`RT1`–`RT4`), provisional `gate_sha256: d6d5eb27…`.
  - `retained-census-mutants.txt` (SHA-256 `57c462c29984d0e878c4c986ca205bee73dd6e3119b802915be31e5f4b549d81`): 8/8 KILLED (`P1`–`P8`), provisional `gate_sha256: d6d5eb27…`.
- **The Full Gate vs. Derived Target Divergence:**
  - Committed full gate at `32118fc1`: `git show 32118fc1:tools/mado-verify.sh | sha256sum` = `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` (177,849 B, 3,711 lines).
  - Derived target executable: `mado_r7_target_build` (`tools/mado-verify.sh:1723-1733`) excises four spans across three marker families (`MADO-R7-REGRESSION-BLOCK`, `MADO-R7-SELFTEST-BLOCK`, `MADO-R8-BLOCK`), stripping 60,247 B (1,308 lines). The resulting target is `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96` (117,602 B).
  - Full-gate selftest is 372/372 (`gate-selftest.txt`); derived-target selftest is 267/267 (`regression-recut.txt:11`).
  - Neither provisional hash (`ef50e262…`, `d6d5eb27…`) exists in Git history; both were ephemeral worktree snapshots before commit `32118fc1` was created (runs occurred at 05:58:44Z–06:01:00Z, whereas `32118fc1` was authored at 06:03:28Z).

### 2.2 Active Contradictions Across Peer Seats
1. **Correction Location Contradiction:**
   - `ReceiptCorrection` (`spec.json:19`) is instructed to create `.ufo/waves/round-15/receipt-correction.json`.
   - `SimplifyScope.md` (F4) argues that a JSON sidecar introduces a second errata format and proposes instead appending directly to `corpus/knowledge/gate-standing-use.md:404`.
   - `ReviewRouted.md` identifies the spec path conflict between `spec.json:19` and the acceptance trailer (`reports/ReceiptCorrection.md`), while warning that `corpus/lessons`, `SCORECARD`, and `LOG` are strictly L1-owned.
2. **Tooling & Check Contradiction:**
   - `MistakeRecord.md` (§3) and `ReceiptMutation.md` draft static checks and in-memory fixtures.
   - `AttackMistake.md` (C1, C3) proves that a format-only check or a check equating `gate_sha256 == fba82a66…` would **launder false provenance** by asserting a full-gate measurement that never happened and grading 1,308 lines of excised code that the mutation suite never touched.
   - `SimplifyScope.md` (F6) and `SCORECARD.md:613-617` note that generic tooling or new gate behavior directly violates the declared contract.

---

## 3. Substantive Bridge to QUALITY Criteria 7, 9, 13

R14-V1 requires no new numbered criterion. It is fully explained by and governed under existing criteria:

| Quality Criterion | Text Requirement | Application to R14-V1 Ancillary Mutation Receipts |
|---|---|---|
| **QUALITY 7** | *"Hash committed artifacts from `git show <commit>:<path>`; label work-window hashes provisional and bind them again at the commit."* | Round 14 applied the first clause by labeling `input_binding: provisional worktree snapshot`, but omitted the second clause (re-binding at the commit). The provisional hashes `ef50e262…` and `d6d5eb27…` were never re-bound to commit `32118fc1` and the derived target `cd1d73d7…`. |
| **QUALITY 9** | *"Bind each audit verdict to a commit or frozen-copy sha; label mid-edit failures in-flight, never as settled defects."* | The three mutation runs took place mid-edit before `32118fc1` was committed, explaining the absence of `measured_commit:`. Without an explanatory mapping, uncommitted runs risk being misread as final-full-gate settled evidence. |
| **QUALITY 13** | *"Evidence meant to outlive a round is a committed path or quoted lines plus sha; `/tmp` records provenance only."* | The receipts cited `MUTATE_TARGET: /tmp/mado-r14-recut-0blumi29/target.mado-verify.sh`. The `/tmp` path is disposable execution provenance; the durable outliving evidence is the hash `cd1d73d7…` (pinned by `PIN_MADO`) and the 22 TSV mutant hashes which independently re-derive from committed specs and derived target. |

**Contract Precedent:** In round 14, outside finding R13-V2/V3 was integrated under existing criteria 7, 9, and 13 without adding duplicate criteria (`corpus/QUALITY.md:57-61`). R14-V1 follows the exact same precedent.

---

## 4. The Proposed Move: Dual-Tier Append-Only Settlement with Zero Generic Tooling

### 4.1 Bounded Synthesis
Synthesize the round's proposals into a **Dual-Tier Settlement** that reconciles wave-local verification with permanent repo storage, completely avoiding generic wrappers:

```
[Wave Tier: Machine-Readable Sidecar]
.ufo/waves/round-15/receipt-correction.json
  ├─ Subject receipt SHA-256 anchors (d5462634…, 267de2b5…, 57c462c2…)
  ├─ Explicit pre-commit run status (no measured_commit laundering)
  ├─ Literal provisional gate_sha256 mapping (ef50e262…, d6d5eb27…)
  ├─ Committed derived target binding (cd1d73d7…, 117602 B)
  ├─ Committed full gate reference (32118fc1, fba82a66…, 177849 B)
  └─ Four exact excised marker ranges & static sed re-derivation command

[Durable Corpus Tier: L1 Closure Text Locations (Zero New Criteria)]
1. corpus/lessons/round-15.md ## Mistakes
   └─ Row M1 (R14-V1): class=ancillary receipt precision; fix=sidecar mapping; no byte changes.
2. corpus/QUALITY.md (Appended after line 61)
   └─ Erratum paragraph noting R14-V1 is governed by criteria 7, 9, 13 (no Criterion 20).
3. corpus/knowledge/gate-standing-use.md ## Errata
   └─ Appended subsection recording the derived target PIN vs. whole gate distinction.
```

### 4.2 Exact Append-Only Correction Locations

1. **Wave Artifact Location (Owned by `ReceiptCorrection`):**
   - Path: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/receipt-correction.json`.
   - Content Structure: Strict JSON mapping each of the three receipts individually. It must include `subject_sha256`, `recorded_input_binding`, `recorded_gate_sha256`, `mutate_date`, `committed_derived_target_sha256` (`cd1d73d7…`), `committed_derived_target_bytes` (`117602`), `committed_full_gate_sha256` (`fba82a66…`), `committed_revision` (`32118fc1…`), and the exact `git show` derivation pipeline.
   - Accompanying Report: `reports/ReceiptCorrection.md` (resolving the spec ambiguity noted in `ReviewRouted.md:47`).

2. **Durable Corpus Locations (Owned strictly by L1 at round closure):**
   - **`corpus/lessons/round-15.md`**: Under `## Mistakes`, record mistake row `M1` (class: `ancillary receipt precision / provenance binding`; evidence: `corpus/lessons/round-14-verifier-spotcheck.md:169`; captured-by: `outside verifier spotcheck`; fix: `append-only sidecar mapping; historical receipt bytes preserved`).
   - **`corpus/QUALITY.md`**: Append an explanatory paragraph after line 61 (beneath the R13-V2/V3 note):
     > *"R14-V1 uses existing criteria 7, 9, and 13: provisional worktree whole-gate headers in historical mutation receipts reflect pre-commit execution provenance, while their recorded `MUTATE_TARGET` directly binds the committed marker-excised derived target `cd1d73d7…` independently derivable from commit `32118fc1`. No duplicate provenance criterion or generic wrapper is introduced; historical receipt bytes remain unchanged."*
   - **`corpus/knowledge/gate-standing-use.md`**: Append `## Erratum — round 15, R14-V1 ancillary mutation receipt precision` at end-of-file after line 449, documenting the exact marker-excision ranges and stating explicitly that mutation kill counts test the derived target, not the full gate.

3. **Historical Receipt Preservation:**
   - Files `.ufo/waves/round-14/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt` MUST NOT be edited, re-headered, or deleted.

### 4.3 Rejection of Generic Tooling
- **Reject `receipt.py` / Generic Wrappers:** As demonstrated in round 14 (`corpus/lessons/round-14.md:47-51`), generic receipt runners introduce unnecessary execution surfaces, maintenance overhead, and second-order failure modes.
- **Reject Gate Modifications:** Do not alter `tools/mado-verify.sh`. It must stay byte-identical to `fba82a66…`.
- **Zero-Tooling Verification:** The validation of the correction requires only standard POSIX pipes (`git show`, `sed`, `sha256sum`, and `jq`), avoiding standing tools or gate extensions.

---

## 5. Trace of Second-Order Effects Across Surfaces

1. **Runtime & Compositor Surface:**
   - Zero interaction. No Hyprland IPC, no input injection, no event listening, no hardware probes. The move is 100% static repository metadata.
2. **Contract Surface:**
   - Adheres strictly to Kaika Rule 2 / QUALITY 4 (append-only errata; rejections and historical evidence preserved).
   - Adheres to L1 sole ownership of `corpus/`, `SCORECARD.md`, and `LOG.md`.
   - Adheres to the prompt contract: leaf seat, no commits, no gates, no live probes.
3. **Substrate & Maintenance Surface:**
   - Eliminates generic tooling bloat. By rejecting a standing receipt-validation wrapper, no new scripts are added to `tools/` that would require selftests, regression pins, or future maintenance.
4. **Verification Surface:**
   - Prevents provenance laundering (`AttackMistake.md` C1): by refusing to stamp `measured_commit: 32118fc1` onto pre-commit runs, the verification record reflects truth.
   - Prevents digest confusion (`AttackMistake.md` C3): clearly isolates full-gate selftest verification (`fba82a66…`) from derived-target mutation verification (`cd1d73d7…`).

---

## 6. Verification and Acceptance/Rejection Conditions

### 6.1 Static Verification Commands (Read-Only)
```sh
# 1. Verify committed gate digest at 32118fc1
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 32118fc1014837b3a385c7a66abbdc59b1560835:tools/mado-verify.sh | sha256sum
# Expected: fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207

# 2. Verify derived target excision matches PIN_MADO (cd1d73d7…, 117602 B)
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 32118fc1014837b3a385c7a66abbdc59b1560835:tools/mado-verify.sh \
  | sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
        -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
        -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' \
  | sha256sum
# Expected: cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96

# 3. Verify original receipt bytes are intact
sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt
# Expected:
# d54626345fa0a37efc4ad1f58cc51520a4e8bd5922d717128f4d5cd19199b75b  .../regression-recut.txt
# 267de2b54b41a7575716d56fcf4433f44d92b6d2f53b8c05e46d701c4762745f  .../regular-target-mutants.txt
# 57c462c29984d0e878c4c986ca205bee73dd6e3119b802915be31e5f4b549d81  .../retained-census-mutants.txt
```

### 6.2 Acceptance Conditions
1. Historical receipt files remain bit-identical.
2. Wave sidecar `.ufo/waves/round-15/receipt-correction.json` maps each provisional header to `cd1d73d7…` using full 64-hex strings.
3. No new numbered criterion is added to `corpus/QUALITY.md`.
4. R14-V1 remains unscored (zero movement on C1/C2 scores).
5. No generic wrapper or standing gate check is added to `tools/`.

### 6.3 Rejection Conditions
1. Modifying or replacing any byte of the round-14 mutation receipts.
2. Stamping `measured_commit: 32118fc1` or `gate_sha256: fba82a66…` directly into the mutation receipts (laundered provenance).
3. Adding a new `QUALITY` criterion 20.
4. Introducing any new script or wrapper in `tools/`.

---

## 7. Tooling Record

- **Installs / Upgrades:** None. Standard system utilities (`git`, `sed`, `sha256sum`, `python3`) inspected read-only.
- **Files Written:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/ReceiptChain.md` only.
