# R14-V1 — raw gate PIN vs `MUTATE_TARGET`

**Axes:** object identity; commit provenance; mutation-claim scope.

## Reconstructed contract

`gate_sha256` and `MUTATE_TARGET` identify different byte objects. The former is the receipt header's raw whole-gate snapshot digest; the latter is the temporary executable passed to the mutation harness after mado's derived-target excision. `PIN_MADO` pins that derived executable, not the whole `tools/mado-verify.sh` file.

In `tools/mado-verify.sh:1723-1733`, `mado_r7_target_build` writes a target by deleting each inclusive, marker-delimited region for `MADO-R7-REGRESSION-BLOCK`, `MADO-R7-SELFTEST-BLOCK`, and `MADO-R8-BLOCK`. The source has one R7 selftest span (`:440-619`), two R8 spans (`:1368-1531`, `:1984-2506`), and the R7 regression span (`:1543-1983`). The helper's comment explains that excising R8 additions too preserves the target when those additions ride along (`:1724-1728`). Thus “two MADO-R7 blocks excised” is not the complete implementation description: the builder also strips the R8 spans.

`PIN_MADO` is `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96` (`:1639`). The regression path builds the temporary target, hashes it and refuses with SETUP if it differs from `PIN_MADO`, then passes that same target and pin into `regression_case` (`:1882-1902`). The code says changes outside the excised blocks require a re-cut (`:1568-1571`); mutations to the excised machinery are outside this table's tested scope.

## Evidence chain and divergence

- The three historical receipts label their input `provisional worktree snapshot` and have no `measured_commit`: `.ufo/waves/round-14/evidence/regression-recut.txt:3-4`; `regular-target-mutants.txt:3-4`; `retained-census-mutants.txt:3-4`. Their raw `gate_sha256` headers are respectively `ef50e262…`, `d6d5eb27…`, `d6d5eb27…`—not the committed whole-gate digest.
- Each receipt separately records `MUTATE_TARGET` as the same derived-target SHA above (117,602 bytes), with a GREEN control whose pristine digest matches and a `MUTATE_RESTORE` line whose before/after digests match: `regression-recut.txt:8,10,75`; `regular-target-mutants.txt:8,10,44`; `retained-census-mutants.txt:8,10,59`. Their measured tables are 10/10, 4/4 and 8/8 KILLED, respectively (same files, final `MUTATE` lines).
- The committed binding is `32118fc1014837b3a385c7a66abbdc59b1560835` with raw whole-gate SHA `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` (`.ufo/waves/round-14/evidence/after.txt:3-4`). Its committed-input frozen regression records that raw gate digest, then derives target SHA `cd1d73…`, matches the recorded pin and passes 10/10 (`frozen-regression.txt:3-20`). This links the provisional receipts' `MUTATE_TARGET` identity to the committed target, while **not** converting their stale raw-gate headers into commit-bound whole-gate receipts.

**R14-V1 disposition:** preserve the three historical files; append an explanatory mapping from each provisional raw-gate header to committed derived target `cd1d73…`. Do not call these standalone final-full-gate receipts, rewrite their bytes, or change gate behavior. This is ancillary provenance precision, not a mutation-coverage failure (`corpus/lessons/round-14-verifier-spotcheck.md:169`; `SCORECARD.md:613-616`).

**Method / confidence:** high confidence in the object mapping and scope, from the inspected helper, pin/guard and retained receipts; no tests, gates, or runtime probes run. No LSP device/tool is mounted (checked `xd://lsp`); text search was used only to locate definitions, and semantic claims above come from read source lines and recorded evidence. No tools installed or updated.