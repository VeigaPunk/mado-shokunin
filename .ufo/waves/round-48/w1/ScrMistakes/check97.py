#!/usr/bin/env python3
"""check97 - every state number a report states carries a committed receipt, not only a revision.

QUALITY criterion 97 (draft, round 48; extension of criterion 69). Criterion 69 extracts
revision tokens (`rev=<hex>`) from a report and requires a committed receipt carrying each.
A number a report states in a detector's own vocabulary (`findings=128`, `files=18371`,
`fixtures=190/190`, `explain ed=190/190`) is not a revision token, so criterion 69 never reads
it: its own instrument returns PASS on a report that carries an unreceipted `findings=128`.

This check extracts every `<lowercase_key>=<number...>` token from the report and requires the
literal token in some committed receipt under `--receipts` at `--rev`.

Usage:
  check97.py --repo . --rev REV --report <path-in-repo|file-on-disk> --receipts <dir-in-repo>
             [--text] [--quiet-ok]
Exit 0 = every number is carried, 1 = at least one is not, 2 = report or receipts unreadable.
"""
import argparse
import re
import subprocess
import sys

TOKEN = re.compile(r"(?<![A-Za-z0-9_])[a-z_]+=[0-9][0-9A-Za-z_/.]*")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                              capture_output=True, text=True, errors="replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--receipts", required=True)
    ap.add_argument("--text", action="store_true")
    ap.add_argument("--quiet-ok", action="store_true")
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

    seen, tokens = set(), []
    for m in TOKEN.finditer(body):
        t = m.group(0)
        if t.endswith(".") or t.endswith("/"):
            t = t.rstrip("./")
        if t not in seen:
            seen.add(t)
            tokens.append(t)
    if not tokens:
        print("NO-NUMBERS %s states no <key>=<number> token" % a.report)
        return 1

    ls = git(a.repo, "ls-tree", "-r", "--name-only", a.rev, "--", a.receipts)
    if ls.returncode:
        print("MISSING-RECEIPTS %s at %s" % (a.receipts, a.rev))
        return 2
    files = [p for p in ls.stdout.splitlines() if p.strip()]
    blobs = {}
    for p in files:
        r = git(a.repo, "show", "%s:%s" % (a.rev, p))
        if not r.returncode:
            blobs[p] = r.stdout

    bad = 0
    for t in tokens:
        where = next((p for p, txt in blobs.items() if t in txt), None)
        if where:
            if not a.quiet_ok:
                print("FOUND %s <- %s" % (t, where))
        else:
            bad += 1
            print("MISSING %s: no committed receipt under %s at %s carries it"
                  % (t, a.receipts, a.rev))
    print("CHECK97: tokens=%d missing=%d receipts=%d verdict=%s"
          % (len(tokens), bad, len(blobs), "UNRECEIPTED" if bad else "OK"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
