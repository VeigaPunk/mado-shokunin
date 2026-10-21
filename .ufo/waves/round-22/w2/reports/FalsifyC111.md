# FalsifyC111: C1 `CXInlineStartAlias`

Verdict: **AGREE**. The sealed exact expectation matches the measured output of the selected C1 tool. Advisory only, from an author-lane seat. No admission, closure, or streak change is granted or implied.

Seat: MadoR22.FalsifyC111 (leaf; no delegation). Receipts: `.ufo/waves/round-22/w2/receipts/FalsifyC111/` (`result.json`, `measure.stdout.json`, `measure.stderr.txt`, `measure.exit.txt`, `hashes-before.txt`, `hashes-after.txt`, `python-version.txt`).

## 1. Identities, checked before and after the single run

| Artifact | sha256 | Status |
|---|---|---|
| `tools/mado-tripwire.py` (C1 selected tool) | 36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce | matches fixed identity; no drift across the run |
| `oracle/expected.json` | b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357 | matches fixed identity; pin file 7cc4aae9017a157faea3d66e47b5bc0181ec9093a3160d1c41d8e2e93b1567f6 |
| `oracle/measure.py` (runner) | 41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7 | unchanged |
| `oracle/assemble.py` (producer) | 0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600 | unchanged |
| `oracle/inputs/CXInlineStartAlias.jsonl` (fixture) | 9470e1b287929f9e173ba3cafff0645ceed13f5307a59efadc43e0c4fef54e7b | matches case `input_sha256`; one line |
| `w1/proposals/CXInlineStartAlias.json` | bb76deacf41e5dc060158bbbcb0dc8e0b3bb4c34ee01106a82b7b1378f045592 | matches sealed proposal sha |
| `w1/sources/SourceThread/threading-v3.14.8.py` | 5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3 | matches sealed citation sha |

The runner re-validated the full population before and after the run: 106 sealed source files, 52 proposal files, 57 input files, `population_sha256` 046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad, truth seal 47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4. `integrity_errors` is empty. Tool hash before equals tool hash after.

## 2. The one measurement

- Command: `/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CXInlineStartAlias` (Python 3.14.8).
- Runner: exit 0, status `complete`, totals pass 1/1.
- Scanner child, one, under the runner's 384 MiB and 15 s caps: exit 1 (findings present; the runner accepts 0 or 1), stderr empty, no scanner error. Its stdout is `MADO_TRIPWIRE: findings` followed by the verdict JSON.
- Actual rows: `[{class: host_mutation, command: "pacman -S r22-cxinline-alias", evidence: observed}]`.
- Sealed rows: the same single row. `accept_exact_want` is null. Both forbid lists are empty. Expected `unparsed` is 0.
- Payload: `eval_calls` 1, `eval_unparsed` 0, `unparsed_spawns` 0, `observed_findings` 1, `lead_findings` 0, rule `pacman:-S`, argv0 `pacman`, line 1, `tool_call_id` `CXInlineStartAlias-0`.
- Result: `unparsed` 0, `reasons` [], `pass` true.

## 3. Independent semantic reasoning (from source, not tool output)

- Command text: `subprocess.run(["pacman","-S","r22-cxinline-alias"])` gives `shlex.join` = `pacman -S r22-cxinline-alias`.
- Class: `-S` with none of the refresh, upgrade, download, or clean flags (`y u w c`) and none of the query or list flags (`s i l g p`) falls to host_mutation (`classify_pacman`, tool 775–781). Package installation is a host mutation.
- Path: `threading.Thread(target=worker)` stores `worker` as `_target` with empty args and kwargs (threading src 925–928). The `.start` bound method is stored in `start`. `start()` calls `Thread.start` (src 975–1011), which sets `_started` (src 1071) and then runs `self._context.run(self.run)` (src 1082). The default `run` calls `self._target(*self._args, **self._kwargs)` (src 1022–1024), which is `worker()`, which calls `subprocess.run`. `start()` returns only after `_started.wait()` (src 1011).
- Unconditional: straight-line module code, one start, no arguments, no rebinding of `worker` or `subprocess`, no cancel path.
- Evidence `observed` is correct. Residuals are environmental: thread creation failing, the executing thread being killed before the spawn, or the executing thread's daemon status (`_daemonic = current_thread().daemon`, src 934). The tool's contract is "issued is not executed" (tool header lines 30–31). The daemon status of the eval host's thread is not shown in the repository [INFERENCE: it affects only completion at interpreter shutdown].
- Exact is the correct kind. Downgrading to lead or uncertain would understate a reached, unconditional command and would weaken the no-harm guard.

## 4. Falsification attempts (static reading; no additional probes run)

