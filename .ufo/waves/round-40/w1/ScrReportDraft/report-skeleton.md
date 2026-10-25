# mado — round 40 report (hyaku run 7, inline v2 wave w1, 64 seats)

<!-- SKELETON. Every `<<...>>` is an unfilled evidence slot; it names the artifact that must fill
     it. Nothing here is a verdict. Filled by the L1 after the wave lands. -->

Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, final lane hash
**`<<tip hash>>`** (`git ls-remote origin refs/heads/master` → `<<output>>`).
L1: `<<L1 seat id>>`. Freeze commit `5e7e88525cc539563de7746361b2650802e81809`; base
`9fc511ddce708327377161202f358ce37dc266ba` (lane tip at round start; registration.md header).

## Work performed

Declared claims (2), frozen in `.ufo/waves/round-40/registration.md` before any round-40 data:

- **C1 — operability (capability acquisition): the option table merges the running compositor.**
  `tools/mado-options.py` gains `--live` (one `hyprctl getoption -j KEY` per declared key through
  the compositor's own read verb), `--hyprctl PATH` and `--probe KEY` (extra live keys with no
  declarer → `live-default`). Native replies are compared in their native forms (`int`, `float`,
  `str`, `custom`, plus the text `no such option`), converted per hyprlang v0.6.8
  `configStringToInt`, Hyprland v0.56.2 gradient/gap/font-weight handlers; a gradient redeclared
  without an angle token inherits the previous declarer's angle. Exit 5 on a compositor failure
  naming the key; exit 2 for a hostile probe key; standard library only; no write.
  Predicate `PRED-C1-r40-v1` = docstring of `quality/counters/c1-r40-live.py`; target
  `fixtures=13/13 tool=present verdict=TARGET_MET`; base `0/13` (`receipts/c1-before-base.txt`).
- **C2 — coverage (sourced): the getoption native-forms ground is admitted.**
  `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` plus registry rows (held S162, S173
  re-opened; ≥2 new rows, one an own-work census receipt). Predicate `PRED-C2-r40-v1` = docstring
  of `quality/counters/c2-r40-forms-entry.py` (clauses a–h; clause h binds the own-work receipt to
  the committed tool sha256 and to two count lines the entry repeats verbatim). Target
  `admitted=1/1 verdict=TARGET_MET`; base `0/1` (`receipts/c2-before-base.txt`).

Work items:

- Freeze `5e7e885`: registration, both counters, both control harnesses and their receipts
  (`receipts/ctl-c1.txt`, `ctl-c2.txt`), base receipts (`c1-before-base.txt`,
  `c2-before-base.txt`, `selftest-base.txt`, `axis-base.txt`, `census-before.txt`), native capture
  (`c1/native-capture.jsonl`), reference control `c1/ctl-ref-tool.py.txt` (never delivered).
- Wave `w1` spec + dispatch committed at `e2b51d3` (64 seats); wave evidence
  `<<w1 evidence commit>>` (`w1/`, `w1-results.json` `<<path>>`).
- C1 tool data: `<<commit>>` — `tools/mado-options.py` `--live`/`--hyprctl`/`--probe` + selftest
  growth `<<n>>` (`<<receipt>>`); live host receipt `<<path>>` (70 keys, reported not scored per
  registration.md residual).
- C2 data: `<<commit>>` — entry, rows `<<new ids>>`, used-by extensions `<<ids>>`, README index
  row, lesson Gate.
- Records: lesson `corpus/lessons/round-40.md` (Gate, `<<M40-n>>`; D2 correction note appended
  per registration.md "Routed defects"), QUALITY criterion `<<n>>`, SCORECARD/LOG round-40
  sections `<<commit>>`.
- Inherited state: `<<nothing inherited / inherited round-39 tip 9fc511d>>` `<<evidence>>`.
- Swarm: one inline v2 wave `w1`, **64 seats** `<<role mix: table below>>`; dead seats `<<n>>`
  `<<names + last error text, w1-results.json>>`; residual call `<<n>>`; **round total 64**
  `<<receipt>>`.
- Planner seat (§3): `<<held by the L1 / validator verdict>>`.

### Seat-role mix (declared in `w1-spec.json`, commit `e2b51d3`; landed/dead slots to fill)

