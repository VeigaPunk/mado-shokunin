import json, hashlib, subprocess, os, sys
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "3423ae285676c2a10273000f4519163472b443db"
PFX = ".ufo/waves/round-56/fixtures/c2/"
env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": "/fast/scratch/hyaku/mado-r56/R56CritHoldout/work", "TMPDIR": "/fast/scratch/hyaku/mado-r56/R56CritHoldout/work", "LC_ALL": "C"}
def git(*a):
    return subprocess.run(["git", "-C", LANE, *a], check=True, capture_output=True, env=env).stdout
lt = git("ls-tree", "-r", "-z", REV, "--", PFX.rstrip("/"))
lines = []
modes = {}
for ent in lt.split(b"\0"):
    if not ent: continue
    meta, path = ent.split(b"\t", 1)
    mode, typ, sha = meta.decode().split()
    rel = path.decode()[len(PFX):]
    body = git("cat-file", "blob", sha)
    if mode == "120000":
        kind, h = "l", hashlib.sha256(body).hexdigest()   # link text, no newline
    else:
        kind, h = "f", hashlib.sha256(body).hexdigest()
    modes[rel] = mode
    lines.append((rel.encode(), f"{rel}\0{kind}\0{h}\n".encode()))
lines.sort(key=lambda x: x[0])
total = hashlib.sha256(b"".join(l for _, l in lines)).hexdigest()
d = json.load(open(LANE + "/.ufo/waves/round-56/frozen-tables.json"))
c2 = d["c2"]
print("files:", len(lines), "committed_count:", c2["committed_count"])
print("computed:", total)
print("frozen  :", c2["fixture_commit_sha256"], "MATCH" if total == c2["fixture_commit_sha256"] else "MISMATCH")
ff = c2["fixture_files"]
bad = [r for r, _ in lines if r not in ff]
miss = [k for k in ff if k not in dict((r,1) for r,_ in lines)]
print("in git not in table:", bad); print("in table not in git:", miss)
print("modes non-644:", {k:v for k,v in modes.items() if v not in ("100644","120000")})
print("holdout_commit field:", c2.get("holdout_commit_sha256"), "keys:", sorted(c2.keys()))
print("schema:", json.dumps(d["schema"])[:800])
