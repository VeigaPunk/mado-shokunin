# mado round 66 — verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-03
round: mado r66 (lane counter 66)
base: eafd500fa7be76dca59e729435e231a5032cc037
lane head: ecfc8ac376ea3152d552496b75f5ae059571943f
report: `.ufo/reports/round-66/mado.md` @ 51432ad435cebf31ae1732b2993be877860f501b
dispatched prompt: `.ufo/prompts/mado-round-66.md`
scope: non-author verification only. No lane-authored file edited, no `[x]` written, no
promotion. The lane's gates and selftests were **not executed**; their committed evidence
was read and the claimed counts were re-derived from committed per-case receipts and
independent counts over committed bytes.

## Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report attribution | `git log --format='%an %H' -- .ufo/reports/round-66/mado.md` | `mado-shokunin mado@shokunin.local 51432ad435cebf31ae1732b2993be877860f501b` | pass |
| report lands last | lane tip vs report commit time | lane tip `ecfc8ac3` 20:37:37-03:00; report 21:09:15-03:00; watchdog `complete` 21:09:56 | pass |
| SHONEN contract | `grep -c '^## SHONEN'` / box lines | `1` heading; 4 `[~]` lines, one per `SHONEN.md` box, each with a pointer | pass |
| cited commits | `git cat-file -e` + `git merge-base --is-ancestor <h> refs/heads/master` | `ed980316`, `043b9af1`, `739a01c5`, `ecfc8ac3` all exist and are ancestors; `git log --oneline eafd500f..ecfc8ac3` = exactly those four | pass |
| lane state | `scripts/hyaku/jj-lane.sh state …/mado-shokunin` | `branch=master local=ecfc8ac3 remote=ecfc8ac3 ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| clean tree | `git -C …/mado-shokunin status --porcelain` | empty | pass |
| prompt fidelity | rendered template diff | prompt body lines 1–140 are a byte-identical rendering of `templates/round-prompt.md` (0 diff lines after `{{ROUND}}`/`{{LANE}}`/`{{FLEET_ROOT}}`/`{{AXES}}`/`<mado-repo>` substitution); §6 addendum follows | pass |
| prompt contract items | read through | mission/axes binding, 1–3 claims, frontier step, L2 floor ≥8 in one batched call, report path and filename, commit-before-report, `SHONEN` heading, commit-hash citation, write scope, commit-then-push, push scope, L0 side channel all present | pass |
| dispatch digest | `.ufo/watchdog.log` lines 2124/2146 | `2026-11-03T19:58:07-03:00 launch mado round=66 pgid=1140062 driver=hyaku-inline attempt=1` / `2026-11-03T21:09:56-03:00 complete mado round=66; hyaku-inline attempt=1` | pass |
| report pushed | `git ls-remote origin refs/heads/master` | local == remote == `beb6ffeb…`; report commit in history | pass |

Conformance defects (status-neutral; none bars admission):

1. **Frozen C2 predicate literal.** The declaration (`.ufo/waves/round-66/claims-declaration-r66.md`)
   names the ledger child marker `MADO_TOOL_LEDGER`; the actual child emits `LEDGER:`
   (`git show 739a01c5:quality/check-tool-ledger.py | grep -c MADO_TOOL_LEDGER` → `0`;
   `grep -n 'LEDGER:'` → lines 350/368/549). The implementation binds the actual marker and the
   erratum is committed (`marker-premise-erratum.md`, 043b9af1). The frozen predicate text was
   not amended; a declaration should quote the child output it intends to bind before freezing.
2. **Freeze/control order.** `process-defects.txt` discloses that the wave registry and ready
   file preceded the freeze commit `ed980316`, and that the executable do-nothing baseline was
   scored after the freeze. No chronology pass is claimed; the claim bytes are unchanged.
3. **Routing drift.** The prompt's run-15 map (scout `@m_antigravity`) is not reproduced by the
   operator config observed at report time (`reviewer`/`executor` `@m_zfl`, `critic`/`scout`
   `@m_flash`); no captured spawn/answering-model attestation was received. The lane passed no
   `model` parameter (`w1-spec.json`/`w1-dispatch.json` contain no model key), edited no config,
   and did not assert the mandated mix.
4. **No planner seat.** The 12-seat wave has no planner; the L1 holds that seat per the prompt's
   orchestrator ruling. Recorded, not a defect of the wave.
5. **Unattributed fleet-root file.** `after` (24 B, `== SCORECARD diff base-`) names no lane or
   round; left untouched per the misroot rule.

## Claims re-check

Both claims are bounded finite-control claims. The lane's harness (`check-controls.py`,
sha256 `2e34eab0…` at both `739a01c5` and `ecfc8ac3`) was **not executed**; each per-case
receipt is a committed file, and the correct counts were recomputed from the recorded rc
against the frozen expectations.

### C1 calibration — register structural discrimination

Declared: reject three r65-accepted forgeries (duplicate returned-host heading; a row without a
receipt; a file-plane-only receipt tree without the exact live receipt) and accept the genuine
register — target 4/4, base at most 1/4; selftest required; state-cell truth explicitly not
measured.

Commands and observed output:

```sh
cd mado-shokunin
git cat-file -e eafd500f:quality/counters/c1-r66-register.py   # absent at base
git cat-file -e 739a01c5:quality/counters/c1-r66-register.py   # present at measure (193 lines)
git diff --stat eafd500f ecfc8ac3 -- quality/counters/c1-r65-register.py   # empty (frozen)
git show 739a01c5:quality/counters/c1-r66-register.py | sha256sum
# 8ca15c66e953b093913559b7eda7f390c111a79062ef22f75caa498a4a04ec31
cd .ufo/waves/round-66/measurement-evidence/c1-after
for n in genuine duplicate-heading row-without-receipt file-plane-only; do
  echo "$n baseline=$(cat baseline-$n.rc) candidate=$(cat candidate-$n.rc)"; done
