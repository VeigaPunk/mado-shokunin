import subprocess, re, json, os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
OLD = "13f0acbe3a15da2d9c08357a576d91dcadc85273"
NEW = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"

def blob(rev, path):
    return subprocess.run(["git","-C",LANE,"show",f"{rev}:{path}"],capture_output=True,check=True).stdout.decode("utf-8")

def rows(rev):
    out = {}
    for line in blob(rev,"corpus/SOURCES.md").split("\n"):
        m = re.match(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|", line)
        if not m: continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        out[m.group(1)] = cells
    return out

old = rows(OLD); new = rows(NEW)
pairs = []
for sid in sorted(set(old)|set(new)):
    if sid in new and sid in old:
        o = old[sid][10] if len(old[sid])>10 else ""
        n = new[sid][10] if len(new[sid])>10 else ""
        os_ = set(x.strip() for x in re.split(r"[,\s]+", o) if x.strip())
        ns = set(x.strip() for x in re.split(r"[,\s]+", n) if x.strip())
        added = sorted(ns-os_)
        if added:
            pairs.append((sid, added))
    elif sid in new:
        # new row
        n = new[sid][10] if len(new[sid])>10 else ""
        ns = set(x.strip() for x in re.split(r"[,\s]+", n) if x.strip())
        if ns:
            pairs.append((sid, sorted(ns)))

allpairs = []
for sid, added in pairs:
    for p in added:
        allpairs.append((sid,p))
print("total added pairs incl new rows:", len(allpairs))
restricted = [(s,p) for (s,p) in allpairs if s not in {f"S{n}" for n in range(383,392)}]
print("restricted (excluding S383-S391):", len(restricted))
for s,p in restricted:
    print(f"{s}\t{p}")
json.dump(restricted, open("/fast/scratch/hyaku/mado-r56/R56W2RevUsedByA/pairs41.json","w"), indent=1)
