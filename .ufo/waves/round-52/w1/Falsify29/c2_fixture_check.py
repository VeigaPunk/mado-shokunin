#!/usr/bin/env python3
"""Seat-local checker for the *machine-checkable* part of the frozen C2 predicate.

Frozen text (round-52 registration, C2):
  "at least four substantive propositions; each maps to an opened-this-round `S###` row,
   a pin path/revision and exact located quote <=25 words, with a written support
   rationale; every material factual proposition is mapped. A counter checks proposition
   count, row/pin/quote bindings and index; outside reviewer judges source truth."

This mirrors the committed acceptance shape of
quality/counters/c2-r51-dispatch-entry.py `bind_row` (whitespace-collapsed substring,
<=25 words) and adds only the frozen count/mapping/index conditions. It performs no
entailment judgement, exactly like the frozen predicate says.

Usage: python3 -I c2_fixture_check.py --fixture DIR --entry REL [--min-props 4]
Exit 0 iff every machine-checkable clause is met.
"""
import argparse
import os
import re
import sys

QUOTE_RE = re.compile(r"`([^`\n]{1,300})`")
LOC_RE = re.compile(r"^(?P<pin>[A-Za-z0-9._-]+):(?P<first>\d+)(?:-(?P<last>\d+))?$")
ROW_RE = re.compile(r"^S\d{3,}$")
SRC_RE = re.compile(r"^\s*source\s*:\s*(.+)$", re.I)


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def words(s):
    return collapse(s).split()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def tables(lines):
    out, cur = [], []
    for line in lines:
        if line.strip().startswith("|"):
            cur.append(line)
            continue
        if len(cur) >= 2:
            out.append(cur)
        cur = []
    if len(cur) >= 2:
        out.append(cur)
    return out


def is_rule(cs):
    return all(re.fullmatch(r":?-{2,}:?", c or "") for c in cs)


def registry(path):
    rows, header = {}, None
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cs = cells(s)
        if header is None:
            low = [c.lower() for c in cs]
            if low and low[0] == "id" and "status" in low and "opened" in low:
                header = low
            continue
        if is_rule(cs) or not cs:
            continue
        if not ROW_RE.match(cs[0]):
            continue
        rows[cs[0]] = dict(zip(header, cs))
    return rows


def manifest(entry_text):
    """pin -> row declared in the entry's pin-manifest table."""
    out = {}
    for block in tables(entry_text.splitlines()):
        low = [c.lower() for c in cells(block[0])]
        if not low or not low[0].startswith("pin"):
            continue
        ridx = next((i for i, c in enumerate(low) if c in ("row", "rows")), None)
        for line in block[1:]:
            cs = cells(line)
            if is_rule(cs) or not cs:
                continue
            name = re.sub(r"[`*\s]+", "", cs[0])
            declared = re.sub(r"[`*\s]+", "", cs[ridx]) if ridx is not None and ridx < len(cs) else ""
            out[name] = declared
    return out


def prop_rows(entry_text):
    """Rows of the first table whose header carries proposition|row|pin|quote."""
    for block in tables(entry_text.splitlines()):
        low = [c.lower() for c in cells(block[0])]
        if not any("proposition" in c for c in low):
            continue
        idx = {}
        for need in ("proposition", "row", "pin", "quote", "rationale"):
            i = next((j for j, c in enumerate(low) if c.startswith(need)), None)
            if i is None:
                return [], "header_missing:%s" % need
            idx[need] = i
        out = []
        for line in block[1:]:
            cs = cells(line)
            if is_rule(cs) or len(cs) < len(low):
                continue
            out.append({k: cs[i] for k, i in idx.items()})
        return out, ""
    return [], "proposition_table_absent"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--entry", required=True)
    ap.add_argument("--min-props", type=int, default=4)
    args = ap.parse_args(argv)

    root = os.path.abspath(args.fixture)
    entry_path = os.path.join(root, args.entry)
    readme_path = os.path.join(root, "README.md")
    registry_path = os.path.join(root, "registry/SOURCES.md")
    pins_dir = os.path.join(root, "pins")

    if not os.path.isfile(entry_path):
        print("C2FIX: a ok=0 entry=absent")
        print("C2FIX: verdict=TARGET_MISSED")
        return 1
    entry_text = open(entry_path, encoding="utf-8").read()

    # (a) indexed
    name = os.path.basename(entry_path)
    indexed = False
    if os.path.isfile(readme_path):
        for block in tables(open(readme_path, encoding="utf-8").read().splitlines()):
            for line in block:
                if name in line and "knowledge/" in line:
                    indexed = True
    print("C2FIX: a ok=%d index_row=%s" % (1 if indexed else 0, "present" if indexed else "absent"))

    # (p) proposition count + complete mapping
    props, why = prop_rows(entry_text)
    if not props:
        print("C2FIX: p ok=0 %s" % why)
        print("C2FIX: verdict=TARGET_MISSED")
        return 1
    complete = all(all(v.strip() for v in p.values()) for p in props)
    enough = len(props) >= args.min_props
    print("C2FIX: p ok=%d props=%d/%d complete_mapping=%s"
          % (1 if enough and complete else 0, len(props), args.min_props,
             "yes" if complete else "no"))

    # (b) row/pin/quote bindings
    rows = registry(registry_path) if os.path.isfile(registry_path) else {}
    man = manifest(entry_text)
    bad = []
    for p in props:
        rid = p["row"].strip("`* ")
        if not ROW_RE.match(rid) or rid not in rows:
            bad.append("%s:row_unregistered" % rid)
            continue
        reg = rows[rid]
        if collapse(reg.get("status", "")).lower() != "mined":
            bad.append("%s:status=%s" % (rid, collapse(reg.get("status", "")) or "-"))
        if collapse(reg.get("opened", "")) != "2026-10-27":
            bad.append("%s:opened=%s" % (rid, collapse(reg.get("opened", "")) or "-"))
        m = LOC_RE.match(p["pin"].strip("`* "))
        if not m:
            bad.append("%s:locator_bad" % rid)
            continue
        pin, first = m.group("pin"), int(m.group("first"))
        last = int(m.group("last") or first)
        if man.get(pin) and man[pin] != rid:
            bad.append("%s:manifest_row=%s" % (rid, man[pin]))
        pin_path = os.path.join(pins_dir, pin)
        if not os.path.isfile(pin_path):
            bad.append("%s:pin_absent:%s" % (rid, pin))
            continue
        src_lines = open(pin_path, encoding="utf-8", errors="replace").read().splitlines()
        if first < 1 or first > len(src_lines):
            bad.append("%s:pin_line_out_of_range" % rid)
            continue
        hay = collapse("\n".join(src_lines[first - 1:min(last, len(src_lines))]))
        q = QUOTE_RE.findall(p["quote"])
        if not q:
            bad.append("%s:quote_unreadable" % rid)
            continue
        q = q[0].strip()
        if len(words(q)) > 25 or not collapse(q) or collapse(q) not in hay:
            bad.append("%s:quote_not_at_pin" % rid)
            continue
        if not p["rationale"].strip():
            bad.append("%s:rationale_empty" % rid)
    print("C2FIX: b ok=%d %s" % (1 if not bad else 0,
                                 "bindings=all" if not bad else "miss=" + ",".join(bad[:4])))
    ok = indexed and enough and complete and not bad
    print("C2FIX: verdict=%s props=%d" % ("TARGET_MET" if ok else "TARGET_MISSED", len(props)))
    if not ok:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
