# FalsifyC141 — C1 case ThreadHygiene (critic, author-lane advisory)

**Verdict: AGREE.** The sealed expectation is semantically correct, and the delivered tool's single measured row matches it exactly. This is advisory only: it grants no admission, does not reset the r19/r20/r21 rejected-harmed streak, and is not non-author falsification.

## Identities (checked before and after; no drift)

| Item | sha256 |
|---|---|
| `tools/mado-tripwire.py` (C1) | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (matches fixed identity) |
| `tools/mado-evidence-audit.py` (C2, not exercised) | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` (matches) |
| `oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` (matches) |
| `oracle/measure.py` (runner) | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `oracle/inputs/ThreadHygiene.jsonl` | `092e4cf035fac15a160984511e28da266895f37e8fe3cca91489c8961af7d93f` (equals sealed `input_sha256`) |
| `w1/proposals/ThreadHygiene.json` | `52e5f4f13ba4ac5c107069db0a887a3936a18f50939497675d766964916fd054` (equals sealed proposal sha) |
| Runner-reported producer / population | `0270c10b…5600` / `046168571f51…86ad`; integrity before == after, `integrity_errors` empty |

## Sealed case (cases[40])

`expected_kind: exact`, `want = [package_query, "pacman -Q r22-thg", observed]`, `accept_exact_want: null`, `forbid_commands_any_tier: []`, `forbid_observed_commands: []`, `cell_count 1`, `reset false`. The sealed `want` equals the original proposal's `want` byte-for-byte; there is no correction and no addenda.

## Independent static truth (written before reading the measured row)

Payload, inert and never executed:

```python
def __mado_thread_target__():
    subprocess.run(["pacman", "-Q", "r22-thg"])
def worker():
    __mado_thread_target__()
threading.Thread(target=worker).start()
```

- `threading.Thread(target=worker).start()` creates a new non-daemon thread and runs `worker`. Interpreter shutdown joins non-daemon threads, so the call is definite, not conditional. There is no cancel, no subclass `run` override, and no race that could suppress it.
- Inside `worker`, `__mado_thread_target__` has no local binding, so it is a global load (LEGB). It resolves to the module-level `def`, which is executed and bound before the thread starts. The trailing `__` means no name mangling applies, and there is no class scope anyway.
- The target body calls `subprocess.run` with a fully literal list and the default `shell=False`, so the argv is `pacman -Q r22-thg`, classified as `package_query`. Because the argv is literal and the path is definite, the evidence tier is `observed`. A missing `pacman` binary raises only after the attempted exec, so it does not remove the attempt.
- Expected result: exactly one row, zero `eval_unparsed`/`unparsed_spawns`, and zero errors.
- Uncertainty boundaries: none apply. There is no dynamic star argument, no conditional or non-Name return, no mutation, and no callback outside the visible code. `exact` is therefore the correct kind. An `accept_exact_want`/uncertain classification would be wrong because it would let a lead or a silent miss pass. The case also has no named invented command to forbid, so the empty forbid lists are not a weakening.

## Measurement (the single authorized run)

`python3 -I .../oracle/measure.py --tool .../tools/mado-tripwire.py --case ThreadHygiene` → runner exit **0**, stderr empty, totals 1/1.

- The runner spawned one scanner child: `python3 -I -c WRAPPER tools/mado-tripwire.py oracle/inputs/ThreadHygiene.jsonl`, capped at 384 MiB / 15 s. The child exited 1, which here means unpermitted findings were present and is accepted by the runner. Child stderr was empty and there was no scanner error.
- Actual rows: `[{"class":"package_query","command":"pacman -Q r22-thg","evidence":"observed"}]`. Counts: `package_query` 1, `lead_findings` 0, `eval_unparsed` 0, `unparsed_spawns` 0. The file row's sha equals the sealed input.
- The full sorted multiset equals `want` and the unparsed total is zero, so the case passes. No other scanner runs were made.
- Raw argv, exit, stdout and stderr, plus before/after hashes, are in `.ufo/waves/round-22/w2/receipts/FalsifyC141/result.json` (sha256 `f1642b7a9929ab909cc74f33373d1943f42ca599262c0e1d24aeb764f2cdecd7`), alongside `stdout.raw`, `stderr.raw`, `exit.txt` and `hashes-{before,after}.txt`.

## Falsification attempts

| Attack | Result |
|---|---|
| False observed / lead argv | No extra rows. The single row is observed, which is the correct tier for this definite literal path. |
| Lost true command | Not lost. |
| Wrong identity (F5 shadowing) | Structurally repaired, not merely masked. The reserved literal `__mado` appears 0 times in the tool. The scheduled target is carried on the node as `ast.Name(id="<scheduled target>")` with `mado_resolved` (tool line 2480–2481). That id is not a legal identifier and is never written into `bindings`. The other synthetic id, `<captured argument>` (line 1422), is also non-identifier. Line 1888 uses the real source `stmt.name` for decorators, which is legitimate source identity. This satisfies the supported-forms F5 rule ("no synthetic metadata under ANY legal identifier"), based on reading the tool's three synthetic-name sites. |
| Duplicate sweep lead for `worker` | Prevented. Line 2733 skips refs whose parent is `threading.Thread`/`Timer`, because the start call owns the target. The measured output confirms there is no lead duplicate. |
| Lifetime / conditional target | The target identity is resolved when `Thread(...)` is constructed (`assignment_binding` 1841–1853). The scheduled state (`done`/`cancelled`) prevents double invocation. Not applicable as a defect here. |
| Parsed-clean ambiguity | Zero unparsed is correct; the case contains nothing to leave unparsed. |
| Was the case discriminating against the r21 tool? (from existing receipt, not rerun) | Yes. `evidence/first/oracle-before-new50.json` (tool `46c82902` = `evidence/tool-before.py`) recorded **no rows, unparsed 0** for this case: a silent miss rather than the lead the proposal predicted (the proposal allowed "a lead or nothing"). The r21 failure counted as a red. `oracle-after-all57.json` with the current tool `36fdc…` recorded the same passing row I measured. |

## Findings

1. **No counterexample for this case.** Impacted axes: none. No correction is needed to the tool or the expectation.
2. **Low, provenance labeling (not this case's defect):** the wrapper field `selected_tool_sha256` in `evidence/first/oracle-before-new50.json` reads `36fdc45950…` (the tree tool at commit `5c7b983`). Its `argv` and inner runner payload show that the measured tool was `evidence/tool-before.py` = `46c82902…`. A reader trusting the wrapper field could attribute the 13/50 before-result to the delivered tool. Impacted axis: calibration/provenance. Smallest safe correction: rename the wrapper field to something like `tree_tool_sha256`, or add `measured_tool_sha256` taken from the inner `tool_sha256_before`. Do not rewrite the original receipt; record the clarification alongside it. Both receipts also record audit `56091de7…` at commit `5c7b983`, which differs from the fixed C2 `277eced2…` at delivered `71228fd`. That is outside this case's scope and is only noted.

## Scope limits

- One finite variant of the F5 family passes. That closes only this tested form (a dunder-named global called from a Thread-scheduled worker, inline `.start()`). It does not cover every F5 trigger, and a green result here is not proof of complete Python semantics.
- I compared against the current target at revision `71228fd` with the tool bytes `36fdc…`. I did not rerun the original r21 tool; its red comes from the existing receipt. No installs. No production, fixture, expected-file or proposal edits.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC141.md
