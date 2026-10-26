# ConnCalibration — SCORECARD/SHONEN calibration vs repo at base (round 46 w1)

Seat: ConnCalibration (calibration connector, leaf). Date: 2026-10-26.
Ground: lane repo at base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe` (all commands name this rev
or the commit the cited statement is scoped to). No host-state reads beyond git objects; no
compositor calls. Every command below was run; outputs are quoted shape-only (no serials/titles).

## Verdict

- Statements checked: 68 verifiable claims (counts, hashes, freeze/base ids, receipt contents,
  capabilities-row evidence, named files/commits).
- **Mismatches: 2** (M1, M2 below).
- **Verified with unstated caveat: 3** (C1-C3 below).
- All other 63 statements verified clean against the named commands.

---

## Mismatches

### M1 — SHONEN box 4 names a receipt id the cited file does not carry
Statement (SHONEN.md:11): "Historical assertion: corpus/knowledge/province-accuracy-selfaudit.md
round-5 receipt (VER-M4B)".
Truth at base:
```
git show b22ea56b:corpus/knowledge/province-accuracy-selfaudit.md | grep -c 'VER-M4B'   -> 0
git show b22ea56b:corpus/knowledge/province-accuracy-selfaudit.md | grep -n 'VER-M4'    -> lines 282,283,285,299,314 (all "VER-M4")
```
The file brands its own verifiers `VER-M4` (append v4). The literal id `VER-M4B` occurs only in
`LOG.md:417` ("VER-M3 | VER-M4B") and in round-16/20 wave reports. Severity: naming; the cited
file exists and is the round-5-era receipt the box describes.

### M2 — Round-43 section: "Mistakes M43-1..8 mined"; the lesson holds 9
Statement (SCORECARD.md round 43, Sources paragraph).
Truth at base:
```
git show b22ea56b:corpus/lessons/round-43.md | grep -c '^\*\*M43-'   -> 9
```
Covered in-line: the round-44 section's published erratum says it "should read M43-1..9" and prints
the same grep -> 9. Counted as a mismatch because the round-43 sentence itself still misstates the
count at base; a reader is repaired only by the later section.

## Verified with unstated caveat

### C1 — Round-45 axis sentence quotes derived numbers from a receipt that flags them STALE
Statement: "Axis table re-derived at ee6659b (receipts/axis-data.txt): navigation 62/62;
calibration resolved-active 73/73; operability selftest 12/12."
```
git show b22ea56b:.ufo/waves/round-45/receipts/axis-data.txt
  -> navigation  published=61/61 derived=62/62 verdict=STALE
  -> calibration published=71/71 derived=73/73 verdict=STALE
  -> operability published=12/12 derived=12/12 verdict=MATCH
  -> MADO_AXIS checked=3 mismatched=2 rev=ee6659b... ; exit=1
```
The stated numbers exist only as the `derived=` column; at the data commit the published table
still read 61/61 and 71/71 (publication lag). The MATCH state for 62/62 and 73/73 first exists at
the records commit: `axis-tip.txt` at `ac3f9dee` prints all three MATCH, checked=3 mismatched=0.
Numbers true as derived; the stale verdict is unmentioned in SCORECARD.

### C2 — Round-43 w2-outcome trailing axis line is the base-rev log, not a tip receipt
Statement ends the tip-receipts list with "`MADO_AXIS checked=3 mismatched=0`".
```
git show b22ea56b:.ufo/waves/round-43/w2/ExecHarmTip/logs/base-axis.log
  -> checked=3 mismatched=0 rev=a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f   (the BASE rev)
git show b22ea56b:.ufo/waves/round-43/w2/ExecHarmTip.md (axis table)
  -> at data: nav 59/59 vs 60/60 STALE; calib 63/63 vs 68/68 STALE; "closed at 2a3707c"
