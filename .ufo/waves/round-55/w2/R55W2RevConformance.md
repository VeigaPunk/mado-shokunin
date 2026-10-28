# R55W2RevConformance — report (round 55, wave w2, falsify)

Scope: landing conformance pre-check of w1 against the claims-frozen "Mistake-fix item" contract, at scored rev `57584ed67716340b3d466fa04333ac0bab3fb79e`. Full write-up: `.ufo/waves/round-55/w2/R55W2RevConformance/conformance.md`. Receipts: `.ufo/waves/round-55/w2/R55W2RevConformance/receipts/`. Reproducer: `.ufo/waves/round-55/w2/R55W2RevConformance/trailer-check.py`.

## Ran
- `python3 -I quality/check-wave-done.py --repo <lane> --rev 57584ed6... --round 55` (rc=0) and at HEAD `721ba9c1` (rc=0). Both: `WAVE wave=w1 ... seats=40 dispatched=40 settled=40 verdict=OK`, `MADO_WAVE_DONE: round=55 waves=1 settled=1 verdict=OK`.
- `python3 -I quality/check-deliverables.py --repo <lane> --rev 57584ed6... --report <39 w1 .md at rev> --require-declaration` (rc=1): `CHECK101: reports=39 declared=31 exists=30 absent=1 undeclared=28 verdict=FAIL`.
- Per-seat trailer check (read-only `git cat-file`): `dispatched=40 results=40 trailer_reports_at_rev=38 missing=2`.
- `git status --porcelain` in the lane and fleet root; `--selftest` of the gate: 58/58.
- Read-only probe of `seat_state` by importing the gate module and calling it on the stub record.

## Findings
1. **BROKEN — 2 w1 seats with no sidecar and no documented absence at the rev:** `R55ScoutCallers`, `R55ScoutHyprlang`. Their recorded outputs are 123 and 298 chars of tool-plan narration. The "provider limit" documented absence exists only in `w2-dispatch.json` at HEAD, not at the scored rev. Cause UNVERIFIED from the artifacts.
2. **BROKEN — gate counts the stubs as settled:** `check-wave-done` reports `settled=40`, against a round account of 38 settled + 2 dead. `seat_state` returns `('settled','output')` for any non-empty string output with no `status`, which is how the stubs pass.
3. **BROKEN — name collision `R55RevC1Contract`:** two writers in `w1/R55RevC1Contract/`. The trailer-named `R55RevC1Contract.md` is the un-recorded writer's C1 attack. The recorded identity `R55RevC1Contract-2` (per `w1.ready.dispatched` line 2 and the results output) wrote `R55RevC1Contract-2.md`, which no trailer names.
4. **FAIL (tool) — `check-deliverables` on w1:** one ABSENT caused by an elided path (`.../w1/R55RevC1Contract-2.md`) in the -2 report, though the file exists at the rev; 28 reports carry no `Report:` trailer (it lives in the dispatch), so the tool cannot prove them.
5. **FINDING — w2 launched but uncommitted:** `w2.ready` and `w2.ready.dispatched` are untracked; the committed-bytes gate therefore reports round 55 as `verdict=OK` with `waves=1`. w2 is invisible to it.
6. **SURVIVES — w1 `results.json`:** present at the rev, `lane=mado round=55 wave=w1`, `seats=40 == len(results)`, no duplicate names.
7. **NOT-REPRODUCED — misrooted fleet-root seat files naming mado/r55:** none. Only ` A .scratch/closure-mado-r50.json` matches (mado, round 50). Not touched.
8. **Name collisions:** 11 seats renamed by the registry (`R55ScribeEntryB-2`, `R55ScribeP19a-3`, `R55ScribeP19b-3`, `R55ScribeIndex-2`, `R55ExecC1CounterA-3`, `R55ExecC1Harness-4`, `R55ExecC3CounterA-2`, `R55ExecTool1-2`, `R55ExecTool4-2`, `R55ScoutWayland-3`, `R55RevC1Contract-2`). Only the `R55RevC1Contract` pair is shown to share a directory; the other 10 are UNVERIFIED for a second writer.

## Not verified
- The provider-limit cause for the two stubs.
- Second writers in the other 10 renamed seat directories.
- w2 conformance (in progress; no w2 results exist).

## Lane hygiene
No tracked file was edited; no git mutation; no commit; no hyprctl; no pacman. Scratch was used under `/fast/scratch/hyaku/mado-r55/R55W2RevConformance/` and removed before yield. Tool installs: none.
