#!/usr/bin/env python3
"""Check every locator findings.md cites: receipts/*:N must exist and be in range, counter:N and the reference's
:N must be a real non-empty line. Bare receipt-relative `:N` forms are printed for eyeball with their context."""
import os
import re
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/CritC1Cheat"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r45-monitors.py")
REF = os.path.join(LANE, ".ufo/waves/round-45/l1-draft/mado-monitors.py")
REC = os.path.join(SEAT, "receipts")

doc = open(os.path.join(SEAT, "findings.md")).read()
lines = doc.split("\n")
cache = {}
bad = 0


def load(path):
    if path not in cache:
        cache[path] = open(path, "r", errors="replace").read().split("\n")
    return cache[path]


def check(label, path, n):
    global bad
    body = load(path)
    if not (1 <= n <= len(body)) or (body[n - 1].strip() == "" and not label.startswith("receipts")):
        print("BAD  %-52s %s:%d (file has %d lines)" % (label, os.path.basename(path), n, len(body)))
        bad += 1
        return False
    return True


print("# receipts/<file>:<n>[-<m>]")
for m in re.finditer(r"receipts/([\w.-]+):(\d+)(?:-(\d+))?", doc):
    f, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
    p = os.path.join(REC, f)
    if not os.path.exists(p):
        print("BAD  missing receipt %s" % f)
        bad += 1
        continue
    body = load(p)
    ok = 1 <= a <= b <= len(body)
    print("%s receipts/%-18s %d-%d (file has %d lines)" % ("OK " if ok else "BAD", f, a, b, len(body)))
    if not ok:
        bad += 1

print("\n# counter:<n>")
for m in re.finditer(r"counter:(\d+)", doc):
    n = int(m.group(1))
    check("counter", COUNTER, n)
    print("%s counter:%-4d %s" % ("OK " if check("counter", COUNTER, n) else "BAD", n,
                                  load(COUNTER)[n - 1].strip()[:70]))

print("\n# l1-draft/mado-monitors.py:<n> and bare `:n` (checked against the reference)")
for m in re.finditer(r"(?:l1-draft/mado-monitors\.py|`):(\d+)`?", doc):
    n = int(m.group(1))
    body = load(REF)
    if not (1 <= n <= len(body)):
        print("BAD  reference:%-4d out of range (%d lines)" % (n, len(body)))
        bad += 1
        continue
    print("OK  reference:%-4d %s" % (n, body[n - 1].strip()[:70]))

print("\nCITATIONS: bad=%d" % bad)
sys.exit(1 if bad else 0)
