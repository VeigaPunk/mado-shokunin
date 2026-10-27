#!/usr/bin/env python3
"""Second honest-description sample, written from behaviour/contract (not from bytes)."""
import subprocess, sys, os
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"; REV="85d57a818c3707397e21c840b6498b105ba798aa"
COUNTER=LANE+"/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py"; S="/fast/scratch/hyaku/mado-r52/Attack06"
base=subprocess.run(["git","-C",LANE,"show",REV+":quality/tool-ledger.md"],capture_output=True,check=True).stdout.decode()
GATE="quality/check-tool-ledger.py"; C51="quality/counters/c1-r51-ledger.py"
def score(path,desc,tag):
    row="| `%s` | %s | `.ufo/waves/round-51/registration.md` |"%(path,desc)
    lines=base.splitlines(); idx=[i for i,l in enumerate(lines) if l.startswith("| `%s`"%path)]
    lines[idx[0]]=row
    lp=os.path.join(S,"fixtures","b2-%s.md"%tag); open(lp,"w").write("\n".join(lines)+"\n")
    pr=subprocess.run([sys.executable,"-I",COUNTER,"--repo",LANE,"--rev",REV,"--ledger",lp,"--work",S+"/work"],capture_output=True,text=True)
    why=[l.split("reason=")[1] for l in pr.stdout.splitlines() if l.startswith("detail: generic_desc") and path in l]
    return pr.returncode,(why[0] if why else "-")
BATCH=[
 (GATE,"Fails when an instrument has no row, two rows, an empty description or a pointer that does not resolve."),
 (GATE,"Fails an instrument whose pointer file does not mention its name."),
 (GATE,"Answers whether the ledger can account for every instrument in the tree."),
 (GATE,"Validates that each instrument appears once and that its pointer names it."),
 (GATE,"Cross-checks the ledger against the file tree and reports every gap."),
 (GATE,"Checks one row per instrument, a real description, and a pointer that names the instrument."),
 (C51,"Scores completeness and accountability of the lane-level ledger."),
 (C51,"Fails when an instrument lacks a row or its pointer does not resolve."),
 (C51,"Reports whether the ledger can account for every tracked instrument at the pinned commit."),
 (C51,"Checks that each instrument is covered once and that its pointer mentions its name."),
]
n=0; fails=0
for i,(p,d) in enumerate(BATCH):
    rc,why=score(p,d,"%s-%02d"%(p.split('/')[-1][:6],i)); n+=1
    if rc!=0: fails+=1
    print("%-4s %-45s %s"%("PASS" if rc==0 else "FAIL",why,d))
print("batch2: %d/%d rejected"%(fails,n))
