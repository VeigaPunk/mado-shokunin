#!/usr/bin/env python3
"""harness_killers.py -- the kill fixtures for the named survivors of quality/r56_ctl_c3.py.

Each killer is a fixture (a concrete input: a counter output line, a synthetic entry pair, the lane tip's
registry/entries, or a patched harness carrying one extra control) plus a check.  A killer is applied to the
PRISTINE harness (must PASS) and to the MUTANT harness (must FAIL -> the mutant is killed).

The checks are the ones the wave-2 seat proposed for the fourteen non-equivalent survivors of its sweep
(.ufo/waves/round-56/w2/R56W2MutC3Harness.md section 3.1), re-derived here against the lane tip and materialized
as fixture files under fixtures/harness/ instead of inline literals.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(HERE)
FIX = os.path.join(HERE, "fixtures", "harness")
MINI = os.path.join(S, "mini")
TREE = os.path.join(S, "src")
HARNESS_SRC = os.path.join(TREE, "quality_r56_ctl_c3.py")
DRIVER_SRC = os.path.join(TREE, "quality_check-r56-controls.py")
REAL_COUNTER = os.path.join(TREE, "quality_counters_c3-r56-used-by.py")


def mini_sha():
    return open(os.path.join(S, "mini_sha.txt")).read().strip()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(*args):
    p = subprocess.run(["git", "-C", MINI] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args, p.stderr.decode()))
    return p.stdout


def good_inputs():
    """(registry text, {path: text}, base registry text) of the lane tip's good tree."""
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


# ---------------------------------------------------------------------------------------------- fixture files
def fixture_path(name):
    return os.path.join(FIX, name)


# ---------------------------------------------------------------------------------------------- killers
def kill_M13(mod):
    """parse_line must reject a `missed` list that holds a leg name outside ALL_LEGS.

    Fixture: fixtures/harness/M13-counter-line.txt -- a grammatical counter line whose missed list names an
    unknown leg.  The harness must treat the line as unparsable (a counter that invents a leg is not trusted)."""
    line = open(fixture_path("M13-counter-line.txt")).read()
    d, why = mod.parse_line(line, "abc")
    return d is None, "parse_line accepted an unknown leg name (%r)" % (why,)


def kill_M15(mod):
    """parse_line must reject a line whose missing count is nonzero while `missing` is absent from missed.

    Fixture: fixtures/harness/M15-counter-line.txt."""
    line = open(fixture_path("M15-counter-line.txt")).read()
    d, why = mod.parse_line(line, "abc")
    return d is None, "parse_line accepted an inconsistent missing count / missed list (%r)" % (why,)


def kill_M24(mod):
    """control 3 (drop-one) must remove exactly ONE path from exactly ONE used-by cell.

    Fixture: the lane tip's registry (corpus/SOURCES.md).  The cell of the row that lists the entry holds
    nine paths; the control must drop exactly one of them, not the whole cell."""
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


def kill_M25(mod):
    """control 3 must SKIP an entry that no registry row lists (the `continue` branch).

    Fixture: the lane tip's registry with the first sorted entry stripped from every used-by cell."""
    src, entries, base_src = good_inputs()
    first = sorted(entries)[0]
    stripped = mod.USEDBY_RE.sub(lambda m: "" if m.group(0) == first else m.group(0), src)
    try:
        ns, ne, note, leg = mod.mut_drop_one(stripped, entries, base_src)
    except Exception as ex:
        return False, "mut_drop_one raised %r instead of skipping the unlisted entry %s" % (ex, first)
    if first in note:
        return False, "the removed path is the unlisted entry %s" % first
    return True, ""


def kill_M26(mod):
    """control 4 must mutate a source: line inside the 15-line SRC window.

    Fixture: fixtures/harness/M26-entries.json -- two synthetic entries, the first (sorted) one with its only
    `source:` line at index 20 (outside the window), the second at index 3 (inside it)."""
    src, entries, base_src = good_inputs()
    syn = json.load(open(fixture_path("M26-entries.json")))
    try:
        ns, ne, note, leg = mod.mut_dangling_source(src, syn, base_src)
    except Exception as ex:
        return False, "mut_dangling_source raised %r" % (ex,)
    want = sorted(syn)[1]
    if list(ne) != [want]:
        return False, "the mutated entry is %r, expected the entry whose source: line is inside the 15-line window" % (list(ne),)
    return True, ""


def kill_M27(mod):
    """control 5 (ghost-path) must add the ghost path to the used-by of S001.

    Fixture: the lane tip's registry."""
    src, entries, base_src = good_inputs()
    ns, ne, note, leg = mod.mut_ghost_path(src, entries, base_src)
    rows = dict((sid, cell) for _, sid, cell in mod.parse_registry(ns)[1])
    ghost = "corpus/knowledge/no-such-entry.md"
    if ghost not in rows.get("S001", ""):
        return False, "the ghost path is not in S001's used-by (%r)" % rows.get("S001", "")[:120]
    return True, ""


def kill_M29(mod):
    """control 6 (fenced-cite) must fence the FIRST candidate pair (sorted by (S, entry)).

    Fixture: the lane tip's registry and entries."""
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


