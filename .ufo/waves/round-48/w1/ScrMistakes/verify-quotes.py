#!/usr/bin/env python3
"""verify-quotes - compute every locator by grep and check the quote against the pinned bytes.

A locator written in this seat's prose is never typed: each entry of quotes.json names a file and
a literal pattern, the script greps the pattern (one command per entry), takes the first matching
line as the locator, and checks that the quote is contained in the whitespace-normalised lines
[start, start+span-1]. Exit 1 on any DIFFER.

Second mode (`--doc`/`--receipt`) reads a prose file and requires every `<file>:<line>` token it
writes to appear as a `LOC <file>:<line>` line of the receipt this script produced, so a locator
in the prose is traceable to the command that emitted it.

Usage:
  verify-quotes.py --repo . --quotes quotes.json
  verify-quotes.py --doc mistakes.md --receipt receipts/quote-check.txt --receipt receipts/check99-run.txt
"""
import argparse
import json
import os
import re
import subprocess
import sys

LOC = re.compile(r"([A-Za-z0-9_./-]+\.(?:md|py|json|txt|sh|xml|conf)):(\d+)")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--quotes", default=None)
    ap.add_argument("--doc", default=None)
    ap.add_argument("--receipt", action="append", default=[])
    a = ap.parse_args()

    if a.doc:
        try:
            body = open(a.doc, encoding="utf-8", errors="replace").read()
            recs = [open(r, encoding="utf-8", errors="replace").read() for r in a.receipt]
        except OSError as exc:
            print("UNREADABLE %s" % exc)
            return 2
        PROOF = ("LOC ", "OK ", "AMBIGUOUS ", "UNK-HEAD-CUT ", "OUT-OF-RANGE ",
                 "UNRESOLVED ", "NOPATTERN ", "DIFFER ", "MISSING ")
        proof_lines = [ln for r in recs for ln in r.splitlines() if ln.startswith(PROOF)]
        locs, missing = [], 0
        for m in LOC.finditer(body):
            t = "%s:%s" % (m.group(1), m.group(2))
            if t in locs:
                continue
            locs.append(t)
            if any(re.search(r"(?<![\w.-])%s(?![\w.])" % re.escape(t), ln)
                   for ln in proof_lines):
                continue
            missing += 1
            print("UNTYPED %s: no verifier line in %s" % (t, ",".join(a.receipt)))
        print("DOCLOC: locators=%d untyped=%d verdict=%s"
              % (len(locs), missing, "DIFFER" if missing else "OK"))
        return 1 if missing else 0

    if not a.quotes:
        print("NO-QUOTES (pass --quotes or --doc)")
        return 2
    quotes = json.load(open(a.quotes, encoding="utf-8"))
    bad = 0
    for q in quotes:
        path = q["file"] if os.path.isabs(q["file"]) else os.path.join(a.repo, q["file"])
        try:
            lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
        except OSError as exc:
            print("MISSING %s (%s)" % (path, exc))
            bad += 1
            continue
        pat = re.compile(re.escape(q["pattern"]))
        hit = next((i for i, ln in enumerate(lines, 1) if pat.search(ln)), None)
        if hit is None:
            print("NOPATTERN %s %r" % (q["file"], q["pattern"]))
            bad += 1
            continue
        span = " ".join(lines[hit - 1:hit - 1 + int(q.get("span", 1))])
        ok = norm(q["quote"]) in norm(span)
        if not ok:
            bad += 1
            print("DIFFER %s:%d quote=%r span=%r"
                  % (q["file"], hit, norm(q["quote"])[:90], norm(span)[:90]))
        else:
            print("OK %s:%d span=%d quote=%r"
                  % (q["file"], hit, int(q.get("span", 1)), norm(q["quote"])[:90]))
        print("LOC %s:%d" % (q["file"], hit))
    print("QUOTES: entries=%d differ=%d verdict=%s"
          % (len(quotes), bad, "DIFFER" if bad else "OK"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
