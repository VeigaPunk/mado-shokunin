# FalsifyC144 — C1 case `ThreadRunAlias` (round 22, seat receipt)

Lane: author-lane advisory falsification. No admission authority; no verdict on
the wave, the streak, or other seats. Base `71228fd582d6d9338d7916cc64e69bd4c2e928b5`.
All paths below are under `/home/vgpnk/Projects/shokunin/mado-shokunin`.

## 1. Measurement actually performed

One runner invocation, exactly as assigned, after the fixed identities were hashed:

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py \
  --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py \
  --case ThreadRunAlias
```

- Runner exit `0`, `status: complete`, `case_filter: ThreadRunAlias`, `cases: 1`
  (`scan_children: 1` — the `--case` path validated the full sealed population
  but spawned exactly one scanner child for one fixture).
- Caps observed in `measure.py`: child `RLIMIT_AS = 384 MiB` via
  `preexec_fn=set_address_space_limit`, 15 s subprocess timeout. Wall 107 544 018 ns.
- Tool hash before and after: `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`
  (stable; no drift, no moving target). Expected `b5cd4cf3…59c4357`; pin
  `7cc4aae9…b1567f6`; runner `41b021bb…eb628c7`; producer `0270c10b…2c5600`;
  truth seal `47f403f6…b24d4` (106 sealed sources verified); fixture
  `bed770f9…983e814`; proposal `1043f19f…f045592`.
- Population integrity `before == after`, `integrity_errors: []`:
  106 sealed source files, 52 proposal files, 57 input files verified.
- Disclosure: one earlier shell wrapper (`/usr/bin/time`) failed with exit 127
  before Python started (`stdout` empty, only `error: command not found`); it
  launched no scanner and is not counted. The authorized runner then ran once.
  No second scanner invocation was made anywhere.

## 2. Sealed case, as read before measurement

- `expected_kind: exact`; `cell_count: 1`, `cell_reset: [false]`; no addenda.
- Fixture (sha `bed770f9…983e814`), one eval cell:

```python
import subprocess
import threading


command = ["pacman", "-Q", "r22-tralias-stale"]


def worker():
    subprocess.run(command)


thread = threading.Thread(target=worker)
run = thread.run
command = ["pacman", "-S", "r22-tralias-live"]
run()
```

- `want` (sorted, one row): `{host_mutation, "pacman -S r22-tralias-live", observed}`.
- `forbid_observed_commands: ["pacman -Q r22-tralias-stale"]`;
  `forbid_commands_any_tier: []`; `accept_exact_want: null`; `require_signal: true`.
- Proposal citation F4 (round-21 `FinalBindingReview.md`, "scheduled `Thread.run()`
  is never followed") plus call-time global resolution.

## 3. Independent semantics (reasoned from CPython source, fixture never executed)

Expected complete multiset: **exactly one `observed` `host_mutation`
`pacman -S r22-tralias-live`; zero `lead`; zero unparsed.** Derivation:

1. `threading.Thread(target=worker)` stores `_target=worker`, `_args=()`,
   `_kwargs={}`; construction never invokes `target`
   (`/usr/lib/python3.14/threading.py` 880–928, sha `53239096…5ea2b7e3`).
2. `run = thread.run` binds the *bound method* of that exact instance. The alias
   keeps a strong reference to the instance, independent of the module name
   `thread` (which is neither rebound nor deleted here).
3. `command = [...]` rebinds the module-global name to a **new** list; the stale
   list object is not mutated and becomes unreachable (its only reference was
   the global name). It is never passed to any spawn call.
4. `run()` dispatches to `Thread.run(thread)` (1013–1025). `run` has no
   `_initialized`/`_started` precondition — those guard `start()` (975–1012) —
   and it executes `self._target(*self._args, **self._kwargs)` synchronously in
   the caller thread, so `worker()` runs.
5. `worker`'s free name `command` is a global load at call time (LEGB), yielding
   the live list.
6. `subprocess.run(["pacman","-S","r22-tralias-live"])` is the sole spawn;
   `pacman -S` maps to `host_mutation` (`classify_pacman`, tool 738–784: `S`
   without `y/u/w/c` or `s/i/l/g/p` flags).
7. No exception path precedes the spawn: the constructor does not raise for
   these arguments, `run()` has no state precondition, and no thread race exists
   because no thread is started.

There is **no true uncertainty**: no dynamic input, cancellation, or conditional
target can change the outcome. `accept_exact_want: null` is therefore correct,
not evasive, and any stale `-Q` row would be an invented command at *every* tier,
not merely a forbidden observation. (Full-multiset equality makes the
`forbid_observed_commands` entry redundant for this case; the empty
`forbid_commands_any_tier` is harmless because exactness leaves no room for an
extra row.)

## 4. Actual rows

Scanner payload (`mado-tripwire-verdict-v1`), measured:

```
observed_findings: 1, lead_findings: 0, unpermitted: 1
counts {host_mutation:1, package_query:0, live_probe:0, tool_install:0, vcs_write:0}
files[0]: eval_calls 1, eval_unparsed 0, unparsed_spawns 0, sha256 = sealed fixture,
          path = the selected fixture
