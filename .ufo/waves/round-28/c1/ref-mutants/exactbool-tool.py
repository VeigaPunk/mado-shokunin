#!/usr/bin/env python3
"""mado-wsrules.py - workspace rule table from config bytes (Hyprland v0.56.2).

Prints, on stdout, the JSON array that Hyprland v0.56.2 prints for
`hyprctl workspacerules -j`, derived only from the bytes of the config tree
rooted at <home>/.config/hypr/hyprland.conf.

This is the round-27 C1 data rule, implemented independently from the pinned
sources:

  * hyprlang 0.6.8 (src/config.cpp)
      - getNextLine: a trailing backslash continues the line,
      - parseLine: comments (`#`, `##` escapes), the `$name = value`
        variable table (one shared table, a redefinition takes effect from
        that line on), `{{ expr }}` single operator float expressions,
        variable expansion before the value is handed to a handler,
      - parseFile: a failing line does not stop the file.
  * Hyprland v0.56.2 (efb5099)
      - src/config/legacy/ConfigManager.cpp
          - handleWorkspaceRules: the legacy `workspace = SELECTOR, RULES`
            keyword; the selector is the first comma field, the rest are
            rule items matched against a fixed key order by substring search,
          - handleSource: glob based `source =`, relative to the sourcing
            file, non regular files skipped,
      - src/config/shared/workspace/WorkspaceRule.cpp / WorkspaceRuleManager.cpp
          - mergeLeft / replaceOrAdd: one row per exact trimmed selector,
            first seen order kept, later lines overwrite only the fields
            they set,
      - src/config/shared/parserUtils/ParserUtils.cpp: parseInt,
      - src/config/shared/complex/ComplexDataTypes.hpp: parseGapData,
      - src/helpers/MiscFunctions.cpp: getWorkspaceIDNameFromString,
        cleanCmdForWorkspace, absolutePath,
      - src/debug/HyprCtl.cpp: getWorkspaceRuleData (the printed fields).

Python 3 standard library only.
"""

import argparse
import glob as globmod
import json
import os
import re
import struct
import sys

# --------------------------------------------------------------------------
# small helpers with C++ semantics
# --------------------------------------------------------------------------

_SPACE = " \t\n\v\f\r"


def c_isspace(ch):
    """C locale isspace()."""
    return ch in _SPACE


def trim(s):
    """Hyprutils::String::trim - strip leading and trailing whitespace."""
    i = 0
    n = len(s)
    while i < n and c_isspace(s[i]):
        i += 1
    j = n
    while j > i and c_isspace(s[j - 1]):
        j -= 1
    return s[i:j]


def is_number(s):
    """Hyprutils::String::isNumber2 - an optional leading '-' and digits."""
    if not s:
        return False
    for i, c in enumerate(s):
        if i == 0 and c == "-":
            continue
        if c not in "0123456789":
            return False
    return s[-1] in "0123456789"


def c_stoi(s):
    """std::stoi - leading whitespace, optional sign, digits, rest ignored.

    Raises ValueError when there is no conversion (std::invalid_argument) or
    when the value does not fit into an int (std::out_of_range).
    """
    i = 0
    n = len(s)
    while i < n and c_isspace(s[i]):
        i += 1
    j = i
    if j < n and s[j] in "+-":
        j += 1
    k = j
    while k < n and s[k] in "0123456789":
        k += 1
    if k == j:
        raise ValueError("stoi")
    value = int(s[i:k])
    if value < -2 ** 31 or value > 2 ** 31 - 1:
        raise ValueError("stoi out of range")
    return value


def str_to_int64(s):
    """Hyprutils::String::strToNumber<int64_t> - strict, no trailing junk."""
    if not s:
        raise ValueError("empty")
    body = s
    if body[0] == "-":
        body = body[1:]
    if not body or not all(c in "0123456789" for c in body):
        raise ValueError("bad integer")
    value = int(s)
    if value < -(2 ** 63) or value > 2 ** 63 - 1:
        raise ValueError("out of range")
    return value


def str_to_uint64_hex(s):
    """Hyprutils::String::strToNumber<uint64_t> for a 0x literal."""
    body = s[2:] if s[:2].lower() == "0x" else s
    if not body or not all(c in "0123456789abcdefABCDEF" for c in body):
        raise ValueError("bad hex")
    value = int(body, 16)
    if value > 2 ** 64 - 1:
        raise ValueError("out of range")
    return value


