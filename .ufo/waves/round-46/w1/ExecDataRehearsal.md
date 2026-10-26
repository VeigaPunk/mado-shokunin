# ExecDataRehearsal — round 46 pre-data dress rehearsal (hyaku run 9, w1)

Date 2026-10-26. Lane `mado-shokunin`. Seat `ExecDataRehearsal` (executor, leaf). Task: build the full **data tree in
scratch** and put **every counter and gate** on it, so the L1 learns the reds before writing data.

## 0. What was built, and the exact digests

Two scratch clones under `/fast/scratch/hyaku/mado-r46/ExecDataRehearsal/` (deleted at exit; nothing outside the lane
was written):

| tree | base commit | data commit built | shape |
|---|---|---|---|
| `tree` | freeze `8c5434c6` (registration freeze) | `f99eee87` | `tools/mado-devices.py` installed + `.ufo/waves/round-46/l1-draft/build-pos.py` applied (entry, S316-S325, lesson Gate, README row) |
| `tree-tip` | tip `e0be61e4` (w1 spec/dispatch committed) | `d7ae208c` | same patch on the round **tip**, i.e. where the real data will land |

Recipe used verbatim from the dispatch (`git clone -q --shared --no-checkout`, `rev-parse --show-toplevel` asserted equal
to the clone before the first commit, `git -C` on every later call):

```
$ cp .ufo/waves/round-46/l1-draft/mado-devices.py <clone>/tools/mado-devices.py
$ python3 -I .ufo/waves/round-46/l1-draft/build-pos.py <clone>      # -> applied
$ git -C <clone> -c user.name=… -c user.email=seat@scratch.invalid commit -q -m …
```

Content digests (all computed, `sha256sum`):

| artifact | sha256 |
|---|---|
| `.ufo/waves/round-46/l1-draft/mado-devices.py` = `tools/mado-devices.py` in both trees | `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b` |
| `quality/counters/c1-r46-devices.py` | `dfeaa4401430ddc2d68711b8dd30b1f470fe1d74b6d1f39477172a30d2fc850a` |
| `quality/counters/c1-r46-fixtures.json` | `027ed50877b345e34b27e38b4a865be4b23f94c0cc0067ac42265ca1778e3fc1` |
| `quality/counters/c2-r46-input-device-entry.py` | `18ea82b1c4372b0c8e7af585d0edf09ffbf6d4a0d276ce19fc97519b720b72b7` |

The data commit's delta (`git show --stat f99eee87`) is exactly 5 files / 662 insertions: `corpus/README.md` (+1),
`corpus/SOURCES.md` (+10), `corpus/knowledge/hyprland-input-devices-r46.md` (+71), `corpus/lessons/round-46.md` (+14),
`tools/mado-devices.py` (+566). `git diff --stat b22ea56b HEAD -- quality/` shows only the three counter files that the
freeze added — no quality tool changed, so every tool red below is inherited, not caused by the data.

Receipts for every line of this report: `.ufo/waves/round-46/w1/ExecDataRehearsal/receipts/` (list in §9).

## 1. Verdict table (data tree, `f99eee87` unless noted)

