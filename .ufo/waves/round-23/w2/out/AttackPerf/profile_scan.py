#!/usr/bin/env python3
"""cProfile one scanner main(['--scan', FIXTURE]) in-process (module-main path).

Run under the same caps as the harness: prlimit --as=402653184 --cpu=15 and
timeout 15. Never executes fixture source; the scanner only parses it.
"""
from __future__ import annotations

import cProfile
import contextlib
import importlib.util
import io
import pstats
import sys

sys.dont_write_bytecode = True
tool, fixture, top = sys.argv[1], sys.argv[2], int(sys.argv[3])
spec = importlib.util.spec_from_file_location("_mado_attackperf_target", tool)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
profiler = cProfile.Profile()
with contextlib.redirect_stdout(io.StringIO()):
    profiler.runcall(module.main, ["--scan", fixture])
stats = pstats.Stats(profiler)
stats.sort_stats("tottime").print_stats(top)
stats.print_callers("parameter_escapes|reference_escapes")
