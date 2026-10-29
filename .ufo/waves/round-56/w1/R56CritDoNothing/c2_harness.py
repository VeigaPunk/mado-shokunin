#!/usr/bin/env python3
"""Critic's C2 scorer over the 18 COMMITTED fixtures (hold-out H01-H08 is sealed and is not used here).

python3 -I c2_harness.py --base BASE_DIR --tool /abs/tool.py [--ablate X]... [--cmd-prefix ...] [--verbose]
Each fixture: args.json with {FX} -> absolute fixture dir; run `python3 -I <tool> [--ablate X] <args>` with cwd=BASE_DIR;
stdout bytes and exit status compared with expected.out / expected.rc (the registration's byte-for-byte rule).
"""
import argparse, json, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True)
ap.add_argument("--tool", required=True)
ap.add_argument("--ablate", action="append", default=[])
ap.add_argument("--verbose", action="store_true")
ap.add_argument("--raw-cmd", default="")  # for contract ctl stubs: tool is run as given, no ablate
A = ap.parse_args()
FIX = os.path.join(A.base, ".ufo/waves/round-56/fixtures/c2")
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1",
       "HOME": "/fast/scratch/hyaku/mado-r56/R56CritDoNothing/home", "TMPDIR": "/fast/scratch/hyaku/mado-r56/R56CritDoNothing"}
os.makedirs(ENV["HOME"], exist_ok=True)
ok = 0
names = sorted(os.listdir(FIX))
for name in names:
    fx = os.path.join(FIX, name)
    args = [a.replace("{FX}", fx) for a in json.load(open(os.path.join(fx, "args.json")))]
    abl = []
    for x in A.ablate:
        abl += ["--ablate", x]
    cmd = [sys.executable, "-I", A.tool, *abl, *args]
    r = subprocess.run(cmd, cwd=A.base, capture_output=True, env=ENV)
    exp_out = open(os.path.join(fx, "expected.out"), "rb").read()
    exp_rc = int(open(os.path.join(fx, "expected.rc")).read().strip())
    good = r.stdout == exp_out and r.returncode == exp_rc
    ok += good
    if A.verbose or not good:
        print(f"{name}: {'ok' if good else 'MISMATCH'} rc={r.returncode}/{exp_rc}")
        if not good and A.verbose:
            import difflib
            for l in difflib.unified_diff(exp_out.decode().splitlines(), r.stdout.decode().splitlines(), "expected", "got", lineterm="", n=0):
                print("   ", l)
            print("   stderr:", r.stderr.decode()[-300:])
print(f"CRITIC_C2: tool={os.path.basename(A.tool)} ablate={','.join(A.ablate) or 'none'} fixtures={ok}/{len(names)} "
      f"target={'MET' if ok == len(names) else 'MISSED'}")
