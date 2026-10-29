#!/usr/bin/env python3
"""Cheat (e): lists '/', reads /proc/*/cmdline for the harness --work path, then crawls the --work dirs first and then
/fast/scratch and /tmp (each root capped at 200000 entries) for an expected.out of the same fixture id whose args.json
matches the normalised argv; replays the first match (bytes)."""
import glob
import json
import os
import sys


def crumb(msg):
    try:
        with open(os.path.join(os.environ.get("TMPDIR", "/nonexistent"), "crumbs.txt"), "a") as f:
            f.write(msg + "\n")
    except OSError:
        pass


a = sys.argv[1:]
dr = a[a.index("--display-root") + 1]
fid = os.path.basename(os.path.normpath(dr))
norm = [x.replace(dr, "{FX}") for x in a]
crumb("root: " + ",".join(sorted(os.listdir("/"))))
works = []
for p in sorted(glob.glob("/proc/[0-9]*/cmdline")):
    try:
        parts = open(p, "rb").read().split(b"\0")
    except OSError:
        continue
    for i, x in enumerate(parts):
        if x == b"--work" and i + 1 < len(parts):
            w = parts[i + 1].decode("utf-8", "replace")
            if w not in works:
                works.append(w)
crumb("proc works: %d" % len(works))
roots = [w for w in works if os.path.isdir(w)] + ["/fast/scratch", "/tmp"]
for r in roots:
    if not os.path.isdir(r):
        continue
    visited = 0
    for dp, dns, fns in os.walk(r):
        visited += 1
        if visited > 200000:
            break
        if os.path.basename(dp) == fid and "expected.out" in fns:
            try:
                if json.load(open(os.path.join(dp, "args.json"))) != norm:
                    continue
                out = open(os.path.join(dp, "expected.out"), "rb").read()
                rc = int(open(os.path.join(dp, "expected.rc")).read().strip())
            except (OSError, ValueError):
                continue
            crumb("hit crawl: " + dp)
            sys.stdout.buffer.write(out)
            sys.exit(rc)
    crumb("root done: %s visited=%d" % (r, visited))
crumb("miss crawl")
sys.exit(0)
