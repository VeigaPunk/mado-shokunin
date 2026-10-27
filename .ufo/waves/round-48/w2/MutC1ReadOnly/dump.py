#!/usr/bin/env python3
"""w2/MutC1ReadOnly - dump raw strace receipts for one tool under the FROZEN sandbox argv.

Two things the frozen counter cannot show, because check_trace() unlinks each trace after scoring it:

  --trace  : keep the trace the frozen counter produces (same bwrap argv, same -e filter) for one run.
  --extend : run the same sandbox argv under a WIDER filter (openat/write/clone/fork/vfork/execve/...) to
             prove that the events which clause r cannot see are traceable at all - i.e. name the clause
             extension concretely.

Usage: dump.py --counter C --tool T --work W --tag TAG [--extend]
"""
import argparse
import importlib.util
import os
import shutil
import sys


def load_counter(path):
    spec = importlib.util.spec_from_file_location("c1r48", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--tool", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--extend", action="store_true")
    ap.add_argument("--fixtures", type=int, default=0, help="run N sampled fixtures with every trace kept")
    a = ap.parse_args()
    m = load_counter(a.counter)
    work = os.path.join(a.work, "dump-" + a.tag)
    os.makedirs(work, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)

    class Keep(m.Box):
        def check_trace(self, path):
            self.seen = getattr(self, "seen", 0) + 1
            dst = os.path.join(a.out, "trace-%s-%02d.txt" % (a.tag, self.seen))
            if not a.extend:
                try:
                    shutil.copy(path, dst)
                except OSError:
                    pass
            super().check_trace(path)

    box = Keep(work, os.path.realpath(a.tool))
    if a.fixtures:
        import random
        cold = m.load_fixtures(m.beside(m.NAME_COLD), m.SHA256_COLD, 100)
        warm = [f for f in m.load_fixtures(m.beside(m.NAME_WARM), m.SHA256_WARM, 20) if f.get("prime")]
        rng = random.Random(4848)
        for fx in cold[:a.fixtures]:
            ok, o, why, _s, _c = m.run_case(box, fx, "A", rng)
            print("FIX cold=%s ok=%s trips_so_far=%d" % (fx["id"], ok, len(box.trips)))
        for fx in warm[:a.fixtures]:
            ok, o, why, _s, _c = m.run_case(box, fx, "A", rng)
            print("FIX warm=%s ok=%s trips_so_far=%d" % (fx["id"], ok, len(box.trips)))
        for t in box.trips:
            print("TRIP %s" % t)
        return 0
    sd = os.path.join(work, "demo", "r")
    os.makedirs(os.path.join(sd, ".rw", "cache"), exist_ok=True)
    os.makedirs(os.path.join(sd, "home"), exist_ok=True)
    with open(os.path.join(sd, "bin"), "a"):
        pass
    env = {"PATH": "/oracle/bin", "HOME": os.path.join(sd, "home"), "TMPDIR": "/tmp", "LANG": "C.UTF-8",
           "XDG_CACHE_HOME": os.path.join(sd, ".rw", "cache")}
    if a.extend:
        wide = ("openat,open,openat2,creat,write,mkdir,mkdirat,unlink,unlinkat,rename,renameat,renameat2,"
                "truncate,ftruncate,execve,execveat,socket,socketpair,connect,clone,clone3,fork,vfork")
        dst = os.path.join(a.out, "trace-%s-wide.txt" % a.tag)
        argv = [box.strace, "-f", "-qq", "-e", "trace=" + wide, "-e", "signal=none", "-o", dst] + \
            box.argv(sd, env, True, ["--selftest"])
        import subprocess
        p = subprocess.run(argv, capture_output=True, env={"PATH": "/usr/bin"}, timeout=300)
        print("WIDE rc=%d out_last=%r" % (p.returncode, (p.stdout.strip().split(b"\n")[-1:] or [b""])[0][:80]))
        print("WIDE trace=%s bytes=%d" % (dst, os.path.getsize(dst) if os.path.exists(dst) else -1))
        return 0
    rc, out, err = box.run(sd, env, True, ["--selftest"], timeout=180)
    last = out.strip().split("\n")[-1] if out.strip() else ""
    print("DUMP rc=%d last=%r trips=%d" % (rc, last[:100], len(box.trips)))
    for ln in err.split("\n"):
        if "R48PROBE" in ln:
            print("TOOL_STDERR %s" % ln.strip()[:300])
    for t in box.trips:
        print("TRIP %s" % t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