```
The committed axis log carrying `checked=3 mismatched=0` is at the base rev; the data commit was
STALE on two axes and the closure commit `2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa` repaired it.
Also the r43 receipts dir holds only `axis-base.txt` (checked=3 mismatched=0, rev=a35cfdf, exit=0).

### C3 — Assimilation parentheticals name staged files that exist only in the lessons' ADMIT rows
Statements: r43 "admitted as one successor entry (`gkeep-size-to-real-size-r11.md`)"; r44
"(`gkeep-client-size-request-r12.md`, three of its sentences corrected)".
```
git ls-tree -r --name-only b22ea56b | grep -E 'gkeep-size-to-real-size-r11|gkeep-client-size-request-r12'  -> (empty)
git show b22ea56b:corpus/lessons/round-43.md:45  -> "ADMIT .../gkeep-size-to-real-size-r11.md as corpus/knowledge/hyprland-gkeep-geometry-r43.md"
git show b22ea56b:corpus/lessons/round-44.md:61  -> staged row for gkeep-client-size-request-r12.md "admitted as the successor"
git show b22ea56b:corpus/README.md:71,72         -> frontier rows name hyprland-gkeep-geometry-r43.md /
                                                    hyprland-gkeep-size-request-r44.md as the admitted entries
```
Consistent with the admission record (rename at admit); the named paths themselves are not in the
tree at base.

---

## Clean verifications (command -> result)

### SHONEN.md
- Box 1/3: `corpus/knowledge/executor-test-sufficiency.md` exists; `grep -c MADO-R3-4` -> 3. `SKILL.md` exists.
- Box 2: `corpus/knowledge/config-health-report-r3.md` exists; `git show b22ea56b:LOG.md | grep -c VER-M3` -> 2 (line 294 "box-3 CLOSED (VER-M3: config-health report reproduces)"; note LOG titles the row "round 4 (training r3)"). `grep -c VER-M3 config-health-report-r3.md` -> 0 (the id lives in LOG.md, not the entry; box text cites "LOG.md round 3 (VER-M3)", accurate).
- Box 4: `corpus/knowledge/province-accuracy-selfaudit.md` exists; `PROVINCE.md` exists. (Id mismatch: M1.)

### Round 43
- Registration `.ufo/waves/round-43/registration.md` base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f` (header line matches); `registration-v2.md` file-add commit = `496340dd53fabd800be42e8fb19090f35e2c235c` (`git log --diff-filter=A`) = claimed v2 freeze. Both commits exist.
- Data commit `1959770657f1f8665097c1aed4be6c1cbb07139f` exists; `receipts/c1-before-base.txt` = `fixtures=0/37 tool=absent verdict=TARGET_MISSED` exit=1 rev=a35cfdf; `receipts/c1-after-data.txt` = `fixtures=37/37 tool=present verdict=TARGET_MET` exit=0 rev=1959770; `receipts/c2-v2-before-base.txt` = `admitted=0/1 TARGET_MISSED` exit=1; `receipts/c2-after-data.txt` = `admitted=1/1 verdict=TARGET_MET` exit=0; `receipts/c2-v1-after-data.txt` = `admitted=1/1 verdict=TARGET_MET` exit=0.
- Byte-identity: `git show b22ea56b:.ufo/waves/round-42/c1/ctl-ref-tool.py.txt | sha256sum` = `e3c2e47150593…5a99` and equals `git show 1959770:tools/mado-geometry.py | sha256sum` -> claim "round-42 reference installed byte-identically (sha256 e3c2e471…)" verified at the data commit. (At base the installed tool is the r44 extension `1da3ddae…`, selftest 94/94; at 1959770 selftest = 73/73 — both matching the claims scoped to their commits.)
- Capabilities row: tool selftest 73/73 at 1959770 (`MADO_GEOMETRY_SELFTEST: 73/73 passed`); counter 37/37 at 1959770 (receipt); `receipts/live-geometry-host.txt` = `verdict=NO_MATCHING_CLIENT`, exit=3.
- `receipts/axis-base.txt` = `MADO_AXIS checked=3 mismatched=0` rev=a35cfdf exit=0 (59/59, 63/63, 12/12 all MATCH) — matches "every published axis ties at its maximum at base".
- Sources 226 -> 234: `git show a35cfdf:corpus/SOURCES.md | grep -cE '^\| S[0-9]+'` = 226; at 1959770 and 2a3707c = 234. S290-S297 all present. Knowledge 59 -> 60 (`git ls-tree corpus/knowledge | grep -c .md` at those commits). S155/S158 used-by old->new logged (round-43.md:89-90, "one item appended").
- QUALITY 77-81 present in `corpus/QUALITY.md` (77 = check-locators.py, line 401). M43 real count 9 (M2). `quality/check-locators.py` exists.
- v2-forgeries fixtures `A1, A2, D1, E2, H1, X1` (+B1,B2,C1,C2,E1,F1,F2,G1,G2,P-genuine) exist under `.ufo/waves/round-43/ctl/v2-forgeries/fixtures/`.
- Controls `receipts/ctl-c2-v2.txt` = `CTL_C2: controls=74 correct=74/74`.
- w1: `CritC1Cheat.md` table rows 4 and 6 both `TARGET_MET` flagged HOLE (cheats 4, 6); `CritC2Cheat.md` "admits 16 forged sets"; `CritClaimSizing.md` exists. w1 seat count 38 (38 .md files in `round-43/w1/`).
- w2 (32 seats, 32 reports): `ConnCalibration.md` "## Result: 0 mismatches" at 2a3707c; `ExecDoNothingV2.md` "all 14 are admitted=1/1"; `MutC2V2.md` "16 mutants… 10 killed, 6 survive"; `MutCheckLocators.md` "37 single-edit mutants… 25 killed, 12 survived"; `CritEntryInf.md` F1 (tiled reads static_.size); `RerunC2Data.md` byte-identical + ten Gate bindings re-derived; `RerunCensus.md` "226 → 234 … measured two independent ways"; `RerunControlsV2.md` "byte-identical reproduction … CTL_C2: controls=74 correct=74/74"; `RerunC1Data.md` "six independent invocations" (prose; 222 fixture lines). Tip receipts: `c1-after-tip.txt` fixtures=37/37 TARGET_MET exit=0 rev=875001662c…; `c2-after-tip.txt` admitted=1/1 TARGET_MET exit=0; `census-after.txt` tail `mado ok … SOURCES.md`, exit=0. (Axis log caveat: C2.)
- `considerthese/2026-10-25.md` proposal 2 = "Count dead attempts and dirty closures from the watchdog digests" -> mined as QUALITY 81 (criterion 81 = closure-row attempt/cleanliness/work counts). Consistent.

