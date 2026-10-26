#!/usr/bin/env python3
"""Score one tool file against the r44 fixture lattice (clause f) and its own selftest."""
import importlib.util, os, sys, tempfile, shutil, json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r44-geometry-states.py")
REV = sys.argv[2] if len(sys.argv) > 2 else "e2289516a9a857f55cda7be635933e89b931c3da"
NONCE = "simpaudit"
WORK = os.environ.get("SIMPCONTRACT_WORK") or os.path.join(tempfile.gettempdir(), "simpcontract-work")

spec = importlib.util.spec_from_file_location("c1r44", COUNTER)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
old = c.old
old.NONCE[0] = NONCE

def score(tool_path, label):
    os.makedirs(WORK, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="mut-", dir=WORK)
    os.chmod(tmp, 0o755)
    td = os.path.join(tmp, old.opaque("real"), "tool")
    os.makedirs(td)
    os.chmod(os.path.dirname(td), 0o755)
    os.chmod(td, 0o755)
    tool = os.path.join(td, "mado-geometry.py")
    shutil.copyfile(tool_path, tool)
    os.chmod(tool, 0o644)
    rc, k, n, has = old.selftest_result(tool, td)
    res = {"label": label, "selftest": [rc, k, n], "fail": [], "pass": 0, "total": 0}
    cases = [("sgen%d" % i, (lambda i=i: c.score_sgen(tool, tmp, REV, NONCE, i))) for i in range(c.N_GEN)]
    for name, fn in c.FIXED:
        cases.append((name, (lambda fn=fn: fn(tool, tmp, REV, NONCE))))
    for name, fn in cases:
        res["total"] += 1
        ok, why = fn()
        if ok:
            res["pass"] += 1
        else:
            res["fail"].append((name, why))
    shutil.rmtree(tmp, ignore_errors=True)
    return res

if __name__ == "__main__":
    r = score(sys.argv[1], os.path.basename(sys.argv[1]))
    print(json.dumps(r, indent=1)[:4000])
    print("SUMMARY %s fixtures=%d/%d selftest=%s fails=%s" % (
        r["label"], r["pass"], r["total"], r["selftest"],
        ",".join(x[0] for x in r["fail"]) or "-"))
