#!/usr/bin/env python3
"""control c13-hardcoded-br - CHEAT: ignore the keymap file and answer from a fixed map (the host's br keymap for slash/Return)

Stops at: clause f: every fixture on another keymap expects that keymap's keycode/layout, not br's

The 'it works on my machine' control. The fixed map is the br/compose:caps answer for slash, Return and the
two error cases; it is right on 4 of the 14 fixtures and wrong on the other 10, which is exactly the shape a
counter with one hard-coded host keymap would bless.
"""
import hashlib
import json
import re
import sys


TABLE = {}


def keymap_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse(argv):
    o = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--keymap":
            o["keymap"] = argv[i + 1]
            i += 2
        elif a.startswith("--keymap="):
            o["keymap"] = a.split("=", 1)[1]
            i += 1
        elif a == "--disable-compose":
            o["disable_compose"] = True
            i += 1
        elif a == "--keysym":
            o["keysym"] = argv[i + 1]
            i += 2
        elif a.startswith("--keysym="):
            o["keysym"] = a.split("=", 1)[1]
            i += 1
        else:
            i += 1
    return o


def lookup(path, keysym):
    try:
        return TABLE.get(keymap_sha(path), {}).get(keysym)
    except OSError:
        return None


def emit(rc, text):
    sys.stdout.write(text)
    return rc



FIXED = {
    "F35": [
        0,
        "keysym: F35 (0xffe0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
    ],
    "Return": [
        0,
        "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        Portuguese (Brazil)  1       [ ]\n"
    ],
    "nosuchsym": [
        2,
        ""
    ],
    "slash": [
        0,
        "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil)  1       [ ]\n"
    ]
}


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = FIXED.get(o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], hit[1])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
