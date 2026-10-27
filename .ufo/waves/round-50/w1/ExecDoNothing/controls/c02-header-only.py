#!/usr/bin/env python3
"""control c02-header-only - CHEAT: the file is a header and nothing else.

The module carries its docstring, the contract restated, and an entry point that returns success. There is no keymap
read, no keysym table, no row list. It is the "I will write the tool later" shape a seat produces when it commits a
scaffold: a blob exists at the tool path, so a presence-only check passes, and the tool then answers nothing.

Stops at: clause f (stdout of the judge) and clause s (no `MADO_KEYSYM_SELFTEST: N/N passed` line).
"""
import sys


def main(argv):
    # The real tool would parse --keymap/--disable-compose/--keysym here and print the judge's report.
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
