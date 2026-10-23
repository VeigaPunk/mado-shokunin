#!/usr/bin/env python3
"""K4EasyOnly: static easy-grammar control, with no embedded table or cache.

Read the ordered source graph, variables, comments, bind[dler]* and unbind.
Only canonical, whitespace-separated SUPER/SHIFT/CTRL/ALT mods are understood.
Keys and dispatchers stay literal: no aliases, modifier separators, keycodes,
mouse semantics, other flags, rejected-line rules, validation or case folding.
This is deliberately not a complete Hyprland bind-table resolver.
"""
import argparse
import glob
import json
import os
import re


MODS = {"SUPER": 64, "SHIFT": 1, "CTRL": 4, "ALT": 8}
EASY_BIND = re.compile(r"bind([dler]*)\Z")
VARIABLE_NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")


def uncomment(line):
    out = []
    i = 0
    while i < len(line):
        if line[i] == "#":
            if line[i:i + 2] != "##":
                break
            out.append("#")
            i += 2
        else:
            out.append(line[i])
            i += 1
    return "".join(out).strip()


def modmask(text):
    mask = 0
    for token in text.split():
        mask |= MODS.get(token, 0)
    return mask


class EasyResolver:
    def __init__(self, home):
        self.home = os.path.abspath(home)
        self.variables = {}
        self.binds = []
        self.active = set()

    def expand(self, text):
        names = sorted(self.variables, key=len, reverse=True)
        out = []
        i = 0
        while i < len(text):
            if text[i] != "$":
                out.append(text[i])
                i += 1
                continue
            for name in names:
                if text.startswith(name, i + 1):
                    out.append(self.variables[name])
                    i += len(name) + 1
                    break
            else:
                match = VARIABLE_NAME.match(text, i + 1)
                if match and match.group() in os.environ:
                    out.append(os.environ[match.group()])
                    i = match.end()
                else:
                    out.append("$")
                    i += 1
        return "".join(out)

    def source(self, pattern, directory):
        if pattern == "~" or pattern.startswith("~/"):
            pattern = self.home + pattern[1:]
        if not os.path.isabs(pattern):
            pattern = os.path.join(directory, pattern)
        for path in sorted(glob.glob(pattern)):
            real = os.path.realpath(path)
            if real in self.active or not os.path.isfile(path):
                continue
            self.active.add(real)
            try:
                with open(path, encoding="utf-8", errors="replace") as stream:
                    for raw in stream:
                        self.line(uncomment(raw), os.path.dirname(path))
            finally:
                self.active.remove(real)

    def line(self, text, directory):
        if "=" not in text:
            return
        keyword, value = text.split("=", 1)
        keyword, value = keyword.strip(), value.strip()
        if keyword.startswith("$"):
            self.variables[keyword[1:]] = self.expand(value)
            return
        value = self.expand(value)
        if keyword == "source":
            self.source(value, directory)
            return
        if keyword == "unbind":
            parts = [part.strip() for part in value.split(",", 1)]
            parts += [""] * (2 - len(parts))
            mask, key = modmask(parts[0]), parts[1]
            self.binds[:] = [entry for entry in self.binds
                             if (entry["modmask"], entry["key"]) != (mask, key)]
            return
        match = EASY_BIND.fullmatch(keyword)
        if not match:
            return
        flags = match.group(1)
        described = "d" in flags
        width = 5 if described else 4
        parts = [part.strip() for part in value.split(",", width - 1)]
        parts += [""] * (width - len(parts))
        mods, key = parts[:2]
        desc = parts[2] if described else ""
        dispatcher, arg = parts[-2:]
        self.binds.append({
            "locked": "l" in flags,
            "mouse": False,
            "release": "r" in flags,
            "repeat": "e" in flags,
            "longPress": False,
            "non_consuming": False,
            "auto_consuming": False,
            "has_description": described,
            "modmask": modmask(mods),
            "submap": "",
            "submap_universal": "false",
            "key": key,
            "keycode": 0,
            "catch_all": False,
            "description": desc,
            "allow_input_capture": False,
            "dispatcher": dispatcher,
            "arg": arg,
        })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    resolver = EasyResolver(args.home)
    resolver.source(os.path.join(resolver.home, ".config/hypr/hyprland.conf"), resolver.home)
    print(json.dumps(resolver.binds, ensure_ascii=False))


if __name__ == "__main__":
    main()
