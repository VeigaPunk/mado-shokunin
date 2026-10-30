# R56W3ExecFixDivB

Attacked item: the four requested tool honesty-boundary divergences of `tools/mado-watchplan.py` at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`: runtime keyword, reload dispatch, fdinfo visibility of `IN_DONT_FOLLOW`, and explicit unsupported constructs.

Materialized four directories under `.ufo/waves/round-56/fixtures/c2-divergences/`: `runtime-keyword-route/`, `reload-dispatch/`, `fdinfo-mask/`, and `unsupported-constructs/`. Inputs/notes document what the static model does not establish; runtime-keyword-route includes an expected stdout/rc example for its static config. No tool or frozen harness was modified. Receipts: `.ufo/waves/round-56/receipts/divergences-b.txt`.

Evidence read at the frozen revision using `git -C ... show ...:tools/mado-watchplan.py`: docstring lists runtime `hyprctl keyword` as unmodelled and states out-of-subset constructs are counted unsupported. Entry Limits read at the frozen revision with `git -C ... show ...:corpus/knowledge/hyprland-config-autoreload-r56.md | grep -n -A12 -B2 'Limits'`: Limit says `IN_DONT_FOLLOW` is an add flag absent from fdinfo and the observation did not confirm it; runtime keyword path is expressly inference/not run; reload registration and full-reset branch were not checked.

Severity/defects: No implementation defect alleged; these are documentation/boundary fixtures. They weaken any interpretation that the entry proves runtime dispatch/reload or confirms the complete mask. No compositor operation or `/proc` inspection was done. Fixture outputs were not run or verified; only `runtime-keyword-route` has expected output/rc. The other three directories are descriptive inputs/notes and are not complete harness-compatible fixtures. No tests/checks ran.
