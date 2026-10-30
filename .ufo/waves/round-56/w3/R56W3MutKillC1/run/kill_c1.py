#!/usr/bin/env python3
"""R56W3MutKillC1 -- land the C1 counter's kill power.

Rebuilds every survivor mutant named in the wave-2 reports
  .ufo/waves/round-56/w2/R56W2MutC1CounterA.md  (seat A namespace: M01..M67)
  .ufo/waves/round-56/w2/R56W2MutC1CounterB.md  (seat B namespace: M01..M71)
against the counter bytes at the lane tip 0f3a5436, materializes each report-proposed
killing fixture (one edit of the good tree) and VERIFIES that the fixture kills the
mutant.  Nothing in the lane is written: the lane is read through `git show`/`git archive`
only, all fixtures and mutants live in scratch.

Kill criterion (the wave-2 method, kept): the fixture kills the mutant when the mutant's
(rc, stdout) differs from the pristine counter's (rc, stdout) on the SAME fixture repo.
The direction is recorded: LEG_LOST (pristine reported a leg, the mutant does not ->
the mutant is too permissive) or LEG_ADDED (the pristine passed, the mutant reports a leg
-> the mutant is too strict).
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = "/fast/scratch/hyaku/mado-r56/R56W3MutKillC1"
BASE = os.path.join(ROOT, "base")
BASE_REV = open(os.path.join(ROOT, "BASE_REV.txt")).read().strip()
W2A = os.path.join(ROOT, "w2a")
W2B = os.path.join(ROOT, "w2b")
MUT_DIR = os.path.join(ROOT, "mutants")
FIX_STORE = os.path.join(ROOT, "fixtures")
WORK = os.path.join(ROOT, "work")
COUNTER_REL = "quality/counters/c1-r56-autoreload-entry.py"
ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
REG = "corpus/SOURCES.md"
README = "corpus/README.md"
TABLES = ".ufo/waves/round-56/frozen-tables-v2.json"
FETCH = ".ufo/waves/round-56/fetch"
EXPORT_PATHS = [ENTRY, REG, README, TABLES, FETCH]

ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8",
       "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_TERMINAL_PROMPT": "0", "GIT_NO_REPLACE_OBJECTS": "1"}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mutA = load("mutA", os.path.join(W2A, "mutate.py"))
killA = load("killA", os.path.join(W2A, "killers.py"))
mutB = load("mutB", os.path.join(W2B, "mutate.py"))
fixB = load("fixB", os.path.join(W2B, "fixtures.py"))


def git(d, *args, check=True):
    p = subprocess.run(["git", "-C", d] + list(args), env=dict(ENV, HOME=ROOT, TMPDIR=ROOT),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed in %s: %s" % (args, d, p.stderr.decode()[-300:]))
    return p.stdout.decode().strip()


def gitb(d, *args, check=True):
    p = subprocess.run(["git", "-C", d] + list(args), env=dict(ENV, HOME=ROOT, TMPDIR=ROOT),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed in %s: %s" % (args, d, p.stderr.decode()[-300:]))
    return p.stdout


# ------------------------------------------------------------------ counter bytes and mutants

PRISTINE_SRC = gitb(BASE, "show", "%s:%s" % (BASE_REV, COUNTER_REL)).decode("utf-8")
PRISTINE_PATH = os.path.join(ROOT, "pristine-counter.py")
with open(PRISTINE_PATH, "w", encoding="utf-8") as fh:
    fh.write(PRISTINE_SRC)


def mutant_a(mid):
    """Seat A namespace: (id, label, line, old, new) applied to the pristine line list."""
    spec = {m[0]: m for m in mutA.MUTANTS}[mid]
    _, label, lineno, old, new = spec
    lines, err = mutA.apply_mutant(PRISTINE_SRC.split("\n"), lineno, old, new)
    if err is not None:
        raise SystemExit("mutant %s does not apply at the lane tip: %s" % (mid, err))
    return label, "\n".join(lines)


def mutant_b(mid):
    """Seat B namespace: (id, area, old, new, note), whole-file single replacement."""
    spec = {m[0]: m for m in mutB.MUTANTS}[mid]
    _, area, old, new, note = spec
    n = PRISTINE_SRC.count(old)
    if n != 1:
        raise SystemExit("mutant %s: old text occurs %d times at the lane tip" % (mid, n))
    return "%s: %s" % (area, note), PRISTINE_SRC.replace(old, new)


def write_mutant(tag, src):
    os.makedirs(MUT_DIR, exist_ok=True)
    path = os.path.join(MUT_DIR, "%s.py" % tag)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)
    c = subprocess.run([sys.executable, "-I", "-m", "py_compile", path], capture_output=True)
    if c.returncode != 0:
        raise SystemExit("mutant %s does not compile: %s" % (tag, c.stderr.decode()[-300:]))
    return path


# ------------------------------------------------------------------ fixture construction

def export_base(dest):
    tar = os.path.join(ROOT, "_base.tar")
    with open(tar, "wb") as fh:
        subprocess.run(["git", "-C", BASE, "archive", BASE_REV, "--"] + EXPORT_PATHS,
                       stdout=fh, check=True, env=dict(ENV, HOME=ROOT))
    with tarfile.open(tar) as tf:
        tf.extractall(dest)
    os.remove(tar)


def build_fixture(tag, edit):
    """One edit of the good tree, committed with the ctl identity; returns (dir, sha, good_sha).

    The good tree is committed first so that the fixture diff is exactly the one edit.
    """
    d = tempfile.mkdtemp(prefix="fx-%s-" % tag.lower(), dir=WORK)
    export_base(d)
    git(d, "init", "-q", "-b", "main")
    top = git(d, "rev-parse", "--show-toplevel")
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit("toplevel mismatch %s %s" % (top, d))
    git(d, "add", "-A", "-f")
    git(d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "good tree")
    good = git(d, "rev-parse", "HEAD")
    edit(d)
    git(d, "add", "-A", "-f")
    git(d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "fixture %s" % tag)
    return d, git(d, "rev-parse", "HEAD"), good


def run_counter(counter, repo, rev, work):
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev, "--work", work],
                       cwd=work, env=dict(ENV, HOME=work, TMPDIR=work), capture_output=True,
                       timeout=600)
    return {"rc": p.returncode, "out": p.stdout.decode("utf-8", "replace").strip(),
            "err": p.stderr.decode("utf-8", "replace").strip()[-400:]}


def legs(out):
    if " missed=" not in out:
        return None
    m = out.rsplit(" missed=", 1)[1].strip()
    return [] if m == "none" else m.split(",")


def verdict_of(out):
    if " verdict=" in out:
        return out.rsplit(" verdict=", 1)[1].split()[0]
    return None


# ------------------------------------------------------------------ fixtures from seat A

killA.rd_tables_global[0] = gitb(BASE, "show", "%s:%s" % (BASE_REV, TABLES)).decode("utf-8")

FIXTURES = []
for fx_id, mids, attacks, edit, must_have, must_not in killA.FIXTURES:
    FIXTURES.append({"ns": "A", "fixture": fx_id, "mutants": mids.split(), "attacks": attacks,
                     "edit": edit, "must_have": must_have, "must_not": must_not,
                     "expect": "pristine reports " + (",".join(must_have) or "no leg")
                               + (" and not " + ",".join(must_not) if must_not else "")})
for fx_id, mid, desc, transform, expect in fixB.FIXTURES:
    FIXTURES.append({"ns": "B", "fixture": fx_id, "mutants": [mid], "attacks": desc,
                     "edit": transform, "must_have": [], "must_not": [],
                     "expect": "seat B expectation: " + expect})


def run_fixture(fx):
    tag = "%s-%s" % (fx["ns"], fx["fixture"])
    d, sha, good = build_fixture(tag, fx["edit"])
    try:
        w = os.path.join(WORK, "w-" + tag)
        pr = run_counter(PRISTINE_PATH, d, sha, os.path.join(w, "p"))
        pr_legs = legs(pr["out"])
        # the pristine expectation of the report: must_have legs present, must_not legs absent
        exp_ok = None
        if fx["ns"] == "A":
            exp_ok = (pr_legs is not None
                      and all(x in pr_legs for x in fx["must_have"])
                      and not any(x in pr_legs for x in fx["must_not"]))
        results = []
        for mid in fx["mutants"]:
            if fx["ns"] == "A":
                label, src = mutant_a(mid)
            else:
                label, src = mutant_b(mid)
            mp = write_mutant("%s-%s" % (tag, mid), src)
            mr = run_counter(mp, d, sha, os.path.join(w, "m-" + mid))
            mr_legs = legs(mr["out"])
            # the same mutant on the GOOD tree: does it misfire there (the harness good=bad route)?
            gr = run_counter(mp, BASE, BASE_REV, os.path.join(WORK, "g-" + tag + "-" + mid))
            differs = (mr["rc"], mr["out"]) != (pr["rc"], pr["out"])
            lost = sorted(set(pr_legs or []) - set(mr_legs or [])) if pr_legs is not None else []
            added = sorted(set(mr_legs or []) - set(pr_legs or [])) if mr_legs is not None else []
            if mr_legs is None and mr["rc"] != 0:
                direction = "CRASH (rc=%s, no counter line on stdout)" % mr["rc"]
            elif mr_legs is None:
                direction = "NO_COUNTER_LINE (rc=%s)" % mr["rc"]
            elif added:
                direction = "LEG_ADDED (mutant too strict: it reports a leg the pristine does not)"
            elif lost:
                direction = "LEG_LOST (mutant too permissive: it drops a leg the pristine reports)"
            elif mr["rc"] != pr["rc"]:
                direction = "RC_DIFF (%s vs %s)" % (pr["rc"], mr["rc"])
            else:
                direction = "OUTPUT_DIFF (same legs, different text)"
            results.append({"mutant": mid, "label": label, "rc": mr["rc"], "out": mr["out"],
                            "err": mr["err"], "legs": mr_legs, "killed": differs,
                            "direction": direction, "legs_lost": lost, "legs_added": added,
                            "good_tree": {"rc": gr["rc"], "out": gr["out"], "err": gr["err"],
                                          "legs": legs(gr["out"])}})
        # materialize the fixture as a binary-safe patch against the base tree
        patch = gitb(d, "diff", "--binary", good, sha)
        with open(os.path.join(FIX_STORE, tag + ".patch"), "wb") as fh:
            fh.write(patch)
        return {"ns": fx["ns"], "fixture": fx["fixture"], "attacks": fx["attacks"],
                "expect": fx["expect"], "repo_sha": sha, "patch": tag + ".patch",
                "pristine_expectation_holds": exp_ok,
                "pristine": {"rc": pr["rc"], "out": pr["out"], "err": pr["err"], "legs": pr_legs},
                "mutants": results}
    finally:
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(os.path.join(WORK, "w-" + tag), ignore_errors=True)


def run_m69():
    """Seat B's CLI-level survivor: --rev <tree oid> instead of a commit."""
    tree = git(BASE, "rev-parse", "%s^{tree}" % BASE_REV)
    label, src = mutant_b("M69")
    mp = write_mutant("B-F69-M69", src)
    w = os.path.join(WORK, "w-B-F69")
    pr = run_counter(PRISTINE_PATH, BASE, tree, os.path.join(w, "p"))
    mr = run_counter(mp, BASE, tree, os.path.join(w, "m"))
    return {"ns": "B", "fixture": "F69", "attacks": "CLI: --rev <tree oid> (not a commit)",
            "expect": "pristine: setup error rc=2 (rev must be a commit); mutant: rc 0 TARGET_MET",
            "repo_sha": tree, "patch": None, "pristine_expectation_holds": pr["rc"] == 2,
            "pristine": {"rc": pr["rc"], "out": pr["out"], "err": pr["err"], "legs": legs(pr["out"])},
            "mutants": [{"mutant": "M69", "label": label, "rc": mr["rc"], "out": mr["out"],
                         "err": mr["err"], "legs": legs(mr["out"]),
                         "killed": (mr["rc"], mr["out"]) != (pr["rc"], pr["out"]),
                         "direction": "RC_DIFF (%s vs %s)" % (pr["rc"], mr["rc"]),
                         "legs_lost": [], "legs_added": []}]}


