author: hyaku closure (non-author integrator, @m_zfl)

# mado round 85 — non-author verifier spot-check

## Decision and scope

**Status ok; admitted false; rejected-honest-stop.** C1's frozen finite predicate verifies at the
revision it names. C2's frozen instrument never executed a case (setup rc2) and its repaired
successor misses the declared kill target (33/37); a successor result is not retroactive. Neither
claim is exploratory. No capability, promotion or score upgrade is awarded from C2. This judge did
not author or improve the round, executed no lane gate, counter, selftest, desktop command or
mutation battery, and changed no lane-authored file.

Reviewed: report `7d7ffdedc00b3c8a584fd60afbc04194c53ee4fd` (fleet), base
`5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`, freeze `3905311c75a39c5710413105865c0a1a7dd0116a`,
measured content `2b6dd76b65de4dfe701db87db13b7e448b3538ee`, lane tip
`b542d3157d5058ac9a6086bd9438969a25bdfb62`. Below, **W** means `.ufo/waves/round-85/` inside the
lane repo and **R** means the lane repo root.

## Step-1 conformance

- `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-85/mado.md`
  returned `mado-shokunin 7d7ffdedc00b3c8a584fd60afbc04194c53ee4fd`. Correct path, lane identity,
  substantive report — not a marker.
- The report carries the `SHONEN` heading with four `[~]` lines, one per box in `R/SHONEN.md`
  (four boxes counted by `grep -c '^- \['`). No `[x]` was written. Pointers resolve:
  `R/SKILL.md:231` is the `### Executable runbook rows (round 85)` heading; `R/LOG.md:4155` is the
  round-85 opening entry; `R/PROVINCE.md:471` is the round-84 boundary paragraph that round 85
  extends.
- Every cited lane hash exists and is an ancestor of the **branch**, never `@{u}`: `cat-file -e`
  and `merge-base --is-ancestor HASH refs/heads/master` both succeeded for `3905311c`, `d7c40e6d`,
  `942365c8`, `2b6dd76b`, `757440ec`, `b542d315` and the base `5f174ca4`.
- `scripts/hyaku/jj-lane.sh state R` printed
  `branch=master local=b542d3157d5058ac9a6086bd9438969a25bdfb62 remote=b542d315… ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git -C R status --porcelain` was empty. No uncommitted round work; pushed.
- Ordering: lane tip committed 17:45:43 -0300; the report commit's **committer** stamp is
  17:47:38 -0300 (author stamp 17:45:16 is the jj change's creation time and precedes the tip by
  27 s). The filed bytes cite `b542d315` twice, a hash that cannot be named before it exists, so
  the report landed after the lane work on the commit evidence; the author-stamp skew is a
  jj-colocation artifact, recorded here as an observation, not a defect.
- Dispatched prompt is durable (`git log -1 -- .ufo/prompts/mado-round-85.md` →
  `mado-shokunin 098c1879… 16:50:32`, before the 16:50:57 launch) and carries the template
  contract §1–§5 plus the hyaku addendum §6: report path §4, commit-then-push §5, `SHONEN` §4,
  hash citation (line 516, "The report lands last and cites the pushed lane hash"), write scope
  (line 448). The ≥8-one-batch L2 floor agrees with `MISSION.md` §L2 concurrency. The prompt's
  routing lines conflict internally (the run-15 split vs the older m_mim-off / scout@m_antigravity
  note); the report discloses that conflict and made no override. Conformance item, status-neutral.
- Wave: `W/receipts/settlement-r85.json` records ONE v1 wave, 13 seats —
  executor3/scribe3/scout1/reviewer2/critic1/mutation-tester1/sentinel1/connector1, planner held by
  L1, 5 attack seats. 13 seat reports are committed under `W/w1/`; all 13 raw `output` bodies are
  null. Disclosed, not inferred.

Committed dispatch/completion digest (mutable watchdog lines, copied):

```text
2026-11-04T16:50:57-03:00 launch mado round=85 pgid=2704703 driver=hyaku-inline attempt=1
2026-11-04T17:47:54-03:00 complete mado round=85; hyaku-inline attempt=1
```

## Claim re-checks: measurement versus evidence verification

### C1 coverage — improved, bounded finite predicate

**Evidence-verified** (never executed here): `W/w1/R85ReviewerC1.md:67` and
`W/receipts/independent-score-r85.txt` Run A both re-execute the frozen counter at `3905311c` and
print verbatim

