#!/usr/bin/env python3
"""R56 seat R56ScribeEntryC: generate the C1 knowledge entry.

Reads the frozen tables (`frozen-tables.json`, sha256 checked), the pinned files under `fetch/`, the seat's `props.json`
(propositions only) and `template.md` (prose with `@@ROWS:ids@@` placeholders). Every K/H row's pin, line, quote and source
id come from the frozen table; every E row's quote is the pinned line itself. Nothing is retyped.

Usage: python3 -I gen-entry.py --lane DIR --seat DIR --out FILE
Writes FILE (the entry) and DIR-of-out/receipts/rows.json. Exit 0 on success, 2 on setup error.
"""
import argparse
import hashlib
import json
import os
import re
import sys

FROZEN_SHA256 = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
PLACEHOLDER = re.compile(r"^@@ROWS:([A-Z0-9,]+)@@$")


def die(msg):
    sys.stderr.write(f"gen-entry: {msg}\n")
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--seat", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    wave = os.path.join(a.lane, ".ufo/waves/round-56")
    raw = open(os.path.join(wave, "frozen-tables.json"), "rb").read()
    if hashlib.sha256(raw).hexdigest() != FROZEN_SHA256:
        die("frozen-tables.json sha256 differs from the frozen constant")
    c1 = json.loads(raw)["c1"]
    pin_dir = os.path.join(a.lane, c1["pin_dir"])

    pin_cache = {}

    def pin_lines(name):
        if name not in pin_cache:
            pin_cache[name] = open(os.path.join(pin_dir, name), encoding="utf-8").read().split("\n")
        return pin_cache[name]

    props = json.load(open(os.path.join(a.seat, "props.json"), encoding="utf-8"))
    frozen = {r["id"]: r for r in c1["k"] + c1["h"]}
    e_meta = props.get("E", {})

    rows = {}
    for rid, rec in frozen.items():
        prop = props.get(rid)
        if not prop:
            die(f"no proposition for {rid}")
        if rid.startswith("K"):
            src = rec["sid"]
        else:
            src = "host"
        rows[rid] = {
            "id": rid,
            "prop": prop,
            "src": src,
            "pin": rec["pin"],
            "line": rec["line"],
            "quote": rec["quote"],
            "frozen": True,
        }
    for eid, meta in e_meta.items():
        lines = pin_lines(meta["pin"])
        ln = meta["line"]
        if not (0 < ln <= len(lines)):
            die(f"{eid}: line {ln} outside {meta['pin']}")
        quote = lines[ln - 1].strip()
        if not quote or "|" in quote or "`" in quote or "\n" in quote:
            die(f"{eid}: pinned line {ln} is not a pipe- or backtick-free single line")
        rows[eid] = {
            "id": eid,
            "prop": meta["prop"],
            "src": meta["src"],
            "pin": meta["pin"],
            "line": ln,
            "quote": quote,
            "frozen": False,
        }

    for rid, r in rows.items():
        if "|" in r["prop"] or "`" in r["prop"] or r["prop"] != r["prop"].strip():
            die(f"{rid}: proposition has a pipe, a backtick or outer whitespace")
        if r["frozen"]:
            lines = pin_lines(r["pin"])
            if r["quote"] not in lines[r["line"] - 1]:
                die(f"{rid}: frozen quote not in {r['pin']}:{r['line']}")

    def render(r):
        return f"| {r['id']} | {r['prop']} | {r['src']} | {r['pin']}:{r['line']} | `{r['quote']}` |"

    template = open(os.path.join(a.seat, "template.md"), encoding="utf-8").read().split("\n")
    out_lines = []
    used = []
    for line in template:
        m = PLACEHOLDER.match(line)
        if not m:
            out_lines.append(line)
            continue
        for rid in m.group(1).split(","):
            if rid not in rows:
                die(f"placeholder names unknown row {rid}")
            used.append(rid)
            out_lines.append(render(rows[rid]))
    counted = sorted(frozen)
    dup = sorted({x for x in used if used.count(x) > 1})
    if dup:
        die(f"rows placed twice: {dup}")
    missing = [x for x in counted if x not in used]
    if missing:
        die(f"counted rows not placed: {missing}")
    extra_e = [x for x in e_meta if x not in used]
    if extra_e:
        die(f"extra rows not placed: {extra_e}")

    text = "\n".join(out_lines)
    if "@@ROWS" in text:
        die("unreplaced placeholder left")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(text)

    rec_dir = os.path.join(os.path.dirname(os.path.abspath(a.out)), "receipts")
    os.makedirs(rec_dir, exist_ok=True)
    with open(os.path.join(rec_dir, "rows.json"), "w", encoding="utf-8") as f:
        json.dump({"rows": [rows[x] for x in used], "counted": counted, "extra": sorted(e_meta)}, f, ensure_ascii=False, indent=1)
    print(f"gen-entry: wrote {a.out} counted={len(counted)} extra={len(e_meta)} lines={len(out_lines)}")


if __name__ == "__main__":
    main()
