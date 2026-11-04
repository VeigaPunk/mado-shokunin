# mado round 69 — verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-03 (closed 2026-11-04 UTC)
round: mado r69 (lane counter 69)
base: 04093b83f73a841117d3b31dbb2a6063f4f2a454
lane head: 9d91f7f6f5c603bdc19cf455ce6f413c5990d744
report: `.ufo/reports/round-69/mado.md` @ cb9881d3653c60f2ac5d80bc1914197ef94f83a2
dispatched prompt: `.ufo/prompts/mado-round-69.md` @ 543c2c8f19a64c55d07a6a6125c71f70a2a1db2f
scope: non-author verification only. No lane-authored file edited, no `[x]` written, no promotion, no
sibling lane touched, no lane `git`/`jj` mutation. The round's counters and gates were **not executed**:
their committed receipts were read, and the claims were re-derived from committed bytes with
`git show`/`cat-file`/`ls-tree`/`merge-base`/`log`, `grep -c`, `jq`, `sha256sum`, `wc`, `stat`, `curl`
and the fleet source census. The one execution this artifact adds is `scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin mado` (exit 0).

## Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report attribution | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-69/mado.md` | `mado-shokunin cb9881d3653c60f2ac5d80bc1914197ef94f83a2` (committer date 23:07:30-03:00) | pass |
| report lands last | lane tip vs report vs watchdog | lane tip `9d91f7f6` 23:06:39 < report committer 23:07:30 < `complete` 23:08:02 | pass |
| SHONEN contract | `grep -c '^## SHONEN'`; marker lines vs `SHONEN.md` | 1 heading; 4 `[~]` lines, one per each of the 4 boxes, each with a resolvable pointer | pass |
| cited commits | `git cat-file -t` + `git -C …/mado-shokunin merge-base --is-ancestor <h> refs/heads/master` | base `04093b83` and the 18 commits named in the report (`789a87f1`, `98bff016`, `5fc29ae7`, `6a5cefd2`, `6d21f535`, `296ed0d7`, `5864b00d`, `3cd68aa3`, `fc0387b9`, `e0e1831a`, `932bc932`, `bba64c3a`, `759c9d7b`, `139f4801`, `4a9482bb`, `1f26080d`, `3b2756e4`, `9d91f7f6`) all exist and are ancestors | pass |
| round commit count | `git rev-list --count 04093b83..9d91f7f6` | 19 — one more than the 18 rows of the report's Landed-changes table; `b9b70a09` is unenumerated (defect 2) | defect |
| lane state | `scripts/hyaku/jj-lane.sh state …/mado-shokunin` | `branch=master local=9d91f7f6… remote=9d91f7f6… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| clean tree | `git -C …/mado-shokunin status --porcelain` | empty | pass |
| report pushed | `git merge-base --is-ancestor cb9881d3 origin/master` | yes (`origin/master` `ca2ce46e`) | pass |
| prompt fidelity | section headings vs `templates/round-prompt.md` | sections 1–5 at the template's own lines 3/9/42/80/99/131, then `## 6. Campaign addendum` and `## 7. Scratch discipline`; mission/axes binding, 1–3 claims on distinct axes, frontier step, L2 ≥8 in one batched call, report path, commit-before-report, `SHONEN` heading, commit-hash citation, lane write scope, commit-then-push, push scope, L0 channel — all present | pass |
| prompt route map | run-15 §6 map vs `MISSION.md:53-65` | MISSION's role-class buckets are explicitly advisory and the prompt binds routing to the host table; the run-15 amendment ("ONLY reviewer uses `@m_zfl`") is the operator's routing, not a MISSION conflict; no model alias hardcoded in the lane | pass |
| dispatch digest | `.ufo/watchdog.log` (mutable) lines 2174/2182 | `2026-11-03T22:35:42-03:00 launch mado round=69 pgid=972874 driver=hyaku-inline attempt=1` / `2026-11-03T23:08:02-03:00 complete mado round=69; hyaku-inline attempt=1` | pass |
| marker test | content read | work items with receipts, real commits, measurements, Sources & frontier and Trend verdicts — not a completion marker | real report |
| freeze ordering | `stat` on the wave inputs vs freeze commit `789a87f1` 22:42:47 | declaration 22:42:43 and control JSON 22:41:49 precede the freeze commit; ready 22:44:47; dispatch marker 22:47:43; instruments committed 22:47:50 | pass |

