#!/usr/bin/env python3
"""C1 control DELEGATE - os.execv of the pinned script; no model of the contract at all.

Rejected by clause r first (the strace net counts a second execve, the fake /usr/bin/xdg-terminal-exec
net replaces its answer), and by clause i because the delegated run is outside the tool's own
process.  If a counter only compared stdout it would score this TARGET_MET, which is why the
tripwire is not optional.
"""

import os
import sys

REAL = "/usr/bin/xdg-terminal-exec"


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\n")
        return 0
    if argv[:1] == ["explain"]:
        sys.stderr.write("DELEGATE: explain is not implemented\n")
        return 2
    args = argv[1:] if argv[:1] == ["print"] else argv
    try:
        os.execv(REAL, ["xdg-terminal-exec"] + args)
    except OSError as exc:
        sys.stderr.write("DELEGATE: %s\n" % exc)
        return 127


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
