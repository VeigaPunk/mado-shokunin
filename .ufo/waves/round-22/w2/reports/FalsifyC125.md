# FalsifyC125 — CaptureMissingRequired

## Findings by severity and verdict

**No actionable severity-ranked defect established for the assigned exact case. Verdict: agree.** The complete expected and actual class/command/evidence multisets are both `[]`, with zero scanner error/unparsed counters. This recommendation is restricted to `CaptureMissingRequired` against delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, selected C1 SHA-256 `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`.

This is an author-lane advisory falsification result, **not non-author admission**, global C1 acceptance, C2 evidence, or permission to reset the r19/r20/r21 rejected-harmed receipts or streak.

## Axes

1. Complete class/command/evidence multiset correctness, including false observed and false lead commands.
2. Lexical callable identity, factory reachability, and captured-binding lifetime.
3. Honest exact-versus-uncertain classification and the meaning of parsed-clean output.
4. Fixed artifact identity, reproducibility, and the authorized one-child resource bound.

## Independent expected semantics

The assigned inert source is the single eval cell in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureMissingRequired.jsonl:1`:

```python
import subprocess


def make(argv):
    def run():
        subprocess.run(argv)
    return run


argv = ["pacman", "-S", "r22-missing-required"]
runner = make()
runner()
```

The original proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureMissingRequired.json`; its sealed counterpart is the `CaptureMissingRequired` record of `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json`. Both specify `expected_kind: exact`, `want: []`, and forbid observed `pacman -S r22-missing-required`. The normalized record has no correction/addendum, `accept_exact_want: null`, `require_signal: false`, and `forbid_commands_any_tier: []`.

The semantic derivation is independent of the measured green result:

- `make` has one required positional parameter and no default. `make()` supplies no positional, keyword, or expanded argument. Argument binding therefore fails with TypeError before entering the factory body. No exception handler exists in this cell. Successful assignment to `runner` never happens, and its following invocation is unreachable.
- Defining `make` does not execute its body. Consequently the nested `run` function is not even constructed by the failing call, let alone invoked. The only `subprocess.run` expression is inside that unreachable body.
- The module variable `argv` cannot fill a missing parameter. Formal parameters bind local names; the nested body's `argv` belongs to the enclosing function scope, not the same-spelled module binding. There is no reachable process invocation and no true command to recover.
- The complete truth is therefore **no class/command/evidence rows at either evidence tier**, not a host-mutation row and not a lead. This is a definitely invalid visible call, not an unresolved `make(*parts)` call. Requiring lead/unparsed uncertainty would misdescribe the source.

The proposal's cited source snapshots were read, not executed: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-compound_stmts.rst:1247-1254,1297-1303,1326-1336` establishes definition-versus-body execution and parameter assignment; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst:59-61,89-115` establishes formal-parameter binding and nearest-enclosing scope resolution. The TypeError/reachability conclusion above is static reasoning, not an observed payload exception.

An empty explicit any-tier forbid list does **not** allow an invented lead here: the exact comparison requires equality of the entire sorted multiset and zero unparsed counters. Any extra lead or observed row fails. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:732-756` implements that contract. Its separate uncertain-case `accept_exact_want` branch at lines 758-778 is not applicable to this case; it is not an excuse to turn definite failure into uncertainty.

## Delivered behavior and relevant diff

The actual classifier diff from base `741122d177ae8ff68a73768777f20484d5bdcbe4` to delivered `71228fd582d6d9338d7916cc64e69bd4c2e928b5` was read for `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`. The relevant change removes the old delayed `capture_owner`/`capture_call` fallback, adds explicit invalid-versus-uncertain binding treatment, and carries the resulting callable state through assignment and invocation. The case-specific source path is:

1. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2148-2154`: `bind_literal` returns `None` for the unsupplied required `argv`.
2. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1629-1639,1652-1656`: there is no unknown star/double-star expansion, so this failure is `invalid`; `factory_result` returns that state before building a captured lexical environment.
3. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1757-1783,1859-1861,1928-1936`: factory resolution and the stored result preserve `invalid`, rather than replacing it with a visible nested helper or borrowing module `argv`.
4. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2051-2058`: eager-call collection does not descend through the function body merely because its definition is present.
5. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2564-2567`: the direct invalid `make()` helper call is skipped before fallback body sweeping. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2461-2466` skips the later scanner-side invalid result as well. This explains the observed absence of both observed and lead findings without treating absence alone as semantics proof.

The prior red authority remains `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:53-56,78-83`: F2 falsely borrowed a module global when factory binding failed, with missing required parameters named among the triggers. Its original measured repro used unresolved expanded arguments. This assigned case is the narrower **decidable missing-required** variant, not a rerun or replacement of that original uncertain repro. No old tool was executed.

## Authorized measurement and raw rows

Exactly one measurement command was executed:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureMissingRequired
```

