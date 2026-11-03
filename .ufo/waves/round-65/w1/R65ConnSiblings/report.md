# R65ConnSiblings — seat report (round 65, wave w1)

Read-only outside this seat. No install. No mutating git. Scratch
`/fast/scratch/hyaku/mado-r65/w1/R65ConnSiblings/` created, used, removed at exit.
Full scoped findings: `../R65ConnSiblings.md` (the Report-trailer path for this seat).

## What I ran (with rc)

| command | rc |
|---|---|
| `ls -d /home/vgpnk/Projects/shokunin/{kumitate,tsukuroi,tameshi}-shokunin/quality` | 2 per repo — **no `quality/` dir in any of the three** |
| `grep -rIln --exclude-dir=.git 'landing' <repo>` ×3 | 0 (hits only in `.jj/` and `.ufo/evidence|waves/` prose) |
| `grep -rIn --exclude-dir=.git -i 'landing-counters\|landing counters' <repo>` ×3 | 1 (no hits) |
| `grep -rIln 'landing-counters' shokunin/{scripts,tools,PROTOCOL.md,PROTOCOL-APPENDIX.md}` | 1 |
| `cd mado-shokunin && ls -l quality/landing-counters.sh` | 2 (absent — C2 before-state re-confirmed) |
| `grep -c -i 'surface.state register' <repo>/{PROVINCE,SCORECARD}.md` ×6 | 0; counts 0/0/0/0/0/0 |
| `grep -c '2026-11-03' <repo>/{PROVINCE,SCORECARD}.md` ×6 | 0; counts 0/0 / 0/**17** / 0/0 |
| `grep -n '2026-11-03' tsukuroi/SCORECARD.md \| grep -E 'surface\|register\|omarchy\|hypr'` | 1 (0 lines) |
| `grep -n -i 'omarchy' tsukuroi/SCORECARD.md` | 0 (2 hits, both round-1 pacman/boot prose) |
| `git -C <repo> log -3 --date=short --format='%h %ad %s'` ×3 | 0 (kumitate 2026-11-02 r73; tsukuroi 2026-11-03 r68; tameshi 2026-11-02 r71) |
| `ls -ld /home/vgpnk/Projects/shokuknow`; `wc -l merge/mado/MERGE-REPORT.md` | 0; 0 (136 lines, mtime 2026-10-24 23:33) |
| `LC_ALL=C comm` package vs lane knowledge basenames | 0 (65 package files, 78 lane files, 7 overlap, 58 absent) |
| `ls -la --time-style=full-iso mado-shokunin/considerthese` | 0 (9 files, newest 2026-10-28 18:46:52) |
| `grep -n -i 'considerthese' mado-shokunin/corpus/lessons/round-64.md` | 0 (`:168-174`, nine re-screened 2026-11-01) |
| `grep -n -i 'arm.liveness\|red arm' considerthese/2026-10-28.md` | 1 (no hits) |

## Findings

**S1 — Landing-counters overlap.** No sibling runs mado's four-leg leg; the lane's *shape* and most *legs*
have prior art, so C2 cites, never claims novelty: `kumitate/scripts/round-gate.mjs` (one command →
`ROUND_GATE: CLEAN|DRIFT`, hermetic `--selftest`, contract `kumitate-round-gate-v1`), `kumitate/scripts/
routed-ledger.mjs` (ledger leg), `kumitate/scripts/readme-map.mjs` (index leg), `kumitate/scripts/
cite-check.mjs` + `tsukuroi/tools/check-cited-receipts-r62.py` ("Cited-receipt landing gate") (citecheck leg),
`kumitate/scripts/counter-pins.mjs` (pin), `tameshi/tools/arm-liveness.py` (standing row sweep re-executed at
pinned revs). **`used-by` is the only leg with no sibling analogue.** mado's `SKILL.md:2589,2667,2746` shows
the name existed only as per-round receipts (`landing-counters-r60..r63.txt`), not a script.

**S2 — Register overlap.** None: `surface state register` = 0 in all six sibling PROVINCE/SCORECARD files;
tsukuroi's 17 `2026-11-03` lines are boot-chain / mkinitcpio / Linux v7.3 pin work (rc=1 on the surface
filter). mado `PROVINCE.md:145` `### Surface state register (2026-10-31, this host)` (7 `absent (2026-10-31)`
rows) is unshared territory — no collision, no sibling coverage; nearest shape precedent is
`tsukuroi/tools/check-freshness-r17.py` (knowledge-file freshness registry, not host-surface).

**S3 — Assimilation.** shokuknow reachable. Package: 147 rows / 69 entries (65 new-file + 4 amendments),
staged 2026-10-24, "nothing written into the lane repo"; 7 basenames already in lane, 58 absent, all 4
amendment targets present (appends). Six clusters derived from its knowledge table: IPC/framing,
focus-grab, idle-lock, gkeep geometry, two-literature, host bar/producer state. **Recommendation: SKIP** —
no cluster is the eight-group register re-derivation C1 froze and none is executable C2; clusters 3 and 6
(omarchy-era surface-state claims) are the ones that must *not* land before the 2026-11-03 re-derivation.

**S4 — Considerthese.** Nine files, newest mtime 2026-10-28 18:46:52 < the 2026-11-01 screen in
`corpus/lessons/round-64.md:168-174`; none newer, none uncovered → **no new adoptable proposal**.
Cross-lane note: tameshi's arm-liveness adopts "considerthese 2026-10-28 proposal 2"; mado's own
2026-10-28.md has no arm-liveness text (rc=1), so S4 is unchanged.

## Defects seen

- Seat-spec probe path defect: `grep -rn 'landing' <repo>/quality` targets a directory absent in all three
  sibling lanes (rc=2 each). Absence of `quality/` is not absence of instrument — they live in
  `kumitate/scripts/` and `{tsukuroi,tameshi}/tools/`. Bounded spec should name those dirs.
- No other defect; nothing opened from r56-era material; no credential-shaped output captured.