```text
MADO_R85_IDENTITY: cases=72 correct=72 mutants=51 killed=51 base_correct=62/72 carried=61/61 tool_selftest=152/152 verdict=TARGET_MET rev=3905311c75a39c5710413105865c0a1a7dd0116a tool_sha256=d2eb4547…
```

**Re-measured here** by plain counts over committed bytes (no gate run):

```sh
jq '.cases|length' W/controls/c1-cases-r85.json            # 72
jq '.cases|length' .ufo/waves/round-84/controls/c1-cases-r84.json  # 61
grep -c 'correct=yes$' W/receipts/final-c1-r85.txt          # 72 of 72 case lines
grep -c 'killed=yes'   W/receipts/final-c1-r85.txt          # 51 of 51 mutant lines
grep -c 'correct=no'   W/receipts/control-c1-r85-base.txt   # 10 -> base 62/72
```

Observed: 72 case lines, 72 `correct=yes`; 51 mutant lines, 51 `killed=yes`; base control 62/72
with `MUTANTS_SKIPPED` (so the control claims no kill); `carried=61/61` and the r85 control's first
61 cases parse-equal the r84 control, 11 new names appended (verified with a JSON prefix compare).
Score arithmetic `10*62/72=8.6111 → 10*72/72=10.0000` reproduces the reported `+1.3889`.

Stability across revisions: the r85 controls are byte-identical at `3905311c`, `d7c40e6d` and
`b542d315` (`bacae37d…` C1, `de8a68fe…` C2). The only post-freeze C1 changes are a docstring
contract line in the counter (`3905311c`→`2b6dd76`) and `VERSION = "r84-v1"`→`"r85-v1"` in
`tools/mado-barfoot.py`; neither touches scoring, and both revisions score 72/72.

Bounded: nine of the ten `cause=` tokens are case-bound (`alloc-negative` is stage-only), the cause
test is stdout substring membership, and a flooding tool scores 72/72 cases while dying on 3/51
mutants (`W/w1/R85ReviewerC1.md:37,43`). This is refusal-edge coverage, not arbitrary-cause
authentication, geometry prediction or a protocol namespace law.

### C2 operability — unprovable as declared; honest stop

**Evidence-verified**: `W/receipts/independent-score-r85.txt` B1 runs the frozen counter at
`3905311c` and exits 2 with
`MADO_R85_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)`;
a clean frozen clone reproduces `ERROR (stage=setup carried case 'version' changes field 'negatives')`
(`W/w1/R85ReviewerC2.md:16`). The frozen instrument therefore executes zero cases and its 37/37
kill predicate cannot be evaluated — it fails, not passes.

**Re-measured here**: successor contract line in `W/receipts/final-c2-r85.txt` and a plain count
over the same file give `cases=36 executed=36 matched=36 … mutants=37 killed=33 verdict=TARGET_MISSED`,
exit 1, survivors `regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped`,
`samples-skipped`, each `matched=36/36`. The independent seat and the reviewer reproduce 33/37 at
`d7c40e6d` including a clean-clone replay. Before-state is 3 contained fixtures only
(`W/receipts/control-c2-r85-unguarded.txt`: unguarded 0/0/0, guarded 0/7/141), not a 36-row
baseline — the report says so.

Bounded: `128+N` is Bash's encoding (S489), not POSIX's (S488), and numeric 141 cannot separate
death-by-SIGPIPE from an explicit `exit 141`; Markdown status/outcome cells are unbound; the
declared mutant ancestry sentence ("nine removed") is arithmetically false — one (`rc-blind`) was
removed, 28 carried + 9 new = 37. All retained, none backdated.

## Harm watch

`git diff 5f174ca4 b542d315 -- SCORECARD.md` is 52 insertions, **0 deletions**: the round appends a
C1 improvement and an explicit C2 honest stop, with no other axis score rewritten and no capability
row added. Committed gate evidence, evidence-verified and not executed here:

