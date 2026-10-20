# ReviewRouted — R14-V1 correction without rewriting historical receipts

Scope: U6 integration risk only. Read-only static review. No gate, harness, mutant, selftest, build, lint or live probe was run. Scratch: one sed-excised copy of the committed gate was hashed under /tmp and deleted. Tool installs/updates: none. No credential or agent.db file was opened. No delegation.

Base: HEAD `ea0446f`; committed gate `32118fc1014837b3a385c7a66abbdc59b1560835`.

## Verdict

The route is sound. The correction can be appended as a sidecar or erratum block. The three receipts do not need rewriting. The correction must be coverage-neutral. Acceptance is conditional on A1–A8 below and on no rejection condition R1–R8 being met.

## Observed facts

Absolute paths are under `/home/vgpnk/Projects/shokunin/mado-shokunin/`.

1. **Receipt bytes are unchanged and committed once.** The three receipts were last changed in `32118fc`. Their blob ids at `32118fc` and `HEAD` are identical, and `git status` reports the evidence directory clean.
   - `.ufo/waves/round-14/evidence/regression-recut.txt` — sha256 `d54626345fa0a37efc4ad1f58cc51520a4e8bd5922d717128f4d5cd19199b75b`
   - `.ufo/waves/round-14/evidence/regular-target-mutants.txt` — sha256 `267de2b54b41a7575716d56fcf4433f44d92b6d2f53b8c05e46d701c4762745f`
   - `.ufo/waves/round-14/evidence/retained-census-mutants.txt` — sha256 `57c462c29984d0e878c4c986ca205bee73dd6e3119b802915be31e5f4b549d81`
2. **Headers.** Lines 1–4 of each receipt carry `command`, `cwd`, `input_binding: provisional worktree snapshot` and `gate_sha256`. None carries a `measured_commit` line.
3. **Whole-gate hashes in the headers do not identify any commit.**
   - `regression-recut.txt:4` — `ef50e262f311d74e05afd558883415d2f47fa2a0247a0c834e37f49cb60c742b`.
   - `regular-target-mutants.txt:4` and `retained-census-mutants.txt:4` — `d6d5eb27d5e6811367c9d447f224485460db13f1b832e131296036dc1fd39b36`.
   - `git log -- tools/mado-verify.sh` lists nine commits. Their gate blobs are `fba82a66` (`32118fc`, `HEAD`), `037b05dc` (`95cbc41`), `ea798ad0` (`6e3b75f`), `fdd3a4d8` (`5174e15`), and older ones. None equals `ef50e262` or `d6d5eb27`.
   - `d6d5eb27` appears only in the three receipts. `ef50e262` appears in `.ufo/waves/round-14/w1/reports/GateImplement.md:19` and `ReviewResolver.md:32,34` as the delivered worktree bytes at that time. Those bytes are not retained.
4. **The target identity is consistent.** All three receipts record `MUTATE_TARGET … sha256=cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96 bytes=117602`. Each has a GREEN control with pristine `cd1d73d7…`. Each has `MUTATE_RESTORE: OK` with before and after both `cd1d73d7…`.
5. **The target re-derives from committed bytes.** Command run (static, hashing only):
   ```sh
   git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 32118fc1014837b3a385c7a66abbdc59b1560835:tools/mado-verify.sh \
     | sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
            -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
            -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' \
     | sha256sum      # → cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96, 117602 bytes
   ```
   The sed expression is the one in `mado_r7_target_build()` at `tools/mado-verify.sh:1723-1733` of `32118fc`. The same pin appears in `.ufo/waves/round-14/frozen/gate.sh:1622,1639`, `LOG.md:1036`, `SCORECARD.md:542`, `corpus/knowledge/gate-standing-use.md:446` and `corpus/lessons/round-14.md:174`.
6. **The bound standalone receipt is different.** `.ufo/waves/round-14/evidence/gate-selftest.txt:2-3` carries `measured_commit: 32118fc…` and `gate_sha256: fba82a66…`, with `372/372`. Its own header is the committed-revision binding. The three mutation receipts have no such binding.
7. **Kill counts (grep over each receipt).**
   - `regression-recut.txt`: KILLED 10, survived 0, GREEN 1, restore OK at `:75`.
   - `regular-target-mutants.txt`: KILLED 4, survived 0, GREEN 1, restore OK at `:44`.
   - `retained-census-mutants.txt`: KILLED 8, survived 0, GREEN 1, restore OK at `:59`.
8. **Spec provenance differs across the three.**
   - `regression-recut.txt:MUTATE_SPEC` points to `/tmp/mado-r14-recut-0blumi29/mado-verify.defects.spec` (defects=10). No committed file matches `defects` (`git ls-files | grep defects` returns nothing). This spec is not retained in the repo.
   - `regular-target-mutants.txt` uses `.ufo/waves/round-14/w1/regular-target.spec` (committed, defects=4).
   - `retained-census-mutants.txt` uses `.ufo/waves/round-13/covering.spec` (committed, defects=8).
   - No receipt records a spec sha256.
