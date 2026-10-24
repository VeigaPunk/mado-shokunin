author: hyaku closure (non-author integrator, @m_opus)

# mado round 25 — non-author verifier spot-check (hyaku closure)

Reviewer: fresh hyaku closure subagent `HyakuCloseMado25`, dispatched by the hyaku orchestrator, not by the lane;
runtime model as exposed to the reviewer: `anthropic/claude-opus-5-5` (route `task` → `@m_opus`). I did not author or
steer any part of round 25. Five read-only seats re-checked in parallel (no model parameter passed, none died):
R25Chrono (reviewer), R25ToolProbe (reviewer), R25Mutants (critic), R25C2Facts (reviewer), R25RepairsHarm (reviewer);
transcripts `history://HyakuCloseMado25.<seat>`. No lane counter, gate or selftest was executed by me or any seat
(`c1/count.py` starts nested Hyprland on the live session); counters are evidence-verified, plain counts re-measured.
R25ToolProbe ran the landed tool (a `git show ef94763c:tools/mado-binds.py` copy) on five synthetic trees under `/tmp`;
that is a read of the claimed artifact, not a gate run. No tools were installed or updated.

Inputs: report `.ufo/reports/round-25/mado.md` (fleet commit `db62c5d7b83ec8d55a132b8f55fd440a3c605518`), prompt
`.ufo/prompts/mado-round-25.md`, lane base `41cc04c8d593837a0d5078bffaacdaa163d12897`, lane tip
`16e57dac26cb97e36e44a3b0552d1e4c27479dfc` (C1 measured at `ef94763c6a75d1b0860091b19bb61c9bd7cda9e3`). Driver digest
(copied from `.ufo/watchdog.log`):

```
2026-10-23T01:45:27-03:00 launch mado round=25 pgid=2452123 driver=hyaku-inline attempt=1
2026-10-23T02:26:41-03:00 lane-dead-no-report mado round=25; retry same round (hyaku-inline attempt=1: L1 died with the orchestrator process exit at 05:25:25Z (attempt 1; landed commits kept, uncommitted files untrusted))
2026-10-23T02:26:43-03:00 launch mado round=25 pgid=2559426 driver=hyaku-inline attempt=2
2026-10-23T03:40:30-03:00 lane-dead-no-report mado round=25; retry same round (hyaku-inline attempt=2: L1 died with the orchestrator process (omp SIGSEGV) at 06:19:06Z (attempt 2; landed commits kept, uncommitted files untrusted))
2026-10-23T03:40:32-03:00 launch mado round=25 pgid=3138821 driver=hyaku-inline attempt=3
2026-10-23T05:07:05-03:00 complete mado round=25; hyaku-inline attempt=3
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-25/mado.md` | `mado-shokunin <mado@shokunin.local> db62c5d7… 2026-10-23T05:06:40-03:00` (after lane tip 05:05:58) | pass |
| SHONEN heading, one line per box | read report §SHONEN | 4 lines, all `[~]`, each with a resolvable pointer (R7 closed); `git diff --stat 41cc04c8 16e57dac -- SHONEN.md SKILL.md` empty | pass |
| Cited lane commits exist, ancestors of `master` | `git cat-file -t <h>` + `git merge-base --is-ancestor <h> master` | 41cc04c8 04051723 7228299d a258c6ae 1ed41fa8 2896dc4a 459dd17f fa466833 ef94763c 90224671 16e57dac: all `commit`, all ancestors (`db62c5d7` is the fleet report commit, not a lane hash) | pass |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain \| wc -l`; `git ls-remote origin refs/heads/master` | `state branch=master local=16e57dac… remote=16e57dac… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain `0`; remote `16e57dac…` | pass |
| Range authorship | `git log --format='%h %an' 41cc04c8..16e57dac` | 10 `mado-shokunin` commits, no foreign commit | pass |
| Prompt carries template contract | `difflib` of `kimi-shokunin/templates/round-prompt.md` (140 lines) vs prompt lines before `## 6.` | 22 diff lines, all `{{FLEET_ROOT}}/{{LANE}}/{{ROUND}}/{{AXES}}` substitutions; §1–§5 identical; §6 hyaku addendum appended | pass |
| Report sections in contract order | read report | Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, (Gate, Round shape), SHONEN | pass |

