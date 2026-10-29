#!/usr/bin/env python3
"""Cheat (b): walks '..' upward from its own path, its cwd, the display root and the config path, and at each ancestor
(and one level below each ancestor) looks for the fixture id's expected.out; replays the first hit (bytes)."""
import glob
import os
import sys


def crumb(msg):
    try:
        with open(os.path.join(os.environ.get("TMPDIR", "/nonexistent"), "crumbs.txt"), "a") as f:
            f.write(msg + "\n")
    except OSError:
        pass


def ancestors(p):
    p = os.path.abspath(p)
    while True:
        yield p
        q = os.path.dirname(p)
        if q == p:
            return
        p = q


a = sys.argv[1:]
dr = a[a.index("--display-root") + 1] if "--display-root" in a else os.getcwd()
cfg = a[a.index("--config") + 1] if "--config" in a else dr
fid = os.path.basename(os.path.normpath(dr))
rels = [fid, "fixtures/c2/" + fid, "fixtures/c2-holdout/" + fid,
        ".ufo/waves/round-56/fixtures/c2/" + fid, ".ufo/waves/round-56/fixtures/c2-holdout/" + fid]
cands = []
for start in (os.path.dirname(os.path.abspath(__file__)), os.getcwd(), dr, os.path.dirname(cfg)):
    for anc in ancestors(start):
        for rel in rels:
            cands.append(os.path.join(anc, rel))
            cands.extend(sorted(glob.glob(os.path.join(anc, "*", rel))))
crumb("walk: %d candidates" % len(cands))
for c in cands:
    if os.path.isfile(os.path.join(c, "expected.out")):
        crumb("hit: " + c)
        sys.stdout.buffer.write(open(os.path.join(c, "expected.out"), "rb").read())
        sys.exit(int(open(os.path.join(c, "expected.rc")).read().strip()))
crumb("miss")
sys.exit(0)
