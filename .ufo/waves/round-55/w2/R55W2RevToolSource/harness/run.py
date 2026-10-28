import subprocess, json, os
C = "/fast/scratch/hyaku/mado-r55/R55W2RevToolSource/cases"
H = "/fast/scratch/hyaku/mado-r55/R55W2RevToolSource/harness/harness14"
T = "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-kbdopts.py"
kbs = json.load(open(os.path.join(C, "kbs.json")))
out = []
for n in sorted(kbs):
    if n.startswith("c14") or not n.startswith("c"): continue
    cfg = os.path.join(C, n + ".conf")
    k = kbs[n] or []
    hk = k if k else []
    h = subprocess.run([H, cfg] + hk, capture_output=True, text=True, cwd=C, timeout=60)
    targs = ["python3", "-I", T, "--config", cfg]
    for kb in k: targs += ["--keyboard", kb]
    if not k: targs += ["--keyboard", "*"]
    t = subprocess.run(targs, capture_output=True, text=True, cwd=C, timeout=60)
    out.append("== " + n)
    out.append(h.stdout.rstrip() + ("  [rc=%d]" % h.returncode if h.returncode else ""))
    out.append(t.stdout.rstrip() + ("  [rc=%d]" % t.returncode if t.returncode else ""))
print("\n".join(out))
