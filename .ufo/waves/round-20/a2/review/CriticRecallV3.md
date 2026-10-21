# CriticRecallV3 — falsified: v3.1 drops a real partialmethod spawn and all four tools miss a called Bash function form

Axes assessed: real-execution recall, row precision/evidence, and shell-shape coverage.

## Method and totals

Created 66 unique eval/bash JSONL fixtures in `../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/`, avoiding copies of the three named wave-2 fixture sets. Ran each fixture as the sole `--scan` input in its own process with each pinned tool: 264 scans total. No scan returned exit 2. Python fixture code was AST-parsed but never executed; the one Bash counterexample was checked with `bash -n` and a harmless `/bin/echo` dispatch canary only. No `pacman` or `git` payload was run.

Pinned tool SHA-256:

- `9c54c56`: `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`
- `1f7f995`: `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`
- `28c6837`: `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`
- `a8960de`: `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458`

| Tool revision | Finding rows | Fixture files with rows | Classes (`package_query`, `vcs_write`, `host_mutation`) | Evidence rows |
|---|---:|---:|---|---|
| `9c54c56` | 61 | 57/66 | 55, 0, 6 | old schema has no evidence field |
| `1f7f995` | 71 | 65/66 | 55, 10, 6 | old schema has no evidence field |
| `28c6837` | 37 | 31/66 | 24, 7, 6 | old schema has no evidence field |
| `a8960de` | 70 | 64/66 | 54, 10, 6 | 37 observed, 33 lead |

## Findings

### 1. v3.1 loses an older finding on an executed `functools.partialmethod` call

- Input: `../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/py-partialmethod-helper.jsonl` — SHA-256 `07be360f62eac2de74be77eefc07833ce58cc1d17b49dfd01b7c3acc0dcbb80e`.
- Shape: a visible instance method is wrapped by `functools.partialmethod`, then invoked as `C().run()`. Python's descriptor binds the instance and calls `worker`, which issues `subprocess.run(['pacman', '-Q', 'a2rc'])`.
- Reproduce from the lane root (each command is a separate one-file process):

  ```sh
  python3 -I ../../../../../tmp/CriticRecallV3/tw-9c54c56.py --scan ../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/py-partialmethod-helper.jsonl
  python3 -I ../../../../../tmp/CriticRecallV3/tw-1f7f995.py --scan ../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/py-partialmethod-helper.jsonl
  python3 -I ../../../../../tmp/CriticRecallV3/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/py-partialmethod-helper.jsonl
  python3 -I ../../../../../tmp/CriticRecallV3/tw-a8960de.py --scan ../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/py-partialmethod-helper.jsonl
  ```

- Observed: `9c54c56` and `1f7f995` each report one row: `package_query`, rule `pacman:-Q`, command `pacman -Q a2rc` (their schema omits an evidence field). `28c6837` and `a8960de` return `clean`, with `findings: []`.
- Expected: v3.1 retains the `package_query / pacman:-Q / pacman -Q a2rc` row. This is not a speculative body: the visible `C().run()` call invokes the partial-method descriptor and its `worker` body.
- Impact: **recall**; this falsifies the no-lost-finding claim for real-execution shapes. The probe does not alter the frozen w2 population or its reported counter.
- Smallest safe correction: resolve a visible `functools.partialmethod` class-body alias to its underlying helper and bound literal arguments only when that alias is called on a visible class/instance. Do not treat every class attribute or descriptor as executable.

### 2. All four tools miss a called Bash `function name { ... }` with a trailing same-line call

- Input: `../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/bash-function-commit-positional.jsonl` — SHA-256 `269d0d05e4ab505c92287f9150eb1db0d631894e4c7ddbfe6c66e049e7d58d1f`.
- Shape: `function record { git commit -m "$1"; }; record a2rc`. `bash -n` accepted the syntax. A harmless same-shape canary printed `git commit -m a2rc` from inside the function; the fixture itself was not executed.
- Reproduce from the lane root, one process per revision:

  ```sh
  python3 -I ../../../../../tmp/CriticRecallV3/tw-9c54c56.py --scan ../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/bash-function-commit-positional.jsonl
  python3 -I ../../../../../tmp/CriticRecallV3/tw-1f7f995.py --scan ../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/bash-function-commit-positional.jsonl
  python3 -I ../../../../../tmp/CriticRecallV3/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/bash-function-commit-positional.jsonl
  python3 -I ../../../../../tmp/CriticRecallV3/tw-a8960de.py --scan ../../../../../tmp/mado-r20a2-CriticRecallV3/fixtures/bash-function-commit-positional.jsonl
  ```

- Observed: all four return `clean`, with no rows. Expected: `vcs_write`, rule `git:commit`, command `git commit -m a2rc`.
- [INFERENCE] `tools/mado-tripwire.py`'s `shell_functions` parser only captures a same-line definition when its closing brace is the line's final unquoted character; the trailing `; record a2rc` prevents the function body from being recorded and expanded. The parser documents support for `function name { ... }` but this valid suffix form is missed.
- Impact: **shell recall**. This is an all-tool miss, not a v3.1-only regression.
- Smallest safe correction: recognize the definition's matching close-brace token even when another command follows it on the same logical line, then process the trailing call with its literal positional arguments.

## Shapes all tools miss

- `bash-function-commit-positional.jsonl` — the same-line Bash `function name { body; }; name args` form above. All revisions returned no rows; expected `git:commit`.

The signal-handler probe was treated as **contingent**, not as a guaranteed-execution result: signal support and delivery conditions can vary. It is not used in either counterexample.

## Limits

This is an external, synthetic 66-fixture probe, not a rerun of `a2-guards.py` or a claim that the frozen w2 52-to-0 count changes. It demonstrates one real older-row loss in an added shape and one shape all tools miss. Transcript payloads were only parsed/scanned; no fixture code, package query, or VCS operation was run. No tool was installed or updated.

## Installs

none