def parse_int(value):
    """Intentional exact-alias boolean mutant; non-boolean integer parsing is unchanged."""
    if value in ("true", "yes", "on", "1"):
        return 1
    if value in ("false", "no", "off", "0"):
        return 0
    if value.startswith("0x"):
        return str_to_uint64_hex(value)
    return str_to_int64(value)


def format_float(value):
    """std::format("{}", float) - the shortest form that round trips."""
    try:
        single = struct.unpack("<f", struct.pack("<f", value))[0]
    except (OverflowError, ValueError):
        return str(value)
    for precision in range(1, 10):
        text = "%.*g" % (precision, single)
        try:
            if struct.unpack("<f", struct.pack("<f", float(text)))[0] == single:
                break
        except (OverflowError, ValueError):
            continue
    else:
        text = repr(single)
    if "e" in text:
        # std::format only uses the exponent form for very large or small
        # magnitudes; expand it where the plain form is the C++ choice.
        mantissa, _, exponent = text.partition("e")
        power = int(exponent)
        if -4 <= power < 17:
            text = "%.*f" % (max(0, 17 - power - len(mantissa.split(".")[0])), single)
            text = text.rstrip("0").rstrip(".") if "." in text else text
    return text


def cvar_list2(text, delim=",", remove_empty=False, allow_escape=True):
    """Hyprutils::String::CVarList2 - split, trim every field."""
    if not text:
        return []
    args = []
    arg_begin = 0
    escaped_indices = []

    def is_delimiter(ch):
        return c_isspace(ch) if delim == "s" else ch == delim

    i = 0
    n = len(text)
    while i < n:
        if not is_delimiter(text[i]):
            i += 1
            continue
        broke = True
        if allow_escape and (i - arg_begin) != 0:
            previous = text[i - 1]
            if (i - arg_begin) == 1:
                if previous == "\\":
                    escaped_indices.append(i - arg_begin - 1)
                    broke = False
            else:
                if previous == "\\":
                    escaped_indices.append(i - arg_begin - 1)
                    if text[i - 2] != "\\":
                        broke = False
        if broke:
            if not escaped_indices:
                field = trim(text[arg_begin:i])
                if field or not remove_empty:
                    args.append(field)
            else:
                copy = text[arg_begin:i]
                for k, index in enumerate(escaped_indices):
                    copy = copy[: index - k] + copy[index - k + 1:]
                args.append(trim(copy))
            arg_begin = i + 1
            escaped_indices = []
        i += 1

    if arg_begin < n:
        if not escaped_indices:
            field = trim(text[arg_begin:])
            if field or not remove_empty:
                args.append(field)
        else:
            copy = text[arg_begin:]
            for k, index in enumerate(escaped_indices):
                copy = copy[: index - k] + copy[index - k + 1:]
            args.append(trim(copy))
    return args


# --------------------------------------------------------------------------
# the workspace rule table
# --------------------------------------------------------------------------

# the fields getWorkspaceRuleData prints, in the order it prints them
PRINT_ORDER = [
    "workspaceString",
    "enabled",
    "monitor",
    "default",
    "persistent",
    "gapsIn",
    "gapsOut",
    "borderSize",
    "border",
    "rounding",
    "decorate",
    "shadow",
    "defaultName",
    "onCreatedEmpty",
]

# the legacy handler looks the key up with its colon and takes the value from
# directly behind it
ON_CREATED_EMPTY = "on-created-empty:"


class RuleError(Exception):
    """A rule could not be parsed - the whole `workspace =` line is dropped."""


