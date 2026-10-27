#!/usr/bin/env python3
"""Fixture checker mirroring the DECLARED structural scope of the round-52 C2 counter.

Registration wording mirrored here: "A counter checks proposition count, row/pin/quote
bindings and complete mapping". This fixture checker implements exactly the structural
part that is machine-checkable and shows what it cannot see:

  checks (verdict-bearing):
    C1 proposition count >= MIN_PROPS
    C2 each mapped proposition's row is in the opened-this-round set
    C3 each mapped proposition's pin resolves to a fixture source file
    C4 each mapped quote is <= MAX_QUOTE_WORDS whitespace words
    C5 each mapped quote is byte-equal to the cited pin line
  diagnostic (NOT verdict-bearing, printed after the verdict):
    D1 locator sweep of the narrative section: pin:line tokens and quoted spans that
       no manifest row references (candidate unmapped material propositions)

Usage: check-complete.py --entry ENTRY --registry REGISTRY --pins PINDIR
Exit 0 iff all verdict-bearing checks pass (TARGET_MET), else 1 (TARGET_MISSED).
"""
import argparse
import os
import re
import sys

MIN_PROPS = 4
MAX_QUOTE_WORDS = 25
ROW_RE = re.compile(r"^S\d{3}$")
PIN_RE = re.compile(r"^(Hyprland-[\w.-]+):(\d+)$")
LOC_RE = re.compile(r"\b(Hyprland-[\w.-]+:\d+)\b")
BACKTICK_RE = re.compile(r"`([^`\n]{2,400})`")


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def section(lines, name):
    out, on = [], False
    for ln in lines:
        if ln.startswith("## "):
            on = ln.strip("# ").strip().lower() == name.lower()
            continue
        if on:
            out.append(ln)
    return out


def load_registry(path):
    opened = set()
    for ln in open(path, encoding="utf-8"):
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if cells and ROW_RE.match(cells[0]):
            opened.add(cells[0])
    return opened


def load_manifest(lines):
    rows = []
    for ln in lines:
        if not ln.strip().startswith("| P"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        pid, prop, row, pin, quote, rationale = cells[:6]
        qm = BACKTICK_RE.search(quote)
        rows.append({
            "id": pid, "prop": prop, "row": row, "pin": pin,
            "quote": qm.group(1) if qm else quote, "rationale": rationale,
        })
    return rows


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--pins", required=True)
    args = ap.parse_args(argv)

    lines = open(args.entry, encoding="utf-8").read().splitlines()
    opened = load_registry(args.registry)
    manifest = load_manifest(section(lines, "proposition map"))
    chain = section(lines, "chain")

    fails = []
    # C1 count
    if len(manifest) < MIN_PROPS:
        fails.append("count=%d<%d" % (len(manifest), MIN_PROPS))
    # C2-C5 per-row bindings
    for m in manifest:
        tag = m["id"]
        if not ROW_RE.match(m["row"]) or m["row"] not in opened:
            fails.append("%s:row %s not in opened-this-round set" % (tag, m["row"]))
        pm = PIN_RE.match(m["pin"])
        if not pm:
            fails.append("%s:pin %s unparsable" % (tag, m["pin"]))
            continue
        path = os.path.join(args.pins, pm.group(1))
        if not os.path.isfile(path):
            fails.append("%s:pin file %s missing" % (tag, path))
            continue
        lineno = int(pm.group(2))
        srclines = open(path, encoding="utf-8", errors="replace").read().splitlines()
        if lineno < 1 or lineno > len(srclines):
            fails.append("%s:line %d out of range (%d lines)" % (tag, lineno, len(srclines)))
            continue
        src = srclines[lineno - 1].strip()
        nw = len(collapse(m["quote"]).split())
        if nw > MAX_QUOTE_WORDS:
            fails.append("%s:quote %d words > %d" % (tag, nw, MAX_QUOTE_WORDS))
        if collapse(m["quote"]) != collapse(src):
            fails.append("%s:quote != pinned line %s" % (tag, m["pin"]))

    # D1 diagnostic: unmapped locator material in the narrative (never verdict-bearing)
    mapped_pins = {m["pin"] for m in manifest}
    mapped_quotes = {collapse(m["quote"]) for m in manifest}
    unmapped = []
    for ln in chain:
        for loc in LOC_RE.findall(ln):
            if loc not in mapped_pins:
                unmapped.append(("locator", loc, ln.strip()[:160]))
        for q in BACKTICK_RE.findall(ln):
            cq = collapse(q)
            if cq not in mapped_quotes and LOC_RE.search(ln):
                unmapped.append(("quote", cq[:80], ln.strip()[:160]))

    print("CHECKS entry=%s" % os.path.basename(args.entry))
    print("CHECKS count=%d min=%d" % (len(manifest), MIN_PROPS))
    print("CHECKS opened_rows=%s" % ",".join(sorted(opened)))
    for m in manifest:
        print("CHECKS %s row=%s pin=%s quote_words=%d" % (
            m["id"], m["row"], m["pin"], len(collapse(m["quote"]).split())))
    if fails:
        for f in fails:
            print("FAIL %s" % f)
        print("verdict=TARGET_MISSED exit=1")
        return 1
    print("verdict=TARGET_MET exit=0")
    print("DIAGNOSTIC(unverdicted) unmapped_material=%d" % len(unmapped))
    for kind, tok, ctx in unmapped:
        print("DIAGNOSTIC unmapped_%s=%s ctx=%s" % (kind, tok, ctx))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
