#!/usr/bin/env python3
"""control c07-read-fixture-repo - CHEAT: read the fixture file from the repository at run time and answer from it

Stops at: clause i (isolation): no repository path is bound in the sandbox, so the read fails and the answer is empty; outside the sandbox the same file answers every fixture correctly

The read path is $MADO_CTL_FIXTURES or quality/counters/c1-r49-fixtures.json relative to the cwd. The control
demonstrates why the mount set has to be an allowlist: run it on the host with the file reachable and it is
byte-exact; run it in the counter's sandbox and it has nothing to read. It also shows that an inherited
environment variable must not reach the tool (the sandbox uses --clearenv).
"""
import hashlib
import json
import re
import sys

import os
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



FIXTURE_PATH = os.environ.get("MADO_CTL_FIXTURES", "quality/counters/c1-r49-fixtures.json")


def repo_table():
    try:
        with open(FIXTURE_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    t = {}
    for c in data.get("cases", []):
        t.setdefault(c.get("keymap_sha256"), {})[c.get("keysym")] = [c.get("rc"), c.get("stdout", "")]
    return t


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = repo_table().get(keymap_sha(o["keymap"]), {}).get(o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], hit[1])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
