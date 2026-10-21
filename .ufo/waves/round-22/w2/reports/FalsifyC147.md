# FalsifyC147 — C1 TimerRun

## Verdict

**Agree, for this exact sealed case.** The delivered tool's complete row multiset, evidence tier and zero-error state match the pre-sealed expectation, and independent semantic derivation of CPython 3.14 `threading.Timer.run()` confirms the expected truth. I found no false observed/lead argv, no lost true command, no wrong identity, no lifetime or conditional-target ambiguity, and no parsed-clean ambiguity for this fixture.

This is author-lane advisory falsification evidence. It grants no admission, no closure, no desktop clearance, and does not alter L1's planner/integration authority or the r19/r20/r21 rejected-harmed streak.

Axes kept: (1) exact class/command/evidence agreement; (2) scheduled-target lifetime and callable identity; (3) observed-vs-lead honesty; (4) tool/fixture/runner identity and bounded-measurement provenance; (5) scope honesty.

## Independent semantic expectation

Original proposal: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/TimerRun.json` (sha256 `c63de1cddc89c038b007956e0baba4a3f123fa3adbcb7c965fd041370befbb68`, sealed in `truth-seal.json` at base `741122d177ae8ff68a73768777f20484d5bdcbe4`, created 2026-10-21T14:39:04Z). Source citation: `/usr/lib/python3.14/threading.py` (CPython 3.14.8, sha256 `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3`) and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:90-95` (F4: scheduled `.run` never followed; "`t.run()` calls the target synchronously in the caller").

The sealed cell is one module-level eval:

```python
import subprocess
import threading

def worker(argv):
    subprocess.run(argv)

argv = ["pacman", "-S", "r22-timer-run"]
t = threading.Timer(1, worker, args=(argv,))
t.run()
```

1. `threading.py:1370-1376`: `Timer.__init__(interval, function, args=None, kwargs=None)` sets `self.interval=1`, `self.function=worker`, `self.args=(argv,)`, `self.kwargs={}`, and `self.finished=Event()` (fresh, unset).
2. `threading.py:1382-1386`: `Timer.run` calls `self.finished.wait(self.interval)` and, because `is_set()` is false, calls `self.function(*self.args, **self.kwargs)` **synchronously in the calling thread**. `interval=1` delays the call; it cannot change which literal argv is issued.
3. No `start()` is called, so no OS thread is created. `t` has no other reference; `cancel()` (`threading.py:1378-1380`, the only pre-run setter of `finished`) is unreachable; a subclass cannot override `run` because `Timer` is the stdlib class, unshadowed.
4. Therefore `worker(argv)` is issued and `subprocess.run(["pacman","-S","r22-timer-run"])` is the one true command. Complete expected multiset: `host_mutation / pacman -S r22-timer-run / observed`, with zero `eval_unparsed` and `unparsed_spawns`.

Observed here means statically issued (the oracle's evidence convention), not runtime executed. `exact` is warranted: the module path is straight-line, with no branch, loop, conditional target, rebinding, later cell (`cell_count=1`, `cell_reset=[false]`), or cancel writer. `accept_exact_want` is null and both forbid lists are empty, so this case does not exercise the all-tier forbidden-argv or accept-exact-vs-uncertainty rules.

## Candidate relevant path in the delivered revision

Delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`; the selected tool was last changed by `330de6887430cf54b1cdaee59b20183f0c3e24a0` ("round-22: implement bounded lifetime repair and independent evidence audit"). That diff is the candidate path: it replaces the old `.start`-only `thread_start` mechanism with `scheduled_invoke` for `.run`/`.start`, adds `scheduled_cancel` for `Timer.cancel`, adds shared `{done, cancelled}` state, and carries the resolved target on the synthetic node via `mado_resolved` instead of injecting `__mado_thread_target__` into the binding namespace (also the F5 hygiene shape).

Current-file trace (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`):

- `:1841-1853` — `assignment_binding` recognizes `threading.Timer`, takes `function=worker` (keyword/positional per timer) and `args=(argv,)`, records `timer=true`, `state={done:false,cancelled:false}`, target helper identity, literal args/kwargs.
- `:1787-1792` — `callable_info` on an attribute of a `scheduled` receiver: `.run`/`.start` → `scheduled_invoke`; `Timer.cancel` → `scheduled_cancel`.
- `:2470-2487` — first non-cancelled, non-done `scheduled_invoke` builds an inert synthetic call to the captured target with the captured literal positional args, then recurses; duplicate/cancelled invokes emit nothing; unbindable args count as unparsed.
- `:2409-2446` — `follow_helper` follows `worker` with `argv` bound; `:2626-2668` classifies `subprocess.run(argv)` and maps `pacman -S` to `host_mutation`; `:2875-2895` marks followed 4-tuples `observed` and swept bodies `lead`.
- `:2733-2734` — a reference whose parent call is `threading.Thread`/`threading.Timer` is not swept, so the constructor alone emits nothing.

`worker` is referenced only as the Timer `function` argument and is never called directly. The observation therefore necessarily comes from the synthetic scheduled-target invocation of `t.run()`, i.e. it demonstrates the F4 `.run` repair for this fixture — not a constructor follow and not an unrelated body sweep (sweeps emit `lead`). [INFERENCE, from source; not separately probed] The pre-repair r21 tool mapped only `.start` (`FinalBindingReview.md:90-95`), so this fixture would have produced no row then; the old tool was not rerun, per contract.

## Sole authorized measurement and actual rows

Executed once, one scanner child, runner-enforced 384 MiB address space and 15 s timeout:

```text
timeout 20 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py \
  --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case TimerRun
```

