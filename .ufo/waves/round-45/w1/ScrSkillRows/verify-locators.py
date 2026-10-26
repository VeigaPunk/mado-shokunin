#!/usr/bin/env python3
"""Re-check every locator in skill-rows.md Block D against the pinned sources.

Reads the draft, extracts each `pin:line` locator and the backticked tokens on that row, then asserts every token
occurs inside the cited line (or line range). Locators are therefore checked against computed file content, not
against the author's memory. Usage:
    python3 verify-locators.py            # from anywhere; paths are absolute
"""
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DRAFT = os.path.join(SEAT, "skill-rows.md")
FETCH = os.path.join(LANE, ".ufo/waves/round-45/fetch")
HOST = os.path.expanduser("~/.config/hypr/monitors.conf")

ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|(.*)\|\s*$")


def resolve(pin):
    if pin.startswith("~/"):
        return os.path.expanduser(pin)
    for base in (LANE, os.path.join(LANE, ".ufo/waves/round-45/l1-draft")):
        lane_path = os.path.join(base, pin)
        if os.path.isfile(lane_path):
            return lane_path
    return os.path.join(FETCH, pin)


def main():
    text = open(DRAFT, encoding="utf-8").read()
    start = text.index("## Block D")
    block = text[start:]
    rows, fails = [], 0
    for line in block.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        locator, cell = m.group(1).strip(), m.group(2)
        if ":" not in locator:
            continue
        pin, _, span = locator.rpartition(":")
        if "-" in span:
            lo, hi = span.split("-", 1)
        else:
            lo = hi = span
        tokens = re.findall(r"`([^`]+)`", cell)
        tokens = [t for t in tokens if t and not t.startswith("—")]
        path = resolve(pin)
        if not os.path.isfile(path):
            rows.append((locator, "FAIL missing file %s" % path))
            fails += 1
            continue
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
        try:
            lo_i, hi_i = int(lo), int(hi)
        except ValueError:
            rows.append((locator, "FAIL unparsable span"))
            fails += 1
            continue
        window = "\n".join(lines[lo_i - 1:hi_i])
        missing = [t for t in tokens if t not in window]
        if missing:
            rows.append((locator, "FAIL token(s) absent from %d-%d: %s" % (lo_i, hi_i, missing)))
            fails += 1
        else:
            rows.append((locator, "PASS %d token(s) in %d-%d" % (len(tokens), lo_i, hi_i)))
    for locator, verdict in rows:
        print("LOCATOR: %-40s %s" % (locator, verdict))
    print("LOCATORS: checked=%d failed=%d" % (len(rows), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
