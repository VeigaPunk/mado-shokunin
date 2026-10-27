# R54W2Seat15 — C1 scratch refusal

## Axes
Operability (can the frozen command execute without an explicit work path); safety (can scratch avoid lane mutation); falsifiability (do the frozen rules specify refusal semantics).

## Finding
**NOT RUN / absent.** The scored C1 counter is not present at the lane path, so its `--work`/`TMPDIR` handling and lane-root refusal behavior cannot be exercised. `test -f /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r54-errata-truth.py` exited 1 (no output). I did not substitute a scratch draft or infer actual counter behavior.

The frozen invocation at `claims-frozen.md:19-21` is `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` and contains no `--work`. Its invocation contract therefore requires a usable default if in-process control runs need writable scratch. `registration.md:49-53` prescribes the form `--repo . --rev <rev>` and separately says `--work <dir>` honours the scratch rule, with “no `/tmp` hardcode”; it does not itself specify the default or explicitly say whether a work directory inside the scored repo is refused. The six controls are mutated copies (`registration.md:36-38`), making scratch location relevant to safe execution.

Frozen pin spans relevant to exercising the actual counter are P19 `Hyprland-ConfigActions.cpp:1554-1558` and P20 `:1576`; P21 `Hyprland-legacy-DispatcherTranslator.cpp:619-622`; P22 same pin `:573-574` (`registration.md:25-34`). They supply read-only inputs but do not establish scratch policy.

Relevant w1 evidence: `w1/R54Seat05.md:148-168` says the no-`--work` frozen invocation needs a default, and reports its draft verified `TMPDIR=<scratch>` and unset-TMPDIR invocations while explicitly refusing `--work` under `/tmp`. That is draft evidence, not evidence about the absent scored implementation. `w1/R54Seat03.md:71-88` separately reports a draft refusal check that ran after `os.makedirs(work)`, leaving an empty directory inside the lane on refusal; it recommends checking before creation. `w1/R54Seat16.md:35-59` reports a repo-relative default created `.c1-r54-work/`, demonstrating that this alternative can pollute the scored checkout. These are prior reports, not rerun results.

## Smallest safe correction
For the implementation, resolve the default beneath caller `TMPDIR` (with the system temp fallback) without hardcoding `/tmp`, and validate any explicit `--work` against the scored repo before creating it; refuse in-repo paths with setup error. Then run the exact frozen no-`--work` invocation with both set and unset `TMPDIR`, plus explicit outside-repo and inside-repo `--work` cases, checking exit/output and absence of residue. This recommendation does not change the frozen predicate or registration. Cannot establish whether the missing implementation already satisfies it.

## Exact commands and results
- `test -f /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r54-errata-truth.py; printf 'test_exit=%s\\n' "$?"` → `test_exit=1`; counter absent.
- Frozen scored command (not executed; file absent): `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` → **NOT RUN**.
- TMPDIR and --work probes → **NOT RUN** (counter absent).
- No pin-span command was needed; cited spans are registration's frozen table above, not fresh runtime output.

## Report trailer
`.ufo/waves/round-54/w2/R54W2Seat15.md` (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`). Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat15` was created empty and removed successfully (`rmdir` exit 0); nothing remains. No ENOSPC observed.