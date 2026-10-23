#!/usr/bin/env python3
"""C1 NO-MERGE control: sources and variables, but one entry per workspace line.

Config traversal follows tools/mado-anims.py's legacy hyprlang parser pattern.
Rule fields follow Hyprland efb50993780079460b0cbed1363e2166a2de1d9f:
  src/config/legacy/ConfigManager.cpp:1676-1792
  src/debug/HyprCtl.cpp:522-550
  src/config/shared/complex/ComplexDataTypes.hpp:80-120
  src/helpers/MiscFunctions.cpp:125-475,478-512
The deliberately omitted operation is WorkspaceRuleManager::replaceOrAdd's
selector lookup and mergeLeft: handle_workspace always appends a fresh object.
This is a stdlib-only, byte-reading control; it never contacts a compositor.

Usage: python3 -I K1NoMerge.py --home DIR
"""
import argparse
import glob
import json
import os
import re
import stat

WS = " \t\n\r\v\f"
RULE_FIELDS = (
    ("gapsin:", "gap", "gapsIn"),
    ("gapsout:", "gap", "gapsOut"),
    ("bordersize:", "integer", "borderSize"),
    ("border:", "boolean", "border"),
    ("shadow:", "boolean", "shadow"),
    ("rounding:", "boolean", "rounding"),
    ("decorate:", "boolean", "decorate"),
    ("monitor:", "monitor", "monitor"),
    ("default:", "boolean", "default"),
    ("persistent:", "boolean", "persistent"),
    ("defaultName:", "name", "defaultName"),
    ("on-created-empty:", "command", "onCreatedEmpty"),
    ("layoutopt:", "layoutopt", None),
    ("layout:", "ignored", None),
    ("animation:", "ignored", None),
)


def trim(value):
    return value.strip(WS)


def parse_int(value):
    """ParserUtils::parseInt's boolean prefixes and whole-token int64 parsing."""
    if value.startswith(("true", "on", "yes")):
        return 1
    if value.startswith(("false", "off", "no")):
        return 0
    if value.startswith("0x"):
        if not re.fullmatch(r"0x[0-9a-fA-F]+", value):
            raise ValueError("invalid hex integer")
        result = int(value[2:], 16)
        if result > (1 << 64) - 1:
            raise ValueError("hex integer outside int64")
        return result if result < (1 << 63) else result - (1 << 64)
    if not re.fullmatch(r"-?[0-9]+", value):
        raise ValueError("invalid integer")
    result = int(value)
    if not -(1 << 63) <= result < (1 << 63):
        raise ValueError("integer outside int64")
    return result


def stoi(value):
    """std::stoi base 10 permits trailing junk, but is bounded to signed int."""
    match = re.match(r"[ \t\n\r\v\f]*([+-]?[0-9]+)", value)
    if not match:
        raise ValueError("invalid decimal prefix")
    result = int(match[1])
    if not -(1 << 31) <= result < (1 << 31):
        raise ValueError("integer outside int32")
    return result


def gap_data(value):
    # CVarList2 uses literal spaces, trims fields, and retains interior empties.
    parts = value.split(" ")
    if parts and parts[-1] == "":
        parts.pop()
    values = [stoi(trim(part)) for part in parts[:4]]
    if len(values) == 1:
        return values * 4
    if len(values) == 2:
        return values * 2
    if len(values) == 3:
        return values + [values[1]]
    if len(values) == 4:
        return values
    raise ValueError("empty gap")


def workspace_name(selector):
    # Only this name, not the runtime-assigned ID, is emitted in cleaned commands.
    if selector.startswith("special"):
        return "special:" + selector[8:] if len(selector) > 8 else "special:special"
    if selector.startswith("name:"):
        return selector[5:]
    if selector.startswith(("+", "-", "empty", "prev", "next")):
        return ""  # no active monitor/workspace while initial config is parsed
    if re.fullmatch(r"[0-9]+", selector):
        return str(max(stoi(selector), 1))
    return "-1"  # WORKSPACE_INVALID; static selectors are not literal workspace IDs


def clean_command(selector, value):
    command = trim(value)
    if not command:
        raise ValueError("empty creation command")
    workspace_rule = "workspace " + workspace_name(selector)
    if command.startswith("["):
        end = command.rfind("]")
        if end == -1:
            # std::string's npos arithmetic leaves the original command tail.
            rules, tail = command[1:], command
        else:
            rules, tail = command[1:end], command[end + 1:]
        rules = [trim(item) for item in rules.split(";")]
        found = False
        for i, item in enumerate(rules):
            if item.startswith("workspace"):
                rules[i] = workspace_rule
                found = True
        if not found:
            rules.append(workspace_rule)
        return "[" + ";".join(rules) + "] " + tail
    return "[" + workspace_rule + "] " + command


class State:
    def __init__(self, home):
        self.home = home
        self.variables = []
        self.ifs = []
        self.entries = []

    def get_var(self, name):
        for key, value in self.variables:
            if key == name:
                return value
        return None

    def set_var(self, name, value):
        for i, (key, _) in enumerate(self.variables):
            if key == name:
                self.variables[i] = (name, value)
                return
        self.variables.append((name, value))
        self.variables.sort(key=lambda item: -len(item[0]))


