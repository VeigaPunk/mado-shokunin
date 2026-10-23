#!/usr/bin/env python3
"""NAIVE-GREP control: independent regex records from the root config only.

Never follows sources, expands variables, or merges repeated selectors. Boolean
values are deliberately restricted to the literal words true and false.
"""
import argparse
import json
import re
from pathlib import Path


WORKSPACE = re.compile(r"^\s*workspace\s*=\s*(.*?)\s*$")
ITEM = re.compile(r"^\s*([A-Za-z][A-Za-z-]*)\s*:\s*(.*?)\s*$")
INTEGER = re.compile(r"^[+-]?\d+")
BOOL_KEYS = {"default", "persistent", "border", "rounding", "decorate", "shadow"}
GAP_KEYS = {"gapsin": "gapsIn", "gapsout": "gapsOut"}


def gap_values(value):
    values = []
    for part in value.split():
        match = INTEGER.match(part)
        if match is None:
            return None
        values.append(int(match.group()))
    if len(values) == 1:
        return values * 4
    if len(values) == 2:
        return values * 2
    if len(values) == 3:
        return values + [values[1]]
    if len(values) >= 4:
        return values[:4]
    return None


def on_empty(selector, command):
    if not command:
        return None
    if selector.startswith("name:"):
        name = selector[5:]
    elif selector.startswith("special"):
        name = selector if len(selector) > 8 else "special:special"
    elif re.fullmatch(r"\d+", selector):
        name = str(max(1, int(selector)))
    else:
        name = "-1"
    workspace_rule = "workspace " + name
    bracket = re.fullmatch(r"\[(.*)\](.*)", command)
    if bracket:
        rules = [part.strip() for part in bracket[1].split(";") if part.strip()]
        found = any(rule.startswith("workspace") for rule in rules)
        rules = [workspace_rule if rule.startswith("workspace") else rule for rule in rules]
        if not found:
            rules.append(workspace_rule)
        return "[" + ";".join(rules) + "] " + bracket[2]
    return "[" + workspace_rule + "] " + command


def record(line):
    # Each physical line is independent. Double hashes are literal hashes.
    line = re.sub(r"##|#.*", lambda match: "#" if match[0] == "##" else "", line)
    match = WORKSPACE.fullmatch(line)
    if match is None:
        return None
    fields = re.split(r"\s*,\s*", match[1])
    selector = fields[0].strip()
    result = {"workspaceString": selector, "enabled": True}
    for field in fields[1:]:
        item = ITEM.fullmatch(field)
        if item is None:
            continue
        key, value = item.groups()
        if key in BOOL_KEYS:
            if value in ("true", "false"):
                result[key] = value == "true"
        elif key in GAP_KEYS:
            gaps = gap_values(value)
            if gaps is not None:
                result[GAP_KEYS[key]] = gaps
        elif key == "bordersize":
            integer = INTEGER.match(value)
            if integer is not None:
                result["borderSize"] = int(integer.group())
        elif key == "monitor":
            if value:
                result["monitor"] = value
        elif key == "defaultName":
            result["defaultName"] = value
        elif key == "on-created-empty":
            command = on_empty(selector, value)
            if command is not None:
                result["onCreatedEmpty"] = command
        # layout/layoutopt/animation do not appear in workspacerules JSON.
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    root = Path(args.home) / ".config/hypr/hyprland.conf"
    rules = []
    with root.open(encoding="utf-8", errors="replace") as config:
        for line in config:
            rule = record(line.rstrip("\r\n"))
            if rule is not None:
                rules.append(rule)
    print(json.dumps(rules, ensure_ascii=False))


if __name__ == "__main__":
    main()
