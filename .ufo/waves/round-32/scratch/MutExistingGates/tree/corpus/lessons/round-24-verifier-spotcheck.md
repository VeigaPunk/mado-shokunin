author: hyaku closure (non-author integrator, @m_opus)

# mado round 24 — non-author verifier spot-check (hyaku closure)

Reviewer: fresh hyaku closure subagent `HyakuCloseMado24`, dispatched by the hyaku orchestrator, not by the lane;
runtime model as exposed to the reviewer: `anthropic/claude-opus-5-5` (route `task` → `@m_opus`). I did not author or
steer any part of round 24. Six read-only seats re-checked in parallel (no model parameter passed, none died):
CloseNoHarm (reviewer), CloseC1PostDataCtl (critic), CloseC2Audit (critic), CloseTimingAudit (reviewer),
CloseSpotCheck (reviewer), CloseC1NoteAudit (reviewer); transcripts `history://HyakuCloseMado24.<seat>`. No lane
counter, gate or selftest was executed by me or any seat; counters are evidence-verified, plain counts re-measured.
No tools were installed or updated.

Inputs: report `.ufo/reports/round-24/mado.md` (fleet commit `17cb0923a24c28ce19b5b542b3edb6d999ae42c1`), prompt
`.ufo/prompts/mado-round-24.md` (fleet commit `35eaed2`), lane base `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`, lane tip
`b02cf2946373a5343ef86876e5688b3210849137` (claims measured at `eb14fa3d53d42c1568dd3fe2708c64eaf2024364`). Driver digest
(copied from `.ufo/watchdog.log:809,823`):

```
2026-10-23T00:01:53-03:00 launch mado round=24 pgid=1346361 driver=hyaku-inline attempt=1
2026-10-23T01:29:02-03:00 complete mado round=24; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report by lane identity | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-24/mado.md` | `mado-shokunin mado@shokunin.local 17cb0923… 2026-10-23 01:28:48 -0300` (after lane tip 01:28:02) | pass |
| SHONEN heading, one line per box | read report §SHONEN; `grep -c '^- \[' SHONEN.md` | 4 lines, all `[~]`, for 4 boxes; `SHONEN.md` byte-identical base→tip | pass (note: boxes 2–3 say "unchanged" without a resolvable pointer) |
| Cited lane commits exist, ancestors of `master` | `git rev-parse <h>^{commit}` + `git merge-base --is-ancestor <h> master` | 8efd00af d9fec1d3 4f21d995 c9b76646 464a0245 81955bd5 cf86f9e0 39c59630 87429be6 eb14fa3d b02cf294 (and base): all commits, all ancestors | pass |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain` | `state branch=master local=b02cf294… remote=b02cf294… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `b02cf294…` | pass |
| Range authorship | `git log --format='%h %an' 8e5d9369..b02cf294` | 11 `mado-shokunin` commits + `5bb2c87` (João Pedro Veiga, `considerthese/2026-10-22.md` +58, parent = base): operator commit, not round work | pass |
| Prompt carries template contract | `difflib` of `templates/round-prompt.md` vs prompt lines before `## 6.` | 34 diff lines, all `{{FLEET_ROOT}}/{{LANE}}/{{ROUND}}/{{AXES}}` substitutions; §1–§5 identical; §6 hyaku addendum appended | pass |
| Report sections in contract order | read report | Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, (Gate, Round shape), SHONEN | pass |
| Registration before data | per-commit times + `w1-record.json` `createdAt` | registration `8efd00af` 00:11:41; C2 counter/manifest `4f21d995` 00:31:24; C1 v2 `c9b76646` 00:33:39; wave-1 registry `createdAt` 00:35:33; first data landing `cf86f9e0` 01:03:16 | pass (see §2.3 wording defect) |

Status: real report with checkable commits → `ok`.

## 2. Claims (judged under prompt §6.9 against each frozen predicate)

### 2.1 C1 — coverage: rule-attribution route

Frozen predicate v2 (`registration.md:42-48`; counter `c1/count.py`, sha256:`b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66`,
blob identical at `c9b76646` and `b02cf294`). Target: PASS_ROW ≥ 6 from ≥ 3 distinct S### rows + README coverage-map row.

Re-measured by me over committed bytes:

