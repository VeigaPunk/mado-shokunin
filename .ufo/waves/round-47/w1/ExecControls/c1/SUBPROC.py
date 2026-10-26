#!/usr/bin/env python3
"""C1 control SUBPROC - subprocess.run of the pinned script, stdout/rc copied through.

Rejected by clause r (two execve calls: the interpreter and the script; and the sandbox's fake
/usr/bin/xdg-terminal-exec answers instead of the script) - clause f can still look byte-equal
when the fake is absent, so r is the clause that has to carry this control.
"""

import subprocess
import sys

REAL = "/usr/bin/xdg-terminal-exec"


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\n")
        return 0
    if argv[:1] == ["explain"]:
        sys.stderr.write("SUBPROC: explain is not implemented\n")
        return 2
    args = argv[1:] if argv[:1] == ["print"] else argv
    try:
        proc = subprocess.run([REAL] + args, capture_output=True)
    except OSError as exc:
        sys.stderr.write("SUBPROC: %s\n" % exc)
        return 127
    sys.stdout.buffer.write(proc.stdout)
    sys.stdout.flush()
    sys.stderr.buffer.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