| receipt | verdict line |
|---|---|
| `final-index-r85.txt` | `MADO_INDEX: … indexed=106/106 missing=0 dangling=0 duplicates=0`, exit0 |
| `final-ledger-r85.txt` | `LEDGER: population=156 ledger_rows=156 uncovered=0 … bad_pointer=0 verdict=TARGET_MET`, exit0 |
| `final-axis-r85.txt` | `MADO_AXIS: checked=3 mismatched=0`, exit0 |
| `final-gate-r85.txt` | `MADO_SELFTEST: 460/460 assertions passed`, exit0 |
| `final-c1/c2-selftest-r85.txt` | `119/119`, `106/106`, exit0 |
| `final-wave-r85.txt` | `MADO_WAVE_DONE: round=85 waves=1 settled=1 verdict=OK`, exit0 |

The freeze ledger red (uncovered 2 → 0, `W/receipts/harm-watch-r85.txt` block [2]) is a real repair,
not a claim of global absence of harm; inherited setup/symlink containment limits and the null wave
telemetry remain open.

## Per-axis verdicts

| axis | verdict | reason |
|---|---|---|
| coverage | improved | Frozen finite cause-bound witness 62/72 → 72/72 with 51/51 kills, base control and carried set re-counted here; bounded, not arbitrary-cause coverage. |
| operability | unprovable | Declared C2 predicate never evaluated at the freeze (setup rc2) and missed at the successor (33/37); the repaired successor is not retroactive. |
| depth | unchanged | No separate technical-depth claim this round. |
| freshness | unchanged | No live-surface re-verification claim; GNU endpoint stayed unreachable and is recorded as unreachable, not as absence. |
| calibration | unchanged | Publication corrections, the ancestry-error correction and the honest stop keep the published record honest; no numeric upgrade. |
| adjacency | unchanged | Connector keeps tsukuroi/tameshi/kumitate ownership; no sibling ground absorbed, no new geometry surface claimed. |

No owned axis is harmed; `unprovable` is not `harmed`. Failure of one declared claim still bars
round admission.

## Outside discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S488 pipeline exit status | admit | `W/fetch/S488.bin` bytes 133030–133104 (POSIX Issue8 §2.9.2, Exit Status table) | agree | Exact 12-word quote present verbatim: "The exit status of the last (rightmost) command specified in the pipeline." Scoped tierA, mined, used-by pointers resolve. |
| S488 second clause, signal status | admit (same row) | `W/fetch/S488.bin` bytes 109001–109128 | agree | Present as "…assign it an exit status\ngreater than 128." — 23 words after normalising the one newline. It grounds "greater than 128", never `128+N`. |
| S489 Bash 128+N | admit | `W/fetch/S489-alt-tiswww.bin` bytes 239046–239200 (Edition 5.3 §3.7.5) | agree | Present as "When a command terminates on a fatal signal whose number is `<var>N</var>`, Bash uses the value 128+`<var>N</var>` as the exit status." — markup stripped, 21 words. Maintainer copy, not the unreachable GNU URL, and the row says so. |
| S490 exit builtin as numeric-cause proof | reject | `W/fetch/S489-alt-tiswww.bin` bytes 266270–266361 (§4.1) | agree | Present: "Exit the shell, returning a status of `<var>n</var>` to the shell's parent." An explicit `exit 141` is indistinguishable from SIGPIPE death, so the reject reason and flip condition hold. |
| "POSIX grounds the `128+N` form" | reject | same S488 pin, signal span | agree | POSIX says only "greater than 128"; the literal encoding is Bash's. The declaration over-claimed and the correction is recorded, not silently dropped. |
| Declaration locators §2.9.3 / §3.7.6 | reject as citations | `W/fetch/S488.bin` byte 33656 → `2.9.2 Pipelines`, byte 110936 → `2.9.3 Lists`; `S489-alt-tiswww.bin` → `3.7.5 Exit Status`, `3.7.6 Signals` | agree | The declaration's section numbers are off by one in both documents; the registry rows cite 2.9.2 and 3.7.5, which is what the pinned bytes show. |

