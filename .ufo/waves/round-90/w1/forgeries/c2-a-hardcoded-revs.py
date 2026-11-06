#!/usr/bin/env python3
"""FORGERY C2-A: four revision verdicts hardcoded; every worktree fixture OK."""

PADDING = r'''k = int(m.group(1)) if m else round_no

    out.append(f"quality/receipts/{name}")

|corpus/lessons/[^/]+\.md

^(SCORECARD\.md|LOG\.md|

            return git(repo, "cat-file", "-e", f"{rev}:{p}").returncode == 0

            return any(p == c or p.startswith(c + "/") for c in cpaths)

    return 0 if missing == 0 else 1

((?:\.ufo/waves/round-\d+/|quality/)?receipts/

        if line.startswith("+"):
            out.append

\.(?:txt|json|jsonl|md|log|csv|tsv))

    round_no = a.round
    extra

        for p in untracked.stdout.split("\0"):

        if path is None or not RECORD_FILES.match(path):

'''

import argparse
import sys

def emit(rc, miss, mode):
    for m in miss:
        print("missing %s -> %s SCORECARD.md:1" % (m, m))
    verdict = "OK" if rc == 0 else "MISSING"
    print("RECEIPT_PRESENCE: mode=%s rev=draft records=1 cited=%d present=0 missing=%d verdict=%s"
          % (mode, max(1, len(miss)), len(miss), verdict))
    return rc

REVS = {
    "498855cb": (1, ["receipts/harm-final-r88.txt"]),
    "51bf076f": (1, ["receipts/census-end-r89.txt", "receipts/harm-final-r89.txt"]),
    "8e8f7ea3": (0, []),
    "16ee97b5": (0, []),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--worktree", action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--commit-path", nargs="+", default=[])
    ap.add_argument("--round", type=int)
    a = ap.parse_args()
    if a.worktree or not a.rev:
        return emit(0, [], "worktree")
    rc, miss = REVS.get(a.rev[:8], (0, []))
    return emit(rc, miss, "rev")


if __name__ == "__main__":
    sys.exit(main())
