#!/usr/bin/env python3
"""Probe: is C6 (FIFO named *.desktop listed as a candidate) a genuine blocking read, not slowness?

Runs the pinned resolver under strace on the same case tree the driver builds, with a 3 s cap, and reports the last
openat/syscall events. Nothing writes to the FIFO.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
sys.path.insert(0, os.path.join(LANE, ".ufo/waves/round-48/w1/ExecHomeUnset"))
import run as R  # noqa: E402  (the driver: fixtures, env, materialize)

SCRATCH = "/fast/scratch/hyaku/mado-r48/ExecHomeUnset"


def main():
    mod = R.load_counter()
    work = tempfile.mkdtemp(dir=SCRATCH, prefix="probe-")
    box = mod.Box(work, tool_path=R.TOOL)
    case = [c for c in R.CASES if c["id"] == "C6-fifo-later-dir-listed"][0]
    root = os.path.join(work, "r")
    os.makedirs(root)
    R.materialize(root, case)
    env = R.case_env(case, root)
    trace = os.path.join(work, "trace-fifo")
    argv = [box.strace, "-f", "-tt", "-e", "trace=openat,read,newfstatat", "-o", trace] + box.argv(root, env, False, case["args"])
    try:
        p = subprocess.run(argv, capture_output=True, timeout=3, env={"PATH": "/usr/bin"})
        rc = p.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    lines = open(trace, encoding="latin-1").read().splitlines()
    fifo = [i for i, ln in enumerate(lines) if "foot.desktop" in ln]
    print("rc", rc, "trace_lines", len(lines))
    for i in (fifo[-1] if fifo else len(lines) - 1,):
        for ln in lines[max(0, i - 2):]:
            print("  ", ln.replace(root, "$ROOT")[:180])
    open(os.path.join(R.SEAT, "fifo-block.txt"), "w").write(
        "rc=%s trace_lines=%d\n%s\n" % (rc, len(lines),
                                       "\n".join(ln.replace(root, "$ROOT") for ln in lines[max(0, (fifo[-1] if fifo else len(lines) - 1) - 2):])))
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
