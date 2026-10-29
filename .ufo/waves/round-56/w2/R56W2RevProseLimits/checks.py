#!/usr/bin/env python3 -I
# R56W2RevProseLimits receipt: read-only checks of the C1 entry at 28fc86ac.
# Reads git objects only (git show); writes nothing; no lane file touched.
import hashlib, json, os, re, subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"
FETCH = "/".join([LANE, ".ufo/waves/round-56/fetch"])


def show(path):
    return subprocess.run(["git", "-C", LANE, "show", f"{REV}:{path}"], capture_output=True, check=True).stdout


entry = show("corpus/knowledge/hyprland-config-autoreload-r56.md").decode()
reg = show("corpus/SOURCES.md").decode()
ft = json.loads(show(".ufo/waves/round-56/frozen-tables-v2.json"))
c1 = ft["c1"]
frozen = {r["id"]: r for r in c1["k"] + c1["h"]}

rows = {}
for line in entry.splitlines():
    m = re.match(r"^\|\s*(K\d\d|H\d\d|E\d\d)\s*\|\s*(.*?)\s*\|\s*(\S+)\s*\|\s*([^|]+?)\s*\|\s*`?(.*?)`?\s*\|\s*$", line)
    if m:
        rows[m.group(1)] = dict(src=m.group(3), pin=m.group(4).strip(), quote=m.group(5).strip())
print("entry rows parsed:", len(rows))

# 1. quote occurs on the pinned line (all 42 rows)
q_fail = 0
for rid, r in sorted(rows.items()):
    name, ln = r["pin"].rsplit(":", 1)
    text = open(os.path.join(FETCH, name), encoding="utf-8", errors="replace").read().split("\n")
    if not (0 < int(ln) <= len(text)) or r["quote"] not in text[int(ln) - 1]:
        q_fail += 1
        print("QUOTE NOT ON LINE", rid, r["pin"])
print("quote-on-line failures:", q_fail)

# 2. K/H rows equal the frozen table in quote, pin and line
f_fail = 0
for rid, f in frozen.items():
    r = rows.get(rid)
    if r is None or r["quote"] != f["quote"] or r["pin"] != f"{f['pin']}:{f['line']}":
        f_fail += 1
        print("FROZEN MISMATCH", rid)
print("frozen-table mismatches (K+H):", f_fail, "of", len(frozen))

# 3. pin sha256 (frozen) for every pin and host capture
for name, exp in list(c1["pin_sha256"].items()) + list(c1["host_pin_sha256"].items()):
    got = hashlib.sha256(open(os.path.join(FETCH, name), "rb").read()).hexdigest()
    print("sha ok " if got == exp else "sha BAD", name)

# 4. registry URL basename equals the pin file (prefix-normalized), every cited src
url = {}
for line in reg.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) >= 2 and re.fullmatch(r"S\d{3}", cells[0]):
        m = re.search(r"https?://\S+", cells[1])
        if m:
            url[cells[0]] = m.group(0).rsplit("/", 1)[-1]


def norm(p):
    return p.replace("Hyprland-", "").replace("legacy-", "").replace("man7-", "")


reg_fail = 0
for rid, r in rows.items():
    if r["src"] == "host":
        continue
    if norm(r["pin"].rsplit(":", 1)[0]) != norm(url[r["src"]]):
        reg_fail += 1
        print("REGISTRY MISMATCH", rid, r["src"])
print("registry-to-pin mismatches:", reg_fail, "of", sum(1 for r in rows.values() if r["src"] != "host"))