```
$ git show b02cf294:corpus/knowledge/rule-attribution-r24.md | grep -cE '^\| *A[0-9]+ *\|'
26
$ git show eb14fa3d:corpus/knowledge/rule-attribution-r24.md | grep -oE '^\| *A[0-9]+ *\|[^|]*\| *S[0-9]+' | awk -F'|' '{print $4}' | sort | uniq -c
1 S153 1 S154 4 S155 2 S156 1 S157 2 S158 1 S159 2 S160 2 S162 1 S163 1 S164 4 S165 1 S166 1 S167 2 S168
$ git diff --quiet eb14fa3d b02cf294 -- corpus/ && echo same     →  same
$ git show 8e5d9369:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'   →  152 (tip: 168)
```

Evidence-verified (committed `evidence/c1-after-eb14fa3d.txt`): `rows=26 PASS_ROW=23 distinct_sources=14 readme_indexed=True
verdict=TARGET_MET counter_sha256=b2f37c57…`, exit 0; A5, A7, A8 `FAIL_ROW quote-off-topic`. Before
(`evidence/c1-before-v2-8e5d9369.txt`): PASS_ROW 0, note absent, exit 1. The reported before→after is reproduced.

§9 test — cheap control after data: **met**. Wave-2 seat AtkC1Coverage (`w2/reports/AtkC1Coverage.md:22-26,127-135`,
sandbox parent `39c59630`, i.e. after data landed at `cf86f9e0`) kept only the nine generic rows A1–A4, A17, A20,
A21, A25, A26 and deleted every attribution row and sweep: `PASS_ROW=9 distinct_sources=6 readme_indexed=True
verdict=TARGET_MET`. That result is forced by committed bytes: all nine rows are `PASS_ROW` in the tip receipt and
cite S153, S154, S155, S163, S165, S168 (six ids). Wave-1 seats RevRegistration (`w1/reports/RevRegistration.md:31-41`,
three generic wiki pages) and CritC1Predicate (`w1/reports/CritC1Predicate.md:121-131`, one 4,465 B page under three ids)
also reached `TARGET_MET` under v2. The lane records this as M24-2 (`corpus/lessons/round-24.md:16`), not fixed.

Non-author content read (CloseC1NoteAudit): all 26 row claims are supported by their pinned bytes; 12 of the 23 passing
rows carry attribution content (A6, A10–A16, A18, A22–A24), 11 are generic rule mechanics (A1–A4, A9, A17, A19–A21,
A25, A26), matching the author's 12/23. The note's central answer ("no channel maps an applied property back to its
rule", `:15`) rests on the explicitly uncounted sweeps (`:135-136`), and the tag-route's rule-tag application is not in
any counted quote (`w2/reports/AtkTagRoute.md:127-132`). A18's body (`:25`, "workspace-rule path") contradicts the
note's own errata (`:152-154`).

v1 → v2 timing (CloseTimingAudit; confirmed): v1 (`d9fec1d3`, sha256:`2fc366ab…2291`) was scored by control seats
CtlC1DoNothing (`controls/CtlC1DoNothing.md:14,32,63`) and CtlC1FabFetch (`controls/CtlC1FabFetch.md:21,31`) before v2
landed at `c9b76646` (00:33:39 −03); v2 landed 114 s before the wave-1 registry `createdAt` (00:35:33 −03) and before any
data landed (01:03:16). No counter, manifest or predicate byte changed after `c9b76646` (`c1/count.py` commits:
8efd00a, d9fec1d, c9b7664 only; `registration.md` after `c9b76646` only gains the additive receipts table at
`464a0245`). Nuance: the two controls that met v1 (CtlC1LabelShortcut, CtlC1OffTopic) scored at 00:36, after v2 had
already landed; v2 answered the designed control, not an observed score.

Verdict: **does not verify.** Under v2 (the declared counted rule) a cheap control that does none of the attribution
work meets the frozen target after data. Under the strict reading of §9 ("a rule changed after any seat has scored is
not the claim's rule"), v1 would be the rule, and v1 was met by two controls. Both readings fail. Axis
`coverage`: **unprovable** (real attribution rows exist, but the claim's frozen instrument cannot tell them from a
generic note).

### 2.2 C2 — calibration: capability table versus re-demonstration

Frozen predicate (`registration.md:61-64`, identical in `c2/count.py:4`, `c2/README.md:3`): "a capability named in a
SCORECARD.md capability table at REV …". Counter sha256:`a2809501…`, manifest sha256:`e02c76d1…`, single commit `4f21d995`
(before controls and data).

Evidence-verified: before `mismatches=1/12` (`c2/smoke/base-8e5d9369.txt`, `c2-stability-1/2.json` identical),
after `mismatches=0/12` (`evidence/c2-after-eb14fa3d.txt`, exit 0). The reported before→after is reproduced.

§9 test — cheap control after data: **met.** `c2/count.py:279` defaults `stated = "works"`, `:319` scores
`ok = in_population and stated == observed`. The landed status table (`SCORECARD.md:1575-1586`) equals the
counter's observed column (CloseC2Audit diff `equal: True, diff: {}` against the base smoke; observed column identical
at base, `81955bd5`, `eb14fa3d`). Wave-2 seat AtkC2Calibration (`w2/reports/AtkC2Calibration.md:44-51`) states it:
"the only input that moved 1/12 → 0/12 is the `stated` column, i.e. the table itself. The after-value is therefore
guaranteed by construction." A single appended row `| tripwire evidence marker | fails |` reaches 0/12; its content (H2,
L 15/18) was known before data (`registration.md:27`, repair 7).

