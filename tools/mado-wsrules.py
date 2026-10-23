#!/usr/bin/env python3
"""Static resolver for the workspace-rule table of a Hyprland v0.56.2 config tree.

Reads DIR/.config/hypr/hyprland.conf and every file it reaches through `source =`
from bytes only (no compositor, no socket, no network), and prints the JSON array
`hyprctl workspacerules -j` prints for that tree.  Exit 0.

Source graph: `source =` is followed depth-first in line order (the legacy manager's
handler parses the matched file synchronously at the point of the source line), with
`~` expanded to DIR, relative paths resolved against the directory of the file that
contains the source line, and glob(3)-sorted glob matches; matches that are not
regular files are skipped.  A file sourced twice is parsed twice.  Line handling
follows hyprlang v0.6.8: `#` comments with `##` escapes, `\\`-continued lines,
`$name = value` variables (one table shared by the whole parse, so a definition is
visible to later lines of the same tree in parse order and a redefinition takes
effect from that line on), and `{{ expr }}` single-operator expressions.

Rule grammar: the legacy `workspace = SELECTOR, RULES` keyword.  The selector is the
first comma field, trimmed; the remainder is split on commas (empty fields dropped,
each field trimmed) and each field is matched by substring search against the fixed
key order gapsin, gapsout, bordersize, border, shadow, rounding, decorate, monitor,
default, persistent, defaultName, on-created-empty, layoutopt, layout, animation
(the first key found in a field wins, the rest of that field is its value).  Value
failures drop the whole line.  Rows are keyed by the exact trimmed selector string:
a later line with the same selector merges into the existing row in place (first-seen
order), overwriting only the fields it sets.  Only the fields of
getWorkspaceRuleData are printed: workspaceString, enabled, monitor, default,
persistent, gapsIn, gapsOut, borderSize, border, rounding, decorate, shadow,
defaultName, onCreatedEmpty.

Sources (corpus/SOURCES.md): S158 HyprCtl.cpp
(https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp,
getWorkspaceRuleData and workspaceRulesRequest); S162 ConfigManager.cpp
(https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp,
handleWorkspaceRules and handleSource); S172 hyprlang syntax page (comment and `##`
escape rules); S173 hyprlang v0.6.8 src/config.cpp
(https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp, parseLine,
parseVariable, parseExpression, getNextLine); S178 wiki Workspace-Rules (selector
grammar and the keys); S179 WorkspaceRuleManager.cpp
(https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp,
replaceOrAdd); S180 ComplexDataTypes.hpp (CCssGapData::parseGapData); S181
ParserUtils.cpp (parseInt); S182 MiscFunctions.cpp
(https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp,
cleanCmdForWorkspace and getWorkspaceIDNameFromString).  hyprutils v0.14.2
src/string/VarList2.cpp, src/string/VarList.cpp, src/string/String.cpp and
include/hyprutils/string/Numeric.hpp (CVarList2, CVarList, trim, replaceInString,
strToNumber).  Pins: Hyprland efb50993780079460b0cbed1363e2166a2de1d9f (v0.56.2),
hyprlang 3a1c1b25b059dae2c6bbc46991562ba1158d125c (v0.6.8), hyprutils v0.14.2.

Environment limit (round-27 note, M26-10, as in tools/mado-binds.py): environment
variables are not imported into the config variable table, unlike hyprlang v0.6.8,
which seeds its variable list from the process environment.  A `$NAME` supplied only
by the environment therefore stays literal, and `source = $VAR` using only an
environment value is not followed.  Variables defined in the config tree are still
expanded.  Selectors that resolve only against live compositor state ("prev", "next",
"empty", r+-/m+-/e+- relative selectors) are outside a static read; their
on-created-empty command prefix uses the empty name Hyprland uses when that state is
absent.

Usage: python3 -I mado-wsrules.py --home DIR
"""

import glob as globmodule
import json
import math
import os
import re
import stat
import struct
import sys

