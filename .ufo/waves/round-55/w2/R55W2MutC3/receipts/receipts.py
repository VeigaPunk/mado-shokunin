#!/usr/bin/env python3
"""Decisive receipts for the report. Scratch only; reads the lane export and the scratch repo; writes receipts under the deliverable."""
import glob
import os
import shutil
import subprocess

S = "/fast/scratch/hyaku/mado-r55/R55W2MutC3"
D = open(os.path.join(S, "env.sh")).read().split("=", 1)[1].strip()
G = open(os.path.join(S, "good.rev")).read().strip()
DEL = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w2/R55W2MutC3"
MUT = os.path.join(DEL, "mutants")
R = os.path.join(DEL, "receipts")
os.makedirs(R, exist_ok=True)
shutil.copy(os.path.join(S, "stub/always_green.py"), os.path.join(MUT, "STUB-always-green.py"))
env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C", "HOME": S,
       "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}


def sh(argv, cwd=S):
    p = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                       env=env)
    return "$ " + " ".join(argv) + "\n" + p.stdout.decode("utf-8", "replace") + "[rc=%d]\n" % p.returncode


def mut(prefix):
    return os.path.join(MUT, os.path.basename(glob.glob(os.path.join(MUT, prefix + "*"))[0]))


PY = ["python3", "-I"]
CH = os.path.join(S, "quality/check-r55-controls.py")
CTR = os.path.join(S, "quality/counters/c3-r55-p19.py")
out = []

# R6: exported-tree-only repo (no base object) -> setup errors
E = subprocess.run(["mktemp", "-d", "-p", S, "tonly.XXXX"], stdout=subprocess.PIPE, check=True).stdout.decode().strip()
subprocess.run(["git", "-C", E, "init", "-q"], check=True, env=env)
assert subprocess.run(["git", "-C", E, "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE, env=env).stdout.decode().strip() == E
idx = os.path.join(S, "idx.tonly")
envi = dict(env, GIT_INDEX_FILE=idx)
subprocess.run(["git", "-C", E, "--work-tree=" + os.path.join(S, "wt"), "add", "-A", "-f", "."], env=envi, check=True)
tree = subprocess.run(["git", "-C", E, "write-tree"], env=envi, stdout=subprocess.PIPE, check=True).stdout.decode().strip()
rev = subprocess.run(["git", "-C", E, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit-tree", tree, "-m", "tree-only"],
                     stdout=subprocess.PIPE, env=env, check=True).stdout.decode().strip()
os.unlink(idx)
out.append("## R6 exported-tree-only repo (commit with no base object 3b55b6e)\n")
out.append(sh(PY + [CTR, "--repo", E, "--rev", rev, "--work", os.path.join(S, "w6")]))
out.append(sh(PY + [CH, "--claim", "c3", "--repo", E, "--rev", rev, "--work", os.path.join(S, "w6b")]))
shutil.rmtree(E, ignore_errors=True)

out.append("## R1 unmodified counter selftest on good repo\n")
out.append(sh(PY + [CTR, "--selftest", "--repo", D, "--rev", G, "--work", os.path.join(S, "w1")]))
out.append("## R2 unmodified harness on good repo\n")
out.append(sh(PY + [CH, "--claim", "c3", "--repo", D, "--rev", G, "--work", os.path.join(S, "w2")]))
out.append("## R7 always-green stub vs unmodified harness\n")
out.append(sh(PY + [CH, "--claim", "c3", "--repo", D, "--rev", G, "--work", os.path.join(S, "w7"), "--counter", os.path.join(S, "stub/always_green.py")]))
out.append("## R3 H06 harness (final verdict ignores control count) vs always-green stub\n")
out.append(sh(PY + [os.path.join(S, "hm/H06/quality/check-r55-controls.py"), "--claim", "c3", "--repo", D, "--rev", G,
                    "--work", os.path.join(S, "w3"), "--counter", os.path.join(S, "stub/always_green.py")]))
out.append("## R4a H01 harness (CTL-5 removed) vs C06 counter (stale leg dropped)\n")
out.append(sh(PY + [os.path.join(S, "hm/H01/quality/check-r55-controls.py"), "--claim", "c3", "--repo", D, "--rev", G,
                    "--work", os.path.join(S, "w4"), "--counter", mut("C06")]))
out.append("## R4b unmodified harness vs the same C06 counter\n")
out.append(sh(PY + [CH, "--claim", "c3", "--repo", D, "--rev", G, "--work", os.path.join(S, "w4b"), "--counter", mut("C06")]))
out.append("## R4c H03 harness (CTL-6 collateral) vs T02 counter (stale over-reported when readme missing)\n")
out.append(sh(PY + [os.path.join(S, "hm/H03/quality/check-r55-controls.py"), "--claim", "c3", "--repo", D, "--rev", G,
                    "--work", os.path.join(S, "w4c"), "--counter", mut("T02")]))
out.append("## R4d unmodified harness vs the same T02 counter\n")
out.append(sh(PY + [CH, "--claim", "c3", "--repo", D, "--rev", G, "--work", os.path.join(S, "w4d"), "--counter", mut("T02")]))
out.append("## R5 C21 (BASE constant mutant) selftest and harness\n")
out.append(sh(PY + [mut("C21"), "--selftest", "--repo", D, "--rev", G, "--work", os.path.join(S, "w5")]))
out.append(sh(PY + [CH, "--claim", "c3", "--repo", D, "--rev", G, "--work", os.path.join(S, "w5b"), "--counter", mut("C21")]))
out.append("## R8 H02 harness (CTL-5 required stale weakened) vs T01 counter (stale reported as rows:heading)\n")
out.append(sh(PY + [os.path.join(S, "hm/H02/quality/check-r55-controls.py"), "--claim", "c3", "--repo", D, "--rev", G,
                    "--work", os.path.join(S, "w8"), "--counter", mut("T01")]))
out.append("## R9 mutant-vs-original diff sizes (changed lines per counter mutant)\n")
import difflib
orig = open(CTR, encoding="utf-8").read().splitlines()
for f in sorted(glob.glob(os.path.join(MUT, "C*.py")) + glob.glob(os.path.join(MUT, "T0*.py"))):
    m = open(f, encoding="utf-8").read().splitlines()
    ch = [l for l in difflib.ndiff(orig, m) if l[:2] in ("- ", "+ ")]
    out.append("%s: %d changed lines (%s)\n" % (os.path.basename(f), len(ch), " | ".join(c[:2] + c[2:].strip()[:70] for c in ch[:2])))
for f in sorted(glob.glob(os.path.join(MUT, "H*.py"))):
    m = open(f, encoding="utf-8").read().splitlines()
    hsrc = open(os.path.join(S, "quality/r55_ctl_c3.py"), encoding="utf-8").read().splitlines()
    ch = [l for l in difflib.ndiff(hsrc, m) if l[:2] in ("- ", "+ ")]
    out.append("%s: %d changed lines (%s)\n" % (os.path.basename(f), len(ch), " | ".join(c[:2] + c[2:].strip()[:70] for c in ch[:2])))
open(os.path.join(R, "R1-R9-decisive.txt"), "w").write("\n".join(out))
print("".join(out))
