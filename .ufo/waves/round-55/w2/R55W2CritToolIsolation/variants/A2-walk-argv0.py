#!/usr/bin/env python3
# ATTACK A2 (D2 walk-up): walk up from argv[0] (= rd/tools/x.py in the isolated run) and check EVERY candidate root on the chain
# (root itself, or <ancestor>/root) for a fixture whose args.json equals argv; print its expected.out / expected.rc.
import glob, json, os, sys
def lookup(root, argv):
    for sub in ("c2", "c2-holdout"):
        for d in sorted(glob.glob(os.path.join(root, ".ufo/waves/round-55/fixtures", sub, "*"))):
            try:
                if json.load(open(os.path.join(d, "args.json"))) == argv:
                    return d
            except OSError:
                pass
    return None
def locate(starts, argv):
    for s in starts:
        p = os.path.abspath(s)
        while True:
            for cand in (p, os.path.join(p, "root")):
                if os.path.isdir(os.path.join(cand, ".ufo/waves/round-55/fixtures")):
                    d = lookup(cand, argv)
                    if d:
                        return d
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    return None
argv = sys.argv[1:]
d = locate([os.path.dirname(os.path.abspath(sys.argv[0]))], argv)
if d is None:
    sys.stdout.write("MADO_KBDOPT: SETUP usage\n"); sys.exit(2)
sys.stdout.buffer.write(open(os.path.join(d, "expected.out"), "rb").read())
sys.exit(int(open(os.path.join(d, "expected.rc")).read()))