WS = " \t\n\r\v\f"
DIGITS = "0123456789"
WORKSPACE_INVALID = -1

HOME = [""]

_INT_RE = re.compile(r"-?[0-9]+\Z")
_HEX_RE = re.compile(r"[0-9a-fA-F]+\Z")


class ExprError(Exception):
    """A closed `{{...}}` pair or a variable loop hyprlang rejects: the line is dropped."""


def trim(s):
    return s.strip(WS)


# --------------------------------------------------------------------------
# hyprutils v0.14.2 string helpers


def cvarlist2(value, delim=",", remove_empty=False):
    """CVarList2::construct with allowEscape=true: split on delim, trim each field,
    drop empties only when asked; a backslash-escaped delim does not split."""
    if not value:
        return []
    args = []
    arg_begin = 0
    escaped = []
    size = len(value)
    i = 0
    while i < size:
        c = value[i]
        if c != delim:
            i += 1
            continue
        if i - arg_begin != 0:
            previous = value[i - 1]
            if i - arg_begin == 1:
                if previous == "\\":
                    escaped.append(i - arg_begin - 1)
                    i += 1
                    continue
            else:
                prev_previous = value[i - 2]
                if previous == "\\":
                    escaped.append(i - arg_begin - 1)
                    if prev_previous != "\\":
                        i += 1
                        continue
        args.extend(_finish_field(value[arg_begin:i], escaped, remove_empty))
        arg_begin = i + 1
        escaped = []
        i += 1
    if arg_begin < size:
        args.extend(_finish_field(value[arg_begin:], escaped, remove_empty))
    return args


def _finish_field(piece, escaped, remove_empty):
    if not escaped:
        arg = trim(piece)
        if arg or not remove_empty:
            return [arg]
        return []
    copy = piece
    for k, idx in enumerate(escaped):
        copy = copy[:idx - k] + copy[idx - k + 1:]
    return [trim(copy)]


def cvarlist(value, delim=","):
    """CVarList: split on delim, trim each field, keep empties (lastArgNo unused)."""
    if not value:
        return [""]
    return [trim(part) for part in value.split(delim)]


def is_number(s):
    """hyprutils isNumber (integers only): optional leading '-', then digits."""
    if not s:
        return False
    for i, c in enumerate(s):
        if i == 0 and c == "-":
            continue
        if c not in DIGITS:
            return False
    return s[-1] in DIGITS


def cpp_stoi(s):
    """std::stoi: skip leading whitespace, optional sign, digits; None where it throws."""
    i = 0
    size = len(s)
    while i < size and s[i] in WS:
        i += 1
    start = i
    if i < size and s[i] in "+-":
        i += 1
    first_digit = i
    while i < size and s[i] in DIGITS:
        i += 1
    if i == first_digit:
        return None
    value = int(s[start:i])
    if value < -2147483648 or value > 2147483647:
        return None
    return value


def str_to_number(sv):
    """hyprutils strToNumber<int64_t>: strict from_chars, optional 0x hex."""
    if not sv:
        return None
    if len(sv) >= 2 and sv[0] == "0" and sv[1] in "xX":
        body = sv[2:]
        if not body or not _HEX_RE.match(body):
            return None
        value = int(body, 16)
        if value > 0xFFFFFFFFFFFFFFFF:
            return None
        if value > 0x7FFFFFFFFFFFFFFF:
            value -= 1 << 64
        return value
    if not _INT_RE.match(sv):
        return None
    value = int(sv)
    if value < -(1 << 63) or value > (1 << 63) - 1:
        return None
    return value


def parse_int(val):
    """ParserUtils::parseInt: prefix booleans, hex, then a strict integer."""
    if val.startswith("0x"):
        return str_to_number(val)
    if val.startswith("true") or val.startswith("on") or val.startswith("yes"):
        return 1
    if val.startswith("false") or val.startswith("off") or val.startswith("no"):
        return 0
    return str_to_number(val)