def parse_comment(text, state):
    comment = trim(text)
    if not comment.startswith("hyprlang"):
        return
    args = comment.split()
    variable = None
    for i in range(1, len(args)):
        if args[i] == "noerror":
            return
        if args[i] == "endif":
            if state.ifs:
                state.ifs.pop()
            return
        if args[i] == "if":
            variable = args[i + 1] if i + 1 < len(args) else ""
            break
    if variable:
        negated = variable.startswith("!")
        if negated:
            variable = variable[1:]
        value = state.get_var(variable)
        if value is None:
            failed = not negated
        else:
            truth = value == "1" or value.lower().startswith(("true", "yes", "on"))
            failed = truth if negated else not truth
        state.ifs.append(failed)


def absolute_path(value, current_path, home):
    if value.startswith("~"):
        return home + value[1:]
    if value.startswith("/"):
        return value
    return os.path.join(os.path.dirname(current_path), value)


def handle_source(value, state, current_path):
    if len(value) < 2:
        return
    pattern = absolute_path(value, current_path, state.home)
    for match in sorted(glob.glob(pattern)):
        path = absolute_path(match, current_path, state.home)
        try:
            mode = os.stat(path).st_mode
        except OSError:
            return
        if stat.S_ISREG(mode):
            parse_file(path, state)


def handle_workspace(value, state):
    selector, separator, rules = value.partition(",")
    selector = trim(selector)
    if not separator:
        rules = value  # C++ npos + 1 wraps to zero
    entry = {"workspaceString": selector, "enabled": True}
    try:
        for raw in rules.split(","):
            rule = trim(raw)
            if not rule:
                continue
            for needle, kind, field in RULE_FIELDS:
                position = rule.find(needle)
                if position == -1:
                    continue
                argument = rule[position + len(needle):]
                if kind == "gap":
                    entry[field] = gap_data(argument)
                elif kind == "integer":
                    entry[field] = stoi(argument)
                elif kind == "boolean":
                    entry[field] = bool(parse_int(argument))
                elif kind == "monitor":
                    if argument:
                        entry[field] = argument
                    else:
                        entry.pop(field, None)
                elif kind == "name":
                    entry[field] = trim(argument)
                elif kind == "command":
                    entry[field] = clean_command(selector, argument)
                elif kind == "layoutopt" and ":" not in argument:
                    raise ValueError("invalid layout option")
                break
    except ValueError:
        return  # the upstream handler rejects the entire failed line
    # NO-MERGE: no selector lookup, deduplication, update, or cross-line state.
    state.entries.append(entry)


def unescape_braces(value):
    output = []
    i = 0
    while i < len(value):
        if value[i] == "\\" and i + 1 < len(value) and value[i + 1] in "\\{}":
            output.append(value[i + 1])
            i += 2
        else:
            output.append(value[i])
            i += 1
    return "".join(output)


def parse_line(line, state, current_path):
    line = trim(line)
    position = line.find("#")
    if position == 0:
        parse_comment(line[1:], state)
        return
    if state.ifs and state.ifs[-1]:
        return
    while position != -1:
        if position + 1 < len(line) and line[position + 1] == "#":
            line = line[:position + 1] + line[position + 2:]
            position = line.find("#", position + 2)
        else:
            line = line[:position]
            break
    line = trim(line)
    if "=" not in line:
        return
    lhs, rhs = (trim(part) for part in line.split("=", 1))
    if not lhs:
        return
    is_variable = lhs.startswith("$")
    for _ in range(100):
        matched = False
        for name, value in state.variables:
            needle = "$" + name
            if not is_variable and needle in lhs:
                lhs = lhs.replace(needle, value)
                matched = True
            if needle in rhs:
                rhs = rhs.replace(needle, value)
                matched = True
        if not matched:
            break
    else:
        return
    if is_variable:
        state.set_var(lhs[1:], rhs)
        return
    rhs = unescape_braces(rhs)
    if lhs == "source":
        handle_source(rhs, state, current_path)
    elif lhs == "workspace":
        handle_workspace(rhs, state)


def parse_file(path, state):
    try:
        with open(path, "rb") as handle:
            lines = handle.read().decode("utf-8", "replace").split("\n")
    except OSError:
        return
    if lines and lines[-1] == "":
        lines.pop()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        while line.endswith("\\"):
            cut = len(line) - 2
            while cut >= 0 and line[cut] in " \t":
                cut -= 1
            line = line[:cut + 1]
            if i >= len(lines):
                return
            line += lines[i]
            i += 1
        parse_line(line, state, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    home = os.path.abspath(args.home)
    state = State(home)
    root = os.path.join(home, ".config/hypr/hyprland.conf")
    parse_file(os.path.realpath(root), state)
    print(json.dumps(state.entries))


if __name__ == "__main__":
    main()
