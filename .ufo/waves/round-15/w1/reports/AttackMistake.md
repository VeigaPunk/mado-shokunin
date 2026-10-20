# AttackMistake — R14-V1 mapping attack (provisional full gate vs exact derived target)

Seat: critic, leaf. Axis: coverage, plus the unscored R14-V1 provenance correction. This report gives no verdict.
Method: read-only `git show`/`cat-file`, and static byte transforms in a private Python process: sed-equivalent excision and the harness's own single-replace rule on committed bytes. No gate, selftest, harness or mutation suite was run. No tools were installed.

## Verified facts (recomputed by this seat)

| # | Fact | Evidence |
|---|---|---|
| F1 | The committed raw gate is `fba82a66…c207` (177849 B, 3711 lines). It is the same at 32118fc, 97c3583, ea0446f and the worktree. It matches neither provisional header. | `git show REV:tools/mado-verify.sh \| sha256sum`; `.ufo/waves/round-14/evidence/committed-bindings.json` |
| F2 | The provisional headers name two different worktree states, not one: `regression-recut.txt:4` = `ef50e262…` (MUTATE_DATE 05:58:44Z); `regular-target-mutants.txt:4` and `retained-census-mutants.txt:4` = `d6d5eb27…` (06:00:23Z and 06:01:00Z). | receipts lines 3–4 and 7 |
| F3 | Neither `ef50e262…` nor `d6d5eb27…` exists in the repository object store. I hashed all 13 blobs of 100–200 kB, which includes the 177849 B gate. Those bytes cannot be recovered. | `git cat-file --batch-all-objects` + sha256 |
| F4 | Excising the committed gate with the exact sed of `mado_r7_target_build` (`tools/mado-verify.sh:1723-1733`) gives `cd1d73d7…3f96`, 117602 B. This equals `MUTATE_TARGET`, CONTROL pristine and MUTATE_RESTORE in all three receipts. It also equals `PIN_MADO` (`:1639`) and `derived_target_sha256` in committed-bindings. | static sed + Python re-implementation; both match |
| F5 | All 22 TSV `mutant-sha256` values reproduce byte-for-byte: 10/10 `historical-results.tsv`, 4/4 `regular-target-results.tsv`, 8/8 `retained-census-results.tsv`. Each one equals the committed derived target with that defect's single replacement applied from the committed spec. Every `@old` count is 1. | Harness rule `tameshi-shokunin/tools/mutate-and-run.sh:359-366` (sha `75ed934d…` = MUTATE_TOOL). Specs: embedded MADO_R7 heredoc at 32118fc (body sha `c7ee75b9…` = SPEC_SHA), `regular-target.spec` `45f1fcd3…`, `round-13/covering.spec` `d7cc64ca…` |
| F6 | The receipt DEFECT ids and descriptions match the committed spec `@defect` lines in order (10, 4 and 8). | static parse |
| F7 | All three runs (05:58–06:01Z) happened **before** commit 32118fc (03:03:28-03:00 = 06:03:28Z). `frozen-regression.txt` (06:04:11Z) is the only regression receipt that ran after the commit. Its `measured_commit: 32118fc…` header is consistent with that. | `git show -s --format=%cI 32118fc`; MUTATE_DATE / REGRESSION_DATE |
| F8 | The derived target leaves out 60247 B and 1308 lines of the gate, in four blocks: R7-SELFTEST `:440-619`, R8 `:1368-1531`, R7-REGRESSION `:1543-1983` and R8 `:1984-2506`. `MADO-R8-OMARCHY-BLOCK` (`:622-801`) is **not** excised, because the sed matches only the exact `MADO-R8-BLOCK`. The derived-target control selftest is 267/267, while the full-gate selftest is 372/372. | `grep -n MADO-R` at HEAD (same bytes as 32118fc); `regression-recut.txt:11`; `gate-selftest.txt:6` |
| F9 | The MUTATE_SPEC lines in the receipts have no spec sha. `committed-bindings.json` binds `regular-target.spec` but not `round-13/covering.spec`, and it does not bind the /tmp recut spec. | receipts line 9; committed-bindings.json |
| F10 | The receipt and TSV bytes are unchanged since 32118fc. This gives the append-only anchors: recut `d5462634…b75b`, regular `267de2b5…745f`, retained `57c462c2…1d81`, historical TSV `573dba02…32e9`, regular TSV `198fcd70…7caf`, retained TSV `3e78c5fd…99c3`. | `git show HEAD:… \| sha256sum`; `git log` shows only 32118fc |

## Counterexamples (ways the correction could launder the headers)

