#!/usr/bin/env python3
"""verify_survivors.py -- for every SURVIVED mutant of quality/r56_ctl_c3.py: propose the smallest new check that
kills it and verify that the addition really kills it.

For each survivor:
  * capture the harness's FULL stderr on the real counter (the reference stderr is captured too) -> if stdout AND
    stderr are byte-identical to the reference, the mutation is behaviour-preserving (EQUIVALENT);
  * run the proposed addition (a unit-level assertion on the harness module, or an end-to-end run of a PATCHED
    harness that carries one extra control) against the UNMUTATED harness  -> the addition must PASS;
  * run the same addition against the MUTANT                        -> the addition must FAIL (it kills the mutant).
A survivor that no addition kills is reported as NOT_KILLED (its argument is recorded).
"""
import difflib
import hashlib
import importlib.util
import inspect
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.environ.get("SCRATCH", "/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness")
TREE = os.path.join(S, "tree")
MINI = os.path.join(S, "mini")
TARGET = "quality/r56_ctl_c3.py"
RESULTS = os.path.join(S, "results.json")
REAL_COUNTER = os.path.join(TREE, "quality", "counters", "c3-r56-used-by.py")

sys.path.insert(0, HERE)
from mutants import MUTANTS  # noqa: E402


def mini_sha():
    if os.environ.get("REV"):
        return os.environ["REV"]
    with open(os.path.join(S, "mini_sha.txt")) as fh:
        return fh.read().strip()


def repo():
    return os.environ.get("REPO", MINI)


def git(*args):
    p = subprocess.run(["git", "-C", MINI] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args, p.stderr.decode()))
    return p.stdout


def good_inputs():
    src = git("show", "HEAD:corpus/SOURCES.md").decode("utf-8", "surrogateescape")
    entries = {}
    for rec in git("ls-tree", "-z", "HEAD", "corpus/knowledge/").split(b"\0"):
        if not rec:
            continue
        meta, _, name = rec.partition(b"\t")
        mode, typ, sha = meta.decode().split()
        if typ == "blob":
            entries[name.decode()] = git("cat-file", "blob", sha).decode("utf-8", "surrogateescape")
    base = json.loads(git("show", "HEAD:.ufo/waves/round-56/frozen-tables-v2.json").decode())["base"]
    base_src = git("show", "%s:corpus/SOURCES.md" % base).decode("utf-8", "surrogateescape")
    return src, entries, base_src


def load_module(path, name="h"):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mut_source(mutid):
    for rec in MUTANTS:
        if rec[0] == mutid:
            src = open(os.path.join(TREE, TARGET), "rb").read()
            return src.replace(rec[2].encode(), rec[3].encode(), 1)
    raise KeyError(mutid)


def write_variant(mutid, where):
    p = os.path.join(where, "r56_ctl_c3.py")
    data = mut_source(mutid) if mutid else open(os.path.join(TREE, TARGET), "rb").read()
    with open(p, "wb") as fh:
        fh.write(data)
    return p


def run_harness(module_path, work, counter=REAL_COUNTER):
    cmd = [sys.executable, "-I", module_path, "--repo", repo(), "--rev", mini_sha(), "--work", work, "--counter", counter]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work, timeout=900)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"), " ".join(cmd)


# --------------------------------------------------------------------------------------------- unit additions
def add_M13(mod):
    """parse_line must reject a `missed` list holding a leg name outside ALL_LEGS."""
    line = ("MADO_USED_BY: rev=abc entries=1 rows=1 missing=1 extra=0 dangling=0 conflict=0 stale=0 lost=0 "
            "exempt=24 verdict=TARGET_MISSED missed=missing,totally_bogus_leg\n")
    d, why = mod.parse_line(line, "abc")
    return d is None, "parse_line accepted an unknown leg name (%r)" % (why,)


def add_M15(mod):
    """parse_line must reject a line whose missing count is nonzero while `missing` is absent from the missed list."""
    line = ("MADO_USED_BY: rev=abc entries=1 rows=1 missing=41 extra=0 dangling=0 conflict=0 stale=0 lost=0 "
            "exempt=24 verdict=TARGET_MISSED missed=extra\n")
    d, why = mod.parse_line(line, "abc")
    return d is None, "parse_line accepted an inconsistent missing count / missed list (%r)" % (why,)


