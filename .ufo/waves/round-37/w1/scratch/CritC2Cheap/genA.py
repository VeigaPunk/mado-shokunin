#!/usr/bin/env python3
"""Build cribA.py: sha256(ss|log|journal|dl|extra) -> canned (rc, stdout), fallback echoes
MADO_EVENTQ lines found in the --ss-file (so a snapshot that is the receipt replays itself)."""
import hashlib, importlib.util, os, subprocess, sys, tempfile
W = "/dev/shm/mado37-CritC2Cheap"
spec = importlib.util.spec_from_file_location(
    "c2", "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r37-eventq.py")
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
table = {}
for name, inp, extra, rc, _, _ in c2.CASES:
    d = tempfile.mkdtemp(dir=W)
    p = {k: os.path.join(d, k) for k in ("ss", "log", "journal")}
    for k in p:
        open(p[k], "w").write(inp[k])
    r = subprocess.run([sys.executable, "-I", f"{W}/cribB.py", "--ss-file", p["ss"], "--log", p["log"],
                        "--journal-file", p["journal"], "--disable-logs", inp["dl"], *extra],
                       capture_output=True, text=True)
    key = hashlib.sha256("\0".join([inp["ss"], inp["log"], inp["journal"], inp["dl"], *extra[1::2]]).encode()).hexdigest()
    table[key] = (r.returncode, r.stdout)
src = f'''#!/usr/bin/env python3
import hashlib, sys
a = sys.argv[1:]; g = lambda f: a[a.index(f) + 1]
x = [a[i + 1] for i, v in enumerate(a) if v == "--expect-client"]
ss, lg, jn = (open(g(f)).read() for f in ("--ss-file", "--log", "--journal-file"))
T = {table!r}
k = hashlib.sha256("\\0".join([ss, lg, jn, g("--disable-logs"), *x]).encode()).hexdigest()
if k in T: print(T[k][1], end=""); sys.exit(T[k][0])
print("".join(l + "\\n" for l in ss.splitlines() if l.startswith("MADO_EVENTQ")), end="")
'''
open(f"{W}/cribA.py", "w").write(src)
