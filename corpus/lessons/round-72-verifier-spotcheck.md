# mado round 72 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04 (UTC), America/Sao_Paulo round window
role: closure judge for mado lane-round 72. I authored none of this round's work: not the
instruments, controls, knowledge entries, lesson, SCORECARD/LOG entries, prompt, or report.

Inputs: report `.ufo/reports/round-72/mado.md` (fleet `61009cc5fb5271532c81d86fec27cd69880da5b6`,
`mado-shokunin <mado@shokunin.local>`); dispatch prompt `.ufo/prompts/mado-round-72.md`
(`62e030fe2fdd9c5e392f53997d576c165b289dd9`); lane base
`976684a27e99c2508037a60eec415f550f53d70e`; lane tip `3894451f71c76d202fe03ead9e05a8c467a3b98d`.
Dispatch digest (`.ufo/watchdog.log`, lines 2221/2224 at read time):
`2026-11-04T01:30:49-03:00 launch mado round=72 pgid=2101027 driver=hyaku-inline attempt=1` /
`2026-11-04T01:47:17-03:00 complete mado round=72; hyaku-inline attempt=1`.

## Conformance (PROTOCOL §Round-robin step 1)

- **Report path and attribution.** `.ufo/reports/round-72/mado.md` exists at the contract path
  and its fleet commit is authored by `mado-shokunin <mado@shokunin.local>` (`git log --format
  '%an %ae %H' -1 -- .ufo/reports/round-72/mado.md` → `mado-shokunin mado@shokunin.local
  61009cc5…`). Report committer time 01:46:53 -03:00 is after the lane tip commit 01:46:09
  -03:00: report lands last. Pushed: `61009cc5` is an ancestor of `origin/master`
  (fleet HEAD = origin/master = `2e6132994825f7e6465dab4dbeca734c580b6748`).
- **SHONEN heading.** `grep -c '^## SHONEN'` → `1`; the section carries 4 box lines
  (`[~]`/`[ ]`), matching the 4 boxes in `SHONEN.md`; no `[x]`. All four are `[~]` with
  resolvable pointers.
- **Cited lane commits.** 9/9 exist and are ancestors of `refs/heads/master` (`git cat-file -e`
  + `git merge-base --is-ancestor` for `5601e526`, `9bcb4fd5`, `fd9ea03b`, `925a3e8a`, `200c1652`,
  `10730ee8`, `4f598cfd`, `18db46bd`, `3894451f`).
- **Lane cleanliness and push.** `jj-lane.sh state` → `branch=master
  local=3894451f… remote=3894451f… ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` prints nothing. `git ls-remote origin refs/heads/master` →
  `3894451f71c76d202fe03ead9e05a8c467a3b98d`.
- **Prompt contract.** `.ufo/prompts/mado-round-72.md` §§1–5 differ from the rendered
  `templates/round-prompt.md` only by the repository path and the lane-axes substitution
  (11 diff lines, both intended); all five child-lane items and the round-level items are
  present; §6 is the run-15 hyaku addendum. One stale sentence, status-neutral: the addendum's
  "ONLY reviewer uses @m_zfl; every other role uses @m_flash" does not match the live
  `task.agentModelOverrides` (executor, critic, connector, sentinel, scribe, mutation-tester are
  `@m_zfl`). The prompt itself names that config file as the authority and forbids passing a
  model, so no seat-route effect is shown; recorded for the operator's prompt-template pass.
- **Wave.** One v1 wave, 13 seats: executor 3, scribe 3, scout 2, reviewer 2, critic 1,
  mutation-tester 1, connector 1; attack 4/13 = 30.8 %; band 8–16. `w1-results.json` carries 13
  entries with non-empty `output`; every seat deliverable resolves on disk except one report-table
  path typo (routed defect 2). No seat died.
- **Fleet-root sweep.** The fleet repo's uncommitted files are `.scratch/*` (orchestrator-owned)
  and the untracked `.ufo/reports/round-70/kaidoku.md`; the fleet-root `after` file is dated
  2026-11-03 20:05, before this launch, and names no mado content. No mado round-72 misroot.
- **Marker predicate.** The report names real committed work, an evidence pointer per work item,
  a checkable commit citation, and all required sections — a report, not a marker: status `ok`.

## Claim re-checks (re-measured, not inherited)

Both claims were re-derived at the lane tip `3894451f…` with the committed counters, from the
lane root, scratch under `/fast/scratch/hyaku/mado-r72-closure` (not `/tmp`). The frozen control
sets hash to their declared digests (`sha256sum`): c1-modes `18144745d65a00e1d812c663dbace402a5714fde74506f54d9adabe858268c13`,
c2-controls `640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793`.

**C1 — calibration: the kill credit requires the run's own failure detail.**

