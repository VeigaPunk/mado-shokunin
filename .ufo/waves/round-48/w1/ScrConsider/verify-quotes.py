#!/usr/bin/env python3
"""verify-quotes.py — seat ScrConsider (round 48 w1): verify every quote the seat's draft lifts from a source.

For each (file, quote) pair the locator is *computed* from the base revision's blob with ``git show <base>:<file>``
(never typed): the script finds the line numbers whose text contains the quote, compares that set with the locator the
draft claims, and counts the quote's words (limit 25).

Output, one line per quote, then the summary line exactly::

    QUOTE: file=<path> claimed=<a|b> found=<a|b|none> words=<n> verdict=PASS|FAIL reason=<...>

Exit status: 0 all PASS, 1 any FAIL, 2 usage/git error.
"""

import subprocess
import sys

BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WORD_LIMIT = 25

QUOTES = [
    ("considerthese/2026-10-26.md", "52", "Lead with round-level outcomes, not counter internals."),
    ("considerthese/2026-10-26.md", "52",
     "the useful signal for Joao is what his desktop tooling can now do".replace("Joao", "Jo\u00e3o")),
    ("corpus/lessons/round-32.md", "120", "operator-authored, read-only \u2014 not edited"),
    ("SCORECARD.md", "2656",
     "Claims declared at `c24adef2` (`.ufo/waves/round-47/claims.md`) before wave `w1` (41 build seats)"),
    ("corpus/QUALITY.md", "367",
     "Every round report states the lane's last-30-commit domain-versus-meta ratio with its command"),
    ("corpus/QUALITY.md", "399", "the reflection is a pointer, not evidence"),
    ("corpus/QUALITY.md", "399", "a number taken on trust is written `relayed:`"),
]


def blob(path):
    p = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (BASE, path)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("git show %s:%s failed: %s" % (BASE, path, p.stderr.strip()[:200]))
    return p.stdout.split("\n")


def main():
    cache, failed = {}, 0
    for path, claimed, quote in QUOTES:
        lines = cache.setdefault(path, blob(path))
        found = [str(i) for i, line in enumerate(lines, 1) if quote in line]
        words = len(quote.split())
        reasons = []
        if not found:
            reasons.append("absent")
        elif found != [claimed]:
            reasons.append("locator")
        if words > WORD_LIMIT:
            reasons.append("too-long")
        ok = not reasons
        failed += 0 if ok else 1
        print("QUOTE: file=%s claimed=%s found=%s words=%d verdict=%s reason=%s"
              % (path, claimed, "|".join(found) or "none", words, "PASS" if ok else "FAIL",
                 ",".join(reasons) or "none"))
    print("QUOTE_SUMMARY: quotes=%d pass=%d fail=%d base=%s"
          % (len(QUOTES), len(QUOTES) - failed, failed, BASE[:12]))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
