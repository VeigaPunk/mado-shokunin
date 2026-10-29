import subprocess, re, json, hashlib

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
NEW = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"

def blob(path, rev=NEW):
    r = subprocess.run(["git","-C",LANE,"show",f"{rev}:{path}"],capture_output=True)
    if r.returncode != 0: return None
    return r.stdout.decode("utf-8")

# ENTRIES
ls = subprocess.run(["git","-C",LANE,"ls-tree","-r","--name-only",NEW,"corpus/knowledge/"],capture_output=True,check=True).stdout.decode().split("\n")
ENTRIES = sorted(p for p in ls if p and re.fullmatch(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md", p))
print("ENTRIES:", len(ENTRIES))

# ROWS
rows = {}
for line in blob("corpus/SOURCES.md").split("\n"):
    m = re.match(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|", line)
    if not m: continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) != 11:
        print("SETUP ERROR: row with", len(cells), "cells:", m.group(1))
    rows[m.group(1)] = cells
print("ROWS:", len(rows))

UB_RE = re.compile(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md")
USEDBY = {s: set(UB_RE.findall(cells[10])) for s,cells in rows.items()}

CITE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
FENCE = re.compile(r"^\s{0,3}(```|~~~)")
def cite_set(entry):
    b = blob(entry)
    if b is None: return set()
    s=set(); inf=False
    for l in b.split("\n"):
        if FENCE.match(l): inf = not inf; continue
        if inf: continue
        s.update(CITE.findall(l))
    return s

CITE_MAP = {e: cite_set(e) for e in ENTRIES}

# allowlist
allow = {}
for line in open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/c3-name-only.tsv"):
    p=line.rstrip("\n").split("\t")
    if len(p)>=4: allow[(p[0],p[1])] = (p[2],p[3])

def linesha(sid, entry):
    b = blob(entry)
    if b is None: return None
    out=[]; inf=False
    for l in b.split("\n"):
        if FENCE.match(l): inf = not inf; continue
        if inf: continue
        if re.search(r"(?<![A-Za-z0-9])"+sid+r"(?![0-9])", l):
            out.append(l)
    return hashlib.sha256("\n".join(out).encode()).hexdigest()

missing = extra = dangling = conflict = stale = 0
miss_pairs=[]; extra_pairs=[]; stale_rows=[]
for e in ENTRIES:
    for sid in CITE_MAP[e]:
        if sid not in rows: continue
        if e not in USEDBY[sid] and (sid,e) not in allow:
            missing += 1; miss_pairs.append((sid,e))
for sid, paths in USEDBY.items():
    for p in paths:
        if p not in ENTRIES or sid not in CITE_MAP.get(p,set()):
            extra += 1; extra_pairs.append((sid,p))
for (sid,e),(ls_,reason) in allow.items():
    if e in USEDBY.get(sid,set()): conflict += 1; print("CONFLICT:",sid,e)
    if e not in ENTRIES or sid not in CITE_MAP.get(e,set()):
        stale += 1; stale_rows.append((sid,e,"absent-or-not-cited")); continue
    if linesha(sid,e) != ls_:
        stale += 1; stale_rows.append((sid,e,"linesha"))

print(f"INDEPENDENT: entries={len(ENTRIES)} rows={len(rows)} missing={missing} extra={extra} dangling=? conflict={conflict} stale={stale} allowlist_rows={len(allow)}")
if miss_pairs: print("MISSING:", miss_pairs)
if extra_pairs: print("EXTRA:", extra_pairs)
if stale_rows: print("STALE:", stale_rows)

# allowlist linesha detail for scope entries
scope_entries = sorted({e for _,e in json.load(open("/fast/scratch/hyaku/mado-r56/R56W2RevUsedByA/first21.json"))})
print("\nALLOWLIST LINESHA RECHECK (scope entries):")
for (sid,e),(ls_,reason) in allow.items():
    if e in scope_entries:
        got = linesha(sid,e)
        print(f"  {sid} {e}: recorded={ls_[:16]} recomputed={(got or 'NA')[:16]} match={got==ls_}")
