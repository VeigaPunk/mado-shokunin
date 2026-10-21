# FalsifyC112: C1 case CXPartialCallableArg (single-case falsification)

Lane: MadoR22.FalsifyC112, leaf falsifier, author-lane advisory. This is not admission; L1 holds planner and integration authority.
Assignment-stated delivered revision: 71228fd582d6d9338d7916cc64e69bd4c2e928b5 (not re-verified; no git commands run).
Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC112/result.json`, with `measure.stdout` and `measure.stderr` alongside.

## 1. Verdict

**AGREE** with the sealed expectation for `CXPartialCallableArg`. The scope is this one frozen case, against tool `tools/mado-tripwire.py` sha256 `36fdc459…badce`, from one runner invocation.

- Actual: `[{"class":"host_mutation","command":"pacman -S r22-cxpcall","evidence":"observed"}]`, unparsed 0, reasons `[]`, runner `pass` 1/1, runner exit 0.
- Sealed expected: the same single row. `expected_kind` is `exact`, both forbid lists are empty, and there is no `accept_exact_want`. The runner's exact check is full multiset equality plus zero unparsed (`measure.py` 752-756).
- None of the six failure modes assigned for this case reproduced (§5).
- Green is not semantic proof. The agreement rests on my independent derivation (§3) and source trace (§4). The run covers 1 of 57 frozen cases. Nothing here grants admission.

## 2. Identities and integrity

| Item | Path (under mado-shokunin) | sha256 | Status |
|---|---|---|---|
| C1 tool (selected) | `tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` | Equals fixed C1 identity; unchanged across run |
| Runner | `.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` | Equals expected `runner_sha256`; unchanged |
| Oracle expected | `.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` | Equals fixed identity |
| Pin | `.ufo/waves/round-22/oracle/expected.sha256` | `7cc4aae9017a157faea3d66e47b5bc0181ec9093a3160d1c41d8e2e93b1567f6` | Matches expected |
| Producer | `.ufo/waves/round-22/oracle/assemble.py` | `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600` | Equals expected `producer_sha256` |
| Truth seal | `.ufo/waves/round-22/truth-seal.json` | `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` | Equals runner constant |
| Fixture | `.ufo/waves/round-22/oracle/inputs/CXPartialCallableArg.jsonl` | `13ff3d5bc56ba9f20a736973f85127a75a814a79ec14d32dc5179c580cc6d0df` | Equals case `input_sha256` |
| Sealed proposal | `.ufo/waves/round-22/w1/proposals/CXPartialCallableArg.json` | `09b7b64d9cb041831d679851c1fae38662a2ba7e109103bece7ce1691b028cf6` | Equals case `proposal.sha256` |
| C2 audit tool | `tools/mado-evidence-audit.py` | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` | Equals fixed C2 identity; not executed |
| Audit expected | `.ufo/waves/round-22/audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` | Equals fixed identity; not executed |

Runner-verified population (validation only, no scanning): 57 inputs, 52 proposal files, 106 sealed sources, population digest `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`. `integrity_before` equals `integrity_after`. Tool drift during the run: none.

## 3. Independent expectation (from the sealed text; nothing executed)

Fixture cell (one eval cell, `reset` false):

```python
import functools
import subprocess

def helper(f, argv):
    f(argv)

sink = subprocess.run
p = functools.partial(helper, sink, ["pacman", "-S", "r22-cxpcall"])
sink = print
p()
```

1. `functools.partial(...)` evaluates `sink` at construction, when it is `subprocess.run`. Host `functools.py` line 353 stores `self.args = tot_args` at construction, and line 393 calls `self.func(*pto_args, *args, **keywords)`. The stored tuple holds the function object, not the name.
2. `sink = print` rebinds only the module global. `p.args` is unchanged.
3. `p()` at module level calls `helper(subprocess.run, ["pacman","-S","r22-cxpcall"])`, and `f(argv)` executes `subprocess.run(["pacman","-S","r22-cxpcall"])`. This is an eager, definite spawn with no shell.
4. Class: `pacman -S` with no `-y/-u/-w/-c` and no query flags is a sync/install, so `host_mutation`. The command text is the argv joined by spaces: `pacman -S r22-cxpcall`.

