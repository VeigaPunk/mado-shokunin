#!/usr/bin/env python3
"""CritC2V2Forgery - lay the seven forgery commits on the data commit in a scratch clone.

Never mutates the lane: every git call names -C <clone>, the clone is cloned --shared from the lane
by repro.sh, and its toplevel is checked before the first commit.
"""
import os
import subprocess
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
DATA = "e46789213830597348fe96a351ae004d10587385"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
CLONE = "/fast/scratch/hyaku/mado-r44/CritC2V2Forgery/clone"
ORDER = ("f1-surface-false.md", "f2-decision-table-noid.md", "f3-census-words.md",
         "f4-wide-range.md", "f4b-eof-range.md", "f5-one-line-all-surfaces.md",
         "f6-census-numbers-false.md")


ENV = dict(os.environ, GIT_AUTHOR_DATE="2026-10-26T00:00:00 +0000",
           GIT_COMMITTER_DATE="2026-10-26T00:00:00 +0000")


def git(*args):
    p = subprocess.run(["git", "-C", CLONE, *args], capture_output=True, text=True,
                       env=ENV)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr))
    return p.stdout


def main():
    if os.path.realpath(git("rev-parse", "--show-toplevel").strip()) != CLONE:
        raise SystemExit("clone toplevel mismatch")
    git("checkout", "-q", "--detach", DATA)
    git("config", "user.name", "crit-c2v2-forgery")
    git("config", "user.email", "crit-c2v2-forgery@invalid")
    out = []
    for name in ORDER:
        with open(os.path.join(SEAT, "fixtures", name), encoding="utf-8") as fh:
            text = fh.read()
        with open(os.path.join(CLONE, ENTRY), "w", encoding="utf-8") as fh:
            fh.write(text)
        git("add", ENTRY)
        git("commit", "-q", "-m", "fixture: %s" % name)
        rev = git("rev-parse", "HEAD").strip()
        out.append((rev, name))
        print("%s %s" % (rev, name))
    with open(os.path.join(SEAT, "fixtures", "commits.txt"), "w", encoding="utf-8") as fh:
        for rev, name in out:
            fh.write("%s %s\n" % (rev, name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
