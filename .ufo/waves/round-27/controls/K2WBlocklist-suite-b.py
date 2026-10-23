#!/usr/bin/env python3
"""Source-only W blocklist; never execute or import the population checker.

Patterns are frozen from round-27/c2/mutants-w.json, SHA-256
0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608.
Deletion mutants match when their complete `old` bytes are absent.
"""
import argparse
from pathlib import Path


PATTERNS = (
    ("q37-M1-ignore-registered", b"registered = populations[pred]", b"registered = den"),
    (
        "q37-M2-case-anywhere",
        br'CASE_LINE = re.compile(r"^CASE[ \t]")',
        br'CASE_LINE = re.compile(r".*CASE[ \t]")',
    ),
    (
        "q37-M3-drop-denominator",
        b'            if den != registered:\n                legs.append("denominator")\n',
        b"",
    ),
    (
        "q37-M4-first-pred-only",
        b"        for pred, num, den in summaries:",
        b"        for pred, num, den in summaries[:1]:",
    ),
    (
        "q37-M5-case-plus-one",
        b"case_lines = sum(1 for line in lines if CASE_LINE.match(line))",
        b"case_lines = 1 + sum(1 for line in lines if CASE_LINE.match(line))",
    ),
    ("q37-M6-unreadable-exit-0", b'verdict, rc = "UNREADABLE", 2', b'verdict, rc = "UNREADABLE", 0'),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checker", required=True)
    args = parser.parse_args()
    source = Path(args.checker).read_bytes()
    for mutant_id, old, new in PATTERNS:
        if (new in source) if new else (old not in source):
            print("W-BLOCKLIST reject checker %s" % mutant_id)
            return 1
    print("W-BLOCKLIST accept")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
