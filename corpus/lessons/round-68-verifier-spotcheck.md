# mado round 68 — verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-03 (closed 2026-11-04 UTC)
round: mado r68 (lane counter 68)
base: 510100c81e6cf63fec6be380c2f2f9c670f32cbc
lane head: 80c6d7aa350f8c66044f002753f6434632446fb0
report: `.ufo/reports/round-68/mado.md` @ 1bea4e187742207c218ce801d2a29840beaa2a58
dispatched prompt: `.ufo/prompts/mado-round-68.md` @ 576ee49093dd6fd83b88d6661889acde8bd4dd19
scope: non-author verification only. No lane-authored file edited, no `[x]` written, no promotion, no
sibling lane touched, no lane `git`/`jj` mutation. The round's counters and gates were **not executed**:
their committed receipts were read, and the claims were re-derived from committed bytes with
`git show`, `ls-tree`, `grep -cF`, `awk`, `sha256sum`, `git ls-remote`, `curl` and `wc`.

## Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report attribution | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-68/mado.md` | `mado-shokunin 1bea4e187742207c218ce801d2a29840beaa2a58` | pass |
| report lands last | lane tip vs report vs watchdog | lane tip `80c6d7aa` 22:24:54-03:00; report `1bea4e18` 22:25:31-03:00; `complete` 22:26:08-03:00 | pass |
| SHONEN contract | `grep -c '^## SHONEN'` and marker lines vs `SHONEN.md` | 1 heading; 4 `[~]` lines, one per each of the 4 boxes, each with a pointer (r68 gate rows, round-3 task, lesson commands, PROVINCE paragraph) | pass |
| cited commits | `git cat-file -e` + `git -C …/mado-shokunin merge-base --is-ancestor <h> refs/heads/master` | base `510100c8` and the 18 round commits (`2ca2bec3`, `e0727cda`, `40d2bef8`, `2a39e741`, `686d6345`, `425d4b2f`, `47819d79`, `1df69fc8`, `18d692f3`, `379e97f8`, `67b47df4`, `ff255b7f`, `049c2e0c`, `20f692be`, `b21f2742`, `180e5b2f`, `a4cb56fe`, `80c6d7aa`) all exist and are ancestors; `git rev-list --count 510100c8..80c6d7aa` = 18 | pass |
| lane state | `scripts/hyaku/jj-lane.sh state …/mado-shokunin` | `branch=master local=80c6d7aa… remote=80c6d7aa… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| clean tree | `git -C …/mado-shokunin status --porcelain` | empty | pass |
| report pushed | `git ls-remote origin refs/heads/master` + ancestry | fleet `origin/master` `7a7a638f`; report commit `1bea4e18` is an ancestor | pass |
| prompt fidelity | render `templates/round-prompt.md` with `LANE=mado`, `ROUND=68`, `FLEET_ROOT=/home/vgpnk/Projects/shokunin`, `<mado-repo>=mado-shokunin`, `AXES=coverage + operability (desktop and compositor craft)` | 8,375-byte prefix **byte-identical**; remainder begins `## 6. Campaign addendum` (63,121 B total, 54,746 B addendum) | pass |
| prompt contract items | read through | mission/axes binding; 1–3 claims with distinct axes and lowest-axis clause; frontier step; L2 floor ≥8 in ONE batched AgentSwarm call; report path/filename; commit-before-report; `SHONEN` heading; commit-hash citation; write scope; commit-then-push; push scope; L0 side channel — all present | pass |
| dispatch digest | `.ufo/watchdog.log` lines 2161/2168 | `2026-11-03T21:58:09-03:00 launch mado round=68 pgid=801947 driver=hyaku-inline attempt=1` / `2026-11-03T22:26:08-03:00 complete mado round=68; hyaku-inline attempt=1` | pass |
| marker test | content read | work items, receipts, real commits, measurements; not a completion marker | real report |

Conformance defects (status-neutral; none bars admission):

1. **Final-revision counter selftest tallies have no committed receipt.** The report, LOG and
   SCORECARD state C1 counter `27/27` and C2 counter `26/26` at `180e5b2f`, but the committed
   selftest battery `measurement-selftests-r68.txt` (measured content `18d692f3`) reads C1 `26/26`
   and C2 `25/25`, and `c2-denominator-erratum-r68.txt` reads `25/25`. The static check counts
   reproduce 27 and 26 (C1: 3×5 recipe assertions + 1 base + 4 contract-line + 1 sha + 6 scratch =
   27; C2: 22 classifier/verdict/CLI wants + 4 contract/guard cases = 26), so the numbers are true,
   but a numeric claim should carry its run at the measured revision.
