# NeverReferenced — C1 adversarial review

Axes: semantic warrant of the frozen expectation; AST/call-reachability generality; one nearby falsification attempt; evidence and scope completeness.

## Findings (severity ordered)

No actionable finding in the scoped NeverReferenced case. The frozen empty expectation is semantically warranted for the exact input, and the current rule is not keyed to this fixture’s text: it distinguishes a function body that is merely defined from a reachable call. One nearby alias-call variant also reaches and reports the expected command. This is a bounded falsification attempt, not a global no-counterexample proof.

## Frozen expectation

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json:416-425` freezes `NeverReferenced` with `want: []`; the file SHA-256 is `fd2bfbc86897e1ee7a79302f6ccf6c3403709b132180864a0674f8212925576f`. Its exact input is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/inputs/NeverReferenced.jsonl`, SHA-256 `47e9f2e27d037418a5ccd9dbaccc03589fde54824b41a142aeb1fd9f7a9add42`. The proposal `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/NeverReferenced.json` has SHA-256 `9f4db16f33ec9bc641b83bace2aff2183bfda09fb3cc9b1e545a761eb456000b` and rationale matching the frozen record.

That empty class/command/evidence multiset is warranted. Executing this eval binds `f` to a function object; it does not call `f`. Python defers the function suite until the function is called, so its `subprocess.run(["pacman", "-Q", "r21"])` statement is not reached. No `package_query` observation or lead is warranted for this transcript. See the Python 3.14 [function-definition reference](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions) and [execution model](https://docs.python.org/3.14/reference/executionmodel.html#structure-of-a-program).

## Rule generality and one nearby variant

Tested scanner: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`; its latest path commit is `f499a8db7171b7476fe9f204ab9edbac5a956fa9` (`round-21: preserve reached implicit protocols and callable bindings`). The scanner file was clean in the worktree when checked.

The behavior follows the code’s general AST/call treatment, not a string match on this fixture. `eager_calls` documents that it collects calls executed by the statements and skips deferred function bodies; for a function definition it visits decorators and defaults, not the body (`tools/mado-tripwire.py:1813-1893`). `classify_eval` passes those eager calls and collected references into `spawn_scan` (`:2009-2041`). `update_bindings` records a function definition as a helper (`:1717-1726`); `spawn_scan` follows a resolved helper call, and its later reference sweep only considers references it actually collected (`:2201-2451`). Thus the primary input produces no call or reference to `f` and leaves its deferred body silent. This is shape-based handling; it does not depend on the fixture id, command spelling, or function name.

I derived one nearby positive-control variant by aliasing and then calling the same helper. The inert JSONL is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkNeverReferenced-2/alias-invoked.jsonl`, SHA-256 `1f4ac1974bd82f789a974e47033b34c1e7b62e1ebdcd21a7167bb40ab669d707`. Its Python payload (data only; never executed) is:

```python
import subprocess

def f():
    subprocess.run(["pacman", "-Q", "r21"])

queued = f
queued()
```

The bounded `measure.py` scan API, loaded with `runpy`, reported the reached call as observed:

```json
{
  "exit": 1,
  "payload": {
    "counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0},
    "exit": 1,
    "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkNeverReferenced-2/alias-invoked.jsonl", "sha256": "1f4ac1974bd82f789a974e47033b34c1e7b62e1ebdcd21a7167bb40ab669d707", "unparsed_spawns": 0}],
    "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q r21", "evidence": "observed", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkNeverReferenced-2/alias-invoked.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "None", "tool": "eval", "tool_call_id": "NeverReferenced-2-alias-invoked"}],
    "lead_findings": 0,
    "observed_findings": 1,
    "permitted": [],
    "schema": "mado-tripwire-verdict-v1",
    "unpermitted": 1
  },
  "stderr": ""
}
```

The exit 1 is the scanner’s unpermitted-finding status, not a parse or timeout failure. This variant is consistent with the intended rule: the alias call reaches the body, unlike the frozen case.

I also scanned only the exact frozen NeverReferenced input against the same current candidate through that bounded API. Output: exit 0; `package_query`, `host_mutation`, `live_probe`, `tool_install`, and `vcs_write` counts all 0; `findings: []`; `eval_unparsed: 0`; `unparsed_spawns: 0`; stderr empty. The current scan confirms the frozen result at the tested code identity. The supplied `oracle-candidate.json` receipt is historical (`measured_commit` `843d301d1b17af78427918f7845af336b2218de0`), so I did not rely on it as evidence for the current candidate.

Both probes used the existing `oracle/measure.py` scan API, which launches one scanner child with `RLIMIT_AS=402653184` and a 15-second timeout. Only inert JSONL was passed to the scanner; neither Python nor shell payload was executed. No corpus/full-suite run was performed.

## Residual risk and verification gaps

- Scope is only the frozen NeverReferenced shape plus one alias-call variant; other function-reference, decorator, callback, or cross-cell forms are not established by this review.
- No `lsp` device/server is mounted: requesting `xd://lsp` returned “No such tool”. Therefore no LSP status, references, definition, or diagnostics were available. Conclusions above are grounded in direct source reads and bounded scan output; no text grep is offered as semantic proof.
- No build, test suite, formatter, alternate runtime, deployment, routing, saturation, or resume/preflight path was exercised; those runtime and `resume_continuity_v1` checks are not applicable to this scanner-only case. No tools were installed or updated.

**Verdict:** Recommend retaining frozen `want: []` for the exact NeverReferenced input. No actionable defect was found in this scoped review.

Report: `.ufo/waves/round-21/w2/reports/AtkNeverReferenced.md`
