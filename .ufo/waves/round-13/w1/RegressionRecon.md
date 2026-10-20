# RegressionRecon — Regression Target Excision, Defect Anchors D1–D10, Recut Workflow, and Harness Path

- **Seat**: `MadoR13.RegressionRecon` (scout)
- **Role**: Scout (read-only investigation, ground truth from source)
- **Wave**: `mado-r13-w1` · 2026-10-20
- **Target Repository**: `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Output Report**: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/RegressionRecon.md` (and mirrored at `.ufo/waves/round-13/w1/reports/RegressionRecon.md`)
- **Status**: Final Scout Deliverable (no tests/build/lint/formatting run; no shared repository files edited).

---

## 1. Executive Summary & Core Ground Truth

1. **Regression Target Excision Mechanism**:
   The gate `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` defines `mado_r7_target_build()` (`:1477-1488`). It derives the regression target by excising three marker block families from itself using `sed`:
   - `MADO-R7-REGRESSION-BLOCK` (`# >>> MADO-R7-REGRESSION-BLOCK >>>` to `# <<< MADO-R7-REGRESSION-BLOCK <<<`, `:1307-1725`)
   - `MADO-R7-SELFTEST-BLOCK` (`# >>> MADO-R7-SELFTEST-BLOCK >>>` to `# <<< MADO-R7-SELFTEST-BLOCK <<<`, `:415-594`)
   - `MADO-R8-BLOCK` (two ranges: `:1133-1296` wrapping scenario S in `selftest()`, and `:1726-2248` wrapping snapshot & diff CLI functions)
   
   *Crucial Invariant*: `MADO-R8-OMARCHY-BLOCK` (`:601-780`) is **not** excised. The derived target represents the frozen code surface under mutation test.