Predicate vs counter: the counter reads only tables under `^#{2,3} Capabilities\b` (`c2/count.py:40`), 12 rows; the
predicate's wording names every capability table, 15 rows (`SCORECARD.md:437`, `:438`, `:782` uncounted). Under the
counter's own convention (no manifest command ⇒ `fails`), the literal population scores 3/15 at the tip; `:437`
("current exits 0") is stale — wave 2 observed `collisions=4`, exit 1 (`w2/reports/AtkC2Table.md:89-96`). The universal
clause is not enumerated by the counter (§9 claim sizing); the lane records it as M24-5. The round-20 over-claim row
(`SCORECARD.md:1342`, "L 17/18") is byte-identical base→tip: superseded by an appended row, with no pointer at the row.

Verdict: **does not verify.** The 0/12 is reached by transcribing the counter's own output, and the frozen predicate's
population is wider than the counter's. Axis `calibration`: **unprovable** (the honest `fails` row and the stale-row
scope note are real calibration information, but the claim's instrument cannot prove an improvement).

### 2.3 Chronology defect (status-neutral)

`registration.md` (at `464a0245`) heads its table "Control receipts (committed before any data seat)" and lesson 24
`:6` says "control receipts `464a0245`, all before any data seat". Receipts were committed 00:53:36 −03, about 18
minutes after the wave-1 data seats were created (00:35:33); two controls scored at 00:36, after wave 1 spawned. True only
as "before any data landed" (01:03:16).

## 3. No-harm check (base → tip)

| Check | Command / evidence | Observed |
|---|---|---|
| Removed lines anywhere | `git diff --numstat 8e5d9369 b02cf294` (CloseNoHarm) | 0 removed lines in 301 files |
| Production instruments | `git diff --quiet 8e5d9369 b02cf294 -- tools/` | exit 0 |
| PROVINCE, SHONEN, SKILL | `git diff --stat` | byte-identical |
| SCORECARD | `git diff 8e5d9369 b02cf294 -- SCORECARD.md` | +61/−0: two appended round-24 sections; no score row edited |
| r23 C3 = 0, r23 C2 = 3/3 | committed `w2/reports/AtkNoHarm.md` (evidence-verified, not run) | hold at `39c59630`; tools and corpora unchanged after |
| Sources census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (run by me) | 7 pre-round W04 lines (S030 S042 S045 S097 S119 S120 S121), `mado ok`, rc=0 |
| Operability | SCORECARD status row `tripwire evidence marker` = `fails` | the same mismatch is present at base (do-nothing 1/12): reported, not caused |

No axis harmed.

