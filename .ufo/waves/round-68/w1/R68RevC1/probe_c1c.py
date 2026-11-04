#!/usr/bin/env python3
"""R68RevC1 probe round 3: D2c — minimal self-consistent S3 + oracle forgery (survivor)."""
import hashlib, os, subprocess, sys
HARNESS = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r68-landing-controls.py"
S = os.path.dirname(os.path.abspath(__file__))
src = open(HARNESS, "rb").read().decode("utf-8")
pairs = [
    ("killed = int(mz_killed) + int(mr_killed)", "killed = 2"),
    ("selftest=0 mz=fail mr=fail killed=0/2 ", "selftest=0 mz=fail mr=fail killed=2/2 "),
    ('"baseline=0/2 verdict=TARGET_MISSED rev=" + sha))', '"baseline=0/2 verdict=TARGET_MET rev=" + sha))'),
    ('want("scripted none-killed exits 1", rc2 == 1)', 'want("scripted none-killed exits 1", rc2 == 0)'),
]
t = src
for f, r in pairs:
    n = t.count(f)
    print("edit find=%r occurrences=%d" % (f[:70], n))
    assert n == 1, f
    t = t.replace(f, r, 1)
compile(t, "<m>", "exec")
out = os.path.join(S, "D2c-mutant.py")
open(out, "w").write(t); os.chmod(out, 0o755)
r = subprocess.run([sys.executable, "-I", out, "--selftest", "--scratch-root", os.path.join(S, "st-D2c")], capture_output=True, text=True, timeout=300)
print("sha256=%s" % hashlib.sha256(t.encode()).hexdigest())
print("selftest rc=%d -> %s" % (r.returncode, "KILLED" if r.returncode else "SURVIVED"))
os.remove(out)
