#!/usr/bin/env python3
"""Repro 2 (round 47 w2, ExecC1Determinism): generated case g012 of nonce 4242 (clause g) is
readdir-order sensitive: the live pin prints a different command line on xfs and on tmpfs.
The frozen 190-fixture set has no such case (see repro-fixture-rebuild.sh: tmpfs rebuild is byte-identical).

usage: repro-g012.py <xfs-base> <tmpfs-base>
Writes only under the two bases."""
import importlib.util
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r47-terminal.py")
PIN = os.path.join(sys.argv[1], "pin") if len(sys.argv) > 2 else ""

spec = importlib.util.spec_from_file_location("c1r47", COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def main():
    x, t = sys.argv[1], sys.argv[2]
    import random
    g = random.Random(4242 ^ 0x47C1)
    case = None
    for k in range(150):
        c = m.gen_case(g, k)
        if c["id"] == "g012":
            case = c
    print("case", case["id"], "args", case["args"], "exec", case["exec"])
    for base in (os.path.join(x, "g012"), os.path.join(t, "g012")):
        root = os.path.join(base, "r")
        import shutil
        shutil.rmtree(base, ignore_errors=True)
        os.makedirs(root)
        m.materialize(root, case)
        env = m.case_env(case, root, "C.UTF-8")
        env["PATH"] = os.path.join(root, "bin") + ":/usr/bin:/bin"
        env["XDG_CACHE_HOME"] = os.path.join(root, ".rw", "cache")
        out = []
        for args in (case["args"], ["--print-id"]):
            p = subprocess.run([PIN] + args, env=env, capture_output=True, text=True, timeout=30)
            out.append((args, p.returncode, p.stdout.replace(root, "$ROOT")))
        fstype = subprocess.run(["stat", "-f", "-c", "%T", base], capture_output=True, text=True).stdout.strip()
        print("==", base, "fstype=" + fstype)
        for args, rc, so in out:
            print("  argv=%r rc=%d stdout=%r" % (args, rc, so))
    return 0


if __name__ == "__main__":
    sys.exit(main())