def add_M24(mod):
    """control 3 must remove exactly ONE path from exactly ONE used-by cell."""
    src, entries, base_src = good_inputs()
    ns, ne, note, leg = mod.mut_drop_one(src, entries, base_src)
    before = mod.parse_registry(src)[1]
    after = mod.parse_registry(ns)[1]
    if len(before) != len(after):
        return False, "row count changed"
    diff = [i for i, (a, b) in enumerate(zip(before, after)) if a[2] != b[2]]
    if len(diff) != 1:
        return False, "%d rows changed instead of 1" % len(diff)
    b = set(mod.USEDBY_RE.findall(before[diff[0]][2]))
    a = set(mod.USEDBY_RE.findall(after[diff[0]][2]))
    if len(b - a) != 1:
        return False, "%d paths removed instead of 1 (%r)" % (len(b - a), sorted(b - a))
    return True, ""


def add_M26(mod):
    """control 4 must mutate a source: line inside the 15-line SRC window (synthetic fixture).

    Two synthetic entries: the first (sorted) one has its only `source:` line at index 20 (outside the window),
    the second at index 3 (inside it).  The harness must mutate the SECOND one."""
    src, entries, base_src = good_inputs()
    a = "corpus/knowledge/aaa-r56.md"
    b = "corpus/knowledge/bbb-r56.md"
    la = ["# a"] + ["filler %d" % i for i in range(19)] + ["source: S001"] + ["tail"]
    lb = ["# b", "filler", "source: S001", "tail"]
    syn = {a: "\n".join(la), b: "\n".join(lb)}
    try:
        ns, ne, note, leg = mod.mut_dangling_source(src, syn, base_src)
    except Exception as ex:
        return False, "mut_dangling_source raised %r" % (ex,)
    if list(ne) != [b]:
        return False, "the mutated entry is %r, expected the entry whose source: line is inside the 15-line window" % (list(ne),)
    return True, ""


def add_M25(mod):
    """control 3 must SKIP an entry that no registry row lists (the `continue` branch)."""
    src, entries, base_src = good_inputs()
    first = sorted(entries)[0]
    # strip `first` from every used-by cell so that no row lists it
    stripped = mod.USEDBY_RE.sub(lambda m: "" if m.group(0) == first else m.group(0), src)
    try:
        ns, ne, note, leg = mod.mut_drop_one(stripped, entries, base_src)
    except Exception as ex:
        return False, "mut_drop_one raised %r instead of skipping the unlisted entry %s" % (ex, first)
    if first in note:
        return False, "the removed path is the unlisted entry %s" % first
    return True, ""


def add_M44(mod, path):
    """the harness's own entry model must agree with the counter on the number of entries."""
    w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "mut"))
    try:
        rc, out, err, _ = run_harness(path, w)
    finally:
        shutil.rmtree(w, ignore_errors=True)
    bad = [l for l in err.split("\n") if "entries counter=" in l]
    if bad:
        return False, "the harness's model reports a different entry count than the counter: %r" % (bad[0][:140],)
    return True, ""


def add_M27(mod):
    """control 5 must add the ghost path to the used-by of S001."""
    src, entries, base_src = good_inputs()
    ns, ne, note, leg = mod.mut_ghost_path(src, entries, base_src)
    rows = dict((sid, cell) for _, sid, cell in mod.parse_registry(ns)[1])
    if "corpus/knowledge/no-such-entry.md" not in rows.get("S001", ""):
        return False, "the ghost path is not in S001's used-by (%r)" % rows.get("S001", "")[:120]
    return True, ""


def add_M29(mod):
    """control 6 must fence the FIRST candidate pair (sorted by (S, entry))."""
    src, entries, base_src = good_inputs()
    ns, ne, note, leg = mod.mut_fenced_cite(src, entries, base_src)
    _, rows = mod.parse_registry(src)
    ids = {sid: set(mod.USEDBY_RE.findall(cell)) for _, sid, cell in rows}
    cands = []
    for path, text in entries.items():
        cl = mod.cite_lines(text)
        for s in set(t for _, t in cl):
            occ = [i for i, t in cl if t == s]
            if len(occ) == 1 and s in ids and path in ids[s]:
                cands.append((s, path, occ[0]))
    want = sorted(cands)[0]
    path = list(ne)[0]
    if want[1] != path:
        return False, "fenced %s instead of the first candidate %s" % (path, want[1])
    if "```" not in ne[path].split("\n")[want[2]]:
        return False, "the first candidate line is not fenced"
    return True, ""


