#!/usr/bin/env python3
"""Check every quote in the seat report: it must sit on the cited source line and appear in the report.

Locators were computed with grep -n over .ufo/waves/round-45/l1-draft/mado-monitors.py, never typed.
"""
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SOURCE = LANE + "/.ufo/waves/round-45/l1-draft/mado-monitors.py"
REPORT = LANE + "/.ufo/waves/round-45/w1/ExecIndepB.md"

# (tag, source line number, verbatim quote inside that line)
QUOTES = [
    ("Q1", 70, "the expected scale E is Hyprland's correction of S for the live `width` and"),
    ("Q2", 75, "`mirrorOf` is the decimal `id` of the dump output named M"),
    ("Q3", 46, "any other key adds one to `badrules` and the rule is not added"),
    ("Q4", 54, "SCALE or transform VALUE outside these forms makes the line `unsupported` (not modelled)."),
    ("Q5", 77, "A live value that is missing or of the wrong JSON type (integers for width, height, x, y, transform, id;"),
    ("Q6", 73, "none found means the scale is not compared."),
    ("Q7", 28, "stdin, `--monitors -`, is read at most 1048577 bytes"),
]


def main():
    with open(SOURCE, encoding="utf-8") as handle:
        source_lines = handle.read().split("\n")
    with open(REPORT, encoding="utf-8") as handle:
        report = handle.read()
    bad = 0
    for tag, number, quote in QUOTES:
        on_source = number <= len(source_lines) and quote in source_lines[number - 1]
        in_report = quote in report
        words = len(quote.split())
        state = "OK" if (on_source and in_report and words <= 25) else "FAIL"
        bad += state == "FAIL"
        print("%s %s %s:%d words=%d source=%s report=%s" % (
            state, tag, "l1-draft/mado-monitors.py", number, words,
            "yes" if on_source else "no", "yes" if in_report else "no"))
    print("QUOTES_CHECKED: %d/%d ok" % (len(QUOTES) - bad, len(QUOTES)))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
