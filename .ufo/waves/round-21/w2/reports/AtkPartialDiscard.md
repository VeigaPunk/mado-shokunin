# PartialDiscard — scoped C1 falsification

## Axes and verdict

- **Semantic fidelity:** the frozen `want: []` is correct for the exact frozen input.
- **Generalization:** the candidate uses AST/callable-shape logic rather than a `PartialDiscard` case-ID rule for the clean result, but it does not preserve a returned `functools.partial` through a helper-call result.
- **Challenge result:** **High-severity false negative** on the one-token-nearby live-call shape below. The current candidate does not fully handle this family; this finding is scoped to partials returned from a reached helper, not to the whole scanner.

## Identity and bounded checks

- Candidate commit observed: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Tested candidate: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.
- Frozen input: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/inputs/PartialDiscard.jsonl`, SHA-256 `6fb4083d2f0736906f032bd9471fdc87981daee3879d7f1fc1c8e89b880b65be`; frozen expected row in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/expected.json` has `want: []` and cites proposal `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/PartialDiscard.json`.
- Ran only the scanner via the existing `measure.py` `scan` API against the frozen input and my inert variant. Each scan used one scanner child with the API's 384 MiB `RLIMIT_AS` and 15-second timeout. The tool reads JSONL and parses eval code to an AST (`scan_file`, lines 2502–2567; `classify_eval`, lines 2028–2040); **neither fixture's Python payload was executed**. No tools were installed.

## Frozen expectation is semantically warranted

The frozen code defines `f`, whose body contains `subprocess.run(["pacman", "-Q", "r21"])`, but does not call `f`. Both occurrences of `functools.partial(f)` only construct partial objects: the one in `C.defer` is inside an uncalled method, and the module-level one is discarded without invocation. `C()` has no user-defined `__init__`, `__new__`, or `__del__`; it does not invoke `defer`. Thus the command expression is not reached in the frozen transcript, and no class/command/evidence finding is warranted. The candidate's exact frozen-input scan returned exit 0, zero findings, zero `eval_unparsed`, and zero `unparsed_spawns`, matching the frozen empty multiset.

If reached, `pacman -Q r21` maps to `package_query` / rule `pacman:-Q` in `classify_pacman` (`tools/mado-tripwire.py:737-780`). That mapping does not make the uncalled lexical body an observed command.

## Generality and source path

The clean result follows structural rules, not a visible case-name or command-text exemption in the inspected path: `eager_calls` distinguishes calls from references (`tools/mado-tripwire.py:1813-1893`); `spawn_scan` limits class construction to actual constructor/finalizer hooks (`tools/mado-tripwire.py:2276-2292`); and the value-reference pass explicitly treats a partial construction as non-invoking (`tools/mado-tripwire.py:2386-2394`). Callable resolution recognizes `functools.partial` and carries fixed arguments for a directly invoked wrapped helper (`tools/mado-tripwire.py:1577-1622`, `2321-2369`), while `assignment_binding` also preserves a partial wrapping a recognized spawn callable (`tools/mado-tripwire.py:1661-1714`). This is mechanism-based handling of the frozen shape, not a special case for its literal `pacman` text.

That generality stops at a helper's returned callable. `callable_info` handles a call returning a nested local function only when it finds a top-level `return <Name>` for that local function (`tools/mado-tripwire.py:1603-1622`); it does not resolve `return functools.partial(f)`. When the outer call target remains unresolved, `spawn_scan` only emits generic leads for name calls or recognized spawn-named attribute calls, then continues (`tools/mado-tripwire.py:2293-2302`).

## One nearby counterexample (retained inert input and observed scanner output)

The retained JSONL fixture is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkPartialDiscard-2/partial-discard-invoked.jsonl`, SHA-256 `53991fba3ec8c94307f1139259e56965867cdb8ae3b9d523771e822ec3667707`. It preserves the frozen helper/class/partial shape and changes the end to `C().defer()()`.

**Observed candidate output:** exit 0; all class counts zero; `findings: []`; `lead_findings: 0`; `observed_findings: 0`; `eval_unparsed: 0`; `unparsed_spawns: 0`; stderr empty. This is a clean result, not a parser error or timeout.

**[INFERENCE] Expected semantic result if the transcript code were executed:** `C().defer()` returns `functools.partial(f)`, and the outer `()` invokes that partial, entering `f` and reaching `subprocess.run`. The appropriate scanner row is therefore `class=package_query`, `rule=pacman:-Q`, `argv0=pacman`, `command=pacman -Q r21`, `evidence=observed`. I did not execute this Python or shell payload; the inference follows from the shown Python call/return shape and the candidate's pacman classifier. The miss is specifically that the called method's return value is not propagated to the outer invocation.

## Verification gaps and residual risk

No LSP device/server route is mounted in this session, so LSP status, references, definitions, and diagnostics could not be obtained. No text-grep output is used as semantic proof. This is one bounded counterexample, not an exhaustive proof over returned callables or the entire scanner. No full corpus or suite was run, per assignment.

Report: `.ufo/waves/round-21/w2/reports/AtkPartialDiscard.md`
