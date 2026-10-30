# R56W3ExecReverifyC3 — C3 re-verification

**Attacked:** frozen C3-v2 predicate and nine-control harness at lane tip, plus the requested before-state at BASE. Claims/registration were read and left unchanged.

**Commands/evidence:** Exact commands and decisive output with rc are in `receipts/c3-a2.txt`.

- At `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, counter returned `MADO_USED_BY: ... entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none`, rc 0.
- Same tip harness returned `MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK`, rc 0. Harness emitted non-scored harness-vs-counter metric notes; all nine controls passed.
- At BASE `13f0acbe3a15da2d9c08357a576d91dcadc85273`, neither v2 command can run: both return setup rc 2 because `.ufo/waves/round-56/frozen-tables-v2.json` is absent as a regular blob at that revision. The exact retained before line, read from `receipts/c3-base-v2.txt`, is `entries=70 rows=319 missing=41 pairs=381 exempt=24 stale=0 conflict=0`.
- The required `git archive` source tree alone lacked git commit objects and returned setup rc 2 for both commands. I then used one `git clone --shared` scratch repository, which provided the immutable revision objects needed to execute the gates. Full attempts are in the receipt.

**Defects / severity:** No tip deviation; both expected tip gates met. The BASE gate invocation deviation is **blocking the claim's before-state execution**: v2 artifacts do not exist at BASE, so the explicit expected BASE metrics could not be independently recalculated by the v2 tool. The recorded baseline line is a preserved receipt, not a fresh counter result. The archive-only execution also did not run successfully (setup rc 2); rerun in the scratch clone succeeded at tip.

**Deliverables:**
- `.ufo/waves/round-56/w3/R56W3ExecReverifyC3/receipts/c3-a2.txt`
- `.ufo/waves/round-56/w3/R56W3ExecReverifyC3.md`

No source edits, git mutations, host reads, installs, or verification beyond the assigned gates were performed. Scratch was removed. No build/lint/tests/formatters were run.