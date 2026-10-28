#!/usr/bin/env python3
# Copies only the argv-named inputs of each committed C2 fixture into a clean tree (no expected.*, no args.json, no sibling fixtures).
# usage: python3 -I sandbox_export.py <exported-tree-root> <clean-dest>
import json, os, shutil, sys

src, dst = sys.argv[1], sys.argv[2]
fx = os.path.join(src, ".ufo/waves/round-55/fixtures/c2")
for n in sorted(os.listdir(fx)):
    for a in json.load(open(os.path.join(fx, n, "args.json"))):
        if a.startswith(".ufo/") and os.path.exists(os.path.join(src, a)):
            os.makedirs(os.path.dirname(os.path.join(dst, a)), exist_ok=True)
            shutil.copy(os.path.join(src, a), os.path.join(dst, a))
print("copied inputs for", len(os.listdir(fx)), "fixtures")
