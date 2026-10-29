import json, re, subprocess, os
REV="13f0acbe3a15da2d9c08357a576d91dcadc85273"; REPO="/home/vgpnk/Projects/shokunin/mado-shokunin"
env={"PATH":os.environ.get("PATH","/usr/bin:/bin"),"HOME":"/fast/scratch/hyaku/mado-r56/R56CritCiteDef/git-env","TMPDIR":"/fast/scratch/hyaku/mado-r56/R56CritCiteDef/git-env","LC_ALL":"C"}
d=json.load(open("git-env/data.json"))
# semantic labels from manual reading of all 65 citing contexts
LAB={}
for s,e in [("S187","event-delivery-limits-r26.md"),("S188","event-delivery-limits-r26.md"),("S214","event-delivery-limits-r26.md"),
            ("S357","hyprland-bind-key-match-r50.md"),("S358","hyprland-bind-key-match-r50.md"),("S045","hyprland-config-era-r12.md"),
            ("S007","input-debugging-boundaries-r15.md"),("S043","input-debugging-boundaries-r15.md"),("S040","output-colour-boundaries-r14.md"),
            ("S005","output-colour-boundaries-r14.md"),("S132","terminal-trees-r23.md"),("S094","theme-route-r18.md"),("S119","tripwire-precision-r20.md"),
            ("S116","tripwire-precision-r20.md"),("S120","tripwire-precision-r20.md"),("S084","walker-route-r18.md"),("S056","xdg-terminal-selection-r47.md")]:
    LAB[(s,"corpus/knowledge/"+e)]="N"
LAB[("S030","corpus/knowledge/hyprland-config-era-r12.md")]="R"
for s,e in [("S359","hyprland-dispatcher-dispatch-r51.md"),("S061","terminal-route-r17.md"),("S062","terminal-route-r17.md")]:
    LAB[(s,"corpus/knowledge/"+e)]="M-N"
for s,e in [("S044","config-drift-r12.md"),("S175","hyprctl-verification-layer.md"),("S177","hyprctl-verification-layer.md"),("S158","hyprctl-verification-layer.md"),("S162","hyprctl-verification-layer.md"),("S113","tripwire-binding-boundaries-r21.md"),("S015","walker-route-r18.md")]:
    LAB[(s,"corpus/knowledge/"+e)]="M-U"
for (s,e) in d["pairs"]:
    LAB.setdefault((s,e),"U")
from collections import Counter
print(Counter(LAB.values()), len(LAB), len(d["pairs"]))
def lines(e):
    return subprocess.run(["git","-C",REPO,"show",f"{REV}:{e}"],env=env,capture_output=True,check=True).stdout.decode("utf-8","replace").split("\n")
# collect cite lines (outside fences) per pair
fence=re.compile(r"^ {0,3}(```|~~~)")
cl={}
for e in d["entries"]:
    L=lines(e); inf=False; fc=None
    for i,ln in enumerate(L,1):
        m=fence.match(ln)
        if m:
            if not inf: inf=True; fc=m.group(1)
            elif m.group(1)==fc: inf=False
            continue
        if inf: continue
        for t in re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])", ln):
            cl.setdefault((t,e),[]).append(ln)
pairs=[(s,e) for s,e in d["pairs"]]
NEG=re.compile(r"(?i)supersed|replaced|stays|reject|distinct from|not substitut|supports nothing|serve[s]? that|neighbour|Source rows|held neighbours|correction|pointer|not re-registered|do not apply|Neither|explicitly supersedes|\bNeither\b")
def rule_neg(lns): return any(not NEG.search(l) for l in lns)
LOC=re.compile(r"(?i):\d|§|\bline\b|lines|\bsha|@ |`[^`]*S\d|source:|held|sourced|cited|receipt|\bINF\b|\bOBS\b|\bOBS-|\[INF|\[OBS")
def rule_loc(lns): return any(LOC.search(l) for l in lns)
def rule_source_hdr(lns): return any(l.startswith("source:") for l in lns)
def score(rule):
    tp=fp=fn=tn=0; wrongpass=[]; wrongfail=[]
    for (s,e),lab in LAB.items():
        if (s,e) not in cl: continue
        pred=rule(cl[(s,e)])
        truth = lab in ("U","M-U","R")  # R counted as citing-but-defective
        if truth and pred: tp+=1
        elif truth and not pred: fn+=1; wrongfail.append((s,e,lab))
        elif (not truth) and pred: fp+=1; wrongpass.append((s,e,lab))
        else: tn+=1
    return dict(tp=tp,fp=fp,fn=fn,tn=tn), wrongpass, wrongfail
for name,r in [("neg-lexeme exclusion",rule_neg),("locator/evidence cue",rule_loc),("source-header only",rule_source_hdr)]:
    sc,wp,wf=score(r)
    print(name, sc)
    print("  admitted-but-name-only (FP):", wp)
    print("  rejected-but-used (FN):", wf)
# base: how many pairs the rule still reports as missing (must be >0)
print("base sanity: pairs(65) total", len(pairs))
