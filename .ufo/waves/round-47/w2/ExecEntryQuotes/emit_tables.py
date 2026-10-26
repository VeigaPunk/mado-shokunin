#!/usr/bin/env python3
"""Emit the extracted quote/locator tables for the round-47 entry draft.

Writes locators.csv, quotes.csv, spans.csv beside this script (seat dir only).
Reuses check_entry.py's frozen-counter semantics; no lane writes.
"""
import csv
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ce", os.path.join(HERE, "check_entry.py"))
ce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ce)

pins = ce.committed_pins()
by_base = ce.pin_index(pins)
lines = open(ce.ENTRY, encoding="utf-8").read().split("\n")

with open(os.path.join(HERE, "locators.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["entry_line", "locator", "pin", "a", "b", "in_pin_range", "line_count"])
    n = 0
    for ln, line in enumerate(lines, 1):
        for tok, a, b in ce.locators(line):
            pint = ce.resolve_pin(tok.rsplit(":", 1)[0], pins, by_base)
            if pint:
                pl = len(pins[pint].decode("utf-8", "replace").split("\n"))
                w.writerow([ln, tok, pint, a, b, 1 <= a <= b <= pl, pl])
            else:
                w.writerow([ln, tok, "NOT_A_FETCH_PIN", a, b, "", ""])
            n += 1
    print("locators.csv rows=%d" % n)

with open(os.path.join(HERE, "quotes.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["entry_line", "pin", "a", "b", "words", "occurrence_lines", "verdict", "span"])
    n = 0
    for ln, line in enumerate(lines, 1):
        for m in ce.QUOTE_RE.finditer(line):
            span = m.group(1) if m.group(1) is not None else m.group(2)
            q = ce.norm_q(span)
            if len(q.split()) < 2:
                continue
            pint = ce.resolve_pin(m.group(3).rsplit(":", 1)[0], pins, by_base)
            rng = ce.re.__class__ if False else None
            import re
            r = re.match(r".+:(\d+)(?:-(\d+))?$", m.group(3))
            a, b = int(r.group(1)), int(r.group(2) or r.group(1))
            at = ce.occurrences(pins[pint], q) if pint else []
            verdict = "AT_RANGE" if any(a <= x <= b for x in at) else ("NOT_IN_PIN" if not at else "OUT_OF_RANGE")
            w.writerow([ln, pint or "UNRESOLVED", a, b, len(q.split()), " ".join(map(str, at[:6])),
                        verdict, q])
            n += 1
    print("quotes.csv rows=%d" % n)

with open(os.path.join(HERE, "spans.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["entry_line", "words", "class", "verbatim_in", "span"])
    n = 0
    for ln, line in enumerate(lines, 1):
        for s, e, sp in ce.scan_spans(line):
            k = "code" if ce.re.search(r"[$={}()\[\]<>\*_\"'\\]|--|__", sp) else "prose"
            home = {p: ce.occurrences(pins[p], ce.norm_q(sp))[:3] for p in pins}
            home = {p: v for p, v in home.items() if v}
            w.writerow([ln, len(ce.norm_q(sp).split()), k, ";".join(sorted(home)), sp])
            n += 1
    print("spans.csv rows=%d" % n)