Expected rows: exactly one `(host_mutation, "pacman -S r22-cxpcall", observed)`, zero unparsed, no lead, no forbidden command. This matches `want` and `want_input_order` in expected.json (proposal copy at lines 604-610; top level at 618-631).

Uncertainty boundary: none in the sealed truth. The case is `exact`, forbid lists are empty, and there is no `accept_exact_want`. Environment variation (pacman absent, or non-root giving a nonzero exit) happens after the spawn attempt, so class, command and evidence do not change. The rationale's phrase "no exception" depends on the environment but does not change the rows. A lead-tier row or a zero-row "clean" result would be wrong for this case. No uncertain outcome is admissible here.

Note: `require_signal: true` is validated by the runner (`measure.py` 248-250, 330-332, 387), but `evaluate()` reads it only in the uncertain branch (765). For this exact case it is inert.

## 4. Tool path that produced the row (source trace on 36fdc459; reading, not a runtime trace)

1. `sink = subprocess.run` goes through `update_bindings` (1928-1937), `assignment_binding` (1838), the `callable_info` Attribute branch (1784-1817), and `spawn_path`. Result: `bindings["sink"] = {kind: spawn, name: subprocess.run}`.
2. `p = functools.partial(helper, sink, [...])` goes through `assignment_binding` Call branch (1839-1874) and `callable_info` Call branch (1761-1769). `functools.partial` is pure via the `functools.` prefix (1586-1596). The wrapped `helper` has kind helper. `captured_node(sink)` (1417-1425) stores the live callable dict in `mado_resolved` and the literal list in `mado_literal`. Each fixed argument is frozen at construction.
3. `sink = print` goes through `update_bindings` (1935), which assigns a new `dict(resolved)` to `bindings["sink"]`. The captured dict is not mutated, so the frozen identity survives.
4. `p()`: `callable_info(Name p)` returns the helper with `fixed_nodes`. The `spawn_scan` helper branch (2547-2568) builds `bound_node` with the fixed arguments. `bind_literal` (2089-2160) yields `{f: LITERAL_MISS, argv: [...]}`.
5. `follow_helper` (2407-2439) runs `bound_callables` (1608-1626). `f` takes `assignment_binding(frozen)`, which is spawn (1822-1823). `argv` becomes parameter kind, while its literal value flows through the environment.
6. Nested `spawn_scan` on `f(argv)`: `callable_info(Name f)` is spawn, and `is_sub` holds (2623-2630). `call_args = [literal list]` (2635-2643), then `argv_strings` (2676), then `classify_shell("pacman -S r22-cxpcall")`. `classify_segment` sets `text = " ".join(seg)` with empty suffix, since tokenization succeeds (1131-1136). `classify_pacman` gives `("host_mutation", "pacman:-S")` (775-780).
7. Evidence: a 4-tuple hit with no explicit lead marker takes the default `observed` in `scan_file` (2876-2885). None of the lead-tagging sites (`+("lead",)` at 2302, 2317, 2333, 2385, 2544, 2574, 2618) is reached for this cell.
8. Reference sweeps (2685-2751): the eager refs are `helper` and `sink`, both with parent `functools.partial` (pure), so they are skipped (2698-2700, 2721-2728). The name `argv` inside `f(argv)` is a parameter and causes no action. The `sink = subprocess.run` attribute has no parent entry, so it yields no ref. `unparsed` stays 0. `classify_eval` compiles the cell (2280-2285), so no `eval_unparsed`.

The trace predicts one observed row with unparsed 0. The run matches.

## 5. Falsification attempts (this case only)

