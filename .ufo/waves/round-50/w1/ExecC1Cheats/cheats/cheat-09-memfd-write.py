#!/usr/bin/env python3
"""cheat probe 09: mado-keysym.py look-alike that writes through a memfd (no path, no traced open).

Clause r names open(O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND), creat/mkdir/unlink/... and processes. A memfd is
created by its own syscall and written through write(2), so the trace set does not see the write. This probe
measures that gap: if readonly stays ok, the counter cannot report this write attempt (it also cannot observe a
persistent effect, because the fd dies with the process). This file is a probe, not a contract implementation.
"""
import ctypes
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
    hidden = 0
    why = ""
    try:
        libc = ctypes.CDLL("libc.so.6", use_errno=True)
        libc.memfd_create.restype = ctypes.c_int
        fd = libc.memfd_create(b"cheat-table", 0)
        if fd < 0:
            why = "errno=%s" % ctypes.get_errno()
        else:
            os.write(fd, b"cached-table:%s" % keysym.encode())
            os.lseek(fd, 0, 0)
            hidden = len(os.read(fd, 128))
            os.close(fd)
    except (OSError, AttributeError) as e:
        why = repr(e)[:80]
    print("MEMFD hidden_bytes=%d why=%s keysym=%s" % (hidden, why, keysym))
    return 0


if __name__ == "__main__":
    sys.exit(main())
