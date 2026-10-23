author: hyaku closure (non-author integrator, @m_opus)

# mado round 26 — non-author verifier spot-check (hyaku closure)

Reviewer: fresh hyaku closure subagent `HyakuCloseMado26`, dispatched by the hyaku orchestrator, not by the lane;
runtime model as exposed to the reviewer: `anthropic/claude-opus-5-5` (route `task` → `@m_opus`). I did not author or
steer any part of round 26. Five read-only reviewer seats re-checked in parallel (no model parameter passed, none died):
CloseC1Evidence, CloseC2Evidence, CloseHostSafety, CloseWaveAndPrompt, CloseGateRegistry; transcripts
`history://HyakuCloseMado26.<seat>`. No lane counter, harness, gate or self-test was executed by me or any seat, and no
Hyprland or compositor was started. Counters and gates are evidence-verified; plain counts and tool behaviour were
re-measured. I ran the landed tools (`git show` copies under `/tmp`) on the operator's own config tree and compared
with read-only `hyprctl … -j` queries against the live instance (pid 1614; `animations`, `binds`, `version`); that is a
read of the claimed artifacts against the real surface, not a gate run. No tools were installed or updated.

Inputs: report `.ufo/reports/round-26/mado.md` (fleet commit `b3f5d22559e116dec60a43c4aa144caf60ad42d9`), prompt
`.ufo/prompts/mado-round-26.md` (fleet commit `392d0bfb`), lane base `96101be523b2f6e897eee743d5b396b0225bf9ed`, lane tip
`14fcb814a4808527f93317d496fe5c87dbfc8036` (C1 measured at `2b3487f7`, C2 at `a496b02a`). Driver digest (copied from
`.ufo/watchdog.log:894,909`):

```
2026-10-23T05:20:09-03:00 launch mado round=26 pgid=916826 driver=hyaku-inline attempt=1
2026-10-23T07:03:22-03:00 complete mado round=26; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-26/mado.md` | `mado-shokunin <mado@shokunin.local> b3f5d225… 2026-10-23T07:02:57-03:00` (after lane tip 07:02:48) | pass |
| SHONEN heading, one line per box | read report §SHONEN | 4 lines, all `[~]`, each with a pointer; `git diff --stat 96101be5 14fcb814 -- SKILL.md SHONEN.md` empty | pass |
| Cited lane commits exist, ancestors of `master` | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> master` | 96101be5 05319e0f 1b0b91e9 2b3487f7 ca135237 a496b02a 178d3353 14fcb814: all commits, all ancestors (`d7835334` wlroots and `efb50993` Hyprland are upstream hashes, not lane hashes) | pass |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain` | `state branch=master local=14fcb814… remote=14fcb814… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | pass |
| Range authorship | `git log --format='%an %ae %cn' 96101be5..14fcb814 \| sort \| uniq -c` | `7 mado-shokunin mado@shokunin.local mado-shokunin` | pass |
| Prompt carries template contract | substituted diff of `kimi-shokunin/templates/round-prompt.md` vs prompt (CloseWaveAndPrompt) | 4 delta lines, only lane-name and `{{AXES}}` substitutions; §1–5 verbatim; §6 hyaku addendum present; L2 route map matches `MISSION.md:53-58` | pass |
| Seat counts | `git ls-tree` of `w1/reports`, `w2/reports`, `res/reports`; `w1-run.json`/`w2-run.json` counts | 40 + 34 seat reports (+ registries), 4 residual; run.json `spawn 40/total 40`, `spawn 34/total 34`; matches report (78, 0 dead, 1 cancelled) | pass |

Status: real report with checkable commits → `ok`.

Wave validation (M26-4, disclosed): the validator (`ufo-swarm-wave.mjs`) checks spec-side properties only (roles,
band, reportDir, prompt size, distinct names); `w1-run.json`/`w2-run.json` store the rendered `taskCall` and no digest
of sent text. The appended block is byte-identical to the operator's `~/.omp/agent/RULES.md` ("always on, every
agent"), which the host injects into dispatched task envelopes (this closure's own assignment carries it the same way).
**Ruling: wave validation stands.** Nothing the validator verified depends on the sent bytes; the delta is an
operator-mandated suffix, not lane-authored content. The §6.2 "taskCall unchanged" clause is byte-unsatisfiable under
host rule injection — a conformance defect of the clause, routed to the protocol lane (item 8 below), status-neutral.

## 2. Claims

### 2.1 C1 — coverage (sourced): `tools/mado-anims.py` + `corpus/knowledge/animation-table-r26.md`

Rule `PRED-C1-r26-v2` (`registration.md` "C1 redesign before data: counter v2"). Evidence-verified (counter not run):

```
$ git show 14fcb814:.ufo/waves/round-26/c1/count-v2.py | sha256sum   → 4ed70b5427f2…e836428 (= report 4ed70b54…6428)
$ git log --format='%h %cI' -- .ufo/waves/round-26/c1/count-v2.py      → only 1b0b91e 2026-10-23T06:16:22-03:00 (frozen pre-data)
$ git show 2b3487f7:tools/mado-anims.py | sha256sum                    → 2beda3f7…cab7d (= receipt tool sha; identical at 14fcb814)
$ git cat-file -e 96101be5:tools/mado-anims.py                         → absent (before receipt: tool=MISSING_TOOL, 41 CASE all FAIL, cases_pass=0/41, exit=1)
evidence/c1-after-v2-2b3487f7.txt: 41 `CASE ` lines, 41 PASS; `PRED-C1-r26-v2 cases_pass=41/41 verdict=TARGET_MET`;
  `ORACLE_VERSION commit=efb50993… tag=v0.56.2`; `HOST_SAFETY 1338→1338 delta=0`; `exit=0`