| Role | Declared | Landed reports | Dead (no report, no retained output) | Residual call |
|---|---|---|---|---|
| executor | 20 | `<<n>>` | `<<n>>` | `<<n>>` |
| scribe | 12 | `<<n>>` | `<<n>>` | `<<n>>` |
| reviewer | 8 | `<<n>>` | `<<n>>` | `<<n>>` |
| scout | 6 | `<<n>>` | `<<n>>` | `<<n>>` |
| connector | 5 | `<<n>>` | `<<n>>` | `<<n>>` |
| critic | 4 | `<<n>>` | `<<n>>` | `<<n>>` |
| mutation-tester | 4 | `<<n>>` | `<<n>>` | `<<n>>` |
| revenger | 2 | `<<n>>` | `<<n>>` | `<<n>>` |
| sentinel | 2 | `<<n>>` | `<<n>>` | `<<n>>` |
| simplifier | 1 | `<<n>>` | `<<n>>` | `<<n>>` |
| **total** | **64** | `<<n>>` | `<<n>>` | `<<n>>` |

Seat names per role (declared; evidence: `w1-spec.json` items):

- executor: ExecToolLive, ExecToolIndep, ExecOracleHlInt, ExecAllOptionsForms, ExecLiveCensus,
  ExecCaptureStable, ExecFetchComplexTypes, ExecFetchConfigMgr, ExecFetchHyprlang,
  ExecFetchK2Sources, ExecK2HostReads, ExecAssimIdGuard, ExecQuarantineSlice, ExecWatchdogTable,
  ExecScratchMirror, ExecHarmChecks, ExecMutBaseline, ExecHostSourceGraph, ExecStubFidelity,
  ExecHostCompose.
- scribe: ScrFormsEntryA, ScrFormsEntryB, ScrSourcesRowsForms, ScrLessonGate, ScrMistakes,
  ScrScorecard, ScrReadmeIndex, ScrSkillTable, ScrProvinceRow, ScrAssimK2, ScrConsidertheseLesson,
  ScrReportDraft.
- reviewer: RevC1Counter, RevC2Counter, RevFreezeOrder, RevModelVsSource, RevHostCensus,
  RevAngleClaim, RevSeparability, RevToolSafety.
- scout: ScoutOptionTypes, ScoutGetoptionHandler, ScoutHeldCoverage, ScoutK1K2Held, ScoutMergeRest,
  ScoutHyprctlDocs.
- connector: ConnCrossClaim, ConnSiblingOverlap, ConnEvidenceResolve, ConnSourcePatterns,
  ConnRunState.
- critic: CritC1Cheat, CritC2Cheat, CritGeneratorCoverage, CritClaimWording.
- mutation-tester: MutC1Controls, MutC2Controls, MutSelftestFixtures, MutAxisGates.
- revenger: RevengerGetoptionFormat, RevengerNaiveMismatch.
- sentinel: SentLiveVerbs, SentEvidenceLeak.
- simplifier: SimpMergeUnify.

## Landed changes

| Commit | Change | LOG entry |
|---|---|---|
| `5e7e88525cc539563de7746361b2650802e81809` | round-40 freeze: registration, C1/C2 counters, controls, base receipts, native capture | `<<LOG bullet>>` |
| `e2b51d3b3f79768282914d57c1fa32cc85dcb06a` | wave `w1` spec + dispatch (64 seats) | `<<LOG bullet>>` |
| `<<C1 data commit>>` | `tools/mado-options.py` `--live`/`--hyprctl`/`--probe` + receipts | `<<LOG bullet>>` |
| `<<C2 data commit>>` | C2 entry, registry rows, used-by, index row, lesson Gate | `<<LOG bullet>>` |
| `<<records commit>>` | lesson/QUALITY/SCORECARD/LOG + after receipts + `w1/` evidence | `<<LOG bullets>>` |

## Before → after measurements

- **C1** — `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r40-live.py --repo . --rev <rev>`
  Before (base `9fc511d`): `PRED-C1-r40-v1 clauses=a:1 b:0 g:1 k:0`, `fixtures=0/13 tool=present
  verdict=TARGET_MISSED`, exit 1 (`receipts/c1-before-base.txt`; base selftest `71/71`, clause b
  needs `k == n >= 79`).
  After (data `<<commit>>`, tip `<<commit>>`): `<<counter output line>>`, exit `<<n>>`
  (`<<receipts/c1-after-data.txt / c1-after-tip.txt>>`). Verdict: **`<<met | miss>>`** under
  `PRED-C1-r40-v1`.
- **C1 controls** (reachability + do-nothing, frozen in the same commit): base tool `0/13`
  `BASE-tool`; reference `c1/ctl-ref-tool.py.txt` `13/13` fixtures but `TARGET_MISSED` overall
  (clause b, 71 selftest); 16 mutants each `<13`; `CTL_C1: controls=18 correct=18/18`
  (`receipts/ctl-c1.txt`, harness `ctl/run-c1-controls.py`).
  Wave re-runs of the same harness: `<<w1 receipt>>`.
