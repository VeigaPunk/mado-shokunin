author: hyaku closure (non-author integrator, @m_zfl)
# mado round 79 — non-author verifier spot-check (hyaku run 15, closure)

Scope: `.ufo/reports/round-79/mado.md` for lane round 79, base
`e4b153dfa4a67ca56f7ec65cb6639082451626a7`, landing tip
`2b3c9c6bad2e98569e7ecaa0689d2b85d3fe574a`. Nothing here is lane-authored: every count was
re-derived from committed bytes and every source re-opened by the integrator on 2026-11-04 (UTC).
Per the closure contract this pass verified the committed gate evidence (receipts, frozen
verdicts, measured revisions) and did **not** execute a sibling's counter or gate.

## 1. Conformance (PROTOCOL §Round-robin steps 1 and 4)

- **Report identity and ordering.** `.ufo/reports/round-79/mado.md` is committed as `1347eaf9`
  by `mado-shokunin <mado@shokunin.local>` at 2026-11-04 08:01:25-03:00, 275 lines, one file;
  it is on `origin/main` and `origin/master`. It lands after the lane tip `2b3c9c6b`
  (07:49:03-03:00) and before the driver's `complete` line (08:07:32-03:00).
- **SHONEN heading.** `## SHONEN` appears once, followed by four `[~]` lines with evidence
  pointers and zero `[x]` (`grep -c '^- \[x\]'` → 0). `SHONEN.md` is byte-unchanged from the
  base (`git diff --numstat e4b153df 2b3c9c6b -- SHONEN.md` → empty; four marks).
- **Cited commits.** The twelve commits in `e4b153df..2b3c9c6b` are all authored by
  `mado-shokunin`. Every commit hash cited in the report resolves (`git cat-file -t` → `commit`)
  and is an ancestor of `refs/heads/master` (`git merge-base --is-ancestor <h> master`):
  `5eb8f20f`, `03e76ee9`, `3b8af34c`, `d6be05ef`, `8696c4dd`, `cf5f09b9`, `c4e71f98`,
  `52178de1`, `89924c1e`, `999a4a3f`, `c5187d98`, `2b3c9c6b`. `9e274157…`, `50a18041…` and
  `c9aa1391…` are sha256 prefixes (tool, control set, frozen tool), not commits.
- **Lane push state.** `jj-lane.sh state` (read-only helper):
  `state branch=master local=2b3c9c6bad2e98569e7ecaa0689d2b85d3fe574a
  remote=2b3c9c6bad2e98569e7ecaa0689d2b85d3fe574a ahead=0 behind=0 head=detached tracked=0
  untracked=0`; `git status --porcelain` is empty. No uncommitted lane round work.
- **Prompt contract.** `.ufo/prompts/mado-round-79.md` (committed `a1d682e5`, 07:07:04-03:00,
  by `mado-shokunin`) carries the round-level items — MISSION/AXES binding (§1), L2 floor
  "at least 8 … ONE batched AgentSwarm call" (§3), commit-then-push (§5), push scope (§5), L0
  side channel (§5) — and the five child-lane items: report path/filename (§4), commit-before-
  report ("the report lands last and cites the pushed lane hash", §6.4), the `SHONEN` heading
  requirement (§6.4), the commit-hash citation rule (§6.4), and the lane write scope (§6.3).
  No model aliases are hardcoded; the prompt points at the route table, so no L2 route-map
  bucket mismatch is gradable.
- **Dispatch and wave.** Watchdog digest: `2026-11-04T07:08:06-03:00 launch mado round=79
  pgid=1511397 driver=hyaku-inline attempt=1` and `2026-11-04T08:07:32-03:00 complete mado
  round=79; hyaku-inline attempt=1` (matches the assignment digest). The wave has 14 items
  (`jq '.items|length' w1-spec.json` → 14), `counts.spawn=14` under policy `waveMinLanes=8`,
  `waveMaxLanes=16`; roles: 2 scout, 1 connector, 4 executor, 2 scribe, 2 reviewer, 1 critic,
  1 mutation-tester, 1 sentinel (attack share 5/14 = 35.7 %). `w1-results.json` carries 14
  results; 13 seats wrote a `.md`, and `R79ExecC1Tool/` has no `.md` (the disclosed partial
  seat), which the report names rather than backfills.