## 4. Discernment spot-check (sources re-opened by ordinary fetch, 2026-10-23)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S153 Engine.cpp | admit (`mined`) | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.cpp` | agree | sha256 `1ecb7afa…ddde6`, 1478 B = SOURCES row and `fetch/S153.bin`; quote at `:14`, 6 words, verbatim; A1 says exactly what it shows (CloseSpotCheck) |
| S165 window-rules.md | admit (`mined`) | `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md` | agree | sha256 `9ecff146…ed95`, 16200 B = row and `fetch/S165.bin`; quote at `:9`, 15 words; A19 matches `name?`/`match`/`effect` (CloseSpotCheck) |
| S168 rules `_index.md` | admit (`mined`) | `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/_index.md` | agree | re-opened by me: `curl -fsSL … \| sha256sum` = `46fee4dba2801e2bb5554df13cbabf1e6476dec948de180e88c687c1a307b789`, 953 B = row and `fetch/S168.bin`; quote "_All_ props must match for a rule to be applied." at `:16`, 10 words (`wc -w`), within anchor `:6-20` |
| S161 LuaBindingsQuery.cpp | reject → `queued` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/bindings/LuaBindingsQuery.cpp` | agree on decision, disagree on stated reason | sha256 `af0d274b…a66db`, 12451 B match; no note row cites it, and the file is a query filter, not attribution. But lesson `:58-59` says "its only quote cell contains `||`"; the committed quote (`query.className = …`, 15 words) has no `\|`; the `\|\|` was in a discarded wave-1 quote (CloseSpotCheck) |
| S149 span `:1013-1014` | reject (r23 closure span) | foot wiki blob `2475351…:Home.md` (fresh `git clone https://codeberg.org/dnkl/foot.wiki.git`) | agree | sha256 `78bd64dc…a5ff7`, 32739 B; "There is no way to dynamically reload the configuration." starts at `:1014` col 21 and ends on `:1015`; `:1013` contains none of it (CloseSpotCheck) |
| Generic rule-line rows (A1–A4, A9, A17, A19–A21, A25, A26) | admit as C1 counted rows | note at `b02cf294` vs pinned bytes | disagree (for the claim, not the corpus) | each row is true of its bytes, but they are not attribution content; counting them as frontier coverage is what lets a generic note meet the target (M24-2) |

## 5. Trend verdicts

- **expansion: unprovable-but-better.** A new entry on the round-12 frontier item, README-indexed, citing 15 `mined`
  rows that re-open intact; 12 counted rows are attribution content. But its universal negative rests on uncounted
  sweeps, the README frontier bullet remains open by the lane's own review, and the claim's counter cannot separate it
  from a generic note.
- **quality: improved.** Routed r23 defects 1–6 repaired and held on re-check (lesson 24 dispositions; S149
  span re-derived above); three unindexed notes re-indexed; the stale collision-screen row and the 17/18 over-claim are
  now marked in appended SCORECARD text; no admitted entry failed its re-check (A18 body error is marked by the
  note's own errata).
- **discernment: improved.** The spot-check agrees with the gate on 3 admits and 2 rejects; the one disagreement
  (S161's stated reason) and the counter weaknesses are routed below; QUALITY 33–35 cite M23-4/5/7 and their checks
  are shown red on round-23 bytes (`quality/m23-4-7-red-green.txt`, `quality/m23-5-red-green.txt`).

## 6. Closure verdict

| Axis | Verdict |
|---|---|
| coverage (C1) | unprovable |
| calibration (C2) | unprovable |
| operability | unchanged |
| depth | unchanged |
| freshness | unchanged |
| adjacency | unchanged |

Status `ok`. **Not admitted** (`rejected-honest-stop`): neither claim verifies under its frozen predicate, because a
cheap control meets each target after data; no axis is harmed. SHONEN boxes remain `[~]`; none looks fully
checkable by a non-author yet.

## 7. Routed defects (lane fixes next round)

1. C1 counter: re-cut before data so a generic or single-page rule note cannot meet it (M24-2); the claim anchor must
   require attribution content, not a rule-topic word.
2. C2 counter: the predicate's population must equal the counter's (all capability tables, 15 rows), and the target
   must not be met by transcribing the counter's observed column (M24-5).
3. `corpus/knowledge/rule-attribution-r24.md:25`: A18 body still says "workspace-rule path", contradicted by the
   note's errata `:152-154` (corrections sweep every mention).
4. `corpus/lessons/round-24.md:58-59`: S161 rationale ("only quote cell contains `||`") is false of the committed quote;
   append a correction.
5. `registration.md` / lesson 24 `:6`: "receipts committed before any data seat" is false (receipts 00:53:36, wave 1
   created 00:35:33); append a correction.
6. `SCORECARD.md:437` collision screen (stale, exit 1) and `:1342` (L 17/18): add pointers at the rows' sections to
   the round-24 correction, append-only.
7. Report SHONEN boxes 2–3 carry no resolvable evidence pointer; cite one or mark `[ ]`.
8. Carried: H2 (L0 `.ufo/l0-questions.md:103`) still open; QUALITY 33–35 check survivors (MutCheckRegOrder,
   MutCheckReceipt) still open.
