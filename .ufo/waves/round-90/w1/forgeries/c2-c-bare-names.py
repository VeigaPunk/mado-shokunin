#!/usr/bin/env python3
"""FORGERY C2-C: flags every bare receipts/ citation as missing."""

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
import re
import subprocess
import sys

def is_record(path):
    if path in ("SCORECARD.md", "LOG.md", "corpus/QUALITY.md", "corpus/README.md"):
        return True
    for sub in ("corpus/lessons/", "corpus/knowledge/"):
        if path.startswith(sub) and path.endswith(".md") and "/" not in path[len(sub):]:
            return True
    return False


BARE = re.compile(r"(?<![A-Za-z0-9_./-])receipts/[A-Za-z0-9._-]+?\.(?:txt|json|jsonl|md|log|csv|tsv)(?![A-Za-z0-9_-])")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")

def emit(rc, miss, mode):
    for m in miss:
        print("missing %s -> %s SCORECARD.md:1" % (m, m))
    verdict = "OK" if rc == 0 else "MISSING"
    print("RECEIPT_PRESENCE: mode=%s rev=draft records=1 cited=%d present=0 missing=%d verdict=%s"
          % (mode, max(1, len(miss)), len(miss), verdict))
    return rc

def bare_cites(diff):
    out, path, n = [], None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
            continue
        if line.startswith("--- ") or line.startswith("diff "):
            continue
        m = HUNK.match(line)
        if m:
            n = int(m.group(1))
            continue
        if path is None or not is_record(path):
            continue
        if line.startswith("+"):
            for c in BARE.finditer(line[1:]):
                out.append(c.group(0))
            n += 1
        elif not line.startswith("-"):
            n += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--worktree", action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--commit-path", nargs="+", default=[])
    ap.add_argument("--round", type=int)
    a = ap.parse_args()
    if a.worktree:
        if not a.base:
            return emit(0, [], "worktree")
        d = subprocess.run(["git", "-C", a.repo, "diff", "--no-color", "--no-ext-diff", "--no-renames",
                            "-U0", a.base, "--"], capture_output=True, text=True).stdout
        mode = "worktree"
    else:
        if not a.rev:
            return emit(0, [], "rev")
        d = subprocess.run(["git", "-C", a.repo, "show", "--no-color", "--no-ext-diff", "--no-renames",
                            "-U0", "--format=", a.rev, "--"], capture_output=True, text=True).stdout
        mode = "rev"
    miss = sorted(set(bare_cites(d)))
    return emit(1 if miss else 0, miss, mode)


if __name__ == "__main__":
    sys.exit(main())