**C1 — The proposed green fixture would be false provenance.** `MistakeRecord.md:62` builds a passing header with `measured_commit: 32118fc1…`, `gate_sha256: fba82a66…` and `input_binding: committed 32118fc1…`. F7 shows all three runs happened before 32118fc existed, and F1/F3 show the bytes they read were `ef50e262…`/`d6d5eb27…`, not `fba82a66…`. If the correction writes that header into, or next to, these receipts as their binding, it asserts a measurement that never happened. The header check in `MistakeRecord.md` §3 would then go green on a laundered receipt, because it checks only shape (its own caveat at `:66`).
*Smallest fix:* the correction must never give these runs `measured_commit` or `gate_sha256`. Instead, add a separate `derived_from` relation: "derived target `cd1d73d7…` = excise(`git show 32118fc:tools/mado-verify.sh`)". Mark it re-derived later, not measured at the commit.

**C2 — One "provisional header" mapping hides two pre-commit states.** F2 shows two distinct raw gates (`ef50e262…` → `d6d5eb27…` → committed `fba82a66…`), each with the same derived target. `GateImplement.md:19` and `ReviewResolver.md:62-64` call `ef50e262…` the reviewed final bytes. That means at least two later edits fell inside the excised blocks, and their content is unrecoverable (F3).
*Smallest fix:* map each receipt separately, with its own header value and MUTATE_DATE. Record raw `ef50e262…`, `d6d5eb27…` and `fba82a66…` as *distinct and unrecoverable*. State only that their non-excised bytes are equal; this follows from the identical excision output. Do not claim the raw gates are equal or that the difference was a no-op.

**C3 — Mixing up the full-gate digest and the derived-target digest.** The proposed value-level extension (`MistakeRecord.md:73`, `gate_sha256 == git show …\|sha256sum`) is correct for whole-gate receipts like `gate-selftest.txt`. It is the wrong check for mutation receipts. A mutation receipt binds the derived target, so a check against `fba82a66…` would grade bytes that the suite never mutated (F8: 1308 excised lines, 105 selftest assertions outside the kill suite).
*Smallest fix:* a future standalone mutation receipt binds `derived_target_sha256` (excise of `git show REV`), `spec_sha256` and the harness sha, alongside `measured_commit`. The full-gate `gate_sha256` stays informational only.

**C4 — Spec input is bound only by path.** F9 shows no spec sha in the receipts. `covering.spec` is missing from committed-bindings, and the recut spec lived in /tmp, read from the *provisional* excised R7 block, which the derived-target equality does not cover. If the correction maps only header → derived target, the spec half of the input stays unbound.
*Smallest fix:* cite F5 in the correction. The 22 TSV mutant hashes re-derive exactly from committed bytes: derived target + committed spec + harness rule. That binds both target and spec to committed content without using the provisional headers. It also proves only that the *mutant inputs* match. GREEN, KILLED and RESTORE verdicts remain observations from the historical run, not reproductions.

**C5 — The excised-block list can be over-stated.** A correction that lists "R7/R8 machinery" as excised could imply that `MADO-R8-OMARCHY-BLOCK` is excluded. It is not (F8): it lies inside the mutated, graded target.
*Smallest fix:* list the four exact excised ranges with their marker names.

**C6 — Rewriting history.** Editing the receipts' lines 3–4 (or the TSVs) breaks the anchors in F10. It also breaks the verifier's "keep historical bytes" instruction (`round-14-verifier-spotcheck.md:169`).
*Smallest fix:* put the correction only in a new append-only file (e.g. `.ufo/waves/round-15/receipt-correction.json`). Record each original's sha256 as `subject_sha256`, so later tampering is detectable.

## No harm found to existing claims

- The round-14 C2 kill counts (10/10, 4/4, 8/8) and `SCORECARD.md:536-545` already limit themselves to "documented derived executable, not excised R7/R8 machinery". F4 and F5 strengthen that statement; nothing here contradicts it.
- `frozen-regression.txt` is correctly bound after the commit (F7) and stays the authority for "regression table reproduces at the committed gate".
- Defect status: a fixable precision gap, not a tradeoff the judge must reject. If C1–C6 are respected, the correction is admissible and status-neutral, as routed.

## Impacted axes

- Coverage (C1 U6): no impact. R14-V1 is unscored.
- Provenance/quality (QUALITY 7/9/13 per peers): affected only if C1 or C3 is adopted. Either would turn an honest provisional label into a false committed binding.

## Acceptance conditions for the correction artifact

Accept the correction only if:
1. Each receipt is mapped separately, with its literal header value.
2. Run time is recorded as before the commit (no `measured_commit` for these runs).
3. The `cd1d73d7…` derivation is stated as excise(`git show 32118fc:tools/mado-verify.sh`).
4. The F5 mutant-hash re-derivation is cited for the spec binding.
5. The four excised ranges are stated exactly.
6. The original sha256 anchors (F10) are included.
7. No receipt or TSV bytes change.

Reject it if any header is restated as `fba82a66…`, `measured_commit: 32118fc…` or `input_binding: committed`.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/AttackMistake.md