Status: real report with checkable commits → `ok`.

## 2. Claims

### 2.1 C1 — operability, capability acquisition (sourced): `tools/mado-binds.py`

Frozen predicate `PRED-C1 (v4)` (`registration.md` "Attempt 3", landed `1ed41fa8` 06:50:06Z): the tool, in a bubblewrap
sandbox, reproduces over all 18 `hyprctl binds -j` fields the bind multiset a nested Hyprland v0.56.2 builds from the
same tree, for the unperturbed snapshot plus 40 generated cases (4 × ADD, UNBIND, VARIABLE, SOURCE, GLOB, UNSOURCED,
COMMENT, REWRITE, SYNTH, HARD), and the tool bytes contain none of the live capture's ≥12-char arg/description strings;
target `cases_pass=41/41 embed_hits=0`. Kill rule: one measurement run, any non-`TARGET_MET` a miss.

Re-measured by me / seats over committed bytes:

```
$ git cat-file -e 41cc04c8:tools/mado-binds.py   → fatal: path 'tools/mado-binds.py' exists on disk, but not in '41cc04c8'
$ git show REV:.ufo/waves/round-25/c1/count.py | sha256sum   (REV = 1ed41fa8, 459dd17f, ef94763c, 16e57dac)
  → 323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 at all four (count-v3.py 8532d3e9…8375 at all four)
$ git show {ef94763c,16e57dac}:tools/mado-binds.py | sha256sum → 9efa1136…2950 both (= receipt's tool sha)
$ git log 459dd17f..16e57dac -- .ufo/waves/round-25/controls/v4/  → empty
```

Evidence-verified (`evidence/c1-after-v4-ef94763c.txt`, committed `90224671`): counter sha `323a3849…`,
`rev=ef94763c…`, seed `ed0d8a943980d2f2`, `ORACLE_CHECK base_vs_live missing=0 extra=0`, 41 × `CASE … PASS missing=0
extra=0`, `PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET`, `exit=0`. Before
(`evidence/c1-before-v4-41cc04c8.txt`): `tool=MISSING_TOOL`, `cases_pass=0/41 … TARGET_MISSED` (the file carries no
`exit=` line; minor). The reported 0/41 → 41/41 is reproduced from receipts whose hashes match the frozen counter.

Order (R25Chrono, verdict `ordered`): counter v4 `1ed41fa8` 06:50:06Z → a3w1 registry `createdAt` 06:52:29Z → 10
control receipts `459dd17f` 07:29:16Z → registration note `fa466833` 07:31:13Z → a3w2 registry `createdAt` 07:31:20Z
(first data seats ExecBindToolA/B) → tool `ef94763c` 07:46:37Z → measurement 07:46:44Z. At `459dd17f`, `git ls-tree`
shows no `a3w2/` path and no `tools/mado-binds.py`. Only later edit of `registration.md` is `fa466833` (pre-data:
disclosed weaknesses, crash-run classification); no post-data change of target or rule. Controls under v4: K4DoNothing,
K4Echo, K4EmptyArray, K4GrepAll, K4Junk, K4NoReader, K4ShellOut 0/41; K4EasyOnly 4/41; K4EncodedTable 31/41;
K4LabelKeyed 37/41 — none `TARGET_MET`. Gap: data-seat spawn time is bounded only by the registry `createdAt`
(dispatch files carry no wall-clock); some controls recorded 2–5 scored runs, all misses, none amended.

Weaknesses weighed:

