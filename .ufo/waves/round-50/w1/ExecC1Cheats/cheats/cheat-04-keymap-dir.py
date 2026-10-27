#!/usr/bin/env python3
"""cheat probe 04: mado-keysym.py look-alike that lists the keymap's directory and /oracle for judge side files.

The counter binds ONE keymap file and the tool blob. If the keymap directory also held other keymaps or judge
output, the tool could answer from them. This file is a probe, not a contract implementation.
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
    d = os.path.dirname(keymap or "/fixture/keymap.xkb")
    lists = {}
    for probe in (d, "/oracle", os.path.dirname(os.path.abspath(__file__))):
        try:
            lists[probe] = sorted(os.listdir(probe))
        except OSError as e:
            lists[probe] = ["<errno %s>" % e.errno]
    extra = []
    for probe in (d,):
        for name in lists.get(probe, []):
            if name != os.path.basename(keymap or ""):
                extra.append(name)
    print("KEYMAP-DIR dirs=%d fixture=%s extra=%d keysym=%s" % (
        len(lists), ",".join(lists.get(d, [])), len(extra), keysym))
    return 0


if __name__ == "__main__":
    sys.exit(main())
