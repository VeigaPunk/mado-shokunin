# FalsifyC120: C1 case CaptureKeyword (round-22 recovery, delivered 71228fd582d6d9338d7916cc64e69bd4c2e928b5)

Seat: MadoR22.FalsifyC120 (leaf member, outside-lane falsification, advisory only).
Attack item: sealed C1 exact expectation `CaptureKeyword` against `tools/mado-tripwire.py`.

## Verdict: AGREE

- The sealed exact expectation for CaptureKeyword is semantically correct under CPython static semantics. Uncertainty is not warranted.
- The one measured run reproduces it row for row: one observed `host_mutation` row, `pacman -S r22-kw-factory`. Zero leads, zero unparsed, zero parse errors. Runner `pass` 1/1.
- No falsifying evidence was found for this case in the six attack classes (section 4).
- Two adjacent risks are reported in sections 7 and 8. Both are unmeasured inference or harness observations, not verdicts on CaptureKeyword.
- No admission is granted. Per registration.md, outside-lane falsification is required evidence, but this report is advisory. Main/L1 own closure and streak disposition.

## 1. Scope and what was executed

Read only: the sealed case entry in `oracle/expected.json`; the original proposal `w1/proposals/CaptureKeyword.json`; the fixture `oracle/inputs/CaptureKeyword.jsonl`; the cited CPython lines; the runner's scan, evaluate and main paths; and the tool code paths for keyword binding, closure overlay and mutation tracking.

Executed exactly one command:

    python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureKeyword

- Runner exit 0 (`status: complete`, `totals: 1/1`). Full-population validation ran before and after the case (57 inputs, 52 proposals, 106 sealed sources; `integrity_errors: []`).
- One scanner child, exit 1 (unpermitted findings, expected for a host_mutation). It ran under RLIMIT_AS 384 MiB and a 15 s timeout, spawned by the runner's `scan()`.
- No other scanner run. No whole-corpus rerun. No old tool. No fixture or printed-command execution. No installs (none needed).

Identities, sha256, identical before and after the run (`hashes-before.txt` vs `hashes-after.txt`):

| identity | sha256 |
|---|---|
| tools/mado-tripwire.py (C1 tool) | 36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce (fixed identity) |
| oracle/measure.py (runner) | 41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7 |
| oracle/expected.json | b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357 (fixed identity) |
| oracle/expected.sha256 | 7cc4aae9017a157faea3d66e47b5bc0181ec9093a3160d1c41d8e2e93b1567f6 |
| oracle/assemble.py | 0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600 |
| oracle/inputs/CaptureKeyword.jsonl | 913d8d340e7966045fb3c702bfbd9c0ce9d1f15ed6fcfb51b4b249ab9f6f13c6 |
| w1/proposals/CaptureKeyword.json | 1fa6dd2819cff700d3f23517d92cf362312a8c5d79a607a38ad82f22165502b5 |
| .ufo/waves/round-22/truth-seal.json | 47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4 |
| population_sha256 (runner-reported) | 046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad |
| tools/mado-evidence-audit.py (C2, hash only, not run or read) | 277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca |

Raw receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC120/result.json`. It holds argv, exit codes, the runner stdout verbatim, empty stderr, and all identity hashes. The same directory holds `measure.stdout.txt`, `measure.stderr.txt` (empty), and the before and after hash files.

## 2. Sealed expectation, reasoned independently (no execution)

Program text (inert input):

```python
import subprocess
def make(argv):
    def run():
        subprocess.run(argv)
    return run
