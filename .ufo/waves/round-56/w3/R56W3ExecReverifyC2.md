# R56W3ExecReverifyC2 — C2 frozen gate rerun

## Item attacked
Frozen PRED-C2-r56-v2 operability gate at requested lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, plus the requested live read-only watchplan half.

## Result / evidence
- `python3 -I tools/mado-watchplan.py --selftest`: `MADO_WATCH_SELFTEST: 86/86 assertions passed`, rc 0.
- C2 harness passed all controls and fixture counts in bwrap: `sandbox=bwrap`; `fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET`, rc 0. The harness needed a git repository. The first exact requested invocation on the bare `git archive` failed setup (`git rev-parse --verify failed`, rc 2). I initialized and committed the archive-backed snapshot in scratch, verified its git top-level equals the scratch directory, then ran the harness against local commit `369a086f1db22bbcedd5e31fbe57bde909c1970e`.
- This does **not** establish the expected output at the original frozen rev: the original rev could not be tested using the archive-only repository, and the passing invocation used the synthetic archive commit. This deviation is a **blocking finding** for exact-tip C2 reverification; it is not evidence of a defect in the frozen predicate/tool.
- Live, read-only call returned `MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE`, and `MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE`, rc 0. Captured getoption says integer 0, `set=false`; Hyprland version reports 0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f`.

## Exact retained evidence and files
- `.../w3/R56W3ExecReverifyC2/c2-a2.txt`: commands, rc values, decisive raw output, setup failure and archive-backed rerun details.
- `.../w3/R56W3ExecReverifyC2/getoption.json`: captured output from `hyprctl getoption misc:disable_autoreload -j`.

## Other defects / limits
No additional defect observed in the executed paths. Original-revision C2 gate is not verified (blocking as noted). The live result is an agreement for this host/config snapshot only. Scratch was removed. No lane tracked files were edited; no tests/build/lint/formatters were run. No `hyprctl` mutating command was invoked.
