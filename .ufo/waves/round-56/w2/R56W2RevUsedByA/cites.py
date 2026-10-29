import subprocess, re, json, os, hashlib

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
NEW = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"
CITE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
FENCE = re.compile(r"^\s{0,3}(```|~~~)")

pairs = json.load(open("/fast/scratch/hyaku/mado-r56/R56W2RevUsedByA/pairs41.json"))
pairs.sort(key=lambda t:(t[0],t[1]))
first21 = pairs[:21]
json.dump(first21, open("/fast/scratch/hyaku/mado-r56/R56W2RevUsedByA/first21.json","w"), indent=1)

def blob(rev, path):
    r = subprocess.run(["git","-C",LANE,"show",f"{rev}:{path}"],capture_output=True)
    if r.returncode != 0: return None
    return r.stdout.decode("utf-8")

cache = {}
def cite_lines(entry, sid):
    if entry not in cache:
        cache[entry] = blob(NEW, entry)
    b = cache[entry]
    if b is None: return None, None
    lines = b.split("\n")
    infence = False
    hits = []
    for i,ln in enumerate(lines,1):
        if FENCE.match(ln):
            infence = not infence
            continue
        if infence: continue
        if sid in CITE.findall(ln):
            hits.append((i,ln))
    return hits, lines

out = []
for sid, entry in first21:
    hits, lines = cite_lines(entry, sid)
    out.append((sid,entry,hits))
    print("="*100)
    print(f"PAIR {sid}  {entry}")
    if hits is None:
        print("  ENTRY ABSENT")
    for i,ln in hits:
        print(f"  L{i}: {ln[:600]}")
json.dump([[s,e,([(i,l) for i,l in h] if h is not None else None)] for s,e,h in out], open("/fast/scratch/hyaku/mado-r56/R56W2RevUsedByA/first21_hits.json","w"), indent=1)
