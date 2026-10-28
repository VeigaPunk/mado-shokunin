import json, os, subprocess, sys
# usage: python3 -I harness.py <root> <tool.py>   (root = scratch tree containing .ufo/waves/round-55/fixtures)
root, tool = sys.argv[1], sys.argv[2]
base = os.path.join(root, ".ufo/waves/round-55/fixtures")
fx = [("c2", "F%02d" % i) for i in range(1, 19)] + [("c2-holdout", "H%02d" % i) for i in range(1, 9)]
res = {}
for grp, fid in fx:
    d = os.path.join(base, grp, fid)
    args = json.load(open(os.path.join(d, "args.json")))
    exp_out = open(os.path.join(d, "expected.out"), "rb").read()
    exp_rc = int(open(os.path.join(d, "expected.rc")).read().strip())
    p = subprocess.run([sys.executable, "-I", tool] + args, cwd=root, capture_output=True, timeout=60)
    ok = (p.stdout == exp_out and p.returncode == exp_rc)
    res[fid] = ok
st = subprocess.run([sys.executable, "-I", tool, "--selftest"], cwd=root, capture_output=True, timeout=60)
sline = st.stdout.decode("utf-8", "replace").strip()
selftest_clean = (st.returncode == 0 and sline.startswith("MADO_KBDOPT_SELFTEST:"))
killed_fx = [k for k, v in res.items() if not v]
print(json.dumps({"tool": tool, "killed_fixtures": killed_fx, "fixtures_passed": 26 - len(killed_fx),
                  "selftest_line": sline, "selftest_rc": st.returncode,
                  "selftest_killed": not selftest_clean, "selftest_stderr": st.stderr.decode("utf-8","replace")[-400:]}))
