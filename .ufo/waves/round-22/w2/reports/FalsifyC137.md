# FalsifyC137 — C1 case CaptureStarUnknown (author-lane advisory critic)

**Verdict: AGREE** for this one sealed case on delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. This is not admission and not a non-author grant. It is not proof of the F2 family either.

## Identities (checked before and after the run; no drift)

| artifact | sha256 |
|---|---|
| `tools/mado-tripwire.py` (C1) | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (matches assignment) |
| `tools/mado-evidence-audit.py` (C2, not run) | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` (matches) |
| `oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` (matches) |
| `audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` (matches) |
| `oracle/measure.py` (runner) | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `oracle/inputs/CaptureStarUnknown.jsonl` | `20d94aa683e93e2537dcfce5d7acb7f7a858b6bce40c98ac07fa84d7a6a4d447` (= sealed `input_sha256`) |
| `w1/proposals/CaptureStarUnknown.json` | `459af4c81ec067ad685032f72b661030ae291ccb8ce1437bc11c381a8930ee62` (= sealed proposal sha) |
| producer `assemble.py` (runner-reported) | `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600` |
| population (runner-reported) | `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` |

The runner validated the full population before and after the run: 106 sealed sources, 52 proposal files and 57 inputs. It then ran exactly one case.

## Measurement (the only scanner run)

`python3 -I .../oracle/measure.py --tool .../tools/mado-tripwire.py --case CaptureStarUnknown` produced runner exit `0`, status `complete`, totals `1/1` and empty stderr. One scanner child ran under the runner's `RLIMIT_AS` = 384 MiB and 15 s caps. Child exit `0`, child stderr empty.

The actual scanner rows:
- `findings: []`, `observed_findings: 0`, `lead_findings: 0`, and every class count is 0.
- `files[0]`: `eval_calls 1`, `eval_unparsed 0`, `unparsed_spawns 1`, sha equals the sealed input.
- Oracle: `got_rows []`, `unparsed 1`, `pass true`, `reasons []`.

The raw receipt is `.ufo/waves/round-22/w2/receipts/FalsifyC137/result.json`, with `measure.stdout`, `measure.stderr`, `measure.exit` and `hashes-{before,after}.txt` alongside it.

## Independent semantic expectation (from source cell + Python 3.14 semantics, not tool output)

The cell:

```python
def make(unknown):
    def run(): subprocess.run(unknown)
    return run
unknown = ["pacman", "-Q", "r22-starunk-decoy"]
parts = list(input())
runner = make(*parts)
runner()
```

- `parts` is a list of the characters of an opaque `input()` string. `make(*parts)` raises TypeError unless the input is exactly one character, and in that case `runner()` never runs.
- When the input is one character, `unknown` is make's parameter. `run`'s free variable `unknown` resolves to make's cell (the nearest enclosing scope), never the module global. The spawn is then `subprocess.run("<c>")`: a real execution whose argv is statically unknowable.
- Expected class/command/evidence: no serializable command exists at any tier. The sound outcome is zero rows (no observed, and no lead, since a lead needs a literal) plus a positive unparsed signal. `accept_exact_want = null` is correct, because no exact alternative truth exists here.
- Expected kind: `uncertain` with `require_signal: true`. Total silence would be a lost true command, because the spawn can execute.

The actual output matches all of this exactly.

## Falsification attempts for this case

| attack | outcome |
|---|---|
| False observed argv / borrowed global | Refuted. No rows at any tier, and neither decoy command appears. |
| Lead downgrade of the decoy (the "cheap patch" shape) | Refuted. There is no lead row. |
| Lost true command (silence) | Refuted. `unparsed_spawns 1` is present. |
| Wrong identity: global vs. lexical parameter | Source path supports the correct identity (below). |
| Lifetime | Not applicable beyond this case. There is a single cell and no rebinding of `parts` or `unknown` after the factory call. |
| Conditional target | Not applicable. `make` has an unconditional Name return. |
| Parsed-clean ambiguity | Refuted. `eval_unparsed 0` is honest because the cell parsed. The uncertainty is carried by `unparsed_spawns`, not reported as clean. |

Here is the mechanism behind the signal, read from source as data and not separately measured:

1. In `factory_result` (around line 1652), `bind_literal` returns `None` for the non-literal star.
2. `binding_failure` reports `"uncertain"`, not `"invalid"`, so `bound = {unknown: LITERAL_MISS}`.
3. `local_env.update(bound)` runs after the module env is copied, so the lexical parameter shadows the decoy global. The returned helper's `closure_env` overlay carries `unknown → LITERAL_MISS`.
4. At `runner()`, `spawn_scan` (around lines 2511–2516) applies that overlay. `follow_helper(run)` then reaches `subprocess.run(MISS)`, `argv_strings` returns `None`, and `unparsed += 1` (around line 2684).
5. `make(*parts)` itself is swept (`sweep_body(make)`). That sweep finds no calls and no refs, because `return run` is not a recorded ref, so there is no double count.

## Uncertainty boundaries / limits

- `[INFERENCE]` The scanner reports unparsed spawns only as a per-file total, not per site. The measurement alone cannot prove that the one unparsed count belongs to `subprocess.run(unknown)`. That attribution rests on the code reading above; `spawn_scan` also increments the same counter for `kind == "uncertain"` callables (line 2463).
- **Oracle looseness (fixable defect in the oracle, not the tool; does not change this verdict).** For an uncertain case with no wanted leads, `evaluate` accepts any lead row whose command is not in `forbid_commands_any_tier`. By this case's own rationale, any row at any tier is a fabrication. Yet a hypothetical invented lead such as `pacman -S r22-starunk-other` would still pass. The smallest safe correction is a future, separately sealed addendum or oracle rule that requires zero rows for this case: "no serializable literal exists". It must not be applied post-measurement to this round's denominator. The actual delivered output has zero rows, so the gap is not exercised here.
- Scope: one fixture, one tool revision. Nearby forms remain unclaimed by this result:
  - `make(*args)` with a varargs factory and an unknown star
  - an unknown star through `functools.partial`
  - a multi-cell factory with the unknown star
  - a star whose value is mutated later

  Prior r19/r20/r21 rejected-harmed receipts and the streak are untouched.

No production, fixture, expected or proposal files were edited. There were no installs, no extra scanner runs, no old-tool runs and no C2 execution.

Report: .ufo/waves/round-22/w2/reports/FalsifyC137.md
Rendered absolute path: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC137.md
