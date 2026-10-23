# ExecSuiteProbes — round 28, wave 2

## Axis and change

- Axis: C1 operability, PRED-C1-r28 leg `h1-rotation` (frozen claim in `registration.md`; not edited).
- Updated only `quality/counter-selftest.py` outside this report. Added three behavioral checks and their required-inventory names: `c1-node-subset`, `c1-version-missing-commit`, and `c1-extra-output-segment`; added the absent-commit fake version; updated the documented count from 55 to 58 probes. Existing check bodies were not changed.
- The new fixtures exercise table behavior: `out[0].pop()` for a strict node subset, `VERSION_MISSING` for an absent commit, and `out.append([])` for an extra output array. Expected assertions require a rejected subject (the version case requires `ORACLE_VERSION`).
- Created three counter copies under `/fast/scratch/hyaku/mado-r28/ExecSuiteProbes/` and changed each specified expression: `node-subset.py` uses `gn <= en`; `missing-version-guard.py` only rejects a non-absent wrong commit; `extra-output-segment.py` accepts `len(data) >= 2`. They were not compiled or run.

## Exact retained evidence

The edit tool returned these source lines (implementation, not runtime results):

```text
Checks (58 behavioural probes + 1 fixed-inventory gate):
+      c1-node-subset      tool omits one node (strict subset)    -> exit 1, TARGET_MISSED
+      c1-extra-output-segment tool adds a third output array     -> exit 1, TARGET_MISSED
+      c1-version-missing-commit version commit absent             -> exit 2, ORACLE_VERSION
+VERSION_MISSING = {"tag": "v0.56.2"}
+    + ["c1-invalid-json", "c1-malformed", "c1-extra-output-segment", "c1-tool-exit", "c1-near-perfect",
+       "c1-node-subset", "c1-drift", "c1-drift-bezier", "c1-oracle-fail",
+       "c1-version-guard", "c1-version-missing-commit"]
+            C1_BASE, mut="out.append([])")
+        rc, out = run_case(c1, run_dir, a.rev, "c1-node-subset", C1_BASE, mut="out[0].pop()")
+                           C1_BASE, version=VERSION_MISSING)
```

Mutant edits shown by the edit tool:

```text
ok = gn <= en and gb == eb
if commit is not None and commit != HYPR_COMMIT:
return (isinstance(data, list) and len(data) >= 2 and all(isinstance(x, list) for x in data)
```

Lane revision command and output:

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse master; rc=$?; printf 'exit=%s\n' "$rc"
4f610066efd90804b055c42ae20c41a7f44404f9
exit=0
```

Scratch setup command returned exit 0 with no output:

```text
mkdir -p /fast/scratch/hyaku/mado-r28/ExecSuiteProbes && cp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/c1/count-v2.py /fast/scratch/hyaku/mado-r28/ExecSuiteProbes/node-subset.py && cp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/c1/count-v2.py /fast/scratch/hyaku/mado-r28/ExecSuiteProbes/missing-version-guard.py && cp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/c1/count-v2.py /fast/scratch/hyaku/mado-r28/ExecSuiteProbes/extra-output-segment.py
```

LSP lookup command returned exit 0 and no output (its `true` fallback ran): `command -v pyright-langserver || command -v pylsp || command -v basedpyright-langserver || true`. No LSP tool is exposed in the provided tool inventory.

## Checks, failures, and blockers

The required suite/scorer commands were **not run**: fleet executor policy says to skip all builds, lint, tests, and formatters while the editing wave is in flight. Therefore no exit code or runtime output is claimed for any of these:

- Red-before committed suite on the three mutants.
- Green-after suite on pristine C1+C2 and rejection on each mutant; `SELFTEST pass=TOTAL` was not measured.
- Frozen scorer on H1 with the new suite; no `PRED-C2-r27-v2` result or `CASE H/HeldC1v2` rows were captured.
- Either K1 control score.
- Mutant compilation.

The frozen scorer source's output template (source evidence only, not a run result) is:

```text
PRED-C2-r27-v2 green=%d/%d b_valid=%d w_killed=%d/%d h_killed=%d/%d h_need=%d h_valid=%d h_min_per_subject=%d invalid=%d verdict=%s
```

A read attempt for `.ufo/waves/round-26/c2/count-v2.py` returned not found; the registered C2 subject is `.ufo/waves/round-26/c2/count.py`, which was read instead. The first scratch-directory read found no directory; setup then created it. No package was installed. No other checks were run, and no check failure is represented as a pass.

## Files written and risk

- `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counter-selftest.py`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/w2/reports/ExecSuiteProbes.md`
- Scratch only: the three named mutant copies above.

Risk/blocker: the requested behavioral outcomes, suite inventory total, frozen H1 target, and K1 misses remain unmeasured pending the parent-owned post-integration gate. No runtime claim is made.