#!/usr/bin/env python3
"""Grep-all control: read every root file, not the Hyprland source graph.

Only comma fields, canonical modifier names and bind suffix flags are mapped.
Variables, unbind, inline comments, source reachability and submaps are ignored.
Rejected flag/dispatcher combinations are deliberately not validated.
"""
import argparse
import json
import os
import re
import sys

ROOTS = (
    ".config/hypr",
    ".config/omarchy/current/theme",
    ".local/share/omarchy/default/hypr",
    ".local/state/omarchy/toggles/hypr",
)
MODS = {
    "SHIFT": 1, "CAPS": 2, "CTRL": 4, "ALT": 8,
    "MOD2": 16, "MOD3": 32, "SUPER": 64, "MOD5": 128,
}
BIND = re.compile(r"^\s*bind([a-z]*)\s*=(.*)$")


def entry(flags, value):
    described = "d" in flags
    handler_index = 3 if described else 2
    # The final comma field retains its own commas and internal whitespace.
    parts = [part.strip() for part in value.split(",", handler_index + 1)]
    if len(parts) <= handler_index:
        return None
    mask = 0
    for name in re.split(r"[\s_+|]+", parts[0].upper()):
        mask |= MODS.get(name, 0)
    key = parts[1]
    keycode = 0
    catch_all = key == "catchall"
    if key.isascii() and key.isdigit() and int(key) > 9:
        keycode, key = int(key), ""
    elif key.startswith("code:") and key[5:].isascii() and key[5:].isdigit():
        keycode, key = int(key[5:]), ""
    elif catch_all:
        key = ""
    mouse = "m" in flags
    dispatcher = "mouse" if mouse else parts[handler_index].lower()
    arg = parts[handler_index] if mouse else (
        parts[handler_index + 1] if len(parts) > handler_index + 1 else ""
    )
    return {
        "locked": "l" in flags,
        "mouse": mouse,
        "release": any(flag in flags for flag in "rcg"),
        "repeat": "e" in flags,
        "longPress": "o" in flags,
        "non_consuming": "n" in flags,
        "auto_consuming": "a" in flags,
        "has_description": described,
        "modmask": mask,
        "submap": "",
        "submap_universal": "true" if "u" in flags else "false",
        "key": key,
        "keycode": keycode,
        "catch_all": catch_all,
        "description": parts[2] if described else "",
        "allow_input_capture": "x" in flags,
        "dispatcher": dispatcher,
        "arg": arg,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", required=True)
    home = parser.parse_args().home
    out = []
    for root in ROOTS:
        for directory, directories, files in os.walk(os.path.join(home, root)):
            directories.sort()
            for name in sorted(files):
                try:
                    with open(os.path.join(directory, name), encoding="utf-8", errors="replace") as source:
                        for line in source:
                            if line.lstrip().startswith("#"):
                                continue
                            match = BIND.match(line.rstrip("\n"))
                            if match:
                                bind = entry(match.group(1), match.group(2))
                                if bind is not None:
                                    out.append(bind)
                except OSError:
                    continue
    json.dump(out, sys.stdout)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
