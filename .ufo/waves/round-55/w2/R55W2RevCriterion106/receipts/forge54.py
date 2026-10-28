import os, subprocess, json
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = "/fast/scratch/hyaku/mado-r55/R55W2RevCriterion106"
WORK = os.path.join(S, "work")
C = os.path.join(S, "clone54")
def sh(args, env=None, inp=None):
    e = dict(os.environ); e = {k: v for k, v in e.items() if not k.startswith("GIT_")}
    e.update(env or {})
    p = subprocess.run(args, capture_output=True, text=True, env=e, input=inp)
    if p.returncode != 0: raise SystemExit("FAIL %s\n%s" % (args, p.stderr))
    return p.stdout.strip()
if not os.path.isdir(C):
    sh(["git", "clone", "-q", "--no-checkout", LANE, C])
top = sh(["git", "-C", C, "rev-parse", "--show-toplevel"]); assert os.path.realpath(top) == os.path.realpath(C), top
TIP = "fe03bb3b2ec05fbf906b83096c637fd6a05b3dc8"
reg_path = ".ufo/waves/round-54/w1/swarm-registry.json"
doc = json.loads(sh(["git", "-C", C, "show", TIP + ":" + reg_path]))
doc["createdAt"] = "2026-10-27T18:00:00.000Z"; doc["updatedAt"] = doc["createdAt"]
blob = sh(["git", "-C", C, "hash-object", "-w", "--stdin"], inp=json.dumps(doc, indent=2) + "\n")
idx = os.path.join(S, "clone54.idx")
if os.path.exists(idx): os.remove(idx)
envi = {"GIT_INDEX_FILE": idx}
sh(["git", "-C", C, "read-tree", TIP], env=envi)
sh(["git", "-C", C, "update-index", "--cacheinfo", "100644,%s,%s" % (blob, reg_path)], env=envi)
tree = sh(["git", "-C", C, "write-tree"], env=envi)
cenv = {"GIT_AUTHOR_NAME": "ctl", "GIT_AUTHOR_EMAIL": "ctl@ctl", "GIT_COMMITTER_NAME": "ctl", "GIT_COMMITTER_EMAIL": "ctl@ctl",
        "GIT_AUTHOR_DATE": "2026-10-27T14:20:00-03:00", "GIT_COMMITTER_DATE": "2026-10-27T14:20:00-03:00"}
forged = sh(["git", "-C", C, "commit-tree", tree, "-p", TIP, "-m", "forged: createdAt moved after freeze"], env=cenv)
print("forged commit", forged, "parent", TIP)
print("diff vs tip:", sh(["git", "-C", C, "diff", "--stat", TIP, forged]))
for rev in [TIP, forged]:
    p = sh(["python3", "-I", os.path.join(LANE, "quality/check-freeze-order.py"), "--repo", C, "--rev", rev, "--round", "54", "--wave", "w1", "--work", WORK]) if False else None
import subprocess as sp
for rev in [TIP, forged]:
    r = sp.run(["python3", "-I", os.path.join(LANE, "quality/check-freeze-order.py"), "--repo", C, "--rev", rev, "--round", "54", "--wave", "w1", "--work", WORK], capture_output=True, text=True)
    print("rev=%s rc=%d %s" % (rev[:12], r.returncode, (r.stdout + r.stderr).strip()))
