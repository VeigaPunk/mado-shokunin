author: hyaku closure (non-author integrator, @m_opus)

# mado round 43 — non-author closure spot-check (attempt 1)

Lane HEAD before `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`, after `58466627de847d6502283c3bb9e652caea97b411`.
Driver digest (`.ufo/watchdog.log`, mutable — copied here):
`2026-10-26T04:09:14-03:00 launch mado round=43 pgid=3089898 driver=hyaku-inline attempt=1` /
`2026-10-26T06:22:15-03:00 complete mado round=43; hyaku-inline attempt=1` /
`2026-10-26T09:23:40-03:00 complete mado round=43; hyaku-inline attempt=1` (a second, duplicate completion line for the same attempt).
I did not author the round. Re-checks ran on committed bytes (`git show`/`git ls-tree` at the cited revisions), on upstream raw files,
and read-only on the host. No lane counter or `quality/` gate was executed; the deliverable tool `tools/mado-geometry.py` was run from
committed bytes in a scratch directory (it starts no process and opens no socket). Two read-only reviewer seats I dispatched (non-lane)
re-read the C2 entry against its receipts and sampled the gate decisions; their findings are folded in below.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-43/mado.md` | `mado-shokunin 906cfe709b7f539375942336b3bb4ce1171834fb` (2026-10-26 06:21:14 -03:00) |
| report lands after the lane commit | commit times | lane tip `5846662` 06:19:23, report 06:21:14 → commit-then-report holds |
| prompt committed | `git log --format='%an %H' -- .ufo/prompts/mado-round-43.md` | `mado-shokunin dfc3f3f9fa48f6564e4e641761359e299af2f56f` (04:09:13, before the launch line) |
| SHONEN heading | report `## SHONEN` | present, 4 lines, all `[~]` with pointers; `SHONEN.md` has 4 boxes and is unchanged `a35cfdf..5846662` |
| cited commits exist + ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for a35cfdf, b2e2efd, 5add5b4, 496340d, 1959770, a47efeb, 2a3707c, 8750016, 5846662 | all 9 `commit`, all ancestors; all 8 round commits authored `mado-shokunin` |
| pushed, clean | `jj-lane.sh state …`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=58466627… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `58466627…` |
| prompt carries template contract | `diff` of prompt lines 1-140 vs `templates/round-prompt.md` (140 lines) | every differing line is a rendered placeholder (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §6 hyaku addendum and §7 scratch directive follow |
| L2 floor | `jq '{seats, n:(.results\|length)}'` on `w1-results.json`, `w2-results.json` at the tip | 38/38 and 32/32 results (70 seats) — floor met |
| real report, not a marker | 8 lane commits, 2505 inserted lines outside `.ufo/` | real report → status `ok` |
| round-42 routed items | lesson `## Round-42 closure items`; `LOG.md:2487` | locator correction appended; C1 tally defined once (`registration.md:59`); SHONEN box 2 receipt committed (`receipts/live-geometry-host.txt`); lesson exists; r41 leftovers stated still open |

## 2. Per-claim re-check

| claim | plain measurement (base → tip) | observed | reported | ruling |
|---|---|---|---|---|
| C1 operability (capability acquisition) `tools/mado-geometry.py` | `git ls-tree -r --name-only <rev> -- tools/mado-geometry.py \| wc -l`; `… -- tools \| wc -l`; `git show <rev>:tools/mado-geometry.py \| sha256sum` vs `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` | 0 → 1; tools 11 → 12; tip, data commit and round-42 reference all `e3c2e471505932f7…`; `git diff --stat 1959770 5846662 -- tools/` empty | tool absent → present, byte-identical to the round-42 reference | **verified (re-measured)** |
| C1 capability run | committed tool + `host-gkeep.conf` pin on my own 3-client dump (gkeep floating 420×500, floating 875×600, tiled 875×600) | `verdict=AGREE` / `DIFFER` / `TILED`, summary `agree=1 differ=1 tiled=1 … verdict=DIFFER`, exit 1 | capability row: AGREE/DIFFER/TILED join | **verified** |
| C1 live host (SHONEN box 2) | `hyprctl clients -j \| python3 -I <tip tool> --clients - --rules ~/.config/hypr/gkeep.conf`; `sha256sum ~/.config/hypr/gkeep.conf` | `rules=1 float_rules=1 … clients=4 matched=0 … verdict=NO_MATCHING_CLIENT`, exit 3; `3726e488…` = pin; Hyprland 0.56.2 `efb50993…` | `receipts/live-geometry-host.txt` same verdict, exit 3 | **agree** |
| C2 coverage (sourced) `corpus/knowledge/hyprland-gkeep-geometry-r43.md` | `git ls-tree … corpus/knowledge \| wc -l`; entry present; `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; `git grep -ciE 'set_default_size\|GEOMETRIC_GOAL\|RE2::FullMatch' a35cfdf -- corpus/knowledge PROVINCE.md SKILL.md tools` | knowledge 59 → 60; entry 0 → 1; rows 226 → 234 (S290-S297 new, none removed); base grep 0 hits | entry, rows 226 → 234, new ground | **verified (re-measured)** |
| C2 Gate bindings | per `GATE` line: `git show <tip>:<receipt> \| sha256sum`; whitespace-flattened `grep -oF <quote>` in its receipt and in the other nine | 10/10 sha256 equal; each quote 1 occurrence in its receipt, 0 in the other nine; 3-11 words (≤25) | same | **verified** |
| C2 content (non-author reading) | reviewer seat: each entry claim opened at its receipt line (rule text, RE2 `FullMatch`, `static_.size`, first-map branch `:49,:55-61,:96`, `Target.cpp:10-13`, `WindowTarget.cpp:70-71`, setBox → `GeometricMovableAnimated.cpp:43-45`, GOAL `:19-20`, HyprCtl `:427-429`, `set_default_size(420, 500)`, census) | 14/14 claims supported, locators land; w2 corrections (`8750016`) leave no superseded claim in the entry | v2 scores bookkeeping; content is the non-author's reading | **supported — real receipt-backed coverage** |

Evidence-verified only (lane-owned instruments, not executed): `receipts/c1-before-base.txt` `fixtures=0/37 tool=absent verdict=TARGET_MISSED`, exit 1;
`c1-after-data.txt` `fixtures=37/37 tool=present verdict=TARGET_MET rev=1959770…`, selftest 73/73, b2 `killed=5/6 forced_dead=1`, exit 0;
`c1-after-tip.txt` same at `8750016`, b2 `killed=6/6`; `c2-v2-before-base.txt` `admitted=0/1`, exit 1; `c2-after-data.txt` / `c2-after-tip.txt`
`admitted=1/1 verdict=TARGET_MET`, exit 0; `ctl-c1.txt` `CTL_C1 VERDICT: PASS (controls scoring TARGET_MET: 0 of 47; reference met: 1)` at `a35cfdf`;
`ctl-c2-v2.txt` `CTL_C2: controls=74 correct=74/74`. Lane-declared predicate limits stand: C1 cheats 4 and 6 reach MET; C2 v2 admits 14/14
shape-keeping do-nothing controls and 6/16 weakening mutants survive — which is why the C2 content was read claim by claim above.

Upstream re-open: `curl` of `…/efb50993…/src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp` → 10359 B, sha256 `f05f256150c8dcf5…`
(= S291 pin), quote at `:56`; `…/src/layout/target/WindowTarget.cpp` → 16614 B, `8bcaf37000cf55e1…` (= S293 pin), `:70-71` hands `m_box.logicalBox`
to `setBox`. Reviewer seat: `RegexMatchEngine.cpp` and `GeometricMovableAnimated.cpp` likewise byte-identical.

Harm watch: `git diff a35cfdf 5846662 -- SCORECARD.md` is a pure append (35 lines: Round 43 section, capability row, axis line). Every changed
doc outside `.ufo/` is append-only (`git diff --numstat`: LOG +12, PROVINCE +1, SKILL +59, QUALITY +10, README +10, SOURCES +10/−2 where the
two deletions are S155/S158 rows whose only changed cell is `used-by`, appended). Axis inputs re-derived plainly: README knowledge links 59 → 60,
QUALITY numbered criteria 76 → 81 (published navigation 60/60, calibration 68/68 = 63 + 5); `2a3707c..5846662` touches neither file, so the
committed `w2/ExecHarmTip/logs/tip-2a3707c-axis.log` `MADO_AXIS: checked=3 mismatched=0` still describes the tip. The red axis window
`[1959770, 2a3707c)` is the lane's two-phase publication, not content harm. Old tool selftests unchanged (`w2/ExecHarmTip.md:12-14`). No axis harmed.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 re-measured: tool absent → present, byte-identical to the frozen reference; capability run AGREE/DIFFER/TILED; live NO_MATCHING_CLIENT reproduced |
| coverage | improved | C2 re-measured: entry 0 → 1, knowledge 59 → 60, rows 226 → 234, ground absent at base; 14/14 entry claims supported by receipts |
| depth | unchanged | SKILL.md only gains rows and a subsection (append-only); one licence cell overstated (routed D3) |
| freshness | unchanged | pins re-fetched and byte-identical to round 42; no held claim re-verified as stale or fixed |
| calibration | unchanged | v1 → v2 re-registration before data and predicate limits disclosed; axis fraction stays 1.0 (63/63 → 68/68) |
| adjacency | unchanged | PROVINCE +1 tool row; sibling overlap scans recorded, nothing absorbed |

## 4. Discernment spot-check (`corpus/lessons/round-43.md` `## Gate` and assimilation ledger)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `REFUSE gkeep-size-rule-application-r10.md` | reject | staged file (`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/`); `fetch/Hyprland-DefaultFloatingAlgorithm.cpp:55-61,96`; `fetch/Hyprland-WindowTarget.cpp:70-71`; `fetch/Hyprland-GeometricMovableAnimated.cpp:19`; `fetch/Hyprland-HyprCtl.cpp:427-428`; `w1/ExecGoalVsValue/pins/window.cpp:1526,1687-1698` | **agree** | Rule value → `windowGeometry` → target box → `m_realSize` → hyprctl `GEOMETRIC_GOAL`; `onAck` only stores the pending acked size. r10's `REPORTSIZE` quote is inside the X11 branch feeding `sendWindowSize`, not the `clients -j` field. Reason under-cites S294/S158 (routed D1). |
| `REFUSE gkeep-observation-route-r11.md` | reject | staged `gkeep-observation-route-r11.md:8,18-26` vs staged `gkeep-size-to-real-size-r11.md:15,17`; `fetch/Hyprland-HyprCtl.cpp:427-428` | **agree** | Same single host receipt and quotes as r11; the route is r11's own recheck line and held S158 — no independent step. |
| `ADMIT gkeep-size-to-real-size-r11.md` as `hyprland-gkeep-geometry-r43.md` | admit | staged r11 vs entry `:3-12,40-48,56-58,72`; `corpus/SOURCES.md` S290-S297; base `git grep` 0 hits | **agree** | Sources re-mapped by document (r11 S302-S305 ↔ S291-S294; S310 → S295/S296/S297); no package id carried; r11's "settled" overclaim replaced by GOAL/CURRENT plus a host UNK. |
| `gkeep-element-rules-r30.md` refusal withdrawn, not adopted | withdrawal | lesson `## Post-data corrections`; `~/.local/share/omarchy/default/hypr/apps/system.conf:4` | **agree** | The recorded flip (rules sourced from the shipped desktop config) fired; adoption is a separate gate (no pinned row; staged r30 claims three rules, quotes two). |
| new row S291 | admit (tier A, `code`) | upstream raw URL re-fetched: 10359 B, sha256 `f05f2561…` = row and Gate; quote `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` at `:56` | **agree** | 5 words, ≤25, single occurrence, outside comments; row `opened 2026-10-26`, `used-by` the entry. |
| new row S293 | admit (tier A, `code`) | upstream raw URL re-fetched: 16614 B, sha256 `8bcaf370…`; quote at `:70-71` | **agree** on bytes, wording defect | Quote verified; the row title "the client's request as input" echoes the refuted r10 premise while its `teaches` cell is correct (routed D2). |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → W04 ×7 (S030, S042, S045,
S097, S119, S120, S121) + W01 S277, `mado ok`, exit 0 — identical to `receipts/census-before.txt` and `census-after.txt`.

## 5. Trend verdicts

- **expansion: improved** — one new capability row demonstrated running (my own fixture run and the live host run), one knowledge entry on
  ground absent at base (knowledge 59 → 60), rows 226 → 234 all opened and re-verified.
- **quality: improved** — C2 instrument tightened before data; round-42's wrong locators corrected in `LOG.md:2487` with a locator checker;
  every w2 content finding on the entry corrected in `8750016` with no superseded claim left in the entry (reviewer sweep).
- **discernment: improved** — 4/4 sampled gate decisions (two refusals, one admit, one withdrawal) agree on outside re-reading, and the lane
  re-registered its own predicate when w1 showed it gameable; residual wording defects do not flip any decision.

Closure: status `ok`, **admitted=true**, verdict `admitted` — both claims verify, no axis harmed.

## 6. Routed defects (lane fixes next round)

1. D1 — lesson `round-43.md:75` r10 refusal reason cites S291/S293 (box path) but not the reported-field links S294/S158; its flip says
   "the reported size" though `CWindow::getReportedSize()` is ack-derived — name the `hyprctl clients -j` `size` field. `:74` maps S310 to
   S295/S296 only; S297 also re-grounds it. Correct by appended erratum, not rewrite.
2. D2 — `corpus/SOURCES.md` S293 title "the client's request as input" reads as the refuted premise; supersede with the other w2-found row-cell
   defects (S290-S294, S296, S297) under CORPUS rule 2.
3. D3 — `SKILL.md:276` TILED licence column asserts "the tiler, not the floating rule path, set its box"; for a pseudo-tiled client the size comes
   from the stored rule pseudo-size (`window.cpp:2402-2408`), as the row's own caveat concedes. Same premise as the open C1 TILED defect (`w2/CritEntryInf.md` F1).
4. D4 — entry `:66` cites `w1/ExecOracleGkeep/20-observation.txt` / `10-cases.txt` by bare path; they did not exist at data commit `1959770`
   (resolve at tip) — the CritOracleClaim dating fix was not applied. Receipt `20-observation.txt:24` cites `gkeep-shm.c:156-164`; correct range 150-159.
5. D5 — `registration.md:5` says 37 w1 seats (38 ran; disclosed in LOG); SCORECARD Round 43 says "Mistakes M43-1..8" while the lesson carries M43-9.
6. D6 — open predicate defects (lane-declared): C1 cheats 4 (source-pin selftest) and 6 (sandbox detection) reach MET; C2 v2 do-nothing 14/14 and
   6/16 surviving mutants; `quality/check-locators.py` compares identifiers not numbers and 12/37 mutants survive its selftest. Re-register before next use.
7. D7 — no committed axis receipt at the tip `5846662` (the report quotes a write-time run); the last committed MATCH is at `2a3707c`. Commit tip receipts.
8. Driver: two `complete mado round=43` lines (06:22:15, 09:23:40) for one attempt — driver-side duplicate, status-neutral.
9. Still open from round 41: S041 held-row citation; tool ergonomics O1-O5; `PROVINCE.md:75-76` cite.

SHONEN boxes remain `[~]`. Box 2 (live run) is reproducible by a non-author — I reproduced its `NO_MATCHING_CLIENT`, exit 3 — and box 3
rests on committed independent-rebuild reports (`w1/ExecIndepA.md`, `ExecIndepB.md`, `ExecIndepC.md`); promotion review is operator-owned.
