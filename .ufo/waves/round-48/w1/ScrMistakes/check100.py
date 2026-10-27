#!/usr/bin/env python3
"""check100 - a wave's scratch bound is enforced by the dispatch, not stated in prose.

QUALITY criterion 100 (draft, round 48). The wave context of round 47 carried one sentence about
scratch ("keep it under 2 GB") and a seat's shell still streamed ~590 GB into a FIFO-named scratch
path before it was cancelled (lesson M47-7, captured-by: none). A prose ceiling is not a bound:
nothing in the seat's shell reads it. The dispatch must carry a limit the seat's shell executes
(`ulimit -f <KB>`, an `RLIMIT_FSIZE` setter, or a named `max_file_bytes=`/`--size-cap` value), and
a GB/MB sentence without such a command is a violation.

Usage:
  check100.py --spec <wave spec or dispatch json> [--context <text file>] [--extra <text file> ...]
Exit 0 = an enforced cap is present, 1 = prose only or absent, 2 = input unreadable.
"""
import argparse
import json
import re
import sys

ENFORCED = [
    re.compile(r"ulimit\s+-f\s+(\d+)"),
    re.compile(r"RLIMIT_FSIZE"),
    re.compile(r"max[_-]?file[_-]?bytes\s*[:=]\s*(\d+)"),
    re.compile(r"--size-cap[= ](\d+)"),
]
PROSE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:GB|MB|MiB|GiB)\b")


def load(path):
    try:
        raw = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        print("UNREADABLE %s (%s)" % (path, exc))
        return None
    try:
        return json.dumps(json.loads(raw))
    except ValueError:
        return raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--context", action="append", default=[])
    a = ap.parse_args()

    blobs = []
    spec = load(a.spec)
    if spec is None:
        return 2
    blobs.append((a.spec, spec))
    for c in a.context:
        t = load(c)
        if t is None:
            return 2
        blobs.append((c, t))

    enforced = 0
    for name, text in blobs:
        for rx in ENFORCED:
            for m in rx.finditer(text):
                enforced += 1
                print("ENFORCED %s %s" % (name, m.group(0)))
    prose = []
    for name, text in blobs:
        for m in PROSE.finditer(text):
            prose.append((name, m.group(0)))
    for name, tok in prose:
        print("PROSE %s ceiling=%s" % (name, tok))

    verdict = "OK" if enforced else ("PROSE-ONLY" if prose else "ABSENT")
    print("CHECK100: sources=%d enforced=%d prose=%d verdict=%s"
          % (len(blobs), enforced, len(prose), verdict))
    return 0 if enforced else 1


if __name__ == "__main__":
    sys.exit(main())
