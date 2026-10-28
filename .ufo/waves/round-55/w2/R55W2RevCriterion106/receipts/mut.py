import os, subprocess, json, shutil
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = "/fast/scratch/hyaku/mado-r55/R55W2RevCriterion106"
WORK = os.path.join(S, "work"); os.makedirs(WORK, exist_ok=True)
MD = os.path.join(S, "mut"); os.makedirs(MD, exist_ok=True)
src = open(os.path.join(LANE, "quality/check-freeze-order.py")).read()
needle = '["show", "-s", "--format=%cI", anchor]'
assert src.count(needle) == 1, src.count(needle)
mut = src.replace(needle, '["show", "-s", "--format=%aI", anchor]')
open(os.path.join(MD, "check-freeze-order-AI.py"), "w").write(mut)
def sh(args, cwd=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()
print("mutant selftest:", sh(["python3", "-I", os.path.join(MD, "check-freeze-order-AI.py"), "--selftest", "--work", WORK])[0])
rc, out = sh(["python3", "-I", os.path.join(MD, "check-freeze-order-AI.py"), "--selftest", "--work", WORK])
fails = [l for l in out.splitlines() if l.startswith("FAIL") or "MISMATCH" in l or "Traceback" in l or ("PASS" not in l and l.strip() and not l.startswith("    ") and "MADO_FREEZE_ORDER" not in l)]
print("\n".join(out.splitlines()[-12:]))
print("MUTANT_SELFTEST_RC=", rc)
print("non-PASS lines (first 12):"); print("\n".join(fails[:12]))
# the real-data round-54 verdict under the %aI mutant (copy, in scratch) vs the unchanged instrument
print("mutant r54 @fe03bb3b:", sh(["python3", "-I", os.path.join(MD, "check-freeze-order-AI.py"), "--repo", LANE, "--rev", "fe03bb3b2ec05fbf906b83096c637fd6a05b3dc8", "--round", "54", "--wave", "w1", "--work", WORK]))
print("author time of freeze 350d30e4:", sh(["git", "-C", LANE, "show", "-s", "--format=%aI %cI", "350d30e4ec5531f65ce99a57efeb8216f38e678a"])[1])
