#!/usr/bin/env python3
"""Verify every quote CritC1Capability lifts is present in the receipts at this seat.

Each entry is (receipt file below receipts/, source locator, quote). The quote must appear
verbatim (whitespace collapsed) in that receipt. Exit 0 = all found.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "receipts")

QUOTES = [
    ("PROVINCE-data.md", "PROVINCE.md:32 (tool row)", "`--selftest` opens no file and writes nothing"),
    ("PROVINCE-data.md", "PROVINCE.md:32 (tool row)",
     "`--clients`, a regular file or `-` for standard input, at most 1048577 B"),
    ("PROVINCE-data.md", "PROVINCE.md:32 (tool row)", "no compositor socket, no Wayland client, no network, no config tree, no process started"),
    ("SKILL-data.md", "SKILL.md:249-251 (subsection)", "reads no config tree of its own"),
    ("SKILL-data.md", "SKILL.md:252 (subsection)", "`MADO_GEOM_RULE:` line per supported rule"),
    ("SKILL-data.md", "SKILL.md:256 (TILED licence row)",
     "the matched client is not floating, so the first-map floating branch that reads `static_.size` never ran for it"),
    ("SKILL-data.md", "SKILL.md:273 (NO_SIZE_RULES licence row)", "the rules files carry no supported `size` line"),
    ("battery.txt", "tool docstring, run output", "MADO_GEOMETRY: SETUP too_large"),
    ("battery.txt", "tool docstring, run output", "MADO_GEOMETRY: SETUP unreadable"),
    ("battery.txt", "tool docstring, selftest", "MADO_GEOMETRY_SELFTEST: 73/73 passed"),
    ("coverage.txt", "host run, 40 closure files",
     "rules=3 float_rules=6 other=61 unsupported=7 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT"),
    ("coverage.txt", "host run, hyprland.conf alone", "rules=0 float_rules=0 other=0 unsupported=0"),
    ("strace.txt", "selftest trace", 'openat(AT_FDCWD, "/dev/null", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3'),
    ("strace.txt", "selftest trace", 'openat(AT_FDCWD, "/", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3'),
    ("honesty-grep.txt", "SKILL.md grep", 'grep -c "match:tag" SKILL-data.md ; grep -c "match:title" SKILL-data.md ; grep -c "windowrulev2" SKILL-data.md'),
]


def norm(s):
    return re.sub(r"\s+", " ", s)


def main():
    bad = 0
    for fname, loc, quote in QUOTES:
        path = os.path.join(R, fname)
        try:
            text = norm(open(path, encoding="utf-8", errors="replace").read())
        except OSError:
            print("FAIL missing-receipt %s (%s)" % (fname, loc))
            bad += 1
            continue
        ok = norm(quote) in text
        print("%s %-20s %-45s %s" % ("PASS" if ok else "FAIL", fname, loc, quote[:58]))
        bad += 0 if ok else 1
    print("QUOTES: %d/%d found" % (len(QUOTES) - bad, len(QUOTES)))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
