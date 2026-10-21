# MethodcallerInvoke — scoped attack

Reviewed candidate `tools/mado-tripwire.py` at commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`; its exact SHA-256 was `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.

## Finding

**Medium — an invoked `operator.methodcaller` stored in a local is missed.** The current repair recognizes only the inline construction-and-invocation form at `tools/mado-tripwire.py:2220-2230`: it requires `node.func` itself to be a call to `operator.methodcaller`, then synthesizes the dispatched call. If the returned callable is assigned first, `assignment_binding` treats the `operator.methodcaller(...)` result as a value (`:1678-1709`), and the later call through that local is skipped by the pure/value branch (`:2293-2294`). This is a nearby invocation of the same process sink, not the stored-and-discarded control.

I retained the probe at `.ufo/waves/round-21/w2/fixtures/AtkMethodcallerInvoke-2/methodcaller-stored-invoked.jsonl` (SHA-256 `4dafe27e0614381fd43b01741842157590fb47f62fdf07dd65905c38ed3e2a42`). Its second tool-call code is:

```python
import operator, subprocess
invoke = operator.methodcaller("__call__", ["pacman", "-Q", "methodcaller-stored"])
invoke(subprocess.run)
```

Expected from source semantics: an `observed` `package_query` finding for `pacman -Q methodcaller-stored`. Actual bounded scanner output contained only the baseline row (`pacman -Q r21`, line 1, `observed`); it emitted no row for line 2. The payload reported `package_query: 1`, `eval_calls: 2`, `eval_unparsed: 0`, `unparsed_spawns: 0`, and `observed_findings: 1`. Scanner exit was 1 because the baseline finding is unpermitted, not because the probe failed to parse. This falsifies generality across the nearby stored-then-invoked form; it does not invalidate the frozen inline case.

## Frozen oracle and direct-form generality

The frozen `MethodcallerInvoke` expectation is semantically warranted: `operator.py:310-327` documents and implements `methodcaller.__call__` as `getattr(obj, name)(*args, **kwargs)`. With `name == "__call__"` and `obj == subprocess.run`, this invokes `subprocess.run` with the bound argv. `subprocess.py:513-515,555-557` describes `run` as running a command and shows it delegates to `Popen`. `tools/mado-tripwire.py:737-771` classifies `pacman -Q` as `package_query`. Because this is a direct top-level invocation with literal argv, `evidence: observed` is correct. Conversely, the stored/discarded control constructs a methodcaller but never enters its `__call__`; the stdlib constructor merely stores its name/arguments (`operator.py:319-324`), so its empty expectation is correct.

For the exact inline form, the repair is structural rather than keyed to fixture path or `r21`: the code resolves the callable identity as `operator.methodcaller`, requires a literal method name, and forwards bound args/kwargs. A bounded alias probe also passed with a changed package operand: `from operator import methodcaller as invoke; invoke("__call__", ["pacman", "-Q", "methodcaller-alias"])(subprocess.run)` produced `observed package_query` rows for both the canonical baseline and `pacman -Q methodcaller-alias`, with no unparsed spawns. Its inert input is retained at `.ufo/waves/round-21/w2/fixtures/AtkMethodcallerInvoke-2/methodcaller-alias.jsonl` (SHA-256 `6996d8ffabaee0cdbfc7c02d48d375d39c59e43eca5c64a5d816f3e62ec2b3c0`).

## Verification gaps and provenance

- Both probes used the existing `oracle/measure.py` `scan` API. Its source sets `RLIMIT_AS` to 384 MiB and a 15-second subprocess timeout (`measure.py:12-38`). The scanner parsed inert JSONL; neither fixture's Python code nor any shell/pacman payload was executed. No corpus/full suite was run.
- The provided `evidence/oracle-candidate.json` is stale for this candidate: it records commit `843d301d1b17af78427918f7845af336b2218de0` and scanner SHA-256 `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`, and its MethodcallerInvoke row has no finding. Do not attribute that receipt to the reviewed `f499a8db...` bytes; the bounded probes above exercised the current SHA-256 instead.
- LSP status/references/definition/diagnostics were unavailable: attempting `xd://lsp` returned “No such tool” and listed no LSP device. Grep was only used to locate source; semantic conclusions above rely on direct source reads and the bounded scanner observations.
- No tools were installed.

## Verdict

The frozen expected row is correct, and the repaired inline form handles a changed import alias and argv rather than matching the frozen text. One actionable nearby false negative remains: storing the methodcaller callable and invoking it later is semantically the same sink but is silently treated as a value. This is a scoped recommendation, not a promotion or admission.

Report: .ufo/waves/round-21/w2/reports/AtkMethodcallerInvoke.md