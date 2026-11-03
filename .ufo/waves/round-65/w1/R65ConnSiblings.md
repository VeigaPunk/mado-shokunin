# R65ConnSiblings — sibling-overlap + assimilation screen (round 65, wave w1)

Read-only everywhere outside this seat. Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`
@ `cb63ab13ccaf85191318701d5db5ace050bd5bd4`; contract `.ufo/waves/round-65/claims-declaration-r65.md`
read first. Scratch `/fast/scratch/hyaku/mado-r65/w1/R65ConnSiblings/` (created, used, removed).
No tool installed. No mutating git run.

## S1 — Landing-counters overlap: no sibling has the leg; every leg and the aggregate *shape* do have prior art

Commands (rc captured explicitly):
- `ls -d /home/vgpnk/Projects/shokunin/{kumitate,tsukuroi,tameshi}-shokunin/quality` → all three
  `No such file or directory`, rc=2 (per repo). The seat's prescribed `grep -rn 'landing' <repo>/quality`
  is therefore a dead path on all three (rc=2, not "no hits").
- `grep -rIln --exclude-dir=.git 'landing' <repo>` ×3 → only `.jj/`, `.ufo/evidence|waves/` prose; zero hits
  under `scripts/`, `tools/`, `corpus/`, `PROVINCE.md`, `SKILL.md`.
- `grep -rIn --exclude-dir=.git -i 'landing-counters|landing counters|landing-counters.sh' <repo>` ×3 → 0 hits, rc=1.
- `grep -rIln 'landing-counters' /home/vgpnk/Projects/shokunin/{scripts,tools,PROTOCOL.md,PROTOCOL-APPENDIX.md}` → 0 hits, rc=1.
- `cd mado-shokunin && ls -l quality/landing-counters.sh` → `No such file or directory`, rc=2 (C2's before-state re-confirmed).

**Verdict S1:** no sibling lane runs a standing leg named or scoped as mado's landing-counters, so C2's
*leg set* (navigation index / used-by / ledger / citecheck over the round receipts) is genuinely new in the
fleet. But C2's *shape* is not new, and each leg already has a sibling instrument — C2 must cite prior art,
never claim novelty of "one command → green verdict over committed bytes":

| mado leg / property | sibling prior art (read, header-verified) |
|---|---|
| navigation index (N/N rows) | `kumitate-shokunin/scripts/readme-map.mjs` — "corpus coverage-map bimap gate", contract `kumitate-readme-map-v2` |
| used-by | **none found** (only mado's own `quality/counters/c3-r56-used-by.py`; sibling `used-by` hits are corpus prose, not instruments) |
| ledger | `kumitate-shokunin/scripts/routed-ledger.mjs` — `ROUTED_LEDGER: CLEAN|DRIFT`, contract `kumitate-routed-ledger-v2` |
| citecheck (missing=0) | `kumitate-shokunin/scripts/cite-check.mjs` (`kumitate-cite-check-v1`); `tsukuroi-shokunin/tools/check-cited-receipts-r62.py` — header: "Cited-receipt landing gate … reads one revision's committed bytes and counts what they CITE" |
| one command, single green verdict, hermetic `--selftest`, pinned | `kumitate-shokunin/scripts/round-gate.mjs` — `ROUND_GATE: CLEAN|DRIFT`, contract `kumitate-round-gate-v1`, `--selftest` hermetic (`SKILL.md:609,716-718`); `kumitate-shokunin/scripts/counter-pins.mjs` — `COUNTER_PINS: CLEAN` (`SKILL.md:625`) |
| standing row sweep re-executed at pinned revs | `tameshi-shokunin/tools/arm-liveness.py` — `ARM_LIVENESS`, "pins one committed input per arm … RE-EXECUTES the row" |
| hosting pod / freshness registry precedent | `tsukuroi-shokunin/tools/check-freshness-r17.py` — "freshness-recheck gate" over a registry of dated, append-only notices; `tsukuroi-shokunin/tools/tsukuroi-census.sh` — six-plane host census, one command |
| landing-adjacent receipt diff | `kumitate-shokunin/scripts/report-receipt-diff.mjs` — contract `kumitate-report-receipt-diff-v3` (round 64) |

Extra in-lane datum: mado's `SKILL.md` already *names* hand-run `landing-counters-r60…r63.txt` receipts
(`SKILL.md:2589,2667,2746`), i.e. the name existed as a per-round receipt, not as a script — consistent with
C2's deficiency sentence ("every round re-types 4+ ad-hoc counter commands").

## S2 — Register overlap: no sibling touched a desktop-surface register this run

Commands (counts, rc=0 for every file that exists):
- `grep -c -i 'surface.state register' <repo>/{PROVINCE,SCORECARD}.md` → kumitate 0/0, tsukuroi 0/0,
  tameshi 0/0 (all six files present).
- `grep -c '2026-11-03' <repo>/{PROVINCE,SCORECARD}.md` → kumitate 0/0, tsukuroi **0 / 17**, tameshi 0/0.
- `grep -n '2026-11-03' tsukuroi/SCORECARD.md | grep -i -E 'surface|register|omarchy|hypr'` → **0 lines**, rc=1.
  The 17 dated lines are tsukuroi rounds 64–68: boot-chain / mkinitcpio-42 / Linux v7.3 pin-watch /
  knowledge-source-ref gate (`SCORECARD.md:4705,4727,4789,4810,4902,5014,5099`).
- `grep -n -i 'omarchy' tsukuroi/SCORECARD.md` → 2 hits, both round-1 pacman/boot prose (`:26`, `:204`).
- Recency: `git -C <repo> log -3 --date=short --format='%h %ad %s'` → kumitate `3c369336 2026-11-02`
  round-73 spot-check; tsukuroi `3f6edcc9 2026-11-03` round-68 declaration; tameshi `f20ba482 2026-11-02`
  round-71 spot-check. rc=0 each.

**Verdict S2:** the desktop-surface register is unshared territory. `mado-shokunin/PROVINCE.md:145`
carries `### Surface state register (2026-10-31, this host)` with `grep -c 'absent (2026-10-31)'` = **7**
— no sibling holds, edits or cites a comparable block, and no sibling's run-15 activity is on desktop
surfaces. C1 collides with nothing and can cite no sibling prior art for the register itself; the nearest
shape precedent is tsukuroi's `check-freshness-r17.py` registry gate (a *knowledge-file* freshness registry,
not a host-surface register) — useful as precedent, not as coverage.