cmd = ["pacman", "-S", "r22-kw-factory"]
runner = make(argv=cmd)
cmd = ["pacman", "-Q", "r22-kw-invoke"]
runner()
```

1. `make`'s body runs only when it is called. `run` closes over the parameter `argv`.
2. The keyword call `make(argv=cmd)` binds the parameter to list object L1 = `["pacman","-S","r22-kw-factory"]` at call time.
3. `cmd = [...-Q...]` rebinds the module global to a new list L2. It neither mutates L1 nor reaches make's frame.
4. `runner()` executes `subprocess.run(L1)`: one spawn, `pacman -S r22-kw-factory`.

Sealed expectation (proposal and expected.json agree): `kind: exact`; want = [host_mutation, `pacman -S r22-kw-factory`, observed]; `forbid_observed_commands` = [`pacman -Q r22-kw-invoke`]; `forbid_commands_any_tier` = []; `accept_exact_want` = null; `require_signal` = true (inert for exact, section 8); `cell_count` = 1.

I agree with every element: one row, zero leads, zero unparsed, zero parse errors.

Uncertainty boundary: none is warranted. The spawn site is unconditional at module level, every argument is a literal, and the only later event is a rebinding, not an in-place mutation of L1. The case therefore sits in the exact class of supported-forms (stored and immediately invoked factory results, keyword arguments). For this program, a lead-only or unparsed result would be a false negative under this oracle.

Citation check: compound_stmts lines 1326–1328 contain the quoted "A function call always assigns values to all parameters..." sentence (verified). executionmodel lines 113–114 contain "resolved using the nearest enclosing scope" (within the cited range 89–115). simple_stmts lines 83–84 contain "(re)bind names to values" (within 72–108). The conclusion that the closure cell holds the creation-time value is an inference from call-time parameter binding, not a verbatim quote [INFERENCE]. It matches CPython semantics.

## 3. Actual rows (single run)

Scanner child: argv `/usr/bin/python3 -I -c <WRAPPER> …/tools/mado-tripwire.py …/oracle/inputs/CaptureKeyword.jsonl`. Exit 1. Stderr empty. Stdout line 1 is `MADO_TRIPWIRE: findings`; line 2 is the JSON payload.

| field | actual |
|---|---|
| findings | 1 row: class `host_mutation`, command `pacman -S r22-kw-factory`, evidence `observed`, line 1, rule `pacman:-S`, tool `eval`, tool_call_id `CaptureKeyword-0`, timestamp `"None"` |
| counts | host_mutation 1; live_probe, package_query, tool_install, vcs_write 0 |
| observed_findings / lead_findings | 1 / 0 |
| unpermitted / permitted | 1 / [] |
| files[0] | lines 1, eval_calls 1, bash_calls 0, eval_unparsed 0, unparsed_spawns 0, sha256 equal to the sealed input digest |
| runner comparison | got_rows equals want (sorted class/command/evidence multiset); unparsed 0; reasons []; pass true |

Internal consistency, checked by hand: one observed plus zero leads equals one finding; counts agree; unpermitted 1 gives exit 1.

## 4. Falsification attempts (CaptureKeyword only)

| attack | outcome |
|---|---|
| false observed/lead argv | Not reproduced. The row's argv is the creation-time literal. No lead, no extra row. |
| lost true command | Not reproduced. The row is present. |
| wrong identity (late `-Q`, or a same-name global) | Not reproduced. `pacman -Q r22-kw-invoke` is absent and `forbid_observed` passes. |
| lifetime | Not reproduced for rebinding (F1 class). Untested lifetime forms are in section 6. |
| conditional target | Not reproduced. `runner()` is unconditional and the row is `observed`, not `lead`. |
| parsed-clean ambiguity | Not reproduced. eval_unparsed 0, unparsed_spawns 0, no parse errors, scanner exit in {0,1}, runner pass. |

## 5. Why the green is principled (static trace of tools/mado-tripwire.py)

1. `classify_eval` calls `prepare_eval_calls` (2203–2254), which walks statements in order. For each call it stores a `statement_snapshot` (2163–2200) of env and bindings at that statement, and `module_binding` updates the env (2243–2250). At the factory statement, `cmd` is L1.
2. `assignment_binding` → `callable_info` → `factory_result` (1642–1684). The `bind_literal` keyword path (2121–2138) evaluates `cmd` against the live env, so `argv := L1`. `literal_value` on a Name returns the env object (1361–1363).
3. `factory_result` overlays `closure_env` for the names in `bound` (1678–1683). The helper for `run` therefore carries `argv := L1`, independent of the later rebinding of `cmd`.
4. At `runner()`, `spawn_scan` overlays `closure_env` into the call environment (2511–2516). `follow_helper` (2407–2439) binds no parameters and evaluates `subprocess.run(argv)` with L1. `classify_shell(shlex.join(L1))` yields rule `pacman:-S`, class host_mutation, evidence observed.
5. The late global L2 is never read, because `run` references only `argv` and `subprocess`.

So the observed row follows from the lifetime rule, not from a coincidence of values. That holds for the rebinding dimension only.

Non-blocking documentation note: the tool header (lines 47–50) lists a "returned closure" among values handed on, which yield `lead`. Here the closure is later called by name and followed (header lines 38–46). The code matches the followed path, but the header example reads ambiguously.

## 6. Discrimination limits (mutants this green would not kill; static reasoning only, nothing run)

Would survive this case:

- First module-level binding of `cmd` used in place of the creation-time value. Result is still `-S`.
- Positional fallback for keyword arguments. Identical on a one-parameter factory.
- Cell-versus-snapshot capture of factory locals. `make` has no statement after `def run`, so no factory-local rebinding is possible.
- Same-name collision. No module global is named `argv`.
- In-place mutation of L1. Not present in this case (section 7).

Killed by this case: late binding (`-Q` observed), observed-to-lead downgrade, dropped row, extra or duplicate row, unparsed greater than 0, scanner exit 2, and a free variable resolved against module globals (unresolved).

## 7. Adjacent risk (not measured; not a verdict on CaptureKeyword)

In-place method mutation of a captured object is not tracked.

- `prepare_eval_calls` marks mutation only for Subscript and Attribute assignment targets (2231–2242), gated by `mutated_literal` (1329–1342). Subscript and attribute mutation are therefore conservative: the closure value becomes LITERAL_MISS.
- A statement such as `cmd.append("r22-kw-extra")` (also extend, insert, clear, remove, pop, sort, reverse, update) is an expression call. `assignment_binding` gives `cmd` kind `value` (1875–1876). `callable_info` on `cmd.append` returns unresolved (1797–1804). In `spawn_scan`, an unresolved Attribute callee whose attribute is not a spawn name falls through to `continue` (2606–2614), so the call is silently ignored. Nothing is marked mutated, and no unparsed count is added.
- The closure's argv is the same list object as `cmd`. At runtime the spawn includes the appended element, but the scanner's stored literal is the pre-mutation list.
- Static prediction [INFERENCE, unmeasured]: for the variant below, the tool prints `pacman -S r22-kw-factory` as observed. The true command is `pacman -S r22-kw-factory r22-kw-extra`. That is a stale pre-mutation command printed as observed, which supported-forms line 17 forbids ("Do not print a stale pre-mutation command as observed").

Variant text for L1 (not executed; not written to any fixture):

```python
import subprocess
def make(argv):
    def run():
        subprocess.run(argv)
    return run