class Rule(object):
    """One row of the workspace rule table (mirrors Config::CWorkspaceRule)."""

    __slots__ = (
        "workspaceString",
        "monitor",
        "isDefault",
        "isPersistent",
        "gapsIn",
        "gapsOut",
        "borderSize",
        "noBorder",
        "noRounding",
        "decorate",
        "noShadow",
        "onCreatedEmpty",
        "defaultName",
    )

    def __init__(self):
        self.workspaceString = ""
        self.monitor = ""
        self.isDefault = None
        self.isPersistent = None
        self.gapsIn = None
        self.gapsOut = None
        self.borderSize = None
        self.noBorder = None
        self.noRounding = None
        self.decorate = None
        self.noShadow = None
        self.onCreatedEmpty = None
        self.defaultName = None

    def merge_left(self, other):
        """Config::CWorkspaceRule::mergeLeft - take over what `other` sets."""
        if other.monitor:
            self.monitor = other.monitor
        if not self.workspaceString:
            self.workspaceString = other.workspaceString
        if other.isDefault is not None:
            self.isDefault = other.isDefault
        if other.isPersistent is not None:
            self.isPersistent = other.isPersistent
        if other.gapsIn is not None:
            self.gapsIn = other.gapsIn
        if other.gapsOut is not None:
            self.gapsOut = other.gapsOut
        if other.borderSize is not None:
            self.borderSize = other.borderSize
        if other.noBorder is not None:
            self.noBorder = other.noBorder
        if other.noRounding is not None:
            self.noRounding = other.noRounding
        if other.decorate is not None:
            self.decorate = other.decorate
        if other.noShadow is not None:
            self.noShadow = other.noShadow
        if other.onCreatedEmpty is not None:
            self.onCreatedEmpty = other.onCreatedEmpty
        if other.defaultName is not None:
            self.defaultName = other.defaultName

    def to_json(self):
        row = {"workspaceString": self.workspaceString, "enabled": True}
        if self.monitor:
            row["monitor"] = self.monitor
        if self.isDefault is not None:
            row["default"] = self.isDefault
        if self.isPersistent is not None:
            row["persistent"] = self.isPersistent
        if self.gapsIn is not None:
            row["gapsIn"] = list(self.gapsIn)
        if self.gapsOut is not None:
            row["gapsOut"] = list(self.gapsOut)
        if self.borderSize is not None:
            row["borderSize"] = self.borderSize
        if self.noBorder is not None:
            row["border"] = not self.noBorder
        if self.noRounding is not None:
            row["rounding"] = not self.noRounding
        if self.decorate is not None:
            row["decorate"] = self.decorate
        if self.noShadow is not None:
            row["shadow"] = not self.noShadow
        if self.defaultName is not None:
            row["defaultName"] = self.defaultName
        if self.onCreatedEmpty is not None:
            row["onCreatedEmpty"] = self.onCreatedEmpty
        return row


# --------------------------------------------------------------------------
# the config reader
# --------------------------------------------------------------------------


