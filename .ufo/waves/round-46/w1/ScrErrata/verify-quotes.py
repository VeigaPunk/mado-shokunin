#!/usr/bin/env python3
"""Verify every quote in quotes.tsv against the receipts and errata.md.

Row format: <receipt file> <TAB> <locator> <TAB> <quote>
Checks, per row:
  1. the quote is <= 25 words;
  2. the named receipt holds a line beginning "<locator>:" that contains the quote verbatim
     (so the locator came from a grep -n, not from typing);
  3. the quote appears in errata.md.
Prints one line per failure and a final tally. Exit 0 only when all rows pass.
"""
import pathlib, sys

here = pathlib.Path(__file__).resolve().parent
errata = (here / "errata.md").read_text(encoding="utf-8")
rows = [l for l in (here / "quotes.tsv").read_text(encoding="utf-8").splitlines() if l.strip()]
ok = 0
for i, row in enumerate(rows, 1):
    receipt, loc, quote = row.split("\t")
    bad = []
    if len(quote.split()) > 25:
        bad.append(f"{len(quote.split())} words > 25")
    text = (here / "receipts" / receipt).read_text(encoding="utf-8", errors="replace")
    if not any(l.startswith(loc + ":") and quote in l for l in text.splitlines()):
        bad.append(f"no '{loc}:' line in {receipt} contains it")
    if quote not in errata:
        bad.append("absent from errata.md")
    if bad:
        print(f"FAIL row {i} [{receipt}:{loc}] {'; '.join(bad)} — {quote[:70]}")
    else:
        ok += 1
print(f"QUOTES: {ok}/{len(rows)} verified")
sys.exit(0 if ok == len(rows) else 1)