Conformance defects (status-neutral; none bars admission):

1. **Round-69 LOG bullets were inserted into the Round 67 and Round 68 entries.** The 10-line block
   ("Critic closures (`R69CriticClaims`, B1-B11) …", "Final measurement at `759c9d7b` …", "Wave
   settlement: 12 seats dispatched …") appears three times: inside the Round 67 entry (before its
   Tooling bullet, LOG.md:3257-3266), inside the Round 68 entry (before its Tooling bullet,
   LOG.md:3314-3323) and in the Round 69 entry where it belongs (LOG.md:3396-3405). All three copies
   were introduced by `139f4801` (`git log -S 'Wave settlement: 12 seats dispatched' -- LOG.md`
   returns only that commit). No prior bytes were deleted, but the insertions alter two filed
   entries and misattribute round-69 facts to rounds 67/68 — an append-only organization defect.
2. **One round commit is not enumerated.** `b9b70a09` ("final measured content and the
   mutation-battery closure in the records", 23:01:21) writes `measurement-final-r69.txt`,
   `cross-set-r69.txt`, `final-gates-r69.txt`, `landing-counters-r69.txt` and the since-removed
   `report-draft.md`; it is absent from the report's Landed-changes table, `LOG.md` and
   `SCORECARD.md` (`grep -rn b9b70a09` → rc 1).
3. **Freeze-order evidence is misdescribed for r69.** The report says `check-freeze-order.py` reads
   `reason=no_freeze` for "both r68 and r69"; the committed r69 receipt
   (`final-gates-r69.txt:17`) reads `MADO_FREEZE_ORDER: SETUP work_not_a_directory`, and the check's
   `REQUIRED = ("claims-frozen.md", "registration.md")` cannot see the lane's
   `claims-declaration-r69.md`. Pre-existing and disclosed, but the r69 line is not the r68 line.
4. **`w1-results.json` carries no settlement status.** Its `results[]` rows have
   `name`/`agent`/`output`/`note` only; "12 settled, no dead seats" is inferred from 12 non-empty
   outputs. The claim is true on the file, but the file does not state it.
5. **`check-deliverables.py` is red on the round-68 seat reports** (`CHECK101: reports=6 declared=4
   exists=1 absent=3 undeclared=5 verdict=FAIL`), reproduced at the base and disclosed by the round;
   pre-existing, not a r69 product.
6. **The report's "measured content `759c9d7b`" is receipt-backed only at `139f4801`.** The two
   revisions carry byte-identical instruments (re-hashed below), so the values transfer, but the
   receipt header names `139f4801`; `LOG.md:3263` attributes the same receipt to `759c9d7b`.

## Claims re-check

Both claims are finite-control claims. The counters were **not executed**; each before/after line
comes from a committed receipt at the named revision, and the structural claims (population, recipe
uniqueness, harness identity, control-set shape) were re-derived from committed bytes.

### C1 calibration — the hardened harness kills paired (decision + oracle) forgeries

Declared: at `REV`, `quality/counters/c1-r69-paired-recipes.py` extracts
`quality/counters/c1-r69-landing-controls.py`, runs its `--selftest` (rc 0), applies R1/R2/R3 once
each, counts a mutant killed iff its own `--selftest` exits nonzero, and requires the same recipes at
`--base-rev` to survive on the round-68 harness (`base=0/3`). Bounded `10 × killed / 3`.

Re-measured (plain, over committed bytes):

```sh
git -C …/mado-shokunin cat-file -e 04093b83:quality/counters/c1-r69-landing-controls.py   # absent
git -C …/mado-shokunin cat-file -e 759c9d7b:quality/counters/c1-r69-landing-controls.py   # present
git -C …/mado-shokunin show 759c9d7b:quality/counters/c1-r69-landing-controls.py | wc -c
# 38461
git -C …/mado-shokunin show 759c9d7b:quality/counters/c1-r69-landing-controls.py | sha256sum
# 9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73  -   (receipt: same)
git -C …/mado-shokunin show 04093b83:quality/counters/c1-r68-landing-controls.py | wc -c
# 36005
```

Recipe uniqueness at both ends, read from the counter's own `RECIPES` (`c1-r69-paired-recipes.py:45-52`):

```
R1 "mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)\n … and forged_credit(mr_rc, mr_marker))"
   candidate 1 · r68 base 1
R2 "mz_killed = mz_rc != 0"                         candidate 1 · r68 base 1
R3 "subprocess.run = _no_spawn"                     candidate 1 · r68 base 1
```

The harness selftest exists and asserts the paired oracles
(`c1-r69-landing-controls.py:659,668`: "a crashing M-R child is not a kill (decision + oracle pair)",
"an M-Z run with no assertion summary is not a kill"). Instrument bytes are identical at `759c9d7b`
and `139f4801` (`sha256 9461a059…` at both; counter `15a43adc…`; control set `975ca3ba…`).

Evidence-verified (committed receipts):

- `control-baseline-r69.txt`: `BASE_UNMUTATED rc=0 … 52/52`; each of R1/R2/R3 `occurrences=1`,
  `killed=no`, `52/52`; `MADO_R69_C1_BASE: selftest=0 killed=0/3 applied=3/3 verdict=TARGET_MISSED`
  — the do-nothing control misses before freeze.
- `measurement-final-r69.txt` at `139f4801`: `MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3
  applied=3/3 base=0/3 verdict=TARGET_MET rev=139f4801…`; harness `59/59`; counter selftest `28/28`;
  each candidate mutant rc 1 with `57/59`, `58/59`, `57/59`; each base mutant rc 0 with `52/52`.
- `measurement-r69.txt` at `296ed0d7` reads the same contract line; `measurement-c1-r69.txt` at
  `5fc29ae7` is the first measurement; `critic-closures-r69.txt` carries the B2 red-before
  (`base applied=1/3` → `TARGET_MET rc 0`) and green-after (28/28).
- Before-line at base: the counter reports `selftest=absent killed=0/3 applied=0/3 base=0/3
  verdict=TARGET_MISSED` (pinned in the counter's own selftest case at
  `c1-r69-paired-recipes.py:377`), and the harness is absent at `04093b83` (re-derived above).

Before → after: `0/3` (bounded `0.0000`) → `3/3` (bounded `10.0000`). **Verdict: improved** on the
frozen three-recipe set. The B1 limit (a text-checking stand-in harness can score the target) is a
disclosed instrument limit, not a claim.

### C2 operability — the guard census requires key position and dominance

Declared: at `REV`, `quality/counters/c2-r69-guard-dominance.py` reads the tracked
`quality/check-[^/]+\.py` population, classifies readers and guarded readers (key position + a
dominance path to a `git` launch), and scores the same 11 frozen cases with the r68 classifier as a
base leg. Target `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11`.
Bounded `10 × controls / 11` for the discrimination move.

Re-measured (plain, over committed bytes):

```sh
git -C …/mado-shokunin ls-tree -r --name-only 139f4801 -- quality \
  | grep -E '^quality/check-[^/]+[.]py$' | wc -l                      # 20
sha256sum …/mado-shokunin/.ufo/waves/round-69/controls/c2-controls-r69.json
# 975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9
jq '.cases|length' …/c2-controls-r69.json                            # 11
jq '[.cases[]|select(.expect_guard==true)]|length' …                 # 6
jq '[.cases[]|select(.expect_guard==false)]|length' …                # 5
jq '[.cases[]|select(.expect_reader==true)]|length' …                # 11
# 13 of the 20 quality/check-*.py files carry GIT_NO_REPLACE_OBJECTS in a key-position shape
# (dict key / subscript store / update-setdefault or dict() keyword), by a crude grep;
# git ls-tree + grep over 139f4801 lists exactly those 13 names.
```

The r68 rule's `7/11` is arithmetically consistent with the frozen set and the baseline receipt's
per-case lines: six cases expect `guard=true` and the r68 rule returns `(True, True)` on each;
`mention-only` expects `(True, False)` and the r68 rule returns `(True, False)`; the other four
negative cases (`value-position-only`, `dead-branch-only`, `uncalled-helper`, `overwritten-env`)
expect `(True, False)` and the r68 rule returns `(True, True)` — 6 + 1 = 7 correct. The r69 rule
scores all 11 (`control-baseline-r69.txt` § C2, proto column).

Evidence-verified (committed receipts):

- `control-baseline-r69.txt` § C2: per-case `r68=(…) proto=(…) expect=(…)`; `MADO_R69_C2_BASE:
  controls=7/11 verdict=TARGET_MISSED`; `MADO_R69_C2_PROTO: controls=11/11 verdict=TARGET_MET`;
  `population_at_base=20`.
- `measurement-final-r69.txt` at `139f4801`: `MADO_R69_GUARD_DOMINANCE: population=20 readers=13
  guarded=13 unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MET rev=139f4801…`;
  counter selftest `43/43`; the counter pins the control digest at
  `c2-r69-guard-dominance.py:69`.
- `c2-classifier-repair-r69.txt`: pre-fix 7 violations → post-fix 8/8 attack cases; the frozen
  controls and the 20/13/13 population unchanged; selftest 40/40 at that commit.
- `cross-set-r69.txt`: r69 rule 11/11 on the round-68 set as well; r68 rule 7/11 on this set.
- The connector seat's differential (`w1/R69ConnSiblings.md` §1) confirms the new rule changes no
  verdict inside the frozen population (`diffs=0`, 13/13 both rules) — the move is discrimination on
  the frozen negative shapes (critic B11), as the SCORECARD row now states.

Before → after: `7/11` (bounded `7.0000`) → `11/11` (bounded `10.0000`) on the discrimination move;
the population fraction `guarded/readers` is `13/13 = 10.0000` at both ends and is harm-watch only.
**Verdict: improved** (bounded syntactic rule; declared limits restated in the entry §5).

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | improved | C1: base control `0/3` (bounded 0.0000) → candidate `3/3` (10.0000) on the frozen paired recipes; the harness selftest drives decision + oracle (`c1-r69-landing-controls.py:659,668`); do-nothing control 0/3 with 52/52 green |
| operability | improved | C2: the new census requires key position and a dominance path to a `git` launch; frozen controls `7/11` → `11/11`, base leg `7/11` printed in the same contract line; two registry rows in `SKILL.md` with entry command, verdict map, selftest spelling, pinned path, write scope, owner |
| depth | improved | `SKILL.md` +9 lines of gate-registry rows and the supersession note; `corpus/knowledge/gate-guard-dominance-r69.md` (provenance trio, five sections, S438/S436/S437 locators); QUALITY 111 (two grounded clauses) |
| freshness | improved (bounded) | the r68 guard rule re-verified against the r69 set (7/11) and the r68 set re-run (11/11); the r68 reviewer's recipe L found equivalent and corrected append-only (`SCORECARD.md` § Closure corrections B8); the axis table re-derived at `4a9482bb` (`checked=3 mismatched=0`) |
| coverage | unchanged | no desktop/compositor/session/service surface touched; one lane-tooling `knowledge/` entry on ground the coverage map already holds (r68 index row); `PROVINCE.md` gains an instrument paragraph only |
| adjacency | unchanged | connector seat scanned sibling overlap and found the population unchanged (13/13 both rules); no contested scope reported; assimilation none; no cross-domain material adopted |
| harmed | **none** | `git diff --numstat 04093b83 9d91f7f6` for SCORECARD `+89 -0`, SKILL `+9 -0`, PROVINCE `+13 -0`, QUALITY `+27 -0`, README `+2 -0`, LOG `+89 -0`; the only in-place registry cells are S436/S437 `used-by` (column 10 only), logged old→new in the lesson Gate |

## Discernment spot-check (non-author, this file)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S438 — git v2.56.0 `Documentation/git.adoc`, tier A `docs`, status `mined` | admit | `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc` re-fetched 2026-11-04T02:17Z: HTTP 200, 47,005 B, 1,212 lines, sha256 `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79` — byte-identical to the row and receipt; `--no-replace-objects` section lines 178-182; `GIT_NO_REPLACE_OBJECTS` environment entry lines 927-929 | agree | the lesson's located quote "This is equivalent to exporting the `GIT_NO_REPLACE_OBJECTS` environment variable with any value" is at lines 180-181 verbatim and 12 words (≤25); the second quote "Setting and exporting this environment variable tells Git to ignore replacement refs and do not replace Git objects" is at 928-929 and 18 words; the row is 11 cells, `mined`, its `used-by` names the round-69 entry, and the tag pin + digest resolve |
| Reject: `git-replace.adoc` as a new row this round (duplicate scope with S436) | reject | same URL at tag v2.56.0 re-fetched: 5,398 B, sha256 `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631`; S436 (`corpus/SOURCES.md:386`) already holds that tag-pinned URL and the replacement-rule scope; the quote "Replacement references will be used by default by all Git commands except those doing reachability traversal…" is at line 34 | agree | a second row would duplicate held ground; the recorded flip condition (a later round re-quoting a different tag, e.g. when the host leaves 2.56.0) is the right boundary |
| New SOURCES row S438 — 11 columns, ≤25-word located quote | row check | `corpus/SOURCES.md:388`; the Gate quote above; row cells re-parsed (`awk -F'|'` NF=13) | agree | the row carries the quote and locators in `anchor`/`teaches`, no pipe in any cell, `S438` unique, census exit 0 with no S438 warning |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0
(`mado ok …/corpus/SOURCES.md`) with the pre-existing W04 duplicate-URL warnings and W01
`S277 tierC mined`; no warning names S438. Row census re-derived here: 374 (base) → 375 (tip);
S438 is the only new row, tier A +1, B +0, C +0; S436/S437 `used-by` only.

## Trend verdicts

- **expansion: unchanged** — the one new admitted entry (`gate-guard-dominance-r69.md`) is on
  lane-tooling ground the coverage map already holds (the r68 gate git-read row and the lane-tooling
  index rows), and `corpus/README.md` advances a Frontier bullet on that same ground; SOURCES
  374 → 375 is one new A/docs/mined row, not a new province surface; no desktop/compositor surface
  is added and `PROVINCE.md` gains no frontier move. This agrees with the report's verdict.
- **quality: improved** — two new measured instruments with frozen do-nothing controls (0/3 and
  7/11), eleven instrument defects repaired before landing with red-before receipts (C2 six, C1
  S1–S5, critic B2/B3), QUALITY 111 added, the r68 guard rule superseded by a stricter one with a
  visible 7/11 base leg, and the r68 control set re-scored 11/11 (`cross-set-r69.txt`). The one
  admitted entry found wrong (r68 recipe L) is corrected append-only, not left unmarked.
- **discernment: improved** — this outside spot-check agrees with the gate on the sampled admit
  (S438) and reject (`git-replace.adoc` duplicate), and the round's own mistakes are mined with
  class/evidence/captured-by/fix (M69-1 equivalent mutant, M69-2 value-position over-inclusion,
  M69-3 setup-default misread). Eleven critic blockers are dispositioned in the open (three
  SCORECARD corrections B8/B9/B11, six disclosures B1/B4/B5/B6/B7/B10, one declared limit) rather
  than smoothed; no disagreement was left unlearned.

## Routed defects for round 70 (append-only fixes; do not rewrite filed bytes)

1. **Name the duplicated round-69 LOG blocks.** Append an erratum in the round-70 LOG entry naming
   the 10-line block at `LOG.md:3257-3266` (Round 67) and `LOG.md:3314-3323` (Round 68) as
   misplaced copies of the Round 69 block at `LOG.md:3396-3405`, introduced by `139f4801`. Delete
   nothing: the filed entries stay byte-identical.
2. **Enumerate `b9b70a09`.** Add the missing row to the next round's Landed-changes table and LOG
   entry: "final measured content and mutation-battery closure in the records"; the filed round-69
   report is not edited.
3. **Fix the final-measurement attribution.** `LOG.md:3263` cites `measurement-final-r69.txt` at
   `759c9d7b`; the receipt header names `139f4801` (instruments byte-identical at both). Append the
   correction in the round-70 entry.
4. **Make `check-freeze-order.py` measurable for this lane.** Its `REQUIRED` names are
   `claims-frozen.md`/`registration.md`; the lane submits `claims-declaration-rN.md`. Align the
   check's expected names (or commit the canonical registration copy) so the gate returns
   OK/FAIL on freeze order instead of `no_freeze`/`SETUP work_not_a_directory`, and stop reporting the
   r68 `reason=no_freeze` line as the r69 result.
5. **Disposition the `check-deliverables.py` red** on the round-68 seat reports
   (`reports=6 declared=4 exists=1 absent=3 undeclared=5`): either scope the check to the current
   round's wave or record a named disposition for the missing r68 files; do not manufacture reports.
6. **Record settlement status per seat.** Add a `status`/`settled`/`dead` field to each
   `results[]` row in the next wave's `-results.json` so "12 settled, no dead seats" is readable
   from the file, not inferred from non-empty outputs.

Carry-forward, no action this round: the r67 `mado` L0 privacy/history question and the r68
citecheck-vacuous-positive L0 question remain open; no new L0 line was filed in round 69, and none
was required.

## Promotion note (operator-owned)

All four `SHONEN.md` boxes remain `[~]` in the report, and no `[x]` is written here. Boxes 1
(SKILL decision tables / cited sources), 2 (end-to-end task logged), 3 (no-oral-context
instructions) and 4 (PROVINCE accuracy) all look checkable by a non-author on these artifacts — box
1 by the `SKILL.md` gate rows and this file's source re-open, box 2 by the two frozen counting
commands and the landing battery, box 3 by the self-contained declarations/receipts, box 4 by the
connector's sibling scan and the unchanged `PROVINCE.md` boundary. Promotion remains operator-owned;
this file is not a promotion review.

## Wave and stale-lane notes

One v1 wave, `w1`, 12 seats (executor 4, scribe 2, scout 1, connector 1, reviewer 2, critic 1,
mutation-tester 1; attack 4/12 = 33 %; connector 1 ≤ 2), one batched dispatch
(`w1-dispatch.json` `counts.spawn=12`, `resume=0`; `w1.ready` taken 22:44:47 < marker 22:47:43),
band 8–16 under `ufo-wave-policy.json` (`waveMinLanes=8`, `waveMaxLanes=16`), L1 holds the planner
seat. `w1-results.json`: 12 rows, 12 non-empty outputs, `note: null` on each, no dead seat — the file
has no status field (defect 4). The mission ran 32 m 20 s (22:35:42 → 23:08:02), under two driver
ticks; the respawn-per-round driver reports no other open mado mission, so no stale-lane action.
No tool installs this round (no `uv`/`npm`/`cargo`/pacman transaction); the pacman pause was
respected.
