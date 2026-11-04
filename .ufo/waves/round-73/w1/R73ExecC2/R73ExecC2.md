# R73ExecC2 — independent C2 execution

## Axes and scope

Axes: C2 operability/carrier recognition; calibration against the frozen controls; no harm to committed files. This seat measured the frozen instrument, without implementation changes. Calibration C1 was not re-scored.

Only the seat-owned directory contains new report/evidence files. The contradictory trailer requesting `w1/R73ExecC2.md` is superseded by the hard only-write-directory bound; the report is inside `w1/R73ExecC2/`.

## Commands and results

Working directory for both commands: `/home/vgpnk/Projects/shokunin/mado-shokunin`. They ran concurrently; the counter writes its own `r73-c2-shapes` subdirectory, while the selftest writes its tampered-control fixture at the supplied scratch root.

### Frozen count

```sh
python3 -I quality/counters/c2-r73-shapes.py --repo . --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9 --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --controls .ufo/waves/round-73/controls/c2-cases-r73.json --scratch-root /fast/scratch/hyaku/mado-r73/R73ExecC2/run
```

Exit code: **0**. Stderr: empty.

Last stdout line:
```text
MADO_R73_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=28/28 base_controls=25/28 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

### Hermetic selftest

```sh
python3 -I quality/counters/c2-r73-shapes.py --selftest --controls .ufo/waves/round-73/controls/c2-cases-r73.json --scratch-root /fast/scratch/hyaku/mado-r73/R73ExecC2/run
```

Exit code: **0**. Stderr: empty.

Last stdout line:
```text
MADO_R73_GUARD_SHAPES_SELFTEST: 75/75 assertions passed
```

## Reconciliation

`count.json` retains the full command, rc, stdout and stderr. Its stdout is byte-identical to the committed `measurement-c2-r73.txt` (compared through the raw reader). Every reader row, all 28 candidate rows, all 28 baseline rows, both control digests, the baseline counter digest, and the terminal contract line agree. **No differences.**

Observed rc 0 agrees with TARGET_MET and the frozen contract. The terminal counts are population 20, readers 13, guarded 13, unguarded 0, candidate controls 28/28, base controls 25/28. The baseline misses exactly `global-rebind-guard`, `environ-splat-guard`, and `environ-call-guard`, as in `control-baseline-r73.txt`. The selftest returns rc 0 with 75/75 assertions; it is a separate selftest marker, not a contradictory population contract.

## Four independently invented snippets

Executed using Python Eval: `subprocess.run(["git", "show", "1459cca11fb5d3956a6e9a128217852dd0c28cb9:quality/counters/c2-r73-shapes.py"], cwd=repo, capture_output=True)` returned rc 0. The returned committed bytes were loaded with `exec(compile(stdout, "<frozen-c2-r73-shapes>", "exec"), {"__name__": "r73_independent_classifier"})`, then the resulting `classify(source)` was called for each snippet below. This evaluates classifier inputs as text; it never executes their environment mutations or git launches. Tuple order is `(reader, guarded)`; functions return tuples, not process exit codes.

The snippets exercise both intended positives and meaningful negatives: a guard key stored globally; a guard name occurring only as a value; a process-environment guard copied with `dict`; and an intervening environment replacement that cancels the earlier guard.

### global-subscript-positive

```python
import os
import subprocess
child_context = dict(os.environ)
def enable_object_safety():
    global child_context
    child_context["GIT_NO_REPLACE_OBJECTS"] = "1"
enable_object_safety()
subprocess.run(["git", "log", "-1"], env=child_context)
```

Independent expected: `(True, True)`. Actual: `(True, True)`. Agrees: **yes**.

### global-value-negative

```python
import os
import subprocess
child_context = dict(os.environ)
def annotate_child():
    global child_context
    child_context = {"TRACE_LABEL": "GIT_NO_REPLACE_OBJECTS"}
annotate_child()
subprocess.run(["git", "log", "-1"], env=child_context)
```

Independent expected: `(True, False)`. Actual: `(True, False)`. Agrees: **yes**.

### environ-dict-positive

```python
import os
import subprocess
os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
subprocess.run(["git", "cat-file", "-t", "HEAD"], env=dict(os.environ))
```

Independent expected: `(True, True)`. Actual: `(True, True)`. Agrees: **yes**.

### environ-replaced-negative

```python
import os
import subprocess
os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
os.environ = {"PATH": "/usr/bin"}
subprocess.run(["git", "cat-file", "-t", "HEAD"], env={**os.environ})
```

Independent expected: `(True, False)`. Actual: `(True, False)`. Agrees: **yes**.

## Evidence, limits and handoff

- `count.json`: exact count argv, rc 0, complete stdout, empty stderr.
- `selftest.json`: exact selftest argv, rc 0, complete stdout, empty stderr.
- `snippets.json`: frozen revision and instrument SHA-256, git-show rc 0, four complete sources, expected/actual tuples and agreement flags.
- Findings: no receipt difference, rc contradiction, or classifier disagreement observed.
- Limits: these four examples do not establish semantic soundness or coverage beyond the declared syntactic grammar. Global flow retains the declared cross-function line-order approximation.
- No committed file edited; no tool installed; no LSP operations required (no code changes); no build, formatter or broad integration gate run. Parent owns broader no-harm gates.
- Scratch was used only at `/fast/scratch/hyaku/mado-r73/R73ExecC2/`; all cited evidence is retained in this directory before removing scratch.
- Blockers: none.

## Self-assessment

Accuracy 4/5: direct receipts and tuple outputs support all findings; no general semantic guarantee is claimed. Completeness 5/5: both assigned executions, reconciliation and four snippets are retained. Clarity 4/5: commands and outputs are explicit; Python Eval loading is less portable than a standalone driver. Actionability 4/5: frozen argv is directly repeatable, while snippet execution requires the documented loading recipe. Conciseness 4/5: snippets repeat imports for independent readability. Overall 4.2/5. Improvement: a future measurement protocol could standardize a standalone snippet-driver command. Would the user agree? Likely, because all required evidence is present without widening scope.

Report: .ufo/waves/round-73/w1/R73ExecC2/R73ExecC2.md
Frozen count: TARGET_MET, rc 0; receipt identical.
Selftest: 75/75, rc 0; four snippets agree.
No production changes or blockers; scratch removed.
