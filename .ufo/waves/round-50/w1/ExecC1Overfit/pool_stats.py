#!/usr/bin/env python3
"""Print the frozen C1 generator's pool sizes, so the report's table-size arithmetic is grounded.

Usage: pool_stats.py <counter.py>
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("frozen_c1", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

pairs = mod.LAYOUT_PAIRS
single = [p for p in pairs if "," not in p[0]]
print("LAYOUT_PAIRS=%d single-layout entries=%d OPTIONS=%d GEN=%d" % (
    len(pairs), len(single), len(mod.OPTIONS), mod.GEN))
print("1-pair single-layout RMLVO = %d * %d = %d" % (len(single), len(mod.OPTIONS), len(single) * len(mod.OPTIONS)))
print("2-pair RMLVO draws = %d, 3-pair = %d (before de-duplication)" % (
    len(pairs) ** 2 * len(mod.OPTIONS), len(pairs) ** 3 * len(mod.OPTIONS)))
print("NAMES=%d ABSENT=%d INVALID=%d small-pool args=%d" % (
    len(mod.NAMES), len(mod.ABSENT), len(mod.INVALID), len(set(mod.NAMES) | set(mod.ABSENT) | set(mod.INVALID))))
