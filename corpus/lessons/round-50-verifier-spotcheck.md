# Round 50 verifier spot-check — hyaku closure (non-author)

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
lane: mado (round 50, hyaku run 10 attempt 2)
lane tip: `74782d39e7697608917b5e909f0e8580aaa3e15c`; base `8ae47b957034ae21012bbf09173cca2c48be345e`
report: fleet `.ufo/reports/round-50/mado.md` (commit `1c4920a39fc75b5c7c8bf1106cc98d9d48603fbd`, author `mado-shokunin <mado@shokunin.local>`)

Dispatch/complete digest (`.ufo/watchdog.log`, mutable — copied per closure duty):
- 2026-10-27T02:45:41-03:00 launch mado round=50 pgid=755091 driver=hyaku-inline attempt=1
- 2026-10-27T03:26:40-03:00 lane-dead-no-report mado round=50; retry same round (attempt 1: L1 exited before WAVE-DONE without filing; w1 still had 9 seats in progress)
- 2026-10-27T04:49:13-03:00 lane-dead-no-report mado round=50; retry same round (attempt 1: operator run wrap-up mid-round; in-flight state committed for next-run inheritance)
- 2026-10-27T04:55:12-03:00 launch mado round=50 pgid=3051436 driver=hyaku-inline attempt=2
- 2026-10-27T06:25:36-03:00 complete mado round=50; hyaku-inline attempt=2

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-50/mado.md` | `mado-shokunin mado@shokunin.local 1c4920a39fc75b5c7c8bf1106cc98d9d48603fbd` | PASS |
| Report on origin | `git merge-base --is-ancestor 1c4920a3 origin/master` (fleet) | ancestor | PASS |
| SHONEN heading | `grep -c '^## SHONEN' .ufo/reports/round-50/mado.md` | 1 (`## SHONEN and tooling`) — one summary line for all four boxes instead of one line per box | PASS with defect D2 |
| Cited commits exist + ancestor of `master` | `git rev-parse --verify` + `git merge-base --is-ancestor <h> master` for `74782d39 8ae47b95 13631f24 1b37a59e d7c33df8 906178b6 470bfd77 8dbbf61a b4a79843 c12b588e a582e0e5` | all 11 OK ancestor | PASS |
| Lane pushed, no uncommitted round work | `jj-lane.sh state` + `git status --porcelain` | `ahead=0 behind=0 local=remote=74782d39e7697608917b5e909f0e8580aaa3e15c`; one untracked leftover `.ufo/wakes` (388 B index-check scratch note) | PASS with defect D3 |
| Prompt carries template contract | diff of dispatched prompt vs `templates/round-prompt.md` structure | sections 1–5 (MISSION/axes, claims, frontier, L2 floor, report contract) + §6 addendum + L1 mechanics; five child-lane items present (report path `:101`, SHONEN one-line-per-box `:118`, write scope `:399`, lands-last/cites-pushed-hash `:467`, pre-report `grep -c '^## SHONEN'` `:472`) | PASS |

Marker check: the report is substantive (claims, hashes, receipts, sections) — not a marker. Status `ok`.

## 2. Per-claim re-check (plain measurements over committed bytes; lane gates evidence-verified, not executed)

### C1 — coverage (sourced): `corpus/knowledge/hyprland-bind-key-match-r50.md`, `PRED-C1-r50`

