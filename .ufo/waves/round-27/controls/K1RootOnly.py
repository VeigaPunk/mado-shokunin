#!/usr/bin/env python3
"""Root-only control for Hyprland v0.56.2 workspace-rule JSON.

Intentionally never opens or traverses a source directive. All config input is
read in one operation from HOME/.config/hypr/hyprland.conf. The root's own
variables, ordered field-wise merges and workspace command rewriting remain
active, so omission of sourced bytes is this control's distinguishing defect.
"""
import argparse
import json
import math
import os
import re
import struct
from pathlib import Path


KEYS = (
    ("gapsin:", "gapsIn"), ("gapsout:", "gapsOut"),
    ("bordersize:", "borderSize"), ("border:", "border"),
    ("shadow:", "shadow"), ("rounding:", "rounding"),
    ("decorate:", "decorate"), ("monitor:", "monitor"),
    ("default:", "default"), ("persistent:", "persistent"),
    ("defaultName:", "defaultName"), ("on-created-empty:", "onCreatedEmpty"),
    ("layoutopt:", None), ("layout:", None), ("animation:", None),
)
BOOL_KEYS = {"border", "shadow", "rounding", "decorate", "default", "persistent"}
INT_PREFIX = re.compile(r"^[ \t\r\n]*[+-]?[0-9]+")
FLOAT_PREFIX = re.compile(r"^[ \t]*[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def stoi(value):
    match = INT_PREFIX.match(value)
    if match is None:
        raise ValueError("not an integer")
    result = int(match.group())
    if not -(1 << 31) <= result < (1 << 31):
        raise ValueError("integer outside stoi range")
    return result


def parse_int(value):
    if value.startswith(("true", "on", "yes")):
        return 1
    if value.startswith(("false", "off", "no")):
        return 0
    if value.startswith("0x"):
        if not re.fullmatch(r"0x[0-9a-fA-F]+", value):
            raise ValueError("invalid hex")
        result = int(value, 16)
    else:
        if not re.fullmatch(r"[+-]?[0-9]+", value):
            raise ValueError("invalid integer")
        result = int(value)
    if not -(1 << 63) <= result < (1 << 63):
        raise ValueError("integer outside parseInt range")
    return result


def varlist(value, delimiter=",", remove_empty=True):
    """CVarList2 delimiter escaping, without shell or quote interpretation."""
    result = []
    start = 0
    escaped = []
    for index, char in enumerate(value):
        if char != delimiter:
            continue
        if index > start and value[index - 1] == "\\":
            escaped.append(index - start - 1)
            if index - start == 1 or value[index - 2] != "\\":
                continue
        part = value[start:index]
        if escaped:
            positions = set(escaped)
            part = "".join(c for i, c in enumerate(part) if i not in positions)
        part = part.strip()
        if part or not remove_empty:
            result.append(part)
        start = index + 1
        escaped = []
    if start < len(value):
        part = value[start:]
        if escaped:
            positions = set(escaped)
            part = "".join(c for i, c in enumerate(part) if i not in positions)
        part = part.strip()
        if part or not remove_empty:
            result.append(part)
    return result


def gap_data(value):
    values = [stoi(part) for part in varlist(value, " ", False)[:4]]
    if len(values) == 1:
        return values * 4
    if len(values) == 2:
        return values * 2
    if len(values) == 3:
        return values + [values[1]]
    if len(values) == 4:
        return values
    raise ValueError("empty gaps")


def workspace_name(selector):
    if selector.startswith("special"):
        return "special:" + selector[8:] if len(selector) > 8 else "special:special"
    if selector.startswith("name:"):
        return selector[5:]
    if re.fullmatch(r"[0-9]+", selector):
        return str(max(1, stoi(selector)))
    # Static selector patterns do not resolve to an existing workspace while
    # startup configuration is parsed: getWorkspaceIDNameFromString returns -1.
    return "-1"


def workspace_command(selector, value):
    command = value.strip()
    if not command:
        raise ValueError("empty workspace command")
    workspace = "workspace " + workspace_name(selector)
    if command.startswith("["):
        closing = command.rfind("]")
        if closing < 0:
            raise ValueError("unclosed command rules")
        rules = [part.strip() for part in command[1:closing].split(";")]
        found = False
        for index, rule in enumerate(rules):
            if rule.startswith("workspace"):
                rules[index] = workspace
                found = True
        if not found:
            rules.append(workspace)
        command = command[closing + 1:]
        prefix = "[" + ";".join(rules) + "]"
    else:
        prefix = "[" + workspace + "]"
    return prefix + " " + command


def workspace_rule(value):
    selector, comma, tail = value.partition(",")
    selector = selector.strip()
    # C++ npos + 1 wraps to zero for a selector-only rule.
    if not comma:
        tail = value
    rule = {"workspaceString": selector, "enabled": True}
    for item in varlist(tail):
        for prefix, output in KEYS:
            position = item.find(prefix)
            if position < 0:
                continue
            argument = item[position + len(prefix):]
            if output in ("gapsIn", "gapsOut"):
                rule[output] = gap_data(argument)
            elif output == "borderSize":
                rule[output] = stoi(argument)
            elif output in BOOL_KEYS:
                rule[output] = bool(parse_int(argument))
            elif output == "onCreatedEmpty":
                rule[output] = workspace_command(selector, argument)
            elif output == "defaultName":
                rule[output] = argument.strip()
            elif output == "monitor":
                if argument:
                    rule[output] = argument
            elif prefix == "layoutopt:" and ":" not in argument:
                raise ValueError("invalid layout option")
            # Layout/animation fields exist internally but are not exposed in
            # workspacerules JSON. Unknown items are likewise not serialized.
            break
    return rule


def strip_comment(line):
    if line.startswith("#"):
        return ""
    index = line.find("#")
    while index >= 0:
        if index + 1 < len(line) and line[index + 1] == "#":
            line = line[:index + 1] + line[index + 2:]
            index = line.find("#", index + 2)
        else:
            return line[:index].strip()
    return line.strip()


def logical_lines(text):
    physical = iter(text.split("\n"))
    for line in physical:
        while line.endswith("\\"):
            following = next(physical, None)
            if following is None:
                return
            line = line[:-1].rstrip(" \t") + following
        yield line.strip()


def float32(value):
    return struct.unpack("f", struct.pack("f", value))[0]


def expression(value, variables):
    tokens = value.split()
    if len(tokens) < 3 or tokens[1] not in ("+", "-", "*", "/"):
        raise ValueError("invalid expression")
    values = []
    for token in (tokens[0], tokens[2]):
        operand = variables.get(token, token)
        match = FLOAT_PREFIX.match(operand)
        if match is None:
            raise ValueError("invalid expression operand")
        values.append(float32(float(match.group())))
    left, right = values
    if tokens[1] == "+":
        result = left + right
    elif tokens[1] == "-":
        result = left - right
    elif tokens[1] == "*":
        result = left * right
    elif right:
        result = left / right
    else:
        result = math.nan if left == 0 else math.copysign(math.inf, left * math.copysign(1, right))
    result = float32(result)
    # std::format's default general float representation is shortest-roundtrip.
    if math.isfinite(result):
        for precision in range(1, 10):
            rendered = format(result, ".%dg" % precision)
            if float32(float(rendered)) == result:
                return rendered
    return str(result)


def expand(lhs, rhs, variables):
    definition = lhs.startswith("$")
    names = sorted(variables, key=len, reverse=True)
    for _ in range(100):
        matched = False
        for name in names:
            token = "$" + name
            if token in rhs or (not definition and token in lhs):
                matched = True
                rhs = rhs.replace(token, variables[name])
                if not definition:
                    lhs = lhs.replace(token, variables[name])
        rhs = re.sub(r"(?<!\\)\{\{(.*?)\}\}", lambda m: expression(m[1], variables), rhs)
        if not matched:
            return lhs, rhs
    raise ValueError("variable expansion limit")


def predict(text):
    variables = dict(os.environ)
    rules = {}
    conditions = []
    for line in logical_lines(text):
        if line.startswith("#"):
            words = line[1:].strip().split()
            if words and words[0] == "hyprlang":
                if "endif" in words:
                    if conditions:
                        conditions.pop()
                elif "if" in words:
                    index = words.index("if") + 1
                    if index < len(words):
                        name = words[index]
                        negated = name.startswith("!")
                        name = name[1:] if negated else name
                        present = bool(os.environ.get(name, variables.get(name, "")))
                        conditions.append(present if negated else not present)
            continue
        if conditions and conditions[-1]:
            continue
        line = strip_comment(line)
        if "=" not in line:
            continue
        lhs, rhs = (part.strip() for part in line.split("=", 1))
        # The deliberate ROOT-ONLY boundary: source arguments are not opened,
        # globbed, resolved, inspected, or used to seed the variable namespace.
        if not lhs or lhs == "source":
            continue
        try:
            lhs, rhs = expand(lhs, rhs, variables)
            if lhs.startswith("$"):
                variables[lhs[1:]] = rhs
                continue
            rhs = re.sub(r"\\([\\{}])", r"\1", rhs)
            if lhs != "workspace":
                continue
            rule = workspace_rule(rhs)
        except (ValueError, OverflowError):
            # Hyprland records a config error and continues with later lines;
            # it does not merge a partially parsed workspace-rule record.
            continue
        selector = rule["workspaceString"]
        if selector in rules:
            rules[selector].update(rule)
        else:
            rules[selector] = rule
    return list(rules.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    root = Path(args.home) / ".config/hypr/hyprland.conf"
    text = root.read_text(encoding="utf-8", errors="replace")
    print(json.dumps(predict(text), ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
