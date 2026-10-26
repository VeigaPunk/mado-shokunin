#!/usr/bin/env python3
"""Verify every quote in pins/quotes.tsv: verbatim, at the claimed line, <= 25 words; pins match SHA256SUMS."""
import hashlib
import os
import sys

PINS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pins")
Q = os.path.join(PINS, "quotes.tsv")
fails = 0
rows = 0
with open(Q, encoding="utf-8") as fh:
    for raw in fh:
        raw = raw.rstrip("\n")
        if not raw or raw.startswith("#"):
            continue
        fname, lineno, quote = raw.split("\t", 2)
        rows += 1
        path = os.path.join(PINS, fname)
        if not os.path.isfile(path):
            print(f"FAIL file missing {fname}")
            fails += 1
            continue
        words = len(quote.split())
        if words > 25:
            print(f"FAIL >25 words ({words}) {fname}:{lineno}")
            fails += 1
        with open(path, encoding="utf-8", errors="replace") as p:
            lines = p.read().split("\n")
        n = int(lineno)
        ok = False
        if n == 0:
            ok = any(quote in ln for ln in lines)
        else:
            if 1 <= n <= len(lines) and quote in lines[n - 1]:
                ok = True
        print(("PASS" if ok else "FAIL") + f" {fname}:{lineno} ({words}w) {quote[:60]}")
        if not ok:
            fails += 1

print(f"quotes={rows} fails={fails}")
# checksum coverage
sums = {}
with open(os.path.join(PINS, "SHA256SUMS"), encoding="utf-8") as fh:
    for raw in fh:
        h, name = raw.split()
        sums[name] = h
missing = []
for name in sorted(os.listdir(PINS)):
    if name == "SHA256SUMS":
        continue
    if name not in sums:
        missing.append(name)
        continue
    with open(os.path.join(PINS, name), "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != sums[name]:
        print(f"FAIL sha256 {name} want {sums[name]} got {got}")
        fails += 1
extra = [n for n in sums if not os.path.exists(os.path.join(PINS, n))]
print(f"checksummed={len(sums)} uncovered={missing} missing={extra}")
if missing or extra:
    fails += 1
print("VERIFY: PASS" if fails == 0 else f"VERIFY: FAIL ({fails})")
sys.exit(0 if fails == 0 else 1)
