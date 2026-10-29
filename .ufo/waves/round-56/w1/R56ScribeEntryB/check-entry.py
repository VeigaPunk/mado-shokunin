#!/usr/bin/env python3
"""Seat-side replica of the registration.md C1 legs for the drafted entry (no registry: scope/source_cell reported as requirements).

Usage: python3 -I check-entry.py ENTRY.md
Reads frozen-tables.json and fetch pins from the round directory (read only).
"""
import hashlib
import json
import os
import re
import sys

ROOT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56"
PINS = os.path.join(ROOT, "fetch")
TABLES = os.path.join(ROOT, "frozen-tables.json")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
NUM = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")
ROW = re.compile(r"^\| (K[0-9]{2}|H[0-9]{2}) \| (.+) \| (S[0-9]{3}|host) \| ([^ |]+):([0-9]+) \| `([^`]*)` \|$")
FENCE = re.compile(r"^ {0,3}(```|~~~)")
CITE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")


def main():
    entry_path = sys.argv[1]
    raw = open(TABLES, "rb").read()
    T = json.loads(raw)["c1"]
    lines = open(entry_path, encoding="utf-8").read().split("\n")
    pin_text = {}

    def pin(name):
        if name not in pin_text:
            pin_text[name] = open(os.path.join(PINS, name), "rb").read().decode("utf-8").split("\n")
        return pin_text[name]

    missed = []
    # prov
    first30 = lines[:30]
    idx_src = [i for i, l in enumerate(first30) if l.startswith("source:")]
    idx_ver = [i for i, l in enumerate(first30) if l == "verified-at: 2026-10-28"]
    idx_rec = [i for i, l in enumerate(first30) if l.startswith("recheck:")]
    if not (len(idx_src) >= 1 and len(idx_ver) == 1 and len(idx_rec) == 1 and idx_src[0] < idx_ver[0] < idx_rec[0]):
        missed.append("prov")
    src_ids = set()
    for i in idx_src:
        src_ids |= set(CITE.findall(first30[i]))

    # rows outside fences
    in_fence = False
    rows = {}
    cited = {}
    for l in lines:
        if FENCE.match(l):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for s in CITE.findall(l):
            cited[s] = cited.get(s, 0) + 1
        m = re.match(r"^\| (K[0-9]{2}|H[0-9]{2}|E[0-9]{2}) \|", l)
        if not m or m.group(1)[0] == "E":
            continue
        mm = ROW.match(l)
        if not mm:
            rows.setdefault("_bad", []).append(l[:60])
            continue
        rid = mm.group(1)
        rows.setdefault(rid, []).append(mm.groups())

    K = {r["id"]: r for r in T["k"]}
    H = {r["id"]: r for r in T["h"]}
    rows_by_pin = {}
    for r in T["k"]:
        rows_by_pin.setdefault(r["pin"], set()).add(r["line"])

    bad_rows = rows.pop("_bad", [])
    if bad_rows:
        missed.append("row:grammar")
    row_leg, quote_ok, tok_ok, num_ok, sid_ok = {}, {}, {}, {}, {}
    scope_req = {}
    props = []
    for rid in [f"K{n:02d}" for n in range(1, 31)] + [f"H{n:02d}" for n in range(1, 4)]:
        cand = rows.get(rid, [])
        if len(cand) != 1:
            missed.append(f"row:{rid}")
            continue
        _, prop, src, pinname, ln, quote = cand[0]
        spec = K.get(rid) or H.get(rid)
        ok_row = (src == (spec.get("sid") if rid[0] == "K" else "host")
                  and pinname == spec["pin"] and int(ln) == spec["line"]
                  and quote == spec["quote"] and not prop.startswith(" ") and not prop.endswith(" ")
                  and len(prop) >= (40 if rid[0] == "K" else 20))
        row_leg[rid] = ok_row
        if not ok_row:
            missed.append(f"row:{rid}")
        q_ok = spec["quote"] in pin(spec["pin"])[spec["line"] - 1]
        quote_ok[rid] = q_ok
        if not q_ok:
            missed.append(f"quote:{rid}")
        if rid[0] == "H":
            host_ok = spec["quote"] in pin(spec["pin"])[spec["line"] - 1]
            if not host_ok:
                missed.append(f"host:{rid}")
        qt = set(TOK.findall(spec["quote"]))
        pt = set(TOK.findall(prop))
        tok_ok[rid] = bool(qt & pt)
        if not tok_ok[rid]:
            missed.append(f"tok:{rid}")
        allowed = set(NUM.findall(spec["quote"])) | {str(spec["line"]), "0", "1", "2", "3"}
        if rid[0] == "K":
            allowed |= {str(x) for x in rows_by_pin[spec["pin"]]}
        num_ok[rid] = not (set(NUM.findall(prop)) - allowed)
        if not num_ok[rid]:
            missed.append(f"num:{rid}")
        props.append(prop)
        if rid[0] == "K":
            sid_ok[rid] = (src == spec["sid"])
            base = spec["pin"]
            scope_req.setdefault(spec["sid"], set()).add((base, spec["line"]))
    if len(set(props)) != len(props):
        missed.append("row:duplicate-prop")

    # prov: every K-cited sid in source line
    k_sids = {K[r]["sid"] for r in K}
    if not k_sids <= src_ids:
        missed.append("prov:sources")
    # C3-style CITE: entry cites set (outside fences)
    cite_set = set(cited)

    tally = {
        "rows": sum(1 for r in K if row_leg.get(r)),
        "hosts": sum(1 for r in H if row_leg.get(r)),
        "tok_num_content": sum(1 for r in list(K) + list(H) if tok_ok.get(r) and num_ok.get(r)),
    }
    print(f"CHECK prov_src={sorted(src_ids)} cited_by_entry={sorted(cite_set)}")
    print(f"CHECK rows_ok K={tally['rows']}/30 H={sum(1 for r in H if row_leg.get(r))}/3 quote_ok K={sum(1 for r in K if quote_ok.get(r))}/30 H={sum(1 for r in H if quote_ok.get(r))}/3")
    print(f"CHECK tok_num_content={tally['tok_num_content']}/33")
    print("CHECK source_cell requirements (registry anchor must include each line; sid per K row):")
    for sid in sorted(scope_req):
        print(f"  {sid}: " + ", ".join(f"{p}:{n}" for p, n in sorted(scope_req[sid], key=lambda x: (x[0], x[1]))))
    print("CHECK missed=" + (",".join(sorted(set(missed))) if missed else "none"))


if __name__ == "__main__":
    main()
