#!/usr/bin/env python3
"""check98 - every seat that reports a frozen-instrument blind spot is routed by name.

QUALITY criterion 98 (draft, round 48). A wave-w2 seat exists to attack a frozen instrument. When
it returns a blind spot (the instrument cannot see a class), a surviving mutant or an unchecked
clause, that gap is the round's most valuable output; a report or a lesson that never names the
seat leaves the gap with no owner and the next round re-freezes the same instrument.

Detection, per top-level `*.md` seat report under `--seats`: at least one line carries
`blind to`, `blind spot`, `coverage hole`, `coverage gap`, `not covered by any clause`, or a table
row whose verdict cell is `survived` without `equivalent`. Routing: the seat stem appears in the
report text or the lesson text.

Usage:
  check98.py --repo . --rev REV --seats <dir-in-repo> --lesson <path-in-repo>
             --report <path-in-repo|file-on-disk> [--report-text]
Exit 0 = every finding seat is routed, 1 = at least one is unrouted, 2 = input unreadable.
"""
import argparse
import glob
import os
import re
import subprocess
import sys

PHRASE = re.compile(r"blind to|blind spot|coverage hole|coverage gap|not covered by any clause", re.I)
SURVIVED = re.compile(r"\|\s*survived\s*\|", re.I)
EQUIV = re.compile(r"equivalent", re.I)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                              capture_output=True, text=True, errors="replace")


def findings(text):
    out = []
    for ln in text.splitlines():
        if PHRASE.search(ln):
            out.append(PHRASE.search(ln).group(0).lower())
        elif SURVIVED.search(ln) and not EQUIV.search(ln):
            out.append("survived-mutant")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--seats", required=True)
    ap.add_argument("--lesson", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--report-text", action="store_true")
    a = ap.parse_args()

    if a.report_text:
        try:
            report = open(a.report, encoding="utf-8", errors="replace").read()
        except OSError as exc:
            print("MISSING-REPORT %s (%s)" % (a.report, exc))
            return 2
    else:
        r = git(a.repo, "show", "%s:%s" % (a.rev, a.report))
        if r.returncode:
            print("MISSING-REPORT %s at %s" % (a.report, a.rev))
            return 2
        report = r.stdout
    r = git(a.repo, "show", "%s:%s" % (a.rev, a.lesson))
    if r.returncode:
        print("MISSING-LESSON %s at %s" % (a.lesson, a.rev))
        return 2
    lesson = r.stdout

    paths = sorted(glob.glob(os.path.join(a.repo, a.seats, "*.md")))
    if not paths:
        print("NO-SEATS %s holds no *.md" % a.seats)
        return 2

    unrouted, flagged = 0, 0
    for p in paths:
        stem = os.path.basename(p)[:-3]
        try:
            body = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        f = findings(body)
        if not f:
            continue
        flagged += 1
        nr, nl = report.count(stem), lesson.count(stem)
        routed = bool(nr or nl)
        if not routed:
            unrouted += 1
        print("SEAT %-22s hits=%-3d token=%-18s report=%d lesson=%d verdict=%s"
              % (stem, len(f), f[0], nr, nl, "ROUTED" if routed else "UNROUTED"))
    print("CHECK98: seats=%d finding_seats=%d unrouted=%d verdict=%s"
          % (len(paths), flagged, unrouted, "UNROUTED" if unrouted else "OK"))
    return 1 if unrouted else 0


if __name__ == "__main__":
    sys.exit(main())
