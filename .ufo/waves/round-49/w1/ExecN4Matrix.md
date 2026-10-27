# ExecN4Matrix — N4: complete 98-row text receipt of the round-48 C2 v2 matrix

Status: DONE. Seat dir `.ufo/waves/round-49/w1/ExecN4Matrix/`. No frozen file was modified; every write is inside the
seat dir plus this report.

## Result

The frozen round-48 stdout receipt `.ufo/waves/round-48/receipts/v2/c2v2-revc2counter-matrix.txt`
(sha256 `ae4ce14c8878bfb9b832cad26d6323fc6372859ad385d7b22522c957ca90e474`) carries 96 rows; its summary
`c2v2-revc2counter-summary.json` (sha256 `f2b6af9bbbc1eee804306941e31af174d7071f4aed8a33f09722e61c9df4106e`) records 98.
Delivered `c2v2-matrix-full.txt` (sha256 `bf496e777c187c6a7c4db8665227321c14072a8d3993071d3c20dc7c6fddff2f`): 98 rows,
one per summary entry, same order, values taken from the summary, with `a-rev-base-direct` and `a-entry-at-base` restored.

Check: `check-matrix-full.py --frozen frozen-c2v2-matrix.txt` → `RESULT PASS failures=0` (all 10 assertions: 7 on the
receipt, 3 on the frozen 96-of-98 claim).
Both-ways receipt `check-matrix-full.receipt.txt`: the delivered file PASSes and 4 negative controls FAIL for named
reasons (frozen text 5 failures, deleted row 4, flipped `pos` rc 1, duplicated+dropped rows 4).

## Why the frozen text dropped two rows

Generator: `.ufo/waves/round-48/l1-draft/v2/c2v2-harness-revc2counter.py` (sha256
`de57c772c24f8c7f17625058c59768a448ab68f09fa95a1073b4e14b9186b12f`, 436 lines). Locators are `grep -n` output in
`locators.txt`, not typed.

1. The generator has exactly four `record()` call sites — `399` (definition), `411` (`pos`), `415`
   (`a-rev-base-direct`), `417` (`a-entry-at-base`), plus the loop at `428` — but only three `print()` sites in `main()`:
   `412` (`pos`), `429` (the per-variant row), `433` (`variants <n>`).
2. `415` and `417` are bare `record(...)` calls: they write `summary.json` and a per-variant log and print nothing. So the
   two base-scoring rows exist only in the JSON (`locators.txt`: `missing_count=2
   missing_names=['a-rev-base-direct', 'a-entry-at-base']`, first returned `rc=1 TARGET_MISSED` against BASE
   `579f694b`, second `rc=2 SETUP precondition_failed entry_present_at_base`).
3. Arithmetic closes: 98 = `pos` + the two base rows + 95 loop rows; the text carries `text_pos_lines=1` and
   `text_harness_rows=95` → 96 lines (`variants 98` on line 99 is the count print, not a row).
4. Secondary defect on the rows that *were* printed: line `429` truncates to 96 characters
   (`results[-1]["last"][:96]`). `a-entry-at-base`'s `last` is 105 characters (`rows_over_96=[('a-entry-at-base', 105)]`),
   so had that row been routed through the row print it would have been clipped. No row that is currently printed exceeds
   96 characters, so the frozen text is not in fact clipped — the truncation is latent, not active.
5. Shape divergence the check pins down: the frozen `pos` line is not the row shape. Line `412` prints the `clauses`
   field, and the frozen line equals `"pos rc 0 " + summary pos clauses` (assertion `frozen_pos_is_clauses`). Any text-row
   validator that assumes `rc=<n>` therefore silently misses `pos` as well; my first count script did (`missing` showed
   `pos` until the `^pos rc ` case was special-cased). The delivered receipt normalizes every row onto `last` and keeps the
   frozen `pos` line verbatim as a comment, so the L1 can freeze one uniform row grammar.
6. The per-variant logs cannot fill the gap: the harness wrote them under its scratch root
   `S = /fast/scratch/hyaku/mado-r48/L1c2v2-rev` (`c2v2-harness-revc2counter.py:14`), and `ls` returns
   "No such file or directory" for it today. `summary.json` is the only surviving per-variant record — hence the rebuild
   reads it and nothing else.

## Delivered files (sha256, all under `.ufo/waves/round-49/w1/ExecN4Matrix/`)

| file | sha256 | role |
|---|---|---|
| `c2v2-matrix-full.txt` | `bf496e77…fddff2f` | 98 rows, `rows 98` footer, provenance header, recovered-row appendix |
| `check-matrix-full.py` | `26fada8b…58e9` | asserts row count 98 + set equality + per-row values + order + footer + recovered rows + the frozen 96/2 claim |
| `generate-matrix-full.py` | `60d4f871…1e2a9` | regenerates the receipt from `summary.json` only (stdlib; deterministic) |
| `source-summary.json` | `f2b6af9b…06e` (`cmp` identical to the frozen file) | row source |
| `frozen-c2v2-matrix.txt` | `ae4ce14c…474` (`cmp` identical) | frozen text, for the 96-of-98 assertion |
| `check-matrix-full.receipt.txt` | `bd99b450…bd5` | positive + 4 negative control runs with rc |
| `locators.txt` | `a1455350…fd` | computed `grep -n` locators and count table |

Row-block fidelity: all 95 shared harness rows reproduce the frozen lines **byte-identically** (computed diff: 95 identical,
0 differing); only the `pos` line shape is normalized, and its frozen form is preserved as a comment. `fails` arrays are not
in the row block — they stay in the byte-identical `source-summary.json` snapshot, so nothing from the summary is lost.

## Check assertions (all fatal, all printed)

`row_count_98` (98 = 98), `set_equality_summary`, `no_duplicate_names`, `order_equals_summary`, `footer_rows_98`,
`recovered_present`, `row_values_match_summary` (declared/rc/last per name), and with `--frozen`: `frozen_96_rows`,
`frozen_missing_two` (`a-entry-at-base,a-rev-base-direct`), `frozen_pos_is_clauses`. Read-only; default inputs are the seat
snapshots, so it is self-contained.

## Values carried (from `summary.json`)

`rc_histogram={0: 12, 1: 85, 2: 1}`; `target_met_rows=12`. The two recovered rows are the only ones the frozen text never
showed: `a-rev-base-direct` (`a`, rc 1, `TARGET_MISSED`, rev `579f694b…`) and `a-entry-at-base` (`a/setup`, rc 2,
`SETUP precondition_failed entry_present_at_base`).

## Risks / limits

- This is a faithful projection of the committed summary, **not a re-measurement**: the harness was not re-executed (a
  counter run is out of w1 scope and would need the deleted scratch clone). If a summary field were wrong, this receipt
  reproduces the error; it proves coverage, not truth.
- The row grammar still cannot carry `fails`/`clauses`/`note`; a w2 fixture that wants those must read the snapshot.
- `pos` remains the one row whose frozen text came from a different field; the receipt says so in-band rather than hiding it.

## Housekeeping

No tool installs, no pacman, no host or compositor access, no git/jj mutation, no writes outside the seat dir and this
report. All negative-control fixtures were built under `/fast/scratch/hyaku/mado-r49/ExecN4Matrix/` and removed.
Blockers: none.
