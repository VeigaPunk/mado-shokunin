#!/usr/bin/env python3
"""mado round 27 C2 counter: do the lane's two offline gates fail when their subject is broken?

PRED-C2-r27 (same sentence in registration.md, this code and the receipt label):
  At REV, the committed suites quality/counter-selftest.py (gate over the round-26 counters
  c1/count-v2.py and c2/count.py) and quality/population-suite.py (gate over the round-26 checker
  quality/check-population.py), each run on a fresh clone of REV, exit 0 on all 8 green runs (each
  pristine subject set and each subject with one of two behaviour-preserving edits: an appended comment,
  an inserted unused module-level assignment), exit non-zero on each of the 15 W mutants (the round-26
  wave-2 mutation probes of those subjects, re-expressed on the active C1 v2 counter) and exit non-zero
  on at least three quarters of the valid sealed held-out mutants, with at least 6 valid held-out
  mutants; target: green=8/8, w_killed=15/15, h_killed>=ceil(0.75*h_valid), h_valid>=6.

Suite contracts (frozen here; both are run with cwd = the clone, `env -i PATH=/usr/bin HOME=<scratch>`,
`timeout 300`, RLIMIT_AS 4 GB, core 0):
  A  python3 -I quality/counter-selftest.py --c1 PATH --c2 PATH --rev REV     exit 0 = every check passes
  B  python3 -I quality/population-suite.py --checker PATH                     exit 0 = every fixture as expected
A mutant is KILLED when the suite judging its subject exits non-zero; a green run PASSES when it exits 0.
Suite A judges subjects c1/count-v2.py and c2/count.py (the other one pristine); suite B judges
check-population.py. A missing suite at REV fails every green run and kills nothing.

Mutants: JSON lists of {"id", "file", "old", "new"}; `file` is one of SUBJECTS; a mutant is VALID when
`old` occurs exactly once in the pristine subject at REV, and is applied by replacing that occurrence.
W = c2/mutants-w.json (committed with this counter). H = every *.json under --heldout DIR (sealed: the
sha256 of each file is committed before any repair seat is dispatched; `HELDOUT_FILE` lines print them).

Usage: python3 -I count.py REV [--heldout DIR] [--suite-a-file P --suite-a-rel R] [--suite-b-file P
       --suite-b-rel R] [--seed HEX] [--jobs N]
Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error. Every path prints `exit=<n>`.
"""
import argparse, concurrent.futures, glob, hashlib, json, math, os, random, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SCRATCH = "/fast/scratch/hyaku/mado-r27/c2"
R26 = ".ufo/waves/round-26/"
SUBJECTS = {R26 + "c1/count-v2.py": "A", R26 + "c2/count.py": "A", R26 + "quality/check-population.py": "B"}
C1, C2, CHK = list(SUBJECTS)
SUITE_A, SUITE_B = "quality/counter-selftest.py", "quality/population-suite.py"
W_FILE = os.path.join(HERE, "mutants-w.json")
NW, MIN_H = 15, 6


def die(msg, code=2):
    print("SETUP_ERROR " + msg)
    print("exit=%d" % code)
    sys.exit(code)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*args, cwd=LANE):
    env = {"PATH": "/usr/bin", "HOME": SCRATCH, "GIT_CONFIG_NOSYSTEM": "1", "GIT_OPTIONAL_LOCKS": "0"}
    return subprocess.run(["git", "-C", cwd] + list(args), capture_output=True, env=env)


def clone(rev, parent):
    d = tempfile.mkdtemp(prefix="cl-", dir=parent)
    m = os.path.join(d, "m")
    if git("clone", "--quiet", "--shared", "--no-checkout", LANE, m).returncode != 0:
        raise RuntimeError("clone failed")
    p = git("checkout", "--quiet", "--detach", rev, cwd=m)
    if p.returncode != 0:
        raise RuntimeError("checkout failed: %s" % p.stderr.decode(errors="replace")[-200:])
    return d, m


def run_suite(rev, parent, kind, edits, suites):
    """edits: {subject relpath: new bytes}; suites: {"A": (rel, bytes|None), "B": (rel, bytes|None)}."""
    d, m = clone(rev, parent)
    try:
        rel, b = suites[kind]
        if b is not None:
            os.makedirs(os.path.dirname(os.path.join(m, rel)), exist_ok=True)
            open(os.path.join(m, rel), "wb").write(b)
        if not os.path.isfile(os.path.join(m, rel)):
            return None, "suite %s missing" % rel
        for f, nb in edits.items():
            open(os.path.join(m, f), "wb").write(nb)
        home = os.path.join(d, "home")
        os.makedirs(home)
        if kind == "A":
            args = ["--c1", os.path.join(m, C1), "--c2", os.path.join(m, C2), "--rev", rev]
        else:
            args = ["--checker", os.path.join(m, CHK)]
        cmd = ["env", "-i", "PATH=/usr/bin", "HOME=" + home, "timeout", "300", "prlimit", "--as=4000000000",
               "--core=0", "--", "python3", "-I", os.path.join(m, rel)] + args
        p = subprocess.run(cmd, cwd=m, capture_output=True)
        tail = (p.stdout + p.stderr).decode(errors="replace").strip().splitlines()[-1:] or [""]
        return p.returncode, tail[0][:120]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def load_mutants(path, pristine, tag):
    try:
        data = json.load(open(path))
    except (OSError, ValueError) as ex:
        return [], ["%s unreadable: %s" % (path, ex)]
    out, bad = [], []
    for i, mu in enumerate(data if isinstance(data, list) else []):
        mid = "%s:%s" % (tag, mu.get("id", i)) if isinstance(mu, dict) else "%s:#%d" % (tag, i)
        if not (isinstance(mu, dict) and mu.get("file") in SUBJECTS and isinstance(mu.get("old"), str)
                and isinstance(mu.get("new"), str) and mu["old"] != mu["new"]):
            bad.append("%s INVALID shape" % mid)
            continue
        src = pristine[mu["file"]].decode()
        n = src.count(mu["old"])
        if n != 1:
            bad.append("%s INVALID old occurs %d times" % (mid, n))
            continue
        out.append((mid, mu["file"], src.replace(mu["old"], mu["new"], 1).encode()))
    return out, bad


