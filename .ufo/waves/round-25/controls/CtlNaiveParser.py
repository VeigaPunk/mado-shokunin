#!/usr/bin/env python3
"""Cheap partial resolver: deliberately no variables, unbinds or d-field offset."""
import argparse, glob, json, os, re

cli = argparse.ArgumentParser()
cli.add_argument("--home", required=True)
home = os.path.abspath(cli.parse_args().home)
binds, active = [], set()
flags = {"locked": "l", "mouse": "m", "release": "rcg", "repeat": "e",
         "longPress": "o", "non_consuming": "n", "auto_consuming": "a",
         "has_description": "d", "allow_input_capture": "x"}
modifiers = [(1, ("SHIFT",)), (2, ("CAPS",)), (4, ("CTRL", "CONTROL")),
             (8, ("ALT", "MOD1")), (16, ("MOD2",)), (32, ("MOD3",)),
             (64, ("SUPER", "WIN", "LOGO", "MOD4", "META")), (128, ("MOD5",))]


def bind(letters, value):
    parts = [p.strip() for p in value.split(",", 3)]
    if len(parts) < 3:
        return
    parts += [""] * (4 - len(parts))
    mods, key, dispatcher, arg = parts
    mask = sum(bit for bit, names in modifiers if any(n in mods.upper() for n in names))
    code = int(key[5:]) if key.startswith("code:") and key[5:].isdigit() else 0
    entry = {field: any(c in letters for c in chars) for field, chars in flags.items()}
    entry.update(modmask=mask, submap="", submap_universal="true" if "u" in letters else "false",
                 key="" if code else key, keycode=code, catch_all=key.lower() == "catchall",
                 description="", dispatcher=dispatcher, arg=arg)
    binds.append(entry)


def source(pattern, parent):
    if pattern.startswith("~"):
        pattern = home + pattern[1:]
    if not os.path.isabs(pattern):
        pattern = os.path.join(parent, pattern)
    for path in sorted(glob.glob(pattern)):
        if path in active or not os.path.isfile(path):
            continue
        active.add(path)
        with open(path, errors="replace") as stream:
            for raw in stream:
                line = raw.strip()
                include = re.fullmatch(r"source\s*=\s*(.+)", line)
                if include:
                    source(include[1], os.path.dirname(path))
                    continue
                match = re.fullmatch(r"bind([a-z]*)\s*=\s*(.*)", line)
                if match:
                    bind(match[1], match[2])
        active.remove(path)


source(os.path.join(home, ".config/hypr/hyprland.conf"), home)
print(json.dumps(binds))
