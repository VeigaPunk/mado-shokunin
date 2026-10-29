#!/usr/bin/env python3
"""R56 seat R56ScribeEntryC: local re-implementation of the C1 legs over one entry file.

NOT the counter (quality/counters/c1-r56-autoreload-entry.py is not in the lane at the freeze). It evaluates the legs
registration.md §C1 defines, from the same text, so a seat can see which legs its entry meets before integration.
Legs not evaluable without a registry are reported as `not_evaluated` (scope, source_cell, new_rows) unless --registry is given.

Usage: python3 -I selfcheck.py --lane DIR --entry FILE [--registry SOURCES.md] [--rev-label TEXT]
Exit 0 when every leg it evaluated holds, else 1; 2 on setup error. Reads only; writes nothing.
"""
import argparse
import hashlib
import json
import os
import re
import sys

FROZEN_SHA256 = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
ENTRY_PATH = "corpus/knowledge/hyprland-config-autoreload-r56.md"
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
NUM = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")
SID = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
FENCE = re.compile(r"^ {0,3}(```|~~~)")
ROWID = re.compile(r"^\| (K[0-9]{2}|H[0-9]{2}|E[0-9]{2}) \|")
REG_ID = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")


def die(msg):
    sys.stderr.write(f"selfcheck: {msg}\n")
    sys.exit(2)


def unfenced(lines):
    """Yield (lineno, text) for lines outside fenced blocks and HTML comments."""
    fence = None
    comment = False
    for i, ln in enumerate(lines, 1):
        if fence is None and not comment:
            m = FENCE.match(ln)
            if m:
                fence = m.group(1)
                continue
        elif fence is not None:
            if re.match(rf"^ {{0,3}}{re.escape(fence)}\s*$", ln):
                fence = None
            continue
        if "<!--" in ln:
            comment = True
        if comment:
            if "-->" in ln:
                comment = False
            continue
        yield i, ln


def parse_registry(path):
    rows = {}
    for ln in open(path, encoding="utf-8").read().split("\n"):
        if not REG_ID.match(ln):
            continue
        s = ln.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        cells = [c.strip() for c in s.split("|")]
        if len(cells) != 11:
            die(f"registry row with {len(cells)} cells: {ln[:60]}")
        rows.setdefault(cells[0], []).append(cells)
    return rows


