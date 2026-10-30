#!/usr/bin/env python3
"""R56W3MutBwrapChannels probe -- what the tool can see inside the harness' sandbox."""
import os
import sys


def walk(root, depth=0, maxdepth=2):
    try:
        names = sorted(os.listdir(root))
    except OSError as e:
        return ["%s! errno=%s" % (root, e.errno)]
    if depth >= maxdepth:
        return ["%s/ -> %s" % (root, " ".join(names[:14]))]
    out = []
    for n in names:
        out += walk(os.path.join(root, n), depth + 1, maxdepth)
    return out


print("=== ENV ===")
for k in sorted(os.environ):
    print("ENV %s=%r" % (k, os.environ[k]))
print("=== CWD ===")
print("cwd=%s" % os.getcwd())
print("=== ROOTS ===")
for p in ("/", "/usr", "/home", "/tmp", "/fast", "/proc", "/dev", "/w"):
    print("%s exists=%s" % (p, os.path.exists(p)))
print("=== WALK / depth2 ===")
for l in walk("/", 0, 2):
    print(l)
print("=== CWD ANCESTORS ===")
cur = os.path.abspath(os.getcwd())
while True:
    try:
        names = sorted(os.listdir(cur))
    except OSError as e:
        names = ["!errno=%s" % e.errno]
    print("%s -> %s" % (cur, " ".join(names[:16])))
    nxt = os.path.dirname(cur)
    if nxt == cur:
        break
    cur = nxt
print("=== ARGV ===")
print(repr(sys.argv))
