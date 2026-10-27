#!/usr/bin/env python3
"""verify-locators.py - check every lesson/code locator this seat's criteria.md cites.

Each row is (path, line, token): the token must occur on that line of that file.
Locators were computed with `grep -n` while the criteria were written, never typed.

Reads only. Usage: verify-locators.py [--lane DIR]
Exit: 0 every locator supported, 1 at least one misses.
"""
import argparse
import os
import sys

ROWS = [
    ("corpus/lessons/round-48.md", 259, "M48-8"),
    ("corpus/lessons/round-48.md", 263, "M48-10"),
    ("corpus/lessons/round-48.md", 269, "M48-13"),
    ("corpus/lessons/round-48-verifier-spotcheck.md", 178, "N2"),
    ("corpus/lessons/round-48-verifier-spotcheck.md", 185, "N4"),
    (".ufo/waves/round-48/w1/SentPrivacy.md", 17, "16 of 19"),
    (".ufo/waves/round-48/a4r1-results.json", 40, "RLIMIT_FSIZE=1 MiB"),
    ("SKILL.md", 770, "mado-session-material"),
    ("quality/check-session-material.py", 1606, 'default="ufo"'),
    (".ufo/waves/round-48/w2/MutC1ReadOnly/mkmutants.py", 31, 'os.environ["HOME"]'),
    (".ufo/waves/round-48/w2/MutC1ReadOnly/mkmutants.py", 39, 'open(_p, "w")'),
    (".ufo/waves/round-48/w2/MutC1ReadOnly/mkmutants.py", 40, "r48-w2"),
    (".ufo/waves/round-48/receipts/v2/c2v2-revc2counter-summary.json", 24, "a-rev-base-direct"),
    (".ufo/waves/round-48/receipts/v2/c2v2-revc2counter-summary.json", 36, "a-entry-at-base"),
    (".ufo/waves/round-48/receipts/a4/session-material-tip.txt", 4, "findings=159"),
    (".ufo/waves/round-48/receipts/live-terminal-cache-r48.txt", 4, "host_cache_untouched_sha256"),
    ("corpus/QUALITY.md", 50, "19."),
    ("corpus/QUALITY.md", 249, "30."),
    ("corpus/QUALITY.md", 318, "33."),
    ("corpus/QUALITY.md", 328, "37."),
    ("corpus/QUALITY.md", 369, "61."),
    ("corpus/QUALITY.md", 373, "63."),
    ("corpus/QUALITY.md", 375, "64."),
    ("corpus/QUALITY.md", 403, "78."),
    ("corpus/QUALITY.md", 422, "87."),
    ("corpus/QUALITY.md", 444, "89."),
    ("corpus/QUALITY.md", 480, "93."),
    ("corpus/QUALITY.md", 498, "95."),
    ("corpus/QUALITY.md", 533, "98."),
]


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--lane", default=".")
    args = parser.parse_args()
    bad = 0
    for path, number, token in ROWS:
        full = os.path.join(args.lane, path)
        try:
            lines = open(full, "r", errors="replace").read().splitlines()
        except OSError as exc:
            print("LOC %s:%d verdict=UNREADABLE %s" % (path, number, exc))
            bad += 1
            continue
        if number > len(lines):
            print("LOC %s:%d verdict=OUT_OF_RANGE" % (path, number))
            bad += 1
            continue
        if token in lines[number - 1]:
            print("LOC %s:%d token=%s verdict=OK" % (path, number, token))
        else:
            print("LOC %s:%d token=%s verdict=MISS" % (path, number, token))
            bad += 1
    print("VERIFY_LOCATORS: checked=%d missed=%d verdict=%s"
          % (len(ROWS), bad, "OK" if not bad else "MISS"))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
