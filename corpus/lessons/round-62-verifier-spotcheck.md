author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# mado round 62 — verifier spot-check (non-author closure)

Closed at 2026-11-01T10:46:30Z against lane tip `df415ef3031c8707fa43c1040dc2fbf12c20f935`
(branch `master`, pushed = local). Base `4c5435d8bb3dd108f1dba4998de73c514609d885`
(the r61 verifier spot-check). Security boundary held on the verifier side
too: no r56-era credential material was opened, diffed, or surfaced; every
command below touches only r62-era paths and read-only counters. This file
is written by the closure judge and is NOT committed by the lane; the
orchestrator commits it under the protocol identity.

## 1. Step-1 conformance

| check | result |
|---|---|
| report committed in fleet repo by lane identity | PASS — `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-62/mado.md` → `mado-shokunin <mado@shokunin.local> 5057cb5b…` |
| `SHONEN` heading in report | PASS — `## SHONEN` present; lane-asserted `[~]` ×4, unchanged; no `[x]` written by the lane (correct: only a non-author may write `[x]`) |
| cited lane commits exist + are ancestors of master | PASS — `git merge-base --is-ancestor` OK for `19407ef2`, `f300b2ce`, `bd06d021`, `4fe4544`, `df415ef3` (and base `4c5435d8`) |
| branch tip pushed | PASS — `ls-remote origin refs/heads/master` = `df415ef3031c…` = local `refs/heads/master` |
| cited work reachable in `4c5435d8..df415ef3` | PASS — all five round commits are the full first-parent range; dispatch digest (launch 01:30:57-07:00, complete 02:05:24-08:00 head=df415ef3 pushed=True) matches |
| report is real, not a marker | PASS — work performed, evidence pointers, landed changes with hashes, before→after measurements, Sources & frontier, trend verdicts all present and checkable |
| dispatched prompt carries the contract | PASS — MISSION/AXES binding, 1–3 falsifiable claims, frontier step, report contract (path, sections, SHONEN heading, commit-before-report, hash-citation rule, write scope), L0 channel, honesty rules, security boundary all embedded; L2 floor: L1-only again, disclosed since r57 with the L0 line open — standing status-neutral disclosure, unchanged, routed around |
| frontier step | PASS — census before→after with committed receipts (exit 0 both ends), ≥1 sourced claim (C2 rests on S418–S423), one bounded search logged (`corpus/SOURCES.md` Search log § Round 62: question, where, date, 6 identified / 6 screened / 6 included / 0 excluded + the URL-correction event), mistakes M62-1..M62-3 mined with class · evidence · captured-by · fix |

## 2. Per-claim re-check (all three RE-MEASURED at `df415ef3` unless marked evidence-verified)

### C1 calibration (r61 carry-in corrections, append-only) — verifies

- `git show 4c5435d8:corpus/lessons/round-61.md | grep -c '^## Corrections (round 62)'` → **0**; at `df415ef3` → **1**. Same grep on `corpus/lessons/round-60.md` → **0 → 1**.
- Erratum numstat re-derivation: `git diff-tree -r --numstat cccda4da ad4e8403 -- LOG.md PROVINCE.md SKILL.md` → **`64 0` / `19 0` / `55 0`**; totals → **`28 files 1416 added 0 deleted`** — exactly the correction the round asserts against the r61 report's +52/+13/+50.
- Preservation: base r61 lesson = 175 lines, base r60 lesson = 208 lines; `git show <base>:<lesson> | diff - <(git show df415ef3:<lesson> | head -n N)` → empty both — **ORIGINAL_PRESERVED**. Correction blocks are pure appends.

### C2 coverage (sourced) — verifies