def add_M30(mod):
    """control 6 must CLOSE the fence it opens."""
    src, entries, base_src = good_inputs()
    ns, ne, note, leg = mod.mut_fenced_cite(src, entries, base_src)
    path = list(ne)[0]
    n = sum(1 for ln in ne[path].split("\n") if ln.strip() == "```")
    if n % 2 != 0:
        return False, "%d ``` markers in the mutated entry: the fence is left open" % n
    return True, ""


def add_M32(mod):
    """control 7 must write an allowlist row for EVERY (S, entry) pair."""
    src, entries, base_src = good_inputs()
    ns, ne, note, leg = mod.mut_allow_everything(src, entries, base_src)
    rows = [r for r in ne[mod.ALLOW_PATH].split("\n") if r]
    ids = set(r[1] for r in mod.parse_registry(src)[1])
    pl = mod.pair_lines(entries, ids)
    if len(rows) != len(pl):
        return False, "the allowlist has %d rows, the tree has %d pairs" % (len(rows), len(pl))
    return True, ""


def add_M52(mod):
    """the harness's citation token rule must be the contract's rule: no token inside a longer identifier."""
    hit = mod.CITE_RE.findall("XS001 and S0021 and S003")
    if hit != ["S003"]:
        return False, "CITE_RE matched %r (only the standalone token may match)" % (hit,)
    return True, ""


# --------------------------------------------------------------------------------------------- patched-harness additions
NOOP_FN = '''

def mut_noop(src, entries, base_src):
    """a deliberately ineffective control (the frozen tree is not changed): the harness must reject it."""
    return src, {}, "no-op mutation", "%s"
'''

NOOP_ENTRY_FN = '''

def mut_noop(src, entries, base_src):
    """a deliberately ineffective control: one entry is touched, but no leg can rise."""
    path = sorted(entries)[0]
    lines = entries[path].split("\\n")
    lines[-1] = lines[-1] + " x"
    return src, {path: "\\n".join(lines)}, "no-op mutation of one entry", "%s"
'''


def patch_noop(src, leg, mode="empty"):
    """add control 10 "noop-control" whose mutation changes nothing (or touches one entry) and targets `leg`."""
    if isinstance(src, bytes):
        src = src.decode("utf-8")
    fn = (NOOP_ENTRY_FN if mode == "entry" else NOOP_FN) % leg
    src = src.replace("\nCONTROLS = [", fn + "\nCONTROLS = [", 1)
    src = src.replace('    ("stale-allow", mut_stale_allow),\n]',
                      '    ("stale-allow", mut_stale_allow),\n    ("noop-control", mut_noop),\n]', 1)
    return src


def run_patched(mutid, leg, mode="empty"):
    """-> (ok, detail): the patched harness must refuse the ineffective control (setup error, exit 2)."""
    d = tempfile.mkdtemp(prefix="patch.", dir=os.path.join(S, "mut"))
    try:
        p = os.path.join(d, "r56_ctl_c3.py")
        data = mut_source(mutid) if mutid else open(os.path.join(TREE, TARGET), "rb").read()
        with open(p, "wb") as fh:
            fh.write(patch_noop(data, leg, mode).encode())
        w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "mut"))
        try:
            rc, out, err, cmd = run_harness(p, w)
        finally:
            shutil.rmtree(w, ignore_errors=True)
        ok = (rc == 2 and "ineffective" in err)
        return ok, "patched harness rc=%d stdout=%r stderr=%r" % (rc, out.strip()[:120], err.strip().split("\n")[-1][:160])
    finally:
        shutil.rmtree(d, ignore_errors=True)


def add_M36(mod):
    return run_patched(None, "missing", "empty")


def add_M37(mod):
    return run_patched(None, "missing", "empty")


def add_M38(mod):
    return run_patched(None, "dangling", "entry")



UNIT_ADDITIONS = {
    "M13": add_M13, "M15": add_M15, "M24": add_M24, "M25": add_M25, "M26": add_M26, "M27": add_M27,
    "M29": add_M29, "M30": add_M30, "M32": add_M32, "M44": add_M44, "M52": add_M52,
}
PATCH_ADDITIONS = {"M36": ("missing", "empty"), "M37": ("missing", "empty"), "M38": ("dangling", "entry")}