# --------------------------------------------------------------------------
# hyprlang v0.6.8 expressions (single operator, binary32 arithmetic)


_F32 = struct.Struct("<f")
QNAN = _F32.unpack(_F32.pack(0xFFC00000))[0]


def to_f32(x):
    try:
        return _F32.unpack(_F32.pack(x))[0]
    except (OverflowError, ValueError):
        return math.inf if x > 0 else -math.inf


def stof(token):
    """std::stof for the tokens hyprlang feeds it; None where libstdc++ throws."""
    if not token:
        return None
    try:
        if token.lower().lstrip("+-").startswith("0x"):
            return to_f32(float.fromhex(token))
        return to_f32(float(token))
    except (ValueError, OverflowError):
        return None


def arith(left, op, right):
    """binary32 `left op right`; invalid operations yield x86's default QNaN."""
    try:
        if op == "+":
            return to_f32(left + right)
        if op == "-":
            return to_f32(left - right)
        if op == "*":
            return to_f32(left * right)
        if right == 0.0:
            if left != left or left == 0.0:
                return QNAN
            return math.copysign(math.inf, left) * math.copysign(1.0, right)
        return to_f32(left / right)
    except (OverflowError, ValueError, ZeroDivisionError):
        return QNAN


def fmt_f32(value):
    """std::format("{}", value) for a binary32 value: the shortest decimal text that
    reads back as the same binary32."""
    if value != value:
        return "-nan" if math.copysign(1.0, value) < 0 else "nan"
    if value == math.inf:
        return "inf"
    if value == -math.inf:
        return "-inf"
    if value == 0.0:
        return "-0" if math.copysign(1.0, value) < 0 else "0"
    rendered = None
    for precision in range(1, 10):
        candidate = "{:.{}g}".format(value, precision)
        if to_f32(float(candidate)) == value:
            rendered = candidate
            break
    if rendered is None:
        rendered = "{:.9g}".format(value)
    return rendered


def parse_expression(text, st):
    """CConfigImpl::parseExpression: two operands and one operator, whitespace split."""
    args = [token for token in text.split() if token]
    op = args[1] if len(args) > 1 else ""
    if op not in ("+", "-", "*", "/"):
        raise ExprError("Invalid expression type")
    operands = []
    for index in (0, 2):
        token = args[index] if index < len(args) else ""
        stored = st.get_var(token)
        value = stof(stored) if stored is not None else stof(token)
        if value is None:
            raise ExprError("Failed to parse expression")
        operands.append(value)
    return arith(operands[0], op, operands[1])


def expand_expressions(rhs, st):
    """The `while (RHS.contains("{{"))` loop of parseLine."""
    while "{{" in rhs:
        begin = rhs.find("{{")
        while begin > 0:
            skipped = 0
            i = begin - 1
            while i >= 0 and rhs[i] == "\\":
                skipped += 1
                i -= 1
            if skipped % 2 == 0:
                break
            begin = rhs.find("{{", begin + 1)
            if begin == -1:
                break
        if begin == -1:
            break
        end = rhs.find("}}", begin + 2)
        if end == -1:
            break
        rhs = rhs[:begin] + fmt_f32(parse_expression(rhs[begin + 2:end], st)) + rhs[end + 2:]
    return rhs


def strip_escapes(rhs):
    """parseLine's escape pass: `\\\\` -> `\\`, `\\{` -> `{`, `\\}` -> `}`; the loop
    stops one character early, so a trailing backslash is kept."""
    out = list(rhs)
    i = 0
    while out and i < len(out) - 1:
        if out[i] != "\\":
            i += 1
            continue
        if out[i + 1] == "\\":
            del out[i]
            i += 1
            continue
        if out[i + 1] in "{}":
            del out[i]
            i -= 1
        i += 1
    return "".join(out)


# --------------------------------------------------------------------------
# state