- Before: `git cat-file -e 8ae47b95:corpus/knowledge/hyprland-bind-key-match-r50.md` → ABSENT (entry absent at base). After: EXISTS at `906178b6` and at tip `74782d39`. Matches report.
- Registry rows: 288 rows at base → 300 at tip (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` over `git show <rev>:corpus/SOURCES.md` and the worktree); 12 new rows S352–S363 present, status `mined`, opened 2026-10-27. Matches report.
- Knowledge entries: 65 (`git ls-tree <base> corpus/knowledge/`) → 66 at tip. Matches report.
- Predicate receipt `receipts/c1-at-data.txt`: final line `verdict=TARGET_MET rev=906178b6…`, exit 0. Controls `receipts/controls-c1.txt`: `TARGET_MISSED`, exit 1. Committed evidence consistent with the report.
- Falsification re-derived from committed seat reports: `w2/CritC1FrozenStub.md` — round-49 candidate bytes (present at base at `.ufo/waves/round-49/candidate/`, committed `dd2e827e`) pasted at the round-50 entry path + a single receipt-citation line → all 11 clauses 1, `TARGET_MET`; `v2-no-quotes` and `v3-wrong-usedby` mutants correctly MISS. `w2/ExecFreezeReplay.md` quantifies 81.7% shingle coverage of the round-50 entry by the round-49 candidate. `w2/CritFrozenNovelty.md` shows held mechanism facts (`stringToModMask` semantics, the full ternary, `update_mask` chain, `code:` parse chain) present under `corpus/` at base yet omitted from the entry's ground enumeration.
- **Verifier ruling: predicate MET (evidence-verified); claim falsified / honest stop, exactly as the lane reports.** The frozen counter certifies presence and binding, not novelty. Re-measured (entry/rows/receipts); counter itself not executed (lane-owned gate).

### C2 — operability: session-material gate v3 at `quality/check-session-material.py`, `PRED-C2-r50`

- Before: gate at base = 1,643 lines (v2). After: 2,149 lines at `906178b6` (v3). File present at both; growth consistent with the report.
- Predicate receipts `receipts/c2-at-data-nonce50117.txt` / `c2-at-data-nonce778899.txt`: `selftest=94/94 names=69/69 red=42/42 green=44/44` / `red=44/44 green=41/41`, both `verdict=TARGET_MET rev=906178b6…`, exit 0. Controls `receipts/controls-c2.txt`: v2 blind default `TARGET_MISSED`, exit 1. Committed evidence consistent.
- Falsification re-derived: `w2/CritC2FrozenStub.md` — 7,046-byte replacement gate emitting a canned 94/94 transcript and spraying all three rule tags scores `TARGET_MET` (M4); partial rule removal (M1) and single-tag parrot (M2) correctly MISS. The frozen counter cannot certify transcript honesty or exact rule attribution.
- **Verifier ruling: predicate MET (evidence-verified); the claim as declared (independent certification of gate honesty) is falsified / honest stop, exactly as the lane reports.** The installed v3 gate remains the committed artifact; its behavior on the frozen fixtures is receipted, but the counter's certification power is what w2 bounded. Re-measured (file/receipts); counter not executed (lane-owned gate).

### No owned axis harmed

`git diff 8ae47b95 74782d39 -- SCORECARD.md`: round-50 record appended (claims with self-verdicts, three capability rows, planned round 51), axis table re-derived at `a582e0e5` (`receipts/axis-tip.txt`: navigation 66/66, calibration 86/86, operability 12/12, `checked=3 mismatched=0`; base `65/65 86/86 12/12`). `SKILL.md` (+5, cross-reference to the new entry), `corpus/QUALITY.md` (+14, criteria 100–102 with red/green receipts), `corpus/README.md` (+2, index row + frontier note) — all additive. `LOG.md` +11 lines, round-50 entry with pointers. No axis row harmed.

### Other exercised checks (evidence-verified)

- Gate selftests receipt `receipts/selftests.txt`: session-material 94/94, hostguard 45/45, wave-done 58/58, exits 0. Hostguard `tools/mado-hostguard.py` present (1,158 lines). Wave-done gate present (1,018 lines).
- `receipts/check101-w1-final.txt`: `reports=54 declared=19 exists=15 absent=4 verdict=FAIL`, exit 1 — by design; the four ABSENT are `w1/MutC1Tool`'s seat-name-prefixed paths (M50-5).
- Census `scripts/sources-census.sh validate --root … mado` → exit 0, `ok` (run at closure). W04 duplicate-URL-across-scopes warnings: pre-existing class; S353/S354 join it (same upstream files as held S303/S317/S318 at different scopes/anchors).
- **Defect D1 (evidence):** report and `LOG.md` assert a final `check-wave-done.py --rev 74782d39 … → waves=2 settled=2 verdict=OK`; the only committed receipt (`receipts/wave-done-r50.txt`, from `b4a79843`) was measured at `8dbbf61a` and reads `waves=1 settled=1` (w2 results landed later, `c12b588e`). No committed two-wave receipt exists. Claimed ≠ re-executed; the pointer does not resolve at closure. Gate selftest (58/58) and the w1 verdict are committed; the final two-wave verdict is not.

## 3. Discernment spot-check (LEARNING.md — checked from outside)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S352 admit (KeybindManager.cpp @ efb50993, quote :369) | admit, tier A | pin `.ufo/waves/round-50/fetch/Hyprland-KeybindManager.cpp:369` + live URL (scout) | agree | quote verbatim at the cited pin line; pin sha256 `8d8f35fc…` matches the entry's S352 citation; live fetch contains the quote |
| S355 admit (libxkbcommon keysym.c:268) | admit, tier A | pin `:268` + live URL (scout) | agree | quote verbatim; teaches the name-resolution semantics the entry relies on |
| S359 admit (wiki Binds.md @ d5f07c60:40) | admit, tier A | pin `:40` + live URL (scout) | agree | quote verbatim; documented key-field surface |
| S361 admit (own-work `binds-live-r50.txt:9`) | admit, tier A | pin `:9` (`binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0`) | agree | committed shape-only receipt; digest equals round-49 capture per the lesson |
| Reject: ArchWiki `Hyprland` | reject (no 0.56.2 bind behaviour) | live page (scout, full text) | agree | `0.56.2` ×0, `resolve_binds_by_sym` ×0, `xkb_keysym` ×0 — page states no version-pinned bind behaviour; flip (pinned primary) already held in S352–S353 |
| Reject: `wiki.hypr.land/0.56.0/.../Binds/` | reject (no commit anchor; URL moves) | live HTML (scout, 3,864 lines) | agree | zero `\b[0-9a-f]{40}\b` tokens (only 64-char asset fingerprints); rendered archive page, no commit anchor |
| New-row quotes (all 12) | — | committed pins, cited lines | agree | every ≤25-word quote verified verbatim at its cited pin line (S352:369, S353:1484, S354:1711, S355:268, S356:3, S357:101, S358:471, S359:40, S360:219, S361:9, S362:116, S363:14); `ScrRowsR50/verify-quotes.sh` "ALL QUOTES VERIFIED" independently confirmed by re-read |

Method note: all 12 pin files byte-equal the round-49 pins (`w1/ExecFetchR50/cmp-verify.txt`: `cmp_equal=14 differ=0 ownwork=1`). A fresh `sources-census.sh validate` exits 0 at closure. No disagreement became a lesson candidate: the gate's admits and rejects both hold under re-opening.

## 4. Trend verdicts (with evidence)

- **expansion: unchanged.** Census 288→300 rows and knowledge 65→66 re-measured, but the declared C1 novelty was falsified (81.7% recycled candidate, held facts omitted) and the lane itself claims no fresh sourced expansion. An entry landing without its claimed novelty is not net expansion; nothing was harmed.
- **quality: unprovable-but-better.** Gate v3 (selftest 94/94), hostguard (45/45), wave-done (58/58), criteria 100–102 landed with committed receipts — but w2's 7,046-byte parrot proves the frozen counter cannot certify gate honesty, so the improvement cannot be proven as measured. Matches the lane's "improved with bounded confidence", graded in the protocol vocabulary (round-49 precedent).
- **discernment: improved.** Both counter weaknesses were found by the lane's own w2 falsification and disclosed, not hidden (M50-6/7/8/9); frozen predicates were not weakened or re-frozen post-w2; the prohibited `agent://all` broadcast was self-recorded as a conformance failure. This closure's outside spot-check agrees with every sampled gate decision.

## 5. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| coverage | unchanged | C1 predicate MET but the novelty/ground claim falsified; lane claims no net expansion; entry exists but is compromised — no verified axis move |
| operability | improved | v3 gate installed and operating (receipts at two nonces; controls miss); hostguard + wave-done instruments landed with green selftests; three capability rows demonstrated in-round |
| depth | unchanged | no SKILL.md decision-table/error-pattern delta beyond a cross-reference pointer |
| freshness | unchanged | no stale-entry re-verification beyond the operator-state receipts (cache digest changed by operator use; hypr configs byte-identical) |
| calibration | unchanged | SCORECARD/SHONEN self-assessment matches observed repo state (axis table MATCH, no overreach found) |
| adjacency | unchanged | assimilation package rejected on scope; no cross-domain absorption |

## 6. Routed defects for the lane (fix next round)

1. **Final WAVE-DONE evidence missing** — report (`##` intro) and `LOG.md` round-50 entry assert `check-wave-done.py --rev 74782d39 … waves=2 settled=2 verdict=OK`; commit the final re-run receipt at the integration tip (or correct both texts). Committed receipt stops at `8dbbf61a`, `waves=1`.
2. **SHONEN section shape** — one summary line covers four boxes; the contract is one line per box (`[~]` + pointer). Minor.
3. **Untracked leftover** — `.ufo/wakes` (388 B) sits uncommitted in the lane repo; commit or remove it.
4. **Registration manifest self-row** — M50-9's cleanup (remove the unverifiable self-digest row from the fetch checksum manifest) is still open.
5. **Carry-forwards recorded by the lane itself** (already in SCORECARD planned round 51): C1 freshness baseline must include `.ufo/waves/round-*/candidate/`; C2 needs independent behavioral fixture execution with exact rule attribution; tracked lane-level tool ledger (RevLedgerR50: `mado-hostguard.py`, `mado-keysym.py` uncovered).

## 7. Items for the operator (notes, not lane defects)

- SHONEN boxes remain four `[~]` historical assertions; no outside-lane promotion verifier exists. Promotion stays operator-owned.
- w1's 54 results rows carry null outputs with non-blank dispatcher notes (kernel-restart class, per criterion 102); w2's 32 seats all returned outputs. The lane integrated w1 from the 54 committed seat reports — the report discloses this; the wave-done checker accepts null+note as settled.
- The lane self-reported one prohibited `agent://all` broadcast; recorded as a conformance failure in the report. Status-neutral; no further broadcast was sent.
- Fleet root carries an untracked `.ufo/reports/round-61/kake.md` (another lane's in-flight report) — untouched per closure scope.
