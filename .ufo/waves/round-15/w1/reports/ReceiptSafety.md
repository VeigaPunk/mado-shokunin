# ReceiptSafety — R14-V1 correction: overclaim / history-alteration audit

Seat: `MadoR15.ReceiptSafety` (sentinel, leaf). Static read only. No gate, harness, mutant, selftest, verifier, `measure.py`, census or live probe was run. git was used only to read committed bytes (`git show`, `cat-file --batch`). `sed`/Python were applied only to bytes in memory, then hashed. No credential or `agent.db*` file was opened, and no omp CLI was launched. Tool installs or updates: **none**.

Axes: (a) **no history alteration**, meaning byte preservation of R14 evidence; (b) **no execution overclaim**, meaning claims stay within what the bytes prove; (c) **coverage neutrality**, meaning R14-V1 stays unscored.

## Verdict

At audit time the correction artifact had **not landed**: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/receipt-correction.json` was absent, and no `corpus/` or `LOG.md` correction was present (`git status`). The only R14-V1 text currently written is the round-15 SCORECARD claim at `SCORECARD.md:613-617`. That text is safe. It preserves historical records, appends a mapping, adds no wrapper and changes no gate. Nothing in the tree has been altered (see H1). The verdict below is therefore a **conditional acceptance contract** for the artifact when it lands, built on facts verified here.

## Verified facts (static; all against `32118fc1014837b3a385c7a66abbdc59b1560835` = C)

| # | Fact | Evidence |
|---|---|---|
| H1 | The historical receipts and TSVs are byte-identical at C, at HEAD `ea0446f` and in the worktree. | sha256 `regression-recut.txt` `d54626345fa0a37efc4ad1f58cc51520a4e8bd5922d717128f4d5cd19199b75b`; `regular-target-mutants.txt` `267de2b54b41a7575716d56fcf4433f44d92b6d2f53b8c05e46d701c4762745f`; `retained-census-mutants.txt` `57c462c29984d0e878c4c986ca205bee73dd6e3119b802915be31e5f4b549d81`; `historical-results.tsv` `573dba02…32e9`; `regular-target-results.tsv` `198fcd70…a87e`; `retained-census-results.tsv` `3e78c5fd…99c3` |
| F1 | The derived target re-derives from committed bytes. | Applying the `mado_r7_target_build` sed to `git show C:tools/mado-verify.sh` (`fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`, 177849 B) gives `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`, 117602 B. Real `sed` and an independent Python range-excisor agree. The committed `frozen/gate.sh` excises to the same value. This equals `PIN_MADO` at C and `committed-bindings.json` `derived_target_sha256`. |
| F2 | **All 22 mutant inputs are statically bound.** | Applying each committed spec's `@old`→`@new` once (the harness `cmd_apply` semantics, `frozen/harness.sh:351-372`) to the F1 bytes reproduces every `mutant-sha256` in the three TSVs exactly: 10/10, 4/4 and 8/8, each `@old` count = 1. The defect IDs and descriptions in each receipt equal the committed spec's `@defect` lines. Specs: gate heredoc body `c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8` (= `SPEC_SHA`, 10 defects); `w1/regular-target.spec` `45f1fcd33df4d38bc231d665656421512c6accf7918a7325cb3822ea38ecdc08`; `round-13/covering.spec` `d7cc64ca351f046264fbbc9fc047b0427e55167c6e5fd9949c6e37dd1cd63340` (unchanged since `95cbc41`). |
| F3 | The provisional whole-gate hashes are **unrecoverable**. | Neither `ef50e262f311d74e05afd558883415d2f47fa2a0247a0c834e37f49cb60c742b` nor `d6d5eb27d5e6811367c9d447f224485460db13f1b832e131296036dc1fd39b36` is the sha256 of any of the 433 blobs in the mado object store. `ef50e262…` is the 3,711-line pre-commit delivery named in `round-14/w1/reports/GateImplement.md:19` and `ReviewResolver.md:34`. `d6d5eb27…` has no other record. |
| F4 | The receipts predate the measured commit. | `MUTATE_DATE` values are 05:58:44Z, 06:00:23Z and 06:01:00Z. Content commit C is 06:03:28Z, and the frozen replay is at 06:04:11Z. The whole gate moved at least twice afterward (ef50→d6d5→fba8, 3711→3712 L) while the excised target stayed `cd1d73d7…`. [INFERENCE] The moves lie inside the excised pairs; the bytes are not retained. |
| F5 | The harness binding is split. | Receipt `MUTATE_TOOL` `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` is the mutable sibling path. The same digest is the committed `frozen/harness.sh` at C. The gate's `HARNESS_SHA_RECORDED` is `b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb`, labelled “provenance, not gated” (`frozen-regression.txt`). |
| F6 | The control and full-gate counts differ. | The derived-target `CONTROL: GREEN` is **267/267**. The full gate `gate-selftest.txt` is **372/372** at C/`fba82a66…`. |
| F7 | Only the historical spec has a commit-bound replay. | `frozen-regression.txt` carries `measured_commit` C and `gate_sha256` `fba82a66…`, verifies the gate and harness inputs, uses `REGRESSION_SPEC` `c7ee75b9…` and matches 10/10. No commit-bound replay exists for RT1–RT4 or P1–P8. |
| F8 | A committed spec comment is stale. | `w1/regular-target.spec:3` says “no mutant was run”, yet `regular-target-mutants.txt` records a run. It is historical text inside a pinned file (`45f1fcd3…`). |

## Exploit paths and boundaries the correction must hold

| Sev | Exploit path (overclaim / alteration) | Why it is false or harmful | Smallest remediation |
|---|---|---|---|
| High | Rewriting the receipt headers to `measured_commit: C` / `gate_sha256: fba82a66…` / a non-provisional `input_binding`, or replacing a file with a “corrected” copy. The MistakeRecord green fixture (`input_binding: committed …`) invites this. | Destroys H1 and fabricates provenance: those runs never executed `fba82a66…` (F4). | Keep the bytes. The correction is a sidecar or appended block. Assert the H1 sha256 values are unchanged. Scope any header check to **future** receipts only. |
| High | Saying the receipts “ran against”, “are bound to” or “measured” commit C or the full gate `fba82a66…`. | They executed a `/tmp` target built from uncommitted gate bytes before C (F3, F4). Only **sha equality** of that target with the excision of C is proven (F1). | Use wording such as: “target sha equals excise(C); run-time whole gate ef50/d6d5 not retained.” |
| High | Mapping `ef50e262…` or `d6d5eb27…` to a commit, to `fba82a66…`, or to “the committed gate”. | Neither digest has bytes anywhere in git (F3). | Label both “provisional, unrecoverable, not a committed identity.” |
| Med | Claiming the 10/10, 4/4 and 8/8 kills were re-verified, re-derived or reproduced by the correction. | F2 proves the **inputs**: target bytes, spec semantics and each mutant's bytes. The KILLED **outcomes** remain recorded and are not re-executed. Only the historical 10/10 has a separate commit-bound replay (F7). | Use two separate labels: “inputs statically reproduced” and “outcomes recorded (RT/P: no commit-bound replay).” |
| Med | Calling the RT and P spec bytes at run time identical to the committed bytes. | The receipts print `MUTATE_SPEC … defects=N` without a sha. F2 binds the ID, description and `@old/@new` semantics, not the comment bytes. | Say “defect semantics equal committed spec,” not “spec bytes equal.” |
| Med | Calling `b56c6e57…` the harness used, or `75ed934d…` an unmutable committed tool. | The receipts ran the sibling path. The frozen copy matches today, but the sibling can drift (F5). | Cite both digests with their roles. |
| Low | Citing 267/267 as the gate selftest, or 372/372 as a mutation-suite control. | These are different executables (F6). | Keep both numbers with their target. |
| Low | “Fixing” the F8 comment in `regular-target.spec`. | That changes the pinned `45f1fcd3…` in `committed-bindings.json`. | Note it in the correction only. |
| Low | Moving C1, C2 or any SCORECARD/LOG score because of R14-V1. | The goal and `SCORECARD.md:613` make it unscored. | Keep the correction coverage-neutral. |

## Acceptance checklist for `receipt-correction.json` (or the L1 append)

1. H1 digests are unchanged, as is every committed R14 evidence/frozen/spec byte (`git diff --quiet ea0446f -- .ufo/waves/round-14/`).
2. There is one row per receipt with full 64-hex values: the provisional `input_binding`, the old `gate_sha256` labelled unrecoverable, `MUTATE_TARGET` `cd1d73d7…`/117602, the spec digest (committed path), the harness `75ed934d…`, `MUTATE_DATE`, and the recorded counts.
3. The re-derivation commands name C, not the worktree:
   `git show 32118fc1014837b3a385c7a66abbdc59b1560835:tools/mado-verify.sh | sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' | sha256sum` → `cd1d73d7…`. Spec digests use `git show C:<spec> | sha256sum`.
4. The correction contains an explicit caution: these are **not standalone final full-gate receipts**. The commit-bound full-gate receipts are `gate-selftest.txt`, `gate-file-plane.txt` and `frozen-regression.txt`.
5. It adds no wrapper, no gate edit and no new QUALITY criterion (QUALITY 7/9/13 already cover the rule).

Rejection on any single item: altered bytes; a commit mapping for ef50/d6d5; a claim that the run executed against C; an execution or re-verification claim; prefix-only digests; a worktree-based derivation; or a score move.

## Peer note

I sent F2–F5 and F8 to `MadoR15.ReceiptCorrection` (agent message) before it landed its artifact. Disagreement with `ReviewRouted.md:55,66,74`: the regression-recut spec **is** recoverable from committed bytes. Its source is the gate heredoc `c7ee75b9…`, and its mutants reproduce exactly (F2). The 10/10 also has a commit-bound frozen replay (F7). Only the KILLED outcomes are non-reproducible statically. Also, `MUTATE_TOOL` digest equals the committed `frozen/harness.sh`.

Report path: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/ReceiptSafety.md`