# genuine baseline=0 candidate=0
# duplicate-heading baseline=0 candidate=1
# row-without-receipt baseline=0 candidate=1
# file-plane-only baseline=0 candidate=1
tail -1 candidate-selftest.out   # MADO_R66_REGISTER_SELFTEST: PASS cases=15 failed=0 (rc 0)
```

Baseline correct = 1/4 (only the genuine fixture); candidate correct = 4/4. The predicate source
confirms the declared shape: `assess()` requires exactly one heading (`headings=2` is MISSED),
exactly eight group rows, a resolving receipt in each row's fourth cell, all named receipts
resolved at the revision, and the exact live `MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live
planes verified read-only)` line. Its `state-truth-not-measured` and `unreferenced-live-receipt`
selftest cases deliberately pass, matching the disclosed limit (an unreferenced live object or
forged state prose still satisfies the tree-level check).

Verdict: **improved**, bounded (1/4 → 4/4; 2.5/10 → 10/10 on the declared finite rubric). The
stronger forgery remains open as declared; no truth-binding claim.

### C2 operability — child-status discrimination

Declared: (a) genuine red child rc=1 with its contract marker → RED/1; (b) child crash rc=2 →
ERROR/2; (c) child skipped/rc forced zero with no marker → ERROR/2; (d) missing used-by sibling →
ERROR/2; plus a green selftest and the real four-leg landing GREEN.

Commands and observed output:

```sh
git cat-file -e eafd500f:quality/counters/c2-r66-landing-instrument.py   # absent at base
git cat-file -e 739a01c5:quality/counters/c2-r66-landing-instrument.py   # present (186 lines)
git show eafd500f:quality/landing-counters.sh | wc -l   # 236
git show 739a01c5:quality/landing-counters.sh | wc -l   # 254
git show 739a01c5:quality/landing-counters.sh | grep -nE '^\s*\[\[ "\$ROUND" =~|verdict=ERROR exitcode=2'
# 223: [[ "$ROUND" =~ ^[1-9][0-9]*$ ]] || fail '--round N required (positive integer)'
# 248: verdict=ERROR exitcode=2
git show 739a01c5:quality/landing-counters.sh | sha256sum   # e4767ec74f1f… (matches lesson)
git show 739a01c5:quality/counters/c2-r66-landing-instrument.py | sha256sum  # e4d62b3c1e6f…
cd .ufo/waves/round-66/measurement-evidence/c2-after
for n in a-genuine-red b-child-crash c-skip-no-marker d-missing-usedby; do
  echo "$n baseline=$(cat baseline/run-$n.rc) candidate=$(cat candidate/run-$n.rc)"; done
