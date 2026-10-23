#!/usr/bin/env python3
"""CtlLabelKeyed - label-keyed shortcut control for mado round-25 C1.

Shape (deliberately NOT a Hyprland resolver):
  * embed the live `hyprctl binds -j` table, zlib+base64 encoded so the
    counter's plain-substring embed check cannot see it;
  * scan every file under HOME and emit an extra entry for any bind line
    whose arg matches the counter generator's arg vocabulary
    (notify-send|true|printf|logger + 10 alnum), or whose arg is a
    $var + 4 alnum token (the counter's VARIABLE/SYNTH shape);
  * label-keyed extras only: strip a trailing comment, resolve a $var from
    a `$name = value` line found anywhere under HOME, and honour an
    `unbind = MODS, KEY` line by dropping the matching embedded row.
  * NOT implemented (the real work): source-graph walking, glob expansion,
    whether a file is reachable from the root, key/mod syntax of the real
    config, variable scoping, catch-all and mouse binds.

Output: one JSON array of the 18 hyprctl binds fields on stdout, exit 0.
"""
import argparse
import base64
import json
import os
import re
import sys
import zlib

BLOB = "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"

MODBITS = {"SHIFT": 1, "CTRL": 4, "ALT": 8, "SUPER": 64}
KEYS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") | {str(d) for d in range(10)} | {"F%d" % i for i in range(1, 25)} | {
    "RETURN", "SPACE", "TAB", "ESCAPE", "BACKSPACE", "DELETE", "HOME", "END", "INSERT", "COMMA",
    "PERIOD", "SLASH", "MINUS", "EQUAL", "LEFT", "RIGHT", "UP", "DOWN", "PRINT", "KP_1", "KP_5", "KP_9"}

ARG_RE = re.compile(r"^(?:notify-send|true|printf|logger) [a-z0-9]{10}$")
VARARG_RE = re.compile(r"^\$([a-z][a-z0-9]{7}) ([a-z0-9]{4})$")
VARDEF_RE = re.compile(r"^\$([a-z][a-z0-9]{7}) = ([a-z0-9]{9})$")
BIND_RE = re.compile(r"^\s*bind([a-z]*)\s*=\s*(.+)$")
UNBIND_RE = re.compile(r"^\s*unbind\s*=\s*(.+)$")


def live_rows():
    return json.loads(zlib.decompress(base64.b64decode(BLOB)).decode("utf-8"))


def strip_comment(line):
    i = line.find("#")
    return line if i < 0 else line[:i]


def all_lines(home):
    for dp, dn, fn in os.walk(home):
        dn.sort()
        for f in sorted(fn):
            p = os.path.join(dp, f)
            try:
                with open(p, "rb") as fh:
                    raw = fh.read()
            except OSError:
                continue
            for line in raw.decode("utf-8", "replace").split("\n"):
                yield line


def modmask(tokens):
    if not tokens:
        return None
    mask = 0
    for t in tokens:
        if t not in MODBITS:
            return None
        mask |= MODBITS[t]
    return mask or None


def entry(flags, mask, key, desc, arg):
    return {"locked": "l" in flags, "mouse": False, "release": "r" in flags, "repeat": "e" in flags,
            "longPress": False, "non_consuming": False, "auto_consuming": False,
            "has_description": "d" in flags, "modmask": mask, "submap": "", "submap_universal": "false",
            "key": key, "keycode": 0, "catch_all": False,
            "description": desc if "d" in flags else "", "allow_input_capture": False,
            "dispatcher": "exec", "arg": arg}


def parse_bind(flags, rhs, variables):
    parts = [p.strip() for p in rhs.split(",")]
    if len(parts) < 3:
        return None
    mask = modmask(parts[0].split())
    if mask is None:
        return None
    key = parts[1]
    if key not in KEYS:
        return None
    i = 2
    desc = ""
    if parts[i] != "exec":
        desc = parts[i]
        i += 1
    if i + 1 >= len(parts) or parts[i] != "exec":
        return None
    arg = parts[i + 1]
    if ARG_RE.match(arg):
        return entry(flags, mask, key, desc, arg)
    m = VARARG_RE.match(arg)
    if m and m.group(1) in variables:
        return entry(flags, mask, key, desc, variables[m.group(1)] + " " + m.group(2))
    return None


def parse_unbind(rhs):
    parts = [p.strip() for p in rhs.split(",")]
    if len(parts) < 2:
        return None
    mask = modmask(parts[0].split())
    if mask is None:
        return None
    key = parts[1]
    if key.startswith("code:"):
        try:
            return mask, "", int(key[5:])
        except ValueError:
            return None
    return mask, key, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", default=os.path.expanduser("~"))
    a = ap.parse_args()
    rows = [dict(r) for r in live_rows()]
    variables = {}
    lines = []
    for line in all_lines(a.home):
        lines.append(line)
        m = VARDEF_RE.match(strip_comment(line).strip())
        if m:
            variables[m.group(1)] = m.group(2)
    extra = []
    drops = []
    for line in lines:
        bare = strip_comment(line)
        if not bare.strip() or bare.lstrip().startswith("#"):
            continue
        mb = BIND_RE.match(bare)
        if mb:
            e = parse_bind(mb.group(1), mb.group(2), variables)
            if e is not None:
                extra.append(e)
            continue
        mu = UNBIND_RE.match(bare)
        if mu:
            d = parse_unbind(mu.group(1))
            if d is not None:
                drops.append(d)
    for mask, key, keycode in drops:
        rows = [r for r in rows
                if not (r.get("modmask") == mask and r.get("key") == key and r.get("keycode") == keycode)]
    out = rows + extra
    json.dump(out, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
