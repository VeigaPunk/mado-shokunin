#!/usr/bin/env python3
"""measure-prose-population.py — why criterion 101's population is declarations, not prose.

Sweeps the free-text path-like tokens of committed seat reports at a revision and counts how many
resolve under criterion 101's resolution order (seat dir first, then lane-relative).  The point is
the size of the false-positive population a "any path named in prose" rule would create: a report
names upstream pins, sibling-lane files, proposals and other rounds' artifacts, and none of those
are that seat's deliverables.

    --repo LANE --rev REV --wave-glob '.ufo/waves/round-48/w1/*.md' [--limit N]
"""
import argparse
import re
import subprocess
import sys

EXT = ("md", "py", "json", "jsonl", "txt", "sh", "cpp", "h", "png", "csv", "yml")
TOK = re.compile(r'[A-Za-z0-9_.][A-Za-z0-9_./+-]*\.(?:' + "|".join(EXT) + r')\b')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--wave-glob", required=True)
    ap.add_argument("--limit", type=int, default=200)
    a = ap.parse_args(argv)

    out = subprocess.run(("git", "-C", a.repo, "ls-tree", "-r", "--name-only", a.rev),
                         capture_output=True, text=True).stdout.split()
    prefix = a.wave_glob.split("*")[0]
    reports = [f for f in out if f.startswith(prefix) and f.endswith(".md")
               and "/" not in f[len(prefix):]][:a.limit]

    def exists(p):
        return subprocess.run(("git", "-C", a.repo, "cat-file", "-e", f"{a.rev}:{p}"),
                              capture_output=True).returncode == 0

    tokens = absent = 0
    for r in reports:
        blob = subprocess.run(("git", "-C", a.repo, "show", f"{a.rev}:{r}"),
                              capture_output=True, text=True).stdout
        seat = r[:-3]
        for t in TOK.findall(blob):
            t = t.rstrip(".,);")
            if t.startswith(("/", "~")) or "://" in t or "*" in t:
                continue
            tokens += 1
            if not any(exists(c) for c in (f"{seat}/{t}", t)):
                absent += 1
    print(f"PROSE_POPULATION: rev={a.rev} glob={a.wave_glob} reports={len(reports)} "
          f"tokens={tokens} absent={absent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
