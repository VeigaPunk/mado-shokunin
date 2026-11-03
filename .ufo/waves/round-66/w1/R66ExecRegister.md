# R66ExecRegister

Axes: calibration / operability. Draft only; no production edits.

Production candidate: `.ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py` → `quality/counters/c1-r66-register.py`; SHA256 `8ca15c66e953b093913559b7eda7f390c111a79062ef22f75caa498a4a04ec31`. Sole post-freeze change (authorized defect fix; predicate and selftest cases untouched): `git()` sets `GIT_NO_REPLACE_OBJECTS=1` after the inherited-env scrub, closing R66SentFrontier's demonstrated refs/replace steering (invalid `--rev` bytes served genuine replacement objects); verified by `.ufo/waves/round-66/w1/R66ExecRegister/replace-refs-check.py` (rc=1 TARGET_MISSED on the steered rev).

Targeted commands: `python3 .ufo/waves/round-66/w1/R66ExecRegister/c1-r66-register.py --selftest` rc=0 (15/15); `python3 .ufo/waves/round-66/w1/R66ExecRegister/demonstrate.py` rc=0. Baseline accepts all three controls; candidate rejects each rc=1 and accepts genuine rc=0. Correctness 1/4 → 4/4. Actual committed base also passes candidate rc=0. Exact live CLEAN line copied from committed gate-live-r65 receipt, not reconstructed.

Evidence, full commands, rc, changed drafts and limitations: `.ufo/waves/round-66/w1/R66ExecRegister/report.md`; machine results: `.ufo/waves/round-66/w1/R66ExecRegister/controls.json`; selftest: `.ufo/waves/round-66/w1/R66ExecRegister/selftest.txt`; source line: `.ufo/waves/round-66/w1/R66ExecRegister/live-line-source.txt`. Scratch removed; cleanup receipt retained. Harness/reviewer/mutation seats received exact interface/hash.

State-cell truth remains NOT measured; valid pointers plus invented state prose intentionally pass. No installs, host writes, production/git mutations, or broad checks. LSP unavailable. No blocker; parent owns integration and shared harness/landing verification.

Post-review L1 ruling: retain candidate unchanged. A file-plane-only register is accepted when the exact live receipt remains committed but unreferenced; the tested control removes that live object. The 4/4 result does not cover the stronger retained-tree citation-gap forge. This declared limitation and reviewer evidence are recorded in the detailed report.
