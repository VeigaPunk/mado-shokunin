#!/usr/bin/env python3
"""N42 evidence: the reference enforces the 30 s live bound (SETUP
journalctl_failed, exit 5); the `timeout=None` mutant does not.

A stub that sleeps 33 s is the journalctl program. The reference must return
exit 5 at ~30 s; the mutant, wrapped in `timeout 32`, must still be running at
32 s (rc 124). Read-only outside a mktemp dir.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

SEAT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.abspath(os.path.join(SEAT, "..", "..", "c1", "ctl-ref-tool.py.txt"))
MUT = os.path.join(SEAT, "mutants", "N42-live-no-timeout.py")


def main():
    d = tempfile.mkdtemp(prefix="n42-")
    try:
        stub = os.path.join(d, "slowjournalctl")
        with open(stub, "w") as fh:
            fh.write("#!/bin/sh\nsleep 33\n")
        os.chmod(stub, 0o755)
        t0 = time.time()
        r = subprocess.run([sys.executable, "-I", REF, "--live",
                            "--journalctl", stub], capture_output=True,
                           text=True, timeout=120)
        rt = time.time() - t0
        print("REF   rc=%d %.1fs stdout=%r" % (r.returncode, rt,
                                               r.stdout.strip()))
        t0 = time.time()
        m = subprocess.run(["timeout", "32", sys.executable, "-I", MUT,
                            "--live", "--journalctl", stub],
                           capture_output=True, text=True, timeout=120)
        mt = time.time() - t0
        print("MUTANT rc=%d %.1fs stdout=%r (124 = still running at the 32 s "
              "bound)" % (m.returncode, mt, m.stdout.strip()))
        ok = r.returncode == 5 and r.stdout.strip() == \
            "MADO_GLOBALS: SETUP journalctl_failed" and m.returncode == 124
        print("N42 killed_by_a_hanging_stub=%d" % ok)
        return 0 if ok else 1
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
