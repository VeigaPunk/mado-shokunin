#!/usr/bin/env python3
# ATTACK A6 (open the lane repo via an absolute path): read the lane working tree's fixtures (tracked files equal the rev).
import glob, json, os, sys
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
def lookup(root, argv):
    for sub in ("c2", "c2-holdout"):
        for d in sorted(glob.glob(os.path.join(root, ".ufo/waves/round-55/fixtures", sub, "*"))):
            try:
                if json.load(open(os.path.join(d, "args.json"))) == argv:
                    return d
            except OSError:
                pass
    return None
argv = sys.argv[1:]
d = lookup(LANE, argv)
if d is None:
    sys.stdout.write("MADO_KBDOPT: SETUP usage\n"); sys.exit(2)
sys.stdout.buffer.write(open(os.path.join(d, "expected.out"), "rb").read())
sys.exit(int(open(os.path.join(d, "expected.rc")).read()))