- **C2** — `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r40-forms-entry.py --repo . --rev <rev>`
  Before (base `9fc511d`): `clauses=a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 admitted=0`,
  `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-before-base.txt`).
  After (data `<<commit>>`, tip `<<commit>>`): `<<counter output line>>`, exit `<<n>>`
  (`<<receipts/c2-after-data.txt / c2-after-tip.txt>>`). Verdict: **`<<met | miss>>`** under
  `PRED-C2-r40-v1`; first-data-commit result, if different: `<<counter output>>`
  (`<<receipt>>`).
- **C2 controls:** 20 mutants each `0/1`; fabricated self-consistent control P `1/1` (declared
  residual); `CTL_C2: controls=21 correct=21/21` (`receipts/ctl-c2.txt`, harness
  `ctl/run-c2-controls.py`). Wave re-runs: `<<w1 receipt>>`.
- **Harm watch** at tip (registration.md "Harm watch"):
  - `bash tools/mado-verify.sh --selftest` → `<<MADO_SELFTEST line>>` (base `460/460`,
    `receipts/selftest-base.txt`; after `<<receipt>>`).
  - `python3 -I tools/mado-options.py --selftest` → `<<line>>` (n ≥ 79 required by C1 clause b).
  - `quality/check-index.py` → `<<indexed/missing/dangling/duplicates line>>` (baseline 56/56
    plus the C2 row; `<<receipt>>`).
  - `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `<<exit>>`
    (`<<receipt>>`).
  - `python3 -I quality/check-axis-scores.py` → `<<MADO_AXIS line>>` (`<<receipt>>`).
  - Write-boundary check: `<<no config tree / compositor state / sibling lane written: evidence>>`.

## Sources & frontier

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
- Round start (`receipts/census-before.txt`): `mado ok`, warnings W04 ×7 (S030, S042, S045, S097,
  S119, S120, S121) + W01 S277; exit 0.
- Round end (at `<<tip>>`): `<<identical / changed warning set>>`, `mado ok`, exit `<<n>>`
  (`<<receipt>>`).
- Rows `<<before>>` → `<<after>>` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`);
  added by tier: A `<<n>>`, B `<<n>>`, C `<<n>>` `<<ids>>`.
- Rows touched old→new: S162 `<<used-by diff>>`, S173 `<<used-by diff>>`, `<<new ids>>`
  `<<tier/locator>>`; `<<unchanged re-opened ids>>` (lesson Gate lists each).
- Frontier advanced: `<<one-sentence edge class moved, with the receipt that proves it>>`.
- Sourced claim: C2 cites `<<new row ids opened this round>>`.
- Mined mistakes: `<<M40-n + the fix and the evidence it fails before the fix>>`.
- **Assimilation: `<<n>>` theme(s)** `<<package, theme, amendment adopted, what was refused and
  why>>`; id-collision guard `<<reg count / staged count / collisions / guard proof>>`;
  quarantine slice `<<n>>` rows: `<<present / refused / unverifiable ids with reason>>`.
- **considerthese:** `2026-10-25.md` proposal 2 (count dead attempts and dirty closures from the
  watchdog digests, mined as a lesson table) → `<<lesson row / receipt>>`; round-39 planned item 1
  served by C1 `<<evidence>>`.

## Trend verdicts

- **expansion: `<<improved | flat | regressed>>`** — `<<new edge class + artifact + commit>>`.
- **quality: `<<improved | flat | regressed>>`** — `<<instrument strength (controls/mutants),
  counter defects found and fixed, disclosed misses>>`.
- **discernment: `<<improved | flat | regressed>>`** — `<<refused candidates with reasons and flip
  conditions, quarantine verdicts, rejected wave drafts>>`.

## SHONEN

One line per box of `SHONEN.md`; `[~]` carries a pointer, `[ ]` means no pointer this round.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — historical (`SHONEN.md:5`); round-40 pointer `<<artifact>>` `<<or [ ] with reason>>`.
- [~] At least one end-to-end domain task executed and logged in LOG.md — historical (`SHONEN.md:7`); round-40 pointer `<<LOG.md "Round 40" + live host receipt>>` `<<or [ ] with reason>>`.
- [~] Instructions executable by an agent without oral context — historical (`SHONEN.md:9`); round-40 pointer `<<tool --help/--selftest + seat reports>>` `<<or [ ] with reason>>`.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — historical (`SHONEN.md:11`); round-40 pointer `<<plane touched + PROVINCE.md line>>` `<<or [ ] with reason>>`.

Stale-lane: `<<respawn-per-round driver state / lane claim>>`.
Tool installs: `<<none | tool, version, channel, reason — per seat>>`.
Open L0 questions: `<<none | question, who must rule>>`.
