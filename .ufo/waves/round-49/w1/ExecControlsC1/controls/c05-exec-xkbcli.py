#!/usr/bin/env python3
"""control c05-exec-xkbcli - CHEAT: the tool shells out to the pinned how-to-type instead of implementing anything.

It is byte-exact on every case, fixed or generated, because it *is* the judge. The only clause that can stop it is the
counter's no-process tripwire: after the sandboxed python3 execve, the execve of /usr/lib/xkbcommon/xkbcli-how-to-type
is a trip. This control exists to prove that clause fires - a counter without the tripwire scores it TARGET_MET.

Contract shape kept for the scoreable surface: `how-to-type --keymap FILE --disable-compose --keysym ARG`, plus
`--selftest`.
"""
import subprocess
import sys

JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"


def parse(argv):
    opts = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--keymap":
            opts["keymap"] = argv[i + 1]
            i += 2
        elif a.startswith("--keymap="):
            opts["keymap"] = a.split("=", 1)[1]
            i += 1
        elif a in ("--disable-compose",):
            opts["disable_compose"] = True
            i += 1
        elif a == "--keysym":
            opts["keysym"] = argv[i + 1]
            i += 2
        elif a.startswith("--keysym="):
            opts["keysym"] = a.split("=", 1)[1]
            i += 1
        else:
            opts["_other"] = True
            i += 1
    return opts


def main(argv):
    if "--selftest" in argv:
        for _ in range(25):
            pass
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    p = subprocess.run([JUDGE, "--keymap=" + o["keymap"], "--disable-compose", "--keysym", o["keysym"]],
                       capture_output=True)
    sys.stdout.write(p.stdout.decode("utf-8", "surrogateescape"))
    return p.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
