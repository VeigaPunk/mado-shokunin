#!/usr/bin/env python3
"""NO-VARIABLES control: follow sources and merge selectors, but never expand $names.

Variable assignments are ignored. Source paths, selectors, and rule values retain
literal dollar signs; there is no variable table or environment substitution.
Only the Python standard library is used, and config commands are never executed.
"""
import argparse
import glob
import json
import os
import re


RULE_FIELDS = (
    ("gapsin:", "gapsIn", "gaps"),
    ("gapsout:", "gapsOut", "gaps"),
    ("bordersize:", "borderSize", "integer"),
    ("border:", "border", "boolean"),
    ("shadow:", "shadow", "boolean"),
    ("rounding:", "rounding", "boolean"),
    ("decorate:", "decorate", "boolean"),
    ("monitor:", "monitor", "string"),
    ("default:", "default", "boolean"),
    ("persistent:", "persistent", "boolean"),
    ("defaultName:", "defaultName", "string"),
    ("on-created-empty:", "onCreatedEmpty", "command"),
    ("layoutopt:", None, "layoutopt"),
    ("layout:", None, "ignored"),
    ("animation:", None, "ignored"),
)


def split_args(text, delimiter, remove_empty=False):
    """CVarList2-style delimiters, including escaped delimiters and empty args."""
    args, escaped = [], []
    start = 0

    def append(end):
        raw = text[start:end]
        if escaped:
            removed = set(escaped)
            raw = "".join(c for i, c in enumerate(raw) if i not in removed)
        arg = raw.strip()
        if escaped or arg or not remove_empty:
            args.append(arg)

    for i, char in enumerate(text):
        if char != delimiter:
            continue
        if i > start and text[i - 1] == "\\":
            escaped.append(i - start - 1)
            if i - start == 1 or text[i - 2] != "\\":
                continue
        append(i)
        start = i + 1
        escaped = []
    if start < len(text):
        append(len(text))
    return args


def uncomment(line):
    """Hyprlang escapes a literal hash with a second hash, not a backslash."""
    pos = line.find("#")
    while pos >= 0:
        if line[pos:pos + 2] != "##":
            return line[:pos].strip()
        line = line[:pos + 1] + line[pos + 2:]
        pos = line.find("#", pos + 2)
    return line.strip()


def logical_lines(stream):
    for raw in stream:
        line = raw.removesuffix("\n")
        while line.endswith("\\"):
            following = next(stream, None)
            if following is None:
                return
            line = line[:-1].rstrip(" \t") + following.removesuffix("\n")
        yield uncomment(line.strip())


def stoi(text):
    match = re.match(r"\s*[+-]?[0-9]+", text)
    if match is None:
        raise ValueError("not an integer")
    value = int(match.group())
    if not -(1 << 31) <= value < 1 << 31:
        raise ValueError("integer out of range")
    return value


def boolean(text):
    if text.startswith(("true", "on", "yes")):
        return True
    if text.startswith(("false", "off", "no")):
        return False
    if text.startswith("0x"):
        if re.fullmatch(r"0x[0-9a-fA-F]+", text) is None:
            raise ValueError("invalid hexadecimal boolean")
        value = int(text, 16)
        if value >= 1 << 64:
            raise ValueError("boolean out of range")
    else:
        if re.fullmatch(r"-?[0-9]+", text) is None:
            raise ValueError("invalid boolean")
        value = int(text)
        if not -(1 << 63) <= value < 1 << 63:
            raise ValueError("boolean out of range")
    return bool(value)


def gaps(text):
    values = [stoi(arg) for arg in split_args(text, " ")[:4]]
    if len(values) == 1:
        return values * 4
    if len(values) == 2:
        return values * 2
    if len(values) == 3:
        return [values[0], values[1], values[2], values[1]]
    if len(values) == 4:
        return values
    raise ValueError("empty gaps")


def workspace_name(selector):
    if selector.startswith("special"):
        return "special:" + selector[8:] if len(selector) > 8 else "special:special"
    if selector.startswith("name:"):
        return selector[5:]
    if re.fullmatch(r"[0-9]+", selector):
        return str(max(stoi(selector), 1))
    return "-1"


def empty_command(selector, command):
    command = command.strip()
    if not command:
        raise ValueError("empty on-created-empty command")
    workspace = "workspace " + workspace_name(selector)
    if not command.startswith("["):
        return "[" + workspace + "] " + command
    closing = command.rfind("]")
    if closing < 0:
        raise ValueError("unclosed command rules")
    rules = [arg.strip() for arg in command[1:closing].split(";")]
    found = any(arg.startswith("workspace") for arg in rules)
    rules = [workspace if arg.startswith("workspace") else arg for arg in rules]
    if not found:
        rules.append(workspace)
    return "[" + ";".join(rules) + "] " + command[closing + 1:]


def workspace_rule(value):
    selector, separator, items = value.partition(",")
    selector = selector.strip()
    if not separator:
        items = value
    patch = {"workspaceString": selector, "enabled": True}
    for item in split_args(items, ",", remove_empty=True):
        for marker, key, kind in RULE_FIELDS:
            offset = item.find(marker)
            if offset < 0:
                continue
            text = item[offset + len(marker):]
            if kind == "gaps":
                patch[key] = gaps(text)
            elif kind == "integer":
                patch[key] = stoi(text)
            elif kind == "boolean":
                patch[key] = boolean(text)
            elif kind == "string":
                patch[key] = text.strip() if key == "defaultName" else text
            elif kind == "command":
                patch[key] = empty_command(selector, text)
            elif kind == "layoutopt" and ":" not in text:
                raise ValueError("invalid layout option")
            break
    if patch.get("monitor") == "":
        del patch["monitor"]
    return selector, patch


def table(home):
    home = os.path.realpath(home)
    rules, active = {}, set()

    def parse(path):
        real = os.path.realpath(path)
        if not real.startswith(home + os.sep) or real in active or not os.path.isfile(real):
            return
        try:
            stream = open(real, encoding="utf-8", errors="replace", newline="")
        except OSError:
            return
        active.add(real)
        try:
            with stream:
                for line in logical_lines(stream):
                    if "=" not in line:
                        continue
                    key, value = (part.strip() for part in line.split("=", 1))
                    if key.startswith("$"):
                        continue  # Deliberate control omission: never store variable definitions.
                    value = re.sub(r"\\([\\{}])", r"\1", value)
                    if key == "source":
                        if len(value) < 2:
                            continue
                        if value.startswith("~"):
                            source = home + value[1:]
                        elif os.path.isabs(value):
                            source = value
                        else:
                            source = os.path.join(os.path.dirname(path), value)
                        for included in sorted(glob.glob(source)):
                            parse(included)
                    elif key == "workspace":
                        try:
                            selector, patch = workspace_rule(value)
                        except ValueError:
                            continue  # Hyprland rejects the whole rule, not just the bad field.
                        rules.setdefault(selector, {}).update(patch)
        finally:
            active.remove(real)

    parse(os.path.join(home, ".config", "hypr", "hyprland.conf"))
    return list(rules.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    print(json.dumps(table(args.home), ensure_ascii=False))


if __name__ == "__main__":
    main()