| # | check | exact result | exit | verdict |
|---|---|---|---|---|
| 1 | `c1-r46-devices.py --repo tree --rev HEAD --work …` | `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` | 0 | **GREEN** |
| 2 | same, `tree-tip` (`d7ae208c`), random nonce | `verdict=TARGET_MET seeds=46,2857552420` | 0 | **GREEN** |
| 3 | `c2-r46-input-device-entry.py --repo tree --rev HEAD --base b22ea56b` | `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1` / `admitted=1/1 verdict=TARGET_MET` | 0 | **GREEN** |
| 4 | same, `tree-tip` | `admitted=1/1 verdict=TARGET_MET rev=d7ae208c…` | 0 | **GREEN** |
| 5 | `check-axis-scores.py --repo tree --rev HEAD` | `navigation published=62/62 derived=63/63 verdict=STALE`; calibration `73/73` MATCH; operability `12/12` MATCH; `mismatched=1` | **1** | **RED (R1)** |
| 6 | `check-index.py --rev HEAD --repo tree` | `indexed=63/63 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 | GREEN |
| 7 | `check-index-rows.py --rev HEAD --repo tree` | `rows=63 errors=0 warns=4`; new `WARN holds-no-overlap: row knowledge/hyprland-input-devices-r46.md at line 74` | 0 | **RED (R2, warn-level)** |
| 8 | `sources-census.sh validate --file <tree>/corpus/SOURCES.md` | `file ok …` + 14×W04 + 1×W01, no E-code | 0 | GREEN (warnings only; content of the W04s is R8) |
| 9 | `check-session-material.py --repo tree --rev HEAD` | `files=17094 findings=97`; base `files=17070 findings=97`; `grep -c "file=.ufo/waves/round-46"` = **0** | **1** | **RED at base too (R4)** |
| 10 | `check-evidence-pointers.py --repo tree --rev HEAD` | `verdict=TARGET_MET … dangling_r36=0` | 0 | GREEN |
| 11 | `tools/*.py --selftest`, every tool that has one (9 files, 11 invocations) | see §5: 6× argless pass, assessment 20/20, tripwire 9/9+16/16+33/33, devices 48/48 | 0 | GREEN except R5 |
| 12 | `check-locators.py --fetch .ufo/waves/round-46/fetch <entry>` | `CHECK_LOCATORS: locators=38 miss=19` | **1** | **RED (R7, advisory — not a registered gate)** |
| 13 | `check-control-receipts.py --round 46 --data-registry registration.md --tip HEAD` | `CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-.ufo/waves/round-46/controls/ receipts=0` | **1** | **RED (R3, layout)** |
| 14 | `population-suite.py --checker quality/check-population.py` | `SUITE verdict=FAIL fixtures=46 failed=9` | **1** | **RED at base too (R6)** |
| 15 | `check-population.py --registration registration.md c1.out c2.out` | `POPULATION verdict=UNREADABLE … reason=no **PRED-...** sentence with a supported target` | 2 | N/A (registration shape) |
| 16 | `counter-selftest.py`, `check-counter-discrimination.py`, `check-r38-discrimination.py` | not applicable: harnesses of the round-26/35/36/38 counter grammars (`--profile r35|r36`, round-26 C1/C2 paths) | — | N/A |
| 17 | `mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures` | `{"code": 2, "error": "FileNotFoundError", …, "result": "could-not-evaluate"}` | **2** | **RED at base too (R5)** |

## 2. RED items — what the L1 must fix before data

### R1 — the axis gate is red at any data tree (blocking, exit 1)

`quality/check-axis-scores.py` re-derives three axes and compares them with the lane's last published table. At base
(`b22ea56b`), at the freeze (`8c5434c6`) and at the tip (`e0be61e4`) it is green (`mismatched=0`). At both data trees it
fails on exactly one row:

```
MADO_AXIS_ROW: axis=navigation published=62/62 derived=63/63 verdict=STALE
MADO_AXIS_ROW: axis=calibration published=73/73 derived=73/73 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=1
```

Cause: the entry adds one knowledge file and the README row indexes it, so `check-index.py` reports `indexed=63/63`
(measured, row 6) while the last publication still says 62/62. The current publication is `SCORECARD.md:2617`:
"Axis table re-derived at `ee6659b` (`receipts/axis-data.txt`): navigation 62/62; calibration resolved-active 73/73; operability selftest 12/12."

**Fix:** in the data commit, add a new last publication line of the same unquoted shape with
`navigation 63/63; calibration resolved-active 73/73; operability selftest 12/12`, write `.ufo/waves/round-45`-style
receipts `.ufo/waves/round-46/receipts/axis-data.txt` (and `axis-tip.txt`), and re-run the gate at the data commit and at
the tip until `mismatched=0`. The lane already has a record of this exact failure mode:
`quality/receipts/red-axis-publication-stale-at-data-commit.txt`. Nothing else in the data tree moves this gate.

### R2 — the README index row's Holds cell is the literal placeholder `draft` (new warning)

`check-index-rows.py` at the data tree: `rows=63 errors=0 warns=4`. The three base warns are unchanged; the fourth is new:

```
WARN holds-no-overlap: row knowledge/hyprland-input-devices-r46.md at line 74
```

The rule is documented in the checker: a Holds cell that "shares no >=5-word sequence with the note's own bytes"
(`quality/check-index-rows.py:28`). `build-pos.py` writes the row as
``| `knowledge/hyprland-input-devices-r46.md` (MADO-R46-1, round 46) | draft | S316-S325 |`` — the middle cell is a
placeholder, so it cannot overlap the note. Exit stays 0 (warns never affect the exit code), but a placeholder cell in
the data registry is the same defect class the r45 row does not have.

**Fix:** the data README row must carry a real Holds sentence drawn from the entry (the r45 row at `corpus/README.md`
line 73 is the template), then re-run `check-index-rows.py` and require `warns=3`.

### R3 — the registered control-receipts gate finds no `controls/` directory for round 46

```
$ python3 -I quality/check-control-receipts.py --round 46 --data-registry .ufo/waves/round-46/registration.md --repo tree --tip HEAD
CONTROL_RECEIPTS verdict=FAIL reason=no-receipt-under-.ufo/waves/round-46/controls/ receipts=0 counter_sha=- …
```

The gate (SKILL.md row `mado-r27-control-receipts`, line 726) reads `.ufo/waves/round-N/controls/`; round 46 keeps its
controls at `.ufo/waves/round-46/receipts/ctl-c1.txt` and `ctl-c2.txt` (both committed at `e0be61e4`; tails measured:
`CTL_C1 VERDICT: PASS (controls scoring TARGET_MET: 0 of 23; reference met: 1)` and
`CTL_C2 VERDICT: PASS (wrong=0 of 15; positive admitted=1)`). Round 45 has no `controls/` directory either, so this is a
layout deviation, not a data defect.

**Fix (L1 decision, pre-data):** either place (or duplicate) the two control receipts under
`.ufo/waves/round-46/controls/` so the registered gate can see them, or state the deviation explicitly in the round-46
lesson/data commit so a later reader does not read `receipts=0` as fabricated controls. Do not claim this gate green
while `receipts=0`.

### R4 — `check-session-material.py` is red at base, unchanged by the data (no new finding)

```
base   f99eee87 … files=17070 findings=97 rev=b22ea56b…      (exit 1)
freeze 8c5434c6  files=17094 findings=97                     (exit 1)
data   f99eee87  files=17094 findings=97                     (exit 1)
```

Per-rule tally identical at all three: `R1_CLIENT_DUMP=23 R2_PROC_TABLE=26 R3_MONITOR_IDENT=46 R4_HOME_LISTING=2`.
**The new material trips nothing:** a grep of the gate's own output for files under `.ufo/waves/round-46/` returns 0 at
the data tree, i.e. neither `receipts/live-devices-host-l1.txt` (the `hyprctl devices -j` dump) nor the new
`.ufo/waves/round-46/*` freeze files produce a finding. The entry itself is outside the gate's scope by construction (the
gate reads only tracked files under `.ufo/`).

**Fix:** none is required by the data. If the round's definition of done demands `findings=0`, the 97 pre-existing
findings must be triaged or allow-listed — that is closure item D3, and its number is **97, not the 48** the round-45
closure names. Composition, computed from the gate's own lines: `R1` 23 lines / 52 objects, `R2` 26 lines / 846 rows,
`R3` 46 lines / 58 objects (45 of the 46 lines are the round-45 `RevengerOmarchy` fixture dumps, the 46th is the
`ExecPrivacyGate` copy of the gate script), `R4` 2 lines / 52 paths. The per-rule numbers the gate prints are **lines
(file, rule pairs)**, not object counts.

### R5 — `mado-evidence-audit.py --selftest` is red in any clone (pre-existing, documented)

```
$ python3 -I tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures
{"code": 2, "error": "FileNotFoundError", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}   rc=2
```

Same in the freeze-based and tip-based trees. Cause is already measured in `.ufo/waves/round-44/w1/ExecHarmBase.md` §F1:
the fixture manifest declares two **empty directories** (a directory entry with no files), git cannot store an empty
directory, so no clone has them. **Fix:** none for data; any round-46 receipt that reports this selftest green must name
where the two directories were created (round-44 measured `46/46` once they exist).

### R6 — `population-suite.py` is red on a byte-identical checker (pre-existing)

```
$ python3 -I quality/population-suite.py --checker quality/check-population.py
SUITE verdict=FAIL fixtures=46 failed=9  (green-numerator-not-compared, red-denominator-larger, red-denominator-smaller,
red-case-lines-and-denominator, red-registered-total-differs, red-second-summary-disagrees, red-first-summary-disagrees,
exit2-cases-pass-space-before-equals, exit2-cases-pass-space-after-equals)
```

`quality/check-population.py` and `quality/population-suite.py` are byte-identical at base and at the data tree
(`17e99993…` and `99e7d876…`, both revisions) — the failure predates round 46 and the data cannot cause it. **Fix:** none
for this round; do not cite the suite as evidence of a healthy population checker.

### R7 — `check-locators.py` on the entry: 19 of 38 locators MISS (advisory; not a registered gate)

```
CHECK_LOCATORS: locators=38 miss=19        exit 1
```

The worst cases (locator named in the prose, `supported=0`): `Hyprland-InputManager.cpp:1213-1238` (entry:32),
`Hyprland-InputManager.cpp:1282-1295` and `Hyprland-IKeyboard.cpp:87-96` / `:101-116` (entry:33),
`Hyprland-HyprCtl.cpp:785-802` (entry:34), `Hyprland-VirtualKeyboard.cpp:36-44` and `Hyprland-IKeyboard.cpp:60-64`
(entry:35), `Hyprland-MiscFunctions.cpp:777-789` and `Hyprland-InputManager.cpp:2119-2131` (entry:36), plus the two
`OBS`-anchored `Hyprland-HyprCtl.cpp:769` (entry:44) and `wiki-Keywords.md:67` (entry:49). The tool's attribution rule is
"nearest backticked fragment on the same line", so a chain paragraph that names eight locators and quotes once produces
MISS verdicts even where the locator is right.

Precedent, measured on the two preceding entries at the same freeze: r45 entry `locators=62 miss=23 exit 1`; r44 entry
`locators=43 miss=8 exit 1`. **Fix (only if the L1 wants this tool green):** one backticked fragment per locator in the
chain paragraphs (30-36) instead of one fragment per paragraph. This is not a C2 clause — the C2 counter's own clause g
locator/quote binding passes for all ten ids.

### R8 — the registration undercounts the census URL repeats: two named, five measured

`census validate` exits 0 at the data tree with **14 W04** lines (base receipt `.ufo/waves/round-46/receipts/census-before.txt`
has **9**). The five new W04s are S317, S318, S320, S321, S324. The held rows already on those URLs (the census prints a
W04 for every occurrence *after* the first, so these are not flagged):

| new row | URL (suffix) | held rows on the same URL | flagged partner |
|---|---|---|---|
| S317 | `src/config/legacy/ConfigManager.cpp` | **S162** (r24), **S303** (r45) | S303 |
| S318 | `src/config/values/ConfigValues.cpp` | **S215** (r37) | — |
| S320 | `src/debug/HyprCtl.cpp` | **S158** (r24), **S307** (r45) | S307 |
| S321 | `src/helpers/MiscFunctions.cpp` | **S182** (r27) | — |
| S324 | `hyprlang/v0.6.8/src/config.cpp` | **S173** (r25) | — |

The registration says "The two cross-scope URL repeats (S317 with S162/S303 …, S320 with S158/S307 …)"; the measured
number is five. **Fix:** correct the registration prose in the data commit / lesson (warnings never change a lane's
status, so no gate moves).

## 3. Separability — measured, and it holds

Built two scratch trees on the tip (`e0be61e4`) to test the registration's Separability paragraph:

| tree | commit | C1 | C2 |
|---|---|---|---|
| tool only (`tools/mado-devices.py`, no data) | `4727d4b4` | `TARGET_MET` (90/90, 150/150, selftest ok, readonly ok, tool present), exit 0 | `admitted=0/1 verdict=TARGET_MISSED`, exit 1 |
| data only (build-pos, tool removed) | `bcaf74f9` | `fixtures=0/90 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED`, exit 1 | `admitted=1/1 verdict=TARGET_MET`, exit 0 |

Neither counter reads the other's artifact. The tool-only tree also reproduces the C2 before-state exactly
(`receipts/c2-before-base.txt`), and the data-only tree reproduces the C1 before-state (`tool=absent`).

## 4. Non-gate completeness the round-45 template carries (not enforced by any gate, easy to forget)

`git show --stat ee6659b9` (the round-45 data commit) touched 14 files; the rehearsal tree carries 5. No `quality/*.py`
reads `QUALITY.md` or `PROVINCE.md` (grep: no match), so these are bookkeeping, not reds — but the lane's own precedent
is to land them with the data commit:

- `SKILL.md`: a prose section for the new tool (round 45 added `## Monitor rule versus running output (round 45)` at
  `SKILL.md:2099`, a 5-line section quoting the tool's invocation and its verdict vocabulary; round 46 needs the
  input-device counterpart). The section is prose, not a table row — the gate registry rows live at `SKILL.md:693-770`
  and `:2082`.
- `PROVINCE.md` row, `corpus/QUALITY.md` criteria (r45 added 85-86; r46 would be 87-88 if a criterion is added).
- `.ufo/waves/round-46/receipts/census-after.txt`, `live-devices-host-r46.txt`, `c1-after-data.txt`, `c2-after-data.txt`,
  `session-material-data.txt`, and `gate-lines.txt` at the wave root (all present for r45).
- A real `corpus/lessons/round-46.md`: `build-pos.py` writes 14 lines and only a `## Gate` section; the r45 lesson is 81
  lines. The lesson is the carrier of the D1 (round-45 w2 falsification) record this round owes.
- The `Frontier` line in `SCORECARD.md` and the round's writers/claim rows.

## 5. Green evidence (exact lines, `receipts/…` in the seat dir)

Counters (two trees, four nonces): `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`
(C1, seeds `46,3670422903`, `46,46`, `46,251757098`, `46,2857552420`); `admitted=1/1 verdict=TARGET_MET` with every clause
of C2 at 1 (C2, both trees).

Tool selftests, all run in the clone at the data commit (`python3 -I`, cwd = clone root):

```
tools/mado-action-plan.py --selftest            rc=0  SELFTEST_SUMMARY: 52/52 passed
tools/mado-assessment.py --selftest <r21 dir>   rc=0  20 cases, 20 pass (result=selftest, code 0)
tools/mado-devices.py --selftest                rc=0  MADO_DEVICES_SELFTEST: 48/48 passed
tools/mado-evidence-audit.py --selftest <r22>   rc=2  FileNotFoundError (R5)
tools/mado-geometry.py --selftest               rc=0  MADO_GEOMETRY_SELFTEST: 94/94 passed
tools/mado-globals.py --selftest                rc=0  MADO_GLOBALS_SELFTEST: 63/63 passed
tools/mado-monitors.py --selftest               rc=0  MADO_MONITORS_SELFTEST: 48/48 passed
tools/mado-options.py --selftest                rc=0  MADO_OPTIONS_SELFTEST: 211/211 passed
tools/mado-tripwire.py --selftest <core>        rc=0  SELFTEST_SUMMARY: 9/9 passed failed=[]
tools/mado-tripwire.py --selftest <compound>    rc=0  SELFTEST_SUMMARY: 16/16 passed failed=[]
tools/mado-tripwire.py --selftest <hardening>   rc=0  SELFTEST_SUMMARY: 33/33 passed failed=[]
```

Tools with **no** `--selftest` (unchanged set): `tools/mado-anims.py`, `tools/mado-binds.py`, `tools/mado-eventq.py`,
`tools/mado-wsrules.py`. Fixture dirs for the three argument-taking selftests were read from each tool's own docstring /
its SKILL.md row, not guessed: `.ufo/waves/round-21/assessment-fixtures`, `.ufo/waves/round-22/audit/fixtures`,
`.ufo/waves/round-17/tripwire/{core,compound,hardening}`.

Other green: `check-index.py` `63/63` and `--selftest` `12/12 assertions passed`; `check-evidence-pointers.py`
`verdict=TARGET_MET`; `sources-census.sh validate` `file ok … exit=0`; `check-axis-scores` green at base, freeze and tip.

## 6. Risks / limits of this rehearsal

- The rehearsal tree is the **positive control** (`build-pos.py`), not the data. It proves the counters and gates admit a
  tree of that shape; it does not prove the L1's hand-written entry text will bind (clause d's quote uniqueness, clause
  g's per-id line rule and the census line are where hand edits usually break). The ten `OBS` lines and the census line
  are copied verbatim from `l1-draft/entry.md`; any rewording must be re-measured.
- C1's clause g oracle is the reference itself, so a contract error shared by reference and tool is invisible to it —
  unchanged residual, declared in the registration.
- `check-locators` MISS verdicts (R7) are a heuristic over long prose lines; treat the 19 as a reading list, not as 19
  factual errors. Two of them (entry:44, entry:49) sit on `OBS` lines whose quotes the C2 counter does verify.
- `check-session-material` cannot go green from the data (R4); the 97 findings are all pre-existing.
- Not run, deliberately: any live `hyprctl` call (the seat may not open a compositor connection), anything that writes
  the lane, and the round-specific harnesses that cannot apply to this round (rows 15-16 of §1).

## 7. Host safety and hygiene

- No compositor call, no input injection, no package transaction, no host-service change; no host file read. No `pacman`.
- No tool installed (nothing was needed): tool/version/channel table is empty.
- All work under `/fast/scratch/hyaku/mado-r46/ExecDataRehearsal/`; the two clones plus the four separator trees and the
  counter work dirs are deleted at exit. Receipts copied into this seat's `receipts/` directory first.
- No git/jj mutation in the lane or the fleet; the four clone commits were made only inside the scratch clones with an
  identity scoped to `seat@scratch.invalid` and `rev-parse --show-toplevel` asserted first.
- No session material committed: the report quotes no window title, monitor serial/description, process table or home
  listing; the live receipt lives where the L1 committed it and was never copied.

## 8. Bottom line for the L1

The **counters are ready**: both C1 and C2 are `TARGET_MET` on a data tree built at the freeze **and** at the tip, and
separability holds in both directions. Before writing data the L1 must: **R1** publish `navigation 63/63` (or the axis
gate fails at the data commit, as it has before), **R2** replace the README row's `draft` cell with a real Holds
sentence, **R3** decide the `controls/` layout for the registered control-receipts gate, and **R8** correct the
"two URL repeats" sentence to five. R4, R5, R6 are pre-existing and must not be attributed to this round's data; R7 is
advisory and has precedent on both preceding entries.

## 9. Receipt inventory (`.ufo/waves/round-46/w1/ExecDataRehearsal/receipts/`)

| file | content |
|---|---|
| `c1-tree-freeze.txt`, `c1-tree-tip.txt` | full C1 clause lines + final line + exit, both trees |
| `c2-tree-freeze.txt`, `c2-tree-tip.txt` | full C2 clause lines + final line + exit, both trees |
| `axis-all-revs.txt` | axis gate at base, freeze, tip, and both data trees |
| `index-and-rows.txt` | check-index, its selftest, index-rows at base and at the data tree |
| `census-data.txt` | the frozen base census receipt + the census validate at the data tree |
| `session-material.txt` | the gate at base / freeze / data, and the round-46 finding count (0) |
| `tools-selftests.txt` | every tool with a selftest, its exact invocation and last line |
| `gates-misc.txt` | evidence-pointers, locators (selftest + entry + r44/r45 baselines), control-receipts, population-suite |
| `separability.txt` | the two separator trees, their commits, and both counter final lines per tree |
| `digests.txt` | the sha256 table of §0 |

Twin copy of this report: `.ufo/waves/round-46/w1/ExecDataRehearsal/report.md` (identical bytes).
