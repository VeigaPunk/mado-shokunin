# R55W2ScoutCensus — frontier census record (round 55, wave 2, falsification)

Seat: R55W2ScoutCensus · Lane: mado-shokunin · Scoring rev: `57584ed6` (corpus files in the
working tree equal it; HEAD `721ba9c1` adds only wave-2 bookkeeping files: `w2-spec.json`,
`w2/swarm-registry.json`, `make-w2-spec.py`, dispatch markers). No lane file was modified by
this seat; every fixture lived in `/fast/scratch/hyaku/mado-r55/R55W2ScoutCensus/` (removed at
yield; receipts copied here first).

## 1. Frontier census, three runs

Command (identical each time, from fleet root):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

| run | UTC moment | exit | output |
|---|---|---|---|
| 1 | 23:20:53Z | 0 | 28 lines: 26 W04 + 1 W01 + `mado	ok	<lane>/corpus/SOURCES.md` |
| 2 | 23:22:07Z | 0 | byte-identical to run 1 (`diff` empty; sha256 `5b0228e5…` all three) |
| 3 | 23:22:57Z | 0 | byte-identical to run 1 |

Zero E-codes in all three runs. Receipts: `census-run{1,2,3}.txt` (sha256 of each: `5b0228e5479aaf0b0c7fa0a5307ecab4a0e1573749179f1589f6f9a5c2d7b51d`).

## 2. Before/after against the frozen receipt and base 3b55b6e

- Frozen receipt `.ufo/waves/round-55/receipts/census-before.txt`: committed in the freeze
  commit `54dacbd8` ("before any dispatch"); worktree copy byte-identical to the frozen copy;
  sha256 `3598bf9bdcb93ea0ba73603220f5644efaf4b341d4672fafd73e9e568052995d`. Content: 25 W04 +
  1 W01 + `mado ok …` + a trailing `exit=0` bookkeeping line.
- Base rows: `git show 3b55b6e:corpus/SOURCES.md` → **314** row-shaped rows.
- Current rows: **317** (+3 = S378, S379, S380; diff base→current is exactly: used-by appends on
  S052/S316/S318/S319, three new rows S378–S380, and the §Search-log block — no row edited
  in place).
- After-vs-before delta of the frontier census is **exactly one line**:
  `mado	W04	S380 duplicate url raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/devices/IKeyboard.hpp across scopes`
  (25→26 W04). That warning is the documented, intended one: S380's URL is the URL already held
  by S363 (`src/devices/IKeyboard.hpp`), scope differs → W04 warning, not E04; stated in the
  SOURCES.md §Search-log block ("the census reports this as a W04 warning, not an E04, because
  the scope differs") and the README round-55 row.
- Warnings are non-failing: exit stays **0** in all runs → frozen harm-watch
  "`scripts/sources-census.sh validate --root … mado` stays exit 0" holds.
- Content reconstruction from base: running validate over the base bytes reproduces the
  receipt's warning set 1:1 (only label differences: lane `file` vs `mado` under `--file`,
  plus the receipt's `exit=0` trailer). See `base-3b55b6e-via-file.out`; the E11 flood in that
  file is a `--file`-mode artifact (used-by paths resolve against the file's own directory,
  not the lane root), not a lane defect — the lane-context run has zero E11.

## 3. Manual CORPUS.md census battery (exact commands, from lane root)

Source: `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 133–148 ("Census — run from the lane root").

| check | expected | observed |
|---|---|---|
| rows (`grep -cE '^\|\s*S[0-9]{3,}\s*\|'`) | — | base **314** → current **317** |
| malformed rows (NF!=13) | 0 | **0** |
| tier histogram | — | base `A=303 B=4 C=7` → current `A=306 B=4 C=7` (+3 A, sums 317) |
| status histogram | — | base `mined=293 queued=10 rejected=11` → current `mined=296 queued=10 rejected=11` (+3 mined, sums 317) |
| duplicate ids | nothing | **nothing** |
| enum violations (kind/tier/status/tier-inflation) | nothing | **nothing** |
| mined rows with unresolvable used-by paths | nothing | **nothing** |

Superset check (my own, beyond the manual battery): used-by paths of **all 317 rows** (any
status, splitting on both `,` and `;`) — **zero** unresolvable. (The script's E11 is
mined-only with comma split; sources-census.sh lines ~555–570.)

Rows S378/S379/S380 and the four modified rows (S052, S316, S318, S319) all point at
`corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` (plus prior targets) — the entry
exists, so every new used-by edge resolves.

## 4. Instrument attack

- `bash scripts/sources-census.sh selftest` → exit **0**, `selftest ok`, **0 SURVIVED**
  (`instrument-selftest.txt`).
- `--file` reconstruction from base bytes reproduced the warning content (§2) — the parser's
  content-derived findings are a pure function of the table bytes.

## 5. Other frozen census-adjacent claims checked

- README navigation index: `^\| ?\`knowledge/` rows 69 (base) → **70** (current) — frozen
  harm-watch "69/69 → 70/70, never fewer" holds.
- C1 entry cites the opened rows: S378 ×3, S379 ×7, S380 ×3 (claims-frozen §2b item 4 duty).

## 6. Files here

- `census-run1.txt`, `census-run2.txt`, `census-run3.txt` — frontier runs (byte-identical)
- `instrument-selftest.txt` — selftest output
- `base-3b55b6e-SOURCES.md`, `current-SOURCES.md` — the two table snapshots (sha256
  `4f6833df…` / `868d59b5…`)
- `base-3b55b6e-via-file.out` — `--file` reconstruction output (see §2 for the E11 artifact)
