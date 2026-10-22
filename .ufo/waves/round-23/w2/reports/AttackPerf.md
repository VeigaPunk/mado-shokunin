# AttackPerf — C1 resource attack on the round-23 scope chain (wave 2, falsify)

**Verdict: REGRESSION FOUND.** The landed classifier (tip `2f1134f3`, `tools/mado-tripwire.py`
sha256 `41489991…`) fails inside the 384 MiB / 15 s caps on two inert fixture families where the
base classifier (`cd9da20c…`) passes:

1. **Time (escape-gate fixpoint).** The new `parameter_escapes` rewalks a receiver's whole body once
   per alias step, and it runs again for every callable reference, with no caching. A
   367-line fixture made tip hit the 15 s wall deadline (exit −9, no verdict) on both the CLI and
   module-main paths. Base finishes the same fixture in 0.12–0.14 s with the correct `observed` row.
2. **Memory (sweep recursion).** On a 2200-helper module chain, CLI path: base exits 0 at 173 MiB
   RSS. Tip exits 2 with `could_not_evaluate` / `internal MemoryError` at 307 MiB RSS, because the
   address-space cap was hit. On every chain and forwarder fixture, tip uses 1.3–2.2× base's RSS.

Both defects can be fixed without changing results. A probe copy with three small changes, kept in
my out dir and not offered as a lane candidate, removes both failures. It gives identical findings
on every fixture and still scores 12/12 on the frozen repair set.