```sh
python3 -I quality/counters/c1-r72-summary-credit.py --repo . \
  --rev 3894451f71c76d202fe03ead9e05a8c467a3b98d \
  --base-rev 976684a27e99c2508037a60eec415f550f53d70e \
  --scratch-root /fast/scratch/hyaku/mado-r72-closure
```

Observed last line, rc 0:
`MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=3894451f71c76d202fe03ead9e05a8c467a3b98d`.
Base leg misses exactly `bare-failing` and `mismatch-detail`; the other six agree. Read at the
tip, `credit(out)` implements the frozen sentence literally: `last_parsed_summary()` scans
backward for a full `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` match,
`total > 0` and `passed < total` are required, and `count_fails(out) == total - passed` with
`count_fails` matching only `^SELFTEST FAIL [0-9]+: `. Freeze precedes the instrument
(`5601e526` 01:35:16 < `9bcb4fd5` 01:37:29), so the do-nothing leg is genuinely pre-freeze.
**Verdict: improved** (8/8 vs 6/8 on the frozen eight-mode set).

**C2 — operability: the outcome verdict reads the summary, not the exit status.**

```sh
python3 -I quality/counters/c2-r72-outcome.py --repo . \
  --rev 3894451f71c76d202fe03ead9e05a8c467a3b98d \
  --base-rev 976684a27e99c2508037a60eec415f550f53d70e \
  --controls .ufo/waves/round-72/controls/c2-controls-r72.json \
  --scratch-root /fast/scratch/hyaku/mado-r72-closure
```

Observed last line, rc 0:
`MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=3894451f71c76d202fe03ead9e05a8c467a3b98d`.
The held leg is wrong on `failing-summary-exit0`, `green-summary-exit2`, `no-summary-exit0`,
`garbled-summary-exit0` — both directions, as declared. `summary_green()`/`outcome_verdict()`
require a last fully parsed summary with `n > 0` and `p == n` plus `killed == 2`, with the
status never read. **Verdict: improved** (8/8 vs 4/8 on the frozen eight-case set).

Supporting legs (evidence-verified from committed receipts, not executed): gate
`MADO_SELFTEST: 460/460` at the tip; axis `checked=3 mismatched=0` after the 10730ee8 re-run;
the frozen r71 instrument blobs identical base→tip. Independently re-derived by me with plain
commands, not the lane's gates: README index 85→87 with 0 missing/dangling/duplicate (regex
`^\| \`knowledge/([^`]+\.md)\`` over `git show <rev>:corpus/README.md` versus `git ls-tree`
knowledge files); ledger 125 data rows (126 `^| \`` lines minus the template row at :12);
census rows 380→383 and `scripts/sources-census.sh validate --root … mado` exit 0 at the tip.

## Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | improved | C1 re-measured 8/8 vs held 6/8 at the tip (rc 0), frozen controls, pre-freeze do-nothing baseline; SCORECARD round-72 row carries the command and the measured commit |
| operability | improved | C2 re-measured 8/8 vs held 4/8 at the tip; ledger 122→125 with `uncovered=0`; gate 460/460 unchanged |
| coverage | unchanged | index 85→87 is navigation completeness on a finite denominator; no new desktop/compositor surface, and the round itself claims none |
| depth | unchanged | no scored depth row moved; the two entries refine the lane's own instruments, not a new domain surface |
| freshness | unchanged | no freshness row re-scored; the r71 four defects are repaired, not re-dated across the province |
| adjacency | unchanged | PROVINCE round-72 refinement keeps the same boundary; no sibling/config/compositor surface touched |

No axis is harmed: the SCORECARD diff base→tip is append-only (62 added lines, no rewritten
scoring row), every previously published finite sub-axis stays at its measured value, and both
claim legs improve.

## Discernment spot-check (LEARNING.md — checked from outside)

Re-opened every row below on 2026-11-04 (my own fetch, not the lane's receipts); digests are my
own `sha256sum` of the fetched bytes.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S444 `unittest.rst` admit | ADMIT | `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/unittest.rst`, sha256 `d6522f68…ae5b86`, 107,372 B; quote at :2129-2130, 14 words | **agree** | Quote resolves at the cited location; `TestResult.wasSuccessful()` is the documented pass/fail read, which is exactly the ground C2 needs (status derived, not authoritative). Tier A/docs fits. |
| S445 `Lib/unittest/main.py` admit | ADMIT | `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/unittest/main.py`, sha256 `12de7da0…61d2`, 11,660 B; `if not self.result.wasSuccessful(): sys.exit(1)` at :272-273, 9 words | **agree** | Quote resolves inside `if self.exit:`; source code is primary for the runner's exit derivation (C2's "status is a projection"). Tier A/code fits. |
| S446 `Doc/builtins/stdtypes.rst` reject | REJECT | `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst`, sha256 `5a6951b7…e8e1`, 248,201 B; the old `Doc/library/stdtypes.rst` returns HTTP 404 | **agree** | It documents mapping-method argument behaviour, not call-site/result-object semantics; no admitted entry cites it; reason and flip are in the row. Defect: the Gate block/row carries no ≤25-word located quote for this new row (CORPUS rule 1) — routed, not a decision disagreement. |
| New-row quote limits | check | S444 row teaches-quote 14 words; S445 9 words (whitespace split) | **agree** | Both are inside the ≤25-word contract; S446 has no quote (defect above). |
| Three-fetch identity | check | Repo receipts `fetch/Doc_library_unittest.rst.{1,2,3}`, `Lib_unittest_main.py.{1,2,3}`, `Doc_builtins_stdtypes.rst.{1,2,3}` | **agree** | Each triplet is byte-identical by `sha256sum` and matches my independent fetch digest. |

