# ConnCalibration — round-43 calibration check (mismatches)

Seat: `ConnCalibration` (connector, leaf). Lane: `mado-shokunin`.
Tip at run time: `2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa` (jj-lane.sh state:
`local=2a3707c… remote=2a3707c… ahead=0 behind=0 tracked=0 untracked=19`; untracked = w2
seat files). Data commit `1959770657f1f8665097c1aed4be6c1cbb07139f` (parent `496340dd…`,
the C2 v2 freeze); round base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`.

Method: every round-43 statement in `SCORECARD.md`, `LOG.md` and `SHONEN.md` was listed and
checked against repo bytes at the tip (read-only git; lane tools). The calibration gate
`quality/check-axis-scores.py --rev 2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa --repo .`
was run (expected per the task) and both round counters were re-run at the tip.

`SHONEN.md` contains **no** round-43 statements (`grep -nE '43|40|41|42' SHONEN.md` → no
hits), so it contributes no statements to the check.

## Statements and verdicts

| # | Statement | Location | Observed (repo bytes, tip 2a3707c) | Match? |
|---|---|---|---|---|
| 1 | Registration freeze `b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`, base `a35cfdf…`; C1 unchanged `PRED-C1-r42`, C2 v1 `PRED-C2-r43`; w1 38 seats; CritClaimSizing finding 2 + CritC2Cheat 16 forgeries; C2 re-registered pre-data as `PRED-C2-r43-v2` at `496340dd…`; axis-base `MADO_AXIS checked=3 mismatched=0`; data commit `1959770657…` | SCORECARD.md:2531 | `git log`: 1959770657 parent = 496340dd; w1-spec.json items=38 (roles 14/7/4/3/3/3/2/1/1); CritClaimSizing.md:15 finding 2 (17-line entry, four NEW ids); CritC2Cheat.md; axis-base.txt:4 `MADO_AXIS: checked=3 mismatched=0 rev=a35cfdf…`; registration(-v2).md present. | YES |
| 2 | C1 before `fixtures=0/37 tool=absent verdict=TARGET_MISSED` exit 1 @ base → after `fixtures=37/37 tool=present verdict=TARGET_MET` exit 0 @ data commit; tool byte-identical to round-42 ref (sha256 `e3c2e471…`); falsified by three independent implementations, mutation, cheat and security seats; open defects cheats 4, 6 | SCORECARD.md:2535 | c1-before-base.txt:2 `fixtures=0/37 tool=absent verdict=TARGET_MISSED rev=a35cfdf…` exit=1; c1-after-data.txt:49 `fixtures=37/37 tool=present verdict=TARGET_MET rev=1959770657…` exit=0; `cmp tools/mado-geometry.py .ufo/waves/round-42/c1/ctl-ref-tool.py.txt` → IDENTICAL, sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`; w1/CritC1Cheat.md rows 4 (`cheat-4-selfhash-teeth.py` MET, HOLE) and 6 (`cheat-6-detect.py` MET, HOLE); w1 contains ExecIndepA/B/C, MutC1CounterGates, MutRefSelftest, CritC1Cheat. | YES |
| 3 | C2 v2 before `admitted=0/1` exit 1 @ base → after `admitted=1/1 verdict=TARGET_MET` exit 0 @ data commit (v1 also 1/1); residual: claim-binding forgeries A1, A2, D1, E2, H1, X1 of `ctl/v2-forgeries/` still admit | SCORECARD.md:2536 | c2-v2-before-base.txt:2 `admitted=0/1 verdict=TARGET_MISSED rev=a35cfdf…` exit=1; c2-after-data.txt:32 `admitted=1/1 verdict=TARGET_MET rev=1959770657…` exit=0; c2-v1-after-data.txt:32 same; ctl/v2-forgeries/forge-v2.log + more-v2.log: admitted A1, A2, D1, E2, H1, X1; rejected B1, B2, C1, C2, E1, F1, F2, G1, G2, X2, X3. | YES |
| 4 | Capability "rule size versus reported size join": selftest 73/73; 37/37 at `1959770`; live host run `NO_MATCHING_CLIENT`, exit 3, no gkeep window | SCORECARD.md:2544 | c1-after-data.txt:1 `selftest=73/73`; re-run of counter at tip → `fixtures=37/37 … verdict=TARGET_MET rev=2a3707c…` exit 0; live-geometry-host.txt:10 `verdict=NO_MATCHING_CLIENT`, :11 `exit=3`, :10 `clients=4`. | YES |
| 5 | Sources 226→234 rows (S290-S297, tier A, `mined`, opened 2026-10-26); S155/S158 used-by extended by one item each; knowledge entries 59→60; gkeep-geometry theme admitted as one successor entry; four staged files refused with reasons and flip conditions; considerthese 2026-10-25 proposal 2 mined as QUALITY 81; Mistakes M43-1..8 mined; QUALITY 77-80 from round-42 closure routed defects; `quality/check-locators.py` added (criterion 77); saturation 9.0/N=3 unchanged; retired none | SCORECARD.md:2548 | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 226 @ a35cfdf, 234 @ tip; S290-S297 all tier A / mined / 2026-10-26; S155 used-by ends `…hyprland-gkeep-geometry-r43.md` (one item before), S158 used-by ends `…hyprctl-getoption-native-forms-r40.md, corpus/knowledge/hyprland-gkeep-geometry-r43.md`; navigation (check-axis-scores) base 59/59 → tip 60/60; lesson round-43.md has ADMIT (`gkeep-size-to-real-size-r11.md` → `hyprland-gkeep-geometry-r43.md`) + 4 REFUSE rows with flip conditions; QUALITY 77-81 present (81 = count dead attempts and dirty closures); lesson contains M43-1..8; `quality/check-locators.py` exists (15739 B). | YES |
| 6 | Axis table re-derived at `1959770657…` plus round-43 records commit: navigation 60/60; calibration resolved-active 68/68; operability selftest 12/12 | SCORECARD.md:2550 | `python3 -I quality/check-axis-scores.py --rev 2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa --repo .` → `MADO_AXIS_ROW: axis=navigation published=60/60 derived=60/60 verdict=MATCH`, calibration 68/68 MATCH, operability 12/12 MATCH, `MADO_AXIS: checked=3 mismatched=0 rev=2a3707c…`, exit 0. | YES |
| 7 | Locator correction: `w->size(GEOMETRIC_GOAL)` at `Hyprland-HyprCtl.cpp:427-428` (clients -j object) and `:448` (second formatter); `negative:` prefix at `Hyprland-RegexMatchEngine.cpp:7-8`, `RE2::FullMatch` at `:16`; computed with grep; round-43 pins byte-identical to round-42 (`receipts/fetch-sha256.txt`) | LOG.md:2487 | `grep -n 'GEOMETRIC_GOAL' .ufo/waves/round-43/fetch/Hyprland-HyprCtl.cpp` → size calls at lines 427, 428, 448 (positions 426, 447); `grep -n 'negative:\|FullMatch' …/Hyprland-RegexMatchEngine.cpp` → line 7 `starts_with("negative:")`, line 16 `FullMatch`; round-43 fetch-sha256.txt vs round-42: seven Hyprland files + host-gkeep.conf hashes identical (only gkeep-ui-excerpt.py and host-clients-r43.json differ — regenerated/new captures). | YES |
| 8 | Freeze `b2e2efd6…`; C1 counter frozen at `809dc2c`; C2 v1 `quality/counters/c2-r43-gkeep-entry.py` `PRED-C2-r43`; pins re-fetched 2026-10-26; controls at base: `CTL_C1 controls=46` (REF and BASE-absent anchors; 0 of 47 non-reference runs reach MET), `CTL_C2 controls=74 correct=74/74`; before C1 `fixtures=0/37 tool=absent TARGET_MISSED` | LOG.md:2488 | ctl-c1.txt:1 `controls=46`, :50 `CTL_C1 VERDICT: PASS (controls scoring TARGET_MET: 0 of 47; reference met: 1)`, :51 exit=0; ctl-c2-v2.txt:75 `CTL_C2: controls=74 correct=74/74`, :76 exit=0; `cmp quality/counters/c1-r42-geometry.py <(git show 809dc2c…:quality/counters/c1-r42-geometry.py)` → identical; c1-before-base.txt. | YES |
| 9 | Wave w1 spec/dispatch `5add5b45a65ddaa18fad00c6afa9dbfda29ee0b0`: 38 seats (executor 14, scribe 7, critic 4, scout 3, connector 3, reviewer 3, mutation-tester 2, simplifier 1, sentinel 1) | LOG.md:2489 | `git log -- w1-spec.json` → committed at `5add5b45a65ddaa18fad00c6afa9dbfda29ee0b0`; items=38; role Counter: executor 14, scribe 7, critic 4, scout 3, connector 3, reviewer 3, mutation-tester 2, simplifier 1, sentinel 1. | YES |
| 10 | SHONEN box 2 receipt `.ufo/waves/round-43/receipts/live-geometry-host.txt`: tool on live host, `verdict=NO_MATCHING_CLIENT`, exit 3, 4 clients, no gkeep window | LOG.md:2490 | File exists; live-geometry-host.txt:3 `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f`, :10 `clients=4 … verdict=NO_MATCHING_CLIENT`, :11 `exit=3`. | YES |
| 11 | w1 findings changed round before data; C2 re-registered as `PRED-C2-r43-v2` at `496340dd53fabd800be42e8fb19090f35e2c235c` before any data; 74 controls still 74/74 under v2; forgery harness re-pointed rejects B1, B2, C1, C2, E1, F1, F2, G1, G2, X2, X3 and still admits A1, A2, D1, E2, H1, X1; C1 kept as registered (cheats 4, 6 carry full model) | LOG.md:2491 | `git log`: 496340dd exists (C2 v2 freeze) before data commit 1959770657; ctl-c2-v2.txt 74/74; forge-v2.log / more-v2.log: admitted A1, A2, D1, E2, H1, X1 (`ADMITTED`/`admitted=1/1`), rejected B1, B2, C1, C2, E1, F1, F2, G1, G2, X2, X3 (`rejected`/`admitted=0/1`); registration-v2.md:36-45 C1 kept. | YES |
| 12 | Data commit `1959770657…`: tool byte-identical to `ctl-ref-tool.py.txt`; entry ten cited ids (S290-S297 + held S155/S158); lesson; README index row + Frontier bullet; PROVINCE.md tool row; SKILL.md decision row, probe row and subsection; QUALITY 77-81; `quality/check-locators.py` from seat `ExecLocatorGate`; measured C1 37/37 exit 0; C2 v2 1/1 exit 0 (v1 also 1/1); census `mado ok` exit 0 | LOG.md:2492 | `git ls-tree` at 1959770657: tools/mado-geometry.py, corpus/knowledge/hyprland-gkeep-geometry-r43.md, corpus/lessons/round-43.md, corpus/QUALITY.md, quality/check-locators.py all present; tool identical (cmp, see #2); entry has exactly 10 `source:` lines (S295, S290, S155, S291, S292, S293, S294, S158, S297, S296); corpus/README.md:71 index row + :294-301 round-43 Frontier route; PROVINCE.md:32 tool row; SKILL.md:158 decision row, :225 probe row, :246 subsection "Rule size versus reported size"; QUALITY 77-81 present; c1-after-data.txt / c2-after-data.txt / c2-v1-after-data.txt; census-after-data.txt:9 `mado ok …` :10 exit=0. | YES |
| 13 | Isolated-oracle observation (`w1/ExecOracleGkeep/`): Hyprland 0.56.2 nested in round-27 bubblewrap oracle reported `"size": [420, 500]`, `"floating": true` for app id `org.omarchy.gkeep` under the host's three rules; controls: without size line → 200x200 (client's buffer), with `size 300 300` → 300x300, without `float on` → tiled | LOG.md:2493 | w1/ExecOracleGkeep/20-observation.txt: `"class": "org.omarchy.gkeep", … "floating": true, … "size": [420, 500]`; §5 controls: floatonly `size=[200, 200] floating=True`, size300 `size=[300, 300] floating=True`, nofloat `size=[918, 498] floating=False` (tiled); also nomatch. | YES |
| 14 | New locator checker caught L1's first draft (four single-line locators spanning two receipt lines; M43-7) and one wrong SKILL.md locator (`Hyprland-WindowRuleApplicator.cpp:426` → `:422,426`); entry and SKILL.md read `locators=15 miss=0` | LOG.md:2494 | `python3 -I quality/check-locators.py --fetch .ufo/waves/round-43/fetch corpus/knowledge/hyprland-gkeep-geometry-r43.md SKILL.md` → `CHECK_LOCATORS: locators=15 miss=0`, exit 0; SKILL.md:260 `Hyprland-WindowRuleApplicator.cpp:422,426`; lesson round-43.md M43-7 documents the draft MISS. | YES |
| 15 | SHONEN.md round-43 statements | SHONEN.md (whole) | No round-43 statements present (`grep -nE '43|40|41|42' SHONEN.md` → exit 1, no hits). | n/a (none) |