def roundtrip(tag):
    """Apply the materialized patch to a fresh export of the base tree; the result must equal the fixture tree."""
    d = tempfile.mkdtemp(prefix="rt-%s-" % tag.lower(), dir=WORK)
    try:
        export_base(d)
        p = subprocess.run(["git", "init", "-q", "-b", "main"], cwd=d, env=dict(ENV, HOME=ROOT),
                           capture_output=True)
        if p.returncode != 0:
            return {"ok": False, "detail": "git init failed"}
        q = subprocess.run(["git", "apply", "--binary", "--whitespace=nowarn",
                            os.path.join(FIX_STORE, tag + ".patch")], cwd=d,
                           env=dict(ENV, HOME=ROOT), capture_output=True)
        if q.returncode != 0:
            return {"ok": False, "detail": "git apply failed: %s" % q.stderr.decode()[-200:]}
        git(d, "add", "-A", "-f")
        git(d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "-c", "commit.gpgsign=false",
            "commit", "-q", "-m", "roundtrip %s" % tag)
        tree = git(d, "rev-parse", "HEAD^{tree}")
        return {"ok": True, "tree": tree}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def kill_matrix(mutants, fixtures):
    """Every named survivor mutant against every fixture: which fixtures kill which mutant."""
    import concurrent.futures as cf
    fxdirs = {}
    for fx in fixtures:
        tag = "%s-%s" % (fx["ns"], fx["fixture"])
        d, sha, good = build_fixture(tag, fx["edit"])
        fxdirs[tag] = (d, sha)
    matrix = {}
    try:
        def one(job):
            tag, mid, ns = job
            d, sha = fxdirs[tag]
            if ns == "A":
                label, src = mutant_a(mid)
            else:
                label, src = mutant_b(mid)
            mp = write_mutant("mtx-%s-%s-%s" % (tag, ns, mid), src)
            pr = run_counter(PRISTINE_PATH, d, sha, os.path.join(WORK, "mtx-%s-p" % tag))
            mr = run_counter(mp, d, sha, os.path.join(WORK, "mtx-%s-%s-%s" % (tag, ns, mid)))
            return (tag, ns, mid, (mr["rc"], mr["out"]) != (pr["rc"], pr["out"]),
                    verdict_of(mr["out"]) or ("rc=%s" % mr["rc"]),
                    (mr["out"] or mr["err"])[:120])
        jobs = [(tag, mid, ns) for tag in fxdirs for (ns, mid) in mutants]
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            for tag, ns, mid, killed, v, out in ex.map(one, jobs):
                matrix.setdefault(tag, {})["%s:%s" % (ns, mid)] = {"killed": killed,
                                                                  "verdict": v, "out": out}
        return matrix
    finally:
        for d, _ in fxdirs.values():
            shutil.rmtree(d, ignore_errors=True)


