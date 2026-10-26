#!/usr/bin/env python3
"""Classify C2 guard mutations: are they reachable (output-changing) or dead?"""
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CTR = LANE + "/quality/counters/c2-r45-monitor-entry.py"
BUILD = LANE + "/.ufo/waves/round-45/l1-draft/build-pos.py"
FREEZE = "22a8dedd02f507689c567777e0f20b5e645c8ce0"
BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
SCR = "/fast/scratch/hyaku/mado-r45/SimpContract"
ENVG = dict(os.environ)
for k in list(ENVG):
    if k.startswith("GIT_"):
        del ENVG[k]


def sh(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, env=ENVG, **kw)


def clone(tag):
    d = os.path.join(SCR, "c2g-" + tag)
    sh("rm", "-rf", d)
    sh("git", "clone", "-q", "--shared", "--no-checkout", LANE, d)
    assert sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.strip() == d
    sh("git", "-C", d, "checkout", "-q", "--detach", FREEZE)
    sh(sys.executable, "-I", BUILD, d)
    commit(d, "pos " + tag)
    return d


def commit(d, msg):
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid", "commit", "-q", "-m", msg)


def run(path, d, rev="HEAD"):
    p = sh(sys.executable, "-I", path, "--repo", d, "--rev", rev, "--base", BASE)
    return p.returncode, p.stdout, p.stderr


def summary(t, r):
    rc, out, err = r
    last = out.strip().splitlines()[-1] if out.strip() else "<no stdout>"
    return "%s rc=%d last=%r err=%r" % (t, rc, last[:90], err.strip().splitlines()[-1][:80] if err.strip() else "")


# --- damaged GATE (S306 = Monitor.cpp) -------------------------------------
d = clone("gate")
lesson = os.path.join(d, "corpus/lessons/round-45.md")
text = open(lesson).read()
lines = [l for l in text.splitlines(keepends=True) if not re.match(r"^GATE S306 ", l)]
open(lesson, "w").write("".join(lines))
commit(d, "drop monitor gate")
print(summary("gate-dropped  baseline", run(CTR, d)))
print(summary("gate-dropped  C8-mutant", run(os.path.join(SCR, "ctr-C8-h-len-guard.py"), d)))

# --- damaged registry row (S302) ------------------------------------------
d2 = clone("row")
reg = os.path.join(d2, "corpus/SOURCES.md")
text = open(reg).read()
lines = [l for l in text.splitlines(keepends=True) if not re.match(r"^ {0,3}\|\s*S302\s*\|", l)]
open(reg, "w").write("".join(lines))
commit(d2, "drop S302 row")
print(summary("row-dropped   baseline", run(CTR, d2)))
print(summary("row-dropped   C6-mutant", run(os.path.join(SCR, "ctr-C6-i-rows-guard.py"), d2)))

# --- entry absent at REV (C7) ---------------------------------------------
d3 = clone("base")
print(summary("entry-absent  baseline", run(CTR, d3, rev=BASE)))
print(summary("entry-absent  C7-mutant", run(os.path.join(SCR, "ctr-C7-j-raw-none.py"), d3, rev=BASE)))
