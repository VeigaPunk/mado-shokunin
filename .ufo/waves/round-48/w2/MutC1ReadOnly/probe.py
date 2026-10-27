#!/usr/bin/env python3
"""w2/MutC1ReadOnly probe - drive the FROZEN r48 C1 counter's own sandbox/trace machinery against one tool.

This is NOT a counter and never a score. It imports c1-r48-terminal-cache.py unchanged and calls its exact
Box / selftest_clause / run_case / check_premise / explain_case code, so the sandbox argv, the strace filter
(TRACE_SET), check_trace() and the fixture preparation are byte-for-byte the frozen ones. What it adds:

  * it prints the tool stderr the frozen counter discards (run_case keeps only stdout/rc), so a mutant can
    report what it did in-sandbox;
  * it fingerprints the tool tree (path, size, mtime_ns, mode) before and after the selftest run, i.e. the
    "tree check" the registration's contract text implies but the frozen counter does not implement;
  * it reports box.trips after each phase, so a boundary violation is attributable to a clause.

Usage: probe.py --counter <c1-r48-terminal-cache.py> --tool <mado-terminal.py> --work <dir> --tag <name>
                [--cold N] [--warm N] [--prime N] [--explain N]
Exit 0 iff every sampled functional check passed (the trips count is reported, not judged).
"""
import argparse
import hashlib
import importlib.util
import os
import random
import sys


def load_counter(path):
    spec = importlib.util.spec_from_file_location("c1r48", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tree_digest(root):
    """The r48-w2 tree fingerprint: every path, its type, mode, size and mtime_ns, hashed."""
    h = hashlib.sha256()
    for d, dirs, files in os.walk(root):
        dirs.sort()
        for n in sorted(dirs) + sorted(files):
            p = os.path.join(d, n)
            try:
                st = os.lstat(p)
            except OSError:
                continue
            h.update(("%s|%o|%d|%d\n" % (os.path.relpath(p, root), st.st_mode, st.st_size,
                                         st.st_mtime_ns)).encode("utf-8", "surrogateescape"))
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--tool", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--cold", type=int, default=6)
    ap.add_argument("--warm", type=int, default=6)
    ap.add_argument("--prime", type=int, default=0, help="how many primed warm fixtures to include")
    ap.add_argument("--explain", type=int, default=2)
    a = ap.parse_args()
    m = load_counter(a.counter)
    work = os.path.join(a.work, a.tag)
    os.makedirs(work, exist_ok=True)
    tool = os.path.realpath(a.tool)
    sha = hashlib.sha256(open(tool, "rb").read()).hexdigest()
    box = m.Box(work, tool)
    cold = m.load_fixtures(m.beside(m.NAME_COLD), m.SHA256_COLD, 100)
    warm = m.load_fixtures(m.beside(m.NAME_WARM), m.SHA256_WARM, 20)
    rng = random.Random(4848)
    print("PROBE tag=%s tool_sha256=%s counter=%s trace_set=%s" % (
        a.tag, sha, os.path.basename(a.counter), m.TRACE_SET))

    # ---- phase 1: one selftest run, with the tool stderr the counter throws away, and a tree fingerprint
    sd = os.path.join(work, "demo", "r")
    os.makedirs(os.path.join(sd, ".rw", "cache"), exist_ok=True)
    with open(os.path.join(sd, "bin"), "a"):
        pass
    env = {"PATH": "/oracle/bin", "HOME": os.path.join(sd, "home"), "TMPDIR": "/tmp", "LANG": "C.UTF-8",
           "XDG_CACHE_HOME": os.path.join(sd, ".rw", "cache")}
    os.makedirs(os.path.join(sd, "home"), exist_ok=True)
    pre = tree_digest(sd)
    rc, out, err = box.run(sd, env, True, ["--selftest"], timeout=180)
    post = tree_digest(sd)
    last = out.strip().split("\n")[-1] if out.strip() else ""
    print("HOOKRUN rc=%d last=%r" % (rc, last[:120]))
    for ln in err.split("\n"):
        if "R48PROBE" in ln:
            print("TOOL_STDERR %s" % ln.strip()[:300])
    print("TREEFP pre=%s post=%s same=%s" % (pre[:16], post[:16], pre == post))
    print("TRIPS_AFTER_HOOK %d %s" % (len(box.trips), ";".join(sorted(set(box.trips)))[:200]))
    n_trips_hook = len(box.trips)

    # ---- phase 2: sampled cold fixtures (variant A only: the sample is functional identity, not a score)
    f_ok = 0
    pick_cold = cold[:a.cold]
    for fx in pick_cold:
        ok, o, why, _st, _c = m.run_case(box, fx, "A", rng)
        if [o[0], o[1]] != [fx["expect"]["rc"], fx["expect"]["stdout"]]:
            ok = False
            why = (why + " expect-drift").strip()
        f_ok += ok
        print("SAMPLE cold=%s %s%s" % (fx["id"], "pass" if ok else "FAIL", "" if ok else " " + why[:200]))
    print("SAMPLE cold=%d/%d" % (f_ok, len(pick_cold)))

    # ---- phase 3: sampled warm fixtures, preferring literal-cache ones, plus --prime primed ones
    lit = [fx for fx in warm if "cache" in fx]
    prim = [fx for fx in warm if fx.get("prime")]
    pick = lit[:max(0, a.warm - a.prime)] + prim[:a.prime]
    w_ok = 0
    for fx in pick:
        ok, o, why, st, coldo = m.run_case(box, fx, "A", rng)
        try:
            m.check_premise(fx, st, coldo)
        except m.Setup as e:
            ok = False
            why = (why + " premise: %s" % e).strip()
        if [o[0], o[1]] != [fx["expect"]["rc"], fx["expect"]["stdout"]]:
            ok = False
            why = (why + " expect-drift").strip()
        w_ok += ok
        print("SAMPLE warm=%s class=%s state=%s %s%s" % (
            fx["id"], fx["class"], st, "pass" if ok else "FAIL", "" if ok else " " + why[:200]))
    print("SAMPLE warm=%d/%d" % (w_ok, len(pick)))

    # ---- phase 4: sampled explain clauses
    x_ok = 0
    pick_x = (pick_cold[:max(1, a.explain)] if pick_cold else []) + (pick[:1] if pick else [])
    for fx in pick_x:
        ok, why = m.explain_case(box, fx, rng)
        x_ok += ok
        print("SAMPLE explain=%s %s%s" % (fx["id"], "pass" if ok else "FAIL", "" if ok else " " + why[:200]))
    print("SAMPLE explain=%d/%d" % (x_ok, len(pick_x)))

    print("TRIPS_TOTAL %d %s" % (len(box.trips), ";".join(sorted(set(box.trips)))[:400]))
    total = len(pick_cold) + len(pick) + len(pick_x)
    good = f_ok + w_ok + x_ok
    print("PROBE_RESULT tag=%s functional=%d/%d trips=%d trips_after_hook=%d" % (a.tag, good, total,
                                                                                len(box.trips), n_trips_hook))
    return 0 if good == total else 1


if __name__ == "__main__":
    sys.exit(main())
