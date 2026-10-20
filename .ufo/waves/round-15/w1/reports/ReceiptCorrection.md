# ReceiptCorrection — round 15 / w1 — R14-V1 provisional-header correction

Seat: `MadoR15.ReceiptCorrection` (executor, leaf; no delegation, no background jobs).
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Artifact: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/receipt-correction.json` (28,752 bytes, schema `mado.receipt-correction/v1`).
Axes: **coverage** (preserve the measured mutation findings by making their input binding checkable) and **evidence integrity** (no promotion to measured-full-gate receipts). No score move; R14-V1 stays unscored.

Static only: no gate, harness, mutant, selftest, verifier, `measure.py`, census or live probe was run. Git was used only to read committed blobs; `sed`/`awk`/Python touched bytes in memory only. No credential or `agent.db*` file opened; no omp CLI. No tool installed or upgraded.

## Assignment-shape note

`spec.json` item `ReceiptCorrection` says "Create ONLY `.ufo/waves/round-15/receipt-correction.json`" while acceptance asks for this report. The Change explicitly assigns a disjoint file, so the JSON is the assigned artifact and this report is the mandated advisory write-up. No other file was created or edited; `.ufo/waves/round-14/` is byte-identical (`git diff --stat ea0446f -- .ufo/waves/round-14/` empty).

## What the correction maps

Measured commit `C` = `32118fc1014837b3a385c7a66abbdc59b1560835` (content time 2026-10-20T03:03:28-03:00 = 06:03:28Z). Derivation HEAD `ea0446fcb4840089f0e541d96350144506fb5d1d`.

| Receipt (unchanged) | Original SHA-256 | Provisional `gate_sha256` | Run time (UTC) | `MUTATE_TARGET` |
|---|---|---|---|---|
| `regression-recut.txt` | `d54626345fa0a37efc4ad1f58cc51520a4e8bd5922d717128f4d5cd19199b75b` | `ef50e262f311d74e05afd558883415d2f47fa2a0247a0c834e37f49cb60c742b` | 05:58:44Z | `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96` / 117602 B |
| `regular-target-mutants.txt` | `267de2b54b41a7575716d56fcf4433f44d92b6d2f53b8c05e46d701c4762745f` | `d6d5eb27d5e6811367c9d447f224485460db13f1b832e131296036dc1fd39b36` | 06:00:23Z | same |
| `retained-census-mutants.txt` | `57c462c29984d0e878c4c986ca205bee73dd6e3119b802915be31e5f4b549d81` | `d6d5eb27d5e6811367c9d447f224485460db13f1b832e131296036dc1fd39b36` | 06:01:00Z | same |

All three headers retain `input_binding: provisional worktree snapshot` and carry no `measured_commit` (lines 3-4). The JSON keeps those strings verbatim and labels both provisional digests **unrecoverable, uncommitted, not a whole-gate identity**: neither is the sha256 of any of the nine committed `tools/mado-verify.sh` revisions or of any of the 484 blobs in the object store. `ef50e262…` is the pre-integration worktree gate named by `round-14/w1/reports/GateImplement.md:19` and `ReviewResolver.md:32,34,64`; `d6d5eb27…` appears only in these two receipts. Neither maps to a commit or to the committed gate `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`.

Target identity is content-derived, not header-derived: the run target's sha equals the excision of the committed gate. The excised derivative omits `PIN_MADO`, `SPEC_SHA`, `TABLE_MADO` and `HARNESS_SHA_RECORDED` (they sit inside the R7 regression span), so the derived-target equality does not authenticate those constants; it authenticates the 117,602 retained bytes.

## Target algorithm and exact re-derivation

`mado_r7_target_build()` (`tools/mado-verify.sh:1723-1733` at `C`) deletes inclusive marker ranges for `MADO-R7-REGRESSION-BLOCK`, `MADO-R7-SELFTEST-BLOCK` and `MADO-R8-BLOCK` (the last twice, at 1368-1531 and 1984-2506), leaving 2403 lines / 117,602 bytes.

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 32118fc1014837b3a385c7a66abbdc59b1560835:tools/mado-verify.sh \
  | sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
        -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
        -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' \
  | sha256sum      # → cd1d73d7… ; 117602 bytes
```

Independent Python range-excision reproduced the same bytes/hash. Committed gate bytes: `git show C:tools/mado-verify.sh | sha256sum` → `fba82a66…` (177,849 B, 3,711 lines).

## Spec, harness, kill table, restore

| Receipt | Spec binding | Harness | Kill table | Restore |
|---|---|---|---|---|
| `regression-recut` | run path `/tmp/.../mado-verify.defects.spec` not retained; committed heredoc `mado_r7_spec_write()` (`:1671-1720`) writes `c7ee75b9…` (2141 B, 10 defects) = `SPEC_SHA` (`:1640`) | `75ed934d…` | 10/10 KILLED `D1`–`D9`,`R1`; equals `TABLE_MADO` (`:1642`); receipt `:77` | `:75` OK, before = after = pristine `cd1d73d7…` |
| `regular-target-mutants` | `.ufo/waves/round-14/w1/regular-target.spec` `45f1fcd3…` (1119 B, 4 defects) | same | 4/4 KILLED `RT1`–`RT4`; `:46` | `:44` OK |
| `retained-census-mutants` | `.ufo/waves/round-13/covering.spec` `d7cc64ca…` (1264 B, 8 defects; unchanged since `95cbc41`) | same | 8/8 KILLED `P1`–`P8`; `:61` | `:59` OK |

Spec bytes at run time are not sha-bound in the receipts. What is proven: the committed spec defect semantics (`@defect` id/description, `@old`/`@new`) and **all 22 mutant sha256** reproduce exactly by applying each replacement once to the committed derived target (harness `cmd_apply` semantics, `frozen/harness.sh:351-372`), each `@old` count = 1. So the historical spec gap is closed at the semantic and mutant-byte level even though the `/tmp` file is gone; the committed gate's own frozen replay independently prints `REGRESSION_SPEC` sha `c7ee75b9…`.

Harness role is split and stated as such: `MUTATE_TOOL` `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` (77,904 B) is the mutable sibling path, currently equal to committed `frozen/harness.sh`; it is not the gate constant `HARNESS_SHA_RECORDED='b56c6e57…'` (`:1641`, printed as provenance, not gated).

## Correct reading (no relabeling)

- These are **not standalone final full-gate receipts**; they measured the excised derivative. No run executed commit `C` or the whole gate `fba82a66…`.
- Inputs are statically reproduced (target, defect semantics, 22 mutant digests). KILLED verdicts, exits, durations and GREEN controls remain **recorded observations**, not re-executed; the historical 10/10 additionally has a commit-bound frozen replay in `frozen-regression.txt`.
- `267/267` is the derived target's selftest control; the committed full gate is `372/372` (`gate-selftest.txt`). Commit-bound full-gate references named in the JSON: `gate-selftest.txt`, `gate-file-plane.txt`, `frozen-regression.txt`.
- `regular-target.spec:3` still says "no mutant was run"; that stale comment is historical and untouched.
- No wrapper, gate edit, new criterion, receipt rewrite or score move. Historical bytes preserved and pinned by the three subject sha256 values.

## Limits

`ef50e262…`/`d6d5eb27…` cannot be reconstructed, so the excision equality rests on the recorded `MUTATE_TARGET` plus the committed-byte derivation, not on retained pre-images. The sibling harness can drift. RT/P spec file bytes at run time are not independently attested comment-for-comment. No outcome was re-measured and no live/substrate state is claimed.

Files changed: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/receipt-correction.json` (created) and this report (created). Nothing else.