| Failure mode | Attack | Evidence | Result |
|---|---|---|---|
| False observed / lead argv | Drop the callable freeze so `f` becomes a parameter. `f(argv)` then goes to `helper_argv_leads` (2606-2609, 2296-2304) and emits a lead. | One observed row, no lead | Not reproduced |
| Lost true command | Re-resolve `sink` at `p()`. It is `print` (pure), so no spawn row. | Row present | Not reproduced |
| Wrong identity | Borrow a command from a same-named module literal, or from `print`. | The only command source is the partial's argv list. No module literal named `f`, `argv` or `sink`. | Not reproduced |
| Lifetime | Call-time freeze of the literal and the callable. | The row needs the construction-time identity, because `sink = print` precedes `p()` | Not reproduced |
| Conditional target | Branch or loop around the partial. | None in the cell; straight-line statements only | Not applicable |
| Parsed-clean ambiguity | Zero rows with zero unparsed would look clean. | Want is non-empty, so the exact check fails. Observed: 1 row, unparsed 0, `eval_unparsed` 0, `unparsed_spawns` 0. | Not reproduced |
| Extra rows | Any extra lead or observed row fails the exact multiset. | Exactly one row | Not reproduced |
| Forbid tiers | Forbidden argv at any tier. | This case declares no forbid lists, so it cannot test this (see §7). | Scope gap, not a failure |
| accept_exact_want | Lead-only output accepted as uncertainty. | Exact kind: a lead-only output fails here. | Not applicable; a lead would fail |

## 6. Predicted sensitivity (source reading; not executed; no fault claimed killed)

- P1: `captured_node` keeps the literal but sets the callable to `{"kind": "unresolved"}`. Predicted: `f` becomes a parameter, `helper_argv_leads` emits `pacman -S r22-cxpcall` at lead tier, and the exact check fails on evidence.
- P2: the fixed callable keeps its source name and is re-resolved against bindings at `p()`. Predicted: `sink` resolves to `print` (pure), no row is emitted, and the exact check fails on a missing observed row.

L1 runs any mutant. Until then these are predictions only.

## 7. Scope against the current C1 target

- Ran: 1 of 57 frozen cases, 1 scanner child, against tool `36fdc459`.
- Validated, not scanned: all 57 inputs, 52 proposals and 106 sealed sources.
- Not covered: the other 56 cases; the no-harm guards (oracle 35+17, the 175-case historical suite, the 1356-fixture removal comparison, the resource population); the C2 audit; and variants of callable-fixed partials (reordered rebinding, aliasing, keyword `f=`, nested partials, partials of Thread or Timer).
- Per the sealed rationale, this case is the only guard for callable-fixed partial arguments in the frozen corpus. I did not verify that claim.
- Forbid-tier gap: this case declares no forbid lists.

## 8. Residual uncertainty and non-scoring notes

- The §4 trace is source reading, not a runtime trace. The single run is consistent with it.
- expected.json's `source` text cites pre-r22 tool (`46c82902`) lines 1635-1638, 2252-2257 and 2384-2388. The same mechanisms now sit at 1417-1425, 1761-1769, 2557-2568 and 2407-2439. This is citation drift only; `source` is not a measured field.
- `findings[].timestamp` is the string `"None"` when the JSONL record has no timestamp (tool line 2890). Cosmetic; not measured here.
- `classify_shell` appends `/unparsed` to the rule when tokenization fails (1090-1096, 1132), but evidence still defaults to `observed` (2880). `classify_shell` itself increments no unparsed counter (1083-1122). This path is not exercised by this eval case. Flagged for L1 to check against the header contract; I did not establish the intended behavior.
- Old-tool red receipts: `evidence/first/oracle-before-new50.json` (tool `evidence/tool-before.py`) records this row as `lead`. I did not run that tool. I saw the row only through a grep quote.

## 9. Constraints observed and commands run

- Read-only on tools, fixtures, expected files and sources. Writes: this report and the receipt directory only.
- Exactly one scanner-bearing run: `python3 -I …/oracle/measure.py --tool …/tools/mado-tripwire.py --case CXPartialCallableArg`, cwd mado-shokunin, exit 0, stdout and stderr redirected into the receipt directory. One child, under the runner's 384 MiB RLIMIT_AS and 15 s timeout (`measure.py` 26-27, 643-661). I did not independently check the rlimit inside the child.
- No whole-corpus run; no old tool; no probes; no mutants; no installs. `jq` is present but unused, and package transactions stay paused.
- Non-scanner commands: sha256sum, stat, cat, ls, `mkdir -p`, `command -v`, `python3 --version` (3.14.8), and a read of host `/usr/lib/python3.14/functools.py` lines 339-403.

Checks for L1 (not run by me): the whole-population measure under the same caps, one child at a time; the P1 and P2 mutants in a private sandbox; and the C2 audit run separately.

Report: .ufo/waves/round-22/w2/reports/FalsifyC112.md
