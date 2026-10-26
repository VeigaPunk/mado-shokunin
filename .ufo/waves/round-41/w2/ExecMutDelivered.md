# Seat ExecMutDelivered — report (wave 2, round 41)

Attacked: the delivered `tools/mado-globals.py` (DATA commit
`07f2641696b5ac73de1404ea737a9f27e9819aa1`, sha256
`286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e`, byte-identical to
`.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt`) — its **selftest** and the **v2
fixtures** of `quality/counters/c1-r41-globals-v2.py` (PRED-C1-r41-v2, 39 fixtures,
clauses a,b,b2,b3,g), with **64 new single-edit mutants** (scored 6-way parallel, nonce
`c1w2mut0001`, rev `07f2641…`).

## Outcome

| bucket | count | mutants |
|---|---|---|
| TARGET_MET survivors (fixtures=39/39, all clauses) | 33 | M100-M106 (regex/grammar value domains), M111, M112, M114, M116, M117, M125, M131, M132, M135, M137, M138-M143, M145, M146, M155-M159, M161-M163 |
| fixtures=39/39, clause-failed (TARGET_MISSED) | 3 | M113 (b2), M115 (b), M154 (b) |
| killed by ≥1 fixture | 28 | M107-M110, M118-M124, M126-M130, M133, M134, M136, M144, M147-M153, M160 |

**Every TARGET_MET survivor is either a missing fixture class with a verified kill
fixture, or an equivalent / selftest-integrity finding (proved).** No "no defect
found" is claimed for the predicate as a whole — it has 16 real blind spots; the
delivered tool itself is byte-identical to the frozen v2 reference and passes the
full predicate (baseline TARGET_MET), so this report's findings are about the
predicate's coverage, not about a defect in the delivered tool's current behavior.

## Findings (each names what it attacks)

1. **Value domains the 39-fixture lattice cannot see (12 classes)** — each proved by a
   kill fixture where the counter's own model diverges from the mutant
   (`logs/_killfix.log`, `KILLFIX fails=0`):
   - ver=0 adverts (`(ver 0)`) — every generator draws ver ≥ 1 (M100);
   - `+`-offset timestamps (all fixtures use `-03:00`) (M101);
   - years ≠ 2026 (M102);
   - host fields containing a space (grammar `\S+`, fixtures ASCII) (M103);
   - any third log level (`[WARNING]`, fixtures only `[LOG]`/`[ERR]`/`[log]`/`[Log]`) (M104);
   - 33-hex boot ids (all fixtures 32) (M105);
   - fractional seconds in the timestamp (M116);
   - interface names containing `.` (M117);
   - calendar-invalid month (13) (M135);
   - >128-char hosts (M145);
   - >7-digit pids (M146);
   - **empty added-side `--diff`** (M106) — convex: the *removed* side is pinned
     (M107 is killed by vernum0), the *added* side is not (every frozen diff adds
     names).
2. **Live size boundary**: a live program emitting exactly 8 MiB then EOF is not
   exercised (`livelarge0` emits 9 MiB), so `>` vs `>=` on the live total is
   indistinguishable (M111; reference NO_SESSIONS rc3 vs mutant
   journalctl_too_large rc5 on the exact-8-MiB stub).
3. **Selftest integrity is not load-bearing for the predicate**: 13 of the 63
   selftest probes can be deleted one at a time (M138-M142, M155-M159, M161-M163)
   and `return 0 if ok == n else 1` can be flatlined (M114) with the predicate
   still green — clause b checks only the tally (k==n≥50), never that a probe
   asserts anything. Only *tally-corrupting* edits are caught (M113/M115/M154).
4. **Equivalent survivors (proved, no defect)**: M112 (read chunk size), M125
   (unreachable `except SystemExit` branch), M131 (stderr pipe vs devnull), M132
   (dedup in `run()` is redundant with `report()`'s set()), M137 (LIVE_TIMEOUT
   reset after last use), M143 (selftest ts literal consumed only by a ±-agnostic
   regex). Each passes a 12-journal corpus equality run vs the reference plus
   identical selftest output.

## Evidence (all receipts under the seat dir)

- `gen_mutants.py` → `MUTANTS total=64 bad=0`; `mutants/*.py` (64, all parse).
- Novelty: zero (old,new) pair overlap with the 55 frozen control pairs
  (`ctl/run-c1-v2-controls.py`) and the 42 w1 `gen_mutants.py` pairs; all edits
  are outside the MutSelftestFixtures matrix operator set (regex/quantifier,
  exit-code, live-plumbing and probe-deletion edits).
- `logs/_baseline.log` — delivered tool: selftest 63/63, b2 sites=18 killed=6/6,
  `fixtures=39/39 verdict=TARGET_MET`.
- `logs/_summary.tsv`, `logs/<name>.log` — per-mutant scoring (above table; kill
  fixture names per mutant in `survivors.md`).
- `verify_kill_fixtures.py`, `logs/_killfix.log` — `KILLFIX fails=0`.
- `survivors.md` — full analysis (kill fixtures, equivalence proofs, contract
  sentences broken).

## Scope / safety

- Wrote only under `.ufo/waves/round-41/w2/ExecMutDelivered/` (+ the Report trailer
  at `.ufo/waves/round-41/w2/ExecMutDelivered.md`). No frozen file touched; the
  counters, controls, registrations, reference and fetch receipts are unchanged.
- No git/jj mutation (read-only `git show` only); no pacman (host-wide pause
  respected); no new tools installed (host python3 3.14.8); no compositor/Wayland/
  journal contact; leaf seat, no subagents/jobs, no labrat used.

## Check the L1 should run

- Confirm the 16 missing fixture classes (12 value-domain + live-exact-MAX +
  3 selftest-integrity groups) are worth closing in a v3; each non-equivalent
  survivor has an exact kill journal in `verify_kill_fixtures.py`.
- Decide whether the selftest's easy flatlining (M114, 13 deletable probes)
  warrants a counter clause (e.g. b4: verify a probe's assertion is non-trivial).
