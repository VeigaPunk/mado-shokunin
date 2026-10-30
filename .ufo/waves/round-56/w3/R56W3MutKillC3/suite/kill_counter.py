#!/usr/bin/env python3
"""kill_counter.py -- materialize each counter kill fixture on a scratch clone of the tip tree and verify that
the PRISTINE counter satisfies the fixture's predicate while the MUTANT counter violates it.

Input : suite/counter_mutants.py (the mutant table), suite/counter_killers.py (the fixtures), and the survivor
        set measured by sweep_counter.py.
Output: kill_counter.json -- one row per survivor: fixture, pristine line, mutant line, verdict.
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import counter_killers as CK  # noqa: E402

_spec = importlib.util.spec_from_file_location("counter_mutants", os.path.join(HERE, "counter_mutants.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
MUTANTS = {m[0]: m for m in _mod.MUTANTS}

MINI = os.path.join(S, "mini")
TREE = os.path.join(S, "src")
COUNTER_SRC = os.path.join(TREE, "quality_counters_c3-r56-used-by.py")
WORK = os.path.join(S, "work")
FIXDIR = os.path.join(HERE, "fixtures", "counter")


def mini_sha():
    return open(os.path.join(S, "mini_sha.txt")).read().strip()


def git(d, *args, **kw):
    p = subprocess.run(["git", "-C", d] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args, p.stderr.decode()))
    return p.stdout


def mutant_source(mid):
    rec = MUTANTS[mid]
    src = open(COUNTER_SRC, "rb").read()
    assert src.count(rec[2].encode()) == 1, mid
    return src.replace(rec[2].encode(), rec[3].encode(), 1)


def run_counter(counter_path, repo, rev, work):
    cmd = [sys.executable, "-I", counter_path, "--repo", repo, "--rev", rev, "--work", work]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=900)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def build_fixture(fid):
    """-> (checkout_dir, commit_sha, ctx): a scratch clone of the tip tree with the fixture mutation committed."""
    spec = CK.FIXTURES[fid]
    d = tempfile.mkdtemp(prefix="fx.%s." % fid, dir=WORK)
    r = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", MINI, d],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise SystemExit("clone failed: %s" % r.stderr.decode())
    top = git(d, "rev-parse", "--show-toplevel").decode().strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit("fixture toplevel mismatch")
    git(d, "checkout", "-q", "--detach", mini_sha())
    ctx = {}
    if fid == "CM19":
        # base_rev must name a commit whose base pairs do NOT hash to the frozen value: use the tip commit
        ctx["base_rev"] = mini_sha()
    if fid == "CM25":
        ctx["two_pairs"] = two_filled_pairs(d)
    spec["mutate"](d, ctx)
    git(d, "add", "-A", "-f", ".")
    git(d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--no-gpg-sign", "-m", "kill fixture %s" % fid)
    os.makedirs(FIXDIR, exist_ok=True)
    with open(os.path.join(FIXDIR, fid + ".diff"), "wb") as fh:
        fh.write(git(d, "diff", "--no-color", "%s" % mini_sha(), "HEAD"))
    return d, git(d, "rev-parse", "HEAD").decode().strip(), ctx


def two_filled_pairs(checkout):
    """two (S, entry) pairs that the good tree back-references and that are not on the frozen allowlist.

    Removing their used-by entries must raise the frozen `missing` count by two."""
    src = git(checkout, "show", "HEAD:corpus/SOURCES.md").decode("utf-8", "surrogateescape")
    entries = {}
    for rec in git(checkout, "ls-tree", "-z", "HEAD", "corpus/knowledge/").split(b"\0"):
        if not rec:
            continue
        meta, _, name = rec.partition(b"\t")
        mode, typ, sha = meta.decode().split()
        if typ == "blob":
            entries[name.decode()] = git(checkout, "cat-file", "blob", sha).decode("utf-8", "surrogateescape")
    allow = set()
    for ln in git(checkout, "show", "HEAD:.ufo/waves/round-56/c3-name-only.tsv").decode().split("\n"):
        if ln:
            c = ln.split("\t")
            allow.add((c[0], c[1]))
    rows = {}
    for i, ln in enumerate(src.split("\n")):
        m = re.match(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|", ln)
        if m:
            cells = ln.split("|")
            rows[m.group(1)] = cells[11]
    ids = set(rows)
    used = {}
    for sid, cell in rows.items():
        used[sid] = set(re.findall(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md", cell))
    pairs = []
    for path, text in entries.items():
        for s in set(re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])", text)):
            if s in ids and path in used.get(s, ()) and (s, path) not in allow and s not in [p[0] for p in pairs]:
                pairs.append((s, path))
    if len(pairs) < 2:
        raise SystemExit("not enough filled pairs")
    return pairs[:2]


def main():
    os.makedirs(WORK, exist_ok=True)
    sweep = json.load(open(os.path.join(S, "sweep_counter.json")))
    survivors = [r["id"] for r in sweep if r["status"] == "SURVIVED"]
    rows = []
    for mid in survivors:
        if mid not in CK.FIXTURES:
            rows.append({"id": mid, "verdict": "NO_FIXTURE", "note": "no fixture proposed for this survivor"})
            print("%-5s NO_FIXTURE" % mid, flush=True)
            continue
        spec = CK.FIXTURES[mid]
        checkout = None
        try:
            checkout, sha, ctx = build_fixture(mid)
            w = tempfile.mkdtemp(prefix="w.", dir=WORK)
            try:
                prc, pout, perr = run_counter(COUNTER_SRC, checkout, sha, w)
                d = tempfile.mkdtemp(prefix="cmut.", dir=WORK)
                try:
                    cpath = os.path.join(d, "c3-r56-used-by.py")
                    with open(cpath, "wb") as fh:
                        fh.write(mutant_source(mid))
                    mrc, mout, merr = run_counter(cpath, checkout, sha, w)
                finally:
                    shutil.rmtree(d, ignore_errors=True)
            finally:
                shutil.rmtree(w, ignore_errors=True)
        finally:
            if checkout:
                shutil.rmtree(checkout, ignore_errors=True)
        if spec["predicate"] is None:
            # population fixture: the reported number must equal the tree's true population
            pred = population_predicate(mid)
        else:
            pred = spec["predicate"]
        ref_ok, ref_why = pred(pout, prc)
        mut_ok, mut_why = pred(mout, mrc)
        verdict = "KILLED" if (ref_ok and not mut_ok) else "NOT_KILLED"
        rows.append({"id": mid, "fixture": mid, "fixture_kind": spec["kind"], "fixture_desc": spec["desc"],
                     "reference_ok": bool(ref_ok), "reference_detail": ref_why, "reference_line": pout.strip(),
                     "reference_rc": prc,
                     "mutant_ok": bool(mut_ok), "mutant_detail": mut_why, "mutant_line": mout.strip(),
                     "mutant_rc": mrc, "verdict": verdict,
                     "mutant_sha256": hashlib.sha256(mutant_source(mid)).hexdigest()})
        print("%-5s %-10s ref=%-5s mutant=%-5s | %s || %s" % (mid, verdict, bool(ref_ok), bool(mut_ok),
                                                            ref_why[:60], mut_why[:60]), flush=True)
    out = os.path.join(S, "kill_counter.json")
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=1)
    k = [r for r in rows if r.get("verdict") == "KILLED"]
    nk = [r for r in rows if r.get("verdict") == "NOT_KILLED"]
    nf = [r for r in rows if r.get("verdict") == "NO_FIXTURE"]
    print("\ncounter survivors=%d killed_by_fixture=%d not_killed=%d no_fixture=%d" % (len(rows), len(k), len(nk), len(nf)))
    print("-> %s" % out)
    return 0


def population_predicate(mid):
    """the reported population must equal the tree's true population."""
    def f(line, rc):
        m = re.search(r" entries=(\d+) rows=(\d+) ", line)
        if not m:
            return False, "no parsable line (rc=%s)" % rc
        # the fixture adds exactly one entry (CM11) or exactly one registry row (CM12)
        if mid == "CM11":
            want = (72, None)
        else:
            want = (None, 333)
        if want[0] is not None and int(m.group(1)) != want[0]:
            return False, "entries=%s, expected %s" % (m.group(1), want[0])
        if want[1] is not None and int(m.group(2)) != want[1]:
            return False, "rows=%s, expected %s" % (m.group(2), want[1])
        return True, "entries=%s rows=%s" % (m.group(1), m.group(2))
    return f


if __name__ == "__main__":
    sys.exit(main())
