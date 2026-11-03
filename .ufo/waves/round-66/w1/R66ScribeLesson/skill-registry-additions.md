# SKILL.md append — Gate registry rows (round 66)

Insertion: add the three rows below to the `## Gate registry` table (`SKILL.md` header at `:692`,
columns `name | gate/probe | entry command | verdict map | self-test command / spelling |
pinned-value path | write scope | owner`). L1 may instead append a dated `## Round 66` section with
these rows; the rows are not a promotion and do not edit the r65 counter bytes.

The r65 counters remain frozen and keep their own records. These rows register the round-66
successors and the hardened standing instrument only.

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-r66-register | gate | `python3 -I quality/counters/c1-r66-register.py --repo . --rev REV` | 0 `verdict=TARGET_MET` (genuine register accepted); 1 `TARGET_MISSED` (any of the three r65-accepted controls, or any clause miss; per-clause `C1_R66: detail=…` on stderr); 2 setup/usage | `python3 -I quality/counters/c1-r66-register.py --selftest` — hermetic string cases, no git and no fixtures; prints `MADO_R66_REGISTER_SELFTEST: PASS cases=N failed=M`; rc 0 only on `failed=0` | frozen predicate `.ufo/waves/round-66/claims-declaration-r66.md` §C1; exact live line `.ufo/waves/round-65/receipts/gate-live-r65.txt:65`; draft sha256 `4e1b94ff…` | reads git objects at the resolved `--rev` only (no worktree reads); writes nothing; strips inherited `GIT_*` | mado |
| mado-r66-landing-instrument | gate | `python3 -I quality/counters/c2-r66-landing-instrument.py --repo . --rev REV --scratch-root DIR` | 0 `TARGET_MET` only when the instrument selftest rc=0 and the landing run is GREEN with four genuine green markers and rc=0; 1 `TARGET_MISSED` (red legs, ERROR, or missing artifact); 2 unsafe setup/usage | the driver runs the instrument's hermetic `--selftest` (round-66 draft: 56/56 then 58/58 at this seat's reads, not final; re-pin at integration); the driver receipt names `selftest=<rc> landing=<rc> green=<yes/no> verdict=…` | frozen predicate `.ufo/waves/round-66/claims-declaration-r66.md` §C2; marker premise `.ufo/waves/round-66/marker-premise-erratum.md`; draft sha / integration path in `.ufo/waves/round-66/w1/R66ExecDriver/report.md` | pins `--rev` to a commit; extracts the instrument and three frozen dependencies at that rev into private scratch; passes `--round 66` and the repo-derived receipts path to the instrument internally (no such flags on the driver CLI); strips inherited `GIT_*` from git and leg children; refuses tmp-family and symlink-ancestor scratch; writes only under scratch | mado |
| mado-landing-counters (round-66 v2) | gate | `bash quality/landing-counters.sh --repo . --rev REV --round N --scratch-root DIR [--citecheck-paths PATH ...] [--selftest]` | 0 GREEN only when all four legs carry their green markers and rc=0; 1 RED only when at least one leg is a genuine rc=1 red with its red marker and no leg is ERROR; 2 ERROR on rc>=2, rc=0 with absent/inconsistent marker, missing used-by sibling, refused scratch, or usage (ERROR dominates RED) | `bash quality/landing-counters.sh --selftest --scratch-root DIR` — real child-execution witnesses per leg, skipped child, crash-vs-red, missing sibling, dirty decoy and selected rounds, explicit dirty paths, inherited Git steering, required `--round`/`--rev`, tmp-family and symlink-escape refusal; round-66 draft `56/56` then `58/58` at this seat's reads, not final | frozen predicate `.ufo/waves/round-66/claims-declaration-r66.md` §C2; actual child markers `indexed=A/B` (nav), `MADO_USED_BY:` (used-by), `LEDGER:` (ledger, not `MADO_TOOL_LEDGER`), `MADO_CITECHECK:` (citecheck); draft sha256 `1671cebc…` (earlier `f0c8d74f…`) | writes only under `--scratch-root`; `--round N` selects `.ufo/waves/round-N/receipts` and its dirty guard | mado |

Notes for the integrator:

1. The rows describe the candidate drafts in
   `.ufo/waves/round-66/w1/R66ExecRegister/`, `.ufo/waves/round-66/w1/R66ExecLanding/` and
   `.ufo/waves/round-66/w1/R66ExecDriver/`; the committed paths, hashes and measured results must be
   re-pinned at the integration revision before these rows are read as current.
2. No row claims a committed four-leg GREEN or a frozen-harness `4/4`; both were unobserved when the
   snippets were written.
3. `quality/landing-counters.sh` is an instrument under `quality/` and is outside
   `quality/check-tool-ledger.py`'s population (that checker counts `tools/**`, `quality/*.py` and
   `quality/counters/*.py`; `.sh` counts only under `tools/`). Its registration belongs in this
   table, not in `quality/tool-ledger.md`.
4. The frozen count harness's a-d `correct=4/4` is a diagnostic, not the whole C2 target: the target
   also requires the candidate selftest green and a real four-leg landing GREEN, and the current
   harness omits both (`.ufo/waves/round-66/w1/R66CriticLanding.md` F1). Do not register a count that
   prints `TARGET_MET` from the four cases alone.
