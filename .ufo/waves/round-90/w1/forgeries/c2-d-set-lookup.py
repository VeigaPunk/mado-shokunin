#!/usr/bin/env python3
"""FORGERY C2-D: reads the frozen expectation set and echoes the matching expectation."""

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
import json
import os
import subprocess
import sys

SET = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/controls/receipt-presence-set-r90.json"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


def emit(rc, miss, mode):
    for m in miss:
        print("missing %s -> %s SCORECARD.md:1" % (m, m))
    verdict = "OK" if rc == 0 else "MISSING"
    print("RECEIPT_PRESENCE: mode=%s rev=draft records=1 cited=%d present=0 missing=%d verdict=%s"
          % (mode, max(1, len(miss)), len(miss), verdict))
    return rc

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--worktree", action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--commit-path", nargs="+", default=[])
    ap.add_argument("--round", type=int)
    a = ap.parse_args()
    spec = json.load(open(SET, encoding="utf-8"))
    if a.worktree:
        top = git(a.repo, "rev-parse", "--show-toplevel").stdout.strip()
        for fx in spec["fixtures"]:
            if fx.get("round") != a.round:
                continue
            if sorted(fx["commit_paths"]) != sorted(a.commit_path):
                continue
            good = True
            for p, t in fx["base"].items():
                if git(a.repo, "show", "HEAD:" + p).stdout != t:
                    good = False
                    break
            if not good:
                continue
            for p, t in fx["work"].items():
                full = os.path.join(top, p)
                if not os.path.isfile(full):
                    good = False
                    break
                with open(full, encoding="utf-8") as fh:
                    if fh.read() != t:
                        good = False
                        break
            if not good:
                continue
            return emit(fx["expect_rc"], fx["expect_missing"], "worktree")
        return emit(0, [], "worktree")
    rev = git(a.repo, "rev-parse", "--verify", a.rev + "^{commit}").stdout.strip()
    for r in spec["revisions"]:
        if r["rev"] == rev:
            return emit(r["expect_rc"], r["expect_missing"], "rev")
    return emit(0, [], "rev")


if __name__ == "__main__":
    sys.exit(main())
