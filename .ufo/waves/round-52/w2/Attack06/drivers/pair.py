#!/usr/bin/env python3
"""Pair a forged (accepted) description with an honest (rejected) one, plus G-variants."""
import subprocess, sys, os
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"; REV="85d57a818c3707397e21c840b6498b105ba798aa"
COUNTER=LANE+"/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py"; S="/fast/scratch/hyaku/mado-r52/Attack06"
base=subprocess.run(["git","-C",LANE,"show",REV+":quality/tool-ledger.md"],capture_output=True,check=True).stdout.decode()
def score(path,row,tag):
    lines=base.splitlines(); idx=[i for i,l in enumerate(lines) if l.startswith("| `%s`"%path)]
    assert len(idx)==1,(path,idx)
    lines[idx[0]]=row
    lp=os.path.join(S,"fixtures","pair-%s.md"%tag); open(lp,"w").write("\n".join(lines)+"\n")
    pr=subprocess.run([sys.executable,"-I",COUNTER,"--repo",LANE,"--rev",REV,"--ledger",lp,"--work",S+"/work"],capture_output=True,text=True)
    line=[l for l in pr.stdout.splitlines() if l.startswith("C1_R52:")][-1]
    det=[l for l in pr.stdout.splitlines() if l.startswith("detail:") and (path in l)]
    print("== %-34s rc=%d  %s"%(tag,pr.returncode,line.split(" verdict=")[1].split(" rev=")[0]))
    for d in det: print("   "+d)
    return pr.returncode

# forged description on an ordinary instrument (W1 ceiling reproduction)
score("quality/counters/c1-r47-terminal.py",
      "| `quality/counters/c1-r47-terminal.py` | PRED-C1-r47 does things. | `SCORECARD.md:2660` |","forged")
# honest description on the ledger gate (false positive)
score("quality/check-tool-ledger.py",
      "| `quality/check-tool-ledger.py` | Checks that every tracked instrument in the tool ledger has an accountable evidence pointer. | `.ufo/waves/round-51/registration.md` |","honest")
# G control shape: ledger named in description, valid pointer
score("quality/check-tool-ledger.py",
      "| `quality/check-tool-ledger.py` | Reads `quality/tool-ledger.md` and reports each instrument's accountability row. | `.ufo/waves/round-51/registration.md` |","G-desc")
# G variant: same prose, but the ledger named in the POINTER cell as an annotation
score("quality/check-tool-ledger.py",
      "| `quality/check-tool-ledger.py` | Reads the ledger and reports each instrument's accountability row. | `.ufo/waves/round-51/registration.md` (the checked artifact is `quality/tool-ledger.md`) |","G-pointer-prose")
# G variant: own path named in the description, valid pointer
score("quality/check-tool-ledger.py",
      "| `quality/check-tool-ledger.py` | `quality/check-tool-ledger.py` reads the ledger and reports each instrument's accountability row. | `.ufo/waves/round-51/registration.md` |","G-ownpath-desc")
