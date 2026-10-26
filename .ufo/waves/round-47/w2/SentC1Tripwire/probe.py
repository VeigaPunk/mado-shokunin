#!/usr/bin/env python3
"""Reproduce clause r of quality/counters/c1-r47-terminal.py exactly, using the counter's own Box.

usage: probe.py <scratch-work-dir> <tool.py> [attack-arg...]
Runs the tool once in the counter's selftest configuration (same argv, same strace set, same check_trace).
"""
import importlib.util, os, sys, tempfile

CT = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r47-terminal.py"
spec = importlib.util.spec_from_file_location("c1r47", CT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

work = tempfile.mkdtemp(dir=sys.argv[1], prefix="probe-")
root = tempfile.mkdtemp(dir=work, prefix="st-")
os.makedirs(os.path.join(root, ".rw"))
box = mod.Box(work, os.path.abspath(sys.argv[2]))
args = sys.argv[3:] or ["--selftest"]
rc, out = box.run(root, {"PATH": "/oracle/bin", "HOME": "/tmp", "TMPDIR": "/tmp", "LANG": "C.UTF-8"}, True, args,
                  timeout=60)
print("rc=%d trips=%d out=%r" % (rc, len(box.trips), out[-200:]))
for t in box.trips:
    print("  TRIP: %s" % t)
for name in sorted(os.listdir(os.path.join(root, ".rw"))):
    p = os.path.join(root, ".rw", name)
    try:
        print("  MARKER %s = %r" % (name, open(p, "rb").read(300)))
    except OSError:
        print("  MARKER %s (dir)" % name)
