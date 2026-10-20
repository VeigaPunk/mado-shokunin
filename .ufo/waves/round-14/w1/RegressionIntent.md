# RegressionIntent — exact recut and regular-source coverage

**Axes:** coverage; operability. **Scope:** read-only inspection only; no gate edits, tests, mutation runs, or installs.

## Evidence and current boundary

- `tools/mado-verify.sh:2374-2402` checks the 18 declared source strings as an exact set and then compares their positions against `EXPECT`; `hypr.root.include_graph` is the owning row for source-set/order failure. This order check already exists.
- `tools/mado-verify.sh:2404-2436` checks source targets under `$ROOT`: direct targets currently pass on `[ -e "$x" ]`; a glob currently passes when `compgen -G "$x"` finds any match. Neither path filters for regular files. A directory at a direct target, or a directory matched by the wildcard, therefore satisfies the current existence test. `hypr.root.sources_resolve` is the target-resolution row.
- Selftest scenarios N1–N8 (`tools/mado-verify.sh:1056-1168`) cover exact-set substitutions, missing `gkeep.conf`, empty source, and conditional directives. N2 proves an existing undeclared replacement still fails set membership; there is no source-order-only permutation fixture in this series. Round-13 `covering.spec` has P1–P8 for census/parser cases only; its recorded sweep reported 8/8 killed (`.ufo/waves/round-13/evidence/covering-mutants.txt:1-8,57-59`). These are prior-round receipts, not a new run or coverage of the regular-file predicate.
- The separate embedded historical regression remains D1–D9/R1: `SPEC_SHA=c7ee75…`, `TABLE_MADO` has ten KILLED entries (`tools/mado-verify.sh:1430-1433`). The round-13 recut receipt measured that set 10/10 killed with GREEN control and restore OK (`.ufo/waves/round-13/evidence/regression-recut.txt:1-9,71-77`). Do not infer a new round-14 measurement from it.

## Exact owner recut recipe

`mado_r7_target_build()` (`tools/mado-verify.sh:1514-1525`) derives the mutation target by deleting these marker ranges; any gate/selftest edit outside them changes the derived target and requires a PIN recut:

```bash
sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
    -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
    -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' \
    "$1" >"$2"
```

After integration, the gate owner runs `bash tools/mado-verify.sh --regression --keep`. On a derived-target pin mismatch, the gate refuses before starting its sweep, keeps the scratch root, and prints the path-expanded `REGRESSION_RECUT` command. Run **that exact printed command**; its argument shape is:

```bash
bash "$harness" --target "$target" --defects "$spec" \
  --suite 'bash "$MUTANT" --selftest' --workdir "$root/recut" \
  --label mado-verify.sh
```

Do not reuse the old `/tmp` paths in the recorded round-13 example. Update `PIN_MADO` only from the measured derived-target SHA and `TABLE_MADO` only from the measured defect table; require all recorded rows, zero flips/inconclusive, GREEN control, `MUTATE_RESTORE: OK`, and unchanged target bytes (source `:1611-1628,1682-1693`). The ordinary successful replay emits `MADO_REGRESSION: PASS`; the run is not performed by this report author.

## Required new coverage

1. Add isolated `--root … --no-live` selftest fixtures for a declared direct source whose target is replaced by a directory, and for a wildcard source whose expansion includes a directory. For the glob, include a mixed regular-file-plus-directory match case so a check that merely finds one regular match cannot silently accept the directory member. Assert exit 1 / `MADO_VERIFY: DIVERGED`, `hypr.root.sources_resolve FAIL` with a stable diagnostic naming the offending declared target or expansion, and `hypr.root.include_graph PASS` (the declarations/order are unchanged). Keep other rows isolated where feasible. The exact diagnostic wording is an implementation choice; preserve the owning row and stable path-bearing failure.
2. Add a regular-predicate defect to the **round-14 covering spec**, separate from the embedded historical D1–D9/R1 spec. Mutate away the regular-file guard(s); the direct-directory and glob-directory fixtures must kill the corresponding mutation(s). If direct/glob checks are separate code paths, cover each path separately; if shared, prove the shared mutant is killed by both fixtures. Require a GREEN control and `MUTATE_RESTORE: OK`; report measured outcomes, not an assumed kill count. The round-13 covering sweep's invocation pattern is `bash <mutate-and-run.sh> --target <fresh derived target> --defects <round-14 covering.spec> --suite 'bash "$MUTANT" --selftest' --workdir <fresh workdir> --label mado-r14-covering` (`round-13/evidence/covering-mutants.txt:1`).
3. Add an **order-only** negative fixture by permuting two declared source lines while preserving the same exact member set and existing targets. Assert `hypr.root.include_graph FAIL` (line/order diagnostic) and `hypr.root.sources_resolve PASS`. This is a regression guard for already-implemented ordering, not a claimed round-14 behavior improvement. Keep the local inventory unchanged.

## Frozen package handoff

Round-13 `frozen/verify.py` pins exactly `gate.sh` and `harness.sh` in `expected.json`, checks their raw SHA-256s, invokes the frozen gate with `MADO_VERIFY_HARNESS` set to the bundled harness, and requires the pinned exit and marker (`frozen/verify.py:24,56-76,79-133`). Its recorded receipt is for the old hashes (`frozen/expected.json:2-7`; `evidence/frozen-regression.txt:1-22`), so it cannot certify round-14 source behavior. Preserve round-13 frozen artifacts; use the parent-owned round-14 frozen copy and pins. The verifier invocation pattern is `python3 .ufo/waves/round-14/frozen/verify.py`, followed by its `--selftest` when the parent runs the planned final checks; neither was run here.

## Provenance / confidence

Direct source reads establish the implementation and command mechanics; recorded round-13 evidence establishes only its historical measured results. No LSP device is mounted in this session (`read xd://lsp` reported no such tool); the text search was navigational only, not semantic proof. Confidence is high for the recut/frozen mechanics and current `[ -e ]` / glob behavior; the fixture assertions above are the minimal recommended operationalization of the requested regular-target contract.