class ConfigReader(object):
    """Reads a config tree the way the pinned Hyprland does."""

    def __init__(self, home):
        self.home = home
        # hyprlang's variable table starts out as the environment
        self.variables = dict(os.environ)
        self.rules = []
        self.stack = []

    # -- the variable table ------------------------------------------------

    def _variable_names(self):
        # hyprlang keeps the variables sorted by name length, longest first,
        # so that a longer name is substituted before a shorter prefix of it
        return sorted(self.variables, key=lambda name: (-len(name), name))

    def _expand(self, lhs, rhs, is_variable):
        """hyprlang's variable and expression expansion."""
        for _ in range(100):
            matched = False
            for name in self._variable_names():
                token = "$" + name
                value = self.variables[name]
                if not is_variable and token in lhs:
                    lhs = lhs.replace(token, value)
                    matched = True
                if token in rhs:
                    rhs = rhs.replace(token, value)
                    matched = True
            rhs = self._expand_expressions(rhs)
            if not matched:
                break
        return lhs, rhs

    def _expand_expressions(self, rhs):
        """`{{ expr }}` - a single operator float expression."""
        while "{{" in rhs:
            begin = -1
            position = 0
            while True:
                candidate = rhs.find("{{", position)
                if candidate < 0:
                    break
                backslashes = 0
                for k in range(candidate - 1, -1, -1):
                    if rhs[k] != "\\":
                        break
                    backslashes += 1
                if backslashes % 2 == 0:
                    begin = candidate
                    break
                position = candidate + 1
            if begin < 0:
                break
            end = rhs.find("}}", begin + 2)
            if end < 0:
                break
            rhs = rhs[:begin] + format_float(self._evaluate(rhs[begin + 2:end])) + rhs[end + 2:]
        return rhs

    def _evaluate(self, body):
        """CConfigImpl::parseExpression."""
        args = [a for a in re.split(r"[ \t\n\v\f\r]+", body) if a]
        if len(args) < 3 or args[1] not in ("+", "-", "*", "/"):
            raise RuleError("Invalid expression type: supported +, -, *, /")
        left = self._operand(args[0])
        right = self._operand(args[2])
        try:
            if args[1] == "+":
                return left + right
            if args[1] == "-":
                return left - right
            if args[1] == "*":
                return left * right
            if right == 0:
                if left == 0:
                    return float("nan")
                return float("inf") if left > 0 else float("-inf")
            return left / right
        except (OverflowError, ZeroDivisionError):
            raise RuleError("Failed to parse expression")

    def _operand(self, token):
        if token in self.variables:
            try:
                return float(self.variables[token])
            except ValueError:
                raise RuleError("Failed to parse expression: value holds a "
                                "variable that does not look like a number")
        try:
            return float(token)
        except ValueError:
            raise RuleError("Failed to parse expression: value does not look "
                            "like a number or the variable doesn't exist")

    # -- lines -------------------------------------------------------------

    @staticmethod
    def _strip_comment(line):
        """hyprlang's comment handling: `##` is an escaped `#`."""
        comment_pos = line.find("#")
        if comment_pos == 0:
            return None  # the whole line is a comment
        last_hash_pos = 0
        while comment_pos != -1:
            escaped = False
            if comment_pos < len(line) - 1 and line[comment_pos + 1] == "#":
                last_hash_pos = comment_pos + 2
                escaped = True
            if not escaped:
                return line[:comment_pos]
            line = line[: comment_pos + 1] + line[comment_pos + 2:]
            comment_pos = line.find("#", last_hash_pos)
        return line

    @staticmethod
    def _logical_lines(text):
        """hyprlang's getNextLine: a trailing backslash continues the line."""
        raw = text.split("\n")
        out = []
        i = 0
        while i < len(raw):
            line = raw[i]
            i += 1
            while line.endswith("\\"):
                stripped = line[:-1].rstrip(" \t")
                if i >= len(raw):
                    line = stripped
                    break
                line = stripped + raw[i]
                i += 1
            out.append(line)
        return out

    def parse_line(self, line, current_path):
        """One logical line of a config file."""
        line = trim(line)
        stripped = self._strip_comment(line)
        if stripped is None:
            return
        line = trim(stripped)
        if not line:
            return
        equals = line.find("=")
        if equals < 0 and not line.endswith("{") and line != "}":
            return  # "Invalid config line"
        if equals < 0:
            return  # a category open or close
        lhs = trim(line[:equals])
        rhs = trim(line[equals + 1:])
        if not lhs:
            return  # "Empty lhs."
        is_variable = lhs.startswith("$")
        try:
            lhs, rhs = self._expand(lhs, rhs, is_variable)
        except RuleError:
            return
        if is_variable:
            self.variables[lhs[1:]] = rhs
            return
        rhs = self._strip_escapes(rhs)
        if lhs == "workspace":
            try:
                self._handle_workspace_rule(rhs)
            except RuleError:
                return
        elif lhs == "source":
            try:
                self._handle_source(rhs, current_path)
            except RuleError:
                return

    @staticmethod
    def _strip_escapes(rhs):
        """hyprlang removes the escape chars before '{', '}' and '\\'."""
        out = []
        i = 0
        n = len(rhs)
        while i < n:
            ch = rhs[i]
            if ch == "\\" and i + 1 < n:
                following = rhs[i + 1]
                if following == "\\":
                    out.append(following)
                    i += 2
                    continue
                if following in "{}":
                    out.append(following)
                    i += 2
                    continue
            out.append(ch)
            i += 1
        return "".join(out)

    # -- `source =` --------------------------------------------------------

    def _absolute_path(self, rawpath, current_path):
        """Helpers::absolutePath."""
        value = rawpath
        if value.startswith("~"):
            return self.home + value[1:]
        if value.startswith("/"):
            return value
        current_dir = current_path.rsplit("/", 1)[0] if "/" in current_path else current_path
        if value.startswith("../"):
            parent = current_dir.rsplit("/", 1)[0] if "/" in current_dir else current_dir
            return parent + value[2:]
        if value.startswith("./"):
            return current_dir + value[1:]
        return current_dir + "/" + value

    def _handle_source(self, rawpath, current_path):
        if len(rawpath) < 2:
            raise RuleError("source= path garbage")
        pattern = self._absolute_path(rawpath, current_path)
        matches = sorted(globmod.glob(pattern))
        if not matches:
            raise RuleError("source= globbing error: found no match")
        for match in matches:
            value = self._absolute_path(match, current_path)
            if not os.path.isfile(value):
                continue  # directories and other non regular files are skipped
            self.parse_file(value)

    # -- `workspace =` -----------------------------------------------------

    def _handle_workspace_rule(self, value):
        """CConfigManager::handleWorkspaceRules."""
        delim = value.find(",")
        if delim < 0:
            first_ident = trim(value)
            rules = value
        else:
            first_ident = trim(value[:delim])
            rules = value[delim + 1:]
        rule = Rule()
        rule.workspaceString = first_ident
        for field in cvar_list2(rules, ",", remove_empty=True):
            self._assign_rule(rule, field, first_ident)
        self._replace_or_add(rule)

    def _replace_or_add(self, rule):
        """CWorkspaceRuleManager::replaceOrAdd."""
        for existing in self.rules:
            if existing.workspaceString == rule.workspaceString:
                existing.merge_left(rule)
                return
        self.rules.append(rule)

    def _assign_rule(self, rule, field, first_ident):
        """The legacy assignRule chain - the first key that occurs in the field
        wins, the value is what follows the key."""
        if "gapsin:" in field:
            delim = field.find("gapsin:")
            rule.gapsIn = self._parse_gap_data(field[delim + 7:])
        elif "gapsout:" in field:
            delim = field.find("gapsout:")
            rule.gapsOut = self._parse_gap_data(field[delim + 8:])
        elif "bordersize:" in field:
            delim = field.find("bordersize:")
            try:
                rule.borderSize = c_stoi(field[delim + 11:])
            except ValueError:
                raise RuleError("Error parsing workspace rule bordersize")
        elif "border:" in field:
            delim = field.find("border:")
            rule.noBorder = not self._parse_bool(field[delim + 7:])
        elif "shadow:" in field:
            delim = field.find("shadow:")
            rule.noShadow = not self._parse_bool(field[delim + 7:])
        elif "rounding:" in field:
            delim = field.find("rounding:")
            rule.noRounding = not self._parse_bool(field[delim + 9:])
        elif "decorate:" in field:
            delim = field.find("decorate:")
            rule.decorate = self._parse_bool(field[delim + 9:])
        elif "monitor:" in field:
            delim = field.find("monitor:")
            rule.monitor = field[delim + 8:]
        elif "default:" in field:
            delim = field.find("default:")
            rule.isDefault = self._parse_bool(field[delim + 8:])
        elif "persistent:" in field:
            delim = field.find("persistent:")
            rule.isPersistent = self._parse_bool(field[delim + 11:])
        elif "defaultName:" in field:
            delim = field.find("defaultName:")
            rule.defaultName = trim(field[delim + 12:])
        elif ON_CREATED_EMPTY in field:
            delim = field.find(ON_CREATED_EMPTY)
            rule.onCreatedEmpty = self._clean_cmd_for_workspace(
                self._workspace_name(first_ident), field[delim + len(ON_CREATED_EMPTY):])
        elif "layoutopt:" in field:
            delim = field.find("layoutopt:")
            opt = field[delim + 10:]
            if ":" not in opt:
                raise RuleError("Invalid workspace rule found: " + field)
            # stored in the rule, but never printed
        elif "layout:" in field:
            pass  # stored in the rule, but never printed
        elif "animation:" in field:
            pass  # stored in the rule, but never printed

    @staticmethod
    def _parse_bool(value):
        try:
            return parse_int(value) != 0
        except ValueError:
            raise RuleError("Failed parsing a workspace rule")

    @staticmethod
    def _parse_gap_data(payload):
        """CCssGapData::parseGapData over a CVarList2 of the payload."""
        varlist = cvar_list2(payload, " ", remove_empty=False)

        def to_int(index):
            token = varlist[index] if index < len(varlist) else ""
            try:
                return c_stoi(token)
            except ValueError:
                raise RuleError("Error parsing workspace rule gaps")

        if len(varlist) == 1:
            value = to_int(0)
            return (value, value, value, value)
        if len(varlist) == 2:
            return (to_int(0), to_int(1), to_int(0), to_int(1))
        if len(varlist) == 3:
            return (to_int(0), to_int(1), to_int(2), to_int(1))
        if len(varlist) == 4:
            return (to_int(0), to_int(1), to_int(2), to_int(3))
        # too many arguments (or none): the first four win, the rest are
        # never converted
        return (to_int(0), to_int(1), to_int(2), to_int(3))

    @staticmethod
    def _workspace_name(selector):
        """getWorkspaceIDNameFromString(selector).name, for `on-created-empty:`.

        The pinned resolver runs in this order: `special`, `name:`, `empty`,
        `prev`, `next`, the relative `r±`/`m±`/`e±` forms, then the numeric
        and plain name cases.  Every branch that would need the live
        compositor resolves to {WORKSPACE_INVALID} while the config is being
        parsed (there is no monitor yet), and that value carries an empty
        name - so `empty`, `prev`, `next`, the relative forms and the `+`/`-`
        forms all print an empty name.
        """
        if selector.startswith("special"):
            if len(selector) > 8:
                return "special:" + selector[8:]
            return "special:special"
        if selector.startswith("name:"):
            return selector[selector.find(":") + 1:]
        if selector.startswith("empty"):
            return ""  # the empty workspace carries no name
        if selector.startswith("prev"):
            return ""  # no monitor yet: the previous workspace is invalid
        if selector == "next":
            return ""  # no monitor yet: the next workspace is invalid
        if len(selector) >= 3 and selector[0] == "r" and selector[1] in "-+~" and is_number(selector[2:]):
            return ""  # relative to the active workspace: invalid while parsing
        if len(selector) >= 3 and selector[0] in "me" and selector[1] in "-+~" and is_number(selector[2:]):
            return ""  # relative to the active monitor: invalid while parsing
        if selector[:1] in ("+", "-"):
            return ""  # relative to the active workspace: invalid while parsing
        if is_number(selector):
            try:
                return str(max(int(selector), 1))
            except ValueError:
                return "-1"
        # a plain name that no workspace carries: the unresolved id
        return "-1"

    @staticmethod
    def _clean_cmd_for_workspace(workspace_name, dirty_cmd):
        """Helpers::cleanCmdForWorkspace."""
        cmd = trim(dirty_cmd)
        if not cmd:
            # nullopt -> the CHECK_OR_THROW in the legacy handler drops the
            # whole `workspace =` line
            raise RuleError("Failed parsing a workspace rule")
        workspace_rule = "workspace " + workspace_name
        if cmd.startswith("["):
            closing = cmd.rfind("]")
            if closing < 0:
                # find_last_of returns npos: substr(1, npos - 1) clamps to the
                # end, and substr(npos + 1) is substr(0), the whole command
                tmp_rules = cmd[1:]
                cmd = cmd
            else:
                tmp_rules = cmd[1:closing]
                cmd = cmd[closing + 1:]
            rules = cvar_list2(tmp_rules, ";")
            had_workspace_rule = False
            for index, entry in enumerate(rules):
                if entry.startswith("workspace"):
                    rules[index] = workspace_rule
                    had_workspace_rule = True
            if not had_workspace_rule:
                rules.append(workspace_rule)
            rules_str = "[" + ";".join(rules) + "]"
        else:
            rules_str = "[" + workspace_rule + "]"
        return rules_str + " " + cmd

    # -- files -------------------------------------------------------------

    def parse_file(self, path):
        """Read one config file."""
        if path in self.stack:
            return  # a source cycle would recurse forever
        try:
            with open(path, "rb") as handle:
                data = handle.read()
        except OSError:
            return
        text = data.decode("utf-8", "surrogateescape")
        self.stack.append(path)
        try:
            for line in self._logical_lines(text):
                self.parse_line(line, path)
        finally:
            self.stack.pop()


