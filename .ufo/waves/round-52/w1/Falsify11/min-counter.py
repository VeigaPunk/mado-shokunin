#!/usr/bin/env python3
"""Seat-local minimal counter: population completeness + row uniqueness ONLY.

Deliberately implements neither of the two clauses C1 registers as distinguishing
(non-self evidence pointer, instrument-specific functional context). Reads committed
bytes from one revision; writes nothing.

Usage: min-counter.py --repo DIR --rev SHA
"""
import argparse
import os
import re
import subprocess
import sys

QUALITY_PY = re.compile(r"^quality/[^/]+\.py$")
COUNTERS_PY = re.compile(r"^quality/counters/[^/]+\.py$")
SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")
HEADER_CELLS = frozenset({"path", "file", "instrument", "tool", "artifact"})
LEDGER = "quality/tool-ledger.md"


def git(repo, *args):
    env = {k: os.environ.get(k, "") for k in ("PATH", "HOME")}
    env.setdefault("PATH", "/usr/bin:/bin")
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["LC_ALL"] = "C"
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, env=env)
    if p.returncode != 0:
        raise SystemExit("git failed: %s" % p.stderr.decode("utf-8", "replace"))
    return p.stdout


def population(repo, rev):
    out = git(repo, "ls-tree", "-r", "-z", rev)
    paths = []
    for rec in out.split(b"\0"):
        if not rec:
            continue
        head, sep, path = rec.partition(b"\t")
        if not sep:
            continue
        fields = head.split()
        if len(fields) < 3 or fields[1] != b"blob":
            continue
        p = path.decode("utf-8", "surrogateescape")
        if p.startswith("tools/") or QUALITY_PY.match(p) or COUNTERS_PY.match(p):
            paths.append(p)
    return sorted(set(paths))


def rows(text):
    out, seen = [], False
    fence = None
    for line in text.splitlines():
        s = line.strip()
        if fence is None:
            m = re.match(r"^(`{3,}|~{3,})", s)
            if m:
                fence = m.group(1)[0] * 3
                continue
        else:
            if s.startswith(fence):
                fence = None
            continue
        if not s.startswith("|"):
            continue
        cells = s.strip("|").split("|")
        if not seen and cells and cells[0].replace("`", "").strip().lower() in HEADER_CELLS:
            seen = True
            continue
        seen = True
        if cells and all(SEPARATOR_CELL.match(c.strip()) for c in cells if c.strip()):
            continue
        out.append(cells)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    pop = population(a.repo, a.rev)
    try:
        text = git(a.repo, "show", "%s:%s" % (a.rev, LEDGER)).decode("utf-8", "replace")
    except SystemExit:
        print("MIN: population=%d ledger_rows=0 dup=0 uncovered=%d verdict=TARGET_MISSED ledger=absent rev=%s"
              % (len(pop), len(pop), a.rev))
        return 1
    parsed = rows(text)
    paths = []
    dup = 0
    for cells in parsed:
        if len(cells) != 3:
            continue
        p = cells[0].replace("`", "").strip()
        p = re.sub(r":(?:\d+)(?:-\d+)?$", "", p)
        if p in paths:
            dup += 1
        else:
            paths.append(p)
    covered = [p for p in paths if p in pop]
    uncovered = [p for p in pop if p not in covered]
    ok = bool(pop) and not uncovered and not dup
    print("MIN: population=%d ledger_rows=%d dup=%d uncovered=%d verdict=%s rev=%s"
          % (len(pop), len(parsed), dup, len(uncovered),
             "TARGET_MET" if ok else "TARGET_MISSED", a.rev))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