- **Defects (status-neutral, routed in §6).** (a) The C1 "after" cell of the Before→after
  table quotes `tool_selftest=44/44 … rc 0 at d6be05ef (receipts/measurement-final-r79.txt)`,
  but that receipt's committed bytes print `tool_selftest=50/50 … rev=999a4a3f`; 44/44 at
  `d6be05ef` is the R1 receipt `measurement-c1-r79-repair.txt`. The report's own header,
  LOG.md and SCORECARD all carry 50/50 at `999a4a3f`, and the claim's predicate is met at the
  final receipt, so this is a citation defect, not a claim failure. (b) The S467 rejection
  reason ("documents the line syntax only, not the static-plus-dynamic summation") overstates:
  the committed fetch says at `:183` "This does stack on top of the calculated reserved area
  (e.g. bars)". (c) LOG.md's round-79 entry says "Seven mined" while the lesson carries eight
  `## Mistakes` rows (M79-1…M79-8). (d) `fetch/S468.bin` and `fetch/S469.bin` are called
  "pinned as S468/S469" in the report but are absent from `fetch/sha256-r79.txt` (10 entries,
  9 distinct digests) and have no registry rows. None is a marker predicate and none changes
  the status.

## 2. Claim re-checks (re-derived by the integrator from committed bytes)

Per the closure contract the counters were **not executed**; each claim's structural facts were
re-derived with plain counts and its committed receipt verified against the measured revision.

### C1 — coverage: the static `addreserved` reserve composes with the bar's band

```sh
jq '.cases|length' .ufo/waves/round-79/controls/c1-cases-r79.json            # 23
jq '.cases|length' .ufo/waves/round-78/controls/c1-cases-r78.json            # 18
jq -S '.cases' .ufo/waves/round-78/controls/c1-cases-r78.json > a            # r78 set
jq -S '.cases[0:18]' .ufo/waves/round-79/controls/c1-cases-r79.json > b      # r79 prefix
diff -q a b                                                                  # identical
grep -cE '^\s+\("' quality/counters/c1-r79-reserve.py                        # 12 mutants
grep -nE '^(CASES|CARRIED|MUTANTS|BASE_EXPECT) =' quality/counters/c1-r79-reserve.py
#   CASES = 23, CARRIED = 18, MUTANTS = 12, BASE_EXPECT = 18
git show e4b153df:tools/mado-barfoot.py | sha256sum                          # 1bceb514…
git show 5eb8f20f:tools/mado-barfoot.py | sha256sum                          # c9aa1391…
git show 999a4a3f:tools/mado-barfoot.py | sha256sum                          # 9e274157…
sha256sum .ufo/waves/round-79/controls/c1-cases-r79.json                     # 108bde32…
```

