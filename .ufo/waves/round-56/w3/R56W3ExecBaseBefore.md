# R56W3ExecBaseBefore

Attacked item: attempt-2 BEFORE receipts at base `13f0acbe3a15da2d9c08357a576d91dcadc85273`.

Re-derived and recorded the archived-base knowledge count (70), registry census (319), keyword census (0), absent watchplan tool, and selftest harm baseline (460/460). C3 counter is absent at base. Exact commands, outputs, and return codes are in `R56W3ExecBaseBefore/receipts/before-a2.txt`.

Deliverable: `.ufo/waves/round-56/w3/R56W3ExecBaseBefore/receipts/before-a2.txt`.

Defect/blocker: requested check-index 70/70 was not verifiable with the suggested style of check: `bash tools/mado-verify.sh --check-index` returns usage error, rc 2, and the archived base checker supports no `--check-index` option. I did not assert a result. The specified `receipts/c3-base-v2.txt` could not be read at base revision (path only exists on disk outside that revision; `git show <base>:...` rc 128); the checkout-side committed receipt could not be safely captured without going beyond the base object archive. No tools installed; no build/test/verification beyond the requested selftest ran. Scratch archive: `/fast/scratch/hyaku/mado-r56/R56W3ExecBaseBefore`.