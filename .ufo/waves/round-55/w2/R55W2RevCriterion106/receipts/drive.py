import os, subprocess, sys, json, shutil
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = "/fast/scratch/hyaku/mado-r55/R55W2RevCriterion106"
CHECK = os.path.join(LANE, "quality/check-freeze-order.py")  # unchanged instrument, read from lane (read-only use)
WORK = os.path.join(S, "work")
os.makedirs(WORK, exist_ok=True)

def env_for(date):
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update({"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date,
              "GIT_AUTHOR_NAME": "ctl", "GIT_AUTHOR_EMAIL": "ctl@ctl",
              "GIT_COMMITTER_NAME": "ctl", "GIT_COMMITTER_EMAIL": "ctl@ctl"})
    return e

def run(args, date=None, cwd=None):
    p = subprocess.run(args, cwd=cwd, env=env_for(date or "2026-10-27T10:00:00-03:00"),
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("FAILED %s\n%s" % (args, p.stderr))
    return p.stdout

def mkrepo():
    D = os.path.realpath(os.path.join(S, "fx-" + str(len(os.listdir(S)))))
    os.makedirs(D, exist_ok=False)
    run(["git", "-C", D, "init", "-q", "--initial-branch=main"])
    top = run(["git", "-C", D, "rev-parse", "--show-toplevel"]).strip()
    assert os.path.realpath(top) == D, (top, D)
    return D

def commit(D, date, files=None, rm=(), msg="c"):
    for rel, content in (files or {}).items():
        p = os.path.join(D, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(content)
    for rel in rm:
        os.remove(os.path.join(D, rel))
    run(["git", "-C", D, "add", "-A"], date)
    run(["git", "-C", D, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--allow-empty", "-m", msg], date)
    return run(["git", "-C", D, "rev-parse", "HEAD"]).strip()

def check(D, rev, rnd, wave):
    p = subprocess.run(["python3", "-I", CHECK, "--repo", D, "--rev", rev, "--round", str(rnd), "--wave", wave, "--work", WORK],
                       capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()

FREEZE = {
 ".ufo/waves/round-55/claims-frozen.md": "# claims v1\nPRED-C1-r55: entry needs 18 K rows\n",
 ".ufo/waves/round-55/registration.md": "# registration v1\nK16 quote: X\n",
 ".ufo/waves/round-55/frozen-tables.json": "{\"K16\": \"X\"}\n",
}
LAUNCH = "2026-10-27T16:00:00.000Z"
def base(D):
    c1 = commit(D, "2026-10-27T10:00:00-03:00", FREEZE, msg="freeze v1")
    c2 = commit(D, "2026-10-27T13:30:00-03:00", {".ufo/waves/round-55/w1/swarm-registry.json": json.dumps({"createdAt": LAUNCH, "updatedAt": LAUNCH, "wave": "w1"}) + "\n"}, msg="w1 registry")
    return c1, c2

out = []
def rec(name, rc, txt):
    out.append("== %s\nrc=%d\n%s" % (name, rc, txt))
    print("== %s rc=%d\n%s" % (name, rc, txt))

# A. post-launch errata under a NEW filename (round-55 pattern: registration-v2.md, frozen-tables-v2.json)
D = mkrepo(); c1, c2 = base(D)
c3 = commit(D, "2026-10-27T14:00:00-03:00", {
  ".ufo/waves/round-55/registration-v2.md": "# registration v2\nK16 quote: Y (errata after launch)\n",
  ".ufo/waves/round-55/frozen-tables-v2.json": "{\"K16\": \"Y\"}\n"}, msg="errata v2 after w1 launch")
rec("A1 post-launch errata under new filenames, tip=%s" % c3[:12], *check(D, c3, 55, "w1"))
# A-control: same predicate change made IN PLACE to registration.md (the instrument's own freeze set)
D2 = mkrepo(); c1b, c2b = base(D2)
c3b = commit(D2, "2026-10-27T14:00:00-03:00", {".ufo/waves/round-55/registration.md": "# registration v1\nK16 quote: Y (in-place edit)\n"}, msg="in-place edit")
rec("A-ctl in-place edit of registration.md after launch, tip=%s" % c3b[:12], *check(D2, c3b, 55, "w1"))

# B. optional freeze file DELETED after launch
D3 = mkrepo(); c1c, c2c = base(D3)
c3c = commit(D3, "2026-10-27T14:00:00-03:00", rm=[".ufo/waves/round-55/frozen-tables.json"], msg="delete frozen-tables after launch")
rec("B1 frozen-tables.json deleted after launch, tip=%s" % c3c[:12], *check(D3, c3c, 55, "w1"))
# B-ctl: required file deleted after launch
D4 = mkrepo(); c1d, c2d = base(D4)
c3d = commit(D4, "2026-10-27T14:00:00-03:00", rm=[".ufo/waves/round-55/registration.md"], msg="delete registration after launch")
rec("B-ctl registration.md deleted after launch, tip=%s" % c3d[:12], *check(D4, c3d, 55, "w1"))

# C. forged createdAt: a commit AFTER launch that rewrites only the registry's createdAt to a later instant
c4 = commit(D3, "2026-10-27T14:00:00-03:00", {".ufo/waves/round-55/w1/swarm-registry.json": json.dumps({"createdAt": "2026-10-27T15:00:00.000Z", "updatedAt": "2026-10-27T15:00:00.000Z", "wave": "w1"}) + "\n"}, msg="registry createdAt rewritten after launch")
rec("C1 registry createdAt rewritten later (freeze c1 at 10:00-03, original launch 13:00Z), tip=%s" % c4[:12], *check(D3, c4, 55, "w1"))


D5 = mkrepo()
r0 = commit(D5, "2026-10-27T13:30:00-03:00", {".ufo/waves/round-55/w1/swarm-registry.json": json.dumps({"createdAt": LAUNCH, "updatedAt": LAUNCH, "wave": "w1"}) + "\n"}, msg="w1 registry (launch 13:00-03)")
f0 = commit(D5, "2026-10-27T14:00:00-03:00", FREEZE, msg="late freeze after launch")
rec("C-honest late freeze (committer 14:00-03 > launch 13:00-03), tip=%s" % f0[:12], *check(D5, f0, 55, "w1"))
f1 = commit(D5, "2026-10-27T14:05:00-03:00", {".ufo/waves/round-55/w1/swarm-registry.json": json.dumps({"createdAt": "2026-10-27T18:00:00.000Z", "updatedAt": "2026-10-27T18:00:00.000Z", "wave": "w1"}) + "\n"}, msg="registry createdAt rewritten after freeze")
rec("C-forged: createdAt rewritten to 18:00Z after the late freeze, tip=%s" % f1[:12], *check(D5, f1, 55, "w1"))

open(os.path.join(S, "attack", "fixture-results.txt"), "w").write("\n".join(out) + "\n")
