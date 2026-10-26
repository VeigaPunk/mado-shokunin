#!/usr/bin/env python3
"""C1 control STUB - the do-nothing candidate: exit 0, print nothing, test nothing.

Usage: mado-terminal.py print [...] | explain | --selftest  (all silent)

Every clause of the C1 counter must reject this: clause s finds no
`MADO_TERMINAL_SELFTEST: N/N passed` line, clauses f and g compare empty stdout with the pinned
script's output on every fixture and nonce case (rc 0 is only right where the script exits 0).
"""

import sys


def main(argv):
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
