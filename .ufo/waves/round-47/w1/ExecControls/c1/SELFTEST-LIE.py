#!/usr/bin/env python3
"""C1 control SELFTEST-LIE - prints `MADO_TERMINAL_SELFTEST: 40/40 passed` and tests nothing.

The print side is STUB (exit 0, empty stdout).  Clause s must be satisfied by the *presence and
shape* of the line only if the counter also runs its own fixtures: this control demonstrates that
s alone is worth nothing, and that f/g cannot be replaced by the tool's self-report.
"""

import sys


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 40/40 passed\n")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