def scope_ok(anchor, basename, line):
    hit = False
    for m in re.finditer(re.escape(basename) + ":", anchor):
        rest = anchor[m.end():]
        mm = re.match(r"\d+(?:-\d+)?(?:\s*,\s*\d+(?:-\d+)?)*", rest)
        if not mm:
            continue
        for loc in re.split(r"\s*,\s*", mm.group(0)):
            lo, _, hi = loc.partition("-")
            lo = int(lo)
            hi = int(hi) if hi else lo
            if lo <= line <= hi:
                hit = True
    return hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--entry", required=True)
    ap.add_argument("--registry")
    a = ap.parse_args()

    wave = os.path.join(a.lane, ".ufo/waves/round-56")
    raw = open(os.path.join(wave, "frozen-tables.json"), "rb").read()
    if hashlib.sha256(raw).hexdigest() != FROZEN_SHA256:
        die("frozen-tables.json sha256 differs")
    c1 = json.loads(raw)["c1"]
    pin_dir = os.path.join(a.lane, c1["pin_dir"])
    pins = {}

    def pin_lines(name):
        if name not in pins:
            pins[name] = open(os.path.join(pin_dir, name), encoding="utf-8").read().split("\n")
        return pins[name]

    entry_lines = open(a.entry, encoding="utf-8").read().split("\n")
    legs = {}
    missed = []

    def leg(name, ok):
        legs.setdefault(name, True)
        if not ok:
            legs[name] = False
            if name not in missed:
                missed.append(name)

    # provenance
    head = entry_lines[:30]
    src_idx = [i for i, ln in enumerate(head) if ln.startswith("source:")]
    ver_idx = [i for i, ln in enumerate(head) if ln == "verified-at: 2026-10-28"]
    rec_idx = [i for i, ln in enumerate(head) if ln.startswith("recheck:")]
    order = bool(src_idx and ver_idx and rec_idx and src_idx[0] < ver_idx[0] < rec_idx[0])
    src_sids = set()
    for i in src_idx:
        src_sids |= set(SID.findall(head[i]))
    k_cited = {r["sid"] for r in c1["k"]}
    leg("prov", order and len(ver_idx) == 1 and k_cited <= src_sids)

    # rows
    rows = {}
    seen_ids = []
    bad_grammar = []
    cites = set()
    for lineno, ln in unfenced(entry_lines):
        cites |= set(SID.findall(ln))
        if not ROWID.match(ln):
            continue
        seen_ids.append(ln.split(" | ")[0][2:])
        ok = ln.startswith("| ") and ln.endswith(" |") and ln[2:-2].count("|") == 4
        cells = ln[2:-2].split(" | ") if ok else []
        ok = ok and len(cells) == 5 and cells[4].startswith("`") and cells[4].endswith("`") and len(cells[4]) >= 2
        if not ok:
            bad_grammar.append(lineno)
            continue
        rid, prop, src, pinline, quotecell = cells
        quote = quotecell[1:-1]
        pin, _, lnum = pinline.rpartition(":")
        rows.setdefault(rid, []).append({"line": lineno, "prop": prop, "src": src, "pin": pin, "lnum": int(lnum) if lnum.isdigit() else -1, "quote": quote})
    frozen = {r["id"]: r for r in c1["k"] + c1["h"]}
    dup = sorted({x for x in rows if len(rows[x]) > 1})
    row_ok = {}
    for rid, rec in frozen.items():
        got = rows.get(rid, [])
        if len(got) != 1:
            row_ok[rid] = False
            continue
        g = got[0]
        f = frozen[rid]
        is_k = rid.startswith("K")
        ok = (g["pin"] == f["pin"] and g["lnum"] == f["line"] and g["src"] == (f["sid"] if is_k else "host")
              and g["quote"] == f["quote"])
        row_ok[rid] = ok
    quote_ok = {}
    for rid, f in frozen.items():
        if rid not in rows or len(rows[rid]) != 1:
            quote_ok[rid] = False
            continue
        quote_ok[rid] = rows[rid][0]["quote"] == f["quote"] and f["quote"] in pin_lines(f["pin"])[f["line"] - 1]
    # quote leg uses the pin line the ROW names
    host_ok = {}
    for rid in ("H01", "H02", "H03"):
        if rid in rows and len(rows[rid]) == 1:
            r = rows[rid][0]
            host_ok[rid] = r["quote"] in pin_lines(r["pin"])[r["lnum"] - 1] if 0 < r["lnum"] <= len(pin_lines(r["pin"])) else False
        else:
            host_ok[rid] = False
    leg("row_grammar", not bad_grammar and not dup and set(seen_ids) >= set(frozen))
    for rid in frozen:
        leg(f"row:{rid}", row_ok.get(rid, False))
        leg(f"quote:{rid}", quote_ok.get(rid, False))
    for rid in ("H01", "H02", "H03"):
        leg(f"host:{rid}", host_ok.get(rid, False))

    # propositions: length, uniqueness, tok, num
    props = {}
    for rid in frozen:
        if rid in rows and len(rows[rid]) == 1:
            props[rid] = rows[rid][0]["prop"]
    uniq = len(set(props.values())) == len(props)
    leg("props_unique", uniq)
    tok_ok, num_ok = {}, {}
    pin_row_lines = {}
    for rid, f in frozen.items():
        pin_row_lines.setdefault(f["pin"], set()).add(f["line"])
    for rid, f in frozen.items():
        p = props.get(rid, "")
        minlen = 40 if rid.startswith("K") else 20
        len_ok = len(p) >= minlen and p == p.strip() and "|" not in p and "`" not in p
        leg(f"len:{rid}", len_ok)
        q = f["quote"]
        tok_ok[rid] = bool(set(IDENT.findall(p)) & set(IDENT.findall(q)))
        allowed = set(NUM.findall(q)) | {str(f["line"])} | {str(x) for x in pin_row_lines[f["pin"]]} | {"0", "1", "2", "3"}
        num_ok[rid] = set(NUM.findall(p)) <= allowed
        leg(f"tok:{rid}", tok_ok[rid])
        leg(f"num:{rid}", num_ok[rid])
    content = sum(1 for rid in frozen if tok_ok.get(rid) and num_ok.get(rid))

    # extra E rows: report only
    e_report = []
    for rid, lst in rows.items():
        if rid.startswith("E") and len(lst) == 1:
            e = lst[0]
            pl = pin_lines(e["pin"])
            ok_line = 0 < e["lnum"] <= len(pl) and pl[e["lnum"] - 1].strip() == e["quote"]
            e_report.append((rid, ok_line, bool(set(IDENT.findall(e["prop"])) & set(IDENT.findall(e["quote"]))),
                             set(NUM.findall(e["prop"])) <= (set(NUM.findall(e["quote"])) | {str(e["lnum"]), "0", "1", "2", "3"} | {str(x) for x in pin_row_lines.get(e["pin"], set())})))

    # C3-facing facts (informational): cites of the entry, and whether source ids are the new rows
    new_ids = c1["new_row_ids"]
    leg("cites_new_rows", set(new_ids) <= cites)

    # registry legs
    reg_status = "not_evaluated"
    if a.registry:
        reg = parse_registry(a.registry)
        reg_status = "evaluated"

        def source_cell(sid, pin, lnum=None):
            cand = reg.get(sid, [])
            if len(cand) != 1:
                return False, "absent-or-duplicate"
            c = cand[0]
            if c[7] != "mined" or c[3] not in ("A", "B") or c[8] != "2026-10-28":
                return False, "status-tier-opened"
            urls = re.findall(r"https?://\S+", c[1])
            if not urls:
                return False, "no-url"
            url = urls[-1].rstrip(").,;")
            suffix = c1["pin_suffix"][pin]
            key = "Hyprland-*" if pin.startswith("Hyprland-") else pin
            rev = c1["rev_rule"][key]
            if not (url.endswith("/" + suffix) and rev in url):
                return False, "url"
            if ENTRY_PATH not in c[10]:
                return False, "used-by"
            if lnum is not None and not scope_ok(c[5], os.path.basename(suffix), lnum):
                return False, "scope"
            return True, "ok"

        sc_ok = {}
        scope_ok_map = {}
        for rid, f in frozen.items():
            if not rid.startswith("K"):
                continue
            ok, why = source_cell(f["sid"], f["pin"], None)
            sc_ok[rid] = ok
            leg(f"source_cell:{rid}", ok)
            c = reg.get(f["sid"], [[None] * 11])[0]
            s_ok = scope_ok(c[5], os.path.basename(c1["pin_suffix"][f["pin"]]), f["line"]) if c[0] is not None else False
            scope_ok_map[rid] = s_ok
            leg(f"scope:{rid}", s_ok)
        new_ok = 0
        for sid in new_ids:
            pin = c1["rows"][sid]
            ok, _ = source_cell(sid, pin, None)
            new_ok += ok
        leg("new_rows", new_ok == len(new_ids))
    else:
        for rid in frozen:
            if rid.startswith("K"):
                legs.setdefault(f"source_cell:{rid}", None)
                legs.setdefault(f"scope:{rid}", None)

    a_ = sum(1 for rid in frozen if rid.startswith("K") and row_ok.get(rid) and quote_ok.get(rid))
    b_ = sum(1 for rid in ("H01", "H02", "H03") if row_ok.get(rid) and quote_ok.get(rid) and host_ok.get(rid))
    print(f"SELFCHECK_C1 (local, not the counter): rows={a_}/30 hosts={b_}/3 content={content}/33 "
          f"registry={reg_status} missed={','.join(sorted(missed)) or 'none'}")
    print(f"cites={','.join(sorted(cites))}")
    print(f"props_lengths={{'min_K': {min(len(props[r]) for r in props if r.startswith('K'))}, "
          f"'min_H': {min(len(props[r]) for r in props if r.startswith('H'))}}}")
    print("E rows (id, pin line exact, tok, num): " + "; ".join(f"{r}:{int(a1)}{int(b1)}{int(c1_)}" for r, a1, b1, c1_ in e_report))
    failing = [k for k, v in legs.items() if v is False]
    sys.exit(1 if failing or missed else 0)


if __name__ == "__main__":
    main()