## Trend verdicts

- **expansion: improved.** Two admitted knowledge entries, README index 85→87 (my re-derivation:
  85/85 at base, 87/87 at tip, 0 missing/dangling/duplicate), each `source:` citing a `mined`
  row (`summary-credit-own-detail-r72.md` → S442; `outcome-verdict-gate-summary-r72.md` →
  S444/S445), plus the round-72 Frontier bullet. The coverage map held no entry for the
  summary-authenticity credit or the summary-driven outcome verdict before this round. Caveat
  kept from r71: the ground is the lane's own instrument lineage, not a desktop surface; the
  LEARNING test is ground the map did not hold, which is met.
- **quality: improved.** The r71 rules are superseded by stronger successors — C1 adds the
  own-detail arithmetic (8/8 vs 6/8) and C2 moves the verdict off the exit status (8/8 vs 4/8) —
  each with a frozen control set, a pre-freeze do-nothing leg, and a review-driven repair
  (`4f598cfd`) whose frozen sets I re-ran and found identical. No admitted entry failed my
  re-check. Defects routed below are documentation/registry drift (stale selftest tallies, one
  wrong report path, one missing reject quote), not false rules.
- **discernment: improved.** My outside spot-check agrees on 2/2 admits and 1/1 reject; the
  reject is curated as a `rejected` row with reason and flip (the r71 routed defect), and
  QUALITY 116–117 entered with "shown able to fail" evidence. The wave's attack seats changed
  the shipped instrument (F1/F2 repair + erratum), and the mutation survivors M3/M5 are
  disclosed as gaps rather than reclassified.

## Routed defects for round 73

1. **Stale selftest tallies after the `4f598cfd` repair (correction sweep).**
   `quality/tool-ledger.md:161,163` and `SKILL.md:731` and
   `corpus/knowledge/outcome-verdict-gate-summary-r72.md` §5 still state the pre-repair
   `83/83` (harness) and `24/24` (C2 counter); the erratum and report state `87/87` and `25/25`
   after the repair. Registry/ledger rows must not pin a tally their own `--selftest` cannot
   print. Update the rows (or annotate the revision) in the next round; the entries' rules
   themselves are not false.
2. **Report evidence-path typo.** The wave table names `w1/R72ExecBattery.md`; the committed
   deliverable is `w1/R72ExecBattery/R72ExecBattery.md` (verified at the tip). The report's
   "each named file exists" claim is contradicted by its own pointer. Correct in the next
   report/erratum, never by rewriting the filed bytes.
3. **S446 Gate quote.** The new `rejected` row has no ≤25-word located quote in
   `corpus/lessons/round-72.md` § Gate (CORPUS rule 1 requires one for every new row). Record
   the quote at the real 3.14 location on the row or in the next Gate block.
4. **r71 routed item 7 still open and unnamed.** The round-69 `check-deliverables.py` reds on
   r69 seat reports (r70 routing, carried by the r71 spot-check) are neither repaired nor named
   in the r72 report. Fix under a round-69 correction entry or state why it stays deferred.
5. **Census warning characterization.** The report says "W04 warnings are the held
   superseding-URL family only"; the census also prints one held `W01` line (S277). No new
   warning was introduced base→tip (39 W0 lines both sides), but the "only" is inaccurate.
   Correct in the next round's errata.
6. **Operator prompt note (not lane debt).** The run-15 addendum's routing sentence is stale
   against the live `task.agentModelOverrides`; the prompt's own "config is authority" rule
   keeps it harmless, but the template/addendum text should be refreshed operator-side.

## SHONEN note for the operator

All four boxes stand at `[~]` with resolvable pointers and the round wrote no `[x]`. Box 1's
pointer is this round's Gate registry rows plus the existing SKILL decision tables; Box 2's
pointer is instrument work, not a fresh desktop end-to-end task (the live desktop plane has been
absent since r57); Box 3's counting commands run as written; Box 4's PROVINCE refinement touches
no sibling/config/compositor surface. A non-author promotion reviewer can check these against
the record; promotion is operator-owned and this closure writes no `[x]` and promotes nothing.