def main():
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(FIX_STORE, exist_ok=True)
    # baseline: the pristine counter on the unmutated base tree must be green
    base_run = run_counter(PRISTINE_PATH, BASE, BASE_REV, os.path.join(WORK, "base"))
    print("BASE rc=%s %s" % (base_run["rc"], base_run["out"]), flush=True)
    out = []
    for fx in FIXTURES:
        try:
            rec = run_fixture(fx)
        except SystemExit as e:
            rec = {"ns": fx["ns"], "fixture": fx["fixture"], "attacks": fx["attacks"],
                   "expect": fx["expect"], "error": str(e), "mutants": []}
        out.append(rec)
        st = "ERROR" if "error" in rec else " ".join(
            "%s:%s" % (m["mutant"], "KILLED" if m["killed"] else "SURVIVED") for m in rec["mutants"])
        print("%-3s %-4s %s" % (rec["ns"], rec["fixture"], st), flush=True)
        if "error" in rec:
            print("     ERROR %s" % rec["error"], flush=True)
        else:
            print("     pristine rc=%s %s" % (rec["pristine"]["rc"], rec["pristine"]["out"][:240]),
                  flush=True)
            for m in rec["mutants"]:
                print("     %-4s rc=%s %s" % (m["mutant"], m["rc"],
                                             (m["out"] or m["err"])[:240]), flush=True)
                print("          %s %s" % (m["direction"],
                                          ("lost=" + ",".join(m["legs_lost"]) if m["legs_lost"] else "")
                                          + (" added=" + ",".join(m["legs_added"]) if m["legs_added"] else "")),
                      flush=True)
    # seat B's CLI-level survivor (M69) is not a tree fixture
    try:
        rec = run_m69()
    except SystemExit as e:
        rec = {"ns": "B", "fixture": "F69", "attacks": "CLI", "expect": "CLI", "error": str(e),
               "mutants": []}
    out.append(rec)
    st = "ERROR" if "error" in rec else " ".join(
        "%s:%s" % (m["mutant"], "KILLED" if m["killed"] else "SURVIVED") for m in rec["mutants"])
    print("%-3s %-4s %s" % (rec["ns"], rec["fixture"], st), flush=True)
    if "error" in rec:
        print("     ERROR %s" % rec["error"], flush=True)
    else:
        print("     pristine rc=%s %s %s" % (rec["pristine"]["rc"], rec["pristine"]["out"][:120],
                                             rec["pristine"]["err"][:120]), flush=True)
        for m in rec["mutants"]:
            print("     %-4s rc=%s %s" % (m["mutant"], m["rc"], (m["out"] or m["err"])[:200]), flush=True)

    # round-trip: each materialized patch must reproduce the fixture tree exactly
    print("\n== ROUNDTRIP ==", flush=True)
    rt = {}
    for r in out:
        if not r.get("patch"):
            continue
        tag = "%s-%s" % (r["ns"], r["fixture"])
        res = roundtrip(tag)
        rt[tag] = res
        print("%-8s %s" % (tag, "OK" if res["ok"] else "FAIL " + res.get("detail", "")), flush=True)

    # kill-power matrix: every named survivor mutant against every fixture
    print("\n== KILL MATRIX (all named survivors x all fixtures) ==", flush=True)
    named = []
    for fx in FIXTURES:
        for mid in fx["mutants"]:
            named.append((fx["ns"], mid))
    named.append(("B", "M69"))
    matrix = kill_matrix(named, FIXTURES)
    for tag in sorted(matrix):
        killed = sorted(k for k, v in matrix[tag].items() if v["killed"])
        print("%-8s kills %2d/%d %s" % (tag, len(killed), len(named), ",".join(killed)), flush=True)

    path = os.path.join(ROOT, "kill-results.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"base_rev": BASE_REV,
                   "base_run": base_run,
                   "counter_sha256": hashlib.sha256(PRISTINE_SRC.encode()).hexdigest(),
                   "roundtrip": rt,
                   "kill_matrix": matrix,
                   "results": out}, fh, indent=1, ensure_ascii=False)
    pairs = [(r["ns"], r["fixture"], m["mutant"], m["killed"]) for r in out
             for m in r.get("mutants", [])]
    print("\nPAIRS %d  KILLED %d  SURVIVED %d  ERRORS %d" % (
        len(pairs), sum(1 for p in pairs if p[3]), sum(1 for p in pairs if not p[3]),
        sum(1 for r in out if "error" in r)))
    print("results: %s" % path)


if __name__ == "__main__":
    main()
