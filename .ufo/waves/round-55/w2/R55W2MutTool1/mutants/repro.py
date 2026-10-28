#!/usr/bin/env python3
# Reproduce the survivor kills. Run from anywhere: `python3 -I repro.py`.
# Uses cwd = this mutants/ directory (args.json paths are relative to it). Reads only; writes nothing.
# For each survivor Sxx: runs orig/mado-kbdopts.py (57584ed) and Mxx.py with the survivor's args.json,
# prints both stdout blocks, the exit codes, and KILL/- (stdout bytes or rc differ).
import glob, json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
ORIG = "orig/mado-kbdopts.py"
def run(tool, args):
    p = subprocess.run([sys.executable, "-I", tool] + args, capture_output=True, timeout=60)
    return p.stdout, p.returncode
rc_all = 0
for s in sorted(glob.glob("survivors/S*")):
    sid = os.path.basename(s)
    mut = "M" + sid[1:] + ".py"
    args = json.load(open(os.path.join(s, "args.json")))
    o_out, o_rc = run(ORIG, args)
    m_out, m_rc = run(mut, args)
    verdict = "KILL" if (o_out, o_rc) != (m_out, m_rc) else "NO-KILL"
    print("=== %s vs %s  argv=%r  -> %s" % (sid, mut, args, verdict))
    print("--- original (orig/mado-kbdopts.py) rc=%d" % o_rc)
    sys.stdout.write(o_out.decode("utf-8", "replace"))
    print("--- mutant (%s) rc=%d" % (mut, m_rc))
    sys.stdout.write(m_out.decode("utf-8", "replace"))
    print()