def main():
    results = json.load(open(RESULTS))
    survivors = [r["id"] for r in results if r["status"] == "SURVIVED"]
    print("survivors (%d): %s" % (len(survivors), ", ".join(survivors)))

    # reference stderr (unmutated harness, real counter)
    refd = tempfile.mkdtemp(prefix="ref.", dir=os.path.join(S, "mut"))
    try:
        refp = write_variant(None, refd)
        w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "mut"))
        try:
            rc, out, err, _ = run_harness(refp, w)
        finally:
            shutil.rmtree(w, ignore_errors=True)
    finally:
        shutil.rmtree(refd, ignore_errors=True)
    print("reference: rc=%d stdout=%r" % (rc, out.strip()))

    out_rows = []
    for mid in survivors:
        row = {"id": mid}
        # 1) observable difference of the survivor against the reference
        d = tempfile.mkdtemp(prefix="mut.", dir=os.path.join(S, "mut"))
        try:
            mutp = write_variant(mid, d)
            w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "mut"))
            try:
                mrc, mout, merr, _ = run_harness(mutp, w)
            finally:
                shutil.rmtree(w, ignore_errors=True)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        row["stdout_identical"] = (mout == out)
        row["stderr_identical"] = (merr == err)
        if not row["stderr_identical"]:
            diff = [l for l in difflib.unified_diff(err.split("\n"), merr.split("\n"), "reference", mid, n=0)
                    if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
            row["stderr_diff"] = diff[:12]

        # 2) the proposed addition
        if mid in UNIT_ADDITIONS:
            fn = UNIT_ADDITIONS[mid]
            rd = tempfile.mkdtemp(prefix="ref.", dir=os.path.join(S, "mut"))
            md = tempfile.mkdtemp(prefix="mut.", dir=os.path.join(S, "mut"))
            try:
                refp = write_variant(None, rd)
                mutp = write_variant(mid, md)
                two = len(inspect.signature(fn).parameters) == 2
                ref_ok = fn(load_module(refp, "ref_" + mid), refp) if two else fn(load_module(refp, "ref_" + mid))
                mut_ok = fn(load_module(mutp, "mut_" + mid), mutp) if two else fn(load_module(mutp, "mut_" + mid))
            finally:
                shutil.rmtree(rd, ignore_errors=True)
                shutil.rmtree(md, ignore_errors=True)
            row["addition"] = "unit:" + fn.__name__
            row["reference_passes"] = bool(ref_ok[0])
            row["mutant_passes"] = bool(mut_ok[0])
            row["mutant_detail"] = mut_ok[1]
        elif mid in PATCH_ADDITIONS:
            leg, mode = PATCH_ADDITIONS[mid]
            ref_ok = run_patched(None, leg, mode)
            mut_ok = run_patched(mid, leg, mode)
            row["addition"] = ("patched harness + control 10 'noop-control' (leg=%s, mode=%s); the harness must exit 2 "
                               "with 'control noop-control is ineffective'" % (leg, mode))
            row["reference_passes"] = bool(ref_ok[0])
            row["mutant_passes"] = bool(mut_ok[0])
            row["mutant_detail"] = mut_ok[1]
        else:
            row["addition"] = None
            row["reference_passes"] = None
            row["mutant_passes"] = None
        if row["addition"] is None:
            row["verdict"] = "EQUIVALENT (no addition proposed)" if (row["stdout_identical"] and row["stderr_identical"]) \
                else "NOT_KILLED (no addition proposed)"
        else:
            row["verdict"] = "KILLED_BY_ADDITION" if (row["reference_passes"] and not row["mutant_passes"]) else "NOT_KILLED"
        out_rows.append(row)
        print("%-5s stdout_same=%-5s stderr_same=%-5s %-22s ref=%-5s mutant=%-5s %s"
              % (mid, row["stdout_identical"], row["stderr_identical"], row.get("addition"),
                 row.get("reference_passes"), row.get("mutant_passes"), str(row.get("mutant_detail", ""))[:70]))
    with open(os.path.join(S, "survivor_verification.json"), "w") as fh:
        json.dump(out_rows, fh, indent=1)
    print("-> %s" % os.path.join(S, "survivor_verification.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
