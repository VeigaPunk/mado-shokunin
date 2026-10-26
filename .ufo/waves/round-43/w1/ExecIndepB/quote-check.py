#!/usr/bin/env python3
"""Verify every contract quote used in ExecIndepB.md sits on the cited line."""
import sys

COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r42-geometry.py"
REPORT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecIndepB.md"

QUOTES = [
    (29, "The effect is the first"),
    (30, "first token of field 0, tokens being separated by runs of spaces and tabs only"),
    (39, "its class holds no character below U+0020 and `re.fullmatch(REGEX, class)` succeeds."),
    (21, "standard input, at most 1048577 bytes"),
    (20, "an input larger than 1048576 bytes is too_large"),
    (19, "a FIFO or any non-regular file is unreadable"),
    (72, "function whose body contains the text `MADO_GEOMETRY: rules=` (which must have a site)"),
    (87, "a tool that CONTAINS a model of this contract is an implementation"),
    (37, "Supported rules are numbered n=1.. across all"),
    (38, "files in argument order; each carries the 1-based index of its file."),
    (54, "WxH are decimal integers without leading zeros"),
    (55, "V = NO_SIZE_RULES (rules=0; exit 4)"),
    (45, "the last matching `size` rule gives want"),
    (32, "field 0 has exactly two argument tokens fully matching"),
    (43, "size is the `size` value when a list of exactly two JSON"),
    (47, "BADSIZE (size none) | TILED (not floating)"),
]


def main():
    lines = open(COUNTER, encoding="utf-8").read().split("\n")
    report = " ".join(open(REPORT, encoding="utf-8").read().split())
    failures = 0
    for number, quote in QUOTES:
        inline = quote in lines[number - 1]
        inreport = " ".join(quote.split()) in report
        words = len(quote.split())
        state = "PASS" if inline and inreport and words <= 25 else "FAIL"
        if state == "FAIL":
            failures += 1
        print("%s counter:%d words=%d line=%s report=%s %r"
              % (state, number, words, int(inline), int(inreport), quote))
    print("QUOTE_CHECK: quotes=%d failures=%d" % (len(QUOTES), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
