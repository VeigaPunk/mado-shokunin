#!/usr/bin/env python3
"""probe-sandbox.py (seat ExecDoNothingC1): run one payload inside the frozen counter's own bwrap sandbox.

Imports quality/counters/c1-r46-devices.py read-only for its sandbox()/hidden_paths()/env_a()/make_fakebin() and
runs probe-payload.py in exactly the argv the counter uses for a fixture run, keeping the work tree so the payload's
report survives (the counter itself deletes it in a finally block).

Usage: probe-sandbox.py <an existing git repo path>   # hidden_paths() argument, e.g. a scratch clone
Prints the payload's report. Nothing in the lane is written; scratch only under /fast/scratch/hyaku/mado-r46/<seat>.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = "/fast/scratch/hyaku/mado-r46/ExecDoNothingC1"


def load_ctr():
    spec = importlib.util.spec_from_file_location("ctr", os.path.join(LANE, "quality/counters/c1-r46-devices.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    c = load_ctr()
    repo = os.path.abspath(sys.argv[1])
    work = tempfile.mkdtemp(dir=SCRATCH, prefix="probe-")
    case = tempfile.mkdtemp(dir=work, prefix="fx-")
    home = os.path.join(case, "home")
    os.makedirs(home)
    marker_dir = tempfile.mkdtemp(dir=work, prefix="mk-")
    marker = os.path.join(marker_dir, "marker")
    fakebin = os.path.join(tempfile.mkdtemp(dir=work, prefix="bin-"), "bin")
    c.make_fakebin(fakebin, marker)
    with open(os.path.join(case, "devices.json"), "wb") as f:
        f.write(b'{"keyboards": [], "mice": []}')
    with open(os.path.join(case, "c0.conf"), "w") as f:
        f.write("input {\n  kb_layout = br\n}\n")
    payload = os.path.join(work, "probe-payload.py")  # must live outside the hidden paths
    with open(os.path.join(HERE, "probe-payload.py"), "rb") as src, open(payload, "wb") as dst:
        dst.write(src.read())
    argv = ["/usr/bin/python3", "-I", payload,
            "--devices", os.path.join(case, "devices.json"), "--config", os.path.join(case, "c0.conf")]
    p = subprocess.run(c.sandbox(argv, case, c.hidden_paths(repo), marker_dir), capture_output=True,
                       env=c.env_a(home, fakebin), timeout=120)
    print("payload rc=%d stdout=%r stderr=%r" % (p.returncode, p.stdout.decode()[-200:], p.stderr.decode()[-300:]))
    print("marker present: %s" % os.path.exists(marker))
    rp = os.path.join(marker_dir, "report.txt")
    print("report %s:" % rp)
    print(open(rp).read() if os.path.exists(rp) else "MISSING")
    print("work=%s" % work)


if __name__ == "__main__":
    main()