## S3 — Assimilation: shokuknow is reachable; adopt nothing this round

Reachability: `ls -ld /home/vgpnk/Projects/shokuknow` → present, rc=0, dir mtime 2026-10-27 14:35.
`merge/mado/MERGE-REPORT.md` = 136 lines, 18,208 B, mtime 2026-10-24 23:33, "Staged by
`corpus-expansion-1`. **Nothing was written into the lane repo.**": 147 rows, 69 entries
(65 new-file + 4 amendments), first staged id `S203`.

Adoption state measured (`LC_ALL=C comm` of package basenames vs lane `corpus/knowledge`, rc=0):
package 65 files, lane 78 files, **7 already in lane**, **58 absent**; all 4 amendment targets
(`ipc-contract-r25.md`, `dispatcher-semantics-r25.md`, `waybar-module-text-route-r25.md`,
`dispatcher-surface-and-request-grammar-r26.md`) are present in the lane → they would be appends.

The report has no `## theme` section (section list: `What gets appended` / `Knowledge files to add` /
`Rows no entry rests on` / `Rows whose source the lane already holds` / `used-by` corrections / `Adopt
checklist`); themes below are the report's own knowledge-file clusters:

1. **IPC contract & framing** (r1/r2/r8/r13/r29–r31: `ipc-contract`, `dispatcher-semantics`,
   `event-delivery-limits`, `socket-*`, `request-limits-upstream`) — corpus content: fits **neither** C1
   (no register rows, no 2026-11-03 probes) nor C2 (not executable).
2. **Focus-grab** (r8–r14, 9 entries) — neither.
3. **Idle-lock** (r7–r15, 7 entries, incl. `idle-lock-offered-in-the-bar-r15`, `idle-lock-runtime-state-r28`)
   — these *are* surface-state claims, so they are C1-*relevant*; but landing them would add register rows
   that C1's frozen predicate does not count and that this host has not re-derived today: it **adds
   freshness work instead of satisfying the predicate**.
4. **gkeep rendered geometry** (r8–r15, 6 entries) — neither.
5. **Two-literature coverage** (r7/r16/r25/r26) — neither.
6. **Host bar / producer state** (r26–r31) — same class as (3): omarchy-era surface-state reads, pre-return,
   unreopened on 2026-11-03.

**Recommendation: SKIP (adopt none).** No theme is the eight-group register re-derivation C1 froze, and none
is an executable instrument C2 froze; the package is a 147-row corpus expansion whose own `Adopt checklist`
step 1–2 requires re-reading every Gate block and spot-reopening rows — a round of its own, not an append to
a round whose claims are a register block and a script. Closest fit if one must be named: theme 3/6
(surface-state claims) — and it is precisely the cluster that must **not** land before the 2026-11-03
re-derivation, because appending omarchy-era state cells beside the new register would recreate the defect
C1 exists to remove. Package stays staged at 2026-10-24 bytes; nothing in the lane changed.

## S4 — Considerthese: no new adoptable proposal

- `ls -la --time-style=full-iso mado-shokunin/considerthese` → **nine** files, rc=0, dir mtime
  2026-10-28 18:46:52: `2026-10-19.md` (2026-10-19 22:04:36), `2026-10-20.md` (10-20 10:18:29),
  `2026-10-21.md` (10-21 11:18:18), `2026-10-22.md` (10-23 00:11:41), `2026-10-23.md` (10-23 15:13:55),
  `2026-10-24.md` (10-24 20:05:26), `2026-10-25.md` (10-25 11:06:33), `2026-10-26.md` (10-26 13:17:13),
  `2026-10-28.md` (10-28 18:46:52).
