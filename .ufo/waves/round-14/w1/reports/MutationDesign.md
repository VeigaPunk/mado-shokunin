# MutationDesign — regular-file source targets (round 14, w1)

Axes: **coverage** (a directory-shaped direct target and a directory among glob results each have a detector) and **operability** (the failure belongs to `hypr.root.sources_resolve`, names the offending target, and is isolated from source-set/order failures).

## Candidate mutants and detectors

| Mutant | Smallest behavior change | Detector fixture | Expected discriminator |
|---|---|---|---|
| RT1 | Revert the direct-source predicate from `[ -f "$x" ]` to `[ -e "$x" ]`. | N9: copy clean fixture; replace default-tree `~/.local/share/omarchy/default/hypr/windows.conf` with a directory, without changing `hyprland.conf`. | Require `hypr.root.sources_resolve` FAIL with `non-regular: ~/.local/share/omarchy/default/hypr/windows.conf`, `hypr.root.include_graph` PASS, and `hypr.local.inventory` PASS. N9 has exactly one hypr FAIL, the source row; RT1 would make that row pass, so its exact row/detail assertion is the expected detector. |
| RT2 | Bypass all per-match glob validation (`if [ -f "$m" ]; then continue; fi` → `continue`). | N11: preserve regular `window-no-gaps.conf` and add directory `dir.conf` to the toggle glob. | Require `hypr.root.sources_resolve` FAIL with `non-regular: ~/.local/state/omarchy/toggles/hypr/dir.conf`, no non-regular label for the regular member, and `include_graph` plus `local.inventory` PASS. RT2 would skip the glob diagnostics; N11's exact row assertion is the expected detector. |
| RT3 | Invert the glob regular-file guard (`if [ -f "$m" ]; then continue; fi` → `if [ ! -f "$m" ]; then continue; fi`). | N11 mixed glob: keep `window-no-gaps.conf` regular and add directory `dir.conf`. | Require `non-regular: .../dir.conf` and forbid `non-regular: .../window-no-gaps.conf`. The inverted guard skips the directory but misclassifies the regular file; the two N11 detail assertions distinguish both errors. |
| RT4 | Remove the `unresolved:` class prefix from the missing-target detail builder (`tdetail="unresolved:$tmiss"` → `tdetail="$tmiss"`). | N4 removes declared `gkeep.conf`; N4 now asserts exact `unresolved: ~/.config/hypr/gkeep.conf`. | The altered detail is expected to fail N4's exact `sources_resolve` row assertion. No mutant or fixture was run. |

N10 is the all-directory counterpart: replace the only regular `window-no-gaps.conf` with a directory of that name. Require the same `sources_resolve` `non-regular:` detail and preserve `include_graph`/local-inventory PASS; the independent toggle row is NOTE. Expected detectors: RT2 by N10/N11, RT3 by N11, and RT4 by N4/N14/N15. N13 (file symlink) and N16 (newline-named regular glob member) are positive controls; none of these cases was run here.

These cases change filesystem target shape only, not source declarations, membership, multiplicity, or order. Assert `include_graph PASS` in each, so a source-set/order failure cannot masquerade as a regular-target kill. N12's same-members order swap remains a separate control for the already-working order invariant; it is not claimed as a new improvement or part of these mutants.

## Spec and evidence boundary

- Candidate mutation syntax is in `regular-target.spec`, using the `@defect`, `@old`, `@new` format read from `.ufo/waves/round-13/covering.spec`.
- At this read, the landed resolver has direct guard `if [ -f "$x" ]; then continue; fi` (`tools/mado-verify.sh:2673`), glob-member guard `if [ -f "$m" ]; then continue; fi` (`:2664`), and unresolved prefix builder `tdetail="unresolved:$tmiss"` (`:2686`). RT1 changes the direct predicate to `-e`; RT2 bypasses per-match validation; RT3 inverts that guard; RT4 removes only the unresolved label. Glob matches enter `gmatch` through null-delimited expansion (`mapfile -d ''`), preserving newline-bearing filenames without line splitting.
- N4 asserts exact unresolved detail at `:1153-1155`; N9/N10/N11 assert the non-regular names and mixed-member exclusion at `:1202-1266`; N13 covers file symlinks, N14 zero-match `unresolved:`, N15 dangling-match `unresolved:`, and N16 newline-named regular matches at `:1300-1367`. Source/fixture read only (`tools/mado-verify.sh:236-377, 1135-1157, 1194-1367, 2638-2689`), after reading the round-13 `covering.spec` format. No gate edit, mutation, test, build, formatter, or runtime invocation was performed. No actual output, kill verdict, or before/after digest was generated. Restoration is not applicable: no target bytes were changed.
- No tool was installed or updated.
