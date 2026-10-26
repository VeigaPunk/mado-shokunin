#!/usr/bin/env python3
"""Verify every source quote in the seat report (seat ExecIndepC, round 43).

Every line of the report shaped

    > "QUOTE" — c1-r42-geometry.py:A[-B]

must (1) be a blockquote, (2) hold a quote of at most 25 words, and (3) be a
literal substring of lines A..B of the frozen counter's docstring once
whitespace is collapsed. One line per quote, then a tally; exit 1 on any
failure. Run from the lane root:

    python3 .ufo/waves/round-43/w1/ExecIndepC/quote-check.py \
        .ufo/waves/round-43/w1/ExecIndepC.md quality/counters/c1-r42-geometry.py
"""
import re
import sys

LINE = re.compile(r'^> "(?P<quote>[^"]+)" — c1-r42-geometry\.py:(?P<first>\d+)'
                  r'(?:-(?P<last>\d+))?$')
MAX_WORDS = 25


def collapse(text):
    return " ".join(text.split())


def main():
    report = open(sys.argv[1]).read().splitlines()
    source = open(sys.argv[2]).read().splitlines()
    checked = 0
    bad = 0
    for number, line in enumerate(report, 1):
        found = LINE.match(line)
        if found is None:
            if line.startswith('> "') and "c1-r42-geometry.py:" in line:
                print("report:%d UNPARSED %s" % (number, line[:80]))
                bad += 1
            continue
        quote = collapse(found.group("quote"))
        first = int(found.group("first"))
        last = int(found.group("last") or found.group("first"))
        words = len(quote.split())
        joined = collapse(" ".join(source[first - 1:last]))
        present = quote in joined
        ok = present and words <= MAX_WORDS and last >= first
        checked += 1
        if not ok:
            bad += 1
        print("report:%d source:%d-%d words=%d present=%d %s"
              % (number, first, last, words, present,
                 "ok" if ok else "FAIL"))
    print("QUOTES checked=%d failed=%d" % (checked, bad))
    return 0 if bad == 0 and checked > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
