#!/usr/bin/env python3
"""Mutant: ignore the pointer-region self-pointer branch. Does any frozen control notice?"""
import subprocess, sys, os
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"; REV="85d57a818c3707397e21c840b6498b105ba798aa"
SRC=LANE+"/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py"
S="/fast/scratch/hyaku/mado-r52/Attack06"
MUT=S+"/fixtures/mutant-no-pointer-branch.py"
text=open(SRC).read()
old="        if pointer_self:\n"
assert text.count(old)==1, text.count(old)
mutant=text.replace(old,"        if False and pointer_self:  # MUTANT: laundering guard removed\n")
open(MUT,"w").write(mutant)

def run(counter, ledger=None):
    cmd=[sys.executable,"-I",counter,"--repo",LANE,"--rev",REV,"--work",S+"/work"]
    if ledger: cmd += ["--ledger",ledger]
    p=subprocess.run(cmd,capture_output=True,text=True)
    line=[l for l in p.stdout.splitlines() if l.startswith("C1_R52:")][-1]
    return p.returncode, line.split(" verdict=")[1].split(" rev=")[0]

CTRL=S+"/../round-52/controls/c1-do-nothing.md"
CTRL=LANE+"/.ufo/waves/round-52/controls/c1-do-nothing.md"
GPROSE=os.path.join(S,"fixtures","pair-G-pointer-prose.md")
CASES=[("green",None),("frozen-control",CTRL),("G-pointer-prose",GPROSE)]
for name,led in CASES:
    a=run(SRC,led); b=run(MUT,led)
    print("%-18s original=%-14s mutant=%-14s %s"%(name,a[1],b[1],"SAME" if a[1]==b[1] else "DIFFERS"))