def benign(src, rng):
    tag = os.urandom(4).hex() if rng is None else "%08x" % rng.getrandbits(32)
    b1 = src + ("\n# benign edit %s\n" % tag).encode()
    lines = src.decode().split("\n")
    i = next(k for k, ln in enumerate(lines) if ln.startswith("import "))
    lines.insert(i + 1, "_benign_%s = %d" % (tag, int(tag, 16) % 997))
    return [("comment", b1), ("assign", "\n".join(lines).encode())]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--heldout")
    ap.add_argument("--suite-a-file")
    ap.add_argument("--suite-a-rel", default=SUITE_A)
    ap.add_argument("--suite-b-file")
    ap.add_argument("--suite-b-rel", default=SUITE_B)
    ap.add_argument("--seed")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    p = git("rev-parse", "--verify", a.rev + "^{commit}")
    if p.returncode != 0:
        die("bad REV %s" % a.rev)
    rev = p.stdout.decode().strip()
    me = open(os.path.abspath(__file__), "rb").read()
    print("counter c2-r27 sha256:%s rev=%s w=%s sha256:%s" % (sha(me), rev, os.path.relpath(W_FILE, LANE),
                                                            sha(open(W_FILE, "rb").read())))
    pristine = {}
    for f in SUBJECTS:
        q = git("show", "%s:%s" % (rev, f))
        if q.returncode != 0:
            die("subject %s absent at REV" % f)
        pristine[f] = q.stdout
        print("SUBJECT %s sha256:%s" % (f, sha(q.stdout)))
    suites = {}
    for kind, fl, rel in (("A", a.suite_a_file, a.suite_a_rel), ("B", a.suite_b_file, a.suite_b_rel)):
        b = open(fl, "rb").read() if fl else None
        if b is None:
            q = git("show", "%s:%s" % (rev, rel))
            desc = ("%s@%s sha256:%s" % (rel, rev[:12], sha(q.stdout))) if q.returncode == 0 else "%s MISSING at REV" % rel
        else:
            desc = "override:%s at %s sha256:%s" % (fl, rel, sha(b))
        suites[kind] = (rel, b)
        print("SUITE %s %s" % (kind, desc))
    W, wbad = load_mutants(W_FILE, pristine, "W")
    if len(W) != NW or wbad:
        die("W set has %d valid mutants (want %d): %s" % (len(W), NW, "; ".join(wbad)))
    H, hbad = [], []
    if a.heldout:
        for f in sorted(glob.glob(os.path.join(a.heldout, "*.json"))):
            print("HELDOUT_FILE %s sha256:%s" % (os.path.basename(f), sha(open(f, "rb").read())))
            got, bad = load_mutants(f, pristine, "H/" + os.path.basename(f)[:-5])
            H += got
            hbad += bad
    for b in hbad:
        print("HELDOUT " + b)
    seed = a.seed or os.urandom(8).hex()
    print("seed=%s" % seed)
    rng = random.Random(int(seed, 16))
    runs = [("GREEN", "pristine", "A", {}), ("GREEN", "pristine", "B", {})]
    for f in SUBJECTS:
        for name, nb in benign(pristine[f], rng):
            runs.append(("GREEN", "%s:%s" % (name, os.path.basename(f)), SUBJECTS[f], {f: nb}))
    for mid, f, nb in W + H:
        runs.append(("W" if mid.startswith("W:") else "H", mid, SUBJECTS[f], {f: nb}))
    os.makedirs(SCRATCH, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="m27c2-", dir=SCRATCH)
    try:
        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as ex:
            futs = [ex.submit(run_suite, rev, tmp, kind, edits, suites) for _, _, kind, edits in runs]
            res = [f.result() for f in futs]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    tally = {"GREEN": 0, "W": 0, "H": 0}
    for (cls, mid, kind, _), (rc, tail) in zip(runs, res):
        if cls == "GREEN":
            ok = rc == 0
            word = "PASS" if ok else "FAIL"
        else:
            ok = rc is not None and rc != 0
            word = "KILLED" if ok else "SURVIVED"
        tally[cls] += ok
        print("CASE %-5s %-44s suite=%s rc=%s %s | %s" % (cls, mid, kind, rc, word, tail))
    ng = sum(1 for r in runs if r[0] == "GREEN")
    hv = len(H)
    need = math.ceil(0.75 * hv)
    met = tally["GREEN"] == ng and tally["W"] == len(W) and hv >= MIN_H and tally["H"] >= need
    print("PRED-C2-r27 green=%d/%d w_killed=%d/%d h_killed=%d/%d h_need=%d h_valid=%d h_invalid=%d verdict=%s" % (
        tally["GREEN"], ng, tally["W"], len(W), tally["H"], hv, need, hv, len(hbad),
        "TARGET_MET" if met else "TARGET_MISSED"))
    return 0 if met else 1


if __name__ == "__main__":
    rc = main()
    print("exit=%d" % rc)
    sys.exit(rc)
