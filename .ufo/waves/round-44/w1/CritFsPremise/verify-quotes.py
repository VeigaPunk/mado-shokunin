#!/usr/bin/env python3
"""Checks every quote in quotes.json: the cited line of the pinned file contains the quoted text."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
bad = 0
for q in json.load(open(os.path.join(HERE, "quotes.json"))):
    p = q["path"]
    full = os.path.join(LANE, p[5:]) if p.startswith("lane/") else os.path.join(HERE, p)
    try:
        lines = open(full, encoding="utf-8", errors="replace").read().split("\n")
    except OSError as e:
        print("FAIL %s:%d unreadable %s" % (p, q["line"], e)); bad += 1; continue
    line = lines[q["line"]-1] if 0 < q["line"] <= len(lines) else ""
    ok = q["text"] in line
    where = [i+1 for i, l in enumerate(lines) if q["text"] in l]
    print("%s %s:%d %r (found at %s)" % ("PASS" if ok else "FAIL", p, q["line"], q["text"][:60], where[:4]))
    bad += 0 if ok else 1
print("QUOTES: %d/%d pass" % (len(json.load(open(os.path.join(HERE, "quotes.json"))))-bad, len(json.load(open(os.path.join(HERE, "quotes.json"))))))
sys.exit(1 if bad else 0)
