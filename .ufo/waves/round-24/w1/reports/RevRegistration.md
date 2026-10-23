# RevRegistration — review of the round-24 registration (reviewer, wave 1)

Seat `MadoR24.RevRegistration`. I reviewed `.ufo/waves/round-24/registration.md` (as at lane tip `81955bd5`) against
fleet `.ufo/prompts/mado-round-24.md` §2 (:9-40) and §6.9 (:343-365), and against `AXES.md` (:26-38). I read the
round-24 counters, the manifest, the control receipts and the SCORECARD, and I ran the checks below. Lane tip when I
read it: `81955bd5f04878320b93e60246a146901cdfd2cf` (00:55:57 −03). That is one commit past the control-receipt
commit `464a0245` and holds the C2 status table. I made no lane edits other than this file. Sandbox work was confined to
`/fast/scratch/hyaku/mado-r24/revreg-ctl` (a clone) and `/fast/scratch/hyaku/mado-r24/revreg-tree` (a `git archive`
extract). No tools were installed or updated. No `lsp` device answers markdown, python or json review here, so
caller checks were done by literal reads and the commands below; no grep result is offered as semantic proof.

Verdict line: **registration not sound as written — 2 high, 5 medium, 6 low.** C1 and C2 are on distinct axes, causally
separable, and both pass the literal do-nothing test. But the C1 counter can be met without any attribution content
(demonstrated below), and the C2 predicate's population leaves out 3 of the 15 capabilities named in SCORECARD
capability tables.

## Question-by-question

| Question | Answer | Evidence |
|---|---|---|
| C1/C2 causally separable | yes, with one shared surface the registration does not name (finding M5) | C2's status table landed at `81955bd` with no C1 data committed. The C1 counter reads only SOURCES, README and the note (`c1/count.py:89-99`). C2's `sources registry` row runs the census over REV's SOURCES (`c2/manifest.json:7-17`) |
| Distinct axes | yes: coverage and calibration | `registration.md:31,54` |
| Lowest axis worked | yes | `python3 .ufo/waves/round-17/measure.py 8e5d9369…` → `c1: criteria 32, lesson_cited 23, score 7.1875`, which matches `registration.md:9-10` and `round-23/registration.md:47`. Operability is 166/175 (H2), coverage rubric V is 10.0 |
| Axis named by surface | C1 names its surface (README frontier `corpus/README.md:101` "Still open: rule *attribution*"), but its counter does not measure it (H1). C2 names its surface (SCORECARD capability tables), but its counter covers only part of it (H2) | below |
| Target out of a do-nothing control's reach | literal test passes: C1 do-nothing PASS_ROW 0, C2 do-nothing 1/12 (`registration.md:99,107`). The §6.9 test of the cheapest control that skips the claimed work fails for C1 (H1) and is untested for C2 (M1) | below |
| Universal clauses enumerated | no, four are not (H2, M3, L2, L1) | below |
| Routed defects 1-7 handled | 1 and 2 landed (`d9fec1d`). 3, 4, 5 and 6 are planned but not landed, even though C2 data has already landed (M4). 7 is correctly left open (`.ufo/l0-questions.md:103`) | table at end |

## HIGH

**H1. The C1 target can be met by generic Hyprland rule lines that contain no attribution content, which breaks §6.9 :352-356 and :361-365.**
I built a sandbox control. It adds three SOURCES rows pinned to hyprland-wiki `c66e8de2…`: `rules/workspace-rules.md`,
`rules/layer-rules.md` and `rules/window-rules.md`. Each row has a `sha256:` from `git show`, status `mined`, opened
`2026-10-23`, and used-by naming the note. It also adds seven claim rows that quote generic rule sentences
(workspace-rules :6, :9, :61; layer-rules :21 and the `-- Named layer rule` comment; window-rules :20, :24), each with a
claim that restates its quote. Every claim is true of its bytes and none overreaches. None says anything about which
rule produced an effect.
Command: `MADO_LANE=/fast/scratch/hyaku/mado-r24/revreg-ctl python3 -I .ufo/waves/round-24/c1/count.py 857967d7d9c4464bd829fe408a191cd0b9d5544c`
Output: `PASS_ROW=6 distinct_sources=3 readme_indexed=True verdict=TARGET_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66`, exit 0.
One row, A4, failed with `claim-not-anchored-to-quote`. The frozen counted v2 bytes were used, and the network re-fetch
was live.
Cause: `TOPIC_RE` (`c1/count.py:37`) accepts any `rule|tag|prop|match` sentence, and the predicate
(`registration.md:42-48`) has no clause about the attribution surface. The registration's own limit note
(`registration.md:112-115`) sends wave-2 reviewers to report *unsupported* rows only. The rows above are supported, so
that reviewer duty, as written, does not catch them.
Consequence: the C1 counted value cannot by itself show that the README frontier item moved. Under §6.9 :357-360 the
predicate cannot change now, because controls have scored and data seats are running. The honest options are:
(a) report C1's after-value together with a per-row, non-author verdict on whether each passing row is about
attribution, labelled as a judgment outside the counter; or (b) report that the counter does not separate attribution
from generic rule syntax and that the C1 coverage claim rests on that judgment. Either way, the closure should not read
`TARGET_MET` as evidence that the surface moved.

