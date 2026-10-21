# CallableFunction — C1 adversarial review
Axes: semantic warrant of the frozen expectation; binding-sensitive generality of the rule; nearby-variant falsification; evidence and verification completeness.

## Findings (severity ordered)

No actionable finding in the scoped CallableFunction case. The frozen empty expectation is semantically warranted for the exact input, and the current scanner distinguishes the builtin predicate from a same-named rebound helper in one nearby falsification probe.

## Frozen expectation

The frozen case at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json:32-40` binds the `CallableFunction` id to the one-line input `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/inputs/CallableFunction.jsonl` (SHA-256 `240f1d469ee6ad3d41c50d04dd03115cfe90152f87b3ff95b5780d9aa1fb5117`) and `want: []`. The proposal file `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/CallableFunction.json` has the frozen proposal SHA-256 `623292b6283d4d34345116ee762be22333e01a7e305379d2979563094a3848ab`.

That empty set is warranted: `def f()` creates a function object and does not execute its body; the only call is the unshadowed builtin `callable(f)`, which asks whether `f` appears callable, not to invoke it. Therefore the nested `subprocess.run(["pacman", "-Q", "hyprland"])` is not reached, and there is no class/command/evidence tuple to assert. The exact rationale in the proposal matches Python's documented semantics: [function definitions](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions) and [`callable`](https://docs.python.org/3.14/library/functions.html#callable).

The existing receipt `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/evidence/oracle-candidate.json` also records `CallableFunction` as passing with no findings, but it is explicitly measured at commit `843d301d1b17af78427918f7845af336b2218de0`; I treat it as historical support, not as a run against the current candidate.

## Rule generality and one nearby variant

Current candidate bytes were SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`, at commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.

The relevant behavior is not a match on fixture text or the exact expression `callable(f)`: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1490-1500` puts builtin `callable` in the general pure-argument-call set; `callable_info` first consults active bindings and only falls through to that builtin set when unbound (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1577-1602`); and `spawn_scan` skips sweeping a referenced body when the call receiving that reference resolves to a pure/value callee (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2371-2393`). Thus an unshadowed builtin check does not follow `f`'s body. The binding-first lookup is important: a local definition or assignment named `callable` is not automatically granted the builtin's non-invoking semantics.

I derived and ran one nearby variant that keeps the same `callable(f)` spelling but rebinds `callable` to a helper that invokes its callback. The retained inert JSONL is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkCallableFunction/callable-shadow-invokes.jsonl` (SHA-256 `d99fdcaf61996680721dfd8594c55965fb82e4fb9706db52f35509d59d166606`). Its code payload was only parsed by the scanner; it was never executed:

```python
import subprocess

def f():
    subprocess.run(["pacman", "-Q", "hyprland"])

def callable(callback):
    callback()

callable(f)
```

The bounded `measure.py` scan API returned this observed result (the outer and payload exit 1 indicate an unpermitted finding, not a scanner error):

```json
{
  "exit": 1,
  "payload": {
    "counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0},
    "exit": 1,
    "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkCallableFunction/callable-shadow-invokes.jsonl", "sha256": "d99fdcaf61996680721dfd8594c55965fb82e4fb9706db52f35509d59d166606", "unparsed_spawns": 0}],
    "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "evidence": "observed", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkCallableFunction/callable-shadow-invokes.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "None", "tool": "eval", "tool_call_id": "CallableFunction-variant"}],
    "lead_findings": 0,
    "observed_findings": 1,
    "permitted": [],
    "schema": "mado-tripwire-verdict-v1",
    "unpermitted": 1
  },
  "stderr": ""
}
```

This is a successful challenge of the binding rule, not a counterexample: rebinding changes the semantics to actually call the callback, and the scanner reports the reached command. In the current resolver this is supported by binding the helper argument in `follow_helper` (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2155-2198`) and following the resolved helper call (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2248-2274`). One nearby variant is only a falsification attempt, not a global no-counterexample proof.

The probe used `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/measure.py` via `runpy` and its `scan` API. That API starts one scanner child with `RLIMIT_AS=402653184` and a 15-second timeout (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/measure.py:12-38`). It completed without timeout, parse errors, stderr, unparsed evals, or unparsed spawns. No fixture Python or shell payload was run.

## Residual risk and verification gaps

- Scope is only this callable-function shape and one rebinding variant; no whole-suite or corpus run was performed (L1 owns final verification).
- No LSP device/server was mounted: requesting `xd://lsp` returned `No such tool`, so no LSP status, references, definition, or diagnostics were available. Source reads and official Python documentation support the semantic conclusions; text search was used only for literal location, not as semantic proof.
- Tools installed or updated: none.

**Verdict:** Recommend retaining the frozen `want: []` for this exact builtin-call case. No actionable CallableFunction defect was found in this bounded review.

Report: .ufo/waves/round-21/w2/reports/AtkCallableFunction.md
