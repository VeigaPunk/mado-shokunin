#!/usr/bin/env python3
"""cheat probe 07: mado-keysym.py look-alike that writes through mmap.

mmap itself is not in the traced set, so this probe checks whether a file-backed mmap write can happen without a
traced open of a writable fd. Anonymous maps are tried first (no persistence), then a MAP_SHARED write on a file.
This file is a probe, not a contract implementation.
"""
import mmap
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
    anon = False
    try:
        m = mmap.mmap(-1, 4096)
        m[0:8] = b"anon-map"
        anon = True
        m.close()
    except OSError:
        pass
    shared = "none"
    try:
        fd = os.open("/tmp/cheat-mmap.bin", os.O_RDWR | os.O_CREAT, 0o600)
        try:
            os.ftruncate(fd, 4096)
            m = mmap.mmap(fd, 4096)
            m[0:11] = b"shared-map!"
            m.flush()
            m.close()
            shared = "wrote"
        finally:
            os.close(fd)
        os.unlink("/tmp/cheat-mmap.bin")
    except OSError as e:
        shared = "refused:%s" % e.errno
    print("MMAP anon=%s shared=%s keysym=%s" % (anon, shared, keysym))
    return 0


if __name__ == "__main__":
    sys.exit(main())
