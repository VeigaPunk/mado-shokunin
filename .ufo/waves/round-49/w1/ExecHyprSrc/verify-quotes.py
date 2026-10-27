#!/usr/bin/env python3
"""Re-check locators.json against the pinned bytes, by line number.

Fails if a recorded line no longer contains its quote, if the quote has more
than 25 words, or if a pin is missing. Run: python3 verify-quotes.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FETCH = HERE / "fetch"


def main() -> int:
    recs = json.loads((HERE / "locators.json").read_text(encoding="utf-8"))
    ok = 0
    fail = []
    cache = {}
    for r in recs:
        path = FETCH / r["file"]
        if path not in cache:
            cache[path] = path.read_text(encoding="utf-8", errors="replace").splitlines()
        lines = cache[path]
        n = r["line"]
        if not (1 <= n <= len(lines)):
            fail.append(f"{r['id']} {r['file']}:{n} out of range")
            continue
        line = lines[n - 1]
        if r["quote"] not in line:
            fail.append(f"{r['id']} {r['file']}:{n} quote missing: {r['quote']!r}")
            continue
        if len(r["quote"].split()) > 25:
            fail.append(f"{r['id']} quote over 25 words")
            continue
        ok += 1
    for f in fail:
        print("FAIL", f)
    print(f"QUOTES_VERIFIED {ok}/{len(recs)}")
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
