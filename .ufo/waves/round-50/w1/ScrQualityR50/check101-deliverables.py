#!/usr/bin/env python3
"""check101-deliverables.py — seat prototype for candidate QUALITY criterion 101 (M49-3).

Every deliverable a seat or report *declares* must exist at the cited revision.

Declarations are read from two grammars, and nothing else in the prose is in scope (free-text
path-like tokens are references, proposals or upstream names, not declarations):

    Report: <path>                       the trailer every seat dispatch requires
    under a `## Deliverables` heading,   one `- \\`<path>\\`` or `- <path>` bullet per deliverable
    (or `## Files written`, `Written:`)

Resolution order for a declared path: as written if it contains `/`, else `<seat-dir>/<path>`
where `<seat-dir>` is `--seat-dir` or the report path with `.md` stripped (the lane's
`w1/<Seat>.md` + `w1/<Seat>/` convention).

Modes:
    --repo R --rev REV --report P...     prove each declaration with `git cat-file -e REV:path`
    --file P... [--seat-dir D]           pre-commit form: prove each with `test -f` (the M49-3 rule)

Output: `DECLARATION report=<p> named=<path> grammar=trailer|section status=EXISTS|ABSENT`, then
`CHECK101: reports=<n> declared=<n> exists=<n> absent=<n> undeclared=<n> verdict=OK|FAIL`;
exit 1 on any ABSENT, or on a report that declares nothing (a seat report carries `Report:`).
"""
import argparse
import os
import re
import subprocess
import sys

HEAD = re.compile(r'^#{2,3}\s+(Deliverables?|Files written)\b', re.I)
WRITTEN = re.compile(r'^\s*Written\s*:', re.I)
BULLET = re.compile(r'^\s*[-*]\s+`?([A-Za-z0-9_.][A-Za-z0-9_./+-]*\.(?:md|py|json|jsonl|txt|sh|cpp|h|png|gif|yml|csv))`?')
TRAILER = re.compile(r'^Report:\s*`?([A-Za-z0-9_.][A-Za-z0-9_./+-]*\.md)`?\s*$', re.M)


def declarations(text):
    out = []
    for m in TRAILER.finditer(text):
        out.append(("trailer", m.group(1)))
    in_sec = False
    for line in text.splitlines():
        if HEAD.match(line) or WRITTEN.match(line):
            in_sec = True
            continue
        if in_sec and re.match(r'^#{1,3}\s', line):
            in_sec = False
            continue
        if in_sec:
            m = BULLET.match(line)
            if m:
                out.append(("section", m.group(1)))
    return out


def candidates(path, seat):
    """GIT_ORDER: seat-dir-relative first (the lane's `w1/<Seat>.md` + `w1/<Seat>/`), then as
    written.  A declaration is not found until one candidate exists."""
    if path.startswith("/") or path.startswith("~") or "://" in path:
        return []
    out = []
    if not path.startswith(seat + "/"):
        out.append(f"{seat}/{path}")
    if path not in out:
        out.append(path)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--report", action="append", nargs="+", default=[])
    ap.add_argument("--file", action="append", nargs="+", default=[])
    ap.add_argument("--seat-dir")
    ap.add_argument("--require-declaration", action="store_true",
                    help="fail a report that declares nothing (use over a wave dir at/after this criterion's round)")
    a = ap.parse_args(argv)

    a.report = [x for g in a.report for x in g]
    a.file = [x for g in a.file for x in g]
    reports = declared = exists = absent = undeclared = 0

    def seat_for(path):
        if a.seat_dir:
            return a.seat_dir.rstrip("/")
        return path[:-3] if path.endswith(".md") else path

    if a.report:
        if not (a.repo and a.rev):
            print("CHECK101: --report needs --repo and --rev", file=sys.stderr)
            return 2
        for path in a.report:
            blob = subprocess.run(("git", "-C", a.repo, "show", f"{a.rev}:{path}"),
                                  capture_output=True, text=True)
            if blob.returncode != 0:
                print(f"REPORT_UNRESOLVED rev={a.rev} report={path}")
                absent += 1
                continue
            reports += 1
            decls = declarations(blob.stdout)
            if not decls:
                print(f"DECLARATION report={path} grammar=none status=UNDECLARED")
                undeclared += 1
            for grammar, name in decls:
                cands = candidates(name, seat_for(path))
                declared += 1
                if not cands:
                    print(f"DECLARATION report={path} named={name} grammar={grammar} status=NOT-LANE")
                    continue
                hit = None
                for c in cands:
                    if subprocess.run(("git", "-C", a.repo, "cat-file", "-e", f"{a.rev}:{c}"),
                                      capture_output=True).returncode == 0:
                        hit = c
                        break
                if hit:
                    exists += 1
                    print(f"DECLARATION report={path} named={hit} grammar={grammar} status=EXISTS")
                else:
                    absent += 1
                    print(f"DECLARATION report={path} named={cands[0]} grammar={grammar} status=ABSENT")

    for path in a.file:
        with open(path, "r", errors="replace") as fh:
            text = fh.read()
        reports += 1
        decls = declarations(text)
        if not decls:
            print(f"DECLARATION report={path} grammar=none status=UNDECLARED")
            undeclared += 1
        for grammar, name in decls:
            cands = candidates(name, seat_for(path))
            declared += 1
            if not cands:
                print(f"DECLARATION report={path} named={name} grammar={grammar} status=NOT-LANE")
                continue
            hit = next((c for c in cands if os.path.isfile(c)), None)
            if hit:
                exists += 1
                print(f"DECLARATION report={path} named={hit} grammar={grammar} status=EXISTS")
            else:
                absent += 1
                print(f"DECLARATION report={path} named={cands[0]} grammar={grammar} status=ABSENT")

    fail = absent + (undeclared if a.require_declaration else 0)
    print(f"CHECK101: reports={reports} declared={declared} exists={exists} absent={absent} "
          f"undeclared={undeclared} verdict={'OK' if fail == 0 else 'FAIL'}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
