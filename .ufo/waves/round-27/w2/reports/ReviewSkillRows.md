# Review: draft gate-registry rows vs actual files — `.ufo/waves/round-27/drafts/skill-registry.md`

Reviewer: `MadoR27.ReviewSkillRows` (UFO-FSD review) · round 27 wave w2 · 2026-10-23 · read-only
Reference: registration.md (PRED-C1-r27-v4, PRED-C2-r27-v2, data rule, host safety); SKILL.md Gate registry (`:593-630`, header at `:600`, table copied by the draft).

## Method

- Read the draft in full (raw), all 7 table rows (3 × round-26 implemented, 3 × round-27 marked pending).
- Compared the draft header verbatim against SKILL.md `:600` (`| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |`) — exact copy; the second SKILL.md registry (kind column, `:1976`) is not the copied one.
- Checked existence + sha256 of every implemented gate, pinned subject, evidence receipt and referenced report.
- Read each implemented gate's argparse surface and exit-return paths; confirmed evidence receipts' recorded verdicts.
- Fresh live verification (no Hyprland started, no lane writes): `--help` on all four gate scripts (rc 0); `check-population.py` green/red/unreadable runs (rc 0/1/2); full offline `counter-selftest.py` run (rc 0, SELFTEST pass=9 total=9). Hyprland coredump count (1338) untouched by this session.

## Row-by-row verdicts

| row | verdict | evidence |
|---|---|---|
| mado-r26-counter-selftest | accurate | entry command == `--help`; exit map 0-only-when-all-checks, 1 otherwise (argparse usage exits 2 → nonzero, not a pass); no `--selftest` flag; pins `f98e264b…d352cd` / `b92c32da…a716a8` == actual sha256 of `.ufo/waves/round-26/c1/count.py` / `c2/count.py`; `counter-selftest-green.txt` 9/9 exit 0, selftest sha `0754f501…` == current bytes; `-red.txt` exists (5 mutant sections); scratch default `/fast/scratch/hyaku/mado-r26` + cleanup-without-`--keep` in code; fresh rerun reproduced `SELFTEST pass=9 total=9 / exit=0`. |
| mado-r26-population | accurate | entry command matches; verdict map 0 PASS / 1 FAIL / 2 UNREADABLE matches code (`check-population.py:162-171`) and was reproduced live (rc 0/1/2); implementation sha256 `803e0096…` matches; no built-in self-test flag; `q37-population-red-green.txt` records the full matrix incl. exit lines. |
| mado-r26-control-receipts | accurate | CLI == `--help` (`--round, --data-registry, --repo, --tip, --shapes, --any-md, --counter-sha`); verdict map matches code: strict `first_commit < createdAt`, missing shapes → FAIL; 0/1/2; self-test runner `q36-fixtures/run_fixtures.py --out …` exists; `q36-mutants.txt` records `Q36MUTANTS killed=8/8 fixtures=10`, `Q36FIXTURES verdict=PASS`, and checker sha `351127bd…` == current bytes. |
| mado-r27-counter-selftest | status correct; two citations stale | `quality/counter-selftest.py` still absent (confirmed) — “not present” stays true; entry command exactly matches suite-A spec in both `c2/count.py` and `c2/count-v2.py`; **corrections**: contract is now `PRED-C2-r27-v2` (not `-r27`) and the tester is `c2/count-v2.py` (v1 `count.py` retired before data). Also “M26-8” motivating evidence exists (`w2/reports/MutSelftest.md`). |
| mado-r27-population-suite | status correct; one citation stale | `quality/population-suite.py` absent (confirmed); entry command exactly matches suite-B spec; **correction**: cite `c2/count-v2.py` and `PRED-C2-r27-v2` as contract source. |
| mado-r27-control-receipts | **outdated — implemented and landed** | `quality/check-control-receipts.py` exists (sha256 `2233db1d…`); provisional CLI flags `--seeds N` + `--receipt-glob PATTERN` match the landed argparse exactly (plus inherited `--any-md`, `--counter-sha`); `DEFAULT_GLOBS = ("*.md", "*.txt")` confirms the M26-8 `.md`-only omission is fixed; verdict map inherited 0/1/2 confirmed in code; red/green fixture receipt now exists at `.ufo/waves/round-27/quality/q36-successor-receipts.txt` (generated 2026-10-23T10:39:33Z; `Q36SUCCESSOR verdict=PASS`, `QS36SEEDS lane_runs=5 fixtures=24 mutants_killed=9/9`, successor sha `2233db1d…` == current bytes). Row should flip from pending to landed; “Confirm exact flags/defaults against the landed CLI” is done and matches. |

## Corrections list (consolidated)

1. **r27 counter-selftest row**: replace contract citations `PRED-C2-r27` → `PRED-C2-r27-v2` and `c2/count.py` → `c2/count-v2.py` (v1 retired before data; both files exist, v2 is the active counter, sha `4dfb34b5…`).
2. **r27 population-suite row**: same contract citation update (`c2/count-v2.py`, `PRED-C2-r27-v2`).
3. **r27 control-receipts row**: mark landed; CLI confirms provisional (no change needed to flags); add pinned-value/evidence pointer to `quality/check-control-receipts.py` and `.ufo/waves/round-27/quality/q36-successor-receipts.txt`; keep note that the fixture runner lives in scratch (`/fast/scratch/hyaku/mado-r27/q36/run_fixtures.py`, sha `f32ea076…`), not in the lane.
4. **r27 suite rows' “no R27 execution receipt claimed”** stays true for suites A/B (none exist yet); the control-receipts row now *does* have an execution receipt, so that phrase must not carry over to it.
5. Cosmetic: `q36-mutants.txt` ends at `Q36FIXTURES verdict=PASS` without a literal `exit=0` token; rc 0 is inferred from the verdict (no code discrepancy).
6. SKILL.md still contains no rows for any of the six gates — consistent with the draft's “for later incorporation” status; nothing in SKILL.md contradicts the draft.

## Residual risk / verification gaps

- The two r27 suites are not yet committed (ExecSuiteA*/ExecSuiteB* are building them this wave), so their rows could only be checked against the contract citations, not execution. Their “pending” markers remain correct.
- I did not rerun `run_fixtures.py` (it regenerates scratch fixture repos under `/fast/scratch/hyaku/mado-r26/q36`; recorded receipts already byte-consistent with current sources via sha256). The 8/8 and 9/9 kill records are therefore verified from the committed receipts + code, not a fresh run.
- No Hyprland was started; coredump count unchanged (1338 before/after this review).
- No lane files were modified; only this report was written under `.ufo/waves/round-27/w2/reports/`.
