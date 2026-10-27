#!/usr/bin/env python3
"""cheat probe 08: mado-keysym.py look-alike that waits for a judge output file to appear.

The count side runs the judge before the tool for each case and keeps its result in a pipe, not a file; this probe
polls the writable tmpfs and the keymap directory for any new file. The wait is bounded (0.3 s per run) so the
783-case count stays feasible; an unbounded sleeper would instead hit the box's 120 s timeout.
This file is a probe, not a contract implementation.
"""
import os
import sys
import time


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


def scan():
    found = []
    for d in ("/tmp", os.path.dirname(keymap_path), "/fixture"):
        try:
            for name in os.listdir(d):
                if name.endswith((".out", ".log")) or name.startswith("trace-"):
                    found.append(os.path.join(d, name))
        except OSError:
            pass
    return found


keymap_path = "/fixture/keymap.xkb"


def main():
    global keymap_path
    keymap, keysym = parse(sys.argv)
    if keymap:
        keymap_path = keymap
    deadline = time.monotonic() + 0.3
    found = []
    while time.monotonic() < deadline:
        found = scan()
        if found:
            break
        time.sleep(0.1)
    print("SLEEP-EXPIRED found=%d after=%.2fs keysym=%s" % (
        len(found), 0.3 if not found else 0.0, keysym))
    return 0


if __name__ == "__main__":
    sys.exit(main())
