import concurrent.futures
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-43/w1/ExecC1ExtraMutants")
SCRATCH = "/fast/scratch/hyaku/mado-r43/ExecC1ExtraMutants"
REV = "b2e2efd6e268920d31f3c32cf52dc097dd6e1d22"
BASE = "a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f"
COUNTER = os.path.join(LANE, "quality/counters/c1-r42-geometry.py")

built = json.load(open(os.path.join(SEAT, "mutants.json")))


def run(m, k):
    name = m["name"]
    tmp = os.path.join(SCRATCH, "run", name)
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ, C1R42_TMP=tmp)
    p = subprocess.run(
        [sys.executable, "-I", COUNTER, "--repo", LANE, "--rev", REV, "--base", BASE,
         "--tool", os.path.join(SEAT, "mutants", name + ".py"),
         "--nonce", "exm43%04d" % k],
        capture_output=True, text=True, env=env, cwd=LANE)
    out = p.stdout
    final = [ln for ln in out.splitlines() if ln.startswith("PRED-C1-r42: fixtures=")]
    clauses = [ln for ln in out.splitlines() if " clauses=" in ln]
    fails = []
    for ln in out.splitlines():
        mm = re.match(r"PRED-C1-r42 fixture=(\S+) ok=0 (.*)", ln)
        if mm:
            fails.append("%s (%s)" % (mm.group(1), mm.group(2)[:80]))
        mm = re.match(r"PRED-C1-r42 clause=(b|b2|b3|g)\b.*", ln)
        if mm and ("killed=" in ln or "variant=" in ln or "sites=" in ln):
            fails.append("clause-" + mm.group(1) + ": " + ln.split("PRED-C1-r42 ")[1][:80])
    fl = final[-1] if final else "NO_FINAL_LINE rc=%d %s" % (p.returncode, out[-300:])
    cl = clauses[-1] if clauses else "NO_CLAUSES"
    met = "verdict=TARGET_MET" in fl
    return {"name": name, "category": m["category"], "old": m["old"], "new": m["new"],
            "final": fl, "clauses": cl, "met": met, "fails": fails, "rc": p.returncode}


res = []
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    futs = [ex.submit(run, m, k) for k, m in enumerate(built)]
    for f in concurrent.futures.as_completed(futs):
        r = f.result()
        res.append(r)
        print("%-30s %s" % (r["name"], r["final"].split("verdict=")[-1].split(" ")[0][:14]))
res.sort(key=lambda r: r["name"])
json.dump(res, open(os.path.join(SEAT, "results.json"), "w"), indent=1)
surv = [r for r in res if r["met"]]
print("\nMET=%d MISSED=%d" % (len(surv), len(res) - len(surv)))
for r in surv:
    print("SURVIVOR", r["name"], r["clauses"])