findings[0]: {class host_mutation, command "pacman -S r22-tralias-live",
              evidence observed, rule "pacman:-S", tool_call_id "ThreadRunAlias-0"}
```

Runner row comparison: `got_rows` equals `want` exactly, `unparsed = 0`,
`pass = true`, `reasons = []`, scanner exit 1 (findings), runner exit 0.
Scanner log prefix `MADO_TRIPWIRE: findings` then one strict-JSON line; the
runner's last-nonempty-line parse and the file path/digest checks passed.

## 5. Falsification axes for this case

| Axis | Observed | Assessment |
|---|---|---|
| False observed/lead argv (stale `-Q`) | absent; only the live command, zero leads | pass — stale list is unreachable at call time |
| Lost true command (F4 silent miss) | present as `observed`; not the r21 "no row, unparsed 0" mode | pass |
| Wrong identity | source path is `callable_info(Attribute)` → scheduled receiver → `scheduled_invoke` (tool 1788–1792) → `scheduled_invoke` branch (2467–2482) → synthetic `Name("<scheduled target>")` carrying `mado_resolved = worker` → `follow_helper` with stored `args=()`/`kwargs={}`. The synthetic id is not a legal source identifier and is resolved before any bindings lookup, so no F5-style namespace collision. | identity correct by source trace; **but** output is observationally invariant under substituting a direct `worker()` call, so the row alone cannot prove bound-method dispatch |
| Lifetime | bound method pins the instance; `thread` stays bound; no deletion/rebinding | not exercised; no defect exposed |
| Conditional target | one unconditional target, one unconditional invocation; no lead invented | pass |
| Parsed-clean ambiguity | `eval_calls 1`, `eval_unparsed 0`, `unparsed_spawns 0`; zero is honest for a text whose argv and sole invocation are fully fixed | pass |

The stale-vs-live choice **is** genuinely discriminated by this fixture (a
construction- or alias-time env capture would emit `-Q`); the observed live row
therefore shows late global resolution, not a coincidence. What the green does
*not* discriminate is bound-method identity versus direct-target identity.

## 6. Verdict

**Agree.** For `ThreadRunAlias` the delivered green is semantically warranted:
the actual row set is the complete expected multiset under the declared
supported forms, no invented argv appears at any tier, no true command is lost,
and `unparsed = 0` is honest. This is an author-lane advisory falsification
receipt only — **no admission grant**, no streak disposition, no statement about
any other case or about family-wide closure.

## 7. Scope relative to the current target

- Covers one fixture: aliased `thread.run` after a module-global rebinding,
  unstarted `Thread`, bound method called synchronously.
- Does not exercise repeated invocation, `start()`+`run()` interaction (which is
  genuinely racy: the started thread may delete `_target` before the explicit
  `run()`), `Timer.run`, cancellation, or `del thread`/`thread` rebinding before
  the alias call. The source retains the scheduled dict in the alias binding, so
  a `thread` rebinding would not disturb `run` [INFERENCE from tool source,
  untested].
- The other 56 sealed cases were validated only structurally (population,
  digests, one-to-one fixtures); their semantics were not measured here.
- One external workspace change was observed during this seat: tracked
  `SCORECARD.md` gained 13 lines at 2026-10-21T12:40:10-03:00 and untracked
  `w2-*.json` files appeared, all from concurrent lanes. This seat wrote only
  its own receipt directory and made no production/fixture/tool edits.

## 8. Evidence

Receipts (absolute):
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC144/`
— `result.json` (argv, exit, stdout, stderr, hashes, payload), `stdout.txt`,
`stderr.txt` (empty), `exit.txt`, `hashes-before.txt`, `hashes-after.txt`.

Confidence: high for the measurement capture and the sealed identities; high for
the CPython semantics (installed 3.14.8 source, sha `53239096…`); high that the
green is warranted for this text; medium for identity attribution (source-traced,
observationally blind); unconditional for nothing beyond this one case.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC144.md