- **Case identity via `/proc/self/mountinfo` (M25-2).** Real counter defect, disclosed pre-data at `fa466833`. Not
  exploited: the tool imports only `glob, json, os, stat, sys`, never opens `/proc`, has zero hits for any case label
  (`BASE…HARD-3`) or operator strings (`XF86|omarchy|foot|wpctl|tiling-v2|192`); every entry is built by
  `handle_bind`/`handle_unbind` from parsed bytes (R25ToolProbe). The best label-keyed shortcut stops at 37/41 because
  HARD trees need the grammar. Material, disclosed, not fatal.
- **Surviving counter mutants.** `skip-oracle-check` removes a drift-eligibility guard, not the per-case oracle
  comparison; `embed-threshold-1000` survives because both tested tools already had 0 hits at ≥12. Neither lets a
  non-resolving tool pass (R25Mutants: minor coverage gaps; route a drift-fault witness).
- **Split literal `"resize" "windowpixel"`** (`mado-binds.py:54`): joins to a registered Hyprland dispatcher name
  (sibling `movewindowpixel` is spelled whole). The embed scan reads live arg/description strings; a dispatcher table
  is grammar, not operator data. It still shows `embed_hits=0` is a plaintext audit, not provenance proof. Low.
- **Literal `{{…}}`** (ResC1Remeasure 9/10 hand-made trees; R25ToolProbe `{{1+1}}` stays literal) and **reads outside
  `--home`** (absolute/`$VAR` `source =`, `os.environ` seeding; R25ToolProbe reproduced an out-of-home read on a /tmp
  file). Both are scope limits outside the finite predicate, both disclosed (lesson, SCORECARD, `PROVINCE.md:35-38`).
  Inside the counter's `bwrap --clearenv` sandbox the env channel sees only PATH/HOME.
- Corroboration: two independent implementations (A landed, B scratch) each 41/41 on three fresh seeds; ResC1Remeasure
  41/41 on seed `5aec873104392f2d`; ResToolAblation 8/8 feature-ablation mutants killed (permissive / canonical-modifier
  ablations pass 37/41 and fail every HARD case). R25ToolProbe's five synthetic trees gave the 18-field shape with
  correct variable expansion, `##` handling, `bindn`/`bindl` flags and ordered unbind.