2. **Wave-settlement wording.** The report says “Settlement at tip `80c6d7aa`:
   `WAVE wave=w1 … verdict=OK`”. The receipt `wave-done-r68.txt` was *committed* at `80c6d7aa` but
   its own command measured `rev=a4cb56fe`; the receipt says so and the report does not.
3. **One round commit is not enumerated.** `20f692be` (“predicate-literal binding receipt for both
   claims”) is in the tree but absent from the report's Landed-changes table and from the LOG
   round-68 entry; the receipt it carries is cited (`predicate-binding-r68.txt`) in the wave
   receipts only.
4. **Prompt route map.** The §6 run-15 map (“ONLY reviewer uses `@m_zfl`… ”) is the operator's
   amendment; `MISSION.md:53-65` role-class buckets are explicitly advisory and the prompt binds
   routing to the host table, so no binding conflict; the lane repo hardcodes no model alias. The
   run-13 “mado stays on SECURITY HOLD” line is superseded by the run-15 preamble (“supersedes the
   run-13 routing, round-size, budget, fresh-start and hold lines below”); no credential material
   appears in the round's files (spot read of the new lesson/entry/receipts).
5. **Lowest-axis posture.** Every published sub-axis sits at its measured maximum (navigation
   80/80, calibration resolved-active 86/86, operability selftest 12/12 at the measured content), so
   no axis is distinctly lowest; the round uses new finite denominators as rounds 56–67 did. The
   stagnation nudge does not waive it (last capability r67, gap 0 < N=3). Recorded as the standing
   posture, not scored as a defect.

## Claims re-check

Both claims are finite-control claims. The counters were **not executed**; each before/after line
comes from a committed receipt at the named revision, and the structural claims (population, reader
set, guard presence, recipe uniqueness, harness identity) were re-derived from committed bytes.
Claim C1's after-line and C2's after-line were additionally re-derived from committed source shape
below.

### C1 calibration — the control harness kills its own forged kill credit

Declared: at `REV`, `c1-r68-selfmutants.py` extracts `c1-r68-landing-controls.py`, runs its
`--selftest`, applies three frozen single-point recipes exactly once each, and counts a recipe
killed iff the mutant's own selftest exits nonzero; the base control applies the same recipes to
`c2-r67-landing-controls.py` at `510100c8`. Bounded `10 × killed / 3`.

Re-measured (plain, over committed bytes):

```sh
git show 180e5b2f55e2c4388f3496ace7574f4288af1450:quality/counters/c1-r68-landing-controls.py | sha256sum
# 25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527  -
git show 510100c81e6cf63fec6be380c2f2f9c670f32cbc:quality/counters/c2-r67-landing-controls.py | sha256sum
# a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58  -
# each frozen recipe occurs exactly once in both harnesses (grep -cF):
#   mr_killed = bool( -> 1 ; mz_killed = mz_rc != 0 -> 1 ; killed = int(mz_killed) + int(mr_killed) -> 1
```

Evidence-verified (committed receipts; not re-executed):

- `control-baseline-r68.txt` at `510100c8`: `MADO_R68_SELFMUTANTS: selftest=absent killed=0/3
  applied=0/3 base=0/3 verdict=TARGET_MISSED` rc 1; base harness `47/47`, `survivors=S1,S2,S3
  killed=0/3 applied=3`.
- `measurement-final-r68.txt` at `180e5b2f`: `MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3
  base=0/3 verdict=TARGET_MET` rc 0; harness `52/52`; mutants rc 1 with `51/52`, `51/52`, `50/52`;
  the same lines at `379e97f8` in `measurement-content-r68.txt`; `record-landing-r68.txt` re-runs
  green at `67b47df4`.
- The counter's `--selftest` body drives `measure()` through `_scripted_run` with no spawn
  (`c1-r68-selfmutants.py:255-300`, harness `_scripted_run` at `:524-560`), so a forced kill credit
  changes the asserted line; this is the r67 routed defect 3 closure.

Before → after: `0/3` → `3/3`, bounded `0.0000` → `10.0000`. **Verdict: improved** (frozen
three-recipe set; multi-point forgeries survive and are named by RevC1 — limit, not a claim).

### C2 operability — the standing gates read git objects through a guarded environment

Declared: population = every tracked `quality/check-[^/]+\.py` at `REV`; reader = blob contains a
quoted verb from the frozen vocabulary plus a `git` token; guarded = an AST construction of
`GIT_NO_REPLACE_OBJECTS`; `population=20` and `readers=13` are part of the target; 11/11 frozen
classification cases scored. Bounded `10 × guarded / readers`.

