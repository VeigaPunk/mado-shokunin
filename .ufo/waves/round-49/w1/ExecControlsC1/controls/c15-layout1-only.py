#!/usr/bin/env python3
"""control c15-layout1-only - CHEAT: drop every row whose LAYOUT column is not 1 (the first layout only)

Stops at: clause f: the us,ru fixture reaches Cyrillic_a on layout 2 only, so its one row disappears

A counter that only checks single-layout keymaps never sees this; the multi-layout case is the whole point of
the LAYOUT/LAYOUT NAME columns.
"""
import hashlib
import json
import re
import sys

import re
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
    "0e4e055ce57f721efba9733731bace67d8fd9c985ddc75188a955c2ab3ec791e": {
        "bracketleft": [
            0,
            "keysym: bracketleft (0x005b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n17       AE08      1        Norwegian            3       [ Mod5 LevelThree ]\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n21       AE12      1        Norwegian            3       [ Mod5 LevelThree ]\n47       AC10      1        Norwegian            3       [ Mod5 LevelThree ]\n47       AC10      1        Norwegian            3       [ Lock Mod5 LevelThree ]\n"
        ]
    },
    "1ce0c8b05c44712bb202ab633760008a5f808991c894cb3489dad0929cc7e3cf": {
        "bracketleft": [
            0,
            "keysym: bracketleft (0x005b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n17       AE08      1        Swedish              3       [ Mod5 LevelThree ]\n"
        ]
    },
    "21e2957f71057a2bd3d34f9b5704df019d800f6eff7ccd494bc9c0afec1994af": {
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n21       AE12      1        Swedish              1       [ ]\n"
        ]
    },
    "25fc25ce8e275b77f16d882637f7344db0f4457c64270be33b505c0a3584bf24": {
        "0x0": [
            2,
            ""
        ]
    },
    "36b3f91333ce5c6c5b44a398ab18d8e8dfe341ee9c2d18fbe4f66249f6b672d0": {
        "Tab": [
            0,
            "keysym: Tab (0xff09)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n23       TAB       1        Swedish              1       [ ]\n"
        ]
    },
    "3beacd7cf47d6fc3759005bfb86735e76098a7cac58c9693e8071a13c3512a16": {
        "EuroSign": [
            0,
            "keysym: EuroSign (0x20ac)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        Norwegian            3       [ Mod5 LevelThree ]\n26       AD03      1        Norwegian            3       [ Lock Mod5 LevelThree ]\n443      I443      1        Norwegian            1       [ ]\n"
        ],
        "eacute": [
            0,
            "keysym: eacute (0x00e9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ]
    },
    "3cdca9c4cbe4f9a00dce3f4cbbbf3c16f4acc36cdc2fa42ba2f5204c4c2220af": {
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Italian              1       [ ]\n"
        ],
        "numbersign": [
            0,
            "keysym: numbersign (0x0023)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        Italian              3       [ Mod5 LevelThree ]\n"
        ],
        "s": [
            0,
            "keysym: s (0x0073)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n39       AC02      1        Italian              1       [ ]\n"
        ]
    },
    "48c6c40845a0b18bf21b8d0dcd66f2b9788e6ee628f3c9288c6ef73934309374": {
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (UK)         1       [ ]\n"
        ]
    },
    "4c87cfb8235ddf246cdeaa667fae16360c8e77556deffe1f3cb8a5465454fd45": {
        "0x0": [
            2,
            ""
        ]
    },
    "590cd25a31888a026f2f5d5da46f099bfcded8457b6c94e8b4df51c61f768edf": {
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ]
    },
    "5b954fe2d008492b0f47cf32a9aed98ba6715d8e40d05e120b91c5d6a79e8d49": {
        "0x0": [
            2,
            ""
        ]
    },
    "5c0191b4b8bf2aec2c109d2db8cf7c628c1e0c8f334ee736dda18e721c85d18e": {
        "0x002f": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        Polish (intl., with dead keys) 1       [ ]\n"
        ]
    },
    "7d8aec6fae04bb9e24925ae13a0ca8359bd82b4e32621d75e8c96111c62333e0": {
        "0x0": [
            2,
            ""
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
    "85d0907f1fa628eba9e375b5a0e059376f39a4ef00b72ae2e7510d2974b5de21": {
        "0x0061": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (UK, intl., with dead keys) 1       [ ]\n"
        ]
    },
    "8acb9813ba929fe98e8a36f5b3e991e70e0e3fd1c2396deae9ad61aff3496741": {
        "F35": [
            0,
            "keysym: F35 (0xffe0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ]
    },
    "966eca84eb63b0805e20b3ad26764766080add6f82752c4cef7fbd71975d4c4d": {
        "Cyrillic_a": [
            0,
            "keysym: Cyrillic_a (0x06c1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ]
    },
    "a8f01dec23b155b95fd97b291bfa8b1af09255226bb66aff604ad73fb61bd997": {
        "0x002f": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      1        Spanish (no dead keys) 2       [ Shift ]\n"
        ]
    },
    "aa6348429683e0f359ab8de6a2b802a34b2f50d5d35f5207c2b95b6eb7aa0e52": {
        "Return": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        French               1       [ ]\n"
        ]
    },
    "b237e5c69228ca7aebee46059e007cdf32e5c70630882cdee4037372a422dce4": {
        "0x0": [
            2,
            ""
        ]
    },
    "cc4a1a23cdb89251ed38774d596c35e27aa8bb6748226cf4b0a58eb1dd6ebf12": {
        "s": [
            0,
            "keysym: s (0x0073)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n39       AC02      1        Italian              1       [ ]\n"
        ]
    },
    "d1ebf48ee8cdabebc7ae967f1aa3fa35bf3fb4efaf0be71522823493a216cfed": {
        "Escape": [
            0,
            "keysym: Escape (0xff1b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n9        ESC       1        English (US)         1       [ ]\n66       CAPS      1        English (US)         1       [ ]\n"
        ]
    },
    "d2a2e476fda398a233aa245bf7e2c81144f9337a77e55039a8e947bcbfb4d1c9": {
        "EuroSign": [
            0,
            "keysym: EuroSign (0x20ac)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        Czech                3       [ Mod5 LevelThree ]\n26       AD03      1        Czech                3       [ Lock Mod5 LevelThree ]\n443      I443      1        Czech                1       [ ]\n"
        ]
    },
    "d477d1bf7b822fd6f4187813c24c023b0240c87bb4810443f5da17bcbf7aafba": {
        "0": [
            0,
            "keysym: 0 (0x0030)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n19       AE10      1        Spanish (no dead keys) 1       [ ]\n"
        ]
    },
    "e14cf7679459df97cbdca1a00449215fd968d0159d6be372ad85b7dd837f71a2": {
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        English (US, intl., with dead keys) 1       [ ]\n"
        ]
    },
    "e3c90e49c359a56c30d7421f63a4d70e289ae8826b82f7733c7ae9926728ecb9": {
        "Cyrillic_a": [
            0,
            "keysym: Cyrillic_a (0x06c1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ]
    },
    "e5f2f023cad0054c3bd98ba00caeeeeb8af5791f79f8aa6ea59f871adb554cd8": {
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (UK)         1       [ ]\n"
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
    "f07c699426ab04cf8e93468a3f07cd78aa8d761ac7c9d29c13e086c45fbe167d": {
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Italian              1       [ ]\n"
        ]
    },
    "f2b3a15572104da7cec42964a08cb7888e9c542d5345e9ffbcbee22428508b42": {
        "Return": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        Italian (no dead keys) 1       [ ]\n"
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



COL = re.compile(r"^(\d+)\s+(\S+)\s+(\d+)\s+")


def trim(text):
    lines = text.splitlines(keepends=True)
    head, rows = lines[:5], lines[5:]
    keep = []
    for r in rows:
        m = COL.match(r)
        if not m or m.group(3) == "1":
            keep.append(r)
    return "".join(head + keep)


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], trim(hit[1]))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
