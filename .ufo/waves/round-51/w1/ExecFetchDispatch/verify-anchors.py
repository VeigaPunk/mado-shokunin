#!/usr/bin/env python3
"""Verify a pin-anchor table against the fetched pin files (mado round 51).

Each anchors line is `<pin-file>:<line>\t<quote>`; the quote must be a verbatim
substring of that exact line of that pin, and at most MAX_WORDS words. This is the
check a C2 `held:`/row quote needs: the cited line must contain the quote.

Usage:
  verify-anchors.py --pins <pin-dir> [--anchors <file>] [--scratch <dir>] [--selftest]

  --pins      directory holding the pin files (e.g. .../ExecFetchDispatch/fetch)
  --anchors   anchor table (default: anchors.txt next to this script)
  --scratch   writable scratch dir for --selftest fixtures (default: mktemp -d under
              $TMPDIR, else /tmp); only used by --selftest
  --selftest  run hermetic positive/negative cases in a private fixture tree, then
              exit non-zero if the checker does not separate them

Exit: 0 all anchors verify; 1 any anchor fails; 2 usage/IO error; 3 selftest failure.
"""
import argparse
import os
import shutil
import sys
import tempfile

MAX_WORDS = 25


def check_anchor(pins, filename, lineno, quote):
    """Return None on success, or a failure string."""
    path = os.path.join(pins, filename)
    if not os.path.isfile(path):
        return f"pin file absent: {filename}"
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    if lineno < 1 or lineno > len(lines):
        return f"{filename}:{lineno} out of range (file has {len(lines)} lines)"
    if quote not in lines[lineno - 1]:
        return f"{filename}:{lineno} quote not verbatim on that line"
    words = quote.split()
    if len(words) > MAX_WORDS:
        return f"{filename}:{lineno} quote has {len(words)} words > {MAX_WORDS}"
    return None


def parse_table(path):
    rows = []
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" not in line or ":" not in line.split("\t")[0]:
            print(f"verify-anchors.py: malformed row in {path}: {line[:80]}", file=sys.stderr)
            sys.exit(2)
        loc, quote = line.split("\t", 1)
        filename, lineno = loc.rsplit(":", 1)
        rows.append((filename, int(lineno), quote))
    return rows


def selftest(scratch):
    root = tempfile.mkdtemp(prefix="anchors-", dir=scratch)
    try:
        os.makedirs(os.path.join(root, "pins"))
        with open(os.path.join(root, "pins", "Pin.cpp"), "w", encoding="utf-8") as fh:
            fh.write("line one\nm_dispatchers.find(handler);\n" + " ".join(f"tok{i}" for i in range(MAX_WORDS + 5)) + "\n")
        pins = os.path.join(root, "pins")
        long_quote = " ".join(f"tok{i}" for i in range(MAX_WORDS + 5))
        cases = [
            ("positive", check_anchor(pins, "Pin.cpp", 2, "m_dispatchers.find(handler);"), True),
            ("wrong-quote", check_anchor(pins, "Pin.cpp", 2, "m_dispMap.find(handler);"), False),
            ("wrong-line", check_anchor(pins, "Pin.cpp", 1, "m_dispatchers.find(handler);"), False),
            ("out-of-range", check_anchor(pins, "Pin.cpp", 9, "line one"), False),
            ("missing-pin", check_anchor(pins, "Nope.cpp", 1, "line one"), False),
            ("too-long", check_anchor(pins, "Pin.cpp", 3, long_quote), False),
        ]
        red = 0
        for name, result, should_pass in cases:
            ok = (result is None) == should_pass
            print(f"selftest {name:<12} {'ok' if ok else 'WRONG'}"
                  f"{'' if result is None else ' (' + result + ')'}")
            if not ok:
                red += 1
        print(f"selftest: cases={len(cases)} wrong={red}")
        return red == 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--pins", required=False)
    ap.add_argument("--anchors", default=os.path.join(here, "anchors.txt"))
    ap.add_argument("--scratch", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        scratch = args.scratch or tempfile.mkdtemp(prefix="anchors-selftest-")
        os.makedirs(scratch, exist_ok=True)
        ok = selftest(scratch)
        sys.exit(0 if ok else 3)

    if not args.pins:
        print("verify-anchors.py: --pins is required", file=sys.stderr)
        sys.exit(2)
    if not os.path.isdir(args.pins):
        print(f"verify-anchors.py: no such pins dir: {args.pins}", file=sys.stderr)
        sys.exit(2)
    if not os.path.isfile(args.anchors):
        print(f"verify-anchors.py: no such anchors file: {args.anchors}", file=sys.stderr)
        sys.exit(2)

    rows = parse_table(args.anchors)
    fails = 0
    files = set()
    for filename, lineno, quote in rows:
        files.add(filename)
        bad = check_anchor(args.pins, filename, lineno, quote)
        if bad:
            fails += 1
            print(f"FAIL {bad}")
    print(f"anchors={len(rows)} pin_files={len(files)} failed={fails}")
    sys.exit(0 if fails == 0 else 1)


if __name__ == "__main__":
    main()