**H2. The C2 predicate and population leave out 3 of the 15 capabilities named in SCORECARD capability tables, so the sentence and the code do not match (§6.9 :346-347, :359-360).**
The registration says "SCORECARD's capability tables (rounds 12–21, 12 named capabilities)" (`registration.md:55`), and
its predicate counts "a capability named in a SCORECARD.md capability table" (`:61`). The code limits the population to
tables under headings that match `^#{2,3} Capabilities\b` (`c2/count.py:40`). Three AXES-shape repertoire rows, with
header `Capability | What it can now do | … | First-working round`, sit under other headings and are skipped:
- `SCORECARD.md:437` `source-fragment collision screen` (r13, under `### Sources and demonstrated repertoire` :425)
- `SCORECARD.md:438` `digest-pinned frozen regression` (r13, same heading)
- `SCORECARD.md:782` `finite declared-action classifier` (r16, under `### Demonstrated capability` :778)

My enumeration (a python scan of every table whose header begins `| Capability |`, compared with
`count.parse_scorecard`) found 15 distinct names against a counter population of 12. None of the three is in
`manifest.json`.
I re-demonstrated the missed rows on a `git archive` of `81955bd`:
- `MistakeFix.py --selftest` → `MISTAKE_FIX_SELFTEST: PASS 25/25`, exit 0.
- `python3 -I tools/mado-action-plan.py --selftest` → `SELFTEST_SUMMARY: 52/52 passed`, exit 0.
- `--frozen .ufo/waves/round-16/frozen` → `MADO_PLAN: frozen_match`, exit 0.
- `python3 .ufo/waves/round-13/frozen/verify.py` → `MADO_REGRESSION: PASS … killed=10/10`, `FROZEN_ID: frozen_match`.
- `verify.py --selftest` → `MADO_FROZEN_SELFTEST: 12/12 assertions passed`.

All three missed capabilities re-demonstrate, so there is no hidden mismatch. The defect is scope: `mismatches=0` will be read as "the SCORECARD capability
tables match observation", while the measured population is 12 of 15. The report must state that population, and the
registration's "12 named capabilities" should be corrected append-only.

## MEDIUM

**M1. The C2 after-state is a one-cell relabel of a failure known before the round, and the cheapest control for it was not registered.**
The only base mismatch is `tripwire evidence marker` (`c2/smoke/base-8e5d9369.txt`). Its cause is round-21 harm H2,
which has been open since round 21 (`.ufo/l0-questions.md:103`; spot-check §7.7). The status table that reaches the
target landed in `81955bd`, 2 minutes 21 seconds after the control receipts (`464a0245`, 00:53:36 → 00:55:57 −03).
Eleven of its twelve rows restate the implied `works`, and one says `fails`. A control that marks only the
H2-affected row `fails` without re-running anything uses the knowledge the lane already had and would score 0
[INFERENCE: these are the same statuses as `81955bd`; I did not run the C2 counter at `81955bd`]. The registered
controls (all-works, all-fails, deleted rows, shuffled, stubs) do not model this case.
The round's real calibration content is the frozen manifest (twelve commands written from each row's claim), not the
1 → 0 delta. The report should say so, and should not present 1 → 0 as twelve re-demonstrations moved by the round.

**M2. C2's observed status depends on more than the committed bytes at REV (§6.9 :344-345).**
Manifest rows read live state outside REV:
- the fleet working tree, through `{FLEET}/scripts/sources-census.sh` (`manifest.json:9`);
- a sibling working tree, through `{FLEET}/tameshi-shokunin/tools/mutate-and-run.sh` (`:47`). The inherited report
  `inherited/r23-post-close-ConnSibling.md:16,123-128` records that tameshi's working tree is dirty;
- the lane working copy, not REV, for `tw-precision.py` and `a2-guards.py`, which run as `{LANE}/…` with cwd `{LANE}`
  (`:94-95, :119-120, :132-133`);
- the network, through `landed-check.sh`'s `ls-remote` (`:82-90`).