# a-genuine-red baseline=1 candidate=1
# b-child-crash baseline=1 candidate=2
# c-skip-no-marker baseline=0 candidate=2
# d-missing-usedby baseline=1 candidate=2
tail -1 candidate-selftest.out   # MADO_LANDING_COUNTERS_SELFTEST: 58/58 assertions passed (rc 0)
cat candidate-driver.out
# MADO_R66_INSTRUMENT: selftest=0 landing=0 green=yes verdict=TARGET_MET rev=739a01c5…
```

Baseline correct = 1/4 (only (a)); candidate correct = 4/4. Independent counts at `739a01c5`
re-derive the real landing legs in the committed driver log:

```sh
git ls-tree --name-only 739a01c5:corpus/knowledge | grep -c '\.md$'          # 78 -> nav indexed=78/78
git show 739a01c5:corpus/README.md | grep -cE '^\| `knowledge/[^`]+\.md`'   # 78
git show 739a01c5:corpus/SOURCES.md | grep -cE '^\|\s*S[0-9]{3,}\s*\|'      # 372 -> used-by rows=372
# population = tools/* + quality/*.py + quality/counters/*.py (suffix exclusions) = 108
# ledger data rows (grammar example excluded) = 108
```

Driver log: `revision=739a01c5 indexed=78/78`; `MADO_USED_BY: entries=78 rows=372 missing=0 …
verdict=TARGET_MET`; `LEDGER: population=108 ledger_rows=108 … verdict=TARGET_MET`;
`MADO_CITECHECK: citations=4 resolved=4 missing=0 … verdict=TARGET_MET`;
`MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0 rev=739a01c5…)`.

Post-measurement commit `ecfc8ac3` changes no `quality/` bytes (`git diff --stat 739a01c5 ecfc8ac3`
touches only `.ufo/waves/round-66/` evidence, `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-66.md`),
so the measured instrument revisions remain valid at the lane tip.

Compatibility note: explicit `--citecheck-paths` outside the repository is now refused
(`realpath` must be under `--repo`). No committed in-lane caller passes an external path
(`grep -rn '--citecheck-paths'` → in-repo receipts and the selftest only), the r65 bytes remain
at their historical revisions, and the restriction is declared in `SKILL.md`, `PROVINCE.md` and
the lesson. The r65 driver (`quality/counters/c2-r65-landing-instrument.py`) is pinned to r65-era
revisions and is not claimed valid against post-cutover bytes. No operability harm observed on
the lane's actual use; the restriction is routed for operator-facing documentation.

Verdict: **improved**, bounded (1/4 → 4/4; 2.5/10 → 10/10), with the declared external-path
restriction recorded, not silent.

## Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | improved | C1 1/4 → 4/4 on the frozen finite rubric; selftest 15/15; residual stronger-forgery and state-truth limits declared, not erased |
| operability | improved | C2 1/4 → 4/4; selftest 58/58; real four-leg landing GREEN (78/78, missing=0, 108/108, 4/4); explicit round scope; external-path cutover declared |
| coverage | unchanged | no desktop surface, PROVINCE frontier move or coverage-map ground entered; report says so |
| depth | unchanged | no `corpus/knowledge/` entry added (`git diff --stat eafd500f ecfc8ac3 -- corpus/knowledge/` empty) |
| freshness | unchanged | no re-verification of an existing knowledge entry; SOURCES cells untouched |
| adjacency | unchanged | connector screened sibling prior art (kumitate NO_CHILD, tsukuroi could-not-evaluate, tameshi ARM_DEAD) and absorbed nothing; no cross-domain write |

## Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S435 — GNU Bash exit status | admit | `https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html`; `https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz` | agree | The lesson's 15-word quote ("So while an exit status of zero indicates success, a non-zero exit status indicates failure.") is verbatim at §3.7.5; the release tarball sha256 is `0d5cd869…` exactly as pinned, and `doc/bashref.texi:3905-3906` carries the quote. The row's scope is correctly bounded to exit-status vocabulary, not marker authenticity. |
| "these structural checks prove state truth or honest invocation" | reject | `quality/counters/c1-r66-register.py`; `quality/landing-counters.sh` | agree | C1 `assess()` reads only heading/row/receipt/live-line structure and its own `state-truth-not-measured` case asserts invented state passes; C2 `marker_valid()` compares self-reported markers to the child's rc with no authentication. The flip condition ("independently authenticated execution and domain observation") is the right bar. |
| ledger marker literal (erratum) | reject-shaped premise defect | `quality/check-tool-ledger.py:350,368,549` | agree | The actual child emits `LEDGER:` and `MADO_TOOL_LEDGER` occurs 0 times; the erratum is accurate, the implementation binds the real child, and the lane did not fabricate an alias. The frozen declaration literal is the defect (routed). |
| Python subprocess returncode docs | not selected (neither admit nor reject) | not re-opened | not graded | The lesson calls it valid but unnecessary for the shell-policy row; no admission rests on it. |

## Trend verdicts

- **expansion: unchanged** — `git diff --stat eafd500f ecfc8ac3 -- corpus/knowledge/ corpus/README.md`
  is empty; one SOURCES row (S435) was admitted but no knowledge entry cites it on uncovered
  ground (its `used-by` is the round lesson); no desktop frontier move (`PROVINCE.md` records
  read-only instruments only).
- **quality: improved** — the two bounded instruments improve 1/4 → 4/4 with selftests 15/15 and
  58/58 and the real four-leg landing GREEN at `739a01c5`; QUALITY 108 is added with a grounded
  failure demonstration; SOURCES census is exit 0 with the row arithmetic re-derived; no admitted
  entry was found false or stale and left unmarked (no entry changed).
- **discernment: improved** — this outside sample agrees with the round's Gate on both the admit
  (S435, quote and pin re-opened) and the reject (structural checks are not truth); the lane's
  declared limits and the marker erratum are recorded rather than learned late, and no
  disagreement was left unlearned.

## Routed defects (round 67 must fix; status-neutral)

1. **Frozen C2 predicate literal** — carry `marker-premise-erratum.md` into the next frozen
   declaration: quote the actual child output (`LEDGER:`) before freezing, never a remembered
   literal; do not rename child output.
2. **C1 stronger-forgery acceptance** — a PROVINCE-only forgery that leaves the real live
   receipt committed, and false state cells with valid receipts, still pass. The lane's planned
   row names this; keep it open until a new frozen predicate demonstrates a red-before/green-after.
3. **C2 external citation paths** — the refusal is declared and unsound-capable r65 behaviour is
   removed; document the operator-facing cutover (in/out of repo) and decide whether an explicit
   opt-out is wanted, keeping the dirty-guard soundness.
4. **Mutation residuals** — zero-citation positivity and replacement-ref safety survive the
   frozen four cases plus selftest; they need auxiliary probes before any universal fault-coverage
   claim. The lane already limits the claim; do not widen it next round.
5. **r65 routed defect 1 closed** — this round added only S435 and changed no existing SOURCES
   cell (`git diff --numstat eafd500f ecfc8ac3 -- corpus/SOURCES.md` → `11 0`); keep rule 2 and
   record future re-opens via `recheck`/a correction row.

## Notes for the operator

- All four `SHONEN.md` boxes remain `[~]`; the report's four `[~]` lines match. Boxes 1 (tables,
   cited sources) and 4 (province boundary) look mechanically checkable by a non-author; boxes
   2/3 rest on historical end-to-end evidence. Promotion is operator-owned; this closure writes
   no `[x]` and performs no promotion.
- Open L0 questions r57/r58/r59/r60 remain operator-owned; no waiver is inferred.