### Round 44
- Registration base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f` (header), v2 freeze `03fa5c618b089064a657b3d79d3d4272ae4b6894` = file-add commit of `registration-v2.md`. Both exist.
- `receipts/c1-v2-before-base.txt` = `fixtures=11/26 tool=present verdict=TARGET_MISSED` exit=1 rev=6a1a9052; `receipts/c1-after-data.txt` = `fixtures=26/26 tool=present verdict=TARGET_MET` exit=0 rev=e46789213830597348fe96a351ae004d10587385; `receipts/c2-v2-before-base.txt` = `admitted=0/1` exit=1; `receipts/c2-after-data.txt` = `admitted=1/1` exit=0.
- Capabilities row: tool at base selftest 94/94 (`MADO_GEOMETRY_SELFTEST: 94/94 passed`); `receipts/live-geometry-host-r44.txt` = NO_MATCHING_CLIENT exit=3 (with the fullscreen dump note).
- Sources 234 -> 238 (counts at 6a1a9052 and e467892); S298-S301 present; knowledge 60 -> 61; S164 used-by old->new (round-44.md:79).
- QUALITY 82-84 in corpus/QUALITY.md; M44 count = 9 (matches "M44-1..9 mined"); erratum M43 -> 9 (M2).
- `quality/ratio-domain-meta.py` run at 8ac15c41 and at b22ea56b (`--from 34 --to 43`) prints exactly `DOMAIN_META: domain=12 meta=5 window=34-43 default=1` — matches the quoted line.
- `receipts/axis-base.txt` (rev=6a1a9052): 60/60, 68/68, 12/12 MATCH, checked=3 mismatched=0 — matches "every published axis ties at its maximum at base". `receipts/axis-data.txt` (rev=e467892): 61/61, 71/71, 12/12 MATCH — matches the round-44 axis sentence.
- Controls `ctl-c1-v2.txt` PASS "0 of 20; reference met: 1"; `ctl-c2-v2.txt` PASS "wrong=0 of 11; positive admitted=1".
- w1 named reports exist (`CritC1Cheat, CritC2Cheat, CritClaimSizing, RevC2Counter, CritFsPremise, ConnCrossClaim`); w1 seat count 38 (matches "38 seats"). (Staged-file naming caveat: C3.)

### Round 45
- Registration base `0c89478af821a6424c9ac922eafe02e39630cf4f` (header), v2 freeze `7c0b00350d70f6e5d3b0259a132d25ee030d525e` = file-add commit of `registration-v2.md`. Data commit `ee6659b90f7bf69aa03283dba804dd90081b7ff5` exists (also the assignment's landed commit; tip `4d22eeb66c2835af8aaa3fac6ad838fa616aa663` exists).
- `receipts/c1-v2-before-base.txt` = `fixtures=0/81 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` exit=1 rev=0c89478a; `receipts/c1-after-data.txt` = `fixtures=81/81 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` exit=0 rev=ee6659b; `c2-v2-before-base.txt` = `admitted=0/1` exit=1; `c2-after-data.txt` = `admitted=1/1 verdict=TARGET_MET` exit=0.
- Round-44 after values (closure D2): `round-44/receipts/c1-after-data.txt` fixtures=26/26 TARGET_MET; `c2-after-data.txt` admitted=1/1 TARGET_MET — as quoted.
- Capabilities row: `tools/mado-monitors.py` selftest at base = `MADO_MONITORS_SELFTEST: 48/48 passed`; counter 81/81 + 150/150 at ee6659b (receipt); `.ufo/waves/round-45/receipts/live-monitors-host-r45.txt` = `MADO_MON_OUTPUT: name="DP-1" … verdict=AGREE`, summary `verdict=OK`, exit=0 — matches "DP-1 AGREE, OK, exit 0" (fields read shape-only; no serial reproduced).
- Sources 238 -> 252 (counts at 0c89478a and ee6659b); S302-S315 present; S303/S307 W04 duplicate-URL warnings in `receipts/census-after.txt` (matches "census W04"); knowledge 61 -> 62; `quality/check-session-material.py` exists; QUALITY 85 = check-session-material (corpus/QUALITY.md:418), 86 present; M45 count = 6 (matches "M45-1..6").
- Session-material: `receipts/session-material-data.txt` = `SESSION_MATERIAL: files=17063 findings=97 rev=ee6659b…`, exit=1; closure (round-45-verifier-spotcheck.md:54,94,112) splits 97 = 49 synthetic + 48 un-triaged pre-existing — matches the planned-round-46 sentence "48 pre-existing and 49 synthetic".
- Controls: `ctl-c1.txt` (v1) PASS "0 of 16; reference met: 1" (matches "met PRED-C1-r45 with 16 cheat/do-nothing tools"); `ctl-c2.txt` (v1) PASS "wrong=0 of 10; positive admitted=1" with header "controls=10 (P positive; 9 do-nothing/forged)" (matches "9 forgeries"); `ctl-c1-v2.txt` PASS "0 of 45; reference met: 1"; `ctl-c2-v2.txt` PASS "wrong=0 of 15; positive admitted=1" (header freeze=7c0b0035, base=0c89478a).
- `receipts/axis-base.txt` (rev=0c89478a): 61/61, 71/71, 12/12 MATCH, checked=3 mismatched=0 — matches "every published axis tied at its maximum at base". (Axis-data caveat: C1.)
- w1 named report `ConnCrossClaim.md` exists; w1 seat count 41 (matches "41 seats"). Closure `corpus/lessons/round-45-verifier-spotcheck.md` section 6 lists D1-D6 (D1 records "w2 falsification not run" — the round-46 assignment's closure D1). Assignment-named counters `quality/counters/c1-r45-monitors-v2.py`, `c2-r45-monitor-entry-v2.py` exist at base.
- `considerthese/2026-10-26.md` proposal 1 = "Add a privacy check on new receipts" -> check-session-material.py + QUALITY 85. Consistent.
- Saturation: each of the three sections prints "Saturation 9.0 / N=3 unchanged; retired: none" — the 9.0/N=3 declaration is the standing SCORECARD publication (declared round-12/13 era, SCORECARD.md:280-282 area); no contradicting value at base.

## Method
- All checks read git objects at `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe` unless the statement
  is scoped to another commit (data/tip/freeze commits named above); selftests ran from blobs
  extracted to `/fast/scratch/hyaku/mado-r46/ConnCalibration/base-tools` (scratch deleted after).
- No writes outside the seat dir; no lane/fleet mutation; no host-state reads beyond git.
- Tool installs: none (python3 stdlib only).
