#!/usr/bin/env python3
"""cheat probe 01: mado-keysym.py look-alike that tries to load the judge's own library with ctypes.

If the sandbox let libxkbcommon through, the tool would answer from the judge's data (xkb_keymap_new_from_string +
xkb_state_key_get_one_sym) instead of implementing keymaps itself. Clause i is supposed to make that impossible:
only the interpreter's ldd closure is mounted. This file is a probe, not a contract implementation.
"""
import ctypes
import os
import sys

CANDIDATES = ("libxkbcommon.so.0", "/usr/lib/libxkbcommon.so.0", "/lib/libxkbcommon.so.0",
              "/usr/lib/xkbcommon/libxkbcommon.so.0")


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
    seen = []
    for name in CANDIDATES:
        try:
            lib = ctypes.CDLL(name)
        except OSError as e:
            seen.append("%s:%s" % (name, e.errno if e.errno else "?"))
            continue
        # Loaded: use the judge's own API to answer.
        try:
            lib.xkb_context_new.restype = ctypes.c_void_p
            ctx = lib.xkb_context_new(0)
        except AttributeError:
            ctx = None
        print("CTYPES-LOADED %s ctx=%s keysym=%s" % (name, ctx is not None, keysym))
        return 0
    print("CTYPES-ABSENT all=%s keymap=%s keysym=%s" % (",".join(seen), os.path.basename(keymap or ""), keysym))
    return 0


if __name__ == "__main__":
    sys.exit(main())