# --------------------------------------------------------------------------
# output, byte for byte what hyprctl workspacerules -j prints
# --------------------------------------------------------------------------


def escape_json_strings(text):
    out = []
    for ch in text:
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif "\x00" <= ch <= "\x1f":
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)


def render(rules):
    """The exact text `hyprctl workspacerules -j` prints."""
    parts = []
    for rule in rules:
        row = rule.to_json()
        body = '    "workspaceString": "%s"' % escape_json_strings(row["workspaceString"])
        body += ',\n    "enabled": %s' % ("true" if row["enabled"] else "false")
        for key in PRINT_ORDER[2:]:
            if key not in row:
                continue
            value = row[key]
            if isinstance(value, bool):
                text = "true" if value else "false"
            elif isinstance(value, int):
                text = str(value)
            elif isinstance(value, list):
                text = "[%d, %d, %d, %d]" % tuple(value)
            else:
                text = '"%s"' % escape_json_strings(value)
            body += ',\n    "%s": %s' % (key, text)
        parts.append("{\n%s\n}" % body)
    return "[" + ",".join(parts) + "]"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Print the workspace rule table Hyprland v0.56.2 builds for "
                    "the config tree under --home.")
    parser.add_argument("--home", required=True,
                        help="the home directory of the config tree")
    args = parser.parse_args(argv)

    home = os.path.abspath(args.home)
    reader = ConfigReader(home)
    root = os.path.join(home, ".config", "hypr", "hyprland.conf")
    if os.path.isfile(root):
        reader.parse_file(root)
    sys.stdout.write(render(reader.rules))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
