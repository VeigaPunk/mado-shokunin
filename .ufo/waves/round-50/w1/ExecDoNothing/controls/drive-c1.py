#!/usr/bin/env python3
"""ExecDoNothing / round 50 - drive the section-9 C1 controls with the FROZEN round-49 counter.

The counter scored is the committed `quality/counters/c1-r49-keysym.py` at 13631f24 (never a draft).
Each control is a committed revision of a scratch clone of the lane:

    c00-absent        BASE 03e4ae76 itself: no `tools/mado-keysym.py` (the do-nothing case)
    c02-header-only   the round-49 control's header-only tool blob at tools/mado-keysym.py
    c03-level1-only   the round-49 candidate tool with the level loop restricted to level 1

Usage: HOME/XDG_*/TMPDIR must already be set to scratch dirs. Writes one receipt per control into
../receipts/ and refuses a scratch path outside /fast/scratch/hyaku/mado-r50/ExecDoNothing.

No file outside this seat dir and the scratch clone is written; the clone is created by the caller
(setup.md) and its toplevel is asserted before the first commit.
"""
import os
import shutil
import subprocess
import sys

SEAT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the lane is derived from this seat's own path (no absolute home path in committed code):
# SEAT is .../w1/ExecDoNothing (this file lives in its controls/), five levels below it
LANE = os.path.realpath(os.path.join(SEAT, "..", "..", "..", "..", ".."))
if not os.path.isfile(os.path.join(LANE, "SKILL.md")):
    raise SystemExit("lane derivation failed: %r has no SKILL.md" % LANE)
COUNTER = os.path.join(LANE, "quality/counters/c1-r49-keysym.py")
SCRATCH = "/fast/scratch/hyaku/mado-r50/ExecDoNothing"
REPO = os.path.join(SCRATCH, "repo")
WORK = os.path.join(SCRATCH, "work")
BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
CTL = os.path.join(SEAT, "controls")
OUT = os.path.join(SEAT, "receipts")
NONCE = "5001"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(*args, check=True):
    p = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, env=ENV)
    if check and p.returncode != 0:
        raise SystemExit("git %s -> %d\n%s%s" % (args, p.returncode, p.stdout[-2000:], p.stderr[-2000:]))
    return p


def commit_tool(control, tool_src):
    top = git("rev-parse", "--show-toplevel").stdout.strip()
    if os.path.realpath(top) != os.path.realpath(REPO):
        raise SystemExit("fixture toplevel %r != %r" % (top, REPO))
    git("checkout", "-q", BASE)
    shutil.copyfile(tool_src, os.path.join(REPO, "tools/mado-keysym.py"))
    git("add", "-A")
    git("-c", "user.name=ctl", "-c", "user.email=ctl@local", "commit", "-q", "-m", "control %s" % control)
    return git("rev-parse", "HEAD").stdout.strip()


def score(name, rev):
    cmd = [sys.executable, "-I", COUNTER, "--repo", REPO, "--rev", rev, "--work", WORK,
           "--nonce", NONCE]
    p = subprocess.run(cmd, capture_output=True, text=True, env=ENV)
    body = p.stdout + p.stderr
    head = ("# ExecDoNothing round 50 - C1 control %s\n"
            "# counter: %s (sha256 %s)\n"
            "# cmd: TMPDIR=%s HOME=%s %s\n"
            "# expected: verdict=TARGET_MISSED\n"
            "# exit: %d\n\n" % (
                name, COUNTER, sha256(COUNTER), os.environ.get("TMPDIR"), os.environ.get("HOME"),
                " ".join(cmd), p.returncode))
    with open(os.path.join(OUT, "c1-%s.txt" % name), "w") as fh:
        fh.write(head + body)
    final = [l for l in body.splitlines() if l.startswith("PRED-C1-r49:")]
    print("%-16s rc=%d %s" % (name, p.returncode, final[-1] if final else "NO FINAL LINE"))
    return p.returncode, final[-1] if final else ""


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    for p in (SCRATCH, REPO, WORK):
        if not os.path.realpath(p).startswith(SCRATCH + "/") and os.path.realpath(p) != SCRATCH:
            raise SystemExit("scratch path %r is outside %s" % (p, SCRATCH))
    if SCRATCH.startswith(("/tmp", "/var/tmp", "/dev/shm")):
        raise SystemExit("refusing a scratch root under /tmp, /var/tmp or /dev/shm")
    os.makedirs(OUT, exist_ok=True)
    recs = []
    recs.append(("c00-absent", score("c00-absent", BASE)))
    for control, src in (("c02-header-only", "c02-header-only.py"),
                         ("c03-level1-only", "c03-level1-only.py"),
                         ("c11-selftest-only", "c11-selftest-only.py")):
        rev = commit_tool(control, os.path.join(CTL, src))
        recs.append((control, score(control, rev)))
    lines = ["control          rc  final line"]
    for name, (rc, final) in recs:
        lines.append("%-16s %d  %s" % (name, rc, final))
    with open(os.path.join(OUT, "c1-controls.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
