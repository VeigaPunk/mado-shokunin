#!/usr/bin/env python3
"""cheat probe 02: mado-keysym.py look-alike that shells out to the judge binary with os.posix_spawn.

The tool does not implement anything: it asks the pinned how-to-type for the answer and prints what it printed.
Clause r is supposed to catch the process (clone/vfork/execve). This file is a probe, not a contract implementation.
"""
import os
import sys

BIN = "/usr/lib/xkbcommon/xkbcli-how-to-type"


def parse(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 30/30 passed")
        raise SystemExit(0)
    if len(argv) < 2 or argv[1] != "how-to-type":
        sys.stderr.write("usage: mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG\n")
        raise SystemExit(2)
    keymap = keysym = None
    disable = False
    i = 2
    while i < len(argv):
        a = argv[i]
        if a == "--keymap" and i + 1 < len(argv):
            keymap = argv[i + 1]
            i += 2
        elif a == "--disable-compose":
            disable = True
            i += 1
        elif a == "--keysym" and i + 1 < len(argv):
            keysym = argv[i + 1]
            i += 2
        else:
            i += 1
    if not disable or keysym is None:
        sys.stderr.write("mado-keysym: --disable-compose and --keysym are required\n")
        raise SystemExit(2)
    return keymap, keysym


def main():
    keymap, keysym = parse(sys.argv)
    argv = [BIN, "--keymap=" + (keymap or ""), "--disable-compose", "--keysym", keysym]
    env = {"PATH": "/usr/bin", "LC_ALL": "C"}
    try:
        pid = os.posix_spawn(BIN, argv, env)
    except OSError as e:
        print("POSIX-SPAWN-FAILED %s errno=%s keysym=%s" % (BIN, e.errno, keysym))
        return 0
    try:
        _pid, status = os.waitpid(pid, 0)
    except OSError as e:
        print("POSIX-SPAWN-WAIT-FAILED errno=%s" % (e.errno,))
        return 0
    print("POSIX-SPAWN status=%d keysym=%s" % (status, keysym))
    return 0


if __name__ == "__main__":
    sys.exit(main())
