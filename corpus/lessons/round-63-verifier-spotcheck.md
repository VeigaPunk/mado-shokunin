author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# mado round 63 — verifier spot-check (non-author closure)

Lane repo: `C:/Users/jpvei/.zcode/workspace/95b1ba4d-5089-47a4-9fd8-54adebbce2ae/fleet/mado-shokunin`
(branch `master`). Base `cb442f663ca6`; tip `ce7f7673482c58dcdfc9130812e6cd7e3d5f8e39` (pushed).
All commands below were run by this verifier at closure time (2026-11-01) against committed bytes
(`git show <rev>:<path>`) or the live host; none were taken from the report on faith. Security
boundary held on this side too: no r56-era credential material opened, diffed, or surfaced.

## 1. Step-1 conformance

| Check | Command (abridged) | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-63/mado.md` (fleet root) | `mado-shokunin <mado@shokunin.local> 0ffe22942…` | OK |
| `SHONEN` heading | read report | `## SHONEN` with four `[~]` lines + evidence pointers | OK |
| Cited commits exist + ancestors | `git merge-base --is-ancestor <h> refs/heads/master` for `c9a70974`, `cdacf215`, `f0c2308b`, `49b053e8`, `ce7f7673` | all ANCESTOR_OK | OK |
| Tip pushed | `ls-remote origin refs/heads/master` vs local `rev-parse refs/heads/master` | both `ce7f7673482c…` | OK |
| Round work in range | `git rev-list --first-parent --count cb442f663ca6..ce7f7673` | `5`; all five commits authored `mado-shokunin <mado@shokunin.local>` | OK |
| Dispatch/complete digest | `grep 'mado round=63' .ufo/watchdog.log` | `02:53:17 launch … base=cb442f663ca6 (zcode run14)` / `05:20:46 complete … head=ce7f7673482c pushed=True` — matches the contract digest | OK |
| Real report, not marker | read report | work performed, evidence pointers, landed changes each tied to commits | OK |

No conformance defects found. L1-only (no ≥8-L2 dispatch surface) is the standing disclosed
posture since r57, routed around, never treated as answered — noted, status-neutral.

## 2. Per-claim re-check

### C1 — calibration (the six r62 carry-in corrections) — RE-MEASURED, verifies

Six-item `## Corrections (round 63)` block present in `corpus/lessons/round-62.md` at the tip
(0 → 1 by `grep -c '^## Corrections (round 63)'`), `## Errata (round 63)` present in
`corpus/knowledge/windows-dwm-attributes-r62.md` (0 → 1). Every correction re-derived by this
verifier:

| # | Correction | Verifier command | Observed | Match |
|---|---|---|---|---|
| 1 | total-range mislabel | `git diff-tree -r --numstat 4c5435d8 {4fe4544,bd06d021,df415ef3} \| awk '{a+=$1;d+=$2;n++} END{print n" files "a" added "d" deleted"}'` | `35 files 1830 added 1 deleted` / `34 files 1806 added 1 deleted` / `35 files 1860 added 1 deleted` | yes |
| 2 | "wave receipts +441" | same, scoped `-- .ufo/waves/round-62/receipts` and `-- .ufo/waves/round-62` | receipts-only `21 files 359 added 0 deleted` @4fe4544; wave `23 files 466 added 0 deleted` @4fe4544; `22 files 442 added 0 deleted` @bd06d021; 441 matches neither | yes |
| 3 | "18 receipt files" | `git ls-tree --name-only 19407ef2:.ufo/waves/round-62/receipts \| wc -l` | `20` | yes |
| 4 | "Four commits" | `git rev-list --first-parent --count 4c5435d8..df415ef3` | `5` | yes |
| 5 | census endpoint 161-170 | `git show ce7f7673:<run1/run2> \| grep -o '"top_level":[0-9]*'` | `161`, `160` → all-run committed range 160-170 | yes |
| 6 | declaration spread | `git show ce7f7673:.ufo/waves/round-62/claims-declaration-r62.md \| sed -n '36p'` | `…source rows S418-S422,` | yes |

Defect-byte preservation re-verified: base line counts 254 / 72
(`git show cb442f663ca6:<file> | wc -l`); `head -n <base-lines>` of the tip file diffed against
the full base file → empty for both (ORIGINAL_PRESERVED confirmed by re-run).