Impacted axis: **operability** (C1's no-harm resource guard). Neither registered resource
population (round-21 scalar assignments, round-22 stored closures) contains a receiver body with an
alias chain or a sweep recursion deep enough to show either defect. So the guard "passed" because
the population could not detect them, not because the tip is free of these regressions.

## What I did

- Extracted the classifiers: `git -C <lane> show 2f1134f3…:tools/mado-tripwire.py > out/AttackPerf/tool-tip.py`
  (sha256 `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`); copied
  `evidence/tool-base-cd9da20c.py` to `out/AttackPerf/tool-base.py` (sha256 `cd9da20c…ea84`).
- Wrote inert eval-JSONL fixtures with `out/AttackPerf/gen.py`. It only writes the files and
  checks that each parses (`compile(..., PyCF_ONLY_AST)`); fixture source is never executed.
  Manifests with sha256 values: `out/AttackPerf/fixtures-manifest*.json`.
- Every scan used the unchanged round-21 scan helper
  `.ufo/waves/round-21/resource/measure.py` (sha256 `6d0362e1…7d4`). My driver `drive.py` loads
  it and calls its `run_one` (child `RLIMIT_AS` 384 MiB, 15 s wall deadline, `wait4` `ru_maxrss`),
  in both of its modes: `module-main` (loads the tool and calls `main()`) and `cli`
  (`python3 -I tool --scan`). Each driver ran under
  `prlimit --as=402653184 --cpu=15 python3 -I -B drive.py <tool> <fixture> <mode> <label>`,
  strictly sequential, one child at a time (`run-matrix.sh`, `run-probe.sh`).
- To attribute the time: `prlimit --as=402653184 --cpu=15 timeout 15 python3 -I -B profile_scan.py <tool> fixtures/unused-aliases300-calls10.jsonl 12`
  (cProfile around `main(['--scan', …])`). Output: `profile-{tip,base}-unused-aliases300-calls10.txt`.
- Built a probe correction (`probe-tip-corrected.py`, sha256 `3e8635cb…5249`), measured it the
  same way, and ran `python3 -I -B .ufo/waves/round-23/repair/measure.py --tool out/AttackPerf/probe-tip-corrected.py`
  (output `repair-probe.json`).
- Tables: `receipts/table.json`, `receipts-series/table.json`, `receipts-memory/table.json`,
  `receipts-probe/table.json`. Each row comes from one raw `run_one` receipt (`*.json`) in the same
  directory.

## Fixtures (shapes; all valid Python, all inert data)

| Fixture | Shape |
|---|---|
| `nested-defs-95x5` | 95 nested defs (near the parser's 100-indent limit), 4 sibling defs per level = 475 defs; each level calls its siblings and the next level and returns it; innermost `subprocess.run(['pacman','-Q','r23-perf-nest'])` |
| `nest-depth95-siblings20` | same with 20 siblings per level (1995 defs) |
| `forwarder-chain-400` / `fwd-length1500` / `fwd-length1900` | `fwd_i(cb, argv): return fwd_{i-1}(cb, argv)`, `fwd0` calls `cb(argv)`; module calls the top with a module `launch` callback |
| `module-helper-chain-2000` / `chain-length2200` / `chain-length2500` | `h_i()` sets a caller-local `PKG = 'r23-perf-shadow'` and calls `h_{i+1}`; the last helper reads module `PKG`. This exercises the caller-frame shadow the repair targets |
| `chain-length1000-literals4000`, `chain-length1200-literals8000` | same chain plus 4000 / 8000 module scalar globals |
| `escape-fixpoint-loop-300x60` | receiver `recv(cb, argv)` with a 300-name reverse-ordered alias chain inside a `for` loop (runs correctly: `a300` is `cb` after the loop); 60 module call sites `recv(launch, [...])` |
| `escape-fixpoint-unused-300x60`, `unused-aliases{300x70,300x90,600x20,150x240}` | receiver calls `cb(argv)` directly; the reverse alias chain sits in a nested `def unused()` that is never called |

## Results: base vs tip (exit / wall s / RSS MiB)

Exit codes are the child's: 0 = clean, 1 = findings, 2 = `could_not_evaluate`, −9 = killed at the
15 s deadline. "RecErr" means the scanner raised `RecursionError` with no verdict line. That
happens in `module-main` mode, which bypasses the scanner's `run_with_stack` wrapper (recursion
limit 1000). It happens on both tools at the same sizes, so it is not a regression.

### The three requested shapes (plus the two escape probes), `receipts/`

| Fixture | Mode | Base | Tip | Same findings? |
|---|---|---|---|---|
| nested-defs-95x5 | module-main | 1 / 0.285 / 22.6 | 1 / 0.421 / 21.8 | yes (`lead`) |
| nested-defs-95x5 | cli | 1 / 0.294 / 31.5 | 1 / 0.436 / 32.9 | yes |
| forwarder-chain-400 | module-main | 0 / 0.535 / 24.2 | 0 / 0.561 / 32.6 | yes (clean, unparsed_spawns 1) |
| forwarder-chain-400 | cli | 0 / 0.558 / 33.8 | 0 / 0.585 / 43.0 | yes |
| module-helper-chain-2000 | module-main | RecErr / 5.146 / 85.9 | RecErr / 5.159 / 116.9 | both fail |
| module-helper-chain-2000 | cli | 0 / 11.563 / **152.1** | 1 / 11.401 / **297.1** | tip better: `lead pacman -Q r23-perf-chain`, no shadow row, unparsed 0 (base: clean + unparsed 1) |
| escape-fixpoint-loop-300x60 | module-main | 1 / 0.584 / 26.5 | 1 / 0.887 / 28.8 | yes (`lead`) |
| escape-fixpoint-loop-300x60 | cli | 1 / 0.593 / 27.2 | 1 / 0.871 / 30.0 | yes |
| escape-fixpoint-unused-300x60 | module-main | 1 / **0.112** / 18.1 | 1 / **13.530** / 18.1 | yes (`observed`) |
| escape-fixpoint-unused-300x60 | cli | 1 / **0.126** / 27.9 | 1 / **13.528** / 28.5 | yes |

### Scaling series, `receipts-series/` and `receipts-memory/`

| Fixture | Mode | Base | Tip | Regression? |
|---|---|---|---|---|
| unused-aliases300-calls70 | module-main | 1 / 0.121 / 18.8 | **−9 / 15.001** / 18.5 | **YES** |
| unused-aliases300-calls70 | cli | 1 / 0.141 / 27.5 | **−9 / 15.002** / 29.8 | **YES** |
| unused-aliases300-calls90 | module-main | 1 / 0.148 / 18.5 | **−9 / 15.001** / 18.8 | **YES** |
| unused-aliases300-calls90 | cli | 1 / 0.170 / 27.8 | **−9 / 15.002** / 29.8 | **YES** |
| unused-aliases600-calls20 | module-main | 1 / 0.079 / 19.3 | **−9 / 15.001** / 18.9 | **YES** |
| unused-aliases600-calls20 | cli | 1 / 0.095 / 27.2 | **−9 / 15.002** / 29.1 | **YES** |
| unused-aliases150-calls240 | module-main | 1 / 0.231 / 19.6 | 1 / 14.175 / 19.6 | passes, 0.8 s from the cap |
| unused-aliases150-calls240 | cli | 1 / 0.249 / 28.8 | 1 / 14.032 / 30.7 | passes, 1 s from the cap |
| chain-length2200 | module-main | RecErr / 5.437 / 88.1 | RecErr / 5.852 / 115.0 | both fail |
| chain-length2200 | cli | 0 / 13.598 / 172.9 | **2 / 13.612 / 307.3, `internal MemoryError`** | **YES** |
| chain-length2500 | module-main | RecErr / 6.509 / 84.1 | RecErr / 6.755 / 116.9 | both fail |
| chain-length2500 | cli | −9 / 15.006 / 170.8 | −9 / 15.010 / 275.3 | both fail (time) |
| chain-length1000-literals4000 | cli | 0 / 2.812 / 69.3 | 1 / 2.891 / 105.8 | no (RSS 1.5×) |
| chain-length1200-literals8000 | cli | 0 / 4.023 / 88.3 | 1 / 4.126 / 130.1 | no (RSS 1.5×) |
| fwd-length1500 | module-main | RecErr / 4.303 / 59.8 | RecErr / 4.221 / 93.6 | both fail |
| fwd-length1500 | cli | 0 / 7.208 / 99.9 | 0 / 7.307 / 221.8 | no (RSS 2.2×) |
| fwd-length1900 | module-main | RecErr / 6.203 / 84.7 | RecErr / 6.386 / 115.6 | both fail |
| fwd-length1900 | cli | 0 / 12.155 / 142.0 | 0 / 12.732 / 281.8 | no (RSS 2.0×, about 100 MiB under the cap) |
| nest-depth95-siblings20 | module-main | 1 / 1.071 / 38.9 | 1 / 1.659 / 39.3 | no (1.5× time) |
| nest-depth95-siblings20 | cli | 1 / 1.094 / 48.4 | 1 / 1.667 / 49.5 | no |
| chain-length1000-literals4000 / 1200-literals8000 | module-main | RecErr | RecErr | both fail |

On every row, tip and base agree on findings where both complete. The only differences are tip's
intended improvements on the shadow chain (`lead` instead of an unparsed spawn) and in
unparsed-spawn counts on the escape fixtures.

## Counterexample 1: unbounded, uncached escape fixpoint (time)

Minimal shape (`gen.py:escape_fixpoint_unused`, shown at aliases=4, calls=2):

```python
import subprocess
def launch(argv):
    subprocess.run(argv)
def recv(cb, argv):
    def unused():
        a4 = a3
        a3 = a2
        a2 = a1
        a1 = cb
        a4()
    cb(argv)
recv(launch, ['pacman', '-Q', 'r23-perf-escape'])
recv(launch, ['pacman', '-Q', 'r23-perf-escape'])
```

Mechanism, from the code at `tool-tip.py:2471–2513` and `2970–2972`:

- `spawn_scan` calls `reference_escapes(parent, ref, …)` for every callable reference passed as an
  argument (line 2971). That calls `parameter_escapes(callee, name)` with no cache.
- `parameter_escapes` reruns `ast.walk` over the receiver's whole body, nested defs included,
  until `reaches` stops growing. Each pass adds only one alias when the chain is in reverse
  textual order. So the cost is about (alias count) × (body size) × (reference count), roughly
  \(K^2 \times M\).
- Measured: 300²×60 and 150²×240 (both \(5.4\times10^6\)) take 13.5 s and 14.0–14.2 s on tip.
  300²×70, 300²×90 and 600²×20 exceed the 15 s cap. Base runs every one of these in 0.08–0.25 s.
- Profile (`profile-tip-unused-aliases300-calls10.txt`): 20 calls to `parameter_escapes` take
  14.28 s of the 14.43 s profiled run, with 7,355,001 `ast.walk` yields and 906,010
  `source_names` calls. Base profile of the same fixture: 674,935 function calls in 0.107 s total.

The input is 367 lines (10 KB) of valid Python that runs correctly. A fixture without the nested
`unused()` def (`escape-fixpoint-loop-300x60`, where the alias loop actually runs) does not
regress, because base already pays the follow cost there: 0.59 s base vs 0.87–0.89 s tip.

## Counterexample 2: duplicate module-sized views held across sweep recursion (memory)

`chain-length2200.jsonl` (sha256 `120015e19901…`), CLI path: base exit 0 / 173 MiB; tip exit 2,
`could_not_evaluate`, `"error": "internal MemoryError"`, 307 MiB RSS.

Mechanism, from code reading of `sweep_body` (`tool-tip.py:2564–2600`) against base
`sweep_body` (`tool-base.py:2360–2387`):

- Past `DESCENT_LIMIT`, each over-depth helper is swept, and the sweep recurses through the whole
  chain on the Python stack (base does this too).
- Base copies the caller's bindings once per level (`body_bindings = dict(bindings)`) and passes
  `{}` as the env.
- Tip's `scope_view` builds a fresh merged `bindings` (and `env`) from the module view.
  `body_bindings = dict(view_bindings)` then copies it again, and both stay live in the frame for
  the whole recursive `spawn_scan`. That is about two module-sized binding dicts per level instead
  of one, plus the module literal environment base never carried.
- Tagged [INFERENCE]: I did not run an allocation trace to confirm this. The probe below supports
  it, though: removing only the second copy drops tip from 307 to 223 MiB on `chain-length2200`
  and from 282 to 188 MiB on `fwd-length1900`. The remaining gap to base (223 vs 173 MiB) is the
  module view the repair needs in order to resolve globals in their defining scope, so it is the
  repair's intended cost rather than a defect.

## Smallest safe correction (measured on a probe copy, not a lane candidate)

All three changes are in `out/AttackPerf/probe-tip-corrected.py`. Diff against `tool-tip.py`:

1. Memoize `parameter_escapes` per (receiver node, parameter). The result depends only on the
   receiver's AST, so a cache on the node (`fn.__dict__.setdefault("mado_escapes", {})`) returns
   identical answers. This removes the per-reference factor \(M\).
2. In the uncached body, walk the tree once before the fixpoint loop. Keep only the `Assign`,
   `Return` and `Call` nodes, and cache `source_names` per expression. The loop logic and its
   history-dependent `escaping` accumulation stay unchanged, so results are identical. This cuts
   the per-pass cost to the relevant nodes. The pass count is still \(K\) in the worst case.
3. In `sweep_body`, copy `view_bindings` only when `scope_view` returned the caller's own dict
   (the fallback), and drop the extra local before the recursive scan:
   `body_bindings = dict(view_bindings) if view_bindings is bindings else view_bindings; del view_bindings`.

Probe results (`receipts-probe/table.json`):

| Fixture | Mode | Tip | Probe | Base |
|---|---|---|---|---|
| unused-aliases300-calls70 | cli | −9 / 15.002 | 1 / 0.242 / 29.4 | 1 / 0.141 |
| unused-aliases300-calls90 | cli | −9 / 15.002 | 1 / 0.298 / 29.1 | 1 / 0.170 |
| unused-aliases600-calls20 | cli | −9 / 15.002 | 1 / 0.231 / 29.5 | 1 / 0.095 |
| unused-aliases150-calls240 | cli | 1 / 14.032 | 1 / 0.358 / 29.8 | 1 / 0.249 |
| escape-fixpoint-unused-300x60 | cli | 1 / 13.528 | 1 / 0.211 / 29.5 | 1 / 0.126 |
| chain-length2200 | cli | **2 MemoryError / 307.3 MiB** | 1 / 14.844 / **222.7 MiB** | 0 / 13.598 / 172.9 |
| fwd-length1900 | cli | 0 / 12.732 / 281.8 | 0 / 13.827 / 187.9 | 0 / 12.155 / 142.0 |

On the module-main path, the probe finishes every escape fixture in 0.19–0.36 s. The chain-2200
and fwd-1900 runs end in RecErr, as they do for base and tip. On every run that completes, the
probe's findings are identical to tip's across all 10 probe fixtures. Repair counter on the probe: **12/12** (`repair-probe.json`, exit 0).

Caveat: `chain-length2200` passes on the probe at 14.84 s wall, close to the 15 s cap. That time
comes from the quadratic sweep recursion that base already has (base takes 13.6 s on the same
fixture), not from the round-23 change.

## Checks not run (not passed)

On the probe copy I did not run the round-22 oracle, the round-21 oracle replay, the round-20
precision set, the eleven selftest suites, or the 1356-file corpus comparator. I also did not
rerun the registered resource populations on the tip, since other wave-2 seats own those guards.
Correction 1 is pure memoization, and correction 2 keeps the loop's evaluation order. Both should
be result-preserving by construction [INFERENCE], but the guards still need to be run before any
patch along these lines lands.

## Hygiene

- Writes were confined to `.ufo/waves/round-23/w2/out/AttackPerf/` and this report. The
  module-main children created `__pycache__` next to the tool copies in my out dir; I removed it.
  The round-21 helper directories are unchanged (their `__pycache__` mtimes are 2026-10-21).
- No jj commands. Lane git use was read-only: `show`, `status`.
- No installs or updates. Tools used: python 3.14.8 and prlimit (util-linux 2.42.4), both already
  installed.

Verdict: C1 operability **harmed** at the landed tip. Two inert fixture families make tip fail where
base passes: a 15 s timeout on `unused-aliases{300x70,300x90,600x20}` (both modes), and a
MemoryError `could_not_evaluate` on `chain-length2200` (CLI). The defect is fixable without
changing results (probe: 12/12, identical findings). It is not a tradeoff the judge has to accept.
