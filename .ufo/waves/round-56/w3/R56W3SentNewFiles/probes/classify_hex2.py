#!/usr/bin/env python3
"""Final classification of every 40/64-hex long token in the scanned surfaces.

Categories:
  lane-object    : a git object id in the lane repo (mado-shokunin) at any revision
  blob-digest    : a 64-hex token equal to the sha256/sha1 of a tracked lane blob
  labelled-digest: 64-hex token whose context names sha256/sha1/md5/blake
  UNRESOLVED     : anything else -> printed with context, value redacted
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
DIGEST_LABEL = re.compile(r"sha256|sha1|sha512|md5|blake|digest|checksum", re.I)

ROOTS = sys.argv[1:]


def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, text=True)


lane_objects = set()
for line in git("cat-file", "--batch-all-objects", "--batch-check=%(objectname)").stdout.splitlines():
    if line.strip():
        lane_objects.add(line.split()[0].lower())
for line in git("rev-list", "--all").stdout.split():
    lane_objects.add(line.lower())

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

blob_digests = set()
out = git("ls-tree", "-r", "0f3a54361a9824484d0801679ceb1fd8ac7c32e1")
for line in out.stdout.splitlines():
    meta, _, path = line.partition("\t")
    parts = meta.split()
    if len(parts) == 3:
        data = subprocess.run(["git", "-C", LANE, "cat-file", "blob", parts[2]],
                              capture_output=True).stdout
        blob_digests.add(hashlib.sha256(data).hexdigest())
        blob_digests.add(hashlib.sha1(data).hexdigest())

classes = defaultdict(set)
unresolved = []
for path in files:
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8", "replace")
    for lineno, line in enumerate(text.split("\n"), 1):
        for m in FIXED3.finditer(line):
            v = m.group(0)
            if not HEXONLY.match(v):
                continue
            low = v.lower()
            ctx = line[max(0, m.start() - 70):m.end() + 70]
            if len(v) == 40:
                if low in lane_objects:
                    classes["lane-object"].add(low)
                else:
                    classes["other-40hex"].add(low)
                    unresolved.append(("other-40hex", path, lineno, len(v), ctx))
            elif len(v) == 64:
                if low in blob_digests:
                    classes["blob-digest"].add(low)
                elif DIGEST_LABEL.search(ctx):
                    classes["labelled-digest"].add(low)
                else:
                    classes["other-64hex"].add(low)
                    unresolved.append(("other-64hex", path, lineno, len(v), ctx))
            else:
                classes["other-hexlen"].add(low)
                unresolved.append(("other-hexlen", path, lineno, len(v), ctx))

print("UNIQUE hex tokens by class:")
for k in sorted(classes):
    print("  %s=%d" % (k, len(classes[k])))
print()
print("UNRESOLVED (value redacted, context shown): %d" % len(unresolved))
seen = set()
for kind, path, lineno, ln, ctx in unresolved:
    key = (path, lineno)
    if key in seen:
        continue
    seen.add(key)
    print("  %s %s:%d len=%d ctx=%s" % (kind, path, lineno, ln, ctx[:150].replace("\n", " ")))
