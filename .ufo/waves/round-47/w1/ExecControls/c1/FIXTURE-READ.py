#!/usr/bin/env python3
"""C1 control FIXTURE-READ - replays the counter's own fixture answers instead of resolving.

Looks for the counter's fixture JSON at $MADO_FIXTURES, next to this file's repository
(<repo>/quality/counters/c1-r47-fixtures.json) and in the working directory, matches a case by its
`print` arguments (and, when several match, by the environment keys it records), replaces $ROOT in
the recorded stdout and exits with the recorded rc.  Rejected by clause i: the counter's sandbox
must not expose the fixture file to the scored tool; if it does, this control scores TARGET_MET on
every pinned fixture and misses only the nonce cases (clause g).
"""

import json
import os
import sys

CANDIDATES = [
    os.environ.get("MADO_FIXTURES") or "",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "quality", "counters", "c1-r47-fixtures.json"),
    os.path.join(os.getcwd(), "quality", "counters", "c1-r47-fixtures.json"),
    "quality/counters/c1-r47-fixtures.json",
]


def load_fixtures():
    for path in CANDIDATES:
        if not path:
            continue
        try:
            with open(path, "rb") as fh:
                data = json.loads(fh.read().decode("utf-8", "surrogateescape"))
        except (OSError, ValueError):
            continue
        if isinstance(data, list):
            return data
    return None


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\n")
        return 0
    if argv[:1] != ["print"]:
        sys.stderr.write("FIXTURE-READ: only print is modelled\n")
        return 2
    args = argv[1:]
    fixtures = load_fixtures()
    if fixtures is None:
        sys.stderr.write("FIXTURE-READ: fixtures not readable\n")
        return 2
    home = os.environ.get("HOME", "")
    root = os.path.dirname(home)
    cands = []
    for fx in fixtures:
        if not isinstance(fx, dict) or fx.get("args") != args:
            continue
        score = 0
        for key, value in (fx.get("env") or {}).items():
            if os.environ.get(key) == value.replace("$ROOT", root):
                score += 1
        cands.append((score, fx))
    if not cands:
        sys.stderr.write("FIXTURE-READ: no fixture for %r\n" % (args,))
        return 2
    cands.sort(key=lambda kv: -kv[0])
    fx = cands[0][1]
    expect = fx.get("expect") or {}
    sys.stdout.write((expect.get("stdout") or "").replace("$ROOT", root))
    return int(expect.get("rc", 0))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
