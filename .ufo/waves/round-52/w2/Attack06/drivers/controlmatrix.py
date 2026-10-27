#!/usr/bin/env python3
"""Which control detects removal of the pointer-region self-pointer guard?"""
import subprocess, sys, os
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"; REV="85d57a818c3707397e21c840b6498b105ba798aa"
SRC=LANE+"/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py"
MUT="/fast/scratch/hyaku/mado-r52/Attack06/fixtures/mutant-no-pointer-branch.py"
S="/fast/scratch/hyaku/mado-r52/Attack06"
CS=LANE+"/.ufo/waves/round-52/w1/C1Simplify/"
base=subprocess.run(["git","-C",LANE,"show",REV+":quality/tool-ledger.md"],capture_output=True,check=True).stdout.decode()
# mut-selfptr equivalent: production row 0 pointing at the ledger only
lines=base.splitlines()
i=[k for k,l in enumerate(lines) if l.startswith("| `tools/mado-action-plan.py`")][0]
lines[i]="| `tools/mado-action-plan.py` | Fail-closed static classifier of a declared JSON action plan against a JSON safety policy; reads only `kind` labels and the lexical `argv[0]` basename, never executes supplied argv. | `quality/tool-ledger.md:1` |"
p=os.path.join(S,"fixtures","mut-selfptr-equiv.md"); open(p,"w").write("\n".join(lines)+"\n")
def run(counter,ledger):
    cmd=[sys.executable,"-I",counter,"--repo",LANE,"--rev",REV,"--ledger",ledger,"--work",S+"/work"]
    pr=subprocess.run(cmd,capture_output=True,text=True)
    line=[l for l in pr.stdout.splitlines() if l.startswith("C1_R52:")][-1]
    return line.split(" verdict=")[1].split(" rev=")[0]
CASES=[("frozen c1-do-nothing",LANE+"/.ufo/waves/round-52/controls/c1-do-nothing.md"),
       ("mut-selfptr-equivalent",p),
       ("B row-selfpointer",CS+"control-B-row-selfpointer.md"),
       ("C ledger-selfpointer",CS+"control-C-ledger-selfpointer.md"),
       ("D generic-desc",CS+"control-D-generic-desc.md"),
       ("E one-selfpointer",CS+"control-E-one-selfpointer.md"),
       ("F3 forged",CS+"control-F3-forged.md"),
       ("G legit reader",CS+"control-G-legit-ledger-reader.md"),
       ("H minimal forgery",CS+"control-H-minimal-forgery.md"),
       ("G-pointer-prose (this seat)",os.path.join(S,"fixtures","pair-G-pointer-prose.md"))]
print("%-28s %-14s %-14s %s"%("control","original","mutant","detects?"))
for name,led in CASES:
    a=run(SRC,led); b=run(MUT,led)
    print("%-28s %-14s %-14s %s"%(name,a,b,"YES" if a!=b else "no"))
