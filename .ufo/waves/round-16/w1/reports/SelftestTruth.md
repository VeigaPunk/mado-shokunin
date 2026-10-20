# SelftestTruth — self-invocation vs helper-only review (Mado round 16, w1)

Seat: `MadoR16.SelftestTruth` (reviewer, leaf). Lane: `mado-shokunin`, baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Scope: `tools/mado-verify.sh` selftest assertions (`selftest()`, `:393-1542`), regression mode (`:1543-1983`), the snapshot block (`:1984-2157`), the tameshi harness contract it relies on (`tameshi-shokunin/tools/mutate-and-run.sh`, read-only), and `PROTOCOL.md:385-389`.

Method: source reading only. Nothing executed: no selftest, no `--regression`, no sweep, no installs, no package operations. Line anchors are from the lane file as read. `[OBS]` = read in source; `[INFERENCE]` = derived from source, not run.

## Verdict

- **Self-invocation (PROTOCOL §Gate standard, "Self-test"): met for the verify path.** `selftest()` contains 66 `"$BASH_BIN" "$0"` sites; every verify-path, census, theme, omarchy, usage and snapshot-diff scenario runs the gate as a child. The mutant copy run by the harness (`bash "$MUTANT" --selftest`, `mutate-and-run.sh:394`) therefore exercises the mutant's own code through `$0`. `[OBS]`
- **Code+finding pairing (same clause: "asserting both the exit code and a stable expected finding-id"): met for most scenarios, not all.** Gaps are OM4–OM8 (no exit code), several usage scenarios (exit code only), and OM1/OM3 exit attribution (confounded by a live-plane UNKNOWN). `[OBS]`
- **Helper-only pitfall: present in three places.** (a) R1–R11 test `regression_case` / pin helpers directly against a stub runner that ignores `--suite`; (b) the assertion helpers `st_*` have no negative controls and no mutant in the spec; (c) the regression and snapshot engines are excised from the sweep target, so their assertions are never mutation-tested.
- **Latent tautological-kill path** in the R10 `DEFECT_ID` branch. Not reached by the recorded sweep. `[OBS]` + `[INFERENCE]`.

Axes reviewed: (1) reach of each assertion through `$0`; (2) exit-code + finding-id pairing; (3) kill attribution (what makes a mutant KILLED); (4) branch coverage of the regression path.

## Findings (severity order)

### F1 — Medium — The assertion layer is outside the kill claim and has no negative controls

- `st_*` helpers are defined inside `selftest()` at `:400-438` (`st_eq`, `st_has`, `st_not_has`, `st_rows`, `st_row_has`, `st_row_detail`, `st_row_exact`, `st_counts_agree`). They are not in any excised marker family, so they are part of the derived target the sweep mutates (excision: `:1729-1731`).
- None of the spec defects (`D1-D9`, `R1`, spec `:1679-1717`) touches an `st_*` helper.
- The only scenario that drives a failure through the helpers is **F** (`:1026-1042`): a nested child with no `sha256sum` on PATH. F asserts only child exit `2` and the `FAILED` token. It does not show that any particular helper's bad branch counts a failure.
- `[INFERENCE]` A mutant such as `st_has() { st_ok; }` or `st_row_has() { st_ok; }` leaves every pristine assertion true, so the mutant suite stays green. It would be SURVIVED unless F's no-sha child happens to fail through the mutated helper. The 10/10 headline therefore does not measure whether the assertion layer can fail.
- **Fix (owner: gate lane):** add a negative control per helper (a known-wrong input, assert the failure counter moved, e.g. via a nested child with a counter read-back), and add `st_*` mutants to the spec with predictions before the sweep.

### F2 — Medium — Regression tests are helper-only over a stub that never self-invokes; the engine is unmeasured

