#!/usr/bin/env python3
"""Verify every located quote in findings.md against the pinned trees in this seat dir.

Rules enforced:
  * each `Q[<path>:<line>] <quote>` names an existing file and a line that contains <quote> verbatim;
  * the quote is at most 25 words;
  * `src/...` paths resolve to pins/<basename> (pinned whole from the clone at efb5099);
    `tools/...` and `corpus/...` resolve to the lane repo;
  * pins/SHA256SUMS matches the files in pins/;
  * the seven round-43 Hyprland pins match this seat's copies byte for byte.
Exit 0 only if everything passes.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
PINS = os.path.join(HERE, "pins")
FINDINGS = os.path.join(HERE, "findings.md")
PIN_ROOT = os.path.join(LANE, ".ufo", "waves", "round-43", "receipts", "fetch-sha256.txt")

QRE = re.compile(r"Q\[([^\]\s]+):(\d+)\] (.*)$")


def resolve(path):
    if path.startswith("src/"):
        return os.path.join(PINS, os.path.basename(path)), "pins"
    return os.path.join(LANE, path), "lane"


def main():
    fails = 0
    quotes = 0
    ledger = []
    for ln, raw in enumerate(open(FINDINGS, encoding="utf-8").read().splitlines(), 1):
        m = QRE.search(raw)
        if not m:
            continue
        path, lineno, quote = m.group(1), int(m.group(2)), m.group(3)
        if quote.endswith("  "):
            quote = quote.rstrip()
        quotes += 1
        full, root = resolve(path)
        words = len(quote.split())
        if words > 25:
            ledger.append("FAIL words=%d %s:%d" % (words, path, lineno))
            fails += 1
            continue
        if not os.path.exists(full):
            ledger.append("FAIL missing-file %s (%s)" % (path, full))
            fails += 1
            continue
        lines = open(full, encoding="utf-8", errors="replace").read().splitlines()
        if lineno > len(lines):
            ledger.append("FAIL past-eof %s:%d" % (path, lineno))
            fails += 1
            continue
        if quote not in lines[lineno - 1]:
            ledger.append("FAIL not-on-line %s:%d quote=%r line=%r" % (path, lineno, quote, lines[lineno - 1]))
            fails += 1
            continue
        ledger.append("ok   %-4d words  %s:%d  [%s]  %s" % (words, path, lineno, root, quote))
    print("\n".join(ledger))
    print("quotes=%d fails=%d" % (quotes, fails))

    # pins/SHA256SUMS
    listed = {}
    for line in open(os.path.join(PINS, "SHA256SUMS"), encoding="utf-8"):
        h, name, rel = line.split()
        listed[name] = (h, rel)
    for name, (h, rel) in sorted(listed.items()):
        p = os.path.join(PINS, name)
        got = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None
        if got != h:
            print("FAIL pin %s %s" % (name, got))
            fails += 1
    print("pins checked=%d" % len(listed))

    # seven round-43 Hyprland fetch pins vs this seat's copies
    fpin = {}
    for line in open(PIN_ROOT, encoding="utf-8"):
        h, name = line.split()
        fpin[name] = h
    checked = 0
    for name, h in fpin.items():
        if not name.startswith("Hyprland-"):
            continue
        base = name[len("Hyprland-"):]
        p = os.path.join(PINS, base)
        got = hashlib.sha256(open(p, "rb").read()).hexdigest()
        checked += 1
        if got != h:
            print("FAIL fetch-pin %s" % name)
            fails += 1
    print("round-43 fetch pins re-checked=%d" % checked)

    for need in ("findings.md", "receipts/re2-anchors.txt", "receipts/re2_anchors.py",
                 "receipts/clone-identity.txt", "receipts/grep-static-size-src.txt",
                 "receipts/grep-geometric-current-src.txt", "receipts/grep-calculateExpression-src.txt",
                 "receipts/grep-geometric-current-hyprctl.txt"):
        if not os.path.exists(os.path.join(HERE, need)):
            print("FAIL missing receipt %s" % need)
            fails += 1

    print("VERIFY: %s" % ("PASS" if fails == 0 else "FAIL"))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
