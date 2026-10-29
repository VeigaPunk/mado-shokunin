#!/usr/bin/env python3
"""Build the two C3 witnesses and counter variants under --work, run the harness on them, print results.
   python3 -I build_witness.py --lane LANE --work WORK [--keep]   (writes only under WORK; removes it at the end)"""
import os, re, shutil, subprocess, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.join(os.path.dirname(HERE), "r56_ctl_c3.py")
sys.path.insert(0, os.path.dirname(HERE))
import r56_ctl_c3 as H

o = dict(zip(sys.argv[1::2], sys.argv[2::2]))
lane, work = o["--lane"], os.path.abspath(o["--work"])
os.makedirs(work, exist_ok=True)
ENV = H.git_env(work)


def sh(*a, d=None, inp=None):
    p = subprocess.run(list(a), cwd=d, input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV)
    if p.returncode:
        raise SystemExit("FAILED %r: %s" % (a, p.stderr.decode()))
    return p.stdout


def init(name):
    d = os.path.join(work, name)
    os.makedirs(d)
    sh("git", "-C", d, "init", "-q")
    assert os.path.realpath(sh("git", "-C", d, "rev-parse", "--show-toplevel").decode().strip()) == os.path.realpath(d)
    with open(os.path.join(d, ".git/objects/info/alternates"), "w") as f:  # makes the frozen base object readable
        f.write(os.path.join(lane, ".git/objects") + "\n")
    return d


def commit(d):
    sh("git", "-C", d, "add", "-A", "-f", ".")
    sh("git", "-C", d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "witness")
    return sh("git", "-C", d, "rev-parse", "HEAD").decode().strip()


def tables(d):
    p = os.path.join(d, H.TABLES_PATH)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    blob = sh("git", "-C", lane, "show", "3423ae285676c2a10273000f4519163472b443db:" + H.TABLES_PATH)
    assert hashlib.sha256(blob).hexdigest() == H.TABLES_SHA256
    open(p, "wb").write(blob)


base = "13f0acbe3a15da2d9c08357a576d91dcadc85273"
# ---- witness A: the REAL base corpus with used-by fixed so missing=0 (extra=0, dangling=0)
A = init("wA")
tar = sh("git", "-C", lane, "archive", "--format=tar", base, "corpus")
sh("tar", "-x", "-C", A, inp=tar)
tables(A)
src = open(os.path.join(A, "corpus/SOURCES.md"), "rb").read().decode()
ents = {"corpus/knowledge/" + n: open(os.path.join(A, "corpus/knowledge", n), "rb").read().decode()
        for n in os.listdir(os.path.join(A, "corpus/knowledge")) if n.endswith(".md")}
lines, rows = H.parse_registry(src)
ub = {sid: set(H.USEDBY_RE.findall(c)) for _, sid, c in rows}
add = {}
for p, t in ents.items():
    for s in set(x for _, x in H.cite_lines(t)):
        if s in ub and p not in ub[s]:
            add.setdefault(s, []).append(p)
for i, sid, cell in rows:
    if sid in add:
        H.set_usedby(lines, i, cell.rstrip() + " " + " ".join(sorted(add[sid])) + " ")
open(os.path.join(A, "corpus/SOURCES.md"), "w").write("\n".join(lines))
print("witness A fix: %d (row,entry) additions over %d rows; metrics after: %r" % (
    sum(map(len, add.values())), len(add), H.metrics("\n".join(lines), ents)))
revA = commit(A)

# ---- witness B: small synthetic tree (6 rows, 4 entries, one fenced citation, one prose non-row id)
B = init("wB")
tables(B)
os.makedirs(os.path.join(B, "corpus/knowledge"))
hdr = "# SOURCES\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
def row(i, ub): return "| S%03d | src %d | docs | A | sc | a:1-2 | t | mined | 2026-10-28 | none | %s |\n" % (i, i, ub)
K = "corpus/knowledge/"
open(os.path.join(B, "corpus/SOURCES.md"), "w").write(hdr + row(1, "`%salpha.md`, `%sbeta.md`" % (K, K)) + row(2, "`%salpha.md`" % K)
    + row(3, "`%sbeta.md` `%sgamma.md`" % (K, K)) + row(4, "—") + row(5, "`%sdelta.md`" % K) + row(6, "`%sgamma.md`" % K))
def ent(n, body): open(os.path.join(B, "corpus/knowledge", n + ".md"), "w").write(body)
ent("alpha", "# alpha\n\nsource: S001, S002\nverified-at: 2026-10-28\n\nclaim cites S001 and S002.\n")
ent("beta", "# beta\n\nsource: S001 S003\n\nthe draft id S243 is not a row.\n\n```\nS004 inside a fence is not a citation\n```\n")
ent("gamma", "# gamma\n\nsource: S003\n\ntext cites S006 once.\n")
ent("delta", "# delta\n\nsource: S005\n\nonly delta.\n")
revB = commit(B)

# ---- counter variants
def variant(name, mode):
    s = open(os.path.join(HERE, "ref_counter.py")).read().replace('MODE = "full"', 'MODE = "%s"' % mode)
    p = os.path.join(work, name + ".py")
    open(p, "w").write(s)
    return p
counters = [("ref", os.path.join(HERE, "ref_counter.py")), ("always_green", variant("always_green", "always_green")),
            ("missing_only", variant("missing_only", "missing_only")), ("no_fence", variant("no_fence", "no_fence")),
            ("always_red", variant("always_red", "always_red"))]
def stub_exit0(): p = os.path.join(work, "exit0_noline.py"); open(p, "w").write("import sys\nsys.exit(0)\n"); return p
counters.append(("silent_exit0", stub_exit0()))
for wname, d, rev in (("witnessA", A, revA), ("witnessB", B, revB)):
    for cname, cpath in counters:
        p = subprocess.run([sys.executable, "-I", HARNESS, "--repo", d, "--rev", rev, "--work", os.path.join(work, "hw"), "--counter", cpath],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("== %s counter=%s rc=%d" % (wname, cname, p.returncode))
        print("   stdout:", p.stdout.decode().strip() or "(empty)")
        for ln in p.stderr.decode().splitlines():
            print("   |", ln[:230])
