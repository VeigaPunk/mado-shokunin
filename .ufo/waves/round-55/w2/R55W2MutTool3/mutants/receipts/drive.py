import json, os, subprocess, sys
ROOT = "/fast/scratch/hyaku/mado-r55/R55W2MutTool3"
FIX = os.path.join(ROOT, ".ufo/waves/round-55/fixtures")
ids = []
for grp, name in (("c2", "F"), ("c2-holdout", "H")):
    base = os.path.join(FIX, grp)
    for d in sorted(os.listdir(base)):
        ids.append((d, os.path.join(base, d)))
assert len(ids) == 26, len(ids)

def run(tool, argv):
    try:
        p = subprocess.run([sys.executable, "-I", tool] + argv, cwd=ROOT, capture_output=True, timeout=60)
        return p.stdout, p.returncode, p.stderr.decode("utf-8", "replace")[-300:]
    except subprocess.TimeoutExpired:
        return b"<TIMEOUT>", -999, ""

def score(tool, pristine_selftest):
    killed, detail = [], {}
    for fid, d in ids:
        argv = json.load(open(os.path.join(d, "args.json")))
        exp_out = open(os.path.join(d, "expected.out"), "rb").read()
        exp_rc = int(open(os.path.join(d, "expected.rc")).read().strip())
        out, rc, err = run(tool, argv)
        ok = out == exp_out and rc == exp_rc
        if not ok:
            killed.append(fid)
            detail[fid] = {"rc": rc, "stdout": out.decode("utf-8", "replace")[:400], "stderr_tail": err}
    st_out, st_rc, st_err = run(tool, ["--selftest"])
    st_killed = st_rc != 0 or st_out != pristine_selftest
    return {"fixtures_killed": killed, "n_killed": len(killed), "selftest_killed": st_killed,
            "selftest_out": st_out.decode("utf-8", "replace").strip(), "selftest_rc": st_rc,
            "detail": detail}

if __name__ == "__main__":
    tool = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--baseline":
        out, rc, _ = run(tool, ["--selftest"])
        res = {}
        for fid, d in ids:
            argv = json.load(open(os.path.join(d, "args.json")))
            o, r, _ = run(tool, argv)
            res[fid] = (o == open(os.path.join(d, "expected.out"), "rb").read() and r == int(open(os.path.join(d, "expected.rc")).read()))
        print(json.dumps({"selftest": out.decode().strip(), "rc": rc, "fixtures_pass": sum(res.values()), "fail": [k for k, v in res.items() if not v]}))
    else:
        pristine_st = run(os.path.join(ROOT, "tools/mado-kbdopts.py"), ["--selftest"])[0]
        print(json.dumps(score(tool, pristine_st), indent=1, sort_keys=True))