Re-measured (plain, over committed bytes):

```sh
# tracked population at both revs
git ls-tree --name-only HEAD quality/ | grep -cE '^quality/check-[^/]+\.py$'   # 20
# readers by the frozen predicate at base and at 180e5b2f: 13 at both
# guard string present (grep -l GIT_NO_REPLACE_OBJECTS quality/check-*.py):
#   510100c8 -> 1  (quality/check-tool-ledger.py)
#   80c6d7aa -> 13 (the twelve repaired + check-tool-ledger.py)
# the twelve base→tip quality/check-*.py diffs are guard-only (+ one `import os` in
# check-landed-contract.py); no argv/stdout/exit-path edit
```

Evidence-verified (committed receipts; not re-executed):

- `control-baseline-r68.txt`: `population=20 readers=13 guarded=1 unguarded=12 controls=11/11
  verdict=TARGET_MISSED` rc 1, per-file `MADO_R68_READER` lines, and 11/11 `MADO_R68_CONTROL` cases.
- `measurement-final-r68.txt` at `180e5b2f`: `population=20 readers=13 guarded=13 unguarded=0
  controls=11/11 verdict=TARGET_MET` rc 0; the same at `379e97f8` and at `67b47df4`
  (`record-landing-r68.txt`).
- Controls sha256 `b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91` at the freeze
  and at the worktree (re-hashed here).
- The reviewer's behaviour table (`w1/R68RevC2.md:54-73`) pairs all twelve base/repaired gates with
  identical rc and byte-identical stdout/stderr on real arguments; `R68ExecHazard.md` and
  `aux-dominance-r68.txt` supply the hazard sample and the declared guard-dominance limit.

Before → after: `1/13` → `13/13`, bounded `0.7692` → `10.0000`. **Verdict: improved** (census
classifies construction, not wiring or dominance; declared limit, restated in the entry §5 and the
axis-posture erratum).

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | improved | C1: base control 0/3 → candidate 3/3 killed on the frozen recipes; the successor harness's selftest drives its own decision body; r67 routed defect 3 closed |
| operability | improved | C2: guarded readers 1/13 → 13/13, unguarded 12 → 0, 11/11 controls, population/reader constants enforced; the twelve gates keep argv/output/rc |
| depth | improved | `SKILL.md` § Round 68 gate-registry rows (entry command, verdict map, selftest spelling, pinned values, write scope, owner) and `corpus/knowledge/gate-git-read-guards-r68.md` (four accepted / three rejected guard shapes, each line-cited) |
| freshness | improved | the axis publication stale since round 56 re-derived at the measured content (`checked=3 mismatched=0`, `measurement-final-r68.txt`); the twelve gates brought under the r67 guard rule after the r67 entry named the read surface |
| coverage | unchanged | no desktop/compositor surface added; `PROVINCE.md` gains an instrument paragraph only, no frontier move; the SOURCES row is lane-tooling scope |
| adjacency | unchanged | the connector screened `shokuknow/merge/mado` (147 rows, 94/147 id collisions) and `considerthese/2026-10-28.md`; sibling prior art cited (kaidoku F2, kama batteries, tsukuroi, kagi), none adopted; no contested scope reported |

## Discernment spot-check (non-author, this file)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S437 — git v2.56.0 `Documentation/git-cat-file.adoc`, tier A `docs`, status `mined` | admit | `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-cat-file.adoc` re-fetched 2026-11-04T01:2xZ: 16,099 B, sha256 `6c32dbda8c2106be08bda471592db50b5afaf185de32f2e513e80d802b4a95b2`; DESCRIPTION lines 21-22; `--batch-all-objects` lines 198-199; `git ls-remote` tag object `2478544319491bbd2a42cc57a83e3d2f4730a280`, peeled `a018953688f1b10bddf91bff8747068f5f4746a4`; host `git version 2.56.0` | agree | the lesson's 18-word quote matches lines 21-22 verbatim (≤25 words); the 198-199 boundary sentence matches and is scoped to `--batch-all-objects`; the tag pin and byte hash resolve; the row is 11 cells with no pipe, `mined`, and both `used-by` paths exist (`corpus/lessons/round-68.md`, `corpus/knowledge/gate-git-read-guards-r68.md`) |
| Reject: “`git cat-file -e` establishes object authenticity or integrity” | reject | same URL, OPTIONS `-e` lines 49-52 and line 291 (“If `-e` is specified, no output, unless the `<object>` is malformed.”) | agree | the page defines `-e` as existence plus format validity (“exists and is a valid object”), never provenance or content truth; the offered flip (a signature/verification sentence, or an instrument that pins bytes to a digest) is the right boundary |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0
(`mado ok …/corpus/SOURCES.md`), with the pre-existing W01/W04 warnings (duplicate URLs across
scopes; `S277 tierC mined`) and no W/E for S437. Row census re-derived here: 373 → 374 rows, tier A
359 → 360, B 7, C 7, malformed 0, no duplicate ids.

