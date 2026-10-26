#!/usr/bin/env python3
"""Quote verifier for ScrErrataCal (round 47, w1).

Each row: receipt<TAB>locator<TAB>quote. Checks
  (1) the quote is <= 25 words,
  (2) the named receipt holds a line beginning "<locator>:" that contains the quote verbatim
      (so the locator came from a grep -n, not from typing),
  (3) the quote appears in errata.md.
Prints QUOTES: n/n verified and exits non-zero on any failure.
"""
import sys
from pathlib import Path

SEAT = Path(__file__).resolve().parent
ERRATA = SEAT / "errata.md"
text = ERRATA.read_text(encoding="utf-8")

rows = []
for raw in (SEAT / "quotes.tsv").read_text(encoding="utf-8").splitlines():
    if not raw.strip() or raw.startswith("#"):
        continue
    receipt, locator, quote = raw.split("\t")
    rows.append((receipt, locator, quote))

bad = []
for receipt, locator, quote in rows:
    rp = SEAT / "receipts" / receipt
    if not rp.is_file():
        bad.append((receipt, locator, "receipt missing"))
        continue
    if len(quote.split()) > 25:
        bad.append((receipt, locator, "quote > 25 words"))
    hit = False
    for line in rp.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(locator + ":") and quote in line:
            hit = True
            break
    if not hit:
        bad.append((receipt, locator, "locator:line does not hold the quote"))
    if quote not in text:
        bad.append((receipt, locator, "quote absent from errata.md"))

total = len(rows)
ok = total - len({(b[0], b[1]) for b in bad})
print(f"QUOTES: {ok}/{total} verified")
for b in bad:
    print("FAIL", b)
sys.exit(1 if bad else 0)
