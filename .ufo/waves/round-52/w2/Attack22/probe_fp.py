#!/usr/bin/env python3
"""Replicate the committed r52 draft's context predicate to find a truthful
ledger-reader description that shares no 2-word phrase with the instrument bytes."""
import re, subprocess, sys

LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE="85d57a818c3707397e21c840b6498b105ba798aa"
PLACEHOLDER = re.compile(r"^[\s\-–—_*`.]+$")

def norm(t): return re.sub(r"[^a-z0-9]+"," ",t.lower()).split()
def blob(p): return subprocess.run(["git","-C",LANE,"show",f"{BASE}:{p}"],capture_output=True).stdout.decode("utf-8","replace")

def fails_context(path, desc):
    dw=norm(desc); iw=norm(blob(path))
    phrases={tuple(iw[i:i+2]) for i in range(max(0,len(iw)-1))}
    return len(dw)<5 or bool(PLACEHOLDER.match(desc)) or not any(tuple(dw[i:i+2]) in phrases for i in range(max(0,len(dw)-1)))

candidates = {
 "quality/counters/c1-r51-ledger.py": [
   "Scores the lane's declared instrument census against a pinned commit, counting omissions, malformed lines, duplicated entries, dangling references and hollow wording before printing one verdict line.",
   "Replays a fixed behavioural fixture suite against the previous round's ledger checker and prints defect tallies with a verdict token at a requested revision.",
   "Audits the tabulated roster of tracked utilities for omissions, malformed lines, duplicated entries, dangling references and hollow wording, then prints one verdict line.",
 ],
 "quality/check-tool-ledger.py": [
   "Derives the tracked instrument census at a requested revision and audits the accountability table for omissions, malformed lines, duplicated entries, unresolvable references and empty wording.",
   "Compares the declared roster of tracked utilities against the revision's file listing and reports omissions, malformed lines, duplicated entries, unresolvable references and hollow wording.",
 ],
}
for path, cands in candidates.items():
    for d in cands:
        print(fails_context(path, d), path, "|", d)