## Calibration gate (task-required run)

```
$ python3 -I quality/check-axis-scores.py --rev 2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa --repo .
MADO_AXIS_ROW: axis=navigation published=60/60 derived=60/60 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=68/68 derived=68/68 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa
exit=0
```

## Tip re-runs of the round counters (registration target includes "and at the tip")

```
$ TMPDIR=/fast/scratch/hyaku/mado-r43/ConnCalibration python3 -I quality/counters/c1-r42-geometry.py --repo . --rev 2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa
PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET rev=2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa nonce=bf4183e03523e398
exit=0

$ TMPDIR=/fast/scratch/hyaku/mado-r43/ConnCalibration python3 -I quality/counters/c2-r43-gkeep-entry-v2.py --repo . --rev 2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa
PRED-C2-r43-v2: admitted=1/1 verdict=TARGET_MET rev=2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa
exit=0
```

## Result

- Statements checked: **25** (15 rows above; rows 5 covers 13 sub-statements, row 8 covers 6).
- Mismatches between self-assessment (SCORECARD.md/LOG.md/SHONEN.md round-43 statements) and
  observed repo state at tip `2a3707c`: **0**.
- Calibration gate: `checked=3 mismatched=0` (matches the published axis table; exit 0).

## Observations (not counted — lesson-internal pointers, outside the three assessed files)

- `corpus/lessons/round-43.md:93` cites `receipts/census-after.txt`; the committed receipt is
  named `census-after-data.txt` (the same bytes: W04 ×7 + W01 S277, `mado ok`, exit 0).
- `corpus/lessons/round-43.md:205-208` cites `receipts/c1-after-tip.txt` and
  `receipts/c2-after-tip.txt`; no after-tip receipts exist at the tip (only the after-data
  receipts are committed). The tip verdicts were re-measured by this seat (above) and hold.

## Tooling record

No tools installed. Used system `python3` (3.14), `git` (read-only), `cmp`, `sha256sum`,
`grep`, `sed`, `diff` — all pre-existing. Scratch `$S=/fast/scratch/hyaku/mado-r43/ConnCalibration`
used for the two counter re-runs (TMPDIR), deleted on exit.