9. **The mutation tool is a mutable sibling.** `MUTATE_TOOL … sha256=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` matches `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` as of this review (read-only hash). It is outside the mado repo, and the `LOG` F2 drift risk applies.
10. **Routing source.** `corpus/lessons/round-14-verifier-spotcheck.md:169` defines R14-V1 as "append an explanatory correction mapping each provisional header to its committed derived target; keep historical bytes … admission does not require rewriting these records." Line 169 is not reproduced in this report.
11. **Spec conflict.** `.ufo/waves/round-15/w1/spec.json` item `ReceiptCorrection` (line 19) says "Create ONLY `.ufo/waves/round-15/receipt-correction.json`". Its acceptance text says `reports/ReceiptCorrection.md`. The two outputs disagree.

## Acceptance conditions (all required)

- **A1 — Byte preservation.** The three receipt sha256 values in Observed 1 are unchanged after the correction. Lines 1–4 and all `MUTATE_*` lines are untouched. The correction is an appended block or a sidecar file. QUALITY 4 requires append-only errata.
- **A2 — Header mapping.** Each provisional header is mapped with full 64-hex values, not `…` prefixes. Its status is stated: `input_binding: provisional worktree snapshot` means no committed or retained bytes back `ef50e262…` or `d6d5eb27…`. It is not a whole-gate identity. QUALITY 6 and 7 apply.
- **A3 — Target mapping.** `cd1d73d7…` is stated with full 64-hex, the byte count 117602, and the exact committed-revision command from Observed 5. The receipt-time build source is labelled as not retained. The target identity is verified from committed bytes, not from the worktree.
- **A4 — Scope limit.** The correction states that these receipts are not standalone final full-gate receipts. The committed-revision whole-gate binding is `gate-selftest.txt` (`fba82a66…`), which runs no mutants.
- **A5 — Counts and dates.** Kill counts are written as `<n> — <command> <date>` (QUALITY 10): `10/10`, `4/4`, `8/8`. The regression-recut row is labelled "not re-runnable from committed bytes; spec is in `/tmp` only" (QUALITY 13).
- **A6 — Coverage neutrality.** No C1 or C2 value, SCORECARD row or `LOG` score changes. R14-V1 remains unscored, as the spec goal says.
- **A7 — Forward binding recommendation.** Future mutation receipts carry `measured_commit`, the committed `gate_sha256`, the derived `MUTATE_TARGET` sha, and the spec sha256. This is a recommendation for L1 only. No wrapper is added, consistent with `lessons/round-14-verifier-spotcheck.md` and QUALITY 7/9/13.
- **A8 — Ownership.** The correction is written by L1 or the ReceiptCorrection seat into its disjoint output. `corpus/lessons`, `SCORECARD`, and `LOG` are L1-owned. The spec conflict in Observed 11 is resolved by L1 before writing.

## Rejection conditions (any one rejects)

- **R1.** Any byte change to the three receipts, including removing the `provisional` label, re-hashing, or replacing the file with a "corrected" copy.
- **R2.** Any text that maps `ef50e262…` or `d6d5eb27…` to a commit, to `fba82a66`, or to a final whole-gate receipt.
- **R3.** Use of `cd1d73d7…` as a prefix only, without full 64-hex values.
- **R4.** A derivation that reads the worktree `tools/mado-verify.sh` instead of `git show 32118fc:`. The worktree equals `fba82a66` today, but the claim must name the committed revision.
- **R5.** Any claim that the regression-recut 10/10 table is reproducible from committed repo bytes, or that `MUTATE_TOOL` is a committed mado artifact.
- **R6.** Any claim that the gate or mutants were re-run by this correction, or that a "fresh" sweep occurred.
- **R7.** Any in-place edit of `corpus/lessons/round-14-verifier-spotcheck.md:169` rather than an appended erratum.
- **R8.** Any change to a coverage or operability score, to SCORECARD, or to PROVINCE/SHONEN.

## Verification gaps and residual risk

- The worktree bytes behind `ef50e262…` are not retained. Equality of their excision with `cd1d73d7…` rests on the receipt's recorded `MUTATE_TARGET` and on the committed-revision derivation above. It is not independently re-derived from the `ef50e262` bytes.
- The regression-recut defect spec (`/tmp/mado-r14-recut-0blumi29/mado-verify.defects.spec`) is not retained. Its 10/10 kill table cannot be re-derived from the repo.
- `d6d5eb27…` has no retained bytes at all.
- The sibling mutation tool is outside mado's control. It matches today but can drift (`LOG` F2).
- I did not verify the lesson's statement that "the filed report explicitly excludes excised machinery" beyond `GateRecon.md:174` and `AttackNoHarm.md:24`, which are related but not identical.
- The ReceiptCorrection output path conflict (Observed 11) is open.

## Evidence pointers

- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14-verifier-spotcheck.md:169`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/evidence/regression-recut.txt:1-4,75`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/evidence/regular-target-mutants.txt:1-4,44`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/evidence/retained-census-mutants.txt:1-4,59`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/evidence/gate-selftest.txt:1-4`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:1723-1733` (at `32118fc`)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/reports/GateImplement.md:19`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/reports/ReviewResolver.md:32-34`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/reports/GateRecon.md:174`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md` criteria 4, 6, 7, 9, 10, 13
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/spec.json:19` (ReceiptCorrection output conflict)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` (sha256 `75ed934d…`, read-only)
