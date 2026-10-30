# R56W3ExecHarmWatch — harm watch at 0f3a54361a9824484d0801679ceb1fd8ac7c32e1

Attacked: post-integration regressions in the requested selftest, index, index-row, tool-ledger, axis-score, navigation-count and SOURCES-census checks. Read `claims-frozen-v2.md` and `registration-v2.md` first; predicates were not altered. No lane tracked files or host/compositor state were changed. No tools were installed.

Commands, complete outputs, and return codes are retained at ` .ufo/waves/round-56/w3/R56W3ExecHarmWatch/receipts/harmwatch-a2.txt` (path without leading space). Ran the archived tip in an isolated scratch tree; its local fixture git commit is `a795213a986297b30ad8d90bc275cabb5ed3ffe7`, not the lane revision. The archive originated at the requested `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`.

Decisive evidence:
- `bash tools/mado-verify.sh --selftest`: `MADO_SELFTEST: 460/460 assertions passed`; rc 0.
- `quality/check-index.py`: `indexed=71/71 missing=0 dangling=0 duplicates=0`; rc 0.
- `quality/check-index-rows.py`: `rows=71 errors=0 warns=3`; rc 0. Warnings: cited globs `.ufo/evidence/round-12/getprop-*.txt`, `.ufo/evidence/round-12/drift-*.txt`, and `.ufo/waves/round-24/fetch/S###.bin` did not match. These are warnings, not regressions of the requested harm-watch predicates.
- `quality/check-tool-ledger.py`: `population=97 ledger_rows=97 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET`; rc 0.
- `quality/check-axis-scores.py`: navigation published/derived `71/71`, MATCH; calibration `86/86`, MATCH; operability `12/12`, MATCH; `mismatched=0`; rc 0. The prior stale 66/66 vs 71/71 is not present at this tip.
- SCORECARD Fleet round 1 counting fence with tip REV: `indexed=71/71 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`; rc 0.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`: emitted `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`; rc 0. Warnings include W04 duplicate URL groups and W01 S277 tierC; full output retained.

Defects: none found that block or weaken the assigned harm-watch checks. Not run: no other checks outside the seven specified. No host live-compositor probe was requested or performed.

Files changed: `.ufo/waves/round-56/w3/R56W3ExecHarmWatch.md` and `.ufo/waves/round-56/w3/R56W3ExecHarmWatch/receipts/harmwatch-a2.txt` only.