class State:
    __slots__ = ("home", "variables", "rules", "categories", "ifs")

    def __init__(self, home):
        self.home = home
        self.variables = []
        self.rules = []
        self.categories = []
        self.ifs = []

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
        self.variables.sort(key=lambda kv: -len(kv[0]))


# --------------------------------------------------------------------------
# legacy workspace rule handler (ConfigManager.cpp handleWorkspaceRules +
# WorkspaceRuleManager replaceOrAdd + CWorkspaceRule::mergeLeft)


def new_rule():
    return {
        "workspaceString": "",
        "workspaceName": "",
        "workspaceId": WORKSPACE_INVALID,
        "enabled": True,
        "monitor": "",
        "isDefault": None,
        "isPersistent": None,
        "gapsIn": None,
        "gapsOut": None,
        "floatGaps": None,
        "borderSize": None,
        "noBorder": None,
        "noRounding": None,
        "decorate": None,
        "noShadow": None,
        "onCreatedEmpty": None,
        "defaultName": None,
        "layout": None,
        "layoutopts": {},
        "animationStyle": None,
    }


def workspace_name_for(selector):
    """The `name` member of getWorkspaceIDNameFromString(first_ident).

    Numeric selectors resolve to their own id text, `name:X` to X, `special:Y` to
    `special:Y`, `special` to `special:special`.  A literal that is neither a known
    prefix nor a number resolves no workspace at config time, so it takes
    std::to_string(WORKSPACE_INVALID).  State-only forms ("empty", "prev", "next",
    relative r+-/m+-/e+- selectors) are outside a static read."""
    if selector.startswith("special"):
        if len(selector) > 8:
            return "special:" + selector[8:]
        return "special:special"
    if selector.startswith("name:"):
        return selector[selector.find(":") + 1:]
    if selector.startswith("empty"):
        return ""
    if selector.startswith("prev"):
        return ""
    if selector == "next":
        return ""
    if len(selector) >= 3 and selector[0] == "r" and selector[1] in "-+~" and is_number(selector[2:]):
        return ""
    if len(selector) >= 3 and selector[0] in "me" and selector[1] in "-+~" and is_number(selector[2:]):
        return ""
    if selector[:1] in ("+", "-"):
        return ""
    if is_number(selector):
        value = cpp_stoi(selector)
        if value is None:
            return ""
        return str(max(value, 1))
    return str(WORKSPACE_INVALID)


def parse_gaps(payload):
    """CCssGapData::parseGapData over CVarList2(payload, 0, ' '): (top, right, bottom,
    left), or None where std::stoi throws."""
    args = cvarlist2(payload, " ", remove_empty=False)

    def as_int(index):
        if index >= len(args):
            return None
        return cpp_stoi(args[index])

    count = len(args)
    first = as_int(0)
    if count == 1:
        if first is None:
            return None
        return (first, first, first, first)
    second = as_int(1)
    if count == 2:
        if first is None or second is None:
            return None
        return (first, second, first, second)
    third = as_int(2)
    if count == 3:
        if first is None or second is None or third is None:
            return None
        return (first, second, third, second)
    values = [as_int(index) for index in range(4)]
    if any(value is None for value in values):
        return None
    return tuple(values)


def clean_cmd_for_workspace(name, dirty_cmd):
    """cleanCmdForWorkspace: `[workspace NAME] cmd`, or None for an empty command."""
    cmd = trim(dirty_cmd)
    if not cmd:
        return None
    workspace_rule = "workspace " + name
    if cmd[0] == "[":
        closing = cmd.rfind("]")
        if closing == -1:
            tmp_rules = cmd[1:]
            cmd = cmd[closing + 1:]
        else:
            tmp_rules = cmd[1:closing]
            cmd = cmd[closing + 1:]
        rules_list = cvarlist(tmp_rules, ";")
        had_workspace_rule = False
        for i, rule in enumerate(rules_list):
            if rule.startswith("workspace"):
                rules_list[i] = workspace_rule
                had_workspace_rule = True
        if not had_workspace_rule:
            rules_list.append(workspace_rule)
        rules = "[" + ";".join(rules_list) + "]"
    else:
        rules = "[" + workspace_rule + "]"
    return rules + " " + cmd


