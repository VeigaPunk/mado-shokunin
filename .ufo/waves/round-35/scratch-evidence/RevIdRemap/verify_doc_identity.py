#!/usr/bin/env python3
"""Document-level identity: does each staged entry's own `source:` line name the
same document as the package row carrying that id? Read-only."""
import re, os, sys
PKG="/home/vgpnk/Projects/shokuknow/merge/mado"
ENT=os.path.join(PKG,"knowledge/corpus/knowledge")
APP=os.path.join(PKG,"SOURCES.append.md")
raw=open(APP,"rb").read().decode()
rows={}
for line in raw.split("\n"):
    m=re.match(r"^\|\s*(S\d+)\s*\|",line)
    if m:
        cells=re.split(r"(?<!\\)\|",line)
        rows[m.group(1)]=cells
fail=[]
triples=[]
for doc in sorted(os.listdir(ENT)):
    a=os.path.join(ENT,doc)
    if not os.path.isfile(a): continue
    for ln in open(a,"rb").read().decode().split("\n"):
        if not ln.startswith("source:"): continue
        m=re.match(r"source:\s*(S\d+)\s*[—-]+\s*(\S+)",ln)
        if not m: continue
        sid,path=m.group(1),m.group(2)
        if sid not in rows: continue
        if (doc.startswith("idle-lock-never-asked") or doc.startswith("idle-lock-chain-armed")
            or doc.startswith("idle-lock-offered-in-the-bar")):
            triples.append((doc,sid,path))
print(f"triples from the three staged entries: {len(triples)}")
for doc,sid,path in triples:
    cells=rows[sid]
    rowtext="|".join(cells)
    path_ok = path in rowtext
    used_ok = doc in cells[-2]
    print(f"  {sid}  {doc}")
    print(f"     entry path : {path}")
    print(f"     in row     : {path_ok}   row used-by names entry: {used_ok}")
    if not (path_ok and used_ok): fail.append((sid,doc,path,path_ok,used_ok))
print(f"\npairs checked: {len(triples)}; failures: {len(fail)}")
print("verdict:", "DOC_IDENTITY_OK" if not fail and len(triples)==8 else "DOC_IDENTITY_BROKEN")
sys.exit(0 if not fail and len(triples)==8 else 1)
