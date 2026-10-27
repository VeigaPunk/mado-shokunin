#!/usr/bin/env python3
"""One-run probe of a cheat tool inside the FROZEN counter's own sandbox.

Imports the counter file (its module level is constants only) and uses its Box/Judge classes, so the mount
allowlist, env and strace set are exactly the counted ones. Prints JSON: the tool's rc/stdout/stderr, the box's
trip list, and the trace lines that answer the isolation question (library/binary lookups, ENOENT, processes).
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile


def load(path):
    spec = importlib.util.spec_from_file_location("c1r49counter", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    counter, work, tool, arg = sys.argv[1:5]
    m = load(counter)
    box = m.Box(work, tool)
    judge = m.Judge(work)
    km = judge.keymap({"layout": "us"})
    rc, out, err = box.run(km, ["how-to-type", "--keymap", "/fixture/keymap.xkb", "--disable-compose",
                                "--keysym", arg])
    trips = list(box.trips)
    fd, trace = tempfile.mkstemp(dir=work, prefix="probe-trace-")
    os.close(fd)
    argv = box.prefix(km) + ["/usr/bin/python3", "-I", "/oracle/tool.py", "how-to-type",
                             "--keymap", "/fixture/keymap.xkb", "--disable-compose", "--keysym", arg]
    trace_set = sys.argv[5] if len(sys.argv) > 5 else "openat,execve,execveat,clone,clone3,unlink,ftruncate"
    argv = [box.strace, "-f", "-qq", "-e", "trace=" + trace_set, "-e", "signal=none", "-o", trace] + argv
    p = subprocess.run(argv, capture_output=True, timeout=240, env={"PATH": "/usr/bin"})
    lines = open(trace, encoding="latin-1").read().splitlines()
    os.unlink(trace)
    keep = [ln.strip()[:200] for ln in lines
            if any(k in ln for k in ("xkbcommon", "xkbcli", "execve(", "clone", "ENOENT", "memfd"))]
    print(json.dumps({"rc": rc, "stdout": out[:400], "stderr": err[:400], "trips": trips,
                      "trace_lines": len(lines), "strace_rc": p.returncode, "filtered": keep[:40]}, indent=1))


if __name__ == "__main__":
    main()