### C2 — coverage, sourced (CCD path/target plane) — RE-MEASURED, verifies

- `git ls-tree <rev>:corpus/knowledge | grep -c '\.md$'` → 77 @base, 78 @tip.
- README index rows (`grep -cE '^\| `knowledge/[^`]+\.md`'`) → 77 @base, 78 @tip.
- Registry rows (`grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`)
  → 360 @base, 371 @tip. Rows S424–S434 present at the tip, tier A, `mined`, opened 2026-11-01.
- Entry `corpus/knowledge/windows-displayconfig-r63.md` absent @base, present @tip; table rows
  `grep -cE '^\| [HJK][0-9]{2} '` → 19 (4 H + 11 K + 4 J; D05 is a Findings bullet), as reported.
- **D05 honest-unknown verified**: the finding records cause `[UNK]` explicitly, names the residue
  (driver-class vs host-state vs Win11 virtual-refresh artifact; `QDC_VIRTUAL_MODE_AWARE` untested)
  and the flip condition; the raw-byte receipt `.ufo/waves/round-63/receipts/displayconfig-rawdump.txt`
  shows struct sizes `PATH_INFO=72 SOURCE=20 TARGET=48 VIDEO=48 TMODE=48 MODEINFO=64`, `hr=0 hr2=0`,
  `mode0.infoType=2`, `FE-FF-FF-FF` at the frequency-field offsets and `80-07`/`38-04` (1920/1080) at
  the size offsets — the sentinel is recorded, never a measurement. The tool prints
  `vsync=unavailable(0xfffffffe)`.
- Navigation counter receipt (`landing-counters-r63.txt`): `indexed=78/78 missing=0 …
  coverage=10.0000/10` at both `cdacf215` and the tip.

### C3 — operability, capability acquisition (`tools/mado-win-displayconfig.py`) — RE-MEASURED, verifies

Per the round note, this verifier read the bytes first, then re-ran:

- **Byte check (getter-only)**: committed bytes extracted with `git show
  ce7f7673:tools/mado-win-displayconfig.py` (758 lines = the numstat figure; `VERSION = "r63-v1"`).
  P/Invoke surface is exactly two getters: `GetDisplayConfigBufferSizes` and `QueryDisplayConfig`
  (user32.dll). `grep -E '\bSet[A-Z]|\bChange[A-Z]'` → no mutating verb (only a comment at line 677
  stating none exists); `DisplayConfigGetDeviceInfo` → absent (deliberately not called, as
  documented). Live mode spawns one fixed PowerShell child; stdin /dev/null; output whitelisted.
- **Selftest re-run**: `python <extracted> --selftest` → `MADO_WINDISPLAYCONFIG_SELFTEST: 13/13
  assertions passed`, exit 0 — matches the committed receipt.
- **Live receipt re-run** (one, per the round note): `python <extracted>` →
  `MADO_WINDISPLAYCONFIG: CLEAN (paths=1 refresh=64/1 vsync=unavailable(0xfffffffe))` + JSON, exit
  0; `cmp` against the committed `windisplayconfig-live-run1.txt` → **byte-identical**. The JSON
  confirms the entry's facts independently: `buffer_hr=0 query_hr=0`, `paths=1` with `flags=1`
  (DISPLAYCONFIG_PATH_ACTIVE), `mode_info_types=[2,1]`, refresh `64/1`, active/total 1920x1080,
  pixel/hsync/vsync all 4294967294 (0xFFFFFFFE) — D05 shape exactly as recorded.
- **Error path re-run**: `--from-file` on this verifier's own malformed fixture → `MADO_WINDISPLAYCONFIG:
  ERROR (stage=parse detail=JSONDecodeError …)`, exit 2, raw bytes never echoed — matches receipt.
- **From-file re-run**: `--from-file` on the committed snapshot → exit 0, CLEAN, refresh=64/1,
  vsync=unavailable(0xfffffffe) — matches receipt.
- **Crosscheck re-run**: `python .ufo/waves/round-63/receipts/displayconfig-crosscheck.py .` →
  5/5 stable fields AGREE + verdict structure, exit 0 — byte-identical to the committed receipt.
- **Ledger re-run**: `python quality/check-tool-ledger.py --repo . --rev <rev>` → `population=102
  ledger_rows=102 … TARGET_MET` @base; `population=103 ledger_rows=103 uncovered=0 … TARGET_MET`
  @tip, exit 0 both — the 102 → 103 claim re-derived at both ends.
- Capability row enters `SCORECARD.md` § Capabilities the same round (first-working round 63), as
  AXES.md §Capabilities requires.

### In-round landing defects — both honestly receipted, verified

- **(a) used-by setup gate red → green.** This verifier's own cell count on row S430:
  `awk -F'|' '/^\| *S430 *\|/ {print NF-2}'` over `corpus/SOURCES.md` → **13 @c9a70974**, **11
  @cdacf215**, **11 @tip**. The c9a70974→cdacf215 row diff is exactly
  `targetMode|sourceMode|desktopImageInfo` → `targetMode/sourceMode/desktopImageInfo` (proposition
  text untouched). The red run (13 cells) and green run
  (`MADO_USED_BY: … entries=78 rows=371 missing=0 extra=0 … verdict=TARGET_MET`) are both recorded
  in `landing-counters-r63.txt` with named sections, disclosed in the lesson Addendum and the
  SCORECARD § Corrections (round 63) block.
- **(b) receipts re-land at 49b053e8.** `git diff-tree -r --name-only 49b053e8` → exactly **24**
  files, all under `.ufo/waves/round-63/receipts/`; `git cat-file -e ce7f7673:<path>` for each →
  **24/24 present in the tip tree**. The drop (the landing named the directory; the helper landed
  none of it) is disclosed in the 49b053e8 subject, the lesson Addendum 2, and the ce7f7673 LOG
  bullet. Receipts dir holds 25 files at the tip as reported.

### Harm watch — no axis harmed (re-measured)

- Every file in `git diff-tree -r --numstat cb442f663ca6 ce7f7673` shows **0 deletions** — the
  round is pure appends/new files, including the two corrected r62 records and SCORECARD
  (`@@ -3279,3 +3279,97 @@`, additions only).
- True-final range re-derived: **39 files, +2248/−0** (report figure exact); landing range
  `cb442f66→c9a70974` = 13 files +1556/−0; wave dir 27 files +680/−0; 25 receipt files at tip.
- Census validate re-run by this verifier: exit 0, `mado ok`, warning set 36 W04 + 1 W01 —
  byte-identical warning set to the committed start/after receipts (sort-diff empty).
- `harmwatch-selftests-r63.txt`: LEDGER 55/55, WAVE_DONE 63/63, `mado-verify.sh` sha prefix
  `050efc720599345a`; `dwm-recheck-r63.txt`: r62 observer verdict unchanged
  (`timing=unavailable(hr=0x88980090)`; cloaked 14 / visible 13 / 7 app + 7 shell + 0 inherited /
  attr_failed 0 — D04 stands). Receipts, not re-executed gates (lane-owned).

Re-measured vs evidence-verified: C1, C2 counts, C3 (bytes, selftest, live, error, from-file,
crosscheck, ledger), both landing defects, ranges, census, push/ancestry — **re-measured**.
Harmwatch selftests, dwm-recheck, the two committed red-run stderr receipts, navigation/used-by
counter receipts at intermediate revs — **evidence-verified** (committed lane-owned artifacts).

## 3. Discernment spot-check (non-author)

Sampled from `corpus/lessons/round-63.md` `## Gate` (4 admits, 4 rejects available):

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S424 QueryDisplayConfig (winuser.h) | admit (tier A, mined) | fetched `https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-querydisplayconfig` | **agree** | page live; the located quote is a verbatim 20-word substring of the body's first sentence; ms.date 2018-12-05, git_commit `39f250c3…`, updated_at 2026-05-15 all match the row; QDC_ONLY_ACTIVE_PATHS=0x2 and the currentTopologyId-NULL requirement (the call shapes the tool pins) are on the page |
| S431 DISPLAYCONFIG_MODE_INFO_TYPE | admit | fetched `https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ne-wingdi-displayconfig_mode_info_type` | **agree** | page documents SOURCE=1, TARGET=2, DESKTOP_IMAGE=3 — the locator event (M63-3: remembered TARGET=1, page says SOURCE=1/TARGET=2) is genuine and the tool's decode branch (`mode_info_types=[2,1]`, mode0.infoType=2 = TARGET) matches the page, not the memory |
| Decode the mode union's SOURCE_MODE view | reject | entry limits + tool docstring | **agree** | no claim this round joins source-mode geometry; a second struct view doubles the marshaling surface for zero claim value; the limit is named, flip condition present |
| Call `DisplayConfigGetDeviceInfo` for target/adapter names | reject | S424 remarks + entry/tool | **agree** | names are identifying strings (the lane's titles-excluded rule r57); the join needs only indexes; the residue is honestly priced — D05's adapter-class reading stays `[UNK]` because of this refusal, and the round says so instead of quietly calling the getter |
| Build a screen-capture probe this round | reject | L0 queue (r60 question, open) | **agree** | operator-owned scope, no ruling; routed around, never treated as answered — the correct disposition |

New SOURCES row re-opened: S424 (above) — quote ≤25 words (20), located (body first sentence),
verbatim. Census validate: exit 0 (re-run, §2 harm watch).

## 4. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | **improved** | C1: all six routed r62 drifts dispositioned beside re-derivations that this verifier reproduced exactly; defect bytes preserved; the class rule applied to the round's own draft (the "255 vs 254" drift caught pre-landing) |
| coverage | **improved** | C2: 77→78 knowledge files, 77→78 index rows, 360→371 registry rows, new entry 19 rows on uncovered ground, S424-S434 opened and quoted before writing; navigation 78/78 |
| operability | **improved** | C3: durable getter-only CCD observer; selftest 13/13 re-run; live receipt byte-identical re-run; error path rc=2 re-run; from-file rc=0 re-run; crosscheck 5/5 re-run; ledger 102→103 re-run at both revs; capability row same round |
| depth | unchanged | no declared depth claim; the entry adds documented rows under C2's coverage move; no prior depth row changed (0 deletions in range) |
| freshness | unchanged | re-verification surfaces re-measured unchanged by design (D04 verdict unchanged; census warning set identical); no stale item found unmarked |
| adjacency | unchanged | no cross-domain evidence absorbed; screen-capture stayed routed to its L0 owner |

Exploratory claims: none declared this round — no `unprovable-but-better` judgment required of the
non-author reviewer.

## 5. Trend verdicts (closure concurs with the report)

- **expansion: improved** — one new sourced plane on uncovered ground (CCD path/target), 11 mined
  tier-A rows, 1 new indexed entry whose `source:` cites them, 1 capability row; every figure
  re-derived above.
- **quality: improved** — a durable read-only observer with red/green-disclosed assertions and
  byte-identical determinism receipts; the r62 carry-in corrections landed append-only with
  preserved defect bytes; prior tools' harm-watch surfaces re-measured unchanged; no admitted entry
  failed a re-check.
- **discernment: improved** — three red runs and two landing defects disclosed rather than smoothed
  (all four receipts read by this verifier); D05 recorded `[UNK]` with residue/flip instead of a
  guessed cause; the round's own draft correction block drift caught and fixed pre-landing; the
  non-author spot-check (§3) agrees with the gate on all sampled admits and rejects.

## 6. Routed defects / notes for next round

None bar admission; all status-neutral notes:

1. `windisplayconfig-error-path.txt` names its input fixture `…receipts/broken-fixture.json`,
   which is not among the committed receipts (ephemeral fixture). The receipt records the observed
   verdict; the path is trivially re-derivable (this verifier re-ran it with an own malformed file,
   rc=2) — noted so the citation does not read as a committed-path pointer.
2. The four SHONEN boxes remain `[~]` lane-asserted. Boxes 2 (end-to-end task, logged r57→r63 with
   live-surface receipts) and 3 (entry §Verify blocks re-derive from committed bytes without oral
   context) look fully checkable by a non-author now — operator may commission the standing
   non-author review. This verifier does not write `[x]`.
3. Standing L0 posture unchanged: five open questions (omarchy freshness disposal, gate-selftest
   host gap, calibration resolved-active re-derivability, screen-capture scope, the L2 dispatch
   floor); L1-only round disclosed, routed around, never treated as answered.
4. D05 residue (`QDC_VIRTUAL_MODE_AWARE` query shape) is already named as the r64 candidate — the
   flip condition is on record; nothing to route.

Security note: this verification opened only the lane files and public Microsoft Learn pages named
above; no r56-era credential material was read or surfaced.
