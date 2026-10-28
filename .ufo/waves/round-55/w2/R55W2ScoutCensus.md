# R55W2ScoutCensus — round 55 wave 2 (falsification): frontier census

Seat scope: run the frontier census three times at different moments, run the manual
CORPUS.md census battery from the lane root, and report rows before/after against the frozen
`receipts/census-before.txt` and base `3b55b6e`, plus every used-by path that does not
resolve. Leaf seat; no subagents. No tracked file was modified; no git/jj mutation anywhere;
all scratch lived under `/fast/scratch/hyaku/mado-r55/R55W2ScoutCensus/` and was removed at
yield (receipts copied into the deliverable directory first). No tool installs were needed
(no pacman, no uv/npx/binary installs; nothing to record under the tooling rule).

## What was attacked and how

1. **Frontier census stability** — `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` at 23:20:53Z, 23:22:07Z, 23:22:57Z (2026-10-28). All three: **exit 0**, output byte-identical (mutual `diff` empty; sha256 `5b0228e5…` each): 26 W04 + 1 W01 + `mado ok <lane>/corpus/SOURCES.md`, zero E-codes. Pre-existing W01 is S277 (tier-C mined), unchanged from base.
2. **Before/after against the frozen receipt** — `receipts/census-before.txt` is committed in the freeze commit `54dacbd8` and the worktree copy is byte-identical to the frozen copy (sha256 `3598bf9b…`). After-vs-before delta is **exactly one added line**: `mado W04 S380 duplicate url …/src/devices/IKeyboard.hpp across scopes` (25→26 W04). That is the documented, intended warning: S380 reuses S363's URL with a different scope → W04, not E04 — stated in SOURCES.md §Search-log ("the census reports this as a W04 warning, not an E04, because the scope differs"). Warnings do not fail validate: exit stays 0, so the frozen harm-watch "…stays exit 0" holds.
3. **Rows before/after** — base `git show 3b55b6e:corpus/SOURCES.md`: **314** rows; current: **317** (+3 = S378, S379, S380). Diff base→current is exactly the three new rows, used-by appends on S052/S316/S318/S319, and the search-log block; no in-place row edits. Histories: tier `A=303→306, B=4, C=7`; status `mined=293→296, queued=10, rejected=11` — both sum to the row counts.
4. **Manual CORPUS.md battery** (exact commands, fleet `CORPUS.md:133-148`, from lane root): malformed rows **0**; duplicate ids **nothing**; enum violations incl. tier-inflation **nothing**; mined rows with unresolvable used-by **nothing**. Superset check beyond the battery: used-by of **all 317 rows** (any status, split on `,` and `;`) — **zero** unresolvable (the script's E11 is mined-only, comma-split; sources-census.sh ~555–570).
5. **New used-by edges resolve** — S378/S379/S380 and the modified S052/S316/S318/S319 all cite `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` (exists) plus prior targets.
6. **Instrument itself** — `sources-census.sh selftest`: exit **0**, `selftest ok`, 0 SURVIVED. Content reconstruction from base bytes via `--file` reproduced the receipt's warning set 1:1 (content findings are a pure function of the table bytes). The E11 flood in that reconstruction is a `--file`-mode artifact (used-by resolves against the file's own directory, not the lane root) — **NOT-REPRODUCED as a lane defect**; parser-compatible control = the standard lane-context run, which is clean. Reported as a non-reproducing attack per QUALITY 105.
7. **Census-adjacent frozen claims** — README knowledge-index rows 69 (base) → **70** (current): "69/69 → 70/70, never fewer" holds. C1 entry cites the opened rows S378 ×3, S379 ×7, S380 ×3.

## Verdicts

| target | verdict | evidence |
|---|---|---|
| Frontier census, 3 runs | **SURVIVES** (identical, exit 0) | `w2/R55W2ScoutCensus/census-run{1,2,3}.txt` |
| census-before vs after delta | **SURVIVES** (exactly the one documented S380 W04; exit 0 kept) | diff vs `receipts/census-before.txt`; search-log block in SOURCES.md |
| Manual battery (malformed/dups/enums/dangling used-by) | **SURVIVES** (all clean; 314→317 consistent) | command outputs quoted in `w2/R55W2ScoutCensus/census.md` §3 |
| All-row used-by resolution (superset) | **SURVIVES** (0 dangling) | §4 superset check |
| README index 69→70 | **SURVIVES** | grep counts in census.md §5 |
| Instrument selftest | **SURVIVES** | `w2/R55W2ScoutCensus/instrument-selftest.txt` |
| `--file` E11 flood as lane defect | **NOT-REPRODUCED** (harness artifact of my reconstruction; control run clean) | `w2/R55W2ScoutCensus/base-3b55b6e-via-file.out` |

## Not verified / limits

- The producing moment of `census-before.txt` is pinned only as "before dispatch" (freeze `54dacbd8`); its warning content matches base-3b55b6e-derived content 1:1, but the exact wave-1 revision it ran at is not recorded in the receipt itself.
- Scope was mado only, per assignment; other lanes' registries not re-censused.
- No mutation test was in this seat's scope; nothing in the lane was mutated or restored because nothing in the lane was touched.

Report: .ufo/waves/round-55/w2/R55W2ScoutCensus/census.md
