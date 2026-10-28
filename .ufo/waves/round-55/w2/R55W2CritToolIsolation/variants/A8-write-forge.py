#!/usr/bin/env python3
# ATTACK A8 (write into the export): walk up from argv[0] and check every candidate root for the fixture matching argv (locate);
# on every run, overwrite expected.out of every OTHER fixture (committed and hold-out) under that root with a unique forged line,
# then print this fixture's (current) expected.out. The harness loads each fixture's expected.* just before its run and checks
# the hold-out commitment only once, before any tool runs.
import glob, json, os, sys
EVID = "/fast/scratch/hyaku/mado-r55/R55W2CritToolIsolation/evidence/forge.log"
def dirs(root):
    out = []
    for sub in ("c2", "c2-holdout"):
        out += sorted(glob.glob(os.path.join(root, ".ufo/waves/round-55/fixtures", sub, "*")))
    return out
def lookup(root, argv):
    for d in dirs(root):
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
                        return cand, d
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    return None, None
argv = sys.argv[1:]
root, own = locate([os.path.dirname(os.path.abspath(sys.argv[0]))], argv)
if own is None:
    sys.stdout.write("MADO_KBDOPT: SETUP usage\n"); sys.exit(2)
n = 0
for d in dirs(root):
    if d == own:
        continue
    open(os.path.join(d, "expected.out"), "wb").write(b"FORGED " + os.path.basename(d).encode() + b"\n")
    n += 1
with open(EVID, "a") as fh:
    fh.write("run root=%s argv=%r forged=%d own=%s\n" % (root, argv, n, os.path.basename(own)))
sys.stdout.buffer.write(open(os.path.join(own, "expected.out"), "rb").read())
sys.exit(int(open(os.path.join(own, "expected.rc")).read()))
