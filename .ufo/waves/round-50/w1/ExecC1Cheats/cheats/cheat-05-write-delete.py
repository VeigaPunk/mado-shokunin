#!/usr/bin/env python3
"""cheat probe 05: mado-keysym.py look-alike that writes a cache file and deletes it again during a scored run.

If writes were invisible to the count side, the tool could memoise answers (or tamper). Clause r is supposed to see
the attempt even when the mount is read-only. This file is a probe, not a contract implementation.
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
    # 1) a writable tmpfs: write, read back, delete.
    wrote = False
    try:
        fd = os.open("/tmp/cheat-cache.bin", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        os.write(fd, b"cached-answer")
        os.close(fd)
        wrote = True
        os.unlink("/tmp/cheat-cache.bin")
    except OSError:
        pass
    # 2) beside the keymap (read-only bind): the attempt still counts.
    ro = None
    try:
        fd = os.open(os.path.join(os.path.dirname(keymap or "/fixture/keymap.xkb"), "cheat-cache.bin"),
                     os.O_WRONLY | os.O_CREAT, 0o600)
        os.close(fd)
        ro = "wrote"
    except OSError as e:
        ro = "refused:%s" % e.errno
    print("WRITE-THEN-DELETE tmp=%s fixture=%s keysym=%s" % (wrote, ro, keysym))
    return 0


if __name__ == "__main__":
    sys.exit(main())
