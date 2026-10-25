# Round-38 verifier spot-check — mado (non-author)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-25
lane HEAD measured: f9057de60896d5c91a879c27fec24a8a9c010038 (base f6e3247f73152a39afb86066af48f3cedf95fb0a)
report: .ufo/reports/round-38/mado.md (fleet, 7 commits, all `mado-shokunin <mado@shokunin.local>`, 8a1cbcd3..9386c91f)
dispatch digest (watchdog.log, mutable — copied here): launch 2026-10-25T10:39:13-03:00 `launch mado round=38 pgid=2523589 driver=hyaku-inline attempt=1`; complete 2026-10-25T12:49:09-03:00 `complete mado round=38; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| check | result |
|---|---|
| report committed by lane identity | PASS — `git log --format='%an %ae' -- .ufo/reports/round-38/mado.md` → 7 commits, all `mado-shokunin <mado@shokunin.local>` |
| SHONEN heading, one line per box | PASS — 4 lines, all `[~]` with pointers, mirrors SHONEN.md at HEAD |
| cited lane commits exist + ancestor of `master` | PASS — bb1adce (report header tip), f6e3247, f9057de, 58e55ec, b6c1d31, efb0ec2, 3f14bd2, b8400aa7, c44873e7, 22f600f1 all `merge-base --is-ancestor … master` |
| pushed / ahead=0 | PASS — `scripts/hyaku/jj-lane.sh state` → ahead=0 behind=0 |
| uncommitted round work | DEFECT — working tree carries 3 modified seat reports (`.ufo/waves/round-38/w1/reports/{RevEntryBound,RevRegistry,ScoutS253}.md`, +187/−7) at closure; next round must commit or revert |
| prompt carries template contract | PASS — `.ufo/prompts/mado-round-38.md` (753ba3f5, lane identity): all 5 round-level items + 4 child-lane §2b items present; route map consistent |
| report minimum content | DEFECT (status-neutral) — no `Sources & frontier` section (SOURCES 207→211 lives only in SCORECARD prose; census never cited in report) and no `Trend verdicts` section; both are conformance defects per the marker rule, not marker predicates |
| report vs later lane errata | DEFECT — addendum 5 (9386c91f, 11:26:06) repeats RevCensusBefore's "frozen pair 19/19 at freeze rev" refinement, refuted by the lane's own later errata (c46f868 11:35:43 dispute record; f551b70 12:25:59 resolution). Correction belongs in r39's report or an appended erratum; the filed bytes are never rewritten |

Marker predicate: not a marker — real work, evidence pointers, checkable hashes throughout. Status `ok`.

## 2. Claims — re-measured vs evidence-verified

Gate standard binds: the counters/checkers are lane-owned gates; this closure verified committed evidence (receipts, digests, seat transcripts, git mechanics) and did not execute them. Plain measurements run here: git diffs, `grep`/`wc` over committed bytes, receipt reads. Three read-only reviewer seats re-checked C2/C3 evidence, lane health, and discernment mechanics.

### C1 — calibration (v3 re-grounding counter + discrimination gate): FAILS AS DECLARED

- Before, re-measured: `receipts/before-discrimination-v2.txt` (committed at the freeze) ends `controls=19 correct=13/19 verdict=TARGET_MISSED` — matches the report. v2-admitted cribs visible line-by-line (c1-duprow, c1-nolineage, c1-r28-verbatim, c2-forged, c2-docconn, c2-proc-mismatch all `ok=0`).
- After, evidence-verified: `receipts/after-discrimination-v3.txt` (added in b6c1d31) ends `controls=19 correct=19/19 verdict=TARGET_MET`. But both instruments changed after the freeze:
  - `git diff 58e55ec 859d0cf -- quality/counters/c1-r38-event-ground.py` → clause c uniqueness patch (later shown verdict-no-op by the f551b70 replay: frozen counter clause j at :223 already enforced `len(rows.get(i,[]))==1`).
  - `git diff 58e55ec b6c1d31 -- .ufo/waves/round-38/controls/manifest.json` → near-total rewrite (101→256 lines); `c1-duprow` write op changed from `append` (file end) to `py` insert after `| S217 |` (inside the table).
- Adjudication of the recorded seat dispute (RevCommitChain/RevFrozenClaims vs RevCensusBefore, LOG c46f868): re-derived from committed bytes — `registry_rows()` in the frozen counter parses only lines inside the `## Registry` section (`section(text, "## Registry")`, frozen blob :135-142). The frozen manifest's duprow appends the second S189 row at file end → never parsed → clause j never attacked → observed TARGET_MET → frozen counter × frozen manifest = **18/19** at any rev. This matches the 859d0cf contemporaneous message ("c1-duprow crib was passing"), the RevFrozenClaims replay (18/19 at both data and freeze revs), and the f551b70 cross-pair resolution (frozen×frozen 18/19; frozen×landed 19/19; landed×frozen 18/19; landed×landed 19/19). RevCensusBefore's "19/19 at the freeze rev" is refuted; its "HEAD × frozen = 18/19" is confirmed.
- Ruling (registration freeze contract, lines 6-7: "any later change to a counter is a new predicate and the claim it belongs to then fails as declared"; the manifest is a named predicate component): the landed 19/19 rests on the post-freeze manifest rewrite `b6c1d31` → **the C1 claim fails as declared; the repaired pair's 19/19 is a new predicate requiring re-registration** (fresh freeze + verification in a future round). The lane declared this honestly (errata 3f14bd2, report addendum RevCommitChain major, f551b70) — an honest stop, not concealment.
- C2-of-C1 note: the report's C1 "before/after" for the counter itself (admitted 1/2 at base → 2/2 at b6c1d31/tip) is corroborated by RevFrozenClaims verbatim re-runs; the failing element is the frozen-pair discrimination, as ruled above.

