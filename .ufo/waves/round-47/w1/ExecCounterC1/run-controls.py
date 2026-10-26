#!/usr/bin/env python3
"""Score the C1 counter against do-nothing and cheat controls.

Every control becomes tools/mado-terminal.py in its own throwaway repository under --work (git init, toplevel
asserted before the first commit), and the counter scores that revision. A counter that lets any control reach
TARGET_MET is broken; one control that is a correct-but-delegating implementation must MISS on clause r and one that
only lies about its selftest must MISS on f/g.

Usage: run-controls.py --counter c1-r47-terminal.py --work DIR --fixtures F [--nonce N] [--good TOOL]
Prints `CTL_C1 <name> <TARGET_MET|TARGET_MISSED>` lines and a final
`CTL_C1 VERDICT: PASS|FAIL (controls scoring TARGET_MET: k of n; reference met: 0|1)`.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
MUST_MISS = ["stub", "lietest", "delegator", "subproc", "embed"]


def git(d, *args):
    p = subprocess.run(["git", "-C", d, "-c", "user.name=ctl", "-c", "user.email=ctl@example.invalid",
                        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"] + list(args),
                       capture_output=True, env=GIT_ENV)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.decode()[:400]))
    return p.stdout


def commit_tooldir(work, name, tool_path):
    d = tempfile.mkdtemp(dir=work, prefix="repo-%s-" % name)
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel").decode().strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit("fixture repo toplevel %r != %r" % (top, d))
    os.makedirs(os.path.join(d, "tools"))
    shutil.copyfile(tool_path, os.path.join(d, "tools", "mado-terminal.py"))
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "control %s" % name)
    return d


def score(counter, repo, work, fixtures, nonce, label):
    w = tempfile.mkdtemp(dir=work, prefix="score-%s-" % label)
    cmd = [sys.executable, counter, "--repo", repo, "--rev", "HEAD", "--work", w,
           "--fixtures", fixtures, "--nonce", str(nonce)]
    p = subprocess.run(cmd, capture_output=True, timeout=3600)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    print(out, end="" if out.endswith("\n") else "\n")
    verdict = "NO_VERDICT"
    for line in out.splitlines():
        if line.startswith("PRED-C1-r47: "):
            for part in line.split():
                if part.startswith("verdict="):
                    verdict = part.split("=", 1)[1]
    return verdict, out, p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--nonce", type=int, default=47)
    ap.add_argument("--good", default=None, help="optional candidate expected to reach TARGET_MET")
    ap.add_argument("--controls", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "controls"))
    ap.add_argument("--receipts", default=None)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    if a.receipts:
        os.makedirs(a.receipts, exist_ok=True)
    names = list(MUST_MISS)
    if a.good:
        names.append("good")
    met = 0
    ref_met = 0
    for name in names:
        path = a.good if name == "good" else os.path.join(a.controls, "%s-tool.py" % name)
        repo = commit_tooldir(a.work, name, path)
        verdict, out, rc = score(a.counter, repo, a.work, a.fixtures, a.nonce, name)
        if a.receipts:
            with open(os.path.join(a.receipts, "ctl-c1-%s.txt" % name), "w") as f:
                f.write("control=%s exit=%d verdict=%s\n" % (name, rc, verdict))
                f.write(out)
        print("CTL_C1 %s %s" % (name, verdict))
        if verdict == "TARGET_MET":
            met += 1
            if name == "good":
                ref_met = 1
    ok = met == ref_met and ref_met == (1 if a.good else 0)
    print("CTL_C1 VERDICT: %s (controls scoring TARGET_MET: %d of %d; reference met: %d)"
          % ("PASS" if ok else "FAIL", met, len(names), ref_met))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