A closure re-run can therefore differ from the lane's run without any lane commit changing. The report should give the
fleet, tameshi and lane-worktree state at measurement time (for example `git -C … rev-parse HEAD` plus
`status --porcelain` counts).

**M3. Controls were not run as registered, and the receipts do not carry the frozen predicate as claimed (§6.9 :359-360).**
- `registration.md:80` registers a "status table keyed on names with shuffled statuses" control. No receipt exists:
  `grep -il shuffl .ufo/waves/round-24/controls/*` returns nothing. The receipt table (`:97-111`) lists a no-reader-stub
  control (`C2NoReader.md`) in its place, without noting the substitution.
- `registration.md:37` and `:58` say the predicate is "identical in … every receipt". A whitespace-collapsed substring
  check finds the C1 v2 sentence in 4 of 7 C1 receipts (`C1Junk`, `C1QuoteSplice`, `CtlC1DoNothing`, `CtlC1FabFetch`). It
  is missing from `CtlC1LabelShortcut`, `CtlC1OffTopic` and `CtlC1Stale`, which include the two v1-target-meeting
  controls. The C2 sentence appears in 1 of 5 C2 receipts (`CtlC2DeleteRows`).

**M4. The repairs did not land before data, contrary to the registration's own rule.**
`registration.md:13-15` says "Non-claim repairs, landed before the claims' data". At `81955bd`, only defects 1 and 2
have landed (`d9fec1d`: `corpus/lessons/round-23.md` +8, `corpus/README.md` +5). The rest have not:
- defect 3: `corpus/QUALITY.md` is unchanged and no `corpus/lessons/round-24.md` exists (`ls corpus/lessons/`);
- defect 5: lesson 24 is absent;
- defect 6: `.ufo/waves/round-24/carry/` is absent;
- defect 4: no sweep has been run.

Meanwhile C2 data landed (`81955bd`) and C1 data seats are writing `fetch/w1/*.bin` (untracked). `81955bd` also cites
an evidence path that is not committed: `.ufo/waves/round-24/w1/reports/ScribeC2Evidence.md` (`git ls-files
--error-unmatch` fails).

**M5. The registration does not name a surface the two claims share.**
Causal separability holds in the AXES sense (`AXES.md:30-32`): C2 verified without C1 at `81955bd`, and the C1 counter
ignores SCORECARD. Still, C2's `sources registry` row runs the census (E11 resolves used-by paths on disk) over REV's
SOURCES (`manifest.json:7-17`), and C1 appends SOURCES rows whose used-by names the new note. A malformed C1 row would
therefore show up as a C1 failure and as a C2 mismatch. The no-harm census guard (`registration.md:88`) is a third
reading of the same defect. `registration.md:28` should say this, so that one defect is not charged against two claims.

## LOW

**L1. The defect-6 population is not enumerated.** `registration.md:24-25` says "the wave-2 regression fixtures". The
spot-check §7.6 (`round-23-verifier-spotcheck.md:150-152`) names five: AttackLateCell, ReClosureNeighbour,
AttackRecallRegress, AttackFrameScopes and AttackEscapeGate. The lane's own SCORECARD plan (`SCORECARD.md:1544-1546`)
names a different four: it adds CritClosureNeighbour and omits AttackLateCell and ReClosureNeighbour. All five
spot-check reports exist in `.ufo/waves/round-23/w2/reports/`. Name the five so that the carry manifest can be checked
against them.

**L2. The defect-4 universal clause has no sweep and is already false in committed round-24 files.** `registration.md:21-22`
says "every sha256 in round-24 files … carries a `sha256:` label". A sweep of 8–39-hex tokens that are neither labelled
nor git objects finds bare sha256 prefixes in the inherited files
`inherited/r23-post-close-ScribeProvinceScope.md:58,59,581` (`cd9da20c…`) and
`inherited/r23-post-close-ConnSibling.md:124` (`b173e3e5…`). Those are inherited bytes and cannot be edited. Narrow the
clause to round-24-authored files and publish the sweep command. The registration itself passes: all six hex tokens in
it are commits.

**L3. The v1 provenance is imprecise.** `registration.md:38` says "v1 (landed `d9fec1d3`)". v1 first landed in `8efd00a`
(counter sha256:`98da7344d071b79d…`). `d9fec1d` changed it (MADO_LANE override, `c1/count.py:29`; predicate unchanged)
and rewrote the committed before-receipt `evidence/c1-before-8e5d9369.txt` in place (counter_sha256 `98da7344…` →
`2fc366ab…`). The predicate did not change, but the receipt history was overwritten rather than appended.

**L4. Calibration moves outside the claim.** Repair 3 adds lesson-cited QUALITY criteria (`registration.md:19-20`). That
raises the same round-17 `c1` calibration counter used to pick the lowest axis (23/32 at base). The report must not
credit that rise to C2, which has its own counter.