- **R1–R9** (`:494-578`) and **R10–R11** (`:582-596`) call `regression_case` and `mado_r7_*` helpers directly. They never run `run_regression` or the real harness.
- The stub runner (`:451-479`) discards the `--suite` value at `:458` (`--label | --target | --defects | --suite) shift`). The suite string `RSUITE='bash "$MUTANT" --selftest'` (`:486`) is therefore never executed or checked by selftest. The one thing the requirement cares about, that the suite self-invokes the mutant, is untested in-suite and is only exercised by a live `--regression` run.
- Stub-reachable branches only. The stub always writes `results.tsv` (`:468`) and exits only via `STUB_EXIT` set to `0` or `1` (`:488`, `:568`). Consequently these `regression_case` branches have no test: sweep `rc=2` refused (`:1764-1767`), other `rc` (`:1768-1772`), no results table (`:1774-1777`), no `MUTATE:` line (`:1763`).
- `run_regression` branches with no test: tool missing (`:1847-1852`), embedded spec sha mismatch (`:1874-1879`), target-build failure (`:1882-1887`), the PASS/FAIL/SETUP mapping of the rc (`:1915-1936`). Only the missing-harness SETUP is self-invoked (R13, `:614-618`).
- The whole R block (`:440-619`), the regression engine (`:1543-1983`) and the snapshot block (`:1368-1531` and `:1984-2157`) are excised from the derived sweep target (`:1729-1731`), and the sweep mutates that derived target (`:1882-1902`). Their assertions are never mutation-tested. The gate's own lessons already state this (`corpus/lessons/round-14.md:174-175`, "excised regression/snapshot machinery is outside those mutant claims"), but the R1–R9 labels read as coverage.
- **Fix:** make the stub assert its `--suite` argument equals `bash "$MUTANT" --selftest` (or run `bash -c "$suite"` with `MUTANT` pointing at a self-invoking fixture); add stub modes for `STUB_EXIT=2` and a missing `results.tsv`; add `run_regression` self-invoked cases for spec mismatch and target-build failure; record in the gate note which code is excised from mutation.

### F3 — Medium-Low — OM block: exit codes unasserted in OM4–OM8; OM1/OM3 exit attribution is confounded

- `om_rc` is captured at `:749`, `:766`, `:777`, `:785`, `:794` but never asserted in OM4–OM8. Only OM1–OM3 assert it (`:687`, `:715`, `:738`). OM4–OM8 assert finding rows only, which breaks the "code and finding" clause.
- OM1 (`:684-711`) and OM3 (`:730-745`) run with `MADO_VERIFY_LIVE=yes` and `PATH="$OMB"`. The `OMB` symlink set (`:677-680`) contains no `hyprctl`. `live_plane()` (`:2968-2981`) then emits `live.plane UNKNOWN` ("hyprctl not on PATH; … verdict cannot be CLEAN"), which by itself makes the verdict non-CLEAN and the exit `1`.
- So the assertion at `:687`, labelled "exit 1 — only the un-reproducible sha row can be red", cannot distinguish the omarchy sha row from the live UNKNOWN. The row assertions (`:700-708`) still pin the sha FAIL, so kill power is preserved; the code assertion's label is false. Same for OM3's "two omarchy FAILs" exit.
- OM2 (`--no-live`, `:713-728`) is clean: live rows are SKIP, not UNKNOWN.
- **Fix:** assert `live.plane UNKNOWN` explicitly in OM1/OM3 (or run them with a `hyprctl` stub that reports absence without UNKNOWN semantics, whichever is intended), relabel the `:687` assertion, and assert the exit code in OM4–OM8.

### F4 — Low (latent) — R10 `DEFECT_ID` branch can record a tautological KILLED

- R10 (`:577-590`) runs `mado_r7_target_build "$0"` and, when `DEFECT_ID` is set and not `CONTROL`, requires `dsha != PIN_MADO`, else `st_bad`. The harness exports `DEFECT_ID` for every mutant run (`mutate-and-run.sh:394`, documented `:56`).
- For a mutation located inside the excised marker blocks, `dsha == PIN_MADO` regardless of behaviour. `st_bad` then turns the suite red, and the harness records KILLED (`mutate-and-run.sh:483-489`: any exit other than 0/124/126/127 is KILLED). No behavioural assertion has to fail.
- **Not reached by the recorded sweep.** R10 lives inside `R7-SELFTEST-BLOCK` (`:440-619`), which is excised from the derived target. The sweep mutates the derived target (`:1882-1902`), so the branch is dead in the recorded configuration. `[INFERENCE]` It becomes live only if someone points the harness `--target` at the full gate.
- **Fix:** remove the branch, or make it unable to convert a survivor into a kill (e.g. report it as a separate attribution, not a suite failure), and say so in the header. This matches the gate's own rule that pin integrity is not behavioural coverage (`corpus/knowledge/gate-standing-use.md` §5 rule 2, and the round-12 entry `corpus/lessons/round-12.md:104`).

### F5 — Low — Usage scenarios assert exit code only (no stable finding-id)

- `D` bad arg (`:1007-1008`); `R12` `--regression --defects=x` and `--bogus` (`:602-607`); `S7` `--snapshot` with no file (`:1446-1447`) and `--bogus` (`:1451-1453`, the no-write check is present, the message is not); `S9` `--snapshot-diff` with no files, with one file, and with `--live` (`:1468-1473`).
- `PROTOCOL.md:385-389` asks for both exit code and a stable finding-id. The messages exist and are stable (`usage error: …` at `:1959`, `:1971`, `:2103`, and the main dispatch at `:3648`), so they can be asserted.
- **Fix:** add a `st_has` on the `usage error:` line to each of these.