def assign_rule(field, rule, name):
    """One comma field, in handleWorkspaceRules' else-if order.

    Returns False where the C++ returns an error string (the whole line is dropped)."""
    delimiter = field.find("gapsin:")
    if delimiter != -1:
        gaps = parse_gaps(field[delimiter + 7:])
        if gaps is None:
            return False
        rule["gapsIn"] = gaps
        return True
    delimiter = field.find("gapsout:")
    if delimiter != -1:
        gaps = parse_gaps(field[delimiter + 8:])
        if gaps is None:
            return False
        rule["gapsOut"] = gaps
        return True
    delimiter = field.find("bordersize:")
    if delimiter != -1:
        value = cpp_stoi(field[delimiter + 11:])
        if value is None:
            return False
        rule["borderSize"] = value
        return True
    delimiter = field.find("border:")
    if delimiter != -1:
        value = parse_int(field[delimiter + 7:])
        if value is None:
            return False
        rule["noBorder"] = not value
        return True
    delimiter = field.find("shadow:")
    if delimiter != -1:
        value = parse_int(field[delimiter + 7:])
        if value is None:
            return False
        rule["noShadow"] = not value
        return True
    delimiter = field.find("rounding:")
    if delimiter != -1:
        value = parse_int(field[delimiter + 9:])
        if value is None:
            return False
        rule["noRounding"] = not value
        return True
    delimiter = field.find("decorate:")
    if delimiter != -1:
        value = parse_int(field[delimiter + 9:])
        if value is None:
            return False
        rule["decorate"] = bool(value)
        return True
    delimiter = field.find("monitor:")
    if delimiter != -1:
        rule["monitor"] = field[delimiter + 8:]
        return True
    delimiter = field.find("default:")
    if delimiter != -1:
        value = parse_int(field[delimiter + 8:])
        if value is None:
            return False
        rule["isDefault"] = bool(value)
        return True
    delimiter = field.find("persistent:")
    if delimiter != -1:
        value = parse_int(field[delimiter + 11:])
        if value is None:
            return False
        rule["isPersistent"] = bool(value)
        return True
    delimiter = field.find("defaultName:")
    if delimiter != -1:
        rule["defaultName"] = trim(field[delimiter + 12:])
        return True
    delimiter = field.find("on-created-empty:")
    if delimiter != -1:
        command = clean_cmd_for_workspace(name, field[delimiter + 16:])
        if command is None:
            return False
        rule["onCreatedEmpty"] = command
        return True
    delimiter = field.find("layoutopt:")
    if delimiter != -1:
        option = field[delimiter + 10:]
        colon = option.find(":")
        if colon == -1:
            return False
        rule["layoutopts"][option[:colon]] = option[colon + 1:]
        return True
    delimiter = field.find("layout:")
    if delimiter != -1:
        rule["layout"] = field[delimiter + 7:]
        return True
    delimiter = field.find("animation:")
    if delimiter != -1:
        rule["animationStyle"] = field[delimiter + 10:]
        return True
    return True


def merge_left(this, other):
    """CWorkspaceRule::mergeLeft: other's set fields overwrite this one's."""
    if other["monitor"]:
        this["monitor"] = other["monitor"]
    if not this["workspaceString"]:
        this["workspaceString"] = other["workspaceString"]
    if not this["workspaceName"]:
        this["workspaceName"] = other["workspaceName"]
    if this["workspaceId"] == WORKSPACE_INVALID:
        this["workspaceId"] = other["workspaceId"]
    for key in ("isDefault", "isPersistent", "gapsIn", "gapsOut", "borderSize",
                "noBorder", "noRounding", "decorate", "noShadow", "onCreatedEmpty",
                "defaultName", "layout", "animationStyle"):
        if other[key] is not None:
            this[key] = other[key]
    if other["floatGaps"] is not None:
        this["floatGaps"] = other["floatGaps"]
    for option, value in other["layoutopts"].items():
        this["layoutopts"][option] = value