Observed in `receipts/measurement-final-r79.txt` (measured rev `999a4a3f`):
`cases=23 correct=23 mutants=12 killed=12 base_correct=18/23 carried=18/18
tool_selftest=50/50 verdict=TARGET_MET rev=999a4a3f… tool_sha256=9e274157…`, exit 0. The
do-nothing control `receipts/control-c1-r79-at-base.txt` at `e4b153df` prints
`correct=18 mutants=12 killed=4 base_correct=18/23 tool_selftest=28/28 verdict=TARGET_MISSED`,
rc 1, `base_sha256=1bceb514…` — matching the base tool bytes I hashed. The frozen run
`receipts/measurement-c1-r79.txt` at `5eb8f20f` prints `23/23`, `killed=12`, `43/43` on tool
bytes `c9aa1391…`. The twelve mutant names in the counter (lines 49–84) match the twelve
receipt lines (`opposite-margin-dropped`, `horizontal-margin-leak`, `level-bottom-swap`,
`right-extent-flip`, `per-side-margin-dropped`, `negative-margin-accepted`,
`opposite-edge-wrong`, `static-dropped`, `static-order-swapped`, `static-first-wins`,
`static-box-unoffset`, `static-selector-ignored`). The measured tool and counter bytes are
unchanged from `999a4a3f` to the tip (`git diff --stat 999a4a3f 2b3c9c6b -- tools/mado-barfoot.py
quality/counters/c1-r79-reserve.py quality/counters/c2-r79-runbook.py SKILL.md` → empty), so
the receipt's revision describes the shipped instrument.
**Source ground re-opened** (committed pins, hashes equal to live URLs): `S465.bin:654`
`m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea);` inside `applyMonitorRuleSoft`
`:652-655`, and `:1772-1774` `logicalBoxMinusReserved()`; `S466.bin:43-51` `calculate()` starts
from `m_initialBottomRight/m_initialTopLeft` and adds every `m_dynamicReserved` entry;
`S303.bin:1331` writes the area into an existing same-selector rule, `:1341` falls through to
`add(parser.rule())`; `S469.bin:92-101` shows the parser holds only the selector. This is the
R1 fall-through the round repaired, and the frozen fixtures' expectations match the sources.
**Verdict: improved** (re-measured structurally; receipt evidence-verified).

### C2 — operability: per-row runbook bindings, refusals and the keybindings shape

```sh
jq '.cases|length' .ufo/waves/round-79/controls/c2-runbook-cases-r79.json     # 22
jq -r '.cases[].skill_anchor' … | sort -u | wc -l                             # 22 distinct
# row binding: each case's command (argv[2] for /bin/sh, else " ".join(argv))
# equals exactly one SKILL.md row command cell after `\|` unescaping; 22 rows parsed, 0 unbound
grep -nE '^(CASES|CARRIED|SHAPES|MUTANTS) =' quality/counters/c2-r79-runbook.py
#   CASES = 22, CARRIED = 17, SHAPES = 17, MUTANTS = 9
sha256sum .ufo/waves/round-79/controls/c2-runbook-cases-r79.json              # 50a18041…
ls .ufo/waves/round-79/fixtures/refuse-{mode,scale,layer-background,output-space}
#   each: config.json layers.json monitors.json
```

Observed in `receipts/measurement-final-r79.txt` (measured rev `999a4a3f`):
`MADO_R79_CONTROLS: sha256=50a18041… cases=22` (equals my hash of the committed set) then
`cases=22 executed=22 matched=22 shapes=17/17 anchors=22/22 rows=22/22 control_new=0/5
mutants=9 killed=9 verdict=TARGET_MET rev=999a4a3f tree=bound`, exit 0; all four `refuse-*`
rows are `rc=3` with distinct `stage=model` reasons, and `omarchy-menu-keybindings` is
`kind=lines_shape match=yes`. The frozen run `receipts/measurement-c2-r79.txt` at `5eb8f20f`
prints the same counts. The held r78 instrument exits 2 on the successor set
(`control set carries 22 cases, frozen target expects 17`); the base-rev control exits 2
(`SKILL.md in the working tree is not the measured revision's bytes`). The nine mutant names
in `receipts/measurement-final-r79.txt` match `MUTANTS = 9`. The live-probe rows are
host-dependent by construction and the report states this as a named limit rather than hiding
it; `matched` is the predicate, `control_all=15/22` an observation.
**Verdict: improved** (structurally re-derived; live receipt evidence-verified).

### Supporting measurements

- **SOURCES census.** `scripts/sources-census.sh validate --root … mado` exits 0 with the
  standing W04 duplicate-URL warnings and `W01 S277`; rows `grep -cE
  '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` 401 at base → 404 at tip; status histogram
  `mined=380 queued=10 rejected=14` (was mined 378/rejected 13); tier histogram
  `A=388 B=8 C=8` (was A 386/B 7); the four touched rows change only column 11 (`used-by`),
  checked cell-by-cell; S465/S466 carry the new entry in `used-by` as well (six mentions).
