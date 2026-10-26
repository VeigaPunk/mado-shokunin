#!/usr/bin/env python3
"""Run ONLY C2 control P (real scorer) — mirror of run-c2-controls.py main()
for kind == "real" (control=P-real). Uses the frozen counter as-is.
"""
import importlib.util
import os
import sys

SPEC = importlib.util.spec_from_file_location(
    "run_c2_controls",
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/ctl/run-c2-controls.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

base = M.base_files()
G = M.admitted()
rc, last, cls = M.score(base, G, "real")
print("control=P-real expected=admitted=1/1 observed=%s clauses=%s ok=%d" % (
    last.split(": ", 1)[-1].split(" rev=")[0], cls, rc == 0 and "admitted=1/1" in last))
print("exit=%d" % rc)
sys.exit(0 if rc == 0 else 1)