def handle_workspace_rules(value, st):
    """ConfigManager::handleWorkspaceRules over one already-expanded RHS."""
    delimiter = value.find(",")
    if delimiter == -1:
        first_ident = trim(value)
        rules = value  # value.substr(npos + 1) wraps to substr(0)
    else:
        first_ident = trim(value[:delimiter])
        rules = value[delimiter + 1:]
    name = workspace_name_for(first_ident)
    rule = new_rule()
    rule["workspaceString"] = first_ident
    rule["workspaceName"] = name
    for field in cvarlist2(rules, ",", remove_empty=True):
        if not assign_rule(field, rule, name):
            return  # any error drops the whole line, before replaceOrAdd
    for existing in st.rules:
        if existing["enabled"] and existing["workspaceString"] == rule["workspaceString"]:
            merge_left(existing, rule)
            return
    st.rules.append(rule)


# --------------------------------------------------------------------------
# hyprlang parseLine / parseFile and the legacy source handler


def parse_comment(text, st):
    """`# hyprlang ...` directives: noerror (no effect here), if/endif nesting."""
    comment = trim(text)
    if not comment.startswith("hyprlang"):
        return
    args = comment.split()
    variable = None
    for i in range(1, len(args)):
        if args[i] == "noerror":
            return
        if args[i] == "endif":
            if st.ifs:
                st.ifs.pop()
            return
        if args[i] == "if":
            variable = args[i + 1] if i + 1 < len(args) else ""
            break
    if variable:
        negated = variable.startswith("!")
        if negated:
            variable = variable[1:]
        value = st.get_var(variable)
        if value is None:
            failed = not negated
        else:
            failed = _truthy(value) if negated else not _truthy(value)
        st.ifs.append(failed)


def _truthy(value):
    if value == "1":
        return True
    if value == "0":
        return False
    lower = value.lower()
    return lower.startswith("true") or lower.startswith("yes") or lower.startswith("on")


def absolute_path(rawpath, current_path):
    """helpers::absolutePath: leading '~' is HOME, else relative paths join the
    directory of the file being parsed."""
    idx = current_path.rfind("/")
    current_dir = current_path if idx == -1 else current_path[:idx]
    if rawpath[:1] == "~":
        return HOME[0] + rawpath[1:]
    if rawpath[:1] == "/":
        return rawpath
    if rawpath[:1] == ".":
        if rawpath[1:3] == "../":
            idx = current_dir.rfind("/")
            parent_dir = current_dir if idx == -1 else current_dir[:idx]
            return parent_dir + rawpath[2:]
        if rawpath[1:2] == "/":
            return current_dir + rawpath[1:]
    return current_dir + "/" + rawpath


def handle_source(rawpath, st, current_path):
    """ConfigManager::handleSource: glob, skip non-regular files, parse inline."""
    if len(rawpath) < 2:
        return
    pattern = absolute_path(rawpath, current_path)
    for match in sorted(globmodule.glob(pattern)):
        value = absolute_path(match, current_path)
        try:
            mode = os.stat(value).st_mode
        except OSError:
            return
        if not stat.S_ISREG(mode):
            continue
        parse_file(value, st)


