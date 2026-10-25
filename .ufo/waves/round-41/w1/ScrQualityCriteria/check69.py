#!/usr/bin/env python3
"""check69 - every measurement a report quotes names a revision a committed receipt carries.

QUALITY criterion 69. A report's evidence row is read as "this number was measured at
revision R". The check extracts every revision token the report writes in measurement form
(`rev=<hex>`, `rev <hex>`, `at <hex>`), then requires, at the report's own revision, at least
one committed receipt under the round's receipts directory whose bytes contain that token.

Usage:
  check69.py --repo . --rev <REV> --report <path-in-repo> --receipts <dir-in-repo>
  check69.py --repo . --rev <REV> --report <file-on-disk> --receipts <dir> --text

Exit 0 = PASS (every cited revision is carried by a committed receipt), 1 = FAIL,
2 = the report itself is not readable at --rev.
"""
import argparse
import re
import subprocess
import sys

TOKEN = re.compile(r'(?:rev=|rev\s|at\s)([0-9a-f]{7,40})\b')


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--receipts", required=True)
    ap.add_argument("--text", action="store_true",
                    help="read --report from disk instead of from --rev")
    a = ap.parse_args()

    if a.text:
        try:
            body = open(a.report, encoding="utf-8", errors="replace").read()
        except OSError as exc:
            print("MISSING-REPORT %s (%s)" % (a.report, exc))
            return 2
    else:
        r = git(a.repo, "show", "%s:%s" % (a.rev, a.report))
        if r.returncode:
            print("MISSING-REPORT %s at %s" % (a.report, a.rev))
            return 2
        body = r.stdout

    tokens = []
    for m in TOKEN.finditer(body):
        if m.group(1) not in tokens:
            tokens.append(m.group(1))
    if not tokens:
        print("NO-CITED-REVISION %s carries no rev=/rev /at token" % a.report)
        return 1

    bad = 0
    for t in tokens:
        g = git(a.repo, "grep", "-l", "-F", t, a.rev, "--", a.receipts)
        hits = [ln for ln in g.stdout.splitlines() if ln.strip()]
        if hits:
            print("FOUND %s <- %s" % (t, hits[0].split(":", 1)[1]))
        else:
            bad += 1
            print("MISSING %s cited at %s: no committed receipt under %s names it"
                  % (t, a.rev, a.receipts))
    if bad:
        print("FAIL %d/%d cited revisions lack a committed receipt" % (bad, len(tokens)))
        return 1
    print("PASS %d/%d cited revisions carried by committed receipts" % (len(tokens), len(tokens)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
