# R87ExecFidelity — C2 control-figure fidelity (executor report)

Seat: R87ExecFidelity (executor). Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin. Base: e4875ba5619053cc3f91bb2f4d819e189df4088c.

## Files written

- `quality/counters/c2-r87-control-fidelity.py` (NEW, sha256 `e4654d9de1dc14a49576b0a8df2e57ad43ca98589735e725179c421cafdbed60`)
- `.ufo/waves/round-87/controls/r86-figures-r87.json` (NEW, sha256 `da21797b07e6ae09f4e78f49f4dcefceee17164c8af148c8ba7676bd125fe092`), content exactly as specified.
- `.ufo/waves/round-87/w1/R87ExecFidelity.md` (this report).

No other file was edited. No git mutation. The lane counters were not run at any REV.

## BLOCKER for the L1 — F2 stated_at text is absent from the file bytes

Figure F2 names `SCORECARD.md` text `flooding 48/75 vs held 75/75`. At base e4875ba this exact byte string does **not** occur.
The text is present only with a line wrap:

- `SCORECARD.md:5062-5063`: `... tool_selftest=152/152, flooding` / `48/75 vs held 75/75, TARGET_MET, exit 0 at \`3afdb713\`;`

Other forms present: `corpus/knowledge/refusal-records-clause-observations-r86.md:47` has `flooding=48/75 held_flooding=75/75` (different format, different file).

Per the item, I did NOT edit the figure file to match. The counter enforces byte-exact presence at REV, so the real run
exits 2 with `stated text absent from SCORECARD.md at <REV> (figure F2_flood_r86)`. Consequence: the declared "before = 5.0"
cannot be produced as specified; the base run is a setup error, not a verdict. The L1 decides the fix (for example,
re-pin the figure file with the wrapped text, or accept whitespace-normalised matching). Either change alters the pinned sha.

## Other base checks (read-only, at e4875ba)

- F1 stated_at `held_rule_new_case=0/1`: present, `corpus/knowledge/refusal-records-clause-observations-r86.md:112`.
- F1 stated_at `held rule 0/1 on the new anchor witness`: present, `SCORECARD.md:5034`.
- Receipt `final-c1-r86.txt` names rev `3afdb7136904b70b0a01ac31963b6e9b14320f1f`, base_rev `2b6dd76b65de4dfe701db87db13b7e448b3538ee`,
  and control sha `f6dd9cdef7daa2e6b51c95f27cf8ebe8509188c551ff18ed42a176a08d8620bf`. At `3afdb713`, `c1-cases-r86.json` hashes to that
  same value (checked with `git show | sha256sum`). The counter checks this at runtime.
- F2 re-run expectation: `flooding 48/75; held 75/75` (receipt line `MADO_R86_REFUSALS: ... flooding=48/75 held_flooding=75/75`).

## Counter design (as declared, section C2)

- Every input is read via `git -C REPO show REV:<path>` under the scrubbed env (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE,
  GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES removed; GIT_NO_REPLACE_OBJECTS=1). `--figures` is a repo-relative path read at REV.
- F1: loads `quality/counters/c2-r85-status-classes.py` at REV via importlib (`sys.dont_write_bytecode = True`), calls its
  `case_correct(case, 0, case["frozen"])` on `border-size-int`. Derived `1/1` or `0/1`. The r86 model is not used.
- F2: parses the receipt for rev, base_rev and control sha; extracts the r86 C1 counter and both control files from the named rev into scratch;
  verifies the control sha; re-runs the counter with `-I`, `--base-rev`, `--controls`, `--carried`, `--scratch-root` in scratch (TMPDIR pinned);
  parses `flooding=a/n held_flooding=b/m` from the `MADO_R86_REFUSALS` line.
- Reconciliation: reproduced, or a `Correction (round 87` heading in `corpus/knowledge/refusal-records-clause-observations-r86.md` or
  `SCORECARD.md` at REV whose block (to the next same-or-higher heading; fenced code ignored) contains the figure id AND the
  re-derived value, both token-bounded.
- Interpretation note: the frozen predicate says "in the same file". I implemented the RECONCILIATION rule of the item (either of the two r86 record files). If the L1 wants "same file as the stated_at", that is a one-line change.
- Output: per-figure `MADO_FIGURE:` lines, then the final `MADO_FIGURES:` line. Exit 0 met, 1 missed, 2 setup. `--expect-figures-sha256` mismatch → 2.
- Docstring carries the predicate sentence verbatim.

## Self-test (hermetic; fixture repos built with `git -C "$D" init -q`, toplevel verified before commit, commits with `-c user.name=mado-selftest -c user.email=selftest@invalid`)

Run 1 (first execution, transcript tail):
```
MADO_FIGURES_SELFTEST_FAIL: F2 corrected in SCORECARD -> exit 0 with reproduced=1 reconciled=2
MADO_FIGURES_SELFTEST: 14/15
SELFTEST_EXIT=1
```
Cause: my own assertion expected `reproduced=1`. In that case F1 is not reproduced (1/1 vs 0/1) and F2 is not reproduced (47/75 vs 48/75), so the correct value is `reproduced=0`, `reconciled=2`. The counter output was right; the test expectation was wrong.

I corrected the expectation to `reproduced=0` and re-ran once more (run 2):
```
MADO_FIGURES_SELFTEST: 15/15
SELFTEST_EXIT=0
```
Assertions (15): pure reconcile — correct block reconciles; bare heading no; wrong value no; id-only correction no; block ends at the next same-level heading; token-bounded value (`21/12` is not `1/1`). End-to-end — both reconciled → exit 0 TARGET_MET; no F1 correction → exit 1 with score 5.0000; bare heading in corpus → 1; wrong-value correction → 1; correction in another file → 1; absent stated text → 2 setup; sha mismatch → 2; heading scope → 1; F2 corrected in SCORECARD → 0.

The selftest used a stub `case_correct` in the fixture and an injected flood function. It does NOT exercise the real r85 module or a real r86 C1 re-run.

## Not executed (honest)

- The real counter was not run at the lane REV (per the item). The F1 value `1/1` is per the declaration and was not executed by me against the real r85 module.
- The F2 re-run of the r86 C1 counter at `3afdb713` was not executed by me.
- Expected base outcome after the F2 text fix is the declared `TARGET_MET` only if F1 is corrected by the L1 and F2 reproduces; that is for the L1 to run.

## Checks for the L1 to run

    python3 -I quality/counters/c2-r87-control-fidelity.py --repo . --rev REV \
      --figures .ufo/waves/round-87/controls/r86-figures-r87.json --scratch-root DIR

(after the F2 stated_at issue is resolved; expect 0 only with both figures reconciled).

## Installs

None. No pacman, no uv, no npm. Only the stdlib of /usr/bin/python3 (3.14.8) was used.

## Scratch

Scratch: `/fast/scratch/hyaku/mado-r87/R87ExecFidelity`. The selftest removes its own subdirectory. My `trap ... EXIT` in a subshell did NOT remove the seat directory (defect; the empty directory survived the subshell), so I removed it manually with `rm -rf`. The parent `/fast/scratch/hyaku/mado-r87/` is shared with other seats and is left in place.

## Summary for the L1

- C2 counter and figure file are written as specified; the counter's selftest passes 15/15 (exit 0).
- The F2 stated text is not present as bytes at base (wrapped across SCORECARD.md:5062-5063). Real run = setup error (exit 2) as designed. Needs an L1 decision.
- Not run: the real counter, the F1 derivation on real bytes, the F2 r86 re-run.
