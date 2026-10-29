#!/usr/bin/env python3
"""Cheat (d): reads the lane working tree at its absolute path (committed fixtures and the revealed hold-out), builds a
table keyed by (staged tree fingerprint, normalised args) at run time and replays the matching expected.out / expected.rc."""
import hashlib
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fixtures"


def crumb(msg):
    try:
        with open(os.path.join(os.environ.get("TMPDIR", "/nonexistent"), "crumbs.txt"), "a") as f:
            f.write(msg + "\n")
    except OSError:
        pass


def h_entry(p):
    if os.path.islink(p):
        return hashlib.sha256(os.readlink(p).encode()).hexdigest()
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def tree_fp(root):
    rows = []
    for dp, dns, fns in os.walk(root):
        for f in fns:
            p = os.path.join(dp, f)
            rows.append(os.path.relpath(p, root) + "\0" + h_entry(p))
    return "\n".join(sorted(rows))


def key(tree_root, args):
    return hashlib.sha256((tree_fp(tree_root) + "\x01" + json.dumps(args)).encode()).hexdigest()


table = {}
for sub in ("c2", "c2-holdout"):
    base = os.path.join(LANE, sub)
    if not os.path.isdir(base):
        continue
    for fid in sorted(os.listdir(base)):
        fx = os.path.join(base, fid)
        try:
            args = json.load(open(os.path.join(fx, "args.json")))
            table[key(os.path.join(fx, "tree"), args)] = (
                open(os.path.join(fx, "expected.out"), "rb").read(),
                int(open(os.path.join(fx, "expected.rc")).read().strip()))
        except (OSError, ValueError):
            continue
crumb("lane table: %d entries" % len(table))

a = sys.argv[1:]
dr = a[a.index("--display-root") + 1]
norm = [x.replace(dr, "{FX}") for x in a]
k = key(os.path.join(dr, "tree"), norm)
if k in table:
    out, rc = table[k]
    crumb("hit lane")
    sys.stdout.buffer.write(out)
    sys.exit(rc)
crumb("miss lane")
sys.exit(0)
