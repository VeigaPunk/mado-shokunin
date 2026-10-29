# Mimics the frozen C2 harness contract ({FX} substitution, child process, cwd = export root, byte + rc compare).
import json, os, subprocess, sys
exp, tool = sys.argv[1], sys.argv[2]
ok = {}
for grp in ("fixtures/c2", "fixtures/c2-holdout"):
    base = os.path.join(exp, grp)
    if not os.path.isdir(base): continue
    for fx in sorted(os.listdir(base)):
        d = os.path.join(base, fx)
        if not os.path.isfile(os.path.join(d, "args.json")): continue
        args = [a.replace("{FX}", d) for a in json.load(open(os.path.join(d, "args.json")))]
        p = subprocess.run([sys.executable, "-I", tool, *args], cwd=exp, capture_output=True, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"})
        want = open(os.path.join(d, "expected.out"), "rb").read()
        rc = int(open(os.path.join(d, "expected.rc")).read().strip())
        ok.setdefault(grp, [0, 0]); ok[grp][1] += 1
        ok[grp][0] += (p.stdout == want and p.returncode == rc)
print({k: f"{v[0]}/{v[1]}" for k, v in ok.items()})
