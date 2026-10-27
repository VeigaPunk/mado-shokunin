#!/usr/bin/env python3
"""Falsify04: r51 counter --work==--repo observation with exact-pid polling."""
import os
import subprocess
import sys
import time

seat = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify04"
scratch = "/fast/scratch/hyaku/mado-r52/Falsify04/r51-driver"
repo = os.path.join(scratch, "repo")
out_txt = os.path.join(scratch, "r51-observe.txt")

subprocess.run(["rm", "-rf", scratch])
os.makedirs(scratch)
subprocess.run(["bash", os.path.join(seat, "build-fixture.sh"), repo],
               stdout=subprocess.DEVNULL, check=True)
rev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()

counter = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r51-ledger.py"
pid = os.fork()
if pid == 0:
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 2)
    os.execv(sys.executable, [sys.executable, "-I", counter,
                              "--repo", repo, "--rev", rev, "--work", repo])

expected = os.path.join(repo, "clone-%d" % pid)
hits = []
deadline = time.time() + 20
while time.time() < deadline:
    if os.path.isdir(expected):
        hits.append(time.time())
        break
    time.sleep(0.02)
_, status = os.waitpid(pid, 0)
during = hits[0] if hits else None
post = os.path.isdir(expected)
status_txt = subprocess.run(["git", "-C", repo, "status", "--porcelain"],
                            capture_output=True, text=True).stdout
with open(out_txt, "w") as fh:
    fh.write("r51 --work==--repo\nrepo=%s\nexpected-clone=%s\n"
             "clone-observed-during-run=%s\nclone-present-after-exit=%s\n"
             "child-exit=%d\ngit-status-porcelain-after:\n%s"
             % (repo, expected, during is not None, post,
                os.waitstatus_to_exitcode(status), status_txt))
print(open(out_txt).read())
