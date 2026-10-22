# CritEscapeNeighbour — C1 callback escape-neighbour discovery (outside the counter)

Seat: `MadoR23.CritEscapeNeighbour` (critic, leaf). Lane tip `a28e4815aabfa85f55274884000fb2608355f8cf`.
Base classifier `tools/mado-tripwire.py` SHA256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`
(checked against the registration; the runner refuses any other sha via `--expect-tool-sha`).

## Result

All three new escape-neighbour fixtures fail at base. One is a full **silent miss**: an executed
`subprocess.run` produces no finding row and no unparsed count, and the scanner exits 0. One is a
**false observed** host mutation: a foreign argv that never runs is reported as observed. This is the
round-23 H4 caller-frame leak again, one forwarding hop deeper. One is **unparsed** with the executed
argv absent, where the dict and attribute store neighbours keep a lead at base.

| Case | Fixture sha256 | Executed argv (truth) | Base rows | Base unparsed | Base class |
|---|---|---|---|---|---|
| `EscapeListAppendThenCalled` | `77ebcdf8b59bcdcb99a9ec8b7d126e14dfb42097fb5f1a6a066416ce7301a6ff` | `pacman -Q r23x-list-global` | none | 1 | base-unparsed |
| `EscapeSecondForwarder` | `d426c7b8b65c21c5d62057f2151e1508a874e5cc3c1314fa8e31a22dc3758a76` | `pacman -Q r23x-chain-global` | `host_mutation pacman -S r23x-chain-inner-foreign observed` | 1 | base-false-observed (also unparsed) |
| `EscapeTupleNestedClosureLater` | `65e8166688594cdefb4cfdc6014836512d9940669822654d2fdab25365920466` | `pacman -Q r23x-tuple-captured` | none | 0 | base-silent-miss |

Base exits were 0, 1 and 0, and no case reported a harness error. Each case's `proposed_rule_pass` is
false. That field applies the pass rule copied from `repair/measure.py` `judge()` to the expectation
proposed in `cases.json`.

## What I did

1. I read `registration.md`, `repair/truth.py`, `repair/measure.py`, `repair/expected.json`, the
   repair fixtures, the base receipt `evidence/repair-before-e33ea304.json`, and the scan helper
   `round-21/oracle/measure.py`.
2. I authored three fixtures in the same JSONL shape as the repair set:
   `out/CritEscapeNeighbour/fixtures/*.jsonl`. They import only `subprocess` and call only
   `subprocess.run(<list literal or name>)`. Each one pairs one escape mechanism with never-executed
   foreign `pacman -S` argv placed in the frames a leaking resolver would wrongly read. That bait is
   the same as the repair set's `forbid_any` convention.
   - **List append then called:** `register(argv, callback)` does `hooks.append(callback)`, and the
     module then runs `for hook in hooks: hook()`. `run` reads module `argv` (`-Q`), and the
     forwarder's `argv` parameter is foreign.
   - **Second forwarder:** `outer(argv, callback)` passes the callback to `inner(argv, callback)`,
     which calls it. Both forwarder `argv` parameters are foreign, and `run` reads module `argv` (`-Q`).
   - **Returned in a tuple, captured by a nested closure that is called later:**
     `make(argv)` returns `(run, argv)`. Then `arm(argv, pair)` unpacks `callback, _ = pair`, wraps it
     in a nested `fire()` and returns it, and the module calls `job()`. The module `argv` and `arm`'s
     `argv` are foreign. Only the argv captured by `make` (`-Q`) runs.
3. I wrote `out/CritEscapeNeighbour/run.py`. It copies truth.py's `CHILD` recording fake-subprocess
   source and `safe()` verbatim, and it adds a shape check that every `subprocess.*` call has exactly
   one list-literal or name argument. Truth runs the child as `python3 -I -S` under 384 MiB and 15 s.
   The real `subprocess` module is never reachable from fixture code. Base results come from
   `runpy.run_path(round-21/oracle/measure.py)["scan"]` (one child, `python3 -I`, 384 MiB, 15 s), the
   same helper that `repair/measure.py` uses. The runner checks that the tool and helper shas do not
   change during the run.
4. `run.py` writes `out/CritEscapeNeighbour/cases.json` with these fields for each case: fixture
   sha256, executed argv, the never-executed shadow argv (all constant list literals minus the
   executed set), a proposed expectation in repair-set format, and the base result. The base result
   holds rows, unparsed, the scanner's per-file counters, foreign rows, missing executed argv, a flag
   list and the proposed-rule pass.

Command (run from the lane root):

```
python3 -I .ufo/waves/round-23/w1/out/CritEscapeNeighbour/run.py --tool tools/mado-tripwire.py --expect-tool-sha cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
```

It exited 0. Receipt: `out/CritEscapeNeighbour/cases.json` (sha256
`4a7a066bd4214dc282e1d51dae4025bba3aa0622bedb3076c07e35d754e18c44`, runner sha256
`28f4055042800d8c03d53c83c5c36b67479450f041e92ee4e407132e6c6c73aa`, helper sha256
`4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da`, Python 3.14.8).

**Classification rule.** A case is `base-error` if the exit is not 0 or 1, or the helper reports an
error. It is `base-false-observed` if any non-executed command appears at the observed tier. It is
`base-unparsed` if `eval_unparsed + unparsed_spawns > 0`. It is `base-silent-miss` if an executed argv
is absent from the observed and lead tiers while unparsed is 0. Otherwise it is `base-correct`. Every
applicable flag is recorded, and the primary label is the first one in that order.

## Counterexamples, evidence, impacted axes

**1. `EscapeTupleNestedClosureLater` is a silent miss (strongest finding).**
- Evidence: the executed `pacman -Q r23x-tuple-captured` gets no row and no unparsed count, and the
  scanner exits 0. Its per-file counters are `eval_calls 1, eval_unparsed 0, unparsed_spawns 0`.
- Contrast within the repair set: `ForwardExistingClosureWithoutFrameContamination` returns the
  closure bare, and `ForwarderInvokesFactoryClosure` passes it as a call argument. Both keep the
  correct observed row at base. Packing the closure into a tuple and re-wrapping it is enough to lose
  all signal.
- Source reading at base: `eager_calls` pairs a loaded name with a parent only when it is a direct
  call argument (`tools/mado-tripwire.py` line 2073, `parents.setdefault(id(arg…), node)` over
  `node.args`). A container literal resolves to `{"kind": "value", "container": node}` (lines
  1877–1878).
- [INFERENCE] `run` inside `return (run, argv)` is never recorded as an escaping callable, and the
  later `callback()` inside `fire` calls a name bound by tuple unpacking, which resolves to unknown
  and is not counted as unparsed. I did not trace the runtime path inside the classifier, so this
  explanation is inferred from the source.
- Impacted axes: operability (recall), and the C1 "no silent miss" premise behind the unparsed
  counter.

**2. `EscapeSecondForwarder` is a false observed host mutation.**
- Evidence: the base emits `host_mutation pacman -S r23x-chain-inner-foreign observed`, plus one
  unparsed. The executed `-Q` argv is missing.
- The leaked argv comes from the innermost forwarder frame that calls the callback (`inner`), not
  from `outer`. This is H4 (`ForwarderInvokesCallback`) at depth 2.
- Attack on the candidate: a repair that strips only the immediate caller frame, or that special-cases
  a forwarder whose own body calls the callback, can pass `ForwarderInvokesCallback` and still leak
  here. It could leak `outer`'s argv or keep `inner`'s.
- Impacted axes: operability (precision: a false observed mutation is the most expensive error class)
  and H4.

**3. `EscapeListAppendThenCalled` is unparsed, with the executed argv absent.**
- Evidence: there are no rows and `unparsed_spawns 1`. The dict-store and attribute-store neighbours
  (`CallbackStoredInDict`, `CallbackStoredOnAttribute`) keep a lead at base.
- `list.append` combined with loop dispatch is the store form that loses recall.
- The fixture combines the append with `for hook in hooks: hook()`, and I did not ablate the two (the
  item caps the fixture count at three). Which of the two loses the lead is unattributed. The loop
  walk at lines 2014–2020 marks iterator parts as `invoke` when the body calls the loop target, so
  [INFERENCE] the store is the more likely cause.
- Impacted axes: operability (recall) and H5, the store-recall guard behind the v3 withdrawal.

**Not covered.** The setattr and `global`-stored callback neighbours are not covered, because the
item caps the count at three fixtures. Attribute stores through `box.cb = callback` are already in the
repair set and pass at base with a lead.

## Smallest safe corrections (advice to the L1; not implemented)

- **Tuple and nested closure:** treat a helper name loaded as an element of a Tuple, List, Set or Dict
  literal that is returned, assigned or passed as an escaping reference. Sweep its body under its
  defining (lexical) frame. The `-Q` argv captured by `make` should come out observed, and at minimum
  as a lead.
  - Do not "fix" this by counting every call to an unknown-bound name as unparsed. That would churn
    the 1356-file corpus comparator and the precision guard (166/175, same passing set).
- **Second forwarder:** resolve a callback's free names in the frame where the callback was defined,
  at every forwarding depth. Never read them from any caller frame on the dynamic stack. Acceptance
  is exactly one row, `package_query pacman -Q r23x-chain-global observed`, with neither foreign argv
  at any tier and unparsed 0.
- **List append:** route `<list>.append(<callable>)` through the same store-recall path as the dict
  subscript and attribute stores, so the executed argv is kept at least as a lead. The frame-leak
  repair must not then resolve `argv` to `register`'s foreign parameter.

## Wave-2 use

`cases.json` carries a `proposed_expectation` for each case in `repair/expected.json` format.
- The exact kind (`package_query`, observed, unparsed 0) is used for the second forwarder and the
  tuple case.
- The present kind (lead accepted) is used for the list case, mirroring `CallbackStoredIn*`.
- `forbid_any` lists every never-executed shadow argv in each case.
- The `package_query` class for `pacman -Q` follows the repair set's convention and base rows. These
  expectations are proposals derived from truth and are not frozen.

Rerun against a candidate:

```
python3 -I .ufo/waves/round-23/w1/out/CritEscapeNeighbour/run.py --tool <candidate tripwire path>
```

This overwrites `cases.json` with that tool's results, so copy the base receipt first.

## Bounds and installs

- I wrote only the files under `out/CritEscapeNeighbour/` and this report. No real subprocess
  executed fixture code, and I ran no jj or mutating git commands.
- Installs or updates: none.

**Verdict:** the base fails all three escape neighbours: one silent miss (tuple and nested closure),
one false observed mutation (second forwarder) and one unparsed recall loss (list append). They are
valid wave-2 attack inputs, and the second forwarder and the tuple case are the strongest
counterexamples to a repair that only satisfies the frozen 12 cases.