cmd = ["pacman", "-S", "r22-kw-factory"]
runner = make(argv=cmd)
cmd.append("r22-kw-extra")
runner()
```

Measuring this variant needs one new source-shaped probe, which this lane does not authorize. Suggested check for L1: whether the sibling case CX3CaptureMutation (not read by me, out of scope) covers method-call mutation. If it does not, route the probe to a measuring seat.

## 8. Oracle observations (measure.py; apply to all cases, checked here against CaptureKeyword)

- The exact path compares the sorted class/command/evidence multiset, `unparsed == 0` (eval_unparsed plus unparsed_spawns), empty parse_errors, scanner exit in {0,1}, input digest, single file and reported path (evaluate 752–756; parse 683–729). It does not compare the tool's own counters (`counts`, `observed_findings`, `lead_findings`, `unpermitted`, the `MADO_TRIPWIRE:` label) or per-finding line, tool_call_id and rule attribution. These are consistent here (1/0/1), but the oracle would not notice a mismatch.
- `require_signal: true` has no effect on exact cases. The exact branch returns (752–756) before the signal check (765–767).
- `forbid_observed_commands` is redundant on exact cases, because any extra row already fails the multiset. It does not single out lead-tier stale commands; the multiset covers those.
- `timestamp` is the string `"None"` when the transcript lacks one (tool line 2890). Cosmetic; the oracle does not compare it.
- Uncertain-path distinction (not exercised here): `accept_exact_want` is an exact alternative, accepted only when rows equal it and unparsed is 0. Otherwise any observed row fails, and a lead or unparsed signal is required (765–778). CaptureKeyword has no accept list, so neither the alternative nor the uncertainty path applies. Its exact want is the only pass path.

## 9. Scope against the current C1 target

- Target (registration.md, C1): every eligible frozen expectation matches; every original red resolves without changing expectations; no-harm guards hold.
- This evidence covers one of 57 sealed cases, one exact case. It supports the claim that the CaptureKeyword expectation matches the tool at the delivered bytes. It says nothing about the other 56 cases, the original reds, or the removal and error comparisons.
- For the lifetime clause, this case covers the rebinding dimension (F1 class). It does not cover in-place mutation (section 7), first-binding versus creation-time (section 6), or positional versus keyword matching (section 6).

## 10. Verdict

AGREE for CaptureKeyword. The sealed exact expectation equals the measured rows. Uncertainty is not warranted. The semantic rationale holds. No falsification was found in the six attack classes.

No admission granted. Advisory only.

Report: .ufo/waves/round-22/w2/reports/FalsifyC120.md
Absolute: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC120.md
Receipt: .ufo/waves/round-22/w2/receipts/FalsifyC120/result.json
