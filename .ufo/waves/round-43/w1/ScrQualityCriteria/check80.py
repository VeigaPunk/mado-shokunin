#!/usr/bin/env python3
"""check80.py - an excerpt header's line range is produced by the command that cut it.

The header of an excerpt names `lines <start>-<end>`.  Those two numbers are
checked against the body that follows the header and against the source file:
  body length == end - start + 1
  end <= number of lines in the source
  body bytes == source[start-1:end], verbatim

A header that cannot be true of its own body (a range past EOF, a body that is
one line longer than the range because of a trailing blank) is a defect of the
header, whichever command produced the file.

Exit 0 when the header, the body and the source agree, 1 otherwise, 2 on setup.

Usage: python3 -I check80.py --excerpt PATH --source PATH [--header-lines 2]
"""
import argparse
import re
import sys


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--excerpt", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--header-lines", type=int, default=2)
    a = ap.parse_args(argv)

    try:
        lines = open(a.excerpt, encoding="utf-8", errors="replace").read().splitlines()
        src = open(a.source, encoding="utf-8", errors="replace").read().splitlines()
    except OSError as e:
        print("SETUP_ERROR %s" % e)
        return 2

    head = "\n".join(lines[: a.header_lines])
    m = re.search(r"lines (\d+)-(\d+)", head)
    if not m:
        print("EXCERPT %s verdict=NO_RANGE header=%r" % (a.excerpt, head[:80]))
        return 1
    start, end = int(m.group(1)), int(m.group(2))
    body = lines[a.header_lines:]
    want_len = end - start + 1

    print("EXCERPT %s header=%d-%d body=%d expected=%d src=%d"
          % (a.excerpt, start, end, len(body), want_len, len(src)))

    bad = 0
    if len(body) != want_len:
        print("EXCERPT_MISMATCH length body=%d range=%d" % (len(body), want_len))
        bad += 1
    if end > len(src):
        print("EXCERPT_MISMATCH end=%d past_src=%d" % (end, len(src)))
        bad += 1
    if start < 1 or start > len(src):
        print("EXCERPT_MISMATCH start=%d src=%d" % (start, len(src)))
        bad += 1
    else:
        truth = src[start - 1: min(end, len(src))]
        if body != truth:
            diff = next((i for i, (x, y) in enumerate(zip(body, truth)) if x != y), min(len(body), len(truth)))
            print("EXCERPT_MISMATCH bytes first_diff_body_line=%d" % (diff + 1))
            bad += 1
    print("CHECK80: verdict=%s mismatches=%d" % ("FAIL" if bad else "OK", bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
