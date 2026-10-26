#!/usr/bin/env python3
"""Score one tool text against the frozen PRED-C1-r45 counter, in a scratch clone of the lane at BASE."""
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
COUNTER = os.path.join(LANE, "quality/counters/c1-r45-monitors.py")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, env=ENV, check=True).stdout


def build(work, name, text):
    d = tempfile.mkdtemp(dir=work, prefix=name + "-")
    git(work, "clone", "-q", "--shared", "--no-checkout", LANE, d)
    top = git(d, "rev-parse", "--show-toplevel").decode().strip()
    if top != os.path.realpath(d):
        raise SystemExit("toplevel mismatch %s != %s" % (top, d))
    git(d, "checkout", "-q", "--detach", BASE)
    if text is not None:
        os.makedirs(os.path.join(d, "tools"), exist_ok=True)
        with open(os.path.join(d, "tools", "mado-monitors.py"), "w") as f:
            f.write(text)
        git(d, "add", "tools/mado-monitors.py")
        git(d, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid",
            "commit", "-q", "-m", name)
    return d


def score(repo, work, seed=None):
    w = tempfile.mkdtemp(dir=work, prefix="w-")
    cmd = [sys.executable, "-I", COUNTER, "--repo", repo, "--rev", "HEAD", "--work", w]
    if seed is not None:
        cmd += ["--seed", str(seed)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout


def main():
    name, src = sys.argv[1], sys.argv[2]
    seeds = [int(x) for x in sys.argv[3:]] or [None]
    work = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(__file__)), prefix="h-")
    text = open(src).read()
    repo = build(work, name, text)
    for seed in seeds:
        rc, out = score(repo, work, seed)
        print("### %s seed=%s rc=%d" % (name, seed, rc))
        print(out.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
