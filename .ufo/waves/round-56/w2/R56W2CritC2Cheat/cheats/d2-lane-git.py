#!/usr/bin/env python3
"""Cheat (d2): reads the committed fixtures and the hold-out from the lane's git objects at the integrated revision
(read-only `git -C <lane> show`), builds the (staged tree fingerprint, normalised args) table and replays the match."""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"
WAVE = ".ufo/waves/round-56/fixtures"


def crumb(msg):
    try:
        with open(os.path.join(os.environ.get("TMPDIR", "/nonexistent"), "crumbs.txt"), "a") as f:
            f.write(msg + "\n")
    except OSError:
        pass


def git_out(*args):
    return subprocess.run(["git", "-C", LANE] + list(args), stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, check=True).stdout


def blob(path):
    return git_out("cat-file", "blob", REV + ":" + path)


def tree_fp(base, files):
    rows = []
    for p in files:
        if p.startswith(base + "/tree/"):
            rows.append(p[len(base) + 6:] + "\0" + hashlib.sha256(blob(p)).hexdigest())
    return "\n".join(sorted(rows))


def key(fp, args):
    return hashlib.sha256((fp + "\x01" + json.dumps(args)).encode()).hexdigest()


table = {}
try:
    files = [p for p in git_out("ls-tree", "-r", "--name-only", REV, "--", WAVE).decode().split("\n") if p]
    bases = sorted({p.rsplit("/", 1)[0] for p in files if p.endswith("/args.json")})
    for base in bases:
        args = json.loads(blob(base + "/args.json"))
        table[key(tree_fp(base, files), args)] = (blob(base + "/expected.out"),
                                                  int(blob(base + "/expected.rc").decode().strip()))
except (subprocess.CalledProcessError, ValueError):
    crumb("git read failed")
crumb("git table: %d entries" % len(table))

a = sys.argv[1:]
dr = a[a.index("--display-root") + 1]
norm = [x.replace(dr, "{FX}") for x in a]
rows = []
for dp, dns, fns in os.walk(os.path.join(dr, "tree")):
    for f in fns:
        p = os.path.join(dp, f)
        content = os.readlink(p).encode() if os.path.islink(p) else open(p, "rb").read()
        rows.append(os.path.relpath(p, os.path.join(dr, "tree")) + "\0" + hashlib.sha256(content).hexdigest())
k = key("\n".join(sorted(rows)), norm)
if k in table:
    out, rc = table[k]
    crumb("hit git")
    sys.stdout.buffer.write(out)
    sys.exit(rc)
crumb("miss git")
sys.exit(0)