| Attack | Result | Code and evidence |
|---|---|---|
| False observed or lead argv | Not falsified | The row is observed because the path is followed. `start` binds to `scheduled_invoke` (tool 1784–1790, 1839–1853). `spawn_scan` follows the captured target (2470–2486) and reaches `subprocess.run` (2623–2684). The Thread target is not swept as a lead: refs whose parent is a Thread constructor are skipped (2731–2734), and argument-protocol refs are dropped (2698–2700). Measured leads: 0. |
| Lost true command | Not falsified | The binding survives into the call's snapshot (`statement_snapshot` 2163–2200). `state.done` is false on the first start (2470–2474). No mutated literal (2477–2479). |
| Wrong identity | Not falsified | Argv is exactly `[pacman, -S, r22-cxinline-alias]`. The target captured at construction is the only definition, `worker`. The comparator checks only class, command, and evidence (`ROW_KEYS` measure.py 32; `row_keys` 732–733). `tool_call_id`, `line`, and `rule` are not compared. They are correct here, but the comparator does not verify them. |
| Lifetime | Not falsified for this shape | The bound method keeps the Thread alive. The scanner captures the target at construction (1849–1851), not at call time. No rebinding exists, so early versus late capture is not exercised. A second start is blocked by the shared `state` (2470–2474), matching the `RuntimeError` at src 988–989. Not exercised here. |
| Conditional target | Not present | `worker` is unconditional. No branch or loop. |
| Parsed-clean ambiguity | Not falsified | Exact mode requires row-multiset equality and `unparsed == 0` (measure.py 753). `parse_scan_output` rejects shape, digest, and path errors (685–709). A silent clean would fail; none occurred. |

## 5. Uncertainty boundary for this case

- `accept_exact_want` is null and `expected_kind` is exact. This is consistent. No alternate uncertain row set is semantically warranted.
- `require_signal` is true and validated, but `evaluate` returns at line 756 before the signal check at 765. It is inert for exact kinds. Here it changes nothing, but it means the field enforces nothing for exact cases.

## 6. Truth, expectation, and provenance observations (reported, not normalized)

- Citation drift: the sealed source cites tool bytes 46c82902 (`dotted()` 1280–1290; exemption 2550–2553). On 36fdc459, `dotted` still returns None for `Attribute(Call)` (1279–1289). The alias is now resolved earlier, in `callable_info` 1784–1790, and the exemption is at 2731–2734. The mechanism changed; the expected row did not.
- The rationale's "the bootstrap calls `self.run()`" is accurate in substance: the call is `self._context.run(self.run)` (src 1082).
- Multiset versus tool: `scan_file` dedupes findings per tool call on `(class, rule, evidence, command)` (tool 2875–2885). Two identical rows within one eval cell cannot be represented. A sealed exact truth with repeated identical rows in one cell is unsatisfiable, which is a false red and not a false green. Not exercised here.

## 7. Scope against the current C1 target

- Claimed form (`supported-forms.md`): "stored/inline/aliased standard .start/.run".
- This case covers one inline-constructed Thread, no args or kwargs, `.start` aliased to a module name, a single call, and a Name target. It is inside the claimed form.
- Not covered: `.run` alias (same branch, synchronous), args and kwargs, Timer, two Thread instances, repeated start, cross-cell persistence, and a Thread returned from a factory. A pass here says nothing about those.

## 8. Out-of-case static leads (NOT executed; for planner decision; none is admission evidence)

A. Silent clean through an unresolved start receiver. Two code facts combine. (i) Thread and Timer target refs are exempt from the sweep unconditionally (2731–2734), so the target body is never reported as a lead. (ii) An unresolved non-spawn method call adds neither a finding nor an unparsed count (2606–2614). Static chain for this fixture, not run:

```python
import subprocess
import threading


def worker():
    subprocess.run(["pacman", "-S", "r22-loop-start"])


threads = [threading.Thread(target=worker) for _ in range(2)]
for t in threads:
    t.start()
```

`t` has no binding when `t.start` is classified. The loop-target binding is applied after the statement snapshot (`update_bindings` 1973–1975), so the receiver is unresolved. The truth is two starts of the same worker, so two identical `pacman -S r22-loop-start` commands. Predicted scanner output: zero rows and zero unparsed [INFERENCE from static reading]. The same route plausibly applies to subscript or container receivers, tuple-unpacked names, and comprehension variables [INFERENCE]. A Thread passed as a Name into a visible helper that starts it is handled, because `bound_callables` (1608–1626) propagates the scheduled binding [INFERENCE]; that shape is not a leak. Confidence in the chain is high from two readings, but it is unmeasured. Scope: outside C1 `CXInlineStartAlias`; it bears on whether unresolved start routes can be certified clean. No probe was run for it.

B. Per-tool-call dedupe (2875–2885). See section 6.

## 9. Records

- Installs or updates: none. No package transactions, services, or probes.
- Scanner runs: exactly one (the authorized `--case` child). Old round-21 tools were not run.
- Writes: this report and this seat's receipts directory only. No production, fixture, expected, or registry edits.
- Admission: none granted.

## 10. Checks for Main

None required from this seat. The runner pass is recorded. Full-population validation and the 175-case historical target remain Main's.

Report: .ufo/waves/round-22/w2/reports/FalsifyC111.md