`timeout 20` was an outer guard and did not fire; the runner's recorded argv is `/usr/bin/python3 <measure.py> --tool <tool> --case TimerRun` (`-I` is an interpreter flag and is not in `sys.argv`).

| Quantity | Actual |
| --- | --- |
| Runner status / OS exit | `complete` / `0` |
| Case comparison | `1/1`, `pass: true`, `reasons: []` |
| Scanner OS exit / scanner error | `1` (findings) / `null` |
| Complete rows | `host_mutation / pacman -S r22-timer-run / observed` |
| Wanted rows | identical, multiset-equal |
| Observed / lead findings | `1 / 0` |
| `eval_unparsed` / `unparsed_spawns` | `0 / 0` |
| File lines / eval calls / bash calls | `1 / 1 / 0` |
| Scanner file sha / path | `d513fafa…` / exact selected fixture |
| Forbidden argv at any tier | none present (lists are empty) |
| Runner stderr / scanner stderr | empty / empty |
| Integrity errors / before-after hash drift | `[]` / none |
| Population validated | 57 inputs, 52 proposal files, 106 sealed source files |

The scanner payload shows `counts.host_mutation=1`, all other class counts 0, `observed_findings=1`, `lead_findings=0`. The runner validates the full frozen population before and after selecting the case (`measure.py:467-643,789-870`); **those are integrity counts, not 57 scanner runs and not 57 semantic passes.**

### Identity evidence (checked before and after; all stable)

| Artifact | SHA-256 |
| --- | --- |
| Selected C1 tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (matches assignment pin) |
| Oracle expected manifest | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` (matches pin) |
| Runner `measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| TimerRun fixture | `d513fafa0986e723f806a5cf8486a1ac6da9d2ae1b0b1d7a310e947d4af82dcb` (equals case/input row) |
| Producer `assemble.py` | `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600` |
| Raw truth seal | `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` |
| Installed `threading.py` (truth basis) | `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3` |

The runner checks the selected tool only for stability across the run, not against a fixed literal; fixed-identity equality was verified independently here by `sha256sum` before and after. Receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC147/result.json` (outer/scanner argv, exits, stdout, stderr, payload, case rows, hashes, and the source trace).

## Falsification checks for this case

| Failure mode | Result |
| --- | --- |
| False observed / false lead argv | None. Command is exactly `pacman -S r22-timer-run`, argv0 `pacman`, rule `pacman:-S`; no truncation, quoting drift, or borrowed global. |
| Lost true command | None. The one true row is present; no dedupe or redaction removed it. |
| Wrong identity | None. `host_mutation` is correct for bare `-S` (tool `:738-790`); the target is `worker`, captured at construction, not the module-global `argv` or an unrelated callable. |
| Lifetime | None here. `t` is bound before `t.run()` in the same cell and is never rebound/deleted; the scheduled state is shared between the binding and the invoke; the fixture is one non-reset cell. |
| Conditional target | None in the executed path. No branch/loop precedes `t.run()`; `Timer.run`'s `finished.is_set()` guard is false by construction and `cancel()` is unreachable. The scanner models the target call unconditionally; for this fixture that coincides with real semantics. |
| Parsed-clean ambiguity | None. Zero unparsed counters, strict single-line JSON payload, empty scanner stderr, exit 1 accepted as a findings verdict, file sha and path matched the sealed fixture. |
| Degenerate green | No. A row requires following a resolved invocation; the constructor-only path is skipped (`:2733-2734`) and swept bodies are `lead` (`:2407-2409`), so the observed row is path-attributable to the scheduled `.run` repair. |

No extra scanner runs, mutants, old-tool reruns, builds, lints, formatters, full-suite tests, live probes, or fixture execution were performed. The fixture code was treated as inert JSON/AST input only.

## Residual uncertainty and scope

- This is one case of 57, and one fixture. It does not establish C1's "all eligible frozen expectations match", does not run the other 56 cases, and does not prove F4 generally: aliased `run`/`start`, inline `Timer(...).run()`, cancellation before run, no-start, subclass `run` overrides, factory-closure targets and repeated invocation are not covered here. `OriginalF4ThreadRunDirect` and the alias/inline/cancel cases remain separate requirements.
- The scanner models `Timer.run` as an unconditional target call and does not simulate `finished.is_set()` or the one-second wait. Here both models coincide (fresh unset Event), so this case cannot discriminate the guard's negative branch; CX6TimerCancel-style cases carry that burden.
- Per-cell `unique_hits` deduplication (`:2876-2895`) collapses identical repeated invocations into one row. This fixture invokes once, so row multiplicity is untested.
- `expected.json` is not itself inside the 106-file raw seal; `materialization_status` states it is a normalized expected materialized later and pinned separately. The TimerRun proposal and fixture are sealed pre-implementation, the runner verifies proposal-byte equality, and the pin fixes the expected digest. That honesty caveat is retained, not normalized away.
- No `lsp` device exists in this seat (`xd://lsp` reports no such tool), so definition/reference requests were impossible. Literal source reads at the cited branches are used; they are path evidence, not semantic absence proof across the tool.
- The pre-repair red for this fixture is taken from the r21 F4 authority and the delivered diff, not from rerunning the old tool; no r21 receipt was re-executed or reinterpreted.
- A sensitivity recipe for L1 (proposed, **not run**, not a killed fault): in a private sandbox copy, disabling the `scheduled_invoke` branch, or redirecting the Timer target extraction to `node.args[0]`, should make this case lose its only row; L1 may use that to confirm the green is path-dependent.

Production, fixtures, expectations, tools, and shared documentation remained read-only. Only the assigned report and receipt were written. No installs or upgrades were needed or performed.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC147.md
