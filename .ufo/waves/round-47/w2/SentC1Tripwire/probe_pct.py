#!/usr/bin/env python3
"""Same clause r, but with strace's %process class instead of the counter's fixed list."""
import importlib.util, os, sys, tempfile
CT = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r47-terminal.py"
spec = importlib.util.spec_from_file_location("c1r47", CT)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.TRACE_SET = os.environ.get("PCT_TRACE", "trace=%process,socket")
work = tempfile.mkdtemp(dir=sys.argv[1], prefix="pct-")
root = tempfile.mkdtemp(dir=work, prefix="st-"); os.makedirs(os.path.join(root, ".rw"))
box = mod.Box(work, os.path.abspath(sys.argv[2]))
args = sys.argv[3:] or ["--selftest"]
rc, out = box.run(root, {"PATH": "/oracle/bin", "HOME": "/tmp", "TMPDIR": "/tmp", "LANG": "C.UTF-8"}, True, args, timeout=60)
print("TRACE_SET=%s rc=%d trips=%d" % (mod.TRACE_SET, rc, len(box.trips)))
for t in box.trips[:6]:
    print("  TRIP: %s" % t)