- `grep -n -i 'considerthese' corpus/lessons/round-64.md` → `:168-174`: "Mined all nine `considerthese/`
  files again this round (directory listing + mtimes re-run 2026-11-01 — no new files since the r58 mining,
  the same nine with unchanged mtimes that r63 screened): no adoptable proposal."

Comparison: newest mtime **2026-10-28 18:46:52 < screen 2026-11-01**; set size 9 = the nine screened; every
file is covered. Files newer than the screen: **none**; files not covered: **none**.
**Verdict S4: no new adoptable proposal.**

Cross-lane note (no action): `tameshi-shokunin/tools/arm-liveness.py:2-4` says it adopts "the operator's
considerthese 2026-10-28 proposal 2, counter-arm liveness check". Mado's own `considerthese/2026-10-28.md`
has no `arm liveness` / `red arm` text (`grep -i` → 0 hits, rc=1), so that proposal is not in mado's file set
and does not reopen S4.

## Findings for the L1 (bounded, no predicate change proposed)

1. **C2 wording risk (only actionable item):** forcing the C2 after-state through the frozen counter is fine,
   but the *prose* around it must not say "no lane has a standing multi-leg instrument". False:
   `kumitate/scripts/round-gate.mjs` (one command, `ROUND_GATE: CLEAN|DRIFT`, hermetic selftest, pinned) and
   `tsukuroi/tools/check-cited-receipts-r62.py` ("cited-receipt landing gate") already exist. Correct claim:
   consolidation of mado's four ad-hoc landing legs into one pinned, selftested script — with the two files
   above cited as prior art for shape and for the cited-receipt leg respectively. `used-by` is the only leg
   with no sibling analogue.
2. **C1 has no sibling prior art to cite and no collision to avoid**; nearest shape precedent is
   `tsukuroi/tools/check-freshness-r17.py` (registry of dated append-only freshness re-checks) — citable as
   precedent for a *register* instrument, explicitly not coverage of host surface state.
3. **Assimilation: none — package reachable (`/home/vgpnk/Projects/shokuknow`, MERGE-REPORT 2026-10-24),
   6 clusters, none fits C1 or C2; skip, stays staged.** Lane knowledge count 78 (7 of the package's 65
   new-file basenames already present).
4. **Considerthese: no new adoptable proposal** (nine files, all ≤ 2026-10-28, screened 2026-11-01).

## Defects seen

- None material. One probe-design note: the seat spec's `grep -rn 'landing' <repo>/quality` names a directory
  that does not exist in any of the three sibling lanes (rc=2 each). Absence of `quality/` is **not** evidence
  of absence of an instrument; the instruments live in `scripts/` (kumitate) and `tools/` (tsukuroi, tameshi),
  and the prior art above was found there. A future seat spec should grep `scripts/ tools/ corpus/` instead.

## Command ledger (all read-only; rc as printed)

| # | command | rc |
|---|---|---|
| 1 | `ls -d .../{kumitate,tsukuroi,tameshi}-shokunin/quality` | 2 (per repo) |
| 2 | `grep -rIln --exclude-dir=.git 'landing' <repo>` ×3 | 0 |
| 3 | `grep -rIn --exclude-dir=.git -i 'landing-counters\|landing counters' <repo>` ×3 | 1 (no hits) |
| 4 | `grep -rIln 'landing-counters' shokunin/{scripts,tools,PROTOCOL.md,PROTOCOL-APPENDIX.md}` | 1 |
| 5 | `cd mado-shokunin && ls -l quality/landing-counters.sh` | 2 |
| 6 | `grep -c -i 'surface.state register' <repo>/{PROVINCE,SCORECARD}.md` ×6 | 0 (counts 0,0,0,0,0,0) |
| 7 | `grep -c '2026-11-03' <repo>/{PROVINCE,SCORECARD}.md` ×6 | 0 (0,0,0,17,0,0) |
| 8 | `grep -n '2026-11-03' tsukuroi/SCORECARD.md \| grep -E 'surface\|register\|omarchy\|hypr'` | 1 |
| 9 | `git -C <repo> log -3 --date=short --format='%h %ad %s'` ×3 | 0 |
| 10 | `ls -ld /home/vgpnk/Projects/shokuknow` ; `wc -l merge/mado/MERGE-REPORT.md` | 0 ; 0 (136) |
| 11 | `LC_ALL=C comm` package-vs-lane knowledge basenames | 0 (7 present / 58 absent) |
| 12 | `ls -la --time-style=full-iso mado-shokunin/considerthese` | 0 (9 files) |
| 13 | `grep -n -i 'considerthese' mado-shokunin/corpus/lessons/round-64.md` | 0 (`:168-174`) |
| 14 | `grep -n -i 'arm.liveness\|red arm' mado-shokunin/considerthese/2026-10-28.md` | 1 |
