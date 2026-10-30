#!/usr/bin/env python3
"""Second triage pass: group the UNRESOLVED long tokens by value and show the shape of
each unique value plus one context line with the value itself redacted (the context
line is printed to stdout only, never to a deliverable).

Classification of a unique value:
  - HEX40 / HEX64 -> try lane git object, then any commit-ish in lane history, then
    sha256 of a file under the scanned roots, then sha1, then "UNKNOWN-HEX".
  - NONHEX -> print the token (non-hex tokens are words/identifiers, not credentials).
"""
import hashlib
import os
import re
import subprocess
import sys
from collections import defaultdict

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FIXED3 = re.compile(r"[A-Za-z0-9_\-]{32,}")
HEXONLY = re.compile(r"^[0-9a-f]+$")

ROOTS = sys.argv[1:]


def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, text=True)


files = []
for root in ROOTS:
    if os.path.isfile(root):
        files.append(root)
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for name in sorted(filenames):
            files.append(os.path.join(dirpath, name))
files = sorted(set(files))

hits = defaultdict(list)
for path in files:
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8", "replace")
    for lineno, line in enumerate(text.split("\n"), 1):
        for m in FIXED3.finditer(line):
            hits[m.group(0)].append((path, lineno, m.start()))

# known digests
git_ids = set()
out = git("cat-file", "--batch-all-objects", "--batch-check=%(objectname)")
for line in out.stdout.splitlines():
    if line.strip():
        git_ids.add(line.split()[0].lower())
out = git("rev-list", "--all")
for line in out.stdout.split():
    git_ids.add(line.lower())

local_digests = set()
for path in files:
    with open(path, "rb") as fh:
        data = fh.read()
    local_digests.add(hashlib.sha256(data).hexdigest())
    local_digests.add(hashlib.sha1(data).hexdigest())

classes = defaultdict(int)
unknown = []
nonhex = defaultdict(list)
for val, places in hits.items():
    low = val.lower()
    if not HEXONLY.match(val):
        classes["nonhex-token"] += 1
        nonhex[val].extend(places)
        continue
    if low in git_ids:
        classes["git-object-or-commit"] += 1
    elif low in local_digests:
        classes["digest-of-scanned-file"] += 1
    else:
        classes["UNKNOWN-HEX"] += 1
        unknown.append((val, places))

print("UNIQUE long tokens: %d" % len(hits))
for k in sorted(classes):
    print("  %s=%d" % (k, classes[k]))
print()
print("UNKNOWN-HEX unique values: %d" % len(unknown))
for val, places in unknown:
    p = places[0]
    print("  len=%d occurrences=%d first=%s:%d" % (len(val), len(places), p[0], p[1]))
    # context with value redacted
    with open(p[0], "rb") as fh:
        lines = fh.read().decode("utf-8", "replace").split("\n")
    ctx = lines[p[1] - 1]
    red = ctx.replace(val, "<%d-HEX>" % len(val))
    print("     ctx: " + red[:300])
print()
print("nonhex unique tokens: %d" % len(nonhex))
for val, places in sorted(nonhex.items()):
    print("  tok=%r occurrences=%d first=%s:%d" % (val, len(places), places[0][0], places[0][1]))
