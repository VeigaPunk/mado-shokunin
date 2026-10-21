# FalsifyC136 — C1 case CaptureStarKnown (author-lane advisory, NOT admission)

**Verdict: agree.** Delivered tool `tools/mado-tripwire.py` (sha256 `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`, identical before and after the run) produced exactly the sealed truth for this one case. No counterexample was found within this case. This is a single bounded static-shape agreement. It grants no admission, does not close F1/F2 families generally, and does not touch the r19/r20/r21 rejected-harmed receipts or the streak.

## Sealed truth (expected.json case `CaptureStarKnown`, group `proposal`)

- expected_kind `exact`; want = `[{host_mutation, "pacman -S r22-starknown", observed}]`; want_input_order identical to the raw proposal.
- forbid_observed_commands `["pacman -Q r22-starknown-rebound"]`; forbid_commands_any_tier `[]`; accept_exact_want `null`; require_signal `true` (derived default `bool(want)`; irrelevant to the exact branch, which requires `unparsed == 0`).
- Proposal `.ufo/waves/round-22/w1/proposals/CaptureStarKnown.json` sha256 `4ebb05df…cd4a` matches the sealed record; fixture `inputs/CaptureStarKnown.jsonl` sha256 `5fd61793…7f48` matches input_sha256. The runner verified the sealed population (106 seal files, 52 proposals, 57 cases) before and after the run. integrity_errors were empty.

## Independent semantic reasoning (payload not executed)

Here is the fixture cell:

```python
import subprocess
def make(*argv):
    def run():
        subprocess.run(argv)
    return run
t = ("pacman", "-S", "r22-starknown")
runner = make(*t)
t = ("pacman", "-Q", "r22-starknown-rebound")
runner()
```

1. `make(*t)` evaluates `t` at the call. Star-unpacking copies its elements into a new vararg tuple, so `argv == ("pacman","-S","r22-starknown")` in `make`'s frame. This is the correct identity and lifetime.
2. `run` closes over the `argv` cell of that frame. The later `t = …` statement rebinds a module NAME only, so it is inert for the closure. There is no global leak, because `argv` is a parameter and not a free global.
3. `runner()` runs unconditionally at top level in the same cell, so the spawn is certainly executed and `observed` is the correct tier. It is not a lead, and there is no conditional target.
4. `subprocess.run(<tuple>)` gives argv `pacman -S r22-starknown`. `pacman -S` is host_mutation, consistent with the r21 truth rows.
5. Every statement is statically determined, so the complete truth is exactly one observed row with `eval_unparsed = unparsed_spawns = 0`. A lead or unparsed downgrade here would be a defect, because the starred argument is a known literal tuple. Emitting the rebound `-Q` command at any tier would be invented argv (the F1 mechanism).

**Uncertainty boundary:** none within this case. The sealed truth is exact, and I agree with it.

## Actual rows (single authorized run)

Runner command: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureStarKnown`.

- The runner exited 0 with status `complete`, totals pass 1 of 1, and empty stderr.
- The scanner child (384MiB / 15s cap, one child) exited 1, which is the normal exit when there is an unpermitted finding. Its stderr was empty.
- got_rows was `[{host_mutation, "pacman -S r22-starknown", observed}]`, with rule `pacman:-S`, line 1 and tool_call_id `CaptureStarKnown-0`.
- unparsed was 0 (eval_unparsed 0, unparsed_spawns 0). observed_findings was 1 and lead_findings 0.
- The forbidden `pacman -Q r22-starknown-rebound` is absent at every tier.
- The result is an exact full-multiset equality with zero error counters, and reasons was `[]`.

## Mechanism check (read-only source inspection, so the green is not coincidental)

- In `factory_result`, `bind_literal(owner, call, env)` binds the factory's arguments using `env` at the factory-call statement. The starred argument binds only when `literal_value(arg.value, env)` is a list or tuple, and here it is the `-S` tuple.
- `factory_result` then snapshots `overlay = {name: local_env[name] for name in names}` into the returned helper's `closure_env`. `names` covers the bound parameters, prefix locals and inherited closure names only. The module `t` is not in `names`, so globals stay late-bound, while `argv` is frozen at creation. That is the semantically correct split.
- `bind_literal` stores the vararg as a list (`extra_args`), whereas Python makes it a tuple. This does not affect the argv serialization for this case, so it has no impact here.

## Impacted axes

None harmed by this case. It supports C1 (operability) for exactly one tested form: a known literal-tuple starred argument into a `*args` factory, with the caller variable rebound before the call. It says nothing about C2.

## Residual / untested (INFERENCE, not measured; no extra scanner run was authorized)

- One neighbour form is untested: a mutable list `t` mutated after `make(*t)`, for example `t.append(...)`. Python semantics leave the closure unaffected, because the starred copy makes a fresh tuple. Whether the tool's `mutated_literal` path wrongly downgrades this or leaks the post-mutation value is unmeasured. It is a candidate for a separately assigned probe, not a finding.
- Absence of a counterexample here does not certify other F1/F2 triggers. Per supported-forms, a finite pass closes only the named tested form.

## Smallest safe correction

None required for this case.

## Hashes and receipts

- tool before/after: `36fdc459…adce` / `36fdc459…adce`
- runner `measure.py`: `41b021bb…c7` (matches the runner_sha256 materialized in expected.json)
- expected.json: `b5cd4cf3…4357`
- population: recorded in the receipt
- Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC136/result.json`. Next to it are `measure.stdout`, `measure.stderr`, `measure.exit`, `hashes-before.txt` and `hashes-after.txt`.
- No installs, no edits to production, fixture or expected files, and no other scanner runs.

Report: .ufo/waves/round-22/w2/reports/FalsifyC136.md
(rendered at /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC136.md)
