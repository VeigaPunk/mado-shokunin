# ThreadReuseName — C1 truth proposal: two thread instances, different targets, one reused local target variable

Seat: `MadoR22.ThreadReuseName` · Round 22 w1 · 2026-10-21 · Author-lane truth freeze only. No production edits, no detector measurements, no payload execution, no probes, no installs, no background jobs, Git untouched (read-only by absence of any write).

## Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/ThreadReuseName.json` — one proposal, one eval cell, `expected_kind: "exact"`, two `want` rows, `forbid_observed_commands: []`.

Frozen input cell source (verbatim, one eval cell):

```python
import subprocess
import threading

def run_install(argv):
    subprocess.run(argv)

def run_query(argv):
    subprocess.run(argv)

target = run_install
t1 = threading.Thread(target=target, args=(["pacman", "-S", "r22-reuse-a"],))
target = run_query
t2 = threading.Thread(target=target, args=(["pacman", "-Q", "r22-reuse-b"],))
t1.start()
t2.start()
```

Cell source sha256 (input digest to freeze): `4ff8ab0bc16ceec846b59cda5230b5d28654246d605bed19e5afa3ed9ecdf206`, computed with `python3 -I` + `hashlib.sha256` over the exact UTF-8 `cells[0]` string as stored in the proposal file; the proposal JSON parsed cleanly (`id`, `expected_kind` exact, 1 cell, 2 want rows, empty forbid list verified).

## Static truth (Python 3.14, nothing executed)

| Statement | Effect |
|---|---|
| `target = run_install` | local name `target` binds to `run_install` |
| `t1 = Thread(target=target, args=(["pacman","-S","r22-reuse-a"],))` | argument expressions evaluate now: instance stores `_target=run_install`, `_args=(["pacman","-S","r22-reuse-a"],)` by reference |
| `target = run_query` | rebinds only the local name; neither existing instance changes |
| `t2 = Thread(target=target, args=(["pacman","-Q","r22-reuse-b"],))` | instance stores `_target=run_query`, `_args=(["pacman","-Q","r22-reuse-b"],)` |
| `t1.start()` / `t2.start()` | each `run()` invokes `self._target(*self._args, **self._kwargs)` |

Want (set; listed in start order):

1. `host_mutation` `pacman -S r22-reuse-a` `observed`
2. `package_query` `pacman -Q r22-reuse-b` `observed`

Command strings are `shlex.join` token serializations, matching the r21 fixture convention (`pacman -S r21-thread-run`).

## Evidence chain

- CPython v3.14.8 `Lib/threading.py`, official opened copy `.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py`, sha256 `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3`, receipt `receipt.json` (tag `refs/tags/v3.14.8`, peeled `8e6e75d9102e39bed2a2b279203a396741180f12`):
  - 925–928: `self._target = target; … self._args = args; self._kwargs = kwargs` — stored by reference at construction; argument expressions evaluate at the construction call site.
  - 1023–1024: `run` calls `self._target(*self._args, **self._kwargs)`.
  - 1082: `start()` schedules `run()` in the new thread; the instance, not the variable, carries the callable.
- `.ufo/waves/round-21/residual/FinalBindingReview.md` (read as needed): scheduled-binding `.start()` maps to `thread_start`; Thread `args`/`kwargs` evaluated at construction is listed as correct timing; a thread target handed on as a value is skipped by the refs sweep, so `.start()` is the owner path. F4 (`.run`) and F1 (closure invoke-time binding) are named defects this wave must fix; my variant is built on the supported `.start()` path and independently discriminates late binding.
- r21 fixtures `thread-run-direct.jsonl`, `thread-key-control.jsonl`: storage + literal-argv + top-level-def conventions copied, not guessed.
- LSP: not used (no `lsp` device answered any file in this seat's reads; evidence is official-source line quotes plus prior-wave review text). Text reads are labeled as such and are not semantic proof of the future implementation — the proposal defines truth independent of any implementation.

## Why the two rows are `exact`

Both argv are literal tuples, both targets are module top-level `def`s whose bodies call `subprocess.run` on their parameter, and both invocations are `.start()` calls on stored instances. Nothing in the cell is conditional, opaque, or imported late, so each row's class, command, and evidence tier is fully determined statically. The two rows share only the variable name `target`; the instances are distinct objects built by distinct calls at distinct statements.

## Discriminating power

- **Construction-time vs start-time target resolution.** Both `.start()` calls happen after the `target = run_query` rebind. A detector that resolves `target` when it sees `.start()` (an F1-shaped defect applied to the thread path) yields two `package_query pacman -Q r22-reuse-b` rows and no `host_mutation` row → red.
- **Per-instance binding vs shared/global collapse.** A detector that keeps one shared entry for the reused name across both scheduled bindings produces the same wrong collapse → red.
- **Evidence tier.** Both rows must be `observed`; neither is reachable through a lead path in truth.

## Supported-form discipline; shapes considered and honestly rejected

Kept — minimal variant inside the declared supported forms: two module top-level `def` targets, one literal argv per instance, stored `Thread` instances, `.start()` only, one cell.

Rejected, not guessed:

1. **`lambda` targets** — the r21 binding machinery builds its callable map from top-level `def`s; a lambda target is not a declared supported callable form. Excluded.
2. **`Thread` subclass overriding `run`** — explicitly out of scope (module docstring: inherited methods are not resolved; r21 review Limits). Excluded.
3. **`**` spread into `Thread(...)`** — named unsupported in r21 review Limits. Excluded.
4. **Conditional target selection** (`target = run_a if flag else run_b`) — non-literal control flow, not a declared supported form. Excluded.
5. **Reusing the variable for the instance too** (`t = Thread(target=run_install, …); t.start(); t = Thread(target=run_query, …); t.start()`) — plausibly supported but conflates instance rebinding with target reuse; not the assigned shape, and it weakens the late-binding discriminator (the first `start()` precedes the rebind). Not chosen.
6. **Rebinding an argv variable instead of the target variable** — different assignment (sibling seats cover argv reuse); the assigned axis here is the target variable. Not chosen.

## Scope limits (disclosed, not gaps in the proposal)

- Does not exercise F4 (`.run()`): my variant uses `.start()`, which is the already-supported owner path; `ThreadRun`/`TimerRun` seats cover `.run`.
- Does not cover `Timer`, cross-cell persistence, or inherited `run`; single-cell by design (bindings persistence across cells is orthogonal).
- No detector behavior is claimed anywhere: nothing was measured, and `tools/mado-tripwire.py` was not read (no changed code exists at base; truth derives from Python semantics only).
- Order of `want` rows is start order, informational; the assertion is the set.

## Tools

None installed or updated. No probes. No subprocess jobs.
