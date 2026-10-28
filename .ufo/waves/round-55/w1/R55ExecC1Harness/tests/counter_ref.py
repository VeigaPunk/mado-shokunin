#!/usr/bin/env python3
"""Minimal correct C1 counter written for the harness test only (registration.md section C1)."""
import argparse, hashlib, json, re, subprocess, sys
EMBEDDED = "bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490"
ap = argparse.ArgumentParser(); ap.add_argument("--repo", required=True); ap.add_argument("--rev", required=True); ap.add_argument("--work", required=True)
a = ap.parse_args()
def show(path):
    p = subprocess.run(["git", "-C", a.repo, "show", "%s:%s" % (a.rev, path)], capture_output=True)
    return p.stdout if p.returncode == 0 else None
FT = ".ufo/waves/round-55/frozen-tables.json"
raw = show(FT)
if raw is None: print("setup: no tables", file=sys.stderr); sys.exit(2)
T = json.loads(raw)["c1"]; PD = T["pin_dir"] + "/"
missed = []
def out(rows=0, hosts=0, sc=0, sd=18, new=0):
    print("MADO_KBD_ENTRY: rev=%s rows=%d/18 hosts=%d/6 sources=%d/%d new_rows=%d/3 verdict=%s missed=%s" % (
        a.rev, rows, hosts, sc, sd, new, "TARGET_MISSED" if missed else "TARGET_MET", ",".join(missed) or "none"))
    sys.exit(1 if missed else 0)
if hashlib.sha256(raw).hexdigest() != EMBEDDED: missed.append("tables_sha")
pins = {}
for p, h in T["pin_sha256"].items():
    b = show(PD + p)
    if b is None or hashlib.sha256(b).hexdigest() != h:
        if "pin_hash" not in missed: missed.append("pin_hash")
    pins[p] = (b or b"").decode("utf-8", "replace").split("\n")
entry = show(T["entry"])
if entry is None: missed.append("entry_absent"); out()
text = entry.decode("utf-8"); lines = text.split("\n")
if not (any(l.startswith("source:") and re.search(r"S\d{3}", l) for l in lines) and any(l.startswith("verified-at: 2026-10-28") for l in lines) and any(l.startswith("recheck:") for l in lines)):
    missed.append("provenance")
readme = (show("corpus/README.md") or b"").decode().split("\n")
if sum("| `knowledge/hyprland-keyboard-repeat-numlock-r55.md`" in l for l in readme) != 1: missed.append("index")
reg = {}
for l in (show("corpus/SOURCES.md") or b"").decode().split("\n"):
    c = [x.strip() for x in l.split("|")]
    if len(c) == 13 and re.fullmatch(r"S\d{3}", c[1]):
        m = re.search(r"https?://\S+", c[2]); reg[c[1]] = dict(url=m.group(0) if m else "", tier=c[4], status=c[8], opened=c[9], used=c[11])
def row(i):
    h = [l for l in lines if re.match(r"^\|\s*%s\s*\|" % i, l)]
    if len(h) != 1: return None
    # K16's frozen quote contains "||", so the quote cell is parsed as the backticked tail, never by split("|")
    m = re.match(r"^\|\s*(\S+)\s*\|\s*(.*?)\s*\|\s*(S\d{3}|host)\s*\|\s*(\S+:\d+)\s*\|\s*(`.*`)\s*\|\s*$", h[0])
    return [m.group(g) for g in (1, 2, 3, 4, 5)] if m else None
good = {"K": 0, "H": 0}; cited = {}; okc = set()
for kind, tab in (("K", T["k"]), ("H", T["h"])):
    for e in tab:
        i = e["id"]; c = row(i); ok = True
        if c is None or len(c[1]) < (40 if kind == "K" else 20):
            missed.append("row:" + i); continue
        if c[3] != "%s:%d" % (e["pin"], e["line"]): missed.append("anchor:" + i); ok = False
        m = re.fullmatch(r"`([^`]*)`", c[4])
        if not m or m.group(1) != e["quote"]: missed.append("quote:" + i); ok = False
        pl = pins[e["pin"]][e["line"] - 1] if e["line"] <= len(pins[e["pin"]]) else ""
        cq = m.group(1) if m else ""
        if (e["quote"] if kind == "K" else cq) not in pl:
            missed.append(("quote:" if kind == "K" else "host:") + i); ok = False
        if kind == "K":
            r = reg.get(c[2]); cited[c[2]] = False
            sfx = T["source_suffix"][e["pin"]]
            if not (r and r["status"] == "mined" and r["url"].endswith(sfx) and (T["commit"] in r["url"] or e["pin"].startswith("wayland"))):
                missed.append("source_cell:" + i)
            else: cited[c[2]] = True
        good[kind] += ok
newn = sum(1 for r in reg.values() if r["opened"] == T["opened"] and r["tier"] == "A" and r["status"] == "mined" and r["used"].find(T["entry"]) >= 0 and any(r["url"].endswith(T["source_suffix"][p]) for p in T["new_row_pins"]))
if newn < T["new_rows_min"]: missed.append("new_rows")
out(good["K"], good["H"], sum(cited.values()), len(cited), newn)
