#!/usr/bin/env python3
"""Robustness sweep: do malformed/unknown options and models ever fail to compile (vs layout/variant/rules)?
Plus a per-compile microbenchmark, so the cost figure is measured, not divided out of interpreter startup."""
import sys, time
sys.path.insert(0, ".")
from importlib import import_module
p = import_module("xkb-probe")

OPTIONS = ["notanoption:x", "foo", "grp:", ":", "a:b:c", "compose:caps,grp:", "ctrl:nocaps,foo:bar",
           "grp:alts_toggle", "compose:caps", "", "grp:alts_toggle,grp:shift_toggle"]
MODELS = ["zzz", "pc105", "pc10", "PC105", "", "evdev"]

print("SWEEP: options (layout=br, defaults elsewhere)")
for o in OPTIONS:
    r = p.compile_names("", "", "br", "", o)
    print(f"SWEEP: options={o!r:38s} compile={'yes' if r is not None else 'NO'} names={r}")
print("SWEEP: models (layout=br, defaults elsewhere)")
for m in MODELS:
    r = p.compile_names("", m, "br", "", "")
    print(f"SWEEP: model={m!r:10s} compile={'yes' if r is not None else 'NO'} names={r}")

# microbenchmark: 200 in-process compiles of the host names
N = 200
t = time.perf_counter()
for _ in range(N):
    p.compile_names("", "", "br", "", "compose:caps")
dt = time.perf_counter() - t
print(f"SWEEP: microbench compiles={N} total_s={dt:.3f} ms_per_compile={1000*dt/N:.2f}")
print(f"SWEEP: options_failing={sum(1 for o in OPTIONS if p.compile_names('', '', 'br', '', o) is None)}/{len(OPTIONS)} "
      f"models_failing={sum(1 for m in MODELS if p.compile_names('', m, 'br', '', '') is None)}/{len(MODELS)}")
