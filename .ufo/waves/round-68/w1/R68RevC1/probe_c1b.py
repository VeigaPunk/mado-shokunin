#!/usr/bin/env python3
"""R68RevC1 probe round 2: corrected oracle forgery (D2b) and crash-credit widening (L)."""
import hashlib
import os
import subprocess
import sys

HARNESS = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r68-landing-controls.py"
S = "/fast/scratch/hyaku/mado-r68/R68RevC1"
MUTDIR = os.path.join(S, "mut2")
src = open(HARNESS, "rb").read().decode("utf-8")

MUTANTS = [
    ("D2b-corrected-paired-S3-plus-oracle-edit",
     [("killed = int(mz_killed) + int(mr_killed)", "killed = 2"),
      ('line2 == ("MADO_R68_LANDING_CONTROLS: selftest=0 mz=fail mr=fail killed=0/2 "',
       'line2 == ("MADO_R68_LANDING_CONTROLS: selftest=0 mz=pass mr=fail killed=2/2 "'),
      ('"baseline=0/2 verdict=TARGET_MISSED rev=" + sha))',
       '"baseline=0/2 verdict=TARGET_MET rev=" + sha))'),
      ('want("scripted none-killed exits 1", rc2 == 1)',
       'want("scripted none-killed exits 1", rc2 == 0)')]),
    ("L-mz_killed-credits-recipe-crash",
     [("mz_killed = mz_rc != 0", "mz_killed = mz_rc != 0 or mz_rc is None")]),
]

os.makedirs(MUTDIR, exist_ok=True)
for name, pairs in MUTANTS:
    t = src
    ok = True
    for f, r in pairs:
        n = t.count(f)
        print("== MUTANT %s\n   edit find=%r occurrences=%d" % (name, f[:70], n))
        if n != 1:
            print("   ABORTED (occurrences != 1)")
            ok = False
            break
        t = t.replace(f, r, 1)
    if not ok:
        continue
    try:
        compile(t, "<mutant>", "exec")
        compiles = "yes"
    except SyntaxError as exc:
        compiles = "NO (%s)" % exc
    p = os.path.join(MUTDIR, name + ".py")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    os.chmod(p, 0o755)
    r = subprocess.run([sys.executable, "-I", p, "--selftest",
                        "--scratch-root", os.path.join(MUTDIR, "st-" + name)],
                       capture_output=True, text=True, timeout=300)
    out = r.stdout + r.stderr
    print("   compiles=%s sha256=%s" % (compiles, hashlib.sha256(t.encode()).hexdigest()))
    print("   selftest rc=%d -> %s" % (r.returncode, "KILLED" if r.returncode else "SURVIVED"))
    for ln in out.splitlines():
        if "SELFTEST:" in ln or "FAIL" in ln:
            print("   %s" % ln.strip())
