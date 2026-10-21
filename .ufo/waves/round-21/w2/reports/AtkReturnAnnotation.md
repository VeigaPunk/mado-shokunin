# ReturnAnnotation review

## Findings (by severity)

### Conditional Medium — possible missed eager return-annotation calls on Python ≤3.13

**Recommendation:** Treat this only as a conditional compatibility risk for Python versions through 3.13, when annotations are eagerly evaluated by default and no postponed-annotations future import applies. The frozen expected empty set is correct. The nearby variant is not a counterexample under Python 3.14.8's default PEP 649 semantics because the transcript does not access its annotation. Forced annotation evaluation is distinct and untested here.

Through Python 3.13, without postponed annotations, defining `g() -> f` evaluates `f` to the function object; it does not call `f`. Neither function is invoked, so no process finding is warranted. In Python 3.14.8's default lazy-annotation mode, the expression is not evaluated at function definition, and this transcript does not request it; again no process finding is warranted. The frozen expected row has `want: []` (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json:593-603`; proposal rationale: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/ReturnAnnotation.json:4-7`).

The implementation uses a structural rule, not a fixture-string special case: `eager_calls` visits a `FunctionDef`'s decorators and defaults but omits its return annotation (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1860-1867`); `prepare_eval_calls` applies that walk to each module statement (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1979-1980`). This suppresses the bare-name false lead generally, but it drops every call expression in a return annotation too. The inspected diff from baseline `2ac0f9ba69051aea22cab3b6cfebe4d906b72d17` to candidate `f499a8db7171b7476fe9f204ab9edbac5a956fa9` contains no case-name or fixture-text match and does not change this `FunctionDef` child-selection rule; the generic exclusion is current behavior, not a newly introduced ReturnAnnotation-specific branch.

I retained one inert nearby variant at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkReturnAnnotation/return-annotation-eager-call.jsonl` (SHA-256 `c938ea065180e8227d0c3f8104e963b5d1aa24736f5755a7a1c7ca95f66bf8b7`). It changes only `g`'s annotation from `f` to `subprocess.run(["pacman", "-Q", "hyprland"])`; the `f` body remains deferred. Through Python 3.13 without postponed annotations, this call runs while defining `g`, so a `package_query` for command `pacman -Q hyprland` with `evidence: observed` is warranted (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:737-780,2570-2588`). Under Python 3.14.8 by default, annotations are lazy and this transcript does not access them, so the call does not run and the scanner's clean output is not a false negative. I did not test or claim handling of forced annotation evaluation.

**Bounded scanner-only observations** (using the existing `measure.py` `scan` API; each call used its one RLIMIT_AS-384-MiB, 15-second child; neither transcript's Python payload was executed):

- Frozen input SHA-256 `f274cac86d87a3148eb0bec758d75d44e74c4fa9f148b35c80852fc777f37948`: `exit=0`, `eval_calls=1`, `eval_unparsed=0`, `unparsed_spawns=0`, `findings=[]`.
- Variant SHA-256 `c938ea065180e8227d0c3f8104e963b5d1aa24736f5755a7a1c7ca95f66bf8b7`: `exit=0`, `eval_calls=1`, `eval_unparsed=0`, `unparsed_spawns=0`, `findings=[]` (all class counts zero). This confirms the scanner output only; on Python 3.14.8 with no annotation access, it matches runtime semantics.

## Residual risk

This is a potential false negative only for eager annotation semantics (Python through 3.13, absent postponed annotations). The project/transcript Python target version is not established here. Python 3.14 forced annotation access and other annotation expressions are outside this check; no broader claim is made. No frozen expectation was changed.

## Verification gaps

- Tested scanner SHA-256: `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`. The announced candidate commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9` resolves to the same scanner bytes; checked-out HEAD was `a8da015624c92f4cb4a7de92adbf6643a3f8b38a` with the same tool hash. The bounded scan output did not record the Python runtime version.
- LSP was unavailable: the initial `read xd://lsp` status request returned `No such tool` and the mounted-device inventory had no LSP device. Findings above are supported by direct source lines and the bounded scan, not by LSP references/definition/diagnostics.
- Official Python 3.14.8 docs state annotations are “lazily evaluated by default” and “not evaluated when the code containing the annotation is evaluated”: https://docs.python.org/3.14/reference/compound_stmts.html#annotations. This invalidates the earlier unqualified eager-evaluation premise for 3.14.8.
- No full corpus/suite was run; only the frozen case and the single retained variant were scanned. No tools were installed.

**Verdict (advisory):** The frozen empty expectation is correct. The generic annotation omission is a conditional concern only for eager annotation runtimes through Python 3.13; the retained variant is clean by default in Python 3.14.8, and forced annotation behavior remains unclaimed.

Report: .ufo/waves/round-21/w2/reports/AtkReturnAnnotation.md
