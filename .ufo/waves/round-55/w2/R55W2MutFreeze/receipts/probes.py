#!/usr/bin/env python3

"""Reproducible probes for the freeze-order mutation survivors (R55W2MutFreeze).

Run: python3 -I probes.py SCRATCH_DIR MUT_DIR BASELINE_CHECKER
Builds scratch git repos under SCRATCH_DIR (never touches the lane) and runs the baseline and mutant instruments.
"""
import json
import os
import subprocess
import sys
import tempfile

S, MUT, BASE = sys.argv[1], sys.argv[2], sys.argv[3]
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV["TMPDIR"] = S
B = ".ufo/waves/round-9"
FZ = {B + "/claims-frozen.md": "claims\n", B + "/registration.md": "reg\n", B + "/frozen-tables.json": "{}\n"}


def g(d, *a, env=None):
    e = dict(ENV)
    e.update(env or {})
    p = subprocess.run(["git", "-C", d] + list(a), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=e)
    assert p.returncode == 0, (a, p.stderr.decode())
    return p.stdout.decode().strip()


def commit(d, files, when, msg="c"):
    for rel, content in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(content)
    g(d, "add", "-A")
    g(d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--allow-empty", "-m", msg,
      env={"GIT_COMMITTER_DATE": when, "GIT_AUTHOR_DATE": when})
    return g(d, "rev-parse", "HEAD")


def repo(prefix):
    D = tempfile.mkdtemp(prefix=prefix, dir=S)
    g(D, "init", "-q", "--initial-branch=main")
    assert g(D, "rev-parse", "--show-toplevel") == os.path.realpath(D)
    return D


def run(instr, D, rnd="9", wave="w1", rev="HEAD"):
    p = subprocess.run(["python3", "-I", instr, "--repo", D, "--rev", rev, "--round", rnd, "--wave", wave,
                        "--work", S], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=ENV)
    return [p.returncode, p.stdout.decode().strip()]


out = {}
# A: M06 -- registry without a createdAt key; late freeze (17:11Z)
D = repo("probeA-")
commit(D, FZ, "2026-10-27T14:11:10-03:00", "freeze late")
commit(D, {B + "/w1/swarm-registry.json": json.dumps({"schema": "ufo-swarm-registry-v1", "wave": "w1"}) + "\n"},
       "2026-10-27T15:00:00-03:00", "registry no createdAt")
out["A_base_M06"] = [run(BASE, D), run(os.path.join(MUT, "M06.py"), D)]
# B: M07 -- createdAt without offset; freeze 17:00Z, naive launch 18:00
D = repo("probeB-")
commit(D, FZ, "2026-10-27T14:00:00-03:00", "freeze")
commit(D, {B + "/w1/swarm-registry.json": json.dumps({"schema": "x", "createdAt": "2026-10-27T18:00:00"}) + "\n"},
       "2026-10-27T15:00:00-03:00", "registry naive")
out["B_base_M07"] = [run(BASE, D), run(os.path.join(MUT, "M07.py"), D)]
# C: M12 -- HEAD root tree object deleted: ls-tree fails
D = repo("probeC-")
commit(D, FZ, "2026-10-27T10:00:00-03:00", "freeze")
commit(D, {B + "/w1/swarm-registry.json": json.dumps({"schema": "x", "createdAt": "2026-10-27T14:00:00.000Z"}) + "\n"},
       "2026-10-27T11:00:00-03:00", "registry")
tree = g(D, "rev-parse", "HEAD^{tree}")
os.remove(os.path.join(D, ".git", "objects", tree[:2], tree[2:]))
out["C_base_M12"] = [run(BASE, D), run(os.path.join(MUT, "M12.py"), D)]
# D: M05 -- drop --full-history; graph 1: merge brings freeze files from side branch
for tag, mutant in (("base", BASE), ("M05", os.path.join(MUT, "M05.py"))):
    D = repo("probeD-" + tag + "-")
    commit(D, {"README": "x\n"}, "2026-10-27T09:00:00-03:00", "root")
    g(D, "checkout", "-q", "-b", "side")
    commit(D, FZ, "2026-10-27T09:30:00-03:00", "side freeze")
    g(D, "checkout", "-q", "main")
    commit(D, {"main.txt": "m\n"}, "2026-10-27T09:40:00-03:00", "main work")
    g(D, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "merge", "-q", "--no-ff", "-m", "merge side", "side",
      env={"GIT_COMMITTER_DATE": "2026-10-27T13:00:00-03:00", "GIT_AUTHOR_DATE": "2026-10-27T13:00:00-03:00"})
    commit(D, {"README": "y\n"}, "2026-10-27T14:30:00-03:00", "tip")
    commit(D, {B + "/w1/swarm-registry.json": json.dumps({"schema": "x", "createdAt": "2026-10-27T14:00:00.000Z"}) + "\n"},
           "2026-10-27T14:31:00-03:00", "registry")
    out["D_graph1_" + tag] = run(mutant, D)
# E: M05 -- graph 2: main freeze 'old' then merge of side 'new' resolved to 'new'
for tag, mutant in (("base", BASE), ("M05", os.path.join(MUT, "M05.py"))):
    D = repo("probeE-" + tag + "-")
    commit(D, {"README": "x\n"}, "2026-10-27T09:00:00-03:00", "root")
    g(D, "checkout", "-q", "-b", "side")
    commit(D, dict(FZ, **{B + "/claims-frozen.md": "new\n"}), "2026-10-27T09:30:00-03:00", "side new")
    g(D, "checkout", "-q", "main")
    commit(D, FZ, "2026-10-27T10:00:00-03:00", "main old")
    subprocess.run(["git", "-C", D, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "merge", "--no-ff", "--no-commit", "side"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV)
    open(os.path.join(D, B + "/claims-frozen.md"), "w").write("new\n")
    g(D, "add", "-A")
    g(D, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "merge side",
      env={"GIT_COMMITTER_DATE": "2026-10-27T13:00:00-03:00", "GIT_AUTHOR_DATE": "2026-10-27T13:00:00-03:00"})
    commit(D, {"README": "y\n"}, "2026-10-27T14:30:00-03:00", "tip")
    commit(D, {B + "/w1/swarm-registry.json": json.dumps({"schema": "x", "createdAt": "2026-10-27T14:00:00.000Z"}) + "\n"},
           "2026-10-27T14:31:00-03:00", "registry")
    out["E_graph2_" + tag] = run(mutant, D)
print(json.dumps(out, indent=1))
