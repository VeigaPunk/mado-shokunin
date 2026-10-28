import json, os, subprocess, sys
MUT = sys.argv[1]   # mutants dir (contains original/ and M*/)
ORIG = os.path.join(MUT, "original", "mado-kbdopts.py")
res = {}
for mid in sorted(d for d in os.listdir(MUT) if d.startswith("M") and os.path.isdir(os.path.join(MUT, d, "kill"))):
    kd = os.path.join(MUT, mid, "kill")
    argv = json.load(open(os.path.join(kd, "argv.json")))
    exp = open(os.path.join(kd, "expected.out"), "rb").read()
    def go(tool):
        p = subprocess.run([sys.executable, "-I", tool] + argv, cwd=kd, capture_output=True, timeout=60)
        return p.stdout, p.returncode, p.stderr.decode().strip().splitlines()[-1:] 
    o, orc, _ = go(ORIG)
    m, mrc, merr = go(os.path.join(MUT, mid, "mado-kbdopts.py"))
    status = "ORIG_MATCHES_HAND_EXPECTED" if (o == exp and orc == 0) else "ORIG_MISMATCH"
    killed = (m != o) or (mrc != orc)
    res[mid] = {"orig_rc": orc, "mut_rc": mrc, "orig_out": o.decode(), "mut_out": m.decode(), "mut_stderr_tail": merr, "status": status, "killed": killed}
    print("%s killed=%s status=%s" % (mid, killed, status))
    print("  orig rc=%d:" % orc, o.decode().replace("\n", " | "))
    print("  mut  rc=%d:" % mrc, m.decode().replace("\n", " | "), merr)
json.dump(res, open(os.path.join(MUT, "repro-results.json"), "w"), indent=1)
