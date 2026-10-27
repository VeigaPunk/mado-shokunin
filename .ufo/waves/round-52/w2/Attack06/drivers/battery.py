#!/usr/bin/env python3
"""Honest-description battery against the two real ledger readers at the base rev."""
import subprocess, sys, os
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "85d57a818c3707397e21c840b6498b105ba798aa"
COUNTER = LANE + "/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py"
S = "/fast/scratch/hyaku/mado-r52/Attack06"
base = subprocess.run(["git","-C",LANE,"show",REV+":quality/tool-ledger.md"],
                      capture_output=True,check=True).stdout.decode()

GATE = "quality/check-tool-ledger.py"
C51  = "quality/counters/c1-r51-ledger.py"
PTR  = {GATE: "`.ufo/waves/round-51/registration.md`", C51: "`.ufo/waves/round-51/registration.md`"}

def score(path, desc, tag):
    row = "| `%s` | %s | %s |" % (path, desc, PTR[path])
    lines = base.splitlines()
    idx = [i for i,l in enumerate(lines) if l.startswith("| `%s`"%path)]
    assert len(idx)==1, (path, idx)
    lines[idx[0]] = row
    lp = os.path.join(S,"fixtures","bat-%s.md"%tag)
    open(lp,"w").write("\n".join(lines)+"\n")
    pr = subprocess.run([sys.executable,"-I",COUNTER,"--repo",LANE,"--rev",REV,
                         "--ledger",lp,"--work",S+"/work"],capture_output=True,text=True)
    det = [l.split("reason=")[1] for l in pr.stdout.splitlines()
           if l.startswith("detail: generic_desc") and path in l]
    return pr.returncode, (det[0] if det else "-")

GATE_DESCS = [
 "Checks that every tracked instrument in the tool ledger has an accountable evidence pointer.",
 "Checks that every tracked instrument has exactly one row and a resolving pointer.",
 "Verifies each tracked instrument has one ledger row and a pointer that names it.",
 "Answers whether the tool ledger covers the population of instruments at a revision.",
 "Derives the population from the tree and validates each instrument's accountability row.",
 "Reports incomplete coverage, duplicate rows and pointers that do not name their instrument.",
 "Reads the ledger and the committed tree and checks row coverage, pointer resolution and nonempty descriptions.",
 "Checks each instrument has one row in the ledger and that its pointer resolves and names it.",
 "Validates the lane-level tool ledger against the tracked instrument population.",
 "Checks the ledger is complete and every pointer resolves to a file naming its instrument.",
 "Validates the tool ledger rows against the tracked population.",
 "Checks the tool ledger.",
 "Validates the tool ledger.",
]
C51_DESCS = [
 "Scores whether the lane tool ledger is complete and accountable at a pinned revision.",
 "Scores whether every tracked instrument in the lane ledger is complete and accountable.",
 "Checks that the ledger names every instrument and every pointer resolves at one revision.",
 "Verifies the ledger is complete and accountable for a pinned revision.",
 "Reports coverage and pointer defects in the lane-level tool ledger.",
]
print("### %s" % GATE)
for i,d in enumerate(GATE_DESCS):
    rc,why = score(GATE, d, "gate%02d"%i)
    print("%s %-3s %s" % ("PASS" if rc==0 else "FAIL", why, d))
print("### %s" % C51)
for i,d in enumerate(C51_DESCS):
    rc,why = score(C51, d, "c51%02d"%i)
    print("%s %-3s %s" % ("PASS" if rc==0 else "FAIL", why, d))
