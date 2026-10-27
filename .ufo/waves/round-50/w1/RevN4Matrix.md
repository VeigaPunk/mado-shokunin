# RevN4Matrix — round-50 w1 (carried round-49 w2 item line 31, retargeted)

Verdict: **VERIFIED — no defect found in the N4 full-matrix receipt.** All four item requirements hold at the
retargeted revisions: 98 rows, set equality with the round-48 summary.json, every row value equal, and an empty
`git diff --stat` of round-48 paths between `03e4ae76aff7a4be59cb69970dd553baa319695a` (round-49 base) and
`8ae47b957034ae21012bbf09173cca2c48be345e` (round-49 tip = round-50 base).

## Item and target

Item (`.ufo/waves/round-49/w2-items.json:31`): "Verify 98 rows, set equality with the round-48 summary.json,
every value equal, and that no frozen round-48 file changed (git diff --stat of round-48 paths between base and
freeze must be empty)." Target: `.ufo/waves/round-49/w1/ExecN4Matrix/c2v2-matrix-full.txt` (sha256
`bf496e777c187c6a7c4db8665227321c14072a8d3993071d3c20dc7c6fddff2f`). I ran my own independent verifier
(`verify-matrix.py`, this seat dir; receipt `receipt-r50.txt`, RESULT PASS failures=0) and separately re-ran the
committed round-49 checker `check-matrix-full.py` on scratch copies of the three inputs (RESULT PASS failures=0,
rc=0) — two independent parsers, same conclusion.

## 1. Input identity (receipt header claims vs committed bytes)

```
sha256 c2v2-matrix-full.txt            bf496e777c187c6a7c4db8665227321c14072a8d3993071d3c20dc7c6fddff2f
sha256 frozen-c2v2-matrix.txt [seat]   ae4ce14c8878bfb9b832cad26d6323fc6372859ad385d7b22522c957ca90e474
sha256 source-summary.json [seat]      f2b6af9bbbc1eee804306941e31af174d7071f4aed8a33f09722e61c9df4106e
sha256 r48 receipts/v2/c2v2-revc2counter-summary.json = f2b6af9b… (byte-equal to seat copy)
sha256 r48 receipts/v2/c2v2-revc2counter-matrix.txt   = ae4ce14c… (byte-equal to seat copy)
```
All three hashes in the receipt header (`c2v2-matrix-full.txt:4-7`) match. The seat's "round-48 summary.json" is
the round-48 committed original `.ufo/waves/round-48/receipts/v2/c2v2-revc2counter-summary.json`; set equality and
value equality were checked against that original (via the byte-equal copy). The five N4 seat worktree files are
byte-identical to their blobs at 8ae47b95 (`git show 8ae47b95:<path> | sha256sum` == worktree sha256, 5/5 SAME).

## 2. 98 rows / set equality / every value equal (independent verifier, all PASS)

```
matrix rows parsed: 98; summary records: 98; footer: 'rows 98'
PASS row-count-98 / count-equals-summary / set-equality / no-duplicate-names
PASS order-equals-summary / footer-rows-98 / row-values-match-summary(all 98)
```
Every row's (declared, rc, last) equals its summary.json record; row order equals summary order; footer says
`rows 98`. The two rows the round-48 harness never printed (`a-rev-base-direct`, `a-entry-at-base`; generator
docstring: record() sites 415/417 vs print site 429) are recovered in the full matrix with values equal to their
summary records, and the receipt's own recovery comment block names both (`c2v2-matrix-full.txt:93-100`).
Frozen side (re-asserting the 96-of-98 claim): frozen text carries 96 names = 95 data rows + the `pos` clauses
line (print site 412 projection); missing set is exactly `{a-rev-base-direct, a-entry-at-base}`; all 95 carried
rows consistent with the summary (declared/rc equal, `last` a prefix of the summary value). Committed checker
witness run on my copies:
```
row_count_98 PASS rows=98 summary=98 | set_equality_summary PASS | no_duplicate_names PASS
order_equals_summary PASS | footer_rows_98 PASS 'rows 98' | recovered_present PASS
row_values_match_summary PASS | frozen_96_rows PASS rows=96 | frozen_missing_two PASS
frozen_pos_is_clauses PASS | RESULT PASS failures=0 (rc=0)
```

## 3. No frozen round-48 file changed (03e4ae76 → 8ae47b95)

```
$ git diff --stat 03e4ae76aff7a4be59cb69970dd553baa319695a 8ae47b957034ae21012bbf09173cca2c48be345e -- .ufo/waves/round-48/
(empty output)
$ git diff --name-only <same range> -- .ufo/waves/round-48/ | wc -l
0
round-48 path count at base=2043 tip=2043 (path sets equal)
```
Key round-48 blobs identical at both revs: `receipts/v2/c2v2-revc2counter-summary.json` (blob 5e5f15e78006),
`receipts/v2/c2v2-revc2counter-matrix.txt` (blob a765dc37cf84),
`l1-draft/v2/c2v2-harness-revc2counter.py` (blob 3f0b92f04141). Whole-tree context: 994 changed paths in the
range, of which 939 under `.ufo/waves/round-49/`, 47 `*.synthetic` sidecars under round-45/46 (the same 47 the
round-49 spotcheck harm-watch describes), plus LOG.md, SCORECARD.md, the two round-49 lessons, the three round-49
counters/fixtures and `tools/mado-keysym.py` — no round-48 artifact among them.

## Notes and residual risk

- Retarget note: the round-49 spotcheck names the round-49 closure tip as `8a370cd4…`; I verified
  `8a370cd4` is an ancestor of `8ae47b95` and the round-48 diff between them is also empty (0 changed lines), so
  the empty-diff conclusion holds across the whole round-49 span regardless of which tip hash is canonical.
- Scope: I verified the receipt's fidelity to the round-48 summary.json and the immutability of round-48 paths. I
  did not re-execute the round-48 harness variants themselves (that would be a re-run of the round-48 counter, not
  of this item); the receipt explicitly derives row text from summary.json alone, and that derivation is what I
  re-checked.
- My first verifier run reported 2 false FAILs (my parser did not count the frozen `pos` clauses line as a name);
  fixed in `verify-matrix.py`, final run PASS. No artifact defect.
- No tools installed (none needed); no host/home writes; all work in scratch `/fast/scratch/hyaku/mado-r50/RevN4Matrix`
  (removed at finish) and this seat dir; lane touched read-only (git diff/ls-tree/rev-parse/show, file reads).

## Deliverables (test -f verified)

- Report: `.ufo/waves/round-50/w1/RevN4Matrix.md` (this file)
- Receipt: `.ufo/waves/round-50/w1/RevN4Matrix/receipt-r50.txt` (RESULT PASS failures=0)
- Verifier: `.ufo/waves/round-50/w1/RevN4Matrix/verify-matrix.py` (read-only on lane; writes only its receipt arg)