## Trend verdicts

- **expansion: improved (bounded)** — one admitted `knowledge/` entry on ground the coverage map did
  not hold (the lane's gate git-read surface), its `source:` citing the mined S437, with its README
  index row landing in the same commit `47819d79`; SOURCES 373 → 374, tier A 359 → 360. No desktop
  or PROVINCE frontier move is claimed, and none is read out of it.
- **quality: improved** — twelve standing gates hardened with behaviour-identity pairs (12/12 rc and
  stdout/stderr identical); the harness selftest now drives its own measurement body (base 0/3 →
  candidate 3/3 kills; 52/52); two counter defects fixed with red-before receipts (`rc 2` →
  contract line; `readers=12 TARGET_MET rc 0` → `TARGET_MISSED rc 1`); the stale axis publication
  re-derived (`checked=3 mismatched=0`); no admitted entry was found false or stale and left
  unmarked, and the one owed S436 `used-by` cell was completed as logged.
- **discernment: improved** — the outside spot-check agrees with the gate on the sampled admit
  (S437) and reject (`cat-file -e` authenticity), and the round's own attack seats caught two real
  counter defects before landing (M68-4/M68-5) with the survivors disclosed; QUALITY 110 is grounded
  in those lessons. (The lane reported `unchanged` because the outside check had not yet run; this
  file is that check.)

## Routed defects for round 69

1. **Commit the final-revision counter-selftest receipt.** Run
   `python3 quality/counters/c1-r68-selfmutants.py --selftest` and
   `python3 quality/counters/c2-r68-reader-guard.py --selftest` at the final content revision and
   commit the output (expected `27/27` and `26/26`), or cite the static count with its command; the
   current committed battery (`measurement-selftests-r68.txt`, `18d692f3`) reads `26/26` and `25/25`.
2. **Name the settlement revision the receipt measured.** `wave-done-r68.txt` measures
   `rev=a4cb56fe`; the report says “Settlement at tip `80c6d7aa`” (the file is *committed* there).
   Write both, as the report already does for the measurement receipts.
3. **Enumerate `20f692be`.** The predicate-literal binding receipt commit is in the round's history
   but absent from the report's Landed-changes table and the LOG round-68 entry; add the row next
   round (append-only; the filed report bytes are not rewritten).
4. **Carry forward (no action this round):** the frozen declaration's control-case index
   parenthetical (“cases 6, 8, 10, 11”) drifts from the JSON order; the lesson records it, the
   counter scores by case name, and the declaration stays frozen. The guard-dominance limit
   (`dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` filtered by `GIT_*` reads forged bytes while
   classified guarded) is disclosed in `aux-dominance-r68.txt` and the entry §5; the round-69 plan
   already lists the dominance predicate.

## Promotion note (operator-owned)

The four `SHONEN.md` boxes are all `[~]` in the report; box 1 (SKILL decision tables and cited
sources) and box 4 (PROVINCE accuracy) look checkable by a non-author on these artifacts, but
closure writes no `[x]` and promotion is operator-owned. This file is not a promotion review.

## Wave and stale-lane notes

One v1 wave, `w1`, 12 seats (executor 4, scribe 2, scout 1, connector 1, reviewer 2, critic 1,
mutation-tester 1; attack 4/12 = 33 %; connector 1 ≤ 2), one batched task call
(`w1-dispatch.json` `counts.spawn=12`, `resume=0`; `w1.ready` taken), band 8–16 under
`ufo-wave-policy.json` (`waveMinLanes=8`, `waveMaxLanes=16`), L1 holds the planner seat. Settlement
`WAVE wave=w1 ready=1 results=present seats=12 dispatched=12 settled=12 verdict=OK` at `a4cb56fe`
(`wave-done-r68.txt`, committed `80c6d7aa`); no dead seats. The driver dispatch/complete digest is
in the Conformance table; the mission ran 28 minutes, under two driver ticks. `.ufo/state/mado.round`
reads `1` (run-scoped for every lane); the round counter evidence is the watchdog `round=68` line.