**L5. C1's indexing check is looser than its wording.** `c1/count.py:160` accepts the
`| \`knowledge/rule-attribution-r24.md\`` row anywhere in `corpus/README.md`, not only inside the coverage map. My
sandbox row was appended at the end of the file and counted as `readme_indexed=True`.

**L6. The no-harm guard list is partial.** `registration.md:83-90` has no guard for the round-17 `c1`/`c2` readings or the
fleet-round-1 note-reachability counter (`SCORECARD.md:46,236`). The C1 note could break the latter if it is not uniquely
indexed. These are residual, not violations, because the registration does not claim the list is complete.

## Checks that passed

- **Anti-loop guard holds at `81955bd`.** `git diff --quiet 8e5d9369 81955bd -- tools/` exits 0, and numstat over
  SCORECARD, SOURCES, LOG, PROVINCE and README shows 0 removals.
- **Predicate text matches the counters.** The C1 v2 sentence is in both `registration.md` and `c1/count.py`. The C2
  sentence is in `registration.md`, `c2/count.py` and `c2/README.md`.
- **Counter hashes match the registration.** `c2/count.py` is sha256:`a280950195d6…` and `manifest.json` is
  sha256:`e02c76d1adb4…`, matching `registration.md:94`. `c1/count.py` is sha256:`b2f37c571455…`, which is v2 at
  `c9b76646`.
- **The v1 → v2 change is allowed.** It came after controls showed v1 met (CtlC1OffTopic and CtlC1LabelShortcut, both
  `TARGET_MET` under v1) and before any data seat. That is the §6.9 :354-356 "fix it before data" path, and the
  registration states it openly (`:37-40`, `:112`).

## Routed defects 1-7

| # | Registration line | Status at `81955bd` | Finding |
|---|---|---|---|
| 1 | :17 | landed `d9fec1d` (append-only correction in lesson 23) | ok |
| 2 | :18 | landed `d9fec1d` (README withdrawal pointer) | ok |
| 3 | :19-20 | not landed (QUALITY unchanged, no lesson 24); the "shown able to fail" design is right | M4, L4 |
| 4 | :21-22 | registration compliant; clause unenumerated and already false in inherited files | L2 |
| 5 | :23-24 | not landed; handling via lesson is correct (`CORPUS.md:116` allows in-place change only for `status`/`recheck`/`used-by`) | M4 |
| 6 | :25-26 | not landed (`carry/` absent); fixture set unnamed | M4, L1 |
| 7 | :27 | left open; `.ufo/l0-questions.md:103` is the open mado r23 H2 question; C2's status table records the H2-caused `fails` | ok |

## Residual risk and verification gaps

- I did not run the C2 counter at `81955bd`. M1's "would score 0" is an inference from statuses that match the smoke.
- H1 shows the counter can be met. Whether the lane's real C1 note will contain generic rows is for wave 2 to judge.
- The sandbox clone and the archive tree remain under `/fast/scratch/hyaku/mado-r24/revreg-*` as evidence.
  `pgrep -af 'revreg-tree|revreg-ctl'` finds no processes, and the regression workdir `/tmp/mado-verify-regression.qULeet`
  removed itself on PASS.
- Exit codes of the missed-capability re-runs, from two independent runs: `MistakeFix --selftest` 0;
  `round-13/frozen/verify.py` 0 (`frozen_match`, both runs); `verify.py --selftest` 0 (12/12, both runs);
  `mado-action-plan.py --selftest` 0 (52/52, both runs); `--frozen` 0 (`frozen_match`, both runs).

## Commands run (all read-only for the lane)

- `git -C mado-shokunin log/show/diff/ls-files` (see lines cited above).
- `scripts/hyaku/jj-lane.sh state` → `local=464a0245… ahead=0` at the start. The tip later moved to `81955bd` (L1 commit).
- `python3 .ufo/waves/round-17/measure.py 8e5d9369…` → `c1 23/32 7.1875`.
- Sandbox clone: `git clone --no-hardlinks` the lane into `/fast/scratch/hyaku/mado-r24/revreg-ctl`, check out
  `81955bd`, append the S901-S903 rows, the note and the README row, then `git -c user.name=ctl commit` (sandbox only),
  giving `6f8359e2…` (5 PASS, not met) and `857967d7…` (6 PASS, `TARGET_MET`). Each was scored with the frozen v2
  counter via `MADO_LANE`.
- `git archive 81955bd | tar -x` into `/fast/scratch/hyaku/mado-r24/revreg-tree`, then the r13/r16 capability pointers
  run under `ulimit -v 4 GiB` and `timeout`.