def kill_M30(mod):
    """control 6 must CLOSE the fence it opens.

    Fixture: the lane tip's entries."""
    src, entries, base_src = good_inputs()
    ns, ne, note, leg = mod.mut_fenced_cite(src, entries, base_src)
    path = list(ne)[0]
    n = sum(1 for ln in ne[path].split("\n") if ln.strip() == "```")
    if n % 2 != 0:
        return False, "%d ``` markers in the mutated entry: the fence is left open" % n
    return True, ""


def kill_M32(mod):
    """control 7 (allow-everything) must write an allowlist row for EVERY (S, entry) pair.

    Fixture: the lane tip's registry and entries; the allowlist the control writes is compared with the pair set."""
    src, entries, base_src = good_inputs()
    ns, ne, note, leg = mod.mut_allow_everything(src, entries, base_src)
    rows = [r for r in ne[mod.ALLOW_PATH].split("\n") if r]
    ids = set(r[1] for r in mod.parse_registry(src)[1])
    pl = mod.pair_lines(entries, ids)
    if len(rows) != len(pl):
        return False, "the allowlist has %d rows, the tree has %d pairs" % (len(rows), len(pl))
    return True, ""


def kill_M52(mod):
    """the harness's citation token rule must be the contract's rule: no token inside a longer identifier.

    Fixture: fixtures/harness/M52-token-string.txt -- "XS001 and S0021 and S003"."""
    text = open(fixture_path("M52-token-string.txt")).read().strip()
    hit = mod.CITE_RE.findall(text)
    if hit != ["S003"]:
        return False, "CITE_RE matched %r (only the standalone token may match)" % (hit,)
    return True, ""


# ---------------------------------------------------------------------------------------------- patched-harness killers
_patch_spec = importlib.util.spec_from_file_location("patch_noop_control", fixture_path("patch_noop_control.py"))
_patch_mod = importlib.util.module_from_spec(_patch_spec)
_patch_spec.loader.exec_module(_patch_mod)
patch_noop = _patch_mod.patch_noop


def run_patched(mut_source, leg, mode="empty"):
    """-> (ok, detail): the patched harness must refuse the ineffective control (setup error, exit 2)."""
    d = tempfile.mkdtemp(prefix="patch.", dir=os.path.join(S, "work"))
    try:
        shutil.copyfile(DRIVER_SRC, os.path.join(d, "check-r56-controls.py"))
        with open(os.path.join(d, "r56_ctl_c3.py"), "wb") as fh:
            fh.write(patch_noop(mut_source, leg, mode).encode())
        w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "work"))
        try:
            cmd = [sys.executable, "-I", os.path.join(d, "check-r56-controls.py"), "--claim", "c3",
                   "--repo", MINI, "--rev", mini_sha(), "--work", w, "--counter", REAL_COUNTER]
            p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=w, timeout=900)
            out = p.stdout.decode("utf-8", "replace")
            err = p.stderr.decode("utf-8", "replace")
        finally:
            shutil.rmtree(w, ignore_errors=True)
        ok = (p.returncode == 2 and "ineffective" in err)
        return ok, "patched harness rc=%d stdout=%r stderr=%r" % (p.returncode, out.strip()[:120], err.strip().split("\n")[-1][:160])
    finally:
        shutil.rmtree(d, ignore_errors=True)


def kill_M36(mod, path):
    """the effectiveness check must reject a control whose mutation raises no leg.

    Fixture: the patched harness (fixtures/harness/patch-noop-control.py) with control 10 "noop-control"
    targeting the `missing` leg."""
    return run_patched(open(path, "rb").read(), "missing", "empty")


def kill_M37(mod, path):
    """same fixture as M36 (the effectiveness check is gone entirely)."""
    return run_patched(open(path, "rb").read(), "missing", "empty")


def kill_M38(mod, path):
    """the effectiveness check must cover the `dangling` leg too.

    Fixture: the patched harness with control 10 "noop-control" targeting the `dangling` leg."""
    return run_patched(open(path, "rb").read(), "dangling", "entry")


def kill_M44(mod, path):
    """the harness's own entry model must agree with the counter on the number of entries.

    Fixture: the lane tip's tree; the harness's stderr must not report an entries divergence."""
    w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "work"))
    try:
        cmd = [sys.executable, "-I", path, "--repo", MINI, "--rev", mini_sha(), "--work", w, "--counter", REAL_COUNTER]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=w, timeout=900)
        err = p.stderr.decode("utf-8", "replace")
    finally:
        shutil.rmtree(w, ignore_errors=True)
    bad = [l for l in err.split("\n") if "entries counter=" in l]
    if bad:
        return False, "the harness's model reports a different entry count than the counter: %r" % (bad[0][:140],)
    return True, ""


KILLERS = {
    "M13": (kill_M13, 1), "M15": (kill_M15, 1), "M24": (kill_M24, 1), "M25": (kill_M25, 1),
    "M26": (kill_M26, 1), "M27": (kill_M27, 1), "M29": (kill_M29, 1), "M30": (kill_M30, 1),
    "M32": (kill_M32, 1), "M52": (kill_M52, 1),
    "M36": (kill_M36, 2), "M37": (kill_M37, 2), "M38": (kill_M38, 2), "M44": (kill_M44, 2),
}