The runner's canonical path validates the full frozen population before selecting one exact case (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:797-810`), invokes only that selected scanner child (lines 829-839), and checks integrity afterward (lines 854-861). The receipt reports validation of 57 input files, 52 proposal files, and 106 sealed sources **before and after**, but measurement totals are **1/1**, not 57/57. The scanner child is sequential, isolated with `-I`, capped at 402653184 bytes RLIMIT_AS and 15 seconds by lines 643-661. No alternate detector/runtime or source-shaped probe was run.

| Observation | Actual value |
|---|---|
| Outer runner exit / stderr | `0` / empty |
| Runner status / selected total | `complete` / `1` |
| Case / pass / reasons | `CaptureMissingRequired` / `true` / `[]` |
| Complete expected rows | `[]` |
| Complete actual rows / raw findings | `[]` / `[]` |
| Scanner exit / stderr / scanner error | `0` / empty / `null` |
| Scanner first stdout line | `MADO_TRIPWIRE: clean` |
| Observed / lead findings | `0` / `0` |
| eval calls / bash calls / JSONL lines | `1` / `0` / `1` |
| eval_unparsed / unparsed_spawns | `0` / `0` |
| All five class counts / unpermitted | all `0` / `0` |
| Fixture path and digest | exact selected absolute path and sealed SHA-256 below |
| Integrity errors / selected-tool drift | `[]` / none |

The raw outer argv, exit, stdout, stderr, parsed runner output, nested scanner argv/exit/stdout/stderr, limits, and before/after hashes are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC125/result.json`. The seat's recorded actual outer argv includes `-I`; the runner's reconstructed top-level `argv` uses `sys.argv` and does not itself preserve that interpreter flag. The nested scanner argv independently includes `-I` and names the selected tool and fixture exactly.

### Identity evidence

Independent `sha256sum` checks before and after the measurement returned identical values:

| Artifact | SHA-256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureMissingRequired.jsonl` | `6ecf3c905c064ba12e99746edba16d6701aca41d7e8e94233386a2b8486a0d78` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureMissingRequired.json` | `b81897471a24495a3bc19d2e0bdffda7bc67acb4ba6a22ceb3e339fd1253339b` |

The runner additionally reported unchanged population SHA-256 `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` and raw-truth-seal SHA-256 `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4`.

## Falsification coverage, residual risk, and verification gaps

- **False observed/lead argv:** none; the entire returned finding population is empty. Neither tier may legitimately name the module literal for this failed call.
- **Lost true command:** none for this source. There is no reachable spawn to lose; this negative case does not measure positive recall.
- **Wrong callable identity or lifetime:** no closure is formed by successful source execution. The candidate's invalid-state path prevents lending the module binding to a fictitious returned helper. This is not a test of multiple live closure instances, later mutation, or cross-cell persistence.
- **Conditional/scheduled target:** the fixture contains no conditional, scheduler, Thread/Timer, or cancellation. No conclusion about those forms follows from this pass.
- **Parsed-clean ambiguity:** zero parsing/uncertainty counters are appropriate to this decidable negative. `clean` means no classified activity in this scan; it does **not** mean the Python cell successfully completes, would be safe to execute, or is cleared for host operations. The payload was never executed.
- **LSP gap:** `read xd://lsp` returned `No such tool`; no LSP device/server is mounted, so status/references/definition/diagnostics were unavailable. Definition/caller review used the literal delivered diff and cited source ranges. Text search is not represented as semantic LSP proof.
- **Broader target gap:** this one case does not establish all eligible C1 expectations, resolution of all original reds, historical recall/no-harm, corpus additions/removals/error handling, resource-population saturation, structural F5 namespace hygiene, or C2 independence. No new closure/scheduler or uncertainty case was run. Resume/rerouting/admission control paths are not exercised by this assignment.
- **Execution and write scope:** one authorized scanner measurement only; no fixture Python or printed command execution, old-tool reruns, builds, linters, formatters, full suite/oracle runs, installs/updates, background jobs, delegation, live probes, or production/fixture/proposal/registry/docs edits. Writes are restricted to this assigned report and its own raw receipt.

**Recommendation:** retain `agree` for `CaptureMissingRequired` only. No admission is granted, and the pre-existing red receipts and rejection streak remain intact.