Required sample (≥1 admit, ≥1 reject) is satisfied twice over, and this judge disagrees with nothing
sampled. Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` →
exit 0, final line `mado ok …/corpus/SOURCES.md`, with the standing W04 duplicate-URL warnings
(including the new `S490` row) and W01 `S277` unfiltered.

Plain counts over `git show REV:corpus/SOURCES.md`: rows 422 → 425 (`^ {0,3}\|\s*S[0-9]{3,}\s*\|`);
tier A 404 → 407, B 10 → 10, C 8 → 8; mined 396 → 398, queued 10 → 10, rejected 16 → 17;
`git ls-tree -r --name-only REV corpus/knowledge` 104 → 106. Every reported census number
reproduces exactly. The two new notes open with `source:`/`verified-at:`/`recheck:`, cite mined
S486/S487/S488/S489, and are indexed at `R/corpus/README.md:12–13` with frontier line 138.

## Trend verdicts

- **expansion improved:** two admitted, sourced, indexed notes on ground the coverage map did not
  hold (cause-bound declaration identity; producer status classes) — knowledge 104→106 and rows
  422→425 counted here, each note citing a mined row. This is corpus expansion, not admission of the
  failed frozen C2.
- **quality improved:** the freeze's instrument-ledger red is repaired (uncovered 2→0, ledger
  156/156), QUALITY 140–142 land citing lesson 85, the `128+N` over-claim and both off-by-one
  locators are corrected rather than repeated, and the frozen failure is retained with survivors
  named. No sampled admitted fact was found false or left falsely advertised as verified.
- **discernment improved:** this independent closure agrees with two sampled admits and three
  sampled rejects, each re-opened at its pinned bytes; the r84 carry-in defect R1 (stage-only
  binding) becomes measured QUALITY 141 plus a repaired instrument. The lane's own report called
  discernment `unchanged` because the outside check was pending; it is performed here, so the
  closure grades `improved`.

## Routed defects — mado owns next-round correction

1. **R1, medium (carry-in, still open):** four declared C2 mutants survive because deleting a
   conjunct cannot lower an already-perfect 36/36 score, and the two anchor mutants survive because
   the frozen patterns already carry `^`/`$`. QUALITY 140 binds the invalid proof but supplies no
   detector; a new declaration needs an independently observable call/negative observation. Never
   widen the r85 frozen population after scoring.
2. **R2, medium:** the C1 cause test is stdout substring membership — an all-cause flooding tool
   scores 72/72 cases (48/51 kills), and `alloc-negative` is bound by stage only, so nine of ten
   tokens are case-bound. QUALITY 141 names the fix (parsed refusal record plus a negative
   observation); land it as a successor instrument with its own frozen controls.
3. **R3, medium:** numeric status cannot authenticate termination cause (QUALITY 142, S490 flip).
   Keep the `signal`/`exact` split declared and do not advertise unbound Markdown status/outcome
   cells as authenticated.
4. **R4, medium:** wave telemetry. All 13 raw seat outputs are null while
   `check-wave-done.py` returns `settled=1 verdict=OK`, so the gate cannot distinguish settled work
   from a lost handoff. The lesson's considerthese proposal 2 (published claim row vs red wave-done)
   is still unimplemented; bind the two and treat null outputs as missing telemetry, not settled.
5. **R5, low:** the append-only LOG correction for "old cells unchanged" **did** land
   (`R/LOG.md:4189–4197`), and it also corrects the false "nine removed" ancestry. Keep that
   correction pointer rather than restating the superseded sentence anywhere else.
6. **R6, low:** declaration source locators were off by one and the GNU endpoint was unreachable.
   Future declarations must cite the section numbers of the bytes actually opened, and an
   unreachable endpoint must stay recorded as unreachable (S489 does this correctly).
7. **R7, low:** two L1 probe directories were created directly under the shared scratch root
   (`W/receipts/cleanup-r85.json`). Keep lane scratch under the lane's own subtree; the defect is
   retained, not hidden.

## Operator notes and self-evaluation

All four `SHONEN.md` boxes look checkable by a dedicated non-author promotion review (cited
decision tables, a logged end-to-end contained replay, executable bounded instructions with the
known C2 defects explicit, and a scoped province). This closure grants no promotion and writes no
mark; promotion is operator-owned. No tool was installed or updated; no sibling repo, lane-authored
file, `[x]` mark, promotion or mint was touched by this judge.

Self-evaluation: accuracy 4 (gate verdicts are evidence-verified, not re-executed here; every count
and every quote was re-derived or re-opened); completeness 4 (conformance, both claims, harm watch,
spot-check, census, trends, routed defects); clarity 4 (frozen/successor separated; bounded claims
labelled); actionability 4 (seven routed items with paths and the QUALITY rows that bind them);
conciseness 3 (reproducible evidence lengthens the record). Mean 3.8/5. Main improvement: keep the
frozen-versus-successor distinction in the one-line handoff instead of restating the evidence.