- **Index.** `corpus/knowledge/*.md` 97 → 98 and README index rows 97 → 98; the new row is
  `knowledge/bar-footprint-reserve-r79.md` (README:179).
- **Ledger.** `quality/tool-ledger.md` 142 → 144 rows; population at the tip (tools/ +
  quality/*.py + quality/counters/*.py) = 144, matching `LEDGER: population=144
  ledger_rows=144 uncovered=0` in `receipts/harm-watch-r79.txt`.
- **No deletions.** `git diff --diff-filter=D --name-only e4b153df 2b3c9c6b` is empty;
  SCORECARD +81/−0, QUALITY +12/−0, LOG +53/−0, PROVINCE +13/−0, README +2/−0; SKILL +38/−1
  (the r77 probe registry row replaced by the r79 generation, intended); SOURCES +8/−4 (the
  four `used-by` cells only, checked above).
- **Harm watch.** `receipts/harm-watch-r79.txt` at `52178de1`: gate 460/460, index 98/98,
  ledger 144/144, axis table 3/3 MATCH, session-material 291 findings with no round-79 path.
  `tools/mado-verify.sh`, `quality/landing-counters.sh`, `check-tool-ledger.py`,
  `check-axis-scores.py` and `check-index.py` keep identical blob ids at base and tip.
- **Fetch manifest.** `sha256sum -c fetch/sha256-r79.txt` → 10/10 OK, no self-entry; the two
  Parser files (S468/S469) are not in it (defect d).
- **Live re-open.** The pinned S465 and S466 URLs return HTTP 200 and their sha256 equal the
  committed pins (`9cf88e15…`, `0a52e145…`); the S467 wiki URL returns 404.

## 3. Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | improved | C1 models the static `addreserved` composition (23/23 vs held 18/23; 12/12 mutants killed; the r78 `NOT_MODELLED` limit moves to core); index 97/97 → 98/98; sources 401 → 404 |
| operability | improved | C2 binds and executes 22/22 rows on 22 distinct anchors, four committed refusals and one shape-bound row; held r78 instrument rc 2; 9/9 matcher mutants killed; base rev rc 2 |
| depth | unchanged | no depth claim this round; the new entry adds cited detail but carries the coverage claim, and no depth score moved |
| freshness | unchanged | S457–S460/S464 re-opened and re-fetched byte-identically, S303 from its committed pin, S462's pin reused with its 404 named; no freshness claim; the dormant freshness value stays operator-owned |
| calibration | unchanged | SHONEN stays 4×`[~]`, limits are named honestly (fixture-fingerprint counterexample, unpinned `band`/`expected`, fall-through not case-covered); the stale C1 after-cell is a report citation defect, not a calibration claim |
| adjacency | unchanged | PROVINCE adds one read-only input and no write surface; the connector found no sibling claiming the reserve/band ground or the C2-shaped runbook |

No axis is harmed: the harm-watch receipts are committed, the round diff has zero deletions,
the frozen instruments keep their blob ids, and both axes that moved did so with held controls.

## 4. Discernment spot-check (LEARNING.md §Discernment is checked from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S465 — Hyprland `src/output/Monitor.cpp` @ `efb5099` | admit (rule the claim rests on) | live pinned URL, HTTP 200; sha256 `9cf88e15…` equals `fetch/S465.bin`; quote `m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea);` at `:654` inside `applyMonitorRuleSoft` `:652-655`; `logicalBoxMinusReserved` at `:1772-1774` | **agree** | the quote is verbatim at the stated line, tier A is right for source code scoped to the 0.56.2 plane, and the entry's claim ("the applied rule's reserve becomes the static band; the layer plane starts from the reduced box") is exactly what `:654` and `:1773` say; 4 words, ≤25 |
| S466 — Hyprland `src/desktop/reserved/ReservedArea.cpp` @ `efb5099` | admit (rule the claim rests on) | live pinned URL, HTTP 200; sha256 `0a52e145…` equals `fetch/S466.bin`; quote `m_bottomRight += e.bottomRight;` at `:47-48` inside `calculate` `:43-51` | **agree** | `calculate()` starts from the static initial box and adds every dynamic entry — the summation the entry claims; tier A source, anchor exact, 5 words |
| S467 — Hyprland wiki Monitors page | reject | live `https://wiki.hypr.land/Configuring/Monitors/` → HTTP 404; committed copy `.ufo/waves/round-45/fetch/wiki-Monitors.md:179` has `monitor = name, addreserved, TOP, BOTTOM, LEFT, RIGHT`, and `:183` adds "This does stack on top of the calculated reserved area (e.g. bars)" | **agree with the decision; reason needs narrowing** | a dead live URL with no revision pin cannot ground a 0.56.2 claim, and tier B prose is not the arithmetic; but "documents the line syntax only" is false — line 183 does state the stacking in prose. The reject stands; the recorded reason must be corrected (routed) |

New-row quote length check: S465 4 words, S466 5 words, S467 9 words — all ≤25 and located.
The admit/reject decisions agree with the gate; the single disagreement is with S467's reason
text, and it is routed as a correction, not left unlearned.

## 5. Trend verdicts

- **expansion — improved.** One net-new admitted entry
  (`corpus/knowledge/bar-footprint-reserve-r79.md`) on ground the coverage map did not hold (the
  r78 entry named it `NOT_MODELLED`), `source:` citing S465/S466 opened this round plus four
  re-opened rows; index 97/97 → 98/98; census 401 → 404 rows.
- **quality — improved.** The weaker r78 limit is superseded by the stronger entry; the wave's
  source re-derivation exposed the `addreserved` fall-through and five more model classes,
  each repaired with a red/green pair (`repair-r79-c1-fallthrough.txt`,
  `repair-r79-c1-oldfixtures.txt`, `repair-r79-c1-model-r2.txt`); the fetch manifest's
  self-referential line is repaired and verifies 10/10; QUALITY 136 was added citing M79-3;
  no admitted entry fails its re-check. The stale after-cell and the S467 reason are record
  defects routed in §6, not admitted-entry failures.
- **discernment — improved.** The outside spot-check agrees with the gate on all three sampled
  decisions (admits S465/S466, reject S467), and every wave disagreement became a committed
  repair or a named limit (R1–R3, M79-5/M79-6/M79-7, the named limits). The S467 reason-text
  overstatement is the one remaining gap and is routed with a fix.

## 6. Routed defects (lane fixes next round)

1. **C1 after-cell citation (evidence).** The Before→after table quotes `tool_selftest=44/44`
   at `d6be05ef` while citing `receipts/measurement-final-r79.txt`; that receipt is `50/50` at
   `999a4a3f`, and 44/44 belongs to `measurement-c1-r79-repair.txt`. Correct in round 80's
   report as an erratum naming the superseded text (a filed report is not rewritten); the
   claim itself is unaffected.
2. **S467 rejection reason (discernment).** Narrow the reason to "dead live URL, no revision
   pin, tier-B prose only": the committed fetch states the stacking at `:183`, so "syntax
   only" is inaccurate. `SOURCES.md` rule 2 requires a new row whose `teaches` opens
   `supersedes S467 —` (append-only; the filed row is not rewritten).
3. **LOG.md count (record).** `## Round 79` says "Seven mined" while `corpus/lessons/round-79.md`
   carries eight `## Mistakes` rows (M79-1…M79-8). Append a correction entry (LOG is
   append-only).
4. **Unmanifested fetch files (evidence).** `fetch/S468.bin` and `fetch/S469.bin` are referenced
   as "pinned as S468/S469" but are absent from `fetch/sha256-r79.txt` and have no
   `SOURCES.md` rows; add them to the manifest or describe them as fetched-but-unmanifested,
   and avoid the `S###` names for files that are not registry rows.
5. **Partial seat (coverage).** `R79ExecC1Tool` settled without a written report (out.txt: 73
   OK / 0 FAIL against the pre-R2 tool); the report discloses it, and the evidence gap stays
   round-80 ground rather than being backfilled.