def parse_line(line, st, current_path):
    """hyprlang parseLine over one logical line."""
    line = trim(line)
    pos = line.find("#")
    if pos == 0:
        parse_comment(line[1:], st)
        return
    if st.ifs and st.ifs[-1]:
        return
    last_hash = 0
    while pos != -1:
        if pos + 1 < len(line) and line[pos + 1] == "#":
            last_hash = pos + 2
            line = line[:pos + 1] + line[pos + 2:]
            pos = line.find("#", last_hash)
        else:
            line = line[:pos]
            break
    line = trim(line)
    if not line:
        return
    equals = line.find("=")
    if equals == -1 and not line.endswith("{") and line != "}":
        return
    if equals != -1:
        lhs = trim(line[:equals])
        rhs = trim(line[equals + 1:])
        if not lhs:
            return
        is_variable = lhs[0] == "$"
        for iteration in range(100):
            matched = False
            for name, value in st.variables:
                needle = "$" + name
                if not is_variable and needle in lhs:
                    lhs = lhs.replace(needle, value)
                    matched = True
                if needle in rhs:
                    rhs = rhs.replace(needle, value)
                    matched = True
            try:
                rhs = expand_expressions(rhs, st)
            except ExprError:
                return  # hyprlang rejects the line: no value, no handler
            if not matched:
                break
            if iteration == 99:
                return  # "Expanding variables exceeded max iteration limit"
        if is_variable:
            st.set_var(lhs[1:], rhs)
            return
        rhs = strip_escapes(rhs)
        if lhs == "workspace":
            handle_workspace_rules(rhs, st)
        elif lhs == "source":
            handle_source(rhs, st, current_path)
        return
    if "}" in line:
        if line != "}":
            return
        if st.categories:
            st.categories.pop()
        return
    if not line.endswith("{"):
        return
    st.categories.append(trim(line[:-1]))


def parse_file(path, st):
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError:
        return
    lines = data.decode("utf-8", "replace").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        idx += 1
        joined = True
        while line.endswith("\\"):
            cut = len(line) - 2
            while cut >= 0 and line[cut] in " \t":
                cut -= 1
            line = line[:cut + 1]
            if idx >= len(lines):
                joined = False
                break
            line += lines[idx]
            idx += 1
        if not joined:
            break
        parse_line(line, st, path)
    # hyprlang clears the category stack at the end of every parsed file
    st.categories = []


# --------------------------------------------------------------------------
# output


def rule_json(rule):
    """getWorkspaceRuleData, FORMAT_JSON: field order and omission as printed."""
    out = {"workspaceString": rule["workspaceString"], "enabled": rule["enabled"]}
    if rule["monitor"]:
        out["monitor"] = rule["monitor"]
    if rule["isDefault"] is not None:
        out["default"] = bool(rule["isDefault"])
    if rule["isPersistent"] is not None:
        out["persistent"] = bool(rule["isPersistent"])
    if rule["gapsIn"] is not None:
        out["gapsIn"] = list(rule["gapsIn"])
    if rule["gapsOut"] is not None:
        out["gapsOut"] = list(rule["gapsOut"])
    if rule["borderSize"] is not None:
        out["borderSize"] = rule["borderSize"]
    if rule["noBorder"] is not None:
        out["border"] = not rule["noBorder"]
    if rule["noRounding"] is not None:
        out["rounding"] = not rule["noRounding"]
    if rule["decorate"] is not None:
        out["decorate"] = bool(rule["decorate"])
    if rule["noShadow"] is not None:
        out["shadow"] = not rule["noShadow"]
    if rule["defaultName"] is not None:
        out["defaultName"] = rule["defaultName"]
    if rule["onCreatedEmpty"] is not None:
        out["onCreatedEmpty"] = rule["onCreatedEmpty"]
    return out


def main(argv):
    home = None
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--home" and i + 1 < len(argv):
            home = argv[i + 1]
            i += 2
            continue
        if arg.startswith("--home="):
            home = arg[len("--home="):]
        i += 1
    if not home:
        sys.stderr.write("usage: mado-wsrules.py --home DIR\n")
        return 2
    HOME[0] = os.path.abspath(home)
    st = State(HOME[0])
    root = os.path.join(HOME[0], ".config", "hypr", "hyprland.conf")
    if os.path.exists(root):
        parse_file(os.path.realpath(root), st)
    sys.stdout.write(json.dumps([rule_json(rule) for rule in st.rules]))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
