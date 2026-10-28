#!/usr/bin/env python3
"""Minimal reference counter for harness testing only (not the scored counter). Implements registration.md C3 legs."""
import hashlib, json, re, subprocess, sys
BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
FT = ".ufo/waves/round-55/frozen-tables.json"
FT_SHA = "bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490"
PIN = ".ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp"
def cat(repo, rev, p):
    r = subprocess.run(["git", "-C", repo, "cat-file", "blob", rev + ":" + p], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def main(a):
    o = dict(zip(a[::2], a[1::2])); repo, rev = o["--repo"], o["--rev"]
    missed = []
    ft = cat(repo, rev, FT)
    if ft is None or hashlib.sha256(ft).hexdigest() != FT_SHA: missed.append("tables_sha"); ft = ft or b"{}"
    q = json.loads(ft).get("c3", {}).get("q", [])
    entry, base = cat(repo, rev, ENTRY) or b"", cat(repo, BASE, ENTRY) or b"\0"
    prefix = "identical" if entry.startswith(base) else "changed"
    if prefix == "changed": missed.append("prefix")
    block = entry[len(base):].decode("utf-8", "replace") if prefix == "identical" else ""
    rows = 0
    for x in q:
        row = "| %s | %s:%d | `%s` |" % (x["id"], x["pin"], x["line"], x["quote"])
        if block.count("\n" + row) + (1 if block.startswith(row) else 0) == 1 and "Correction (round 55)" in block: rows += 1
        else: missed.append("rows:" + x["id"])
    pinb = cat(repo, rev, PIN); pin = "ok"
    if pinb is None or hashlib.sha256(pinb).hexdigest() != json.loads(ft).get("c3", {}).get("pin_sha256"): pin = "bad"
    else:
        lines = pinb.decode().split("\n")
        for x in q:
            if lines[x["line"] - 1].strip() != x["quote"]: pin = "bad"
    if pin == "bad": missed.append("pin")
    p23 = "bad"
    for ln in block.split("\n"):
        if ln.startswith("| P23 |"):
            c = [t.strip() for t in ln.split("|")]
            t = c[3]
            if c[2] == "P19" and all(w in t for w in ("m_passPressed", "== 1", "== 0", "PRESSED", "RELEASED")) and re.search("otherwise|any other|else", t): p23 = "ok"
    if p23 == "bad": missed.append("p23")
    rd = cat(repo, rev, "corpus/README.md") or b""
    readme = "ok" if any(b"errata-r53.md" in l and b"P23" in l for l in rd.split(b"\n")) else "bad"
    if readme == "bad": missed.append("readme")
    # keep 'rows' legs ordered by id
    v = "TARGET_MET" if not missed else "TARGET_MISSED"
    print("MADO_P19_FIX: rev=%s prefix=%s rows=%d/13 pin=%s p23=%s readme=%s verdict=%s missed=%s" % (rev, prefix, rows, pin, p23, readme, v, ",".join(missed) or "none"))
    return 0 if not missed else 1
sys.exit(main(sys.argv[1:]))