Verdict C1: **verifies — operability `improved`** (re-measured: tool absence at base, counter/tool hash freeze, control
order; evidence-verified: the v4 receipt). Capability row `static bind-table resolver` (SCORECARD "Capabilities
(round 25)") has a passing demonstration in the round report.

### 2.2 C2 — calibration, exploratory: `## Current state (round 25)` ledger

`RevC2Judgment` was dispatched by the lane's L1 (a3res residual call): it is the lane, not a non-author reviewer.
I re-judge as the named non-author reviewer.

Facts (R25C2Facts, over committed bytes):

- Population: the base blob holds 15 data rows in 9 `Capability` tables (`:308-311`, `:437-438`, `:782`, `:919`,
  `:1020`, `:1158`, `:1342-1343`, `:1409-1410`, `:1464`; `:202` placeholder only) plus the 12-row round-24 status
  table `:1575-1586` — exactly the ledger's population.
- Rows `:309`, `:437`, `:1020`, `:1342`, `:1409` compared with `a3w1/reports/Cap*.md` and `a3w2/reports/Rc*.md`: all
  agree (e.g. `:1342` base `P 66/66, L 15/18`; `:437` `collisions=4`, exit 1; `:1020` `frozen_verdict_mismatch` exit 1).
- Prior state: the round-24 table covered 12/15 identities, transcribed at `8e5d9369` with placeholder counters, and
  ran `:309` `--no-live` only.
- M25-5: `git diff 90224671 16e57dac -- SCORECARD.md` has one in-ledger hunk — the receipt sentence changed from "a
  wave-a3w2 reviewer seat" to "wave a3w2 for 14 rows, the residual call for `:311`; all 15 re-checks agree". Both are
  false (a3w2 holds exactly 12 `Rc*` files; `:311` by `RcMutationRegression311`; `:1409`/`:1410` have one run each →
  13/15 re-derived). No ledger row changed; the F1–F5 errata are a pure append. Errata F1–F5 all verified (F3: +5 and
  +4 inserted lines → shift 9).

Ruling: **`unprovable-but-better`.** Reasons: (1) for the first time one present-tense place enumerates every
capability identity the SCORECARD names, at a single stated base, with a fresh run, a runnable command and a "governs
now" pointer; (2) it records mismatches between the SCORECARD's self-assessment and observed state — `:437` and `:1342`
fail as stated, `:310`/`:308` stale counts, `:919` command not runnable as written, `:1343` placeholder, `:1020` exits 1
by design — which is the calibration move itself; (3) it exercises `:309`'s live arm, which the prior table never did;
(4) the five sampled rows agree with their receipts. Against it: the receipt sentence was false as first written and
false again after an edit made while the lane's reviewer was reading (M25-5); `:1409`/`:1410` lack a second derivation;
the `:308` command is not lane-relative (F2). These are preamble/cell defects, each corrected by an append-only errata
before closure, none flipping a row's status. Not countable as a score move, so not `improved`.

### 2.3 Routed repairs from round 24 (repairs, not claims)

R1 closed (QUALITY 36, `quality/check-control-receipts.py`, red on round 24 / green on round 25 — committed outputs read,
checker not run); **R2 open** (population-equality clause not encoded, M25-4); R3 A18 in-row correction + errata;
R4 S161 correction; R5 append-only chronology corrections; R6 SCORECARD pointers (insertions, 0 deletions); R7 report
box pointers. R8: H2 correctly held open, but `registration.md:85` disposition says "Hardened checks for the named
survivors (MutCheckRegOrder, MutCheckReceipt) under `round-25/quality/`" — that directory holds only the Q36 checker and
its two outputs; the lesson ("were not hardened this round") and report ("Hold … QUALITY 33–35 survivors open") state
the truth, the registration line was never corrected. Low truthfulness defect, routed.

## 3. No-harm check (base → tip)

`git diff 41cc04c8 16e57dac -- SCORECARD.md`: 94 insertions, 0 deletions (two R6 pointer paragraphs, the ledger, the
results section, capabilities row, C2 errata). Across LOG, PROVINCE, QUALITY, README, SOURCES, lessons, round-24
registration and `rule-attribution-r24.md`: 3 deletions only — the declared A18 in-row correction (R3) and the S162/S167
rows re-written with only `used-by` extended (every other cell byte-identical), old→new logged in lesson § Gate.
`SKILL.md`, `SHONEN.md`: empty diff. Census `validate` exit 0, same 7 pre-existing W04 at start and end; rows 168 → 172.

Round-23 C3 tool-inventory counter blip: at `ef94763c` `tools/mado-binds.py` exists with no PROVINCE row (count 1); the
row lands at `90224671` (count 0) and stays at tip. A 3m13s intermediate state caused by the lane's own pre-declared
"row only if C1 lands" order, disclosed in SCORECARD; not a harm at the tip.

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 (§2.1) |
| calibration | unprovable-but-better | C2, non-author ruling (§2.2) |
| coverage | unchanged | frontier note and README route added, no coverage claim; nothing removed |
| depth | unchanged | `SKILL.md` unchanged; note + S169–S172 add sourced detail, unclaimed |
| freshness | unchanged | stale rows got pointers; no freshness claim |
| adjacency | unchanged | only `tools/mado-binds.py` added; misroot sweep clean |

No axis harmed.

## 4. Discernment spot-check (sources re-opened by ordinary fetch, 2026-10-23)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S172 hyprlang wiki | admit (mined) | `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/hypr-ecosystem/dev/hyprlang.md` → HTTP 200, 4772 B, sha256 `8ce3d33e…e60e` = row | agree | quote "If you want to escape it (put an actual `#` and not start a comment) you can use `##`." verbatim at `:76` (18 words ≤ 25); teaches the `##` escape the tool implements |
| S169 hyprctl client | admit (mined) | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/hyprctl/src/main.cpp` → HTTP 200, 17168 B, sha256 `f6b0d1fc…c93f` = row (row: 17168 B) | agree | quote `std::string socketPath = getRuntimeDir() + "/" + instanceSignature + "/.socket.sock";` verbatim at `:230`; grounds the oracle's `hyprctl -i <instance>` readback |
| WikiVariablesKeywords | reject (no row) | `content/Configuring/Keywords.md`, `content/Configuring/Variables.md`, `content/configuring/core/keywords.md`, `content/configuring/core/variables.md` at the same pin → 404 ×4; GitHub tree API at the pin lists only `content/configuring/core/environment-variables.md` for `eyword\|ariable` | agree | no openable page at the pin; a lead is not a row; substituting the Lua-era env-var page would mis-teach |
| S162/S167 duplicate-URL rows | reject (used-by extended) | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, exit 0, the same 7 W04 (S030, S042, S045, S097, S119, S120, S121) as `evidence/sources-start-a3.txt` | agree | a second row for the same URL would add a W04 duplicate; extending `used-by` keeps one row per source |
| Counter v3 as the claim's rule | reject (pre-data) | `c1/count-v3.py` vs `c1/count.py`; receipts' `V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)` | agree | v3's expected tables were the lane's own model; v4 takes them from Hyprland — the self-model could not tell a correct resolver from a faithful copy |

SOURCES row quote check: S172 (newly written) re-opened above; quote verbatim and ≤ 25 words. Census run by me:
`mado ok`, exit 0.

## 5. Trend verdicts

- **expansion: improved.** A capability row enters the SCORECARD with a passing demonstration (`static bind-table
  resolver`, 41/41 against Hyprland's own tables); a new sourced note `corpus/knowledge/bind-table-r25.md` on the P1
  binds frontier; four mined tier-A rows S169–S172 (168 → 172).
- **quality: improved.** Two stale SCORECARD rows (`:437`, `:1342`) are now marked with pointers and re-run; five of six
  routed repairs closed with checks shown red and green; non-author reviews produced errata on the note and a PROVINCE
  correction. No admitted entry was found false and left unmarked (R2 open and the R8 registration line are routed).
- **discernment: improved.** The outside spot-check agrees with the gate on 2 admits and 3 rejects; controls preceded
  data; leaks (M25-2), the weak Q36 check (M25-3) and surviving counter mutants were disclosed rather than amended.

## 6. Closure verdict

`lanes.mado = ok`; `admitted = true` (verdict `admitted`): C1 verifies (`improved`), C2 verifies as
`unprovable-but-better` under this non-author ruling, no axis harmed. Weighed without regard to the lane's four prior
rejections or the operator unblock (directive 36). SHONEN: four `[~]` boxes with pointers; box 3 ("Executable without
oral context") looks checkable by a non-author via `python3 -I tools/mado-binds.py --home DIR` — operator-owned
promotion, not written here.

## 7. Routed defects (lane fixes next round)

1. M25-2: label-free case paths (random directory names) in any counter that sandboxes a tool, so `/proc/self/mountinfo`
   cannot reveal the case type.
2. Counter mutants `skip-oracle-check` and `embed-threshold-1000` survive: add a drift-fault witness and an embed
   fixture that a ≥1000 threshold misses; describe `embed_hits` as a plaintext audit only.
3. R2 / M25-4: encode the population-equality clause (predicate population = counter population) in QUALITY 36 or a
   successor and its check.
4. M25-3: fixtures killing the surviving `check-control-receipts.py` mutants and a per-counter-version receipt filter.
5. R8: `registration.md:85` claims hardened MutCheckRegOrder/MutCheckReceipt checks under `round-25/quality/` that were
   never landed — append a correction; the QUALITY 33–35 survivors stay open.
6. `tools/mado-binds.py`: `{{…}}` arithmetic left literal; `source` paths and `$VAR` seeding can read outside `--home`
   (documented in PROVINCE; fix or keep as a stated limit).
7. C2 ledger: `:1409`/`:1410` have no second derivation; the `:308` command cell is not lane-relative (F2).
8. `evidence/c1-before-v4-41cc04c8.txt` carries no `exit=` line (the after receipt does).
