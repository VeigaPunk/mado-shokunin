#!/usr/bin/env python3
"""mado round-25 C1 control, GREP-ALL SHORTCUT (CtlGrepAll).

Shape under test: the cheapest program that answers "what would this config
tree bind" without building a Hyprland bind-table resolver.

  * walk every file under the four config roots (no source graph, no glob
    evaluation, no `~` expansion): .config/hypr, .config/omarchy/current/theme,
    .local/share/omarchy/default/hypr, .local/state/omarchy/toggles/hypr;
  * regex-match every `bind*=...` line, commented-out ones included;
  * split the value on commas and stuff the pieces into the 18 hyprctl fields;
  * modmask from the mod names present in field 0;
  * flag booleans read straight off the bind keyword's letter suffix.

Deliberately skipped (this is the shortcut): source following, globbing,
`unbind`, `$variable` expansion, comment stripping, quoting/submap/device
handling, dispatcher validation.  Not a Hyprland resolver; a grep.
"""
import json
import os
import re
import sys

ROOTS = [".config/hypr", ".config/omarchy/current/theme",
         ".local/share/omarchy/default/hypr", ".local/state/omarchy/toggles/hypr"]

# HL_MODIFIER_* bits, matched by substring exactly as stringToModMask does.
MODS = [("SHIFT", 1), ("CAPS", 2), ("CTRL", 4), ("CONTROL", 4), ("ALT", 8), ("MOD1", 8),
        ("MOD2", 16), ("MOD3", 32), ("SUPER", 64), ("WIN", 64), ("LOGO", 64), ("MOD4", 64),
        ("META", 64), ("MOD5", 128)]

# commented-out lines are not stripped: "# bind = ..." matches too
BIND_RE = re.compile(r"^\s*(?:#+\s*)?bind([a-z]*)\s*=(.*)$")


def modmask(text):
    up = text.upper()
    mask = 0
    for name, bit in MODS:
        if name in up:
            mask |= bit
    return mask


def parse_key(key):
    if key.isdigit():
        return {"key": "", "keycode": int(key), "catch_all": False} if int(key) > 9 else \
               {"key": key, "keycode": 0, "catch_all": False}
    if key.startswith("code:") and key[5:].isdigit():
        return {"key": "", "keycode": int(key[5:]), "catch_all": False}
    if key == "catchall":
        return {"key": "", "keycode": 0, "catch_all": True}
    return {"key": key, "keycode": 0, "catch_all": False}


def entry(flags, value):
    parts = [p.strip() for p in value.split(",")]
    if len(parts) < 3:
        return None
    desc_flag = "d" in flags
    mouse = "m" in flags
    keyinfo = parse_key(parts[1])
    off = 1 if desc_flag else 0
    description = parts[2] if desc_flag else ""
    handler_idx = 2 + off
    if handler_idx >= len(parts):
        return None
    if mouse:
        dispatcher = "mouse"
        arg = parts[handler_idx]
    else:
        dispatcher = parts[handler_idx].lower()
        arg = ",".join(parts[handler_idx + 1:]).strip()
    return {
        "locked": "l" in flags,
        "mouse": mouse,
        "release": "r" in flags or "c" in flags or "g" in flags,
        "repeat": "e" in flags,
        "longPress": "o" in flags,
        "non_consuming": "n" in flags,
        "auto_consuming": "a" in flags,
        "has_description": desc_flag,
        "modmask": modmask(parts[0]),
        "submap": "",
        "submap_universal": "true" if "u" in flags else "false",
        "key": keyinfo["key"],
        "keycode": keyinfo["keycode"],
        "catch_all": keyinfo["catch_all"],
        "description": description,
        "allow_input_capture": "x" in flags,
        "dispatcher": dispatcher,
        "arg": arg,
    }


def main(argv):
    home = None
    i = 1
    while i < len(argv):
        if argv[i] == "--home" and i + 1 < len(argv):
            home = argv[i + 1]
            i += 2
        else:
            i += 1
    if home is None:
        home = os.environ.get("HOME", "")
    out = []
    for root in ROOTS:
        base = os.path.join(home, root)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames.sort()
            for name in sorted(filenames):
                path = os.path.join(dirpath, name)
                try:
                    with open(path, "r", errors="replace") as fh:
                        for line in fh:
                            m = BIND_RE.match(line.rstrip("\n"))
                            if not m:
                                continue
                            e = entry(m.group(1), m.group(2))
                            if e is not None:
                                out.append(e)
                except OSError:
                    continue
    json.dump(out, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