```

Controls (`controls/v2/*.txt`, 10 shapes, counter v2): DoNothing 0, EmptyTable 0, EmptyTableZeroNodes 0, Junk 0,
LabelKeyed 2, NaiveGrep 9, NoValidation 0, RootOnly 2, SnapshotCache 4, StaticDefault 0 — one seed each; w2 Rescore
fresh seeds: NaiveGrep 13 (max anywhere), RootOnly 3, SnapshotCache 2, LabelKeyed 1, rest 0. Chronology: controls
`1b0b91e9` 09:16:22Z < w2 registry `createdAt` 09:16:39.175Z < data `2b3487f7` 09:36:07Z.

Independent re-measure on the real surface (mine):

```
$ python3 -I /tmp/…/anims.py --home /home/vgpnk  (anims.py = git show 2b3487f7:tools/mado-anims.py, sha 2beda3f7…)  → exit 0, [35 nodes, 6 beziers]
$ hyprctl version -j → {"tag":"v0.56.2","commit":"efb50993…"};  hyprctl animations -j → [35 nodes, 6 beziers]
numeric comparison (floats rounded to 6 dp, multiset of entries): nodes 35/35 equal, beziers 6/6 equal
```

(Text-level diffs are number formatting only, e.g. `5.0` vs Hyprland's `5.00`.)

**M26-9 ruling (one seed per v2 control before data): conformance defect, status-neutral.** Registration
`:86` asks "two fresh seeds" per control; the pre-data v2 set had one. The seed clause serves the kill rule (a control
meeting target forces redesign); it is not an admission precondition the registration states. Every observed seed of
every shape missed by ≥28 cases (max 13/41 vs 41/41), the counter and tool bytes are pinned and pre-data, and the
w2 rescore seats could not inform the data seats' tools. The residual critic is right that post-data rescores cannot
repair the pre-data record; that is a process defect (routed, item 2), not evidence that a shortcut meets the counter.

Verdict: **coverage improved** — re-measured 0/41 → 41/41 (evidence-verified) plus an out-of-sample agreement with the
live Hyprland on the operator's tree (re-measured).

### 2.2 C2 — operability: `tools/mado-binds.py` evaluates hyprlang `{{…}}`

Rule `PRED-C2-r26`. Evidence-verified (counter not run):

```
$ git show 14fcb814:.ufo/waves/round-26/c2/count.py | sha256sum   → b92c32da…a716a8 (= report)
$ git show a496b02a:tools/mado-binds.py | sha256sum                → 01751e133eddb927… (= receipt tool sha)
evidence/c2-before-96101be5.txt: 51 CASE, 22 PASS (BASE + A11 + 20 V*), `cases_pass=22/51 … TARGET_MISSED`, exit=1
evidence/c2-after-a496b02a.txt:  51 CASE, 51 PASS, `PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET`, exit=0, HOST_SAFETY delta=0
round-25 V3 half (20 V* + BASE = 21): all PASS before and after
```

Independent re-measure on the real surface (mine):

```
$ python3 -I binds-r25.py --home /home/vgpnk ; python3 -I binds-r26.py --home /home/vgpnk   (git show 96101be5 / a496b02a copies)
  → both exit 0, 192 binds each; `diff` of sorted canonical JSON → 0 lines
$ hyprctl binds -j → 192; multiset of 18-field entries: tool(a496b02a) == Hyprland  → True
```

**M26-10 ruling (environment seeding removed): a disclosed trade inside the tool's scope, not an axis harm; claim
verified.** Facts: hyprlang v0.6.8 seeds variables from `environ` with env-first precedence (`fetch/SrcHyprlangExpr.bin`
`:543-556`, `:1073-1074`); round-25's tool mirrored it; `a496b02a` has no `environ` reference; CloseC2Evidence's /tmp
probe shows an env-using tree gives 3 binds (literal `$TERMINAL`, literal `$HOME/bin/ed`, `source = $HOME/extra.conf`
not followed) where the round-25 tool gave 4. Reasons it does not void C2 or harm operability: (1) the registered
no-harm scope is the 20-case V3 sample ("not an exhaustive no-harm proof", registration), and it holds 21/21; (2) the
change answers round-25 routed defect 6, which offered "fix or keep as a stated limit" for the env/`source` read
channel outside `--home` — the lane chose the fix and it closes that channel (probe: `$HOME/extra.conf` unread);
(3) the round-25 seeding read the *tool's* process environment, only a proxy for Hyprland's session environment;
(4) on the operator's real tree the round-25 and round-26 tools agree byte-for-byte and both equal live Hyprland.
Against it: the fidelity loss is undocumented — the tool docstring and PROVINCE row do not state that environment
`$NAME` stays literal, and PROVINCE's round-25 residual correction (`PROVINCE.md:36-39`, "it seeds config variables
from the whole process environment") is now stale for the tool at tip (routed, item 3).

Verdict: **operability improved** — re-measured 22/51 → 51/51 (evidence-verified) plus real-tree agreement (re-measured).

### 2.3 Host safety (orchestrator ask)

`HOST_SAFETY measurement-runs-touched-live=no` (CloseHostSafety). `harness/oracle.py` (sha `680798ed…e441`): `bwrap
--unshare-all --tmpfs /run --clearenv --dev-bind /dev/dri/renderD129 …`, private `XDG_RUNTIME_DIR`, no host
`/run/user`, no `card*`, no `WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE`. `evidence/isolation-probe.txt`: 288 nested
pids, 770/770 samples without `/run/user` or card nodes, live clients 2 and monitors 1 in 81/81 samples, live pid 1614
in every sample. `git grep HOST_SAFETY 14fcb814` over evidence/controls/res/harness: 66 hits, all `delta=0` (the two
`K2DoNothing-base-guard-run*` guard receipts print none; rc=1 before answering). Host: `coredumpctl list Hyprland` →
1338 total, 1330 before 08:20Z, 8 in the window: 05:22:34, 05:23:21, 05:25:26, 05:26:22, 05:27:47 −03 (five failed
pilots) and 06:32:14, 06:32:54 (SIGABRT), 06:36:06 (SIGSEGV) −03 (seat crash probes, M26-6), none after 07:05; live
Hyprland pid 1614 started 2026-10-22 04:55:44 −03, `hyprctl instances` shows only it; no user-journal warnings matching
hypr/wayland 08:00–10:10Z. Both after-receipts and both residual re-measures were launched `env -i PATH=/usr/bin
HOME=/home/vgpnk` (M26-5 mitigated for measurements); the two before-receipts record no `env -i` prefix (routed,
item 6).

### 2.4 Gates (§Gate standard, committed evidence only)

| gate | committed evidence | registry row in `SKILL.md` |
|---|---|---|
| `quality/counter-selftest.py` | green `SELFTEST pass=9 total=9 exit=0`; red receipts per mutant (`pass=7-8 total=9`, `RUN_EXIT=1`); w2 MutSelftest `killed=4 survived=6`; pins v1 `c1/count.py`, not the active v2 rule | no |
| `quality/check-population.py` (QUALITY 37) | 8 committed runs (green 0, 4 red 1, two base receipts 0, unreadable 2); w2 MutQ37 3/6 survive the committed fixtures | no |
| `quality/check-control-receipts.py` (Q36 successor) | `Q36MUTANTS killed=8/8`; on round 26 exits 1 (`no-receipt-under-…/controls/`, receipts are `.txt`; chronology itself holds by 17 s, w2 MutQ36) | no |

None is conformant under §Gate standard Delivery until its registry row exists (`git diff 96101be5 14fcb814 --
SKILL.md` empty). SCORECARD's "check-population … on both after-receipts → PASS" has no committed run (the red/green
file covers the base receipts only). Conformance defects, status-neutral, routed (items 4–5).

## 3. No-harm check (base → tip)

`git diff --numstat 96101be5 14fcb814 -- . ':!.ufo/waves'`: LOG +17, PROVINCE +1, SCORECARD +36/−0, QUALITY +4,
README +9, SOURCES +7/−2 (S158/S162 rows rewritten with only `used-by` extended; old→new logged in lesson § Gate),
`animation-table-r26.md` +100, `hyprctl-verification-layer.md` +6/−1 (the −1 is the missing final newline; an
append-only pointer), lesson +98, `tools/mado-anims.py` +503 (new), `tools/mado-binds.py` +438/−24 (C2). `SKILL.md`,
`SHONEN.md`: empty diff. Census `validate` (mine, 10:05Z): `mado ok`, exit 0, the same 7 pre-existing W04 (S030,
S042, S045, S097, S119, S120, S121); rows 172 → 177.

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1 (§2.1) |
| operability | improved | C2 (§2.2); M26-10 ruled a disclosed in-scope trade, real tree unchanged |
| depth | unchanged | `SKILL.md` unchanged; note and S173–S177 add sourced detail, unclaimed |
| freshness | unchanged | verification-layer pointer appended; live counts not re-captured; no claim |
| calibration | unchanged | errata appended (M26-3 fix cell, M26-9, M26-10); SCORECARD population sentence unbacked (routed) |
| adjacency | unchanged | `tools/` diff touches only `mado-anims.py` (new) and `mado-binds.py` |

No axis harmed.

## 4. Discernment spot-check (sources re-opened by ordinary fetch, 2026-10-23 10:05Z)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S175 Hyprland wiki Animations (new row) | admit (mined) | `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Animations.md` → 4023 B, sha256 `f30f6bf4…120b` = row | agree | quote "The animations are a tree. If an animation is unset, it will inherit its parent's values." verbatim at `:23-24` (16 words ≤ 25); grounds the inheritance the tool implements |
| S177 hyprutils AnimationConfig.cpp (new row) | admit (mined) | `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp` → 2354 B, sha256 `dbb5d50a…268e` = row | agree | quote `if (anim->pParentAnimation == PANIM && !anim->overridden) { // if a child isnt overridden, set the values of the parent` verbatim at `:63-64` (19 words) |
| S176 AnimationTree.cpp, S173 hyprlang config.cpp, S174 parse tests (new rows) | admit (mined) | pinned raw URLs → 3483 B `313ed201…`, 43049 B `fa1b6898…`, 26205 B `ffedaa5e…`, all = rows | agree | quotes verbatim at `:35`, `:630`, `:252` |
| Duplicate-URL rows for HyprCtl.cpp / legacy ConfigManager.cpp | reject (used-by extended on S158/S162) | both URLs re-fetched: 97582 B `798b7c6c…` (S158), 90963 B `9db68cf4…` (S162) = rows; `animationsRequest` at `HyprCtl.cpp:927`, registered `:2018`; `CConfigManager::handleBezier`/`handleAnimation` at `ConfigManager.cpp:1389`/`:1426`; census: same 7 W04 | agree | the URLs already have rows; a second row would add a W04 duplicate; the new line ranges lie outside the rows' anchor cells, so `used-by` is the only in-place change permitted |
| Counter v1 as C1's rule | reject (pre-data) | `c1/count.py` (v1) vs `c1/count-v2.py`; `controls/v2/K1SnapshotCache.txt` (4/41 under v2) | agree | v1's append-only population let a snapshot cache plus suffix reader score without reading the original bytes; v2 adds edit/delete and independent-tree cases and pins the oracle version — replaced before any data seat |

SOURCES row quote check: S175 and S177 (newly written rows) re-opened above; quotes verbatim, ≤ 25 words, located.
Census run by me: `mado ok`, exit 0.

## 5. Trend verdicts

- **expansion: improved.** New sourced note `corpus/knowledge/animation-table-r26.md` on ground the coverage map held
  only as `[INF]` (`hyprctl-verification-layer.md` animations row), citing mined rows S175–S177, S158, S162; five new
  tier-A rows (172 → 177); two capability rows (static animation-table resolver, isolated Hyprland oracle), the first
  re-confirmed against the live Hyprland here.
- **quality: unprovable-but-better.** Round-25 routed repairs landed with red/green evidence (label-free case paths,
  counter self-test, QUALITY 37, Q36 successor fixtures, `:1409`/`:1410` second derivations, R8 correction). Against:
  M26-10 fidelity trade, PROVINCE's now-stale env-seeding sentence, the Q36 successor red on round 26, three
  unregistered gates and surviving mutants. No admitted knowledge entry found false and left unmarked, so not `harmed`.
- **discernment: improved.** The outside spot-check agrees with the gate on 3 admit items (5 rows) and 2 rejects; a
  pre-data critic finding became counter v2 before data; residual-critic objections were recorded as errata rather than
  argued away.

## 6. Closure verdict

`lanes.mado = ok`; `admitted = true` (verdict `admitted`): C1 and C2 verify under their frozen rules and re-measure on
the live surface; M26-9 and M26-4 are status-neutral conformance defects; M26-10 is ruled an in-scope trade, not an axis
harm; no axis harmed; no measurement run touched the live session. SHONEN: four `[~]` boxes with pointers; box 3
("Executable without oral context") looks checkable by a non-author via `python3 -I tools/mado-anims.py --home DIR`
(run by this closure) — operator-owned promotion, not written here.

## 7. Routed defects (lane fixes next round)

1. M26-10: document in the `tools/mado-binds.py` docstring and PROVINCE that an environment `$NAME` stays literal and
   `source = $VAR` is not followed (unlike hyprlang); optionally restore seeding behind an explicit flag; add
   env-using cases to the next C2-family counter.
2. M26-9: a pre-data control receipt set is complete only with the registered seed count per control; teach the Q36
   successor to count seeds per control shape.
3. `PROVINCE.md:36-39` round-25 residual correction says the tool seeds from `os.environ`; append a round-26 correction
   (corrections sweep every mention).
4. Add `SKILL.md` registry rows for `counter-selftest.py`, `check-population.py`, `check-control-receipts.py` (name,
   gate|probe, entry command, verdict map, self-test, pinned path, write scope, owner); make the self-test pin the
   active v2 counter.
5. Q36 successor exits 1 on round 26 (`.txt` receipts): add a receipt-path option; land the w2 MutSelftest (6/10) and
   MutQ37 (3/6) survivor witnesses as committed fixtures (M26-8).
6. Commit the `check-population.py` runs on both after-receipts that SCORECARD cites, or correct the sentence; record
   the launcher environment on before-receipts as on after-receipts.
7. Successor harness: bwrap under `env -i` (M26-5); data seats must not feed known-crash inputs, and each seat reports
   its own coredump delta (M26-6).
8. Protocol lane (routed, not mado's): hyaku addendum §6.2 "taskCall unchanged" is byte-unsatisfiable under host
   `RULES.md` injection — carve out the operator suffix or have the validator emit a digest of the rendered text.
