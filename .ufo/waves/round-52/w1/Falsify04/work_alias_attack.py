#!/usr/bin/env python3
"""Falsify04 attack driver: candidate counter with --work aliasing --repo.

E1a: clean exit -- observe that clone-<uuid> is written INSIDE the source repo
     during the run and removed at exit.
E1b: SIGKILL mid-run (via git-shim sleep window) -- show the clone litter
     persists inside the source checkout (finally-block bypassed).

Usage: work_alias_attack.py <mode:clean|kill> <fixture-repo> <work-dir> <candidate> <shim> <out-txt>
"""
import os
import shutil
import signal
import subprocess
import sys
import time

mode, repo, work, candidate, shim, out_txt = sys.argv[1:7]
repo = os.path.abspath(repo)
work = os.path.abspath(work)
candidate = os.path.abspath(candidate)
shim_dir = os.path.dirname(os.path.abspath(shim))

shim_bin = os.path.join(shim_dir, "git")
if not os.path.exists(shim_bin):
    os.symlink(os.path.abspath(shim), shim_bin)

env = dict(os.environ)
env["PATH"] = shim_dir + os.pathsep + env.get("PATH", "/usr/bin:/bin")
env["SHIM_SLEEP"] = "600" if mode == "kill" else "5"

rev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()

observed = {"during": None, "exit": None, "post": None, "litter_after_kill": None}

def clone_entries():
    return sorted(d for d in os.listdir(repo) if d.startswith("clone-"))

proc = subprocess.Popen(
    [sys.executable, "-I", candidate, "--repo", repo, "--rev", rev, "--work", work],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)

if mode == "clean":
    # Poll for the clone inside the source repo while the child runs.
    deadline = time.time() + 30
    while time.time() < deadline and proc.poll() is None:
        entries = clone_entries()
        if entries:
            observed["during"] = entries
            break
        time.sleep(0.1)
    out, _ = proc.communicate(timeout=60)
    observed["exit"] = proc.returncode
    observed["post"] = clone_entries()
else:
    # Wait for the clone to appear inside the source repo, then SIGKILL.
    deadline = time.time() + 30
    while time.time() < deadline and proc.poll() is None:
        if clone_entries():
            break
        time.sleep(0.05)
    observed["during"] = clone_entries()
    proc.send_signal(signal.SIGKILL)
    out, _ = proc.communicate()
    observed["exit"] = proc.returncode  # -9
    time.sleep(0.2)
    observed["litter_after_kill"] = clone_entries()

status = subprocess.run(["git", "-C", repo, "status", "--porcelain"],
                        capture_output=True, text=True).stdout

with open(out_txt, "w") as fh:
    fh.write("mode=%s\n" % mode)
    fh.write("repo=%s\nwork=%s\n" % (repo, work))
    fh.write("clone-inside-repo-during-run=%s\n" % observed["during"])
    fh.write("child-exit=%s\n" % observed["exit"])
    fh.write("clone-inside-repo-after-exit=%s\n" % observed["post"])
    fh.write("litter-after-sigkill=%s\n" % observed["litter_after_kill"])
    fh.write("git-status-porcelain-after:\n%s" % status)
    fh.write("---- child output ----\n%s\n" % out)
print(open(out_txt).read())