### C2 — operability (eventq live triplet): VERIFIED (evidence)

- Reported after: `fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET` + `live-detail replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1`.
- Committed evidence: `receipts/eventq-live.txt` pins `tool_sha256=436f550e…`, `verdict=CLEAN`, ts 2026-10-25T11:00-03:00 (header restored 4aad0e8); `receipts/after-discrimination-v3.txt` line 10 `control=c2-live … ok=1`; RevLiveTriplet re-derived the triplet ~15 min post-freeze (same socket2 inodes, same client graph, `OVERALL: AGREE` from /proc, `markers_observable=no` corroborated by `debug:disable_logs int:1`) — PASS; RevFrozenClaims verbatim re-runs at b6c1d31 and tip 23a0e0f reproduce the exact reported line.
- Defect: no standalone committed after-receipt for `c2-r38-eventq.py` exists (quoted output lives in the report + seat transcripts only). Route: commit the receipt at tip or cite `after-discrimination-v3.txt` as the committed verdict evidence.
- Routed (lane-authored, to r39): SentSocketSafety HIGH — committed `eventq-live-ss.txt` is a full `ss -xpa` table (190 KB, 147 pids incl. 1password/gnome-keyring/ssh/docker) on a public repo; regenerate as the tool's census-only `--snapshot-out` (keep ≥1 non-socket2 row for the `full_table` clause — RevC2v3 F1 confirms a minimal export still passes). RevC2v3 residuals F1/F2 (snapshot-out crib survives v3; proc clause verifies digests/inodes/AGREE but not holder pids) → r39.

### C3 — coverage (request-socket admission): VERIFIED

- Entries: `git ls-tree` — all three absent at freeze 58e55ec and base f6e3247, added by 245065c, present at HEAD.
- Frozen tokens: flags (`flag list`, `select instance`), r8 (`poll(pollfds`, `1023`), limits (`REQUEST_LIMIT`, `FOLLOW_QUEUE_LIMIT`) — all present in HEAD committed bytes (`git show HEAD:… | grep -c`); no predicate drift in registration.md (sole commit 58e55ec). Note: the counter's own flags tokens were substituted (`select instance`/`force state refresh` for `flag list`, RevDomCounter) — freeze-internal divergence; the entry carries all tokens and the counter discriminates (probe: drop `force state refresh` → 2/3 MISSED), so the claim verifies at HEAD.
- Receipts: `receipts/before-c2.txt` `admitted=0/3 … rev=f6e3247… exit=1`; `receipts/after-c2.txt` `admitted=3/3 … exit=0`. Minor: report/SCORECARD say "at efb0ec2" but the committed receipt pins rev 3674cf28 — citation slippage, verdict unaffected (RevFrozenClaims: 3/3 at b6c1d31 and tip 23a0e0f too).
- Refusals: 4 recorded in `corpus/lessons/round-38.md` :40-43 with evidence pointers. Re-opened: r29's "requests capped at 64 KiB" is chonkstep's own cap (S277 :61 re-fetched verbatim) — refusal agrees; r28's null-channel reasoning consistent with the 942 KB log having zero marker lines. SCORECARD.md:2420 stale ("2 refused" vs corrected 3) — self-defect routed.

