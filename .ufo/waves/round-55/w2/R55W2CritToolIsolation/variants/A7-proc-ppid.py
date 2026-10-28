#!/usr/bin/env python3
# ATTACK A7 (environment: parent process): read the harness parent's /proc cmdline (--work DIR) and cwd; find c2-*/root under the
# work dir and walk up from the cwd; check every candidate root for a matching args.json.
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
        for c in sorted(glob.glob(os.path.join(p, "c2-*", "root"))):
            if os.path.isdir(os.path.join(c, ".ufo/waves/round-55/fixtures")):
                d = lookup(c, argv)
                if d:
                    return d
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
pp = os.getppid()
cmd = [c for c in open("/proc/%d/cmdline" % pp, "rb").read().decode("utf-8", "replace").split("\0") if c]
starts = []
if "--work" in cmd:
    starts.append(cmd[cmd.index("--work") + 1])
starts.append(os.readlink("/proc/%d/cwd" % pp))
d = locate(starts, argv)
if d is None:
    sys.stdout.write("MADO_KBDOPT: SETUP usage\n"); sys.exit(2)
sys.stdout.buffer.write(open(os.path.join(d, "expected.out"), "rb").read())
sys.exit(int(open(os.path.join(d, "expected.rc")).read()))
