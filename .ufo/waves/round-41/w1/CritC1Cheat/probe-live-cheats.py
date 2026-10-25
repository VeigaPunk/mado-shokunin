#!/usr/bin/env python3
"""Probe receipts for the two live-mode cheats (no counter, no sandbox).

P1  ch1-stub-oracle.read_live returns the stub's payload without executing it:
    the stub touches a marker file if it is ever run; the marker must not exist.
P2  ch2-cwd-replay.read_live returns <cwd>/journal.txt, not what the program
    would print: the program would exit 9 and print a different journal.
Both tools are loaded as modules (their __main__ guard keeps main() off).
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    path = os.path.join(HERE, name)
    g = {"__name__": "probe_" + name.replace("-", "_"), "__file__": path}
    exec(compile(open(path).read(), path, "exec"), g)
    return g


def main():
    tmp = tempfile.mkdtemp(prefix="probe-c1cheat-")
    try:
        # ---- P1: stub oracle never executes the program
        p1 = os.path.join(tmp, "p1")
        os.makedirs(p1)
        marker = os.path.join(p1, "ran")
        payload = b"2026-10-25T13:36:24-03:00 h xdg-desktop-portal-hyprland[77]: [LOG]  | Got interface: wl_seat (ver 9)\n"
        import base64
        stub = os.path.join(p1, "journalctl")
        with open(stub, "w") as fh:
            fh.write("#!/bin/sh\n"
                     '[ "$*" = "--user -u xdg-desktop-portal-hyprland --no-pager -o short-iso" ] || exit 9\n'
                     "touch %s\n"
                     "printf '%%s' '%s' | base64 -d\n"
                     % (marker, base64.b64encode(payload).decode()))
        os.chmod(stub, 0o755)
        g1 = load("ch1-stub-oracle.py")
        got = g1["read_live"](stub)
        print("P1 read_live_returned_payload=%d marker_created=%d equal=%d"
              % (len(got), os.path.exists(marker), got == payload))

        # ---- P2: cwd replay beats the program
        p2 = os.path.join(tmp, "p2")
        os.makedirs(p2)
        other = b"2026-10-25T00:00:00-03:00 h xdg-desktop-portal-hyprland[1]: [LOG]  | Got interface: wl_shm (ver 1)\n"
        with open(os.path.join(p2, "journal.txt"), "wb") as fh:
            fh.write(other)
        prog = os.path.join(p2, "journalctl")
        with open(prog, "w") as fh:
            fh.write("#!/bin/sh\nprintf 'WRONG'\nexit 9\n")
        os.chmod(prog, 0o755)
        g2 = load("ch2-cwd-replay.py")
        cwd = os.getcwd()
        os.chdir(p2)
        try:
            got2 = g2["read_live"](prog)
        finally:
            os.chdir(cwd)
        print("P2 read_live_returned_cwd_file=%d from_program=%d"
              % (got2 == other, got2 == b"WRONG"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
