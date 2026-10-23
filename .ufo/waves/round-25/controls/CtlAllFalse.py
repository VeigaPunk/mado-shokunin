#!/usr/bin/env python3
"""Count reachable bind-like lines; emit default objects without resolving binds."""
import argparse
import glob
import json
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("--home", required=True)
home = parser.parse_args().home
seen = set()


def count(pattern):
    total = 0
    if pattern.startswith("~"):
        pattern = home + pattern[1:]
    for path in sorted(glob.glob(pattern)):
        if path in seen or not os.path.isfile(path):
            continue
        seen.add(path)
        with open(path, errors="replace") as source:
            for raw in source:
                line = raw.split("#", 1)[0]
                total += bool(re.match(r"^\s*bind[a-z]*\s*=", line))
                match = re.match(r"^\s*source\s*=\s*(.+?)\s*$", line)
                if match:
                    total += count(match.group(1))
    return total


entry = {
    "locked": False, "mouse": False, "release": False, "repeat": False,
    "longPress": False, "non_consuming": False, "auto_consuming": False,
    "has_description": False, "modmask": 0, "submap": "",
    "submap_universal": "false", "key": "", "keycode": 0,
    "catch_all": False, "description": "", "allow_input_capture": False,
    "dispatcher": "", "arg": "",
}
print(json.dumps([entry] * count(os.path.join(home, ".config/hypr/hyprland.conf"))))
