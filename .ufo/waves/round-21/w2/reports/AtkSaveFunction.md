# SaveFunction — C1 adversarial review

Axes: semantic warrant of the frozen expectation; whether the repair is AST/semantics-based rather than fixture-text keyed; nearby-variant behavior; evidence and verification completeness.

## Findings (severity ordered)

### High — chained callable assignment loses a reached function body

A nearby chained-assignment form produces a concrete false negative. In the inert variant below, `alias = saved = f` binds both names to the same function object; the following `saved()` invokes `f`, whose body calls `subprocess.run(["pacman", "-Q", "hyprland"])`. The current scanner returns no finding where a reached call should be reported as `package_query`, command `pacman -Q hyprland`, evidence `observed`.

The relevant implementation is structural, but only preserves the callable for a single assigned name: `assignment_binding` resolves an assigned `Name` from its current binding (`tools/mado-tripwire.py:1661-1673`), while `update_bindings` replaces each target with `{"kind": "unknown"}` whenever the assignment binds more than one distinct name (`:1717-1756`). `callable_info` consequently resolves `saved` as unknown (`:1593-1602`); the unknown-call path in `spawn_scan` does not follow this function body (`:2293-2303`). This explains the missed reached call and identifies a generality gap, not a fixture-text match. Preserve the resolved callable binding for each name bound by a chained assignment, then exercise the variant in the owning verification.

## Frozen expectation

The frozen record is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json:605-613`: case `SaveFunction`, fixture SHA-256 `55d54aff5abe5deac6c38232ec357b13f40dadddeb5812ac95c7b0792d12a124`, proposal SHA-256 `e1439eef5ca080d6fd3803c254c9d46422077952276b56e5254d00a938c75bbd`, and `want: []`. The proposal file's SHA-256 matches that registered proposal digest.

The empty expectation is semantically warranted for the exact input in `w1/oracles/SaveFunction.json:4-6`: `def f()` defines a function without running its body; `saved = f` only binds that function object and neither calls it nor passes it to an invoking sink. Thus the body containing `subprocess.run` is deferred and there is no command/evidence tuple for this exact input. Keep the frozen `want: []` unchanged.

The existing candidate receipt records this case passing with no findings, but its `measured_commit` is `843d301d1b17af78427918f7845af336b2218de0`; it is historical support, not a fresh result for the current candidate.

## Candidate generality and one nearby variant

The current candidate is commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`; the actual `tools/mado-tripwire.py` bytes have SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d` (the file was unchanged in the working tree). The exact pure-binding negative is handled by AST context: `eager_calls` records calls and values passed to calls, and only gives value references a parent when they are passed as arguments (`:1813-1893`); a bare `saved = f` is not an invocation. This supports that the negative behavior is not keyed to `saved`, `f`, or the fixture's command text. However, the reached-callable behavior is not general across the chained-name variant above because the binding pass discards callable identity for multiple target names.

I retained one nearby variant and a baseline control as inert JSONL under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkSaveFunction-2/`. The variant is `chained-assignment-invoked.jsonl` (SHA-256 `76a60d412eca9370c5e21154f2c93b0b00ad95258680c7bc322bf44d88fe49e8`) and contains:

```python
import subprocess

def f():
    subprocess.run(["pacman", "-Q", "hyprland"])

alias = saved = f
saved()
```

The adjacent `baseline.jsonl` contains the exact frozen code and is only a control (SHA-256 `f2028c3147ad5c2cc8b2807e240210d6fbebe66225fc1db502d174b5ed738aeb`). I called the existing `measure.py` `scan` API once on that fixture directory; it launched one bounded scanner child with `RLIMIT_AS=402653184` and a 15-second timeout. Observed output: outer exit `0`, payload exit `0`, `findings: []`, `lead_findings: 0`, `observed_findings: 0`, `counts.package_query: 0`; both files had `eval_unparsed: 0` and `unparsed_spawns: 0`, and stderr was empty. The baseline stayed clean, while the chained-assignment variant was missed. Scanner parsing only; neither Python nor shell payload was executed.

## Residual risk and verification gaps

- This falsifies callable preservation for one nearby chained-assignment form only; it is not a global claim about other alias forms. No whole corpus or suite was run; L1 owns final verification.
- No LSP device/server is mounted (`xd://lsp` returned `No such tool`), so LSP status, references, definition, and diagnostics were unavailable. Direct source reads support the source-path explanation; text search was only used to locate code, not as semantic proof.
- Tools installed or updated: none.

**Verdict:** Recommend retaining the frozen empty expectation for the exact `saved = f` input, but do not treat reached-callable preservation as general until chained assignments retain their callable binding and the scoped variant is rechecked by L1.

Report: .ufo/waves/round-21/w2/reports/AtkSaveFunction.md
