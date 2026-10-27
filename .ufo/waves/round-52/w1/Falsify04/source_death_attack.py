#!/usr/bin/env python3
"""Falsify04 attack driver 2: delete the source repo mid-run.

The candidate's scratch clone is made with `git clone --shared`, so every
`git show` read goes through .git/objects/info/alternates into the SOURCE repo's
object store. This driver waits for the clone to appear, deletes the source
repo, then lets the candidate resume its first `git show`.

Usage: source_death_attack.py <fixture-repo> <work-dir> <candidate> <shim> <out-txt>
"""
import os
import shutil
import signal
import subprocess
import sys
import time

repo, work, candidate, shim, out_txt = [os.path.abspath(p) for p in sys.argv[1:6]]
shim_dir = os.path.dirname(shim)
shim_bin = os.path.join(shim_dir, "git")
if not os.path.exists(shim_bin):
    os.symlink(shim, shim_bin)

env = dict(os.environ)
env["PATH"] = shim_dir + os.pathsep + env.get("PATH", "/usr/bin:/bin")
env["SHIM_SLEEP"] = "600"

rev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()

proc = subprocess.Popen(
    [sys.executable, "-I", candidate, "--repo", repo, "--rev", rev, "--work", work],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)

clone_dir = None
deadline = time.time() + 30
while time.time() < deadline and proc.poll() is None:
    if os.path.isdir(work):
        for d in os.listdir(work):
            if d.startswith("clone-"):
                clone_dir = os.path.join(work, d)
                break
    if clone_dir:
        break
    time.sleep(0.05)

events = ["clone-dir=%s" % clone_dir]
if clone_dir and os.path.isfile(os.path.join(clone_dir, ".git/objects/info/alternates")):
    with open(os.path.join(clone_dir, ".git/objects/info/alternates")) as fh:
        events.append("alternates=%s" % fh.read().strip())

if clone_dir:
    shutil.rmtree(repo)  # source repo dies mid-run
    events.append("source-repo-removed=mid-run")

out, _ = proc.communicate(timeout=90)
events.append("child-exit=%s" % proc.returncode)
with open(out_txt, "w") as fh:
    fh.write("\n".join(events) + "\n---- child output ----\n" + out + "\n")
print(open(out_txt).read())
