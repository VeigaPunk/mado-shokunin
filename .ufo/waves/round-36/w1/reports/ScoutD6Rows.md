# ScoutD6Rows — re-derive the round-35 row-correction count (D6)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only pass; only this file written.

## Verdict

**Three rows is correct — D6 is confirmed.** The round-35 `SCORECARD.md` text that ran at
`4f35c80`…`7d708cf^` read *"four new rows' `scope`/`teaches` cells were corrected"*; committed
bytes show exactly **three** rows changed (`S203`, `S204`, `S205`) and the corrected cells are
`scope` (1 row), `teaches` (3 rows) and `recheck` (2 rows) — so the original wording is wrong
twice over: the count (four, not three) and the cell set (it omitted `recheck`). Commit
`7d708cf` already corrected the scorecard text; D6's residual ask is the matching erratum on
the report claim.

## Commands run and exact output

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --numstat 02088b4 7a068cb -- corpus/SOURCES.md
```
```
3	3	corpus/SOURCES.md
```

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --oneline 02088b4..7a068cb -- corpus/SOURCES.md
```
```
4f35c80 round-35: wave-2 falsifications as errata — the shape-scored counter, the falsified ledger claim, the census gaps and the misroot
```
One commit only touched `corpus/SOURCES.md` in the range; nothing else changed the file.

`git diff 02088b4 7a068cb -- corpus/SOURCES.md` (hunk header, full rows quoted below):
```
@@ -202,9 +202,9 @@ recorded in `lessons/round-13.md` § Gate. Only `status`, `recheck` and
-| S203 | host omarchy first-run installer - ... | ... | on-request | corpus/knowledge/idle-lock-never-asked-r12.md |
-| S204 | host evidence that the idle lock was never asked about and never toggled - ... | ... | on-request | corpus/knowledge/idle-lock-never-asked-r12.md |
-| S205 | host idle-lock chain - ... | ... | 90d | corpus/knowledge/idle-lock-chain-armed-r14.md |
+| S203 | ... (new teaches) ... | on-change | ...
+| S204 | ... (new scope + teaches) ... | on-change | ...
+| S205 | ... (new teaches) ... | 90d | ...
```
Three `-` rows and three `+` rows, all carrying ids `S203`, `S204`, `S205`. No other registry
line appears in the diff — the other five new rows (S206–S210) and all pre-existing rows are
untouched.

## Which cells changed (columns: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`, `corpus/SOURCES.md:11`)

| row | `scope` | `teaches` | `recheck` |
|---|---|---|---|
| S203 | unchanged | "runs twelve first-run scripts … none of the twelve asks" → "runs thirteen items, twelve of them first-run scripts … none of the thirteen executed items asks" | `on-request` → `on-change` |
| S204 | "the paired negative: … never made it afterwards either" → "… the journal's zero omarchy-toggle count is a null channel, and the daemon's stop/start is consistent with a toggle-off" | appended ", which is a null channel rather than a negative" | `on-request` → `on-change` |
| S205 | unchanged | "the journal holds two start lines on 2026-10-23" → "the journal holds one start line in the current boot (two across two boots) on 2026-10-23" | unchanged (`90d`) |

Verified cell-level with:
```sh
for rev in 02088b4 7a068cb; do git show $rev:corpus/SOURCES.md | grep -E '^\| S20[345] ' | awk -F'|' '{print $2 "| recheck=" $11}'; done
```
```
=== 02088b4 ===  S203 on-request | S204 on-request | S205 90d
=== 7a068cb ===  S203 on-change | S204 on-change | S205 90d
```
So 6 cells across 3 rows: `teaches`×3, `recheck`×2, `scope`×1. D6's "the corrected cells
include `recheck`" holds.

## Where "four" lived

`git log -S "four new rows" -- SCORECARD.md` → commits `4f35c80` (introduced) and `7d708cf`
(corrected). The phrase was committed at `SCORECARD.md:2203` in `4f35c80` — the *same* commit
that changed the three SOURCES.md rows — so the wrong count was written alongside the bytes it
miscounts (plausible cause: counting the three `idle-lock-*` knowledge entries' errata plus the
registry, or simply off-by-one). `7d708cf` replaced it with "three new rows (S203, S204, S205)
had `scope`/`teaches`/`recheck` cells corrected in-round" (`SCORECARD.md:2203-2205` at tip).

## Remaining unknowns

- None for the count itself. Whether "four" was meant to include a fourth artifact (e.g. the
  registration's stale id list, M35-1) is inference only; the diff admits no fourth row.

No installs; no writes outside this report.
