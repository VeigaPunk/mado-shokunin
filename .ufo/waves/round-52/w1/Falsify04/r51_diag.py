#!/usr/bin/env python3
"""Diagnostic: observe r51 --work==--repo with full timeline."""
import os
import subprocess
import sys
import time

seat = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify04"
scratch = "/fast/scratch/hyaku/mado-r52/Falsify04/r51-diag"
repo = os.path.join(scratch, "repo")
subprocess.run(["rm", "-rf", scratch])
os.makedirs(scratch)
subprocess.run(["bash", os.path.join(seat, "build-fixture.sh"), repo],
               stdout=subprocess.DEVNULL, check=True)
rev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()
counter = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r51-ledger.py"
t0 = time.time()
pid = os.fork()
if pid == 0:
    os.execv(sys.executable, [sys.executable, "-I", counter,
                              "--repo", repo, "--rev", rev, "--work", repo])
timeline = []
deadline = t0 + 15
while time.time() < deadline:
    now = time.time() - t0
    try:
        entries = sorted(d for d in os.listdir(repo) if d.startswith("clone-"))
    except FileNotFoundError:
        entries = ["<repo-missing>"]
    alive = os.path.exists("/proc/%d" % pid)
    if entries or not alive:
        timeline.append((round(now, 3), alive, entries))
        if not alive and not entries:
            break
    time.sleep(0.01)
_, status = os.waitpid(pid, 0)
print("child pid=%d exit=%d" % (pid, os.waitstatus_to_exitcode(status)))
for row in timeline[:20]:
    print(row)