## 3. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C3 verified 0/3→3/3, entries on unheld ground, tokens intact |
| operability | improved | C2 verified (triplet pinned, live clause TARGET_MET, verbatim re-runs at two revs) |
| calibration | unchanged | C1 fails as declared (18/19 frozen pair; 19/19 = new predicate pending re-registration); SCORECARD diff 15+/0−, no score touched |
| depth / freshness / adjacency | unchanged | not claimed; SCORECARD untouched |

No owned axis harmed.

## 4. Discernment spot-check

| item | decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S158 admit (r8 live bound) | admit | raw.githubusercontent HyprCtl.cpp@efb5099 re-fetched: sha256 798b7c6c… matches GATE + row; quote `int ret = poll(pollfds, 1, 5000);` verbatim at :2264 | agree | 5-second poll bound confirmed at the host's own commit |
| S253 admit (upstream ceilings) | admit | Unix.cpp@a1c2428f re-fetched: sha256 3ba8e461… matches; `REQUEST_LIMIT = 1024*1024`, `FOLLOW_QUEUE_LIMIT = 64*1024` verbatim at :43-44 | agree | upstream-ahead framing correct (host tag 404s) |
| S277 admit (community tier) | admit | chonkstep docs re-fetched: sha256 ff561fe0… matches; :61 "Requests are capped at 64 KiB…" verbatim | agree | tier-C row used only as cross-check, not load-bearing |
| r29 socket-client reject | reject | package body + S277 :61 | agree | conflates chonkstep's own request cap with upstream's follow-queue bound |
| r28 host-measurement reject | reject | package body + S226 log premise | agree | zero marker counts under `debug:disable_logs=1` is a null channel (measured r37) |
| S277 row quote | — | `grep -cF` quote occurs once; 7 words | agree | ≤25-word quote floor honored (all 6 Gate quotes: 2-8 words) |

`scripts/sources-census.sh validate --root … mado` exit=0: 6 pre-existing W04 duplicate-url warnings, 1 W01 (S277 tier-C mined used-by), final `ok`. `## Mistakes` present with 3 items (freeze-discipline failure; refusal-count correction; S258 header omission).

## 5. Trends

- expansion: improved — 3 entries admitted re-grounded, S-rows 207→211 (SCORECARD capabilities table), staged register left unassimilated rather than bulk-appended (f9057de corrected refusal).
- quality: improved — all 6 Gate receipt digests recompute to the GATE values; entries byte-verified against first-party sources; registry pins/anchors/sizes corrected (b8400aa7). Freeze-discipline failure is process, recorded honestly under calibration (unchanged) and Mistakes.
- discernment: improved — 4 refusals with re-opened evidence (sampled agrees), id collisions (15) detected and confined to the refused register block.

## 6. Routed defects for round 39

1. **Re-register the C1 repaired predicate**: fresh freeze of the discrimination manifest + counters, verify 19/19 under the new registration; until then calibration holds no verified r38 move.
2. Correct the fleet report's refuted addendum-5 refinement (frozen-pair 19/19 at freeze rev) in r39's report or an appended erratum.
3. Regenerate `receipts/eventq-live-ss.txt` as a census-only snapshot (SentSocketSafety HIGH); commit the eventq counter's after-receipt or cite `after-discrimination-v3.txt`.
4. Instrument residuals already routed by the lane and confirmed: RevC1v3 F1/F2/F4, RevC2v3 F1/F2, MutC1/MutC2 control gaps, LabratProcProof reachability, LabratClockSkew holes, request-ground frozen control set (f551b70), SCORECARD "2 refused"→3 staleness.
5. Resolve the 3 uncommitted seat reports in the working tree (commit or revert) before r39 dispatch.
