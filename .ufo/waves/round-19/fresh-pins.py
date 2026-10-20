#!/usr/bin/env python3
"""Round-19 C2 counter: walker version-pin currency (freshness sub-axis).

Usage: fresh-pins.py REV  -> one JSON object on stdout; exit 0 printed, 2 could-not-evaluate.

Fixed denominator (pinned at pre-registration): the owned files at commit
9c54c56 whose bytes contain the token `2.17.0` — paths under
corpus/knowledge/*.md, corpus/README.md, SKILL.md, PROVINCE.md and tools/*.
Lessons, verifier spot-checks and SOURCES.md are dated records, not
present-tense claims, and are outside the set.

A file is current at REV when it still exists there and carries at least one
line containing the superseding version `2.17.2` together with an `S###`
SOURCES row token on that same line (an in-file, source-cited forward
pointer or a re-pinned value). score = 10 * current / denominator.

Reads committed bytes only (`git ls-tree`, `git show`).
"""
import json
import os
import re
import subprocess
import sys

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PIN_REV = "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d"
OLD = "2.17.0"
POINTER = re.compile(r"2\.17\.2.*\bS\d{3}\b|\bS\d{3}\b.*2\.17\.2")


def git(*a):
    return subprocess.run(["git", "-C", LANE, *a], capture_output=True)


def in_scope(p):
    return ((p.startswith("corpus/knowledge/") and p.endswith(".md"))
            or p in ("corpus/README.md", "SKILL.md", "PROVINCE.md")
            or p.startswith("tools/"))


def main():
    if len(sys.argv) != 2:
        print("usage: fresh-pins.py REV", file=sys.stderr)
        return 2
    rev = sys.argv[1]
    c = git("rev-parse", "--verify", rev + "^{commit}")
    if c.returncode != 0:
        print(f"could_not_evaluate: rev {rev}", file=sys.stderr)
        return 2
    ls = git("ls-tree", "-r", "--name-only", PIN_REV)
    if ls.returncode != 0:
        print("could_not_evaluate: ls-tree", file=sys.stderr)
        return 2
    denom = []
    for p in ls.stdout.decode().splitlines():
        if not in_scope(p):
            continue
        b = git("show", f"{PIN_REV}:{p}")
        if b.returncode != 0:
            print(f"could_not_evaluate: show {p}", file=sys.stderr)
            return 2
        if OLD.encode() in b.stdout:
            denom.append(p)
    rows = []
    for p in sorted(denom):
        b = git("show", f"{rev}:{p}")
        if b.returncode != 0:
            rows.append({"path": p, "current": False, "reason": "absent at REV"})
            continue
        hits = [i + 1 for i, ln in enumerate(b.stdout.decode(errors="replace").splitlines())
                if POINTER.search(ln)]
        rows.append({"path": p, "current": bool(hits), "pointer_lines": hits[:5]})
    cur = sum(r["current"] for r in rows)
    print(json.dumps({
        "schema": "mado-fresh-pins-r19-v1",
        "rev": rev,
        "commit": c.stdout.decode().strip(),
        "pin_rev": PIN_REV,
        "denominator": len(rows),
        "current": cur,
        "score": round(10 * cur / len(rows), 4) if rows else None,
        "rows": rows,
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
