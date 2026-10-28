#!/usr/bin/env python3
# Mimics the frozen harness fixture loop: cwd = exported tree, argv from args.json, byte compare of stdout and rc.
import json, os, subprocess, sys
tree, tool, fixroot = sys.argv[1], sys.argv[2], sys.argv[3]
ok = 0; names = sorted(os.listdir(fixroot)); res = []
for n in names:
    d = os.path.join(fixroot, n)
    args = json.load(open(os.path.join(d, "args.json")))
    p = subprocess.run([sys.executable, "-I", tool] + args, cwd=tree, capture_output=True)
    exp = open(os.path.join(d, "expected.out"), "rb").read()
    rc = int(open(os.path.join(d, "expected.rc")).read())
    good = p.stdout == exp and p.returncode == rc
    ok += good; res.append(f"{n}:{'ok' if good else 'FAIL'}")
print(" ".join(res)); print(f"fixtures={ok}/{len(names)}")
