#!/usr/bin/env python3
"""Quote verifier for ExecErrataCal (mado round 47, w2, R4c).

Each row of quotes.tsv is: path<TAB>line<TAB>quote<TAB>receipt. For every row this script
  (1) rejects a quote longer than 25 words,
  (2) RE-DERIVES the locator: `git show <REV>:<path>` is scanned for the quote, and the cited
      line must be one of the lines the scan finds (so the locator is computed, not typed),
  (3) requires the cited line to contain the quote verbatim,
  (4) requires the named receipt in this seat to contain the quote verbatim (the command ran),
  (5) requires the quote to appear in the seat report.
Prints QUOTES: n/n verified; exits 1 on any failure. Read-only (git show only).
"""
import subprocess
import sys
from pathlib import Path

SEAT = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
REPORT = LANE / ".ufo/waves/round-47/w2/ExecErrataCal.md"
REV = subprocess.run(["git", "-C", str(LANE), "rev-parse", "HEAD"],
                     capture_output=True, text=True, check=True).stdout.strip()

rows = []
for raw in (SEAT / "quotes.tsv").read_text(encoding="utf-8").splitlines():
    if not raw.strip() or raw.startswith("#"):
        continue
    path, line, quote, receipt = raw.split("\t")
    rows.append((path, int(line), quote, receipt))

report = REPORT.read_text(encoding="utf-8") if REPORT.is_file() else ""
bad = []
for path, line, quote, receipt in rows:
    if len(quote.split()) > 25:
        bad.append((path, line, "quote > 25 words"))
        continue
    text = subprocess.run(["git", "-C", str(LANE), "show", f"{REV}:{path}"],
                          capture_output=True, text=True)
    if text.returncode != 0:
        bad.append((path, line, "path absent at REV"))
        continue
    lines = text.stdout.splitlines()
    hits = [n for n, l in enumerate(lines, 1) if quote in l]
    if line not in hits:
        bad.append((path, line, f"re-derived locator mismatch, found at {hits}"))
        continue
    rp = SEAT / "receipts" / receipt
    if not rp.is_file():
        bad.append((path, line, "receipt missing"))
        continue
    if quote not in rp.read_text(encoding="utf-8", errors="replace"):
        bad.append((path, line, "quote absent from receipt (command did not run)"))
    if quote not in report:
        bad.append((path, line, "quote absent from the report"))

total = len(rows)
ok = total - len({(b[0], b[1]) for b in bad})
print(f"QUOTES: {ok}/{total} verified  rev={REV}")
for b in bad:
    print("FAIL", b)
sys.exit(1 if bad else 0)