2. **Defect Anchors (D1–D10 / D1–D9 + R1)**:
   The embedded defect spec in `mado_r7_spec_write()` (`:1425-1475`) defines exactly 10 defects across 6 contract clauses (A–F):
   - **D1**: Clause A (`CLEAN` verdict token renamed to `OK`)
   - **D2**: Clause B (`UNKNOWN` guard dropped from `CLEAN` condition)
   - **D3**: Clause B (`live.plane` row reports `PASS` instead of `SKIP` when live layer skipped)
   - **D4**: Clause C (`DIVERGED` exit path changes from `exit 1` to `exit 0`)
   - **D5**: Clause C (`failing --selftest` returns `1` instead of `2`)
   - **D6**: Clause D (Local inventory mutant: historically dropped `xdph` from 12-conf list; in round 13, local inventory was updated with `LOCAL+=(gkeep)`, keeping the 12-conf literal base so D6's `@old` anchor remains unique and valid)
   - **D7**: Clause D (`include_graph` count check `-ne` changed to `-lt`)
   - **D8**: Clause E (`hyprland.conf` sha pin comparison always matches: `$sha = "4f52854a3c14"` replaced with `-n "$sha"`)
   - **D9**: Clause E (read-only boundary comparison always reads byte-identical: `$after = "$before"` replaced with `-n "$after"`)
   - **R1** (10th defect): Clause F (reader fallback: `walker.config` row reports `PASS` instead of `UNKNOWN` when `tomllib` unavailable)

3. **Read-Only Harness Path & Contract**:
   - Pinned harness: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh`
   - Invocation environment variable: `MADO_VERIFY_HARNESS` (defaults to `$MADO_R7_FLEET/tameshi-shokunin/tools/mutate-and-run.sh`)
   - The harness is strictly read-only: it copies the target into a pristine file, creates ephemeral mutant copies, verifies target hash before and after (`MUTATE_RESTORE: OK`), and runs `--suite 'bash "$MUTANT" --selftest'`.

4. **Recut Workflow**:
   - Running `bash tools/mado-verify.sh --regression` compares the derived target's SHA-256 against `PIN_MADO`.
   - On mismatch, it exits with code `2` (SETUP) and prints the exact `REGRESSION_RECUT` command.
   - The developer / L1 planner runs the printed command, observes 10/10 KILLED with `MUTATE_RESTORE: OK`, and updates `PIN_MADO` (and `TABLE_MADO` if verdicts change).

5. **Edits Forcing New Target vs New Spec**:
   - **New Target (`PIN_MADO`)**: Any edit *outside* the excised marker pairs (e.g. edits in `verify()`, `build_fixture()`, helper functions, or new scenarios outside R7-SELFTEST/R8-BLOCK) changes the derived target bytes and SHA-256, forcing a recut of `PIN_MADO`.
   - **New Spec (`SPEC_SHA`)**: Only edits that change the 10 defect definitions in `mado_r7_spec_write()`, add an 11th defect (e.g., a theme-clause mutant), or alter an anchor string so that `@old` ceases to match uniquely against the target code will force a new spec and a recalculation of `SPEC_SHA`.

---

## 2. Regression Target Excision Deep-Dive

### 2.1 The Excisor Implementation
In `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`:
```bash
mado_r7_target_build() { # <src-file> <dest-file> — excise the MADO-R7/R8 marker blocks
  sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
      -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
      -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' \
      "$1" >"$2" || return 1
  [ -s "$2" ]
}
```

### 2.2 Excision Block Boundaries in `mado-verify.sh`
1. **`MADO-R7-SELFTEST-BLOCK`**:
   - Start: Line 415 (`# >>> MADO-R7-SELFTEST-BLOCK >>>`)
   - End: Line 594 (`# <<< MADO-R7-SELFTEST-BLOCK <<<`)
   - Contents: Scenario R (`--regression` engine unit selftests using runner stub, stub verdicts, exit map assertions R1–R13, R10 derived target check).
2. **`MADO-R8-BLOCK` (First Occurrence — Scenario S)**:
   - Start: Line 1133 (`# >>> MADO-R8-BLOCK >>>`)
   - End: Line 1296 (`# <<< MADO-R8-BLOCK <<<`)
   - Contents: Scenario S (snapshot and snapshot-diff selftests S1–S10).
3. **`MADO-R7-REGRESSION-BLOCK`**:
   - Start: Line 1307 (`# >>> MADO-R7-REGRESSION-BLOCK >>>`)
   - End: Line 1725 (`# <<< MADO-R7-REGRESSION-BLOCK <<<`)
   - Contents: Header documentation, `PIN_MADO`, `SPEC_SHA`, `TABLE_MADO`, table helper functions, `mado_r7_spec_write()`, `mado_r7_target_build()`, `regression_case()`, and `mado_r7_regression_cli()`.
4. **`MADO-R8-BLOCK` (Second Occurrence — Snapshot CLI)**:
   - Start: Line 1726 (`# >>> MADO-R8-BLOCK >>>`)
   - End: Line 2248 (`# <<< MADO-R8-BLOCK <<<`)
   - Contents: Implementation of `--snapshot` and `--snapshot-diff` CLI parsing, execution, and rendering.

### 2.3 Non-Excised Marker Blocks:
- **`MADO-R8-OMARCHY-BLOCK`** (`:601-780`): Contains scenarios OM (omarchy drift watch). Because it is not deleted by the `sed` expression, any modification inside `MADO-R8-OMARCHY-BLOCK` alters the derived target bytes and thus invalidates `PIN_MADO`.

---

## 3. Defect Anchors D1–D10 (Clauses A–F)

The 10 defects embedded in `mado_r7_spec_write()` (`:1425-1475`) define the mutation surface:

| Defect ID | Clause & Concept | Target `@old` String in Code | Replacement `@new` String | Target Location in Code | Kill Mechanism in `--selftest` |
|---|---|---|---|---|---|
| **D1** | **Clause A**: File-plane verdict token | `MADO_VERIFY: CLEAN (%s pass, %s notes; file plane only` | `MADO_VERIFY: OK (%s pass, %s notes; file plane only` | `verify()` (`:3342`) | Scenarios T1, T8 assert exact string `MADO_VERIFY: CLEAN`. Exits 2. |
| **D2** | **Clause B**: UNKNOWN guard dropped | `if [ "$FAIL" = 0 ] && [ "$UNKNOWN" = 0 ]; then` | `if [ "$FAIL" = 0 ]; then` | `verify()` (`:3340`) | Scenario C (missing `hyprctl`), E (missing `tomllib`), T9 assert DIVERGED / exit 1 when UNKNOWN>0. With mutant, exit is 0 and verdict CLEAN. Exits 2. |
| **D3** | **Clause B**: Skipped live layer status | `row hypr-live live.plane SKIP "live layer skipped ($live_skipped_reason) — file plane only"` | `row hypr-live live.plane PASS "live layer skipped ($live_skipped_reason) — file plane only"` | `verify()` (`:2436`) | Scenario A asserts row `live.plane SKIP`. With PASS, row assertion fails. Exits 2. |
| **D4** | **Clause C**: DIVERGED exit map | `"$reason"\nexit 1` | `"$reason"\nexit 0` | End of script (`:3353-3354`) | Scenarios B, C, E, H, I assert exit 1 on DIVERGED. With exit 0, exits 2. |
| **D5** | **Clause C**: Failing selftest exit map | `  return 2` | `  return 1` | `selftest()` exit (`:1305`) | Scenario F runs child selftest in broken PATH, asserting exit 2. With exit 1, exits 2. |
| **D6** | **Clause D**: Local inventory declared set | `(hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)` | `(hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs)` | `verify()` (`:2394`) | Scenario B asserts `hypr.local.inventory FAIL`. Also N1/N3/N4 assert exact set. Exits 2. |
| **D7** | **Clause D**: Include-graph count tolerance | `if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then` | `if [ "${#got[@]}" -lt "${#EXPECT[@]}" ]; then` | `verify()` (`:2339`) | Scenario H appends undeclared extra source, asserting FAIL and DIVERGED. If count tolerates extra lines, it reads PASS. Exits 2. |
| **D8** | **Clause E**: Sha pin comparison | `if [ "$sha" = "4f52854a3c14" ]; then` | `if [ -n "$sha" ]; then` | `verify()` (`:2422`) | Scenario A asserts `hypr.file.sha_pin NOTE` containing `'drifted from round-1 pin 4f52854a3c14'`. If always matching, detail says "matches round-1 pin". Exits 2. |
| **D9** | **Clause E**: Read-only boundary proof | `if [ "$after" = "$before" ]; then` | `if [ -n "$after" ]; then` | `verify()` (`:2596`) | Scenario I modifies hash mid-run, asserting `boundary.readonly FAIL`. If mutant always evaluates true, it passes silently. Exits 2. |
| **R1** (10) | **Clause F**: Reader fallback | `row walker walker.config UNKNOWN "python3 tomllib unavailable — cannot parse TOML"` | `row walker walker.config PASS "python3 tomllib unavailable — cannot parse TOML"` | `verify()` (`:2499`) | Scenario E sandboxes python without `tomllib`, asserting `walker.config UNKNOWN`. With PASS, assertion fails. Exits 2. |

### Note on D6 Anchor Preservation in Round 13
In Round 13 (C2 exact-set census), `tools/mado-verify.sh` added `gkeep` to the local inventory. To prevent breaking the recorded D6 defect anchor:
```bash
  local -a LOCAL=(hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
  LOCAL+=(gkeep)
```
By keeping the original 12-element literal array unchanged and appending `gkeep` via `LOCAL+=(gkeep)`, the `@old` string for D6 remains unique in the file (occurs exactly once in code, and once in the heredoc which is excised in the derived target). If `LOCAL=(... gkeep ...)` were written directly into the array literal, the spec's `@old` string would fail to find a match (`old-string-count=0`), aborting the sweep with `APPLY FAIL`.

---

## 4. Read-Only Harness Path and Contract

- **Canonical Path**: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh`
- **Recorded Provenance Digest**: `b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb`
- **Current Disk Digest**: `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` (Provenance note: `HARNESS_SHA_RECORDED` is printed for provenance only; the harness is not gated by hash, the kill table is the check).

### Execution Contract:
1. **Target Immutability**:
   `mutate-and-run.sh` copies the target to `$WORKDIR/pristine.<ext>` and verifies SHA-256 before and after the suite runs. The target file itself is never modified.
2. **Suite Execution**:
   Each mutant is run with `--suite 'bash "$MUTANT" --selftest'`.
   - Control run runs `$PRISTINE --selftest`. Must exit `0` (`CONTROL: GREEN`).
   - Each mutant runs `$MUTANT --selftest`.
   - Verdict is `KILLED` if exit code is non-zero (typically exit `2` for failing selftest assertions, exit `1` for general errors).
   - Verdict is `SURVIVED` if exit code is `0`.
   - Verdict is `INCONCLUSIVE` if exit is 124 (timeout) or 126/127 (exec failure).
3. **Restoration Verification**:
   The harness outputs:
   `MUTATE_RESTORE: OK (target-sha256 before=... after=...)`
   If the target hash changed, it outputs `MUTATE_RESTORE: DRIFT` and exits 1.

---

## 5. Recut Workflow

When `tools/mado-verify.sh --regression` detects that the derived target hash does not match `PIN_MADO`, it performs the following fail-closed protocol:

```
REGRESSION_TARGET: /tmp/mado-verify-regression.XXXXXX/target.mado-verify.sh sha256=<NEW_DERIVED_SHA> (recorded pin <OLD_PIN_MADO>; match=no)
REGRESSION_RECUT: bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh --target /tmp/mado-verify-regression.XXXXXX/target.mado-verify.sh --defects /tmp/mado-verify-regression.XXXXXX/mado-verify.defects.spec --suite 'bash "$MUTANT" --selftest' --workdir /tmp/mado-verify-regression.XXXXXX/recut --label mado-verify.sh
MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)
REGRESSION_WORKDIR: /tmp/mado-verify-regression.XXXXXX (kept)
exit=2
```

### Exact Step-by-Step Recut Procedure:
1. **Execute Gate in Regression Mode**:
   Run `bash tools/mado-verify.sh --regression`.
2. **Observe SETUP Refusal**:
   Confirm exit code is `2` and note the printed `<NEW_DERIVED_SHA>` and the `REGRESSION_RECUT` command line.
3. **Execute Mutation Sweep**:
   Run the exact `REGRESSION_RECUT` command printed in the output.
   - Verify that all 10 mutants report `APPLY OK`.
   - Verify `CONTROL: GREEN`.
   - Verify `DEFECT D1..D9, R1: KILLED` (10/10 KILLED, 0 SURVIVED, 0 INCONCLUSIVE).
   - Verify `MUTATE_RESTORE: OK`.
4. **Update `PIN_MADO`**:
   In `tools/mado-verify.sh`:
   Update line `PIN_MADO='...'` with the new `<NEW_DERIVED_SHA>`.
   If the table changed (it should not for ordinary widenings), update `TABLE_MADO`.
5. **Verify Clean Pass**:
   Run `bash tools/mado-verify.sh --regression`.
   Confirm output displays:
   `MADO_REGRESSION: PASS (case=mado-verify-hardened; target=<NEW_DERIVED_SHA>)`
   and returns exit code `0`.

---

## 6. Boundary Matrix: What Forces a New Target vs What Forces a New Spec

| Change Location / Description | Inside/Outside Excision Blocks | Modifies Derived Target? | Forces New `PIN_MADO`? | Forces New Spec (`SPEC_SHA`)? |
|---|---|---|---|---|
| **Editing `verify()`** (e.g. adding new checks, exact-set census) | Outside | Yes | **YES** | No (unless anchor strings changed) |
| **Editing `build_fixture()`** (e.g. adding `gkeep.conf` to fixture A) | Outside | Yes | **YES** | No |
| **Adding new selftest scenario** (e.g. scenarios N1–N4 for exact-set) | Outside (inside `selftest()` but outside R7-SELFTEST and R8-BLOCK) | Yes | **YES** | No |
| **Editing scenarios OM** (`MADO-R8-OMARCHY-BLOCK`) | Inside OM block, but OM block is **not** excised | Yes | **YES** | No |
| **Editing scenario R** (`MADO-R7-SELFTEST-BLOCK`) | Inside excised block | No | **NO** | No |
| **Editing scenario S** (`MADO-R8-BLOCK`) | Inside excised block | No | **NO** | No |
| **Editing `--snapshot` / `--snapshot-diff` code** (`MADO-R8-BLOCK`) | Inside excised block | No | **NO** | No |
| **Editing `--regression` engine** (`MADO-R7-REGRESSION-BLOCK`) | Inside excised block | No | **NO** | No |
| **Modifying defect description or replacement string in heredoc** | Inside excised block (inside `mado_r7_spec_write`) | No | No | **YES** (spec bytes & `SPEC_SHA` change) |
| **Adding an 11th defect (e.g. theme-plane clause)** | Inside excised block | No | No | **YES** (spec bytes, `SPEC_SHA`, and `TABLE_MADO` change) |
| **Renaming a variable in `verify()` that matches a defect `@old`** | Outside | Yes | **YES** | **YES** (must update `@old` anchor in spec heredoc to match new code, else sweep fails SETUP) |

---

## 7. Operational Recommendations for L1 / Integrator

1. **Custody & Verification**:
   - `PIN_MADO` updates must be measured, never pre-calculated or faked (`gate-standing-use.md` §5 rule 4).
   - In Round 13 w1, `GateImplement` modified `EXPECT` comments, added scenarios N1–N4, updated `hypr.local.inventory` exact-set logic, and appended `gkeep` to `LOCAL`.
   - Because these edits reside outside the excised blocks, `PIN_MADO` moved.
   - When L1 runs the recut, L1 must execute `mutate-and-run.sh`, confirm `10/10 KILLED`, update `PIN_MADO`, and verify that `tools/mado-verify.sh --regression` terminates with exit code 0 (`PASS`).
2. **Read-Only Preservation**:
   - No subagent should attempt to edit `tameshi-shokunin/tools/mutate-and-run.sh`.
   - The harness is an external authority consumed read-only.