### F6 — Low — Kill attribution is by exit code only

- `mutate-and-run.sh` marks any non-zero exit other than 124/126/127 as KILLED (`:483-489`). A mutant that breaks parsing (bash syntax error, exit 2) therefore counts as KILLED without any assertion or finding-id firing. `regression_case` (`:1801-1811`, `:1816-1828`) checks only the verdict column, not the cause.
- The recorded round-8 kills do name assertion labels (`corpus/knowledge/gate-mutation-sweep-r8.md:61-65`), but that is by inspection of the evidence, not enforced by the gate.
- **Fix (harness owner, recommendation only):** for KILLED, require the suite output to contain `MADO_SELFTEST: FAILED` (or the gate's equivalent finding line) and record the cause; otherwise report `KILLED-CRASH`.

### F7 — Info — Comment and numbering drift

- S10 header says "against a crafted pair (no child process)" (`:1482-1483`), but the test runs `"$BASH_BIN" "$0" --snapshot-diff` (`:1519`). The comment is wrong; the test is self-invoked.
- Scenario labels jump N4 → N7 (`:1152`, `:1159`); N5 and N6 do not exist. Confirm whether they were removed deliberately.
- R10/R11 assert constants (`PIN_MADO`, `SPEC_SHA`, `@defect` count) by helper, not by behaviour. Fine in a pristine run; they are not behavioural kills (see F4).

## Compliance matrix (selftest scenarios)

| Group | Lines | Self-invoked via `$0` | Exit code asserted | Finding-id asserted | Notes |
|---|---|---|---|---|---|
| A, B, C, E, H, I | `:940-1074` | yes | yes | yes | Clean pairing. |
| D (usage) | `:1003-1008` | yes | yes | partial | F5. |
| F (failing suite exit map) | `:1026-1042` | yes (nested) | yes | yes (`FAILED`) | Kills D5. |
| N1–N16 | `:1076-1367` | yes | yes | yes | Clean; N5/N6 absent (F7). |
| OM1–OM3 | `:684-745` | yes | yes | yes | F3 attribution. |
| OM4–OM8 | `:747-800` | yes | **no** | yes | F3. |
| T1–T9 | `:811-938` | yes | yes | yes | Clean. |
| S1–S6, S8, S10 | `:1377-1530` | yes | yes | yes | Clean; S10 comment (F7). |
| S7, S9 (usage) | `:1441-1480` | yes | yes | partial | F5. |
| R1–R9 | `:494-578` | **no** (helper + stub) | via helper rc | yes (helper output) | F2. |
| R10–R11 | `:582-596` | **no** (helper constants) | n/a | pin check only | F4 / F7. |
| R12–R13 | `:598-618` | yes | yes | yes | R13 is the only self-invoked regression SETUP. |

## Verified-OK items (source-read)

- Self-invocation is real: `$0` is the mutant path under `bash "$MUTANT" --selftest`; no scenario depends on the lane's original file path.
- F covers the exit-map flatten (`D5` class; `corpus/knowledge/gate-mutation-proof.md:113-117` records the exit-flatten residual honestly).
- Stub output shape matches the harness: `results.tsv` header (`:468` vs `mutate-and-run.sh:478`), control and restore line prefixes (`:466-467`).
- Every T and N scenario asserts both code and finding.

## Residual risk and verification gaps

- **Not executed (by assignment).** No selftest run, no `--regression`, no mutant sweep. Every `[INFERENCE]` above needs a run to confirm. Suggested checks for the main agent after integration (not run by this seat): `bash tools/mado-verify.sh --selftest`, `bash tools/mado-verify.sh --no-live`, and, if a gate edit lands, `bash tools/mado-verify.sh --regression` with the recut command it prints. A helper-mutant probe (F1) should be a separate spec, run once.
- **Known and accepted limits, restated so they are not lost:** excised R/S machinery is outside mutation claims (F2); the recorded 10/10 is measured on the derived target only.
- **Not reviewed:** the frozen verifier (`.ufo/waves/round-14/frozen/verify.py`) and its self-invocation (outside this seat's scope); `tameshi-shokunin` beyond the harness contract lines cited.

## Tooling

No installs, updates or package operations were performed by this seat. Pacman remains paused host-wide per the lane contract. No peer messages were sent. No files other than this report were written.
