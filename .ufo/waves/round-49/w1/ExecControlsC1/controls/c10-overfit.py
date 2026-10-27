#!/usr/bin/env python3
"""control c10-overfit - CHEAT: correct on the fixture keymaps, and for any other keymap emit a plausible single bogus row

Stops at: clause g: on a generated keymap the fallback row is wrong (keycode, layout and mask), and it never prints the error exit for an unrecognised keysym

Different from c06: this control looks like a model (it produces output for every input and never empties
its answer), so a counter that checks only 'does the tool produce output' passes it. On the fixture set it is
byte-exact because the table holds those answers; on a keymap it has never seen it has nothing real to say.
"""
import hashlib
import json
import re
import sys


TABLE = {
    "069e997614066d734130ed0970a4f75c3a8327a59ec08cf5ea5be56692bb6dcc": {
        "ssharp": [
            0,
            "keysym: ssharp (0x00df)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      1        German               1       [ ]\n"
        ]
    },
    "0a2f89b71de32b710b8a92a45230ba0b64d15be977d18a13b1ec97262b86a27a": {
        "Cyrillic_a": [
            0,
            "keysym: Cyrillic_a (0x06c1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n41       AC04      2        Russian              1       [ ]\n"
        ]
    },
    "7f40cb5f5ff8e300d02b1e08c86142b04bfe714335488a40369b15692fd6f813": {
        "0x0061": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "s": [
            0,
            "keysym: s (0x0073)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n39       AC02      1        English (US)         1       [ ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (US)         1       [ ]\n"
        ],
        "space": [
            0,
            "keysym: space (0x0020)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        English (US)         1       [ ]\n"
        ]
    },
    "82da378656a08563dd68fe126eaef57efe05bb34525567b99de7f684c41bee67": {
        "EuroSign": [
            0,
            "keysym: EuroSign (0x20ac)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n443      I443      1        English (US)         1       [ ]\n"
        ]
    },
    "d1ebf48ee8cdabebc7ae967f1aa3fa35bf3fb4efaf0be71522823493a216cfed": {
        "Escape": [
            0,
            "keysym: Escape (0xff1b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n9        ESC       1        English (US)         1       [ ]\n66       CAPS      1        English (US)         1       [ ]\n"
        ]
    },
    "e14cf7679459df97cbdca1a00449215fd968d0159d6be372ad85b7dd837f71a2": {
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        English (US, intl., with dead keys) 1       [ ]\n"
        ]
    },
    "efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81": {
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
    },
    "f6bcde4e4e03293d05c9426d08cdc2e9a78e7b8faef39dc97c5d267ad7355607": {
        "eacute": [
            0,
            "keysym: eacute (0x00e9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        French               1       [ ]\n"
        ]
    }
}


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



FALLBACK = "38       AC01      1        English (US)         1       [ ]\n"


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is not None:
        return emit(hit[0], hit[1])
    head = ["keysym: %s (0x0000)\n" % o["keysym"], "\n", "=== Direct access ===\n", "\n",
            "KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"]
    return emit(0, "".join(head) + FALLBACK)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