- knowledge files `76 → 77` (`git ls-tree … | grep -c '\.md$'`); README index rows `76 → 77` and the new entry's row exists; SOURCES registry rows `354 → 360` (grep per CORPUS.md census); entry rows **14 = 4 H + 6 K + 4 J**, D04 a Findings bullet — all as reported.
- Navigation counter (lane gate): evidence-verified from the committed receipt `landing-counters-r62.txt` — `indexed=77/77 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0, stamped at both `19407ef2` and `bd06d021`; underlying state corroborated by my own greps (77 files = 77 index rows).
- Sources: S418–S423 present, tier A, `mined`, opened 2026-11-01, each used-by cell cites the new entry + the round lesson.

### C3 operability (capability acquisition, `tools/mado-win-dwm.py` r62-v1) — verifies

- **Bytes read first:** the only P/Invokes are getters (`DwmIsCompositionEnabled`, `DwmGetWindowAttribute` ×2 overloads, `DwmGetCompositionTimingInfo`, `EnumWindows`, `IsWindowVisible`, `IsWindow`, `GetWindowRect`, `GetConsoleWindow`, `GetForegroundWindow`); **no Set*/Move*/Change* verb exists** — the only such strings in the file are the selftest's own `assertNotIn` pins (`dwmsetwindowattribute`, `setwindowpos`, `setwindowlong`, `movewindow`, `setprocessdpiawareness`, `changedisplaysettings`). `VERSION = "r62-v1"`; committed sha256 prefix `8a8ddf2be6833603` = worktree = report's claim.
- **Selftest re-run by the closure judge:** `python -I tools/mado-win-dwm.py --selftest` → `MADO_WINDWM_SELFTEST: 11/11 assertions passed`, **exit 0**.
- **Live receipt re-run by the closure judge:** `python -I tools/mado-win-dwm.py` → `MADO_WINDWM: CLEAN (composition=on reasons=app+shell timing=unavailable(hr=0x88980090))`, **exit 0** — the exact committed verdict line; JSON line carries composition true, `timing.cb_size 320`, `hr −2003304304` (= 0x88980090 signed).
- **Error paths re-run:** `--from-file` on the committed snapshot → `MADO_WINDWM: CLEAN (source=file …)`, exit 0; malformed snapshot → `MADO_WINDWM: ERROR (stage=parse detail=JSONDecodeError …)`, **exit 2**, raw bytes never echoed.
- Crosscheck 5/5 (`windwm-crosscheck.txt`: 5 stable fields AGREE + census structure, no equality claim on churn-prone counters) — committed evidence, consistent with the probe receipts I read (probe runs byte-identical except `top_level` 161→160).
- Tool ledger 101 → 102: committed receipt `LEDGER: population=102 ledger_rows=102 … verdict=TARGET_MET` at both `19407ef2` and `bd06d021`; my own count of `quality/tool-ledger.md` pipe-rows 104 → 105, the +1 being the `mado-win-dwm.py` row. (Lane gate: evidence-verified, not executed.)

### D04 honest-unknown — verified, not papered over

Entry D04 + J24 record `DwmGetCompositionTimingInfo` failing with undocumented
`0x88980090` (−2003304304 signed) in BOTH documented call shapes (the Windows
8.1+ NULL shape and the non-NULL shape S420 promises E_INVALIDARG for),
cbSize 320 per the documented layout, deterministic, cause **`[UNK]`**, with
the residue named and "not guessed at". S420 re-opened by the verifier (below)
confirms the page documents only S_OK / HRESULT-error + the non-NULL
E_INVALIDARG promise, so the divergence reading is correct. My own live re-run
reproduced `timing=unavailable(hr=0x88980090)`. The lesson's Rejected list
names the flip (an operator ruling could move it into the L0 set) — the
honest-unknown is recorded, not smoothed.

### Used-by red-amber-green (M59-4 fired on the lane's own landing) — verified

- Receipt `landing-counters-r62.txt` records all three states with revision stamps: **red** `TARGET_MISSED missing=1` at `19407ef2` (detail: S400 × the new entry), **amber** `missing=1 extra=1` at `f300b2ce`, **green** `missing=0 … TARGET_MET` at `bd06d021`.
- Row-level verification by the closure judge: S400's line at `bd06d021` differs from base only by the used-by cell gaining `, corpus/knowledge/windows-dwm-attributes-r62.md` (keyed on `| S400 |`, proposition text untouched); S405's line at `bd06d021` is **byte-identical** (cmp) to its pre-amber state at `19407ef2` — the amber mis-aim (S405's cell extended at `f300b2ce`) was reverted exactly; `f300b2ce..bd06d021` touches exactly those two lines in SOURCES.md.
- Lesson Addendum + Addendum 2 and the SCORECARD § Corrections amendment disclose the amber state and carry the class rule (key on the row id, never a tail substring).

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | **improved** | C1 verifies (above); the drift class gained a carried rule (SKILL § Round 62 rule 3); corrections append-only with preserved defect bytes |
| coverage | **improved** | C2 verifies: new sourced plane (S418–S423, entry indexed, navigation 77/77 committed receipt) |
| operability | **improved** | C3 verifies: capability runs, output verifies, ledger row landed the same round; selftest + live + error paths re-run by the closure judge |
| depth | unchanged | no claim; entry detail verified under C2 |
| freshness | unchanged | no claim; recheck lines present on the new entry |
| adjacency | unchanged | no cross-domain evidence absorbed; L1-only/L2-floor standing disclosure restated |

No axis harmed: harm-watch receipts (`harmwatch-selftests-r62.txt`) show both
fail-closed checkers' selftests green at current bytes (55/55, 63/63) and
`mado-verify.sh` bytes untouched (sha256 prefix `050efc720599345a`); census
exit 0 with the identical warning set; SCORECARD diff inspected — only the
round-62 section is new plus the disclosed used-by amendment.

## 4. Discernment spot-check (non-author; ≥1 admit + ≥1 reject)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S420 (DwmGetCompositionTimingInfo, tier A) | admit | URL fetched live 2026-11-01 | **agree** | quote "Starting with Windows 8.1, this parameter must be set to NULL." is a verbatim page substring; ms.date 2018-12-05, git_commit `fa536415…`, updated_at 2025-07-01 all match the Gate row; page confirms the E_INVALIDARG promise and the cbSize requirement that ground K40/J24/D04 |
| S418 (DwmGetWindowAttribute, tier A) | admit | URL fetched live 2026-11-01 | **agree** | quote verbatim ("Retrieves the current value of a specified Desktop Window Manager (DWM) attribute applied to a window."); ms.date 2019-05-30 + same git_commit match; S_OK/HRESULT-error return vocabulary matches K38; teaches grounds the probe/tool getter |
| Treating D04 as an operator question / L0 line | reject (recorded as host finding, cause `[UNK]`) | the finding's re-derivation command, re-run by the closure judge | **agree** | the live re-run reproduces the undocumented `0x88980090` in both documented shapes — a host observation with a documented call shape and an undocumented result; nothing in lane scope changes either way, and the flip condition is named |
| Building a screen-capture probe this round | reject (held behind open L0) | `.ufo/l0-questions.md` (fleet repo) | **agree** | the r60 mado screen-capture-scope question is present and unruled; the rendered-pixel limit stays named rather than worked — routing around an open L0 is the required posture |

New-row quote check: both re-opened rows are NEW this round (S418, S420);
each Gate quote is ≤25 words and a verbatim substring of the opened page body
at the recorded anchor. Census validate re-run by the verifier:
`sources-census.sh validate … mado` → **exit 0**, `mado ok`, warning set
**36 W04 + 1 W01** — byte-consistent with the committed census-start/after
receipts and the r57–r61 warning set.

## 5. Trend verdicts (verifier)

- **expansion — improved.** One new sourced plane on uncovered ground: 6 new mined tier-A rows, 1 new indexed entry whose `source:` cites them, 1 new capability row; 76 → 77 knowledge files, index 77/77, used-by TARGET_MET at the final revision.
- **quality — improved.** A durable read-only observer with red/green-disclosed assertions, named-churn receipt discipline, and a crosscheck; corrections append-only with preserved defect bytes; the number-shape rule carried into SKILL. No admitted entry failed its re-check.
- **discernment — improved.** D04 kept `[UNK]` instead of a guessed cause (verified); the amber mis-aim disclosed and reverted byte-exact within the round (verified); three red selftest runs disclosed rather than smoothed (M62-3); the spot-check agrees with the gate on the sampled admits and rejects.

## 6. Routed defects (status-neutral; the lane must fix next round)

All are instances of the round's own M62-1 class (a number asserted beside a
command that does not re-derive it) or locator nits, in the round's report
records — none touches the claims:

1. **Total-line range mislabel (report § Landed changes; repeated in SCORECARD § Corrections (round 62), the LOG round-62 amendment, and the `df415ef3` commit subject):** "base `4c5435d8` → receipts tip `4fe4544`: 34 files, +1806/−1". Measured: `4c5435d8→4fe4544` = **35 files, +1830/−1**; the printed numbers equal `4c5435d8→bd06d021` (34 files, +1806/−1); the true final range `4c5435d8→df415ef3` = **35 files, +1860/−1** (the `df415ef3` amendment's own +30 LOG/SCORECARD lines are excluded from the printed figure).
2. **"wave receipts +441/−0" (report per-file list):** measured 466 at `4fe4544` / 442 at `bd06d021` (wave total incl. before-state + claims-declaration); 441 matches neither.
3. **"18 receipt files" (report landing row):** measured **20** `receipts/` files at `19407ef2` (22 wave files including before-state + claims-declaration).
4. **"Four commits" (report prose) vs five rows** in the same table (`4fe4544` is the fifth).
5. **Census range endpoint (entry H22; report C2 bullet):** "161-170 top-level in every committed execution" — committed probe run 2 shows `top_level` **160** (all-run range 160–170). The load-bearing invariants (14 cloaked, 13 visible, reasons 7 app + 7 shell + 0 inherited, `attr_failed` 0) hold in every committed run including run 2.
6. **Declaration spread (nit):** the claims declaration names source rows S418–S422; the landing carries S418–S423 (S423 GetWindowRect, the documented side of the already-declared frame-bounds join). No predicate changed after scoring; noted for the record.

Routed disposition: fix under SKILL § Round 62 rule 3 in the next round's own
records (append-only corrections; fleet-root report files are not lane-edited).

## 7. Notes for the operator

- SHONEN: the four boxes remain `[~]` lane-asserted with no named non-author verifier to date. Nothing this round upgrades them, and the closure judge did not write into `SHONEN.md` (only a non-author may write `[x]`). The boxes look fully checkable by a non-author review (SKILL decision tables/error patterns/checklists with resolvable sources; end-to-end tasks logged r57–r62; instructions self-contained; PROVINCE refined in-round) — the operator may commission that review.
- L1-only round: the ≥8-L2 dispatch floor still has no surface on this host; disclosed since r57 with the L0 line open. Unchanged, status-neutral.
- Security boundary: held by the lane per the report and by this verifier — no r56-era credential material was opened, diffed, or surfaced; only counts and clean-tree paths were touched.
