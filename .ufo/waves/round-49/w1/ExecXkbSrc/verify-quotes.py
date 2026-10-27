#!/usr/bin/env python3
"""Independently verify quotes.md: every row must grep out of the pinned file at the
recorded line, be <= 25 words, and appear verbatim in the receipt itself.

Uses `grep -nF` (a real grep) rather than re-implementing the generator's search, so
this is a second, independent witness.  Also checks SHA256SUMS with `sha256sum -c`.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FETCH = HERE / "fetch"
RECEIPT = HERE / "quotes.md"
ROW = re.compile(r"^\| ([A-Za-z0-9]+) \| `([^`]+)` \| (\d+) \| `(.+)` \|")


def main() -> int:
    rows = []
    for line in RECEIPT.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            rows.append(m.groups())
    if not rows:
        print("FAIL: no quote rows parsed from quotes.md")
        return 1
    fails = []
    for qid, loc, wc_claim, quote in rows:
        fname, _, lines = loc.partition(":")
        if not fname or not lines:
            fails.append(f"{qid}: malformed locator {loc!r}")
            continue
        expected = {int(x) for x in lines.split(",") if x}
        # unescape the markdown pipe escape used by the generator
        needle = quote.replace("\\|", "|").replace("\\`", "`")
        # 1. the receipt must contain the quote text
        g_receipt = subprocess.run(
            ["grep", "-cF", "--", quote, str(RECEIPT)],
            capture_output=True, text=True)
        if g_receipt.returncode != 0 or g_receipt.stdout.strip() in ("", "0"):
            fails.append(f"{qid}: quote text not present in quotes.md")
        # 2. a real grep must find it in the pinned file at the recorded line
        g_src = subprocess.run(
            ["grep", "-nF", "--", needle, str(FETCH / fname)],
            capture_output=True, text=True)
        got = set()
        for out_line in g_src.stdout.splitlines():
            got.add(int(out_line.split(":", 1)[0]))
        if not expected <= got:
            fails.append(f"{qid}: recorded lines {sorted(expected)} not in grep hits {sorted(got)} for {fname}")
        # 3. word count rule
        wc = len(needle.split())
        if wc > 25:
            fails.append(f"{qid}: {wc} words > 25")
        if str(wc) != wc_claim:
            fails.append(f"{qid}: word count claim {wc_claim} != recomputed {wc}")
        print(f"{'ok ' if not fails or fails[-1].split(':')[0] != qid else 'BAD'} {qid:4s} {loc:24s} words={wc}")

    print()
    sums = subprocess.run(["sha256sum", "-c", "SHA256SUMS"], cwd=FETCH,
                          capture_output=True, text=True)
    for out_line in sums.stdout.splitlines():
        print("sums: " + out_line)
    if sums.returncode != 0:
        fails.append("SHA256SUMS check failed:\n" + sums.stdout + sums.stderr)

    print()
    if fails:
        print(f"FAIL ({len(fails)} problem(s))")
        for f in fails:
            print("  " + f)
        return 1
    print(f"PASS: {len(rows)} quotes verified, all <= 25 words, all found by grep at the recorded line")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
