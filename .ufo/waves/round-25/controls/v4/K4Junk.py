#!/usr/bin/env python3
"""JUNK control: count root-file bind-prefixed lines; invent every entry."""
import argparse
import json
from pathlib import Path
import random


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    root = Path(args.home) / ".config/hypr/hyprland.conf"
    with root.open("rb") as source:
        count = sum(line.startswith(b"bind") for line in source)

    rng = random.SystemRandom()
    entries = []
    for _ in range(count):
        entries.append({
            "locked": bool(rng.getrandbits(1)),
            "mouse": bool(rng.getrandbits(1)),
            "release": bool(rng.getrandbits(1)),
            "repeat": bool(rng.getrandbits(1)),
            "longPress": bool(rng.getrandbits(1)),
            "non_consuming": bool(rng.getrandbits(1)),
            "auto_consuming": bool(rng.getrandbits(1)),
            "has_description": bool(rng.getrandbits(1)),
            "modmask": rng.randrange(256),
            "submap": "",
            "submap_universal": rng.choice(("false", "true")),
            "key": rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"),
            "keycode": 0,
            "catch_all": False,
            "description": "%032x" % rng.getrandbits(128),
            "allow_input_capture": bool(rng.getrandbits(1)),
            "dispatcher": "exec",
            "arg": "%032x" % rng.getrandbits(128),
        })
    print(json.dumps(entries, separators=(",", ":")))


if __name__ == "__main__":
    main()
