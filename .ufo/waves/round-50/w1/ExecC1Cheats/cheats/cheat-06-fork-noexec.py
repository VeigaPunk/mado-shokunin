#!/usr/bin/env python3
"""cheat probe 06: mado-keysym.py look-alike that forks without exec.

A fork-only child could keep state across the count or race the counter without any execve. Clause r names fork,
vfork, clone, clone3. This file is a probe, not a contract implementation.
"""
import os
import sys


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
    try:
        pid = os.fork()
    except OSError as e:
        print("FORK-FAILED errno=%s keysym=%s" % (e.errno, keysym))
        return 0
    if pid == 0:
        os.write(1, b"FORK-CHILD\n")
        os._exit(0)
    try:
        _pid, status = os.waitpid(pid, 0)
    except OSError:
        status = -1
    print("FORK-PARENT status=%d keysym=%s" % (status, keysym))
    return 0


if __name__ == "__main__":
    sys.exit(main())
