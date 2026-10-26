#!/usr/bin/env python3
"""Read-only probe: run the superseded v1 counter's own fixtures at the data rev and log,
per fixture, the tool's rc + final stdout line and the v1 model's expected rc + final line.
Only writes under the given --work scratch; the lane is read-only (git show).
"""
import importlib.util
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
V1 = os.path.join(LANE, "quality/counters/c1-r44-geometry-states.py")
REV = "e46789213830597348fe96a351ae004d10587385"

spec = importlib.util.spec_from_file_location("c1v1", V1)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
old = m.old

LOG = []
_orig_exec = old.execute
_orig_judge = old.judge


def execute(tool, d, argv, stdin=None, timeout=30):
    rc, out, err = _orig_exec(tool, d, argv, stdin, timeout) if timeout != 30 else _orig_exec(tool, d, argv, stdin)
    LOG.append({"fixture": os.path.basename(str(d)), "rc": rc,
                "last": out.decode("utf-8", "replace").strip().splitlines()[-1] if out else ""})
    return rc, out, err


def judge(rc, out, err, want_out, want_rc):
    ok, why = _orig_judge(rc, out, err, want_out, want_rc)
    notice = LOG[-1] if LOG else {}
    notice["ok"] = ok
    notice["why"] = why
    notice["want_rc"] = want_rc
    notice["want_last"] = want_out.strip().splitlines()[-1] if want_out else ""
    return ok, why


old.execute = execute
old.judge = judge

sys.argv = ["c1-r44-geometry-states.py", "--repo", LANE, "--rev", REV,
            "--work", sys.argv[1], "--nonce", sys.argv[2]]
rc = 1
try:
    rc = m.main()
except SystemExit as exc:
    rc = exc.code

for e in LOG:
    print("PROBE fixture=%-10s ok=%s tool_rc=%-4s want_rc=%-4s"
          % (e["fixture"], e["ok"], e["rc"], e.get("want_rc")))
    print("  tool: %s" % e["last"])
    print("  want: %s" % e.get("want_last"))
    if not e["ok"]:
        print("  why:  %s" % e["why"])
print("PROBE counter_main_rc=%s" % rc)
sys.exit(0)
