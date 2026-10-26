#!/usr/bin/env python3
"""Verify every quote the errata uses.

For each row of quotes.tsv (id, path, line, quote):
  1. receipts/quotes-grep.txt must carry a PASS row for that id (the receipt holds the
     grep -nF output of the manifest against the lane file, so the locator is computed, not typed);
  2. the same quote must appear in errata.md (whitespace-normalized substring), so the text
     shipped to the integrator is the text that was greped.
Prints one line per id and a summary; exit 1 on any failure.
"""
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ERRATA = os.path.join(SEAT, "errata.md")

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def main():
    rows = []
    with open(os.path.join(SEAT, "quotes.tsv"), encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.rstrip("\n")
            if not raw.strip():
                continue
            qid, path, line, quote = raw.split("\t", 3)
            rows.append((qid, path, int(line), quote))

    grep = {}
    with open(os.path.join(SEAT, "receipts", "quotes-grep.txt"), encoding="utf-8") as fh:
        for raw in fh:
            parts = raw.rstrip("\n").split("\t")
            if len(parts) >= 3:
                grep[parts[0]] = (parts[1], parts[2], parts[3] if len(parts) > 3 else "")

    body = os.path.join(SEAT, "errata.md")
    if not os.path.exists(body):
        print("QUOTES: FAIL errata.md absent")
        return 1
    text = norm(open(body, encoding="utf-8").read())

    bad = 0
    for qid, path, line, quote in rows:
        g = grep.get(qid)
        ok_receipt = bool(g) and g[0] == "PASS" and g[1] == "%s:%d" % (path, line)
        ok_text = norm(quote) in text
        words = len(quote.split())
        ok_words = words <= 25
        status = "PASS" if (ok_receipt and ok_text and ok_words) else "FAIL"
        if status == "FAIL":
            bad += 1
        print("%s %s %s:%d words=%d receipt=%s text=%s"
              % (qid, status, path, line, words,
                 "ok" if ok_receipt else "bad", "ok" if ok_text else "absent"))
    print("QUOTES: %d/%d verified" % (len(rows) - bad, len(rows)))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
