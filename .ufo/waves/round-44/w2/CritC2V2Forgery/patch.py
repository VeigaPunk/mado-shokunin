#!/usr/bin/env python3
"""Regenerate the two patched counter copies in this seat from the frozen counter.

P1 width cap  : clause j (surfaces_ok) rejects a locator whose range is wider than 40 lines.
P2 census     : clause h rejects a `default_size=WxH` or `size_request_calls=N` on any other line
                that disagrees with the census.
P3 both       : P1 + P2.

The frozen counter is only read; the copies live in this seat directory.
"""
import os
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SRC = os.path.join(LANE, "quality/counters/c2-r44-gkeep-size-request-v2.py")

WIDTH_OLD = "                if int(a) <= L <= int(b or a):"
WIDTH_NEW = ("                if int(a) <= L <= int(b or a) "
             "and int(b or a) - int(a) <= 40:")
H_OLD = """                for v in re.findall(r"x11_configure=(\\d+)", l):
                    if int(v) != Y0:
                        h_ok = False
                        print("%s %s clause=h prose x11_configure=%s != %d" % (PRED, name, v, Y0))
"""
H_NEW = H_OLD + """                for w, h in re.findall(r"(?<!set_)default_size=(\\d+)x(\\d+)", l):
                    if (w, h) != (W0, H0):
                        h_ok = False
                        print("%s %s clause=h prose default_size=%sx%s != %sx%s" % (PRED, name, w, h, W0, H0))
                for v in re.findall(r"size_request_calls=(\\d+)", l):
                    if int(v) != N0:
                        h_ok = False
                        print("%s %s clause=h prose size_request_calls=%s != %d" % (PRED, name, v, N0))
"""


def main():
    with open(SRC, encoding="utf-8") as fh:
        src = fh.read()
    width = src.replace(WIDTH_OLD, WIDTH_NEW)
    hfix = src.replace(H_OLD, H_NEW)
    both = width.replace(H_OLD, H_NEW)
    for name, text, marker, expect in (
            ("c2-r44-v2-widthcap.py", width, WIDTH_NEW, 1),
            ("c2-r44-v2-censusforms.py", hfix, H_NEW, 1),
            ("c2-r44-v2-widthcap-censusforms.py", both, WIDTH_NEW, 1)):
        ok = text.count(marker) == expect and text != src
        with open(os.path.join(SEAT, name), "w", encoding="utf-8") as fh:
            fh.write(text)
        print("%-34s %s" % (name, "PASS" if ok else "FAIL"))
        if not ok:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